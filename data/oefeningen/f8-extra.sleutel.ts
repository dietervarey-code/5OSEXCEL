import 'server-only';
import type { Check } from '@/lib/nakijken';
import { DOELEN, GEHAALD, GEVRAAGDE_MAANDEN, KLANTCODES, MAANDEN } from './f8-extra';

const cel = (k: string, van: number, n: number) => Array.from({ length: n }, (_, i) => `${k}${van + i}`);
const index = (m: string) => MAANDEN.indexOf(m);

export const horizZoekenChecks: Check[] = [
  {
    id: 'doelen',
    omschrijving: 'Doel opgehaald met HORIZ.ZOEKEN',
    punten: 4,
    cellen: cel('B', 11, 4),
    verwachteWaarden: GEVRAAGDE_MAANDEN.map((m) => DOELEN[index(m)]),
    formulePatronen: [{ patroon: 'HORIZ\\.ZOEKEN\\s*\\(', uitleg: 'gebruik HORIZ.ZOEKEN, niet VERT.ZOEKEN' }],
    hint: 'Gebruik =HORIZ.ZOEKEN(A11;$B$3:$G$5;2;ONWAAR). Rij 2 van die tabel is de doelrij.',
  },
  {
    id: 'gehaald',
    omschrijving: 'Gehaalde omzet opgehaald met HORIZ.ZOEKEN',
    punten: 3,
    cellen: cel('C', 11, 4),
    verwachteWaarden: GEVRAAGDE_MAANDEN.map((m) => GEHAALD[index(m)]),
    formulePatronen: [
      { patroon: 'HORIZ\\.ZOEKEN\\s*\\(', uitleg: 'gebruik HORIZ.ZOEKEN' },
      { patroon: '[,;]\\s*3\\s*[,;]', uitleg: 'de gehaalde omzet staat op de derde rij van de tabel' },
    ],
    hint: 'Zelfde formule, maar met rijnummer 3.',
  },
  {
    id: 'resultaat',
    omschrijving: 'Gehaald of Niet gehaald met ALS',
    punten: 3,
    cellen: cel('D', 11, 4),
    verwachteWaarden: GEVRAAGDE_MAANDEN.map((m) => (GEHAALD[index(m)] >= DOELEN[index(m)] ? 'Gehaald' : 'Niet gehaald')),
    formulePatronen: [{ patroon: 'ALS\\s*\\(', uitleg: 'gebruik ALS' }],
    hint: 'Gebruik =ALS(C11>=B11;"Gehaald";"Niet gehaald").',
  },
];

export const tekstChecks: Check[] = [
  {
    id: 'stadscode',
    omschrijving: 'Stadscode met LINKS',
    punten: 3,
    cellen: cel('B', 4, 5),
    verwachteWaarden: KLANTCODES.map((c) => c.slice(0, 3)),
    formulePatronen: [{ patroon: '^=\\s*LINKS\\s*\\(', uitleg: 'gebruik de functie LINKS' }],
    hint: 'Gebruik =LINKS(A4;3).',
  },
  {
    id: 'categorie',
    omschrijving: 'Categorie met RECHTS',
    punten: 3,
    cellen: cel('C', 4, 5),
    verwachteWaarden: KLANTCODES.map((c) => c.slice(-1)),
    formulePatronen: [{ patroon: '^=\\s*RECHTS\\s*\\(', uitleg: 'gebruik de functie RECHTS' }],
    hint: 'Gebruik =RECHTS(A4;1).',
  },
  {
    id: 'lengte',
    omschrijving: 'Aantal tekens met LENGTE',
    punten: 2,
    cellen: cel('D', 4, 5),
    verwachteWaarden: KLANTCODES.map((c) => c.length),
    formulePatronen: [{ patroon: '^=\\s*LENGTE\\s*\\(', uitleg: 'gebruik de functie LENGTE' }],
    hint: 'Gebruik =LENGTE(A4).',
  },
  {
    id: 'behandeling',
    omschrijving: 'Voorrang of Gewoon op basis van de categorie',
    punten: 2,
    cellen: cel('E', 4, 5),
    verwachteWaarden: KLANTCODES.map((c) => (c.endsWith('A') ? 'Voorrang' : 'Gewoon')),
    formulePatronen: [{ patroon: 'ALS\\s*\\(', uitleg: 'gebruik ALS' }],
    hint: 'Gebruik =ALS(C4="A";"Voorrang";"Gewoon").',
  },
];
