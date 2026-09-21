import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 2 — MAX, MIN, GEMIDDELDE, en het verschil tussen AANTAL en AANTALARG. */

export const VERKOPERS: [string, number, number | string, number][] = [
  ['An Peeters', 12450, 13120, 11890],
  ['Bram De Smet', 9870, 10240, 10990],
  ['Cindy Vermeulen', 15300, 14780, 16120],
  ['Dries Maes', 8420, 'ziek', 9150],
  ['Eva Janssens', 11100, 11640, 12030],
  ['Filip Coppens', 13760, 12890, 13410],
];

export const verkoopOpgave: Opgave = {
  id: 'verkoopcijfers',
  titel: 'Verkoopcijfers samenvatten',
  focus: 'Focus 2 — MAX, MIN, GEMIDDELDE, AANTAL, AANTALARG',
  focusNummer: 2,
  volgnummer: 4,
  niveau: 2,
  leerdoel: 'Een reeks cijfers samenvatten, en weten waarom AANTAL en AANTALARG verschillen.',
  stagecontext:
    'De verkoopleider wil een samenvatting van het eerste kwartaal voor de vergadering van morgen. ' +
    'Let op: één verkoper was een maand ziek, en dat staat als tekst in de tabel.',
  opdrachten: [
    'Bereken in E4 tot en met E9 het kwartaaltotaal per verkoper met SOM.',
    'Bereken in C12 het hoogste kwartaaltotaal met MAX.',
    'Bereken in C13 het laagste kwartaaltotaal met MIN.',
    'Bereken in C14 het gemiddelde kwartaaltotaal met GEMIDDELDE.',
    'Tel in C15 met AANTAL hoeveel verkopers een cijfer hebben voor februari.',
    'Tel in C16 met AANTALARG hoeveel vakjes in februari niet leeg zijn.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('verkoopcijfers', 'Kwartaal', samen(
    { A1: { v: 'Verkoop eerste kwartaal', s: 'titel' } },
    rij(3, 'A', ['Verkoper', 'Januari', 'Februari', 'Maart', 'Kwartaaltotaal'], 'kop'),
    ...VERKOPERS.map(([naam, jan, feb, mrt], i) => rij(4 + i, 'A', [naam, jan, feb, mrt])),
    { A11: { v: 'Samenvatting', s: 'nadruk' } },
    { B12: { v: 'Hoogste kwartaaltotaal' } },
    { B13: { v: 'Laagste kwartaaltotaal' } },
    { B14: { v: 'Gemiddeld kwartaaltotaal' } },
    { B15: { v: 'Verkopers met een cijfer in februari' } },
    { B16: { v: 'Ingevulde vakjes in februari' } },
  ), { rijen: 30, kolommen: 8 }),
};
