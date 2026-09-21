import 'server-only';
import type { Check } from '@/lib/nakijken';
import { ARTIKELTABEL, GEVRAAGD, NIET_GEVONDEN } from './06-xzoeken';

const OMSCHRIJVINGEN = GEVRAAGD.map((code) => ARTIKELTABEL.find(([c]) => c === code)?.[1] ?? NIET_GEVONDEN);
const PRIJZEN = GEVRAAGD.map((code) => ARTIKELTABEL.find(([c]) => c === code)?.[2] ?? 0);

const RIJEN_B = ['B4', 'B5', 'B6', 'B7', 'B8', 'B9'];
const RIJEN_C = ['C4', 'C5', 'C6', 'C7', 'C8', 'C9'];

export const xzoekenChecks: Check[] = [
  {
    id: 'omschrijving',
    omschrijving: 'Omschrijving opgehaald met X.ZOEKEN',
    punten: 4,
    cellen: RIJEN_B,
    verwachteWaarden: OMSCHRIJVINGEN,
    formulePatronen: [{ patroon: 'X\\.ZOEKEN\\s*\\(', uitleg: 'gebruik X.ZOEKEN' }],
    hint: 'Gebruik =X.ZOEKEN(A4;$G$4:$G$10;$H$4:$H$10;"niet gevonden").',
  },
  {
    id: 'terugval',
    omschrijving: 'Onbestaande code geeft "niet gevonden" in plaats van een foutwaarde',
    punten: 3,
    cellen: ['B6'],
    verwachteWaarden: [NIET_GEVONDEN],
    hint: 'Het vierde argument van X.ZOEKEN is wat je krijgt als er niets gevonden wordt.',
  },
  {
    id: 'prijs',
    omschrijving: 'Prijs opgehaald met X.ZOEKEN, met 0 als terugval',
    punten: 3,
    cellen: RIJEN_C,
    verwachteWaarden: PRIJZEN,
    formulePatronen: [
      { patroon: 'X\\.ZOEKEN\\s*\\(', uitleg: 'gebruik X.ZOEKEN' },
      { patroon: '\\$G\\$\\d+', uitleg: 'verwijs absoluut naar de tabel, bv. $G$4:$G$10' },
    ],
    hint: 'Gebruik =X.ZOEKEN(A4;$G$4:$G$10;$I$4:$I$10;0).',
  },
];
