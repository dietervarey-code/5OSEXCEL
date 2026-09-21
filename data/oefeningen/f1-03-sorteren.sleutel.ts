import 'server-only';
import type { Check } from '@/lib/nakijken';
import { OMZET } from './f1-03-sorteren';

const GESORTEERD = [...OMZET].sort((a, b) => b[2] - a[2]);
const RIJEN = ['A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'];
const STEDEN = ['B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10'];

export const sorterenChecks: Check[] = [
  {
    id: 'volgorde',
    omschrijving: 'Klanten staan van hoogste naar laagste omzet',
    punten: 5,
    cellen: RIJEN,
    verwachteVolgorde: GESORTEERD.map(([klant]) => klant),
    hint: 'Selecteer A4:C10, klik bovenaan op Data en kies de sorteerknop. Sorteer aflopend op de kolom Omzet.',
  },
  {
    id: 'rijen-heel',
    omschrijving: 'De stad is bij de juiste klant gebleven',
    punten: 3,
    cellen: STEDEN,
    verwachteVolgorde: GESORTEERD.map(([, stad]) => stad),
    hint: 'Sorteer je maar één kolom, dan raken de gegevens door elkaar. Selecteer altijd de hele tabel.',
  },
  {
    id: 'totaal',
    omschrijving: 'Totale omzet met SOM',
    punten: 2,
    cellen: ['C12'],
    verwachteWaarden: [OMZET.reduce((s, [, , o]) => s + o, 0)],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],
    hint: 'Gebruik =SOM(C4:C10).',
  },
];
