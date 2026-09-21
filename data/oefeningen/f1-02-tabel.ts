import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { Opgave } from '@/lib/werkblad-types';

export const UREN: [string, string, number, number][] = [
  ['An Peeters', 'Magazijn', 38, 12.4],
  ['Bram De Smet', 'Verkoop', 40, 14.1],
  ['Cindy Vermeulen', 'Magazijn', 32, 12.4],
  ['Dries Maes', 'Transport', 40, 13.8],
  ['Eva Janssens', 'Verkoop', 24, 14.1],
  ['Filip Coppens', 'Transport', 38, 13.8],
];

export const tabelOpgave: Opgave = {
  id: 'f1-tabel-opmaken',
  titel: 'Een tabel leesbaar maken',
  focus: 'Focus 1 — celopmaak, uitlijning, totaalrij',
  focusNummer: 1,
  volgnummer: 2,
  niveau: 2,
  leerdoel: 'Een ruwe tabel omvormen tot iets dat een collega meteen begrijpt.',
  stagecontext:
    'Deze urenlijst gaat naar de zaakvoerder. Zoals ze er nu uitziet, moet hij zoeken waar ' +
    'de koppen staan en waar het totaal. Maak er een verzorgde tabel van.',
  opdrachten: [
    'Zet de koptekst in rij 3 in het vet, met een achtergrondkleur.',
    'Lijn de koptekst in rij 3 gecentreerd uit.',
    'Bereken in D10 het totaal aantal uren met SOM.',
    'Zet de totaalrij (C10 en D10) in het vet.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f1-tabel-opmaken', 'Uren', samen(
    { A1: { v: 'Gepresteerde uren — week 38', s: 'titel' } },
    { A3: { v: 'Medewerker' }, B3: { v: 'Afdeling' }, C3: { v: 'Uren' }, D3: { v: 'Loonkost' } },
    ...UREN.map(([naam, afd, uren, tarief], i) => rij(4 + i, 'A', [naam, afd, uren, Math.round(uren * tarief * 100) / 100])),
    { C10: { v: 'Totaal' } },
  ), { rijen: 25, kolommen: 8 }),
};
