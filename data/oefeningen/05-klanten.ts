import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 3 — VERT.ZOEKEN met een exacte match. */

export const KLANTEN: [string, string, string][] = [
  ['K-101', 'Aannemingen Verbeke', 'Roeselare'],
  ['K-102', 'Dakwerken Lievens', 'Izegem'],
  ['K-103', 'Bouwbedrijf Maes', 'Kortrijk'],
  ['K-104', 'Schrijnwerk Dobbels', 'Tielt'],
  ['K-105', 'Installatie Vandaele', 'Waregem'],
  ['K-106', 'Klusbedrijf Six', 'Menen'],
];

export const BESTELLINGEN: [string, string][] = [
  ['B-3001', 'K-103'],
  ['B-3002', 'K-101'],
  ['B-3003', 'K-106'],
  ['B-3004', 'K-102'],
  ['B-3005', 'K-105'],
  ['B-3006', 'K-104'],
];

export const klantenOpgave: Opgave = {
  id: 'klanten-vertzoeken',
  titel: 'Klantenbestand aanvullen',
  focus: 'Focus 2 & 8 — VERT.ZOEKEN',
  focusNummer: 2,
  volgnummer: 6,
  niveau: 3,
  leerdoel: 'Gegevens uit een andere tabel halen op basis van een code, in plaats van ze over te typen.',
  stagecontext:
    'De bestellijst bevat alleen klantnummers. De boekhouding wil er ook de naam en de stad bij. ' +
    'Typ ze niet over: haal ze op uit de klantentabel rechts, zodat de lijst mee verandert als daar iets wijzigt.',
  opdrachten: [
    'Haal in C4 tot en met C9 de naam van de klant op met VERT.ZOEKEN.',
    'Haal in D4 tot en met D9 de stad op met VERT.ZOEKEN.',
    'Verwijs absoluut naar de klantentabel, zodat je de formule kunt doorvoeren.',
    'Zoek exact: geef ONWAAR mee als laatste argument.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('klanten-vertzoeken', 'Bestellingen', samen(
    { A1: { v: 'Bestellingen aanvullen', s: 'titel' } },
    rij(3, 'A', ['Bestelnummer', 'Klantnummer', 'Naam klant', 'Stad'], 'kop'),
    ...BESTELLINGEN.map(([nr, klant], i) => rij(4 + i, 'A', [nr, klant])),
    { G2: { v: 'Klantentabel', s: 'nadruk' } },
    rij(3, 'G', ['Klantnummer', 'Naam', 'Stad'], 'kop'),
    ...KLANTEN.map(([nr, naam, stad], i) => rij(4 + i, 'G', [nr, naam, stad])),
  ), { rijen: 30, kolommen: 12 }),
};
