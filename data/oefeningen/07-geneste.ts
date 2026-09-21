import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 5 — een VERT.ZOEKEN en een ALS in één formule. */

export const KORTINGEN: [string, number][] = [
  ['A', 0.1],
  ['B', 0.07],
  ['C', 0.05],
];

export const EXTRA_VANAF = 100;
export const EXTRA = 0.02;

export const ORDERS: [string, string, number, number][] = [
  ['O-501', 'A', 150, 2450],
  ['O-502', 'B', 80, 1180],
  ['O-503', 'C', 220, 3620],
  ['O-504', 'A', 40, 890],
  ['O-505', 'B', 300, 5140],
  ['O-506', 'C', 95, 1275],
];

export const genesteOpgave: Opgave = {
  id: 'geneste-functies',
  titel: 'Korting berekenen met geneste functies',
  focus: 'Focus 8 — geneste functies: VERT.ZOEKEN binnen een berekening',
  volgnummer: 8,
  niveau: 5,
  leerdoel: 'Twee functies in één formule combineren, en begrijpen in welke volgorde ze rekenen.',
  stagecontext:
    'De zaak geeft korting volgens de categorie van de klant. Wie meer dan 100 stuks bestelt, ' +
    'krijgt daar nog 2 procentpunt bovenop. Bereken het kortingspercentage in één formule — ' +
    'niet met de hand per lijn.',
  opdrachten: [
    'Haal in E5 tot en met E10 het basispercentage uit de kortingstabel met VERT.ZOEKEN.',
    `Tel er in dezelfde formule ${EXTRA * 100} procentpunt bij als het aantal groter is dan ${EXTRA_VANAF}, met de functie ALS.`,
    'Bereken in F5 tot en met F10 de korting in euro: het bedrag maal het percentage.',
    'Geef F5 tot en met F10 de getalnotatie valuta met twee decimalen.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('geneste-functies', 'Kortingen', samen(
    { A1: { v: 'Kortingen per order', s: 'titel' } },
    { A2: { v: `Extra ${EXTRA * 100} procentpunt vanaf ${EXTRA_VANAF} stuks.` } },
    rij(4, 'A', ['Order', 'Categorie', 'Aantal', 'Bedrag', 'Kortingspercentage', 'Korting'], 'kop'),
    ...ORDERS.map(([nr, cat, aantal, bedrag], i) => rij(5 + i, 'A', [nr, cat, aantal, bedrag])),
    { H3: { v: 'Kortingstabel', s: 'nadruk' } },
    rij(4, 'H', ['Categorie', 'Basispercentage'], 'kop'),
    ...KORTINGEN.map(([cat, pct], i) => rij(5 + i, 'H', [cat, pct])),
  ), { rijen: 30, kolommen: 12 }),
};
