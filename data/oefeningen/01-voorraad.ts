import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 1 — vermenigvuldigen, SOM en getalnotatie. Geen valstrikken. */

export const ARTIKELEN: [string, number, number][] = [
  ['Schroeven 4x40 (doos)', 120, 3.45],
  ['Pluggen 8 mm (100 st)', 85, 4.2],
  ['Siliconenkit wit', 46, 6.75],
  ['Schuurpapier K80', 210, 1.15],
  ['Montagelijm', 38, 8.9],
  ['Isolatietape zwart', 150, 2.3],
  ['Spuitbus primer', 24, 12.5],
  ['Werkhandschoenen maat 10', 95, 5.6],
];

export const voorraadOpgave: Opgave = {
  id: 'voorraad-basis',
  titel: 'Voorraadlijst afwerken',
  focus: 'Focus 1 & 2 — vermenigvuldigen, SOM, getalnotatie',
  focusNummer: 2,
  volgnummer: 1,
  niveau: 1,
  leerdoel: 'Een bedrag berekenen met een formule in plaats van een rekenmachine, en optellen met SOM.',
  stagecontext:
    'Je eerste dag in het magazijn. De magazijnier heeft geteld wat er in de rekken ligt en ' +
    'wat elk stuk kost. Jij moet uitrekenen hoeveel de voorraad waard is.',
  opdrachten: [
    'Bereken in D4 tot en met D11 de waarde per artikel (aantal × prijs per stuk).',
    'Bereken in D13 de totale voorraadwaarde met de functie SOM.',
    'Geef D4 tot en met D13 de getalnotatie valuta met twee decimalen.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('voorraad-basis', 'Voorraad', samen(
    { A1: { v: 'Bouwmaterialen De Vlieger bv — voorraadlijst', s: 'titel' } },
    { A2: { v: 'Telling van 18 september' } },
    rij(3, 'A', ['Artikel', 'Aantal', 'Prijs per stuk', 'Waarde'], 'kop'),
    ...ARTIKELEN.map(([naam, aantal, prijs], i) => rij(4 + i, 'A', [naam, aantal, prijs])),
    { B13: { v: 'Totale voorraadwaarde', s: 'totaal' }, C13: { v: '', s: 'totaal' }, D13: { v: '', s: 'totaal' } },
  ), { rijen: 30, kolommen: 8 }),
};
