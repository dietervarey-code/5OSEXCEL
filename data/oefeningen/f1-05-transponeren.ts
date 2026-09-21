import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

export const MAANDEN = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni'];
export const CIJFERS = [24500, 21870, 26340, 23180, 27960, 25410];

export const transponerenOpgave: Opgave = {
  id: 'f1-transponeren',
  titel: 'Gegevens van rijen naar kolommen',
  focus: 'Focus 1 — transponeren',
  focusNummer: 1,
  volgnummer: 5,
  niveau: 3,
  leerdoel: 'Een tabel kantelen zonder alles opnieuw te typen.',
  stagecontext:
    'De omzetcijfers staan naast elkaar, maar de boekhouder wil ze onder elkaar om er een ' +
    'grafiek van te maken. Kantel de tabel met Plakken speciaal › Transponeren.',
  opdrachten: [
    'Kopieer het bereik B3:G4.',
    'Klik in A7, gebruik de rechtermuisknop en kies Paste Special met de optie Transpose. In het Nederlandse Excel heet dat Plakken speciaal › Transponeren.',
    'De maanden komen in A7 tot en met A12, de omzet in B7 tot en met B12.',
    'Bereken in B14 de totale omzet met SOM.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f1-transponeren', 'Omzet', samen(
    { A1: { v: 'Omzet eerste halfjaar', s: 'titel' } },
    { A3: { v: 'Maand', s: 'kop' }, A4: { v: 'Omzet', s: 'kop' } },
    ...MAANDEN.map((m, i) => ({ [`${String.fromCharCode(66 + i)}3`]: { v: m, s: 'kop' } })),
    ...CIJFERS.map((c, i) => ({ [`${String.fromCharCode(66 + i)}4`]: { v: c } })),
    { A6: { v: 'Hieronder komt de gekantelde tabel:', s: 'nadruk' } },
    { A14: { v: 'Totaal', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 10 }),
};
