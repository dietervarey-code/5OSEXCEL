import 'server-only';
import type { Check } from '@/lib/nakijken';
import { CIJFERS, MAANDEN } from './f1-05-transponeren';

const MAANDCELLEN = MAANDEN.map((_, i) => `A${7 + i}`);
const CIJFERCELLEN = CIJFERS.map((_, i) => `B${7 + i}`);

export const transponerenChecks: Check[] = [
  {
    id: 'maanden',
    omschrijving: 'De maanden staan onder elkaar in kolom A',
    punten: 4,
    cellen: MAANDCELLEN,
    verwachteVolgorde: MAANDEN,
    hint: 'Kopieer B3:G4, klik met de rechtermuisknop in A7 en kies Paste Special › Transpose.',
  },
  {
    id: 'cijfers',
    omschrijving: 'De omzetcijfers staan bij de juiste maand',
    punten: 4,
    cellen: CIJFERCELLEN,
    verwachteWaarden: CIJFERS,
    hint: 'Transponeren kantelt rijen naar kolommen: wat naast elkaar stond, komt onder elkaar.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totale omzet met SOM',
    punten: 2,
    cellen: ['B14'],
    verwachteWaarden: [CIJFERS.reduce((s, n) => s + n, 0)],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(B7:B12).',
  },
];
