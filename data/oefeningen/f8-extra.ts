import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Focus 8 — HORIZ.ZOEKEN en tekstfuncties. */

export const MAANDEN = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni'];
export const DOELEN = [22000, 21000, 24000, 23000, 25000, 26000];
export const GEHAALD = [24500, 18700, 26340, 23180, 21960, 27410];
export const GEVRAAGDE_MAANDEN = ['Maart', 'Mei', 'Januari', 'Juni'];

export const horizZoekenOpgave: Opgave = {
  id: 'f8-horiz-zoeken',
  titel: 'Maanddoelen opzoeken met HORIZ.ZOEKEN',
  focus: 'Focus 8 — HORIZ.ZOEKEN',
  focusNummer: 8,
  volgnummer: 4,
  niveau: 3,
  leerdoel: 'Zoeken in een tabel die horizontaal is opgebouwd in plaats van verticaal.',
  stagecontext:
    'De doelstellingen staan naast elkaar, één kolom per maand. Voor het maandrapport moet je ' +
    'er een paar uit halen. VERT.ZOEKEN werkt hier niet — die zoekt naar beneden.',
  opdrachten: [
    'Haal in B11 tot en met B14 het doel op van de gevraagde maand, met HORIZ.ZOEKEN.',
    'Haal in C11 tot en met C14 de werkelijk gehaalde omzet op.',
    'Bereken in D11 tot en met D14 of het doel gehaald is: zet Gehaald of Niet gehaald met ALS.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f8-horiz-zoeken', 'Doelen', samen(
    { A1: { v: 'Doelstellingen eerste halfjaar', s: 'titel' } },
    { A3: { v: 'Maand', s: 'kop' }, A4: { v: 'Doel', s: 'kop' }, A5: { v: 'Gehaald', s: 'kop' } },
    ...MAANDEN.map((m, i) => ({ [`${String.fromCharCode(66 + i)}3`]: { v: m, s: 'kop' } })),
    ...DOELEN.map((d, i) => ({ [`${String.fromCharCode(66 + i)}4`]: { v: d } })),
    ...GEHAALD.map((g, i) => ({ [`${String.fromCharCode(66 + i)}5`]: { v: g } })),
    { A9: { v: 'Rapport', s: 'nadruk' } },
    rij(10, 'A', ['Maand', 'Doel', 'Gehaald', 'Resultaat'], 'kop'),
    ...GEVRAAGDE_MAANDEN.map((m, i) => rij(11 + i, 'A', [m])),
  ), { rijen: 25, kolommen: 10 }),
};

export const KLANTCODES = ['ROE-1042-A', 'IZE-0873-B', 'KOR-2251-A', 'TIE-0119-C', 'MEN-1780-B'];

export const tekstOpgave: Opgave = {
  id: 'f8-tekstfuncties',
  titel: 'Klantcodes uit elkaar halen',
  focus: 'Focus 8 — LINKS, RECHTS, LENGTE',
  focusNummer: 8,
  volgnummer: 5,
  niveau: 4,
  leerdoel: 'Stukken uit een tekst halen, zodat je niet handmatig moet knippen en plakken.',
  stagecontext:
    'Het oude systeem levert klantcodes aan als één lange tekst: de stadscode, het klantnummer ' +
    'en de categorie aan elkaar. De boekhouding wil die stukken in aparte kolommen.',
  opdrachten: [
    'Haal in B4 tot en met B8 de eerste drie letters op met LINKS. Dat is de stadscode.',
    'Haal in C4 tot en met C8 het laatste teken op met RECHTS. Dat is de categorie.',
    'Bereken in D4 tot en met D8 hoeveel tekens de volledige code telt, met LENGTE.',
    'Zet in E4 tot en met E8 met ALS het woord Voorrang als de categorie A is, en anders Gewoon.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f8-tekstfuncties', 'Klantcodes', samen(
    { A1: { v: 'Klantcodes opsplitsen', s: 'titel' } },
    rij(3, 'A', ['Volledige code', 'Stadscode', 'Categorie', 'Lengte', 'Behandeling'], 'kop'),
    ...KLANTCODES.map((code, i) => rij(4 + i, 'A', [code])),
  ), { rijen: 25, kolommen: 10 }),
};
