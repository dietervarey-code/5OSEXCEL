import 'server-only';
import type { Check } from '@/lib/nakijken';
import { PRIJZEN, VERHOGING } from './02-prijslijst';
import { VALUTA_PATROON } from './bouwstenen';

const NIEUW = PRIJZEN.map(([, , prijs]) => Math.round(prijs * (1 + VERHOGING) * 100) / 100);
const VERSCHIL = PRIJZEN.map(([, , prijs], i) => Math.round((NIEUW[i] - prijs) * 100) / 100);

const RIJEN_D = ['D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11'];
const RIJEN_E = ['E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11'];

export const prijslijstChecks: Check[] = [
  {
    id: 'nieuwe-prijs',
    omschrijving: 'Nieuwe prijs klopt en is afgerond met AFRONDEN',
    punten: 4,
    cellen: RIJEN_D,
    verwachteWaarden: NIEUW,
    formulePatronen: [{ patroon: 'AFRONDEN\\s*\\(', uitleg: 'gebruik de functie AFRONDEN op twee decimalen' }],
    hint: 'Bijvoorbeeld =AFRONDEN(C5*(1+$C$2);2).',
  },
  {
    id: 'absoluut',
    omschrijving: 'De verhoging wordt absoluut aangesproken',
    punten: 3,
    cellen: RIJEN_D,
    formulePatronen: [
      { patroon: '\\$C\\$2', uitleg: 'verwijs met $C$2 naar de verhoging, anders schuift ze mee bij het doorvoeren' },
    ],
    hint: 'Zet dollartekens voor kolom en rij: $C$2. Met F4 gaat dat vanzelf.',
  },
  {
    id: 'verschil',
    omschrijving: 'Verschil tussen oude en nieuwe prijs',
    punten: 2,
    cellen: RIJEN_E,
    verwachteWaarden: VERSCHIL,
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =D5-C5.',
  },
  {
    id: 'getalnotatie',
    omschrijving: 'Bedragen in valuta met twee decimalen',
    punten: 1,
    cellen: [...RIJEN_D, ...RIJEN_E],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Selecteer D5:E11 en kies de getalnotatie Valuta.',
  },
];
