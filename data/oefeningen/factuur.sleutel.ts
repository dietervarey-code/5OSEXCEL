import 'server-only';
import type { Check } from '@/lib/nakijken';

/**
 * ANTWOORDSLEUTEL — server-only. Nooit importeren in een client component.
 * De import van 'server-only' bovenaan laat de build falen als dat toch gebeurt.
 */

const BEDRAGEN = [403.2, 508.8, 994, 765, 582.4];
const SUBTOTAAL = BEDRAGEN.reduce((s, n) => s + n, 0); // 3253.40
const BTW = SUBTOTAAL * 0.21;                          // 683.214
const TOTAAL = SUBTOTAAL + BTW;                        // 3936.614

export const factuurChecks: Check[] = [
  {
    id: 'bedragen',
    omschrijving: 'Bedrag per factuurlijn berekend met een formule',
    punten: 3,
    cellen: ['E12', 'E13', 'E14', 'E15', 'E16'],
    verwachteWaarden: BEDRAGEN,
    formulePatronen: [
      { patroon: '^=.*C\\d+\\s*\\*\\s*D\\d+', uitleg: 'vermenigvuldig de cel met het aantal met de cel met de eenheidsprijs' },
    ],
    hint: 'Typ in E12 de formule =C12*D12 en voer ze door tot E16.',
  },
  {
    id: 'subtotaal',
    omschrijving: 'Subtotaal berekend met de functie SOM',
    punten: 2,
    cellen: ['E18'],
    verwachteWaarden: [SUBTOTAAL],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik de functie SOM en niet E12+E13+E14+E15+E16' }],
    hint: 'Gebruik =SOM(E12:E16).',
  },
  {
    id: 'btw-bedrag',
    omschrijving: 'Btw-bedrag klopt',
    punten: 1,
    cellen: ['E19'],
    verwachteWaarden: [BTW],
    hint: 'De btw is het subtotaal vermenigvuldigd met het tarief in B21.',
  },
  {
    id: 'btw-absoluut',
    omschrijving: 'Btw verwijst absoluut naar het tarief in B21',
    punten: 2,
    cellen: ['E19'],
    formulePatronen: [{ patroon: '\\$B\\$21', uitleg: 'verwijs absoluut naar het btw-tarief, dus $B$21 en niet B21' }],
    hint: 'Zet dollartekens voor de kolom en de rij: =E18*$B$21. Zo blijft de verwijzing staan als je de formule doorvoert.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal te betalen berekend uit subtotaal en btw',
    punten: 1,
    cellen: ['E20'],
    verwachteWaarden: [TOTAAL],
    formulePatronen: [{ patroon: 'E18', uitleg: 'reken verder met het subtotaal in E18 in plaats van het bedrag opnieuw in te typen' }],
    hint: 'Gebruik =E18+E19 of =SOM(E18:E19).',
  },
  {
    id: 'getalnotatie',
    omschrijving: 'Bedragen staan in valuta met twee decimalen',
    punten: 1,
    cellen: ['E12', 'E13', 'E14', 'E15', 'E16', 'E18', 'E19', 'E20'],
    // Twee decimalen én een valutateken, welk teken dan ook: de valutaknop van
    // het werkblad levert dollars, en daar kan de leerling niets aan doen.
    getalnotatiePatroon: '^(?=.*0\\.00)(?=.*(€|\\$|£|EUR|\\[\\$)).*$',
    hint: 'Selecteer E12:E20 en kies in de werkbalk de getalnotatie Valuta.',
  },
];
