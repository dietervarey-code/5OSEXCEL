import 'server-only';
import type { CelInzending } from '@/lib/werkblad-types';

/**
 * Nakijklogica. Draait UITSLUITEND op de server: de antwoordsleutel mag nooit
 * mee naar de browser, anders leest een leerling ze binnen twee minuten uit
 * de ontwikkelaarsconsole.
 */

export type Check = {
  id: string;
  omschrijving: string;
  punten: number;
  /** Cellen waarop deze check slaat. */
  cellen: string[];
  /** Verwachte waarde per cel (zelfde volgorde als `cellen`). */
  verwachteWaarden?: (number | string)[];
  /** Afrondingsmarge bij getallen. */
  tolerantie?: number;
  /** Reguliere expressies die in de formule moeten voorkomen. */
  formulePatronen?: { patroon: string; uitleg: string }[];
  /** Reguliere expressie waaraan de getalnotatie moet voldoen. */
  getalnotatiePatroon?: string;
  /** Tekst die de leerling ziet als de check faalt. */
  hint: string;
};

export type CheckResultaat = {
  checkId: string;
  omschrijving: string;
  punten: number;
  behaald: boolean;
  feedback: string;
};

function zoekCel(inzending: CelInzending[], cel: string): CelInzending | undefined {
  return inzending.find((c) => c.cel.toUpperCase() === cel.toUpperCase());
}

const FOUTWAARDEN = ['#NAME?', '#NAAM?', '#VALUE!', '#WAARDE!', '#REF!', '#VERW!', '#DIV/0!', '#DEEL/0!', '#N/A', '#N/B', '#NUM!', '#GETAL!', '#NULL!', '#LEEG!'];

/** Een cel met een foutwaarde is nooit correct, ook al staat de juiste functie erin. */
function isFoutwaarde(waarde: unknown): boolean {
  return typeof waarde === 'string' && FOUTWAARDEN.includes(waarde.trim().toUpperCase());
}

/**
 * Zet een celwaarde om naar een getal.
 *
 * Zodra er een getalnotatie op de cel staat, stuurt het werkblad de opgemaakte
 * tekst door: "$3,253.40 " of "€ 1.234,56". Beide schrijfwijzen komen voor, en
 * welk teken de decimalen aangeeft hangt van de notatie af. We kijken daarom
 * naar het LAATSTE voorkomen van een komma of punt: dat is de decimaalscheiding,
 * al de rest zijn duizendtalscheidingen.
 */
export function naarGetal(waarde: unknown): number {
  if (typeof waarde === 'number') return waarde;
  if (typeof waarde !== 'string') return Number.NaN;

  // Valutatekens, spaties en haakjes eraf; het minteken en de scheidingstekens blijven.
  const negatief = /^\(.*\)$/.test(waarde.trim()) || waarde.includes('-');
  let tekst = waarde.replace(/[^\d,.]/g, '');
  if (!tekst) return Number.NaN;

  const laatsteKomma = tekst.lastIndexOf(',');
  const laatstePunt = tekst.lastIndexOf('.');

  if (laatsteKomma > laatstePunt) {
    // 1.234,56 — punt scheidt duizendtallen, komma de decimalen.
    tekst = tekst.replace(/\./g, '').replace(',', '.');
  } else if (laatstePunt > laatsteKomma) {
    // 1,234.56 — komma scheidt duizendtallen.
    tekst = tekst.replace(/,/g, '');
  } else {
    // Geen van beide, of alleen scheidingstekens van één soort.
    tekst = tekst.replace(/,/g, '');
  }

  const getal = Number(tekst);
  if (!Number.isFinite(getal)) return Number.NaN;
  return negatief ? -Math.abs(getal) : getal;
}

function getalGelijk(cel: CelInzending, verwacht: number, tolerantie: number): boolean {
  // Eerst het onderliggende getal; de opgemaakte tekst is alleen terugval.
  for (const kandidaat of [cel.ruweWaarde, cel.waarde]) {
    if (kandidaat === undefined || kandidaat === null || kandidaat === '') continue;
    const getal = naarGetal(kandidaat);
    if (Number.isFinite(getal) && Math.abs(getal - verwacht) <= tolerantie) return true;
  }
  return false;
}

export function voerCheckUit(check: Check, inzending: CelInzending[]): CheckResultaat {
  // Standaard één cent speling: een cel die op twee decimalen staat toont
  // 683,21 terwijl de echte uitkomst 683,214 is. Zonder deze marge zou een
  // correcte berekening afgekeurd worden zodra de leerling valuta-opmaak zet.
  const tolerantie = check.tolerantie ?? 0.01;
  const problemen: string[] = [];

  check.cellen.forEach((cel, i) => {
    const ingevuld = zoekCel(inzending, cel);

    if (!ingevuld || (ingevuld.waarde === null && !ingevuld.formule)) {
      problemen.push(`${cel} is leeg`);
      return;
    }

    // 1. Levert de cel een foutwaarde op? Dan heeft de rest geen zin.
    if (isFoutwaarde(ingevuld.waarde) || isFoutwaarde(ingevuld.ruweWaarde)) {
      problemen.push(`${cel} geeft ${String(ingevuld.ruweWaarde ?? ingevuld.waarde).trim()}`);
      return;
    }

    // 2. Klopt de uitkomst?
    const verwacht = check.verwachteWaarden?.[i];
    if (verwacht !== undefined) {
      const juist =
        typeof verwacht === 'number'
          ? getalGelijk(ingevuld, verwacht, tolerantie)
          : String(ingevuld.ruweWaarde ?? ingevuld.waarde ?? '').trim().toLowerCase() ===
            verwacht.trim().toLowerCase();
      if (!juist) problemen.push(`${cel} geeft niet het juiste resultaat`);
    }

    // 3. Is het met een formule opgelost, en met de juiste functie?
    if (check.formulePatronen?.length) {
      const formule = (ingevuld.formule ?? '').toUpperCase();
      if (!formule) {
        problemen.push(`${cel} bevat een getal in plaats van een formule`);
      } else {
        for (const { patroon, uitleg } of check.formulePatronen) {
          if (!new RegExp(patroon, 'i').test(formule)) problemen.push(`${cel}: ${uitleg}`);
        }
      }
    }

    // 4. Is de opmaak correct?
    if (check.getalnotatiePatroon) {
      const notatie = ingevuld.opmaak?.getalnotatie ?? '';
      if (!new RegExp(check.getalnotatiePatroon, 'i').test(notatie)) {
        problemen.push(`${cel} heeft nog niet de gevraagde getalnotatie`);
      }
    }
  });

  return {
    checkId: check.id,
    omschrijving: check.omschrijving,
    punten: check.punten,
    behaald: problemen.length === 0,
    // Maximaal drie problemen tonen, anders wordt de feedback een muur tekst.
    feedback: problemen.length === 0 ? 'Correct.' : `${problemen.slice(0, 3).join('; ')}. ${check.hint}`,
  };
}

export function kijkNa(checks: Check[], inzending: CelInzending[]) {
  const resultaten = checks.map((c) => voerCheckUit(c, inzending));
  const score = resultaten.filter((r) => r.behaald).reduce((s, r) => s + r.punten, 0);
  const maxScore = checks.reduce((s, c) => s + c.punten, 0);
  return { score, maxScore, resultaten };
}
