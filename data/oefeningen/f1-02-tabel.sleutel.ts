import 'server-only';
import type { Check } from '@/lib/nakijken';
import { UREN } from './f1-02-tabel';

const KOPPEN = ['A3', 'B3', 'C3', 'D3'];
const TOTAAL = UREN.reduce((s, [, , uren, tarief]) => s + Math.round(uren * tarief * 100) / 100, 0);

export const tabelChecks: Check[] = [
  {
    id: 'koppen-opmaak',
    omschrijving: 'Koptekst vet met een achtergrondkleur',
    punten: 3,
    cellen: KOPPEN,
    opmaakEisen: { vet: true, achtergrondkleur: true },
    hint: 'Selecteer A3:D3, klik op B (of Ctrl+B) en kies een opvulkleur met het emmertje.',
  },
  {
    id: 'koppen-gecentreerd',
    omschrijving: 'Koptekst gecentreerd',
    punten: 2,
    cellen: KOPPEN,
    opmaakEisen: { uitlijning: 'center' },
    hint: 'Selecteer A3:D3 en klik in de werkbalk op de knop voor centreren.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal van de loonkost met SOM',
    punten: 3,
    cellen: ['D10'],
    verwachteWaarden: [TOTAAL],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(D4:D9).',
  },
  {
    id: 'totaalrij-vet',
    omschrijving: 'Totaalrij in het vet',
    punten: 2,
    cellen: ['C10', 'D10'],
    opmaakEisen: { vet: true },
    hint: 'Selecteer C10:D10 en klik op B.',
  },
];
