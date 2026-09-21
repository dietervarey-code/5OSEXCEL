import 'server-only';
import type { Check } from '@/lib/nakijken';
import { ARTIKELEN, FILIAALOMZET, FILIALEN } from './f6-koppelen';
import { VALUTA_PATROON } from './bouwstenen';

const PRIJSBLAD = { patroon: "(Prijslijst|'Prijslijst')\\s*!", uitleg: 'haal de prijs van het blad Prijslijst' };
const cel = (k: string, van: number, n: number) => Array.from({ length: n }, (_, i) => `${k}${van + i}`);

// --- 1 · prijzen koppelen --------------------------------------------
const AANTALLEN = [240, 80, 35, 12, 60, 8];
const PRIJZEN = ARTIKELEN.map(([, , p]) => p);
const BEDRAGEN = PRIJZEN.map((p, i) => Math.round(p * AANTALLEN[i] * 100) / 100);

export const koppelenPrijzenChecks: Check[] = [
  {
    id: 'prijzen',
    omschrijving: 'Prijzen gekoppeld aan het blad Prijslijst',
    punten: 5,
    cellen: cel('C', 4, 6),
    verwachteWaarden: PRIJZEN,
    formulePatronen: [PRIJSBLAD],
    hint: 'Typ in C4 de formule =Prijslijst!C4 en voer door.',
  },
  {
    id: 'bedragen',
    omschrijving: 'Bedrag per lijn berekend',
    punten: 3,
    cellen: cel('D', 4, 6),
    verwachteWaarden: BEDRAGEN,
    formulePatronen: [{ patroon: '^=.*B\\d+.*\\*|^=.*\\*.*B\\d+', uitleg: 'vermenigvuldig aantal met prijs' }],
    hint: 'Gebruik =B4*C4.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal met SOM',
    punten: 2,
    cellen: ['D11'],
    verwachteWaarden: [Math.round(BEDRAGEN.reduce((s, n) => s + n, 0) * 100) / 100],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(D4:D9).',
  },
];

// --- 2 · koppelen met VERT.ZOEKEN ------------------------------------
const VOLGORDE = ['DZ-300', 'SB-190', 'GP-125', 'CM-225', 'WN-150', 'IS-060'];
const AANTALLEN2 = [6, 500, 40, 25, 10, 18];
const zoek = (code: string) => ARTIKELEN.find(([c]) => c === code)!;

