import 'server-only';
import type { Check } from '@/lib/nakijken';
import { BESTELLINGEN, DREMPEL } from './04-bestellingen';
import { VALUTA_PATROON } from './bouwstenen';

const LEVERING = BESTELLINGEN.map(([, , bedrag]) => (bedrag >= DREMPEL ? 'Gratis' : 'Verzendkosten'));
const GRATIS = BESTELLINGEN.filter(([, , b]) => b >= DREMPEL);
const RIJEN_D = ['D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'];

export const bestellingenChecks: Check[] = [
  {
    id: 'als-kolom',
    omschrijving: 'Gratis of Verzendkosten per bestelling, met de functie ALS',
    punten: 4,
    cellen: RIJEN_D,
    verwachteWaarden: LEVERING,
    formulePatronen: [{ patroon: '^=\\s*ALS\\s*\\(', uitleg: 'gebruik de functie ALS' }],
    hint: 'Gebruik =ALS(C5>=$D$2;"Gratis";"Verzendkosten") en voer door tot D12.',
  },
  {
    id: 'drempel-absoluut',
    omschrijving: 'De drempel wordt absoluut aangesproken',
    punten: 2,
    cellen: RIJEN_D,
    formulePatronen: [{ patroon: '\\$D\\$2', uitleg: 'verwijs met $D$2 naar de drempel' }],
    hint: 'Zonder dollartekens schuift de verwijzing mee en vergelijk je met een lege cel.',
  },
  {
    id: 'aantal-als',
    omschrijving: 'Aantal gratis leveringen met AANTAL.ALS',
    punten: 2,
    cellen: ['D15'],
    verwachteWaarden: [GRATIS.length],
    formulePatronen: [{ patroon: 'AANTAL\\.ALS\\s*\\(', uitleg: 'gebruik AANTAL.ALS' }],
    hint: 'Gebruik =AANTAL.ALS(D5:D12;"Gratis").',
  },
  {
    id: 'som-als',
    omschrijving: 'Bedrag van de gratis leveringen met SOM.ALS',
    punten: 2,
    cellen: ['D16'],
    verwachteWaarden: [GRATIS.reduce((s, [, , b]) => s + b, 0)],
    formulePatronen: [{ patroon: 'SOM\\.ALS\\s*\\(', uitleg: 'gebruik SOM.ALS' }],
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Gebruik =SOM.ALS(D5:D12;"Gratis";C5:C12): zoek in kolom D, tel op uit kolom C.',
  },
];
