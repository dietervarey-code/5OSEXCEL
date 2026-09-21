import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 2 — absolute celverwijzing en AFRONDEN. */

export const VERHOGING = 0.035;

export const PRIJZEN: [string, string, number][] = [
  ['Buitenkraan messing', 'SK-012', 34.5],
  ['Sifon 40 mm', 'SF-040', 12.8],
  ['Flexibel 50 cm', 'FX-050', 7.95],
  ['Afvoerbuis 110 mm', 'AB-110', 22.4],
  ['Dakgoot zink 3 m', 'DZ-300', 58],
  ['Regenpijp 80 mm', 'RP-080', 19.75],
  ['Bladvanger', 'BV-001', 14.3],
];

export const prijslijstOpgave: Opgave = {
  id: 'prijslijst-verhoging',
  titel: 'Prijslijst bijwerken',
  focus: 'Focus 2 — absolute celverwijzing, AFRONDEN',
  focusNummer: 2,
  volgnummer: 2,
  niveau: 2,
  leerdoel: 'Eén percentage op een hele lijst toepassen met een verwijzing die blijft staan.',
  stagecontext:
    'De leverancier verhoogt al zijn prijzen. Het percentage staat in C2. Werk de prijslijst bij, ' +
    'en zorg dat je de formule één keer typt en daarna doorvoert.',
  opdrachten: [
    'Bereken in D5 tot en met D11 de nieuwe prijs: de huidige prijs plus de verhoging uit C2.',
    'Verwijs absoluut naar C2, zodat je de formule kunt doorvoeren zonder dat ze stukgaat.',
    'Rond de nieuwe prijs af op twee decimalen met de functie AFRONDEN.',
    'Bereken in E5 tot en met E11 hoeveel elk artikel duurder wordt.',
    'Geef D5 tot en met E11 de getalnotatie valuta met twee decimalen.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('prijslijst-verhoging', 'Prijslijst', samen(
    { A1: { v: 'Prijslijst sanitair — herziening', s: 'titel' } },
    { B2: { v: 'Prijsverhoging', s: 'nadruk' }, C2: { v: VERHOGING, s: 'invoer' } },
    rij(4, 'A', ['Artikel', 'Artikelcode', 'Huidige prijs', 'Nieuwe prijs', 'Verschil'], 'kop'),
    ...PRIJZEN.map(([naam, code, prijs], i) => rij(5 + i, 'A', [naam, code, prijs])),
  ), { rijen: 30, kolommen: 8 }),
};
