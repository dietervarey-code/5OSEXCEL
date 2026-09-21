import 'server-only';
import type { Check } from '@/lib/nakijken';
import { EXTRA, EXTRA_VANAF, KORTINGEN, ORDERS } from './07-geneste';
import { VALUTA_PATROON } from './bouwstenen';

const PERCENTAGES = ORDERS.map(([, cat, aantal]) => {
  const basis = KORTINGEN.find(([c]) => c === cat)![1];
  return basis + (aantal > EXTRA_VANAF ? EXTRA : 0);
});

const KORTINGEN_EUR = ORDERS.map(([, , , bedrag], i) => Math.round(bedrag * PERCENTAGES[i] * 100) / 100);

const RIJEN_E = ['E5', 'E6', 'E7', 'E8', 'E9', 'E10'];
const RIJEN_F = ['F5', 'F6', 'F7', 'F8', 'F9', 'F10'];

export const genesteChecks: Check[] = [
  {
    id: 'percentage',
    omschrijving: 'Kortingspercentage klopt, inclusief de extra staffel',
    punten: 4,
    cellen: RIJEN_E,
    verwachteWaarden: PERCENTAGES,
    tolerantie: 0.0005,
    hint: 'Denk in twee stukken: het basispercentage uit de tabel, plus eventueel 2 procentpunt.',
  },
  {
    id: 'vertzoeken',
    omschrijving: 'Basispercentage komt uit de tabel met VERT.ZOEKEN',
    punten: 2,
    cellen: RIJEN_E,
    formulePatronen: [
      { patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'haal het basispercentage op met VERT.ZOEKEN in plaats van het te typen' },
      { patroon: '\\$H\\$\\d+', uitleg: 'verwijs absoluut naar de kortingstabel' },
    ],
    hint: '=VERT.ZOEKEN(B5;$H$5:$I$7;2;ONWAAR) geeft het basispercentage.',
  },
  {
    id: 'als',
    omschrijving: 'De extra staffel wordt met ALS bepaald',
    punten: 2,
    cellen: RIJEN_E,
    formulePatronen: [{ patroon: 'ALS\\s*\\(', uitleg: 'gebruik ALS voor de voorwaarde op het aantal' }],
    hint: `Vul aan met + ALS(C5>${EXTRA_VANAF};${EXTRA};0).`,
  },
  {
    id: 'korting-euro',
    omschrijving: 'Korting in euro, met valuta-opmaak',
    punten: 2,
    cellen: RIJEN_F,
    verwachteWaarden: KORTINGEN_EUR,
    formulePatronen: [{ patroon: '^=.*D\\d+.*\\*|^=.*\\*.*D\\d+', uitleg: 'vermenigvuldig het bedrag met het percentage' }],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Gebruik =D5*E5 en geef de kolom de getalnotatie Valuta.',
  },
];
