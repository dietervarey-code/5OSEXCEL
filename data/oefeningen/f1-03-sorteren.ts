import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

export const OMZET: [string, string, number][] = [
  ['Bouwbedrijf Maes', 'Kortrijk', 46200],
  ['Aannemingen Verbeke', 'Roeselare', 37460],
  ['Klusbedrijf Six', 'Menen', 17570],
  ['Dakwerken Lievens', 'Izegem', 31100],
  ['Installatie Vandaele', 'Waregem', 40060],
  ['Schrijnwerk Dobbels', 'Tielt', 34770],
  ['Tuinaanleg Groen', 'Ardooie', 22890],
];

export const sorterenOpgave: Opgave = {
  id: 'f1-sorteren',
  titel: 'Klanten sorteren op omzet',
  focus: 'Focus 1 — sorteren',
  focusNummer: 1,
  volgnummer: 3,
  niveau: 2,
  leerdoel: 'Een lijst herschikken zonder de rijen uit elkaar te trekken.',
  stagecontext:
    'De zaakvoerder wil weten wie de grootste klanten zijn. Sorteer de lijst van hoogste naar ' +
    'laagste omzet. Let op dat de stad bij de juiste klant blijft staan.',
  opdrachten: [
    'Selecteer het volledige bereik A4:C10, inclusief de stad en de omzet.',
    'Sorteer op de kolom Omzet, van groot naar klein. De sorteerknop staat bovenaan onder Data.',
    'Bereken in C12 de totale omzet met SOM.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f1-sorteren', 'Klanten', samen(
    { A1: { v: 'Omzet per klant — vorig boekjaar', s: 'titel' } },
    rij(3, 'A', ['Klant', 'Stad', 'Omzet'], 'kop'),
    ...OMZET.map(([klant, stad, omzet], i) => rij(4 + i, 'A', [klant, stad, omzet])),
    { B12: { v: 'Totale omzet', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 8 }),
};
