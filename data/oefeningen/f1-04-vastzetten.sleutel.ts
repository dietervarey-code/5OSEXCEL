import 'server-only';
import type { Check } from '@/lib/nakijken';
import { LEVERINGEN } from './f1-04-vastzetten';
import { VALUTA_PATROON } from './bouwstenen';

const BEDRAGEN = LEVERINGEN.map(([, , aantal, prijs]) => Math.round(aantal * prijs * 100) / 100);
const RIJEN = LEVERINGEN.map((_, i) => `E${4 + i}`);

export const vastzettenChecks: Check[] = [
  {
    id: 'vastzetten',
    omschrijving: 'De eerste drie rijen staan vast',
    punten: 4,
    cellen: [],
    vastzettenEisen: { rijen: 3 },
    hint: 'Klik met de rechtermuisknop op het nummer van rij 4 en kies Freeze. In het Nederlandse Excel heet dat Beeld › Titels blokkeren.',
  },
  {
    id: 'bedragen',
    omschrijving: 'Bedrag per levering berekend',
    punten: 4,
    cellen: RIJEN,
    verwachteWaarden: BEDRAGEN,
    formulePatronen: [{ patroon: '^=.*C\\d+\\s*\\*\\s*D\\d+', uitleg: 'vermenigvuldig aantal met eenheidsprijs' }],
    hint: 'Typ =C4*D4 in E4 en voer door tot E27.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal met SOM, in valuta',
    punten: 2,
    cellen: ['E29'],
    verwachteWaarden: [Math.round(BEDRAGEN.reduce((s, n) => s + n, 0) * 100) / 100],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Gebruik =SOM(E4:E27) en geef de cel de getalnotatie Valuta.',
  },
];
