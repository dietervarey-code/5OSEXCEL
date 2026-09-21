'use client';

import { useEffect, useRef, useState } from 'react';
import '@univerjs/presets/lib/styles/preset-sheets-core.css';
import type { WerkmapData, CelInzending } from '@/lib/werkblad-types';
import { positieNaarCel } from '@/lib/werkblad-types';
import { NL_FUNCTIES } from '@/lib/nl-functies';
import { vertaalScheidingstekens } from '@/lib/formules';

type Props = {
  werkmap: WerkmapData;
  /** Wordt aangeroepen zodra het werkblad klaar is; geeft een leesfunctie terug. */
  opGereed: (lees: () => CelInzending[]) => void;
  opWijziging?: () => void;
};

/**
 * Het rekenblad zelf. Univer draait volledig client-side op een canvas, dus dit
 * component mag nooit server-side gerenderd worden (zie dynamic import in
 * OefeningWerkruimte).
 */
export default function Werkblad({ werkmap, opGereed, opWijziging }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const [fout, setFout] = useState<string | null>(null);
  const [bezig, setBezig] = useState(true);

  // In refs, want de effect-hook mag maar één keer draaien: Univer opnieuw
  // opstarten zou het werk van de leerling wissen.
  const opGereedRef = useRef(opGereed);
  const opWijzigingRef = useRef(opWijziging);
  opGereedRef.current = opGereed;
  opWijzigingRef.current = opWijziging;

  useEffect(() => {
    if (!container.current) return;
    let opruimen: (() => void) | undefined;
    let afgebroken = false;

    (async () => {
      try {
        const [{ createUniver, defaultTheme, LocaleType, merge }, { UniverSheetsCorePreset }, locale] =
          await Promise.all([
            import('@univerjs/presets'),
            import('@univerjs/presets/preset-sheets-core'),
            import('@univerjs/presets/preset-sheets-core/locales/en-US'),
          ]);
        if (afgebroken || !container.current) return;

        const { univer, univerAPI } = createUniver({
          locale: LocaleType.EN_US,
          locales: { [LocaleType.EN_US]: merge({}, locale.default) },
          theme: defaultTheme,
          presets: [
            UniverSheetsCorePreset({
              container: container.current,
              footer: { sheetBar: true, statisticBar: true },
            }),
          ],
        });

        /**
         * Nederlandse functienamen registreren.
         *
         * Dit kan pas als Univer de levenscyclusfase Rendered bereikt heeft: daarvoor
         * bestaat IRegisterFunctionService nog niet en gooit de injector een fout,
         * waardoor elke formule uit de cursus #NAME? zou geven.
         */
        function registreerNederlandseFuncties() {
          const formule = univerAPI.getFormula();
          const nietGelukt: string[] = [];
          for (const { naam, fn, uitleg } of NL_FUNCTIES) {
            try {
              formule.registerFunction(naam, fn as never, uitleg);
            } catch (e) {
              nietGelukt.push(`${naam} (${e instanceof Error ? e.message : 'onbekend'})`);
            }
          }
          if (nietGelukt.length) {
            console.warn('[5OS] Niet-registreerbare functienamen:', nietGelukt.join(', '));
          }
          return nietGelukt.length === 0;
        }

        let geregistreerd = false;
        univerAPI.addEvent(univerAPI.Event.LifeCycleChanged, ({ stage }: { stage: number }) => {
          // 3 = LifecycleStages.Rendered
          if (!geregistreerd && stage >= 3) {
            geregistreerd = registreerNederlandseFuncties();
          }
        });

        /**
         * Puntkomma's omzetten naar komma's nadat de leerling een cel verlaat.
         *
         * De cursus schrijft =ALS(B5>100;"ja";"nee"). De rekenmachine verwacht
         * komma's en geeft bij puntkomma's géén fout maar een verkeerd antwoord
         * (=SOM(1;2;3) levert 0 op). Een leerling ziet niet wat er scheelt.
         *
         * We laten de invoer gewoon doorgaan en corrigeren daarna. Eerder
         * annuleerden we de bewerking en schreven we ze zelf weg, maar dan raakte
         * de eerstvolgende cel die de leerling invulde zoek.
         */
        univerAPI.addEvent(univerAPI.Event.SheetEditEnded, (params) => {
          const { row, column, worksheet, isConfirm } = params as unknown as {
            row: number;
            column: number;
            isConfirm: boolean;
            worksheet: {
              getRange: (r: number, k: number) => {
                getFormula: () => string;
                setValue: (v: unknown) => void;
              };
            };
          };
          if (!isConfirm) return;

          try {
            const cel = worksheet.getRange(row, column);
            const formule = cel.getFormula();
            if (!formule) return;

            const vertaald = vertaalScheidingstekens(formule);
            if (vertaald !== formule) cel.setValue({ f: vertaald });
          } catch (e) {
            console.warn('[5OS] formule vertalen mislukte:', e);
          }
        });

        univerAPI.createWorkbook(werkmap as never);

        // Vangnet: als de levenscyclusfase al voorbij was toen we ons abonneerden.
        if (!geregistreerd) {
          setTimeout(() => {
            if (!geregistreerd) geregistreerd = registreerNederlandseFuncties();
          }, 1000);
        }

        if (opWijzigingRef.current) {
          univerAPI.addEvent(univerAPI.Event.SheetValueChanged, () => opWijzigingRef.current?.());
        }

        /** Leest het gebruikte bereik uit en levert waarde, formule en getalnotatie per cel. */
        function lees(): CelInzending[] {
          const werkboek = univerAPI.getActiveWorkbook();

          // Bewust NIET het actieve blad: heeft een oefening meerdere bladen en
          // staat de leerling op een ander tabblad wanneer die op Nakijken klikt,
          // dan zouden we het verkeerde blad nakijken. We lezen altijd het eerste
          // blad uit de opgave — daar staan de antwoorden.
          const hoofdblad = werkmap.sheets[werkmap.sheetOrder[0]];
          const blad = werkboek?.getSheetByName(hoofdblad.name) ?? werkboek?.getActiveSheet();
          if (!blad) return [];

          const laatsteRij = Math.min(hoofdblad.rowCount, 60);
          const laatsteKolom = Math.min(hoofdblad.columnCount, 20);
          const bereik = blad.getRange(0, 0, laatsteRij, laatsteKolom);

          // getValues() levert de OPGEMAAKTE tekst zodra er een getalnotatie op
          // staat ("$3,253.40 "). getRawValues() geeft het onderliggende getal.
          // We sturen allebei mee: de server rekent met het getal en gebruikt de
          // tekst alleen als terugval.
          const waarden = bereik.getValues();
          const ruwe = bereik.getRawValues();
          const formules = bereik.getFormulas();
          const notaties = bereik.getNumberFormats();
          const stijlen = bereik.getCellStyles();

          const cellen: CelInzending[] = [];
          for (let r = 0; r < laatsteRij; r++) {
            for (let k = 0; k < laatsteKolom; k++) {
              const waarde = waarden?.[r]?.[k] ?? null;
              const formuleTekst = formules?.[r]?.[k] || null;
              if ((waarde === null || waarde === '') && !formuleTekst) continue;

              const ruw = ruwe?.[r]?.[k];

              cellen.push({
                cel: positieNaarCel(r, k),
                waarde: waarde as CelInzending['waarde'],
                ruweWaarde: (typeof ruw === 'object' && ruw !== null ? undefined : ruw) as CelInzending['ruweWaarde'],
                formule: formuleTekst,
                opmaak: {
                  vet: Boolean((stijlen?.[r]?.[k] as { bl?: number } | undefined)?.bl),
                  getalnotatie: notaties?.[r]?.[k] ?? '',
                },
              });
            }
          }
          return cellen;
        }

        opGereedRef.current(lees);
        setBezig(false);
        opruimen = () => univer.dispose();
      } catch (e) {
        console.error(e);
        setFout(e instanceof Error ? e.message : 'Het rekenblad kon niet geladen worden.');
        setBezig(false);
      }
    })();

    return () => {
      afgebroken = true;
      opruimen?.();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ position: 'relative', height: '100%', width: '100%' }}>
      {bezig && (
        <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', zIndex: 2 }}>
          <span className="gedempt">Rekenblad laden…</span>
        </div>
      )}
      {fout && (
        <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', zIndex: 3, padding: '1rem' }}>
          <div className="melding fout">{fout}</div>
        </div>
      )}
      <div ref={container} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}
