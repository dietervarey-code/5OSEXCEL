import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

export const REGELS: [string, string, number, number, number][] = [
  ['Snelbouwsteen 19 cm', 'SB-190', 0.84, 0.21, 4800],
  ['Cement CEM II 25 kg', 'CM-225', 7.95, 0.21, 640],
  ['Isolatieplaat PIR 60', 'IS-060', 28.4, 0.06, 350],
  ['Wapeningsnet 150', 'WN-150', 42.5, 0.21, 180],
  ['Gipsplaat 12,5 mm', 'GP-125', 11.2, 0.06, 520],
  ['Dakgoot zink 3 m', 'DZ-300', 58, 0.21, 95],
];

export const getalnotatieOpgave: Opgave = {
  id: 'f1-getalnotatie',
  titel: 'Getalnotatie toepassen',
  focus: 'Focus 1 — getalnotatie en celopmaak',
  focusNummer: 1,
  volgnummer: 1,
  niveau: 1,
  leerdoel: 'Elk soort getal de juiste notatie geven, en de koptekst laten opvallen.',
  stagecontext:
    'De artikellijst is ingetypt, maar alles staat er als kaal getal. Een prijs, een btw-tarief ' +
    'en een aantal horen er anders uit te zien. Maak de lijst leesbaar.',
  opdrachten: [
    'Geef B4 tot en met B9 de getalnotatie valuta met twee decimalen.',
    'Geef C4 tot en met C9 de notatie percentage.',
    'Zet de koptekst in rij 3 in het vet.',
    'Geef de koptekst in rij 3 een achtergrondkleur.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f1-getalnotatie', 'Artikelen', samen(
    { A1: { v: 'Artikellijst — opmaak afwerken', s: 'titel' } },
    { A3: { v: 'Artikel' }, B3: { v: 'Prijs' }, C3: { v: 'Btw-tarief' }, D3: { v: 'Voorraad' } },
    ...REGELS.map(([naam, , prijs, btw, voorraad], i) => rij(4 + i, 'A', [naam, prijs, btw, voorraad])),
  ), { rijen: 25, kolommen: 8 }),
};