export const koppelenZoekenChecks: Check[] = [
  {
    id: 'omschrijving',
    omschrijving: 'Omschrijving opgehaald met VERT.ZOEKEN',
    punten: 4,
    cellen: cel('B', 4, 6),
    verwachteWaarden: VOLGORDE.map((c) => zoek(c)[1]),
    formulePatronen: [{ patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' }, PRIJSBLAD],
    hint: 'Gebruik =VERT.ZOEKEN(A4;Prijslijst!$A$4:$C$9;2;ONWAAR).',
  },
  {
    id: 'prijs',
    omschrijving: 'Prijs opgehaald met VERT.ZOEKEN, absoluut verwezen',
    punten: 3,
    cellen: cel('C', 4, 6),
    verwachteWaarden: VOLGORDE.map((c) => zoek(c)[2]),
    formulePatronen: [
      { patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' },
      { patroon: '\\$A\\$\\d+\\s*:\\s*\\$C\\$\\d+', uitleg: 'verwijs absoluut naar de tabel, bv. $A$4:$C$9' },
    ],
    hint: 'Zelfde formule met kolomnummer 3.',
  },
  {
    id: 'bedrag',
    omschrijving: 'Bedrag per lijn',
    punten: 3,
    cellen: cel('E', 4, 6),
    verwachteWaarden: VOLGORDE.map((c, i) => Math.round(zoek(c)[2] * AANTALLEN2[i] * 100) / 100),
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =C4*D4.',
  },
];

// --- 3 · consolideren ------------------------------------------------
const FILIAALBLAD = { patroon: `(${FILIALEN.join('|')})\\s*!`, uitleg: 'verwijs naar het blad van het filiaal' };
const KWARTAAL = FILIALEN.map((f) => FILIAALOMZET[f].reduce((s, n) => s + n, 0));
const PER_MAAND = [0, 1, 2].map((m) => FILIALEN.reduce((s, f) => s + FILIAALOMZET[f][m], 0));

export const koppelenConsoliderenChecks: Check[] = [
  {
    id: 'maandcijfers',
    omschrijving: 'Maandomzet per filiaal opgehaald uit het juiste blad',
    punten: 5,
    cellen: FILIALEN.flatMap((_, r) => ['B', 'C', 'D'].map((k) => `${k}${4 + r}`)),
    verwachteWaarden: FILIALEN.flatMap((f) => FILIAALOMZET[f]),
    formulePatronen: [FILIAALBLAD],
    hint: 'Gebruik =Roeselare!B4 voor januari, =Roeselare!B5 voor februari, enzovoort.',
  },
  {
    id: 'kwartaal',
    omschrijving: 'Kwartaaltotaal per filiaal',
    punten: 3,
    cellen: cel('E', 4, 3),
    verwachteWaarden: KWARTAAL,
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(B4:D4).',
  },
  {
    id: 'totaalrij',
    omschrijving: 'Totalen per maand en het eindtotaal',
    punten: 2,
    cellen: ['B7', 'C7', 'D7', 'E7'],
    verwachteWaarden: [...PER_MAAND, KWARTAAL.reduce((s, n) => s + n, 0)],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(B4:B6) en voer door naar rechts.',
  },
];

// --- 4 · herstellen ---------------------------------------------------
export const koppelenHerstellenChecks: Check[] = [
  {
    id: 'juiste-cijfers',
    omschrijving: 'Elk filiaal toont zijn eigen kwartaaltotaal',
    punten: 6,
    cellen: cel('B', 4, 3),
    verwachteWaarden: KWARTAAL,
    formulePatronen: [FILIAALBLAD],
    hint: 'Het totaal van een filiaal staat in cel B8 van zijn blad. Controleer per cel of de bladnaam én de cel kloppen.',
  },
  {
    id: 'eigen-blad',
    omschrijving: 'Kortrijk verwijst naar het blad Kortrijk',
    punten: 2,
    cellen: ['B6'],
    formulePatronen: [{ patroon: "(Kortrijk|'Kortrijk')\\s*!", uitleg: 'deze cel wijst nog naar een ander filiaal' }],
    hint: 'Kijk goed naar de bladnaam in de formule van B6.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal van de drie filialen',
    punten: 2,
    cellen: ['B8'],
    verwachteWaarden: [KWARTAAL.reduce((s, n) => s + n, 0)],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(B4:B6).',
  },
];

// --- 5 · gekoppelde factuur -------------------------------------------
const FACTUURCODES = ['SB-190', 'CM-225', 'IS-060', 'GP-125', 'DZ-300'];
const FACTUURAANTAL = [600, 45, 22, 80, 9];
const REGELBEDRAGEN = FACTUURCODES.map((c, i) => Math.round(zoek(c)[2] * FACTUURAANTAL[i] * 100) / 100);
const SUBTOTAAL = Math.round(REGELBEDRAGEN.reduce((s, n) => s + n, 0) * 100) / 100;
const KORTING = SUBTOTAAL > 1000 ? Math.round(SUBTOTAAL * 0.05 * 100) / 100 : 0;
const BTW = Math.round((SUBTOTAAL - KORTING) * 0.21 * 100) / 100;
const TEBETALEN = Math.round((SUBTOTAAL - KORTING + BTW) * 100) / 100;

export const koppelenFactuurChecks: Check[] = [
  {
    id: 'gegevens',
    omschrijving: 'Omschrijving en prijs gekoppeld met VERT.ZOEKEN',
    punten: 4,
    cellen: [...cel('B', 5, 5), ...cel('C', 5, 5)],
    verwachteWaarden: [...FACTUURCODES.map((c) => zoek(c)[1]), ...FACTUURCODES.map((c) => zoek(c)[2])],
    formulePatronen: [{ patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' }, PRIJSBLAD],
    hint: 'Gebruik =VERT.ZOEKEN(A5;Prijslijst!$A$4:$C$9;2;ONWAAR) en met kolom 3 voor de prijs.',
  },
  {
    id: 'regels',
    omschrijving: 'Bedrag per lijn en subtotaal',
    punten: 2,
    cellen: [...cel('E', 5, 5), 'E11'],
    verwachteWaarden: [...REGELBEDRAGEN, SUBTOTAAL],
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =C5*D5 per lijn en =SOM(E5:E9) voor het subtotaal.',
  },
  {
    id: 'korting',
    omschrijving: 'Korting met ALS, gekoppeld aan de drempel',
    punten: 2,
    cellen: ['E12'],
    verwachteWaarden: [KORTING],
    formulePatronen: [
      { patroon: 'ALS\\s*\\(', uitleg: 'gebruik ALS voor de voorwaarde' },
      { patroon: '\\$B\\$1[67]', uitleg: 'verwijs naar de drempel en het percentage onderaan' },
    ],
    hint: 'Gebruik =ALS(E11>$B$16;E11*$B$17;0).',
  },
  {
    id: 'btw-totaal',
    omschrijving: 'Btw op het bedrag na korting, en het totaal',
    punten: 2,
    cellen: ['E13', 'E14'],
    verwachteWaarden: [BTW, TEBETALEN],
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Gebruik =(E11-E12)*$B$15 voor de btw en =E11-E12+E13 voor het totaal.',
  },
];
