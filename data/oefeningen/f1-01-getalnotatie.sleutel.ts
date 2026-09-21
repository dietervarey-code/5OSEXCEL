import 'server-only';
import type { Check } from '@/lib/nakijken';
import { VALUTA_PATROON } from './bouwstenen';

const PRIJZEN = ['B4', 'B5', 'B6', 'B7', 'B8', 'B9'];
const TARIEVEN = ['C4', 'C5', 'C6', 'C7', 'C8', 'C9'];
const KOPPEN = ['A3', 'B3', 'C3', 'D3'];

export const getalnotatieChecks: Check[] = [
  {
    id: 'valuta',
    omschrijving: 'Prijzen in valuta met twee decimalen',
    punten: 3,
    cellen: PRIJZEN,
    getalnotatiePatroon: VALUTA_PATROON,
    hint: 'Selecteer B4:B9 en kies in de werkbalk de getalnotatie Valuta.',
  },
  {
    id: 'percentage',
    omschrijving: 'Btw-tarieven als percentage',
    punten: 3,
    cellen: TARIEVEN,
    getalnotatiePatroon: '%',
    hint: 'Selecteer C4:C9 en klik op de knop met het procentteken.',
  },
  {
    id: 'koppen-vet',
    omschrijving: 'Koptekst in het vet',
    punten: 2,
    cellen: KOPPEN,
    opmaakEisen: { vet: true },
    hint: 'Selecteer rij 3 en klik op B, of druk op Ctrl+B.',
  },
  {
    id: 'koppen-kleur',
    omschrijving: 'Koptekst met een achtergrondkleur',
    punten: 2,
    cellen: KOPPEN,
    opmaakEisen: { achtergrondkleur: true },
    hint: 'Selecteer rij 3 en kies een opvulkleur in de werkbalk — het emmertje onder het tabblad Start.',
  },
];
