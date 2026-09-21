import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

/** Niveau 4 — X.ZOEKEN, inclusief wat er moet gebeuren als iets niet bestaat. */

export const ARTIKELTABEL: [string, string, number][] = [
  ['SB-190', 'Snelbouwsteen 19 cm', 0.84],
  ['CM-225', 'Cement CEM II 25 kg', 7.95],
  ['IS-060', 'Isolatieplaat PIR 60 mm', 28.4],
  ['WN-150', 'Wapeningsnet 150/150', 42.5],
  ['GP-125', 'Gipsplaat 12,5 mm', 11.2],
  ['DZ-300', 'Dakgoot zink 3 m', 58],
  ['RP-080', 'Regenpijp 80 mm', 19.75],
];

/** XX-999 bestaat niet: daar gaat het in deze oefening om. */
export const GEVRAAGD = ['IS-060', 'GP-125', 'XX-999', 'DZ-300', 'SB-190', 'CM-225'];

export const NIET_GEVONDEN = 'niet gevonden';

export const xzoekenOpgave: Opgave = {
  id: 'xzoeken-artikelen',
  titel: 'Artikelen opzoeken met X.ZOEKEN',
  focus: 'Focus 8 — X.ZOEKEN met terugvalwaarde',
  focusNummer: 8,
  volgnummer: 7,
  niveau: 4,
  leerdoel: 'Opzoeken met X.ZOEKEN, en netjes omgaan met een code die niet bestaat.',
  stagecontext:
    'De magazijnier stuurt een lijst artikelcodes door. Eén ervan is verkeerd overgetypt. ' +
    'Zorg dat je lijst daar niet op stukloopt maar netjes "niet gevonden" toont.',
  opdrachten: [
    'Haal in B4 tot en met B9 de omschrijving op met X.ZOEKEN.',
    `Geef als vierde argument de tekst "${NIET_GEVONDEN}" mee, zodat een onbestaande code geen foutwaarde geeft.`,
    'Haal in C4 tot en met C9 de prijs op met X.ZOEKEN. Geef daar 0 mee als terugval.',
    'Verwijs absoluut naar de artikeltabel.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('xzoeken-artikelen', 'Opzoeken', samen(
    { A1: { v: 'Artikelgegevens opzoeken', s: 'titel' } },
    { A2: { v: 'Let op: niet elke code bestaat.' } },
    rij(3, 'A', ['Gevraagde code', 'Omschrijving', 'Prijs'], 'kop'),
    ...GEVRAAGD.map((code, i) => rij(4 + i, 'A', [code])),
    { G2: { v: 'Artikeltabel', s: 'nadruk' } },
    rij(3, 'G', ['Code', 'Omschrijving', 'Prijs'], 'kop'),
    ...ARTIKELTABEL.map(([code, oms, prijs], i) => rij(4 + i, 'G', [code, oms, prijs])),
  ), { rijen: 30, kolommen: 12 }),
};
