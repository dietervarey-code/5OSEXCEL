import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Een lange lijst, zodat vastzetten echt nut heeft. */
export const LEVERINGEN: [string, string, number, number][] = Array.from({ length: 24 }, (_, i) => {
  const klanten = ['Maes', 'Verbeke', 'Six', 'Lievens', 'Vandaele', 'Dobbels'];
  return [
    `L-${4100 + i}`,
    klanten[i % klanten.length],
    [12, 45, 8, 23, 60, 17][i % 6] + i,
    Math.round(([34.5, 12.8, 58, 7.95, 22.4, 19.75][i % 6] + i * 0.35) * 100) / 100,
  ];
});

export const vastzettenOpgave: Opgave = {
  id: 'f1-vastzetten',
  titel: 'Titels vastzetten in een lange lijst',
  focus: 'Focus 1 — beeld vastzetten',
  focusNummer: 1,
  volgnummer: 4,
  niveau: 2,
  leerdoel: 'De koptekst in beeld houden terwijl je door een lange lijst scrolt.',
  stagecontext:
    'Deze leveringslijst loopt over meer dan twintig rijen. Zodra je naar beneden scrolt, ' +
    'weet je niet meer welke kolom wat is. Zet de koptekst vast.',
  opdrachten: [
    'Zet de eerste drie rijen vast, zodat de koptekst in beeld blijft bij het scrollen. Klik met de rechtermuisknop op het rijnummer en kies Freeze.',
    'Bereken in E4 tot en met E27 het bedrag per levering (aantal × eenheidsprijs).',
    'Bereken in E29 het totaal met SOM.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f1-vastzetten', 'Leveringen', samen(
    { A1: { v: 'Leveringen september', s: 'titel' } },
    { A2: { v: 'Scroll naar beneden: zonder vastzetten ben je de koppen kwijt.' } },
    rij(3, 'A', ['Leveringsnummer', 'Klant', 'Aantal', 'Eenheidsprijs', 'Bedrag'], 'kop'),
    ...LEVERINGEN.map(([nr, klant, aantal, prijs], i) => rij(4 + i, 'A', [nr, klant, aantal, prijs])),
    { D29: { v: 'Totaal', s: 'nadruk' } },
  ), { rijen: 40, kolommen: 8 }),
};
