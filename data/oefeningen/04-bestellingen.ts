import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 3 — ALS met een voorwaarde, plus AANTAL.ALS en SOM.ALS. */

export const DREMPEL = 500;

export const BESTELLINGEN: [string, string, number][] = [
  ['B-2401', 'Aannemingen Verbeke', 745.2],
  ['B-2402', 'Dakwerken Lievens', 312.5],
  ['B-2403', 'Bouwbedrijf Maes', 1280],
  ['B-2404', 'Schrijnwerk Dobbels', 489.95],
  ['B-2405', 'Installatie Vandaele', 625.4],
  ['B-2406', 'Klusbedrijf Six', 178.3],
  ['B-2407', 'Renovatie Top', 934.75],
  ['B-2408', 'Tuinaanleg Groen', 500],
];

export const bestellingenOpgave: Opgave = {
  id: 'bestellingen-als',
  titel: 'Bestellingen beoordelen',
  focus: 'Focus 2 — ALS, AANTAL.ALS, SOM.ALS',
  focusNummer: 2,
  volgnummer: 5,
  niveau: 3,
  leerdoel: 'Een beslissing laten nemen door het rekenblad, en tellen en optellen op voorwaarde.',
  stagecontext:
    'De zaak geeft gratis levering vanaf een bepaald bedrag. Die drempel staat in D2 en verandert ' +
    'af en toe. Vul per bestelling in of de levering gratis is, en maak de samenvatting.',
  opdrachten: [
    'Zet in D5 tot en met D12 het woord Gratis als het bedrag minstens de drempel uit D2 haalt, en anders Verzendkosten.',
    'Verwijs absoluut naar D2, zodat de drempel op één plaats aangepast kan worden.',
    'Tel in D15 met AANTAL.ALS hoeveel bestellingen gratis geleverd worden.',
    'Tel in D16 met SOM.ALS het totale bedrag van die gratis bestellingen op.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('bestellingen-als', 'Bestellingen', samen(
    { A1: { v: 'Bestellingen deze week', s: 'titel' } },
    { C2: { v: 'Drempel gratis levering', s: 'nadruk' }, D2: { v: DREMPEL, s: 'invoer' } },
    rij(4, 'A', ['Bestelnummer', 'Klant', 'Bedrag', 'Levering'], 'kop'),
    ...BESTELLINGEN.map(([nr, klant, bedrag], i) => rij(5 + i, 'A', [nr, klant, bedrag])),
    { B14: { v: 'Samenvatting', s: 'nadruk' } },
    { B15: { v: 'Aantal gratis leveringen' } },
    { B16: { v: 'Bedrag van de gratis leveringen' } },
  ), { rijen: 30, kolommen: 8 }),
};
