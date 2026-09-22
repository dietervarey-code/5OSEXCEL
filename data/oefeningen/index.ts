import { factuurOpgave } from './factuur.opgave';
import { voorraadOpgave } from './01-voorraad';
import { prijslijstOpgave } from './02-prijslijst';
import { verkoopOpgave } from './03-verkoopcijfers';
import { bestellingenOpgave } from './04-bestellingen';
import { klantenOpgave } from './05-klanten';
import { xzoekenOpgave } from './06-xzoeken';
import { genesteOpgave } from './07-geneste';
import { getalnotatieOpgave } from './f1-01-getalnotatie';
import { tabelOpgave } from './f1-02-tabel';
import { sorterenOpgave } from './f1-03-sorteren';
import { vastzettenOpgave } from './f1-04-vastzetten';
import { transponerenOpgave } from './f1-05-transponeren';
import {
  bladenOphalenOpgave, bladenFiliaalOpgave, bladenVerschilOpgave,
  bladenGemiddeldeOpgave, bladenZoekenOpgave,
} from './f5-bladen';
import {
  koppelenPrijzenOpgave, koppelenZoekenOpgave, koppelenConsoliderenOpgave,
  koppelenHerstellenOpgave, koppelenFactuurOpgave,
} from './f6-koppelen';
import { horizZoekenOpgave, tekstOpgave } from './f8-extra';
import {
  afdrukStandOpgave, afdrukPassendOpgave, afdrukKopVoetOpgave,
  afdrukTitelrijenOpgave, afdrukRapportOpgave,
} from './f3-afdrukken';
import {
  staafOpgave, lijnOpgave, cirkelOpgave, grafiekOpmaakOpgave, tweeReeksenOpgave,
} from './f4-grafieken';
import {
  draaiEersteOpgave, draaiKruistabelOpgave, draaiFunctieOpgave,
  draaiFilterOpgave, draaiRapportOpgave,
} from './f7-draaitabellen';
import type { EenOpgave } from '@/lib/werkblad-types';

/**
 * Publieke catalogus: veilig om naar de browser te sturen.
 * Per Focus loopt de moeilijkheid op van ● naar ●●●●●.
 */
const ALLE: EenOpgave[] = [
  // Focus 1 — rekenblad gebruiken en opmaken
  getalnotatieOpgave, tabelOpgave, sorterenOpgave, vastzettenOpgave, transponerenOpgave,
  // Focus 2 — formules en functies
  voorraadOpgave, prijslijstOpgave, factuurOpgave, verkoopOpgave, bestellingenOpgave, klantenOpgave,
  // Focus 3 — afdrukken (in echt Excel)
  afdrukStandOpgave, afdrukPassendOpgave, afdrukKopVoetOpgave,
  afdrukTitelrijenOpgave, afdrukRapportOpgave,
  // Focus 4 — grafieken (in echt Excel)
  staafOpgave, lijnOpgave, cirkelOpgave, grafiekOpmaakOpgave, tweeReeksenOpgave,
  // Focus 5 — meerdere werkbladen
  bladenOphalenOpgave, bladenFiliaalOpgave, bladenVerschilOpgave, bladenGemiddeldeOpgave, bladenZoekenOpgave,
  // Focus 6 — koppelen
  koppelenPrijzenOpgave, koppelenZoekenOpgave, koppelenConsoliderenOpgave,
  koppelenHerstellenOpgave, koppelenFactuurOpgave,
  // Focus 7 — draaitabellen (in echt Excel)
  draaiEersteOpgave, draaiKruistabelOpgave, draaiFunctieOpgave,
  draaiFilterOpgave, draaiRapportOpgave,
  // Focus 8 — geavanceerde functies
  xzoekenOpgave, genesteOpgave, horizZoekenOpgave, tekstOpgave,
];

export const OEFENINGEN: Record<string, EenOpgave> = Object.fromEntries(ALLE.map((o) => [o.id, o]));

/** Gegroepeerd per Focus, binnen elke Focus op volgnummer. */
export function oefeningenPerFocus(): { focus: number; oefeningen: EenOpgave[] }[] {
  const groepen = new Map<number, EenOpgave[]>();
  for (const o of ALLE) {
    if (!groepen.has(o.focusNummer)) groepen.set(o.focusNummer, []);
    groepen.get(o.focusNummer)!.push(o);
  }
  return [...groepen.entries()]
    .sort(([a], [b]) => a - b)
    .map(([focus, oefeningen]) => ({
      focus,
      oefeningen: oefeningen.sort((a, b) => a.volgnummer - b.volgnummer),
    }));
}

export function oefeningenOpVolgorde(): EenOpgave[] {
  return oefeningenPerFocus().flatMap((g) => g.oefeningen);
}

export function vindOpgave(id: string): EenOpgave | undefined {
  return OEFENINGEN[id];
}
