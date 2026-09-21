import 'server-only';
import type { Check } from '@/lib/nakijken';
import { BESTELLINGEN, KLANTEN } from './05-klanten';

function klant(nummer: string) {
  return KLANTEN.find(([nr]) => nr === nummer)!;
}

const NAMEN = BESTELLINGEN.map(([, nr]) => klant(nr)[1]);
const STEDEN = BESTELLINGEN.map(([, nr]) => klant(nr)[2]);

const RIJEN_C = ['C4', 'C5', 'C6', 'C7', 'C8', 'C9'];
const RIJEN_D = ['D4', 'D5', 'D6', 'D7', 'D8', 'D9'];

export const klantenChecks: Check[] = [
  {
    id: 'naam',
    omschrijving: 'Naam van de klant opgehaald met VERT.ZOEKEN',
    punten: 4,
    cellen: RIJEN_C,
    verwachteWaarden: NAMEN,
    formulePatronen: [{ patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN en typ de naam niet over' }],
    hint: 'Gebruik =VERT.ZOEKEN(B4;$G$4:$I$9;2;ONWAAR).',
  },
  {
    id: 'stad',
    omschrijving: 'Stad opgehaald met VERT.ZOEKEN',
    punten: 3,
    cellen: RIJEN_D,
    verwachteWaarden: STEDEN,
    formulePatronen: [
      { patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' },
      { patroon: '[,;]\\s*3\\s*[,;]', uitleg: 'de stad staat in de derde kolom van de tabel' },
    ],
    hint: 'Zelfde formule als bij de naam, maar met kolomnummer 3.',
  },
  {
    id: 'absoluut-exact',
    omschrijving: 'Tabel absoluut aangesproken en exact gezocht',
    punten: 3,
    cellen: [...RIJEN_C, ...RIJEN_D],
    formulePatronen: [
      { patroon: '\\$G\\$\\d+\\s*:\\s*\\$I\\$\\d+', uitleg: 'verwijs absoluut naar de klantentabel, bv. $G$4:$I$9' },
      { patroon: '(ONWAAR|FALSE|[,;]\\s*0\\s*\\))', uitleg: 'zoek exact: sluit af met ONWAAR' },
    ],
    hint: 'Zonder dollartekens schuift de tabel mee bij het doorvoeren. Zonder ONWAAR zoekt Excel bij benadering.',
  },
];
