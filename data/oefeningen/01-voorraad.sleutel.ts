import 'server-only';
import type { Check } from '@/lib/nakijken';
import { ARTIKELEN } from './01-voorraad';
import { VALUTA_PATROON } from './bouwstenen';

const WAARDEN = ARTIKELEN.map(([, aantal, prijs]) => aantal * prijs);
const TOTAAL = WAARDEN.reduce((s, n) => s + n, 0);

export const voorraadChecks: Check[] = [
  {
    id: 'waarden',
    omschrijving: 'Waarde per artikel berekend met een formule',
    punten: 4,
    cellen: ['D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11'],
    verwachteWaarden: WAARDEN,
    formulePatronen: [
      { patroon: '^=.*B\\d+\\s*\\*\\s*C\\d+', uitleg: 'vermenigvuldig de cel met het aantal met de cel met de prijs' },
    ],
    hint: 'Typ in D4 de formule =B4*C4 en voer ze met de vulgreep door tot D11.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totale voorraadwaarde met de functie SOM',
    punten: 3,
    cellen: ['D13'],
    verwachteWaarden: [TOTAAL],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM en tel niet elke cel apart op' }],
    hint: 'Gebruik =SOM(D4:D11).',
  },
  {
    id: 'getalnotatie',
    omschrijving: 'Bedragen in valuta met twee decimalen',
    punten: 3,
    cellen: ['D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D13'],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Selecteer D4:D13 en kies in de werkbalk de getalnotatie Valuta.',
  },
];
