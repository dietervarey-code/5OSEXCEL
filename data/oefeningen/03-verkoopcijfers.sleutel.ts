import 'server-only';
import type { Check } from '@/lib/nakijken';
import { VERKOPERS } from './03-verkoopcijfers';

const TOTALEN = VERKOPERS.map(([, jan, feb, mrt]) => jan + (typeof feb === 'number' ? feb : 0) + mrt);
const GEMIDDELDE = TOTALEN.reduce((s, n) => s + n, 0) / TOTALEN.length;

export const verkoopChecks: Check[] = [
  {
    id: 'totalen',
    omschrijving: 'Kwartaaltotaal per verkoper met SOM',
    punten: 3,
    cellen: ['E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
    verwachteWaarden: TOTALEN,
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM over de drie maanden' }],
    hint: 'Gebruik =SOM(B4:D4) en voer door tot E9. SOM slaat tekst zoals "ziek" gewoon over.',
  },
  {
    id: 'maximum',
    omschrijving: 'Hoogste kwartaaltotaal met MAX',
    punten: 2,
    cellen: ['C12'],
    verwachteWaarden: [Math.max(...TOTALEN)],
    formulePatronen: [{ patroon: '^=\\s*MAX\\s*\\(', uitleg: 'gebruik de functie MAX' }],
    hint: 'Gebruik =MAX(E4:E9).',
  },
  {
    id: 'minimum',
    omschrijving: 'Laagste kwartaaltotaal met MIN',
    punten: 2,
    cellen: ['C13'],
    verwachteWaarden: [Math.min(...TOTALEN)],
    formulePatronen: [{ patroon: '^=\\s*MIN\\s*\\(', uitleg: 'gebruik de functie MIN' }],
    hint: 'Gebruik =MIN(E4:E9).',
  },
  {
    id: 'gemiddelde',
    omschrijving: 'Gemiddeld kwartaaltotaal met GEMIDDELDE',
    punten: 1,
    cellen: ['C14'],
    verwachteWaarden: [GEMIDDELDE],
    tolerantie: 0.5,
    formulePatronen: [{ patroon: '^=\\s*GEMIDDELDE\\s*\\(', uitleg: 'gebruik de functie GEMIDDELDE' }],
    hint: 'Gebruik =GEMIDDELDE(E4:E9).',
  },
  {
    id: 'aantal',
    omschrijving: 'AANTAL telt alleen de getallen',
    punten: 1,
    cellen: ['C15'],
    verwachteWaarden: [VERKOPERS.filter(([, , feb]) => typeof feb === 'number').length],
    formulePatronen: [{ patroon: '^=\\s*AANTAL\\s*\\(', uitleg: 'gebruik AANTAL, niet AANTALARG' }],
    hint: '=AANTAL(C4:C9). "ziek" is tekst en telt niet mee.',
  },
  {
    id: 'aantalarg',
    omschrijving: 'AANTALARG telt alles wat niet leeg is',
    punten: 1,
    cellen: ['C16'],
    verwachteWaarden: [VERKOPERS.length],
    formulePatronen: [{ patroon: '^=\\s*AANTALARG\\s*\\(', uitleg: 'gebruik AANTALARG' }],
    hint: '=AANTALARG(C4:C9). Hier telt "ziek" wél mee.',
  },
];
