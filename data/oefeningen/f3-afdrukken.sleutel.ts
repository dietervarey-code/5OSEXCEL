import 'server-only';
import type { BestandCheck } from '@/lib/nakijken-bestand';

const LIGGEND: BestandCheck = {
  id: 'liggend',
  omschrijving: 'Het blad staat liggend',
  punten: 4,
  eis: { soort: 'afdruk', liggend: true },
  hint: 'Pagina-indeling › Afdrukstand › Liggend.',
};

export const afdrukStandChecks: BestandCheck[] = [
  { ...LIGGEND, punten: 6 },
  {
    id: 'marges',
    omschrijving: 'De marges zijn smal ingesteld',
    punten: 4,
    eis: { soort: 'afdruk', maxZijmarge: 0.5 },
    hint: 'Pagina-indeling › Marges › Smal. Dat zet de linker- en rechtermarge op 0,64 cm.',
  },
];

export const afdrukPassendChecks: BestandCheck[] = [
  { ...LIGGEND, punten: 3 },
  {
    id: 'passend-aan',
    omschrijving: 'De optie "Aanpassen aan" staat aan',
    punten: 3,
    eis: { soort: 'afdruk', passendMaken: true },
    hint: 'Kies Aanpassen aan in plaats van Vergroten/verkleinen met een percentage.',
  },
  {
    id: 'een-pagina-breed',
    omschrijving: 'Alles past op één pagina breed',
    punten: 4,
    eis: { soort: 'afdruk', passendBreed: 1 },
    hint: 'Zet Breedte op 1 pagina en laat Hoogte op Automatisch staan.',
  },
];

export const afdrukKopVoetChecks: BestandCheck[] = [
  {
    id: 'kopvoet',
    omschrijving: 'Er is een kop- of voettekst ingesteld',
    punten: 4,
    eis: { soort: 'afdruk', kopVoettekst: true },
    hint: 'Invoegen › Kop- en voettekst, of via Pagina-instelling.',
  },
  {
    id: 'paginanummer',
    omschrijving: 'Het paginanummer staat in de kop- of voettekst',
    punten: 4,
    eis: { soort: 'afdruk', paginanummer: true },
    hint: 'Gebruik de knop voor paginanummer; in de code verschijnt dan &P.',
  },
  { ...LIGGEND, punten: 2 },
];

export const afdrukTitelrijenChecks: BestandCheck[] = [
  {
    id: 'titelrijen',
    omschrijving: 'Rij 3 wordt op elke pagina herhaald',
    punten: 6,
    eis: { soort: 'afdruk', titelrijen: true },
    hint: 'Pagina-indeling › Afdruktitels › Rijen bovenaan herhalen: $3:$3.',
  },
  { ...LIGGEND, punten: 2 },
  {
    id: 'een-pagina-breed',
    omschrijving: 'Alles past op één pagina breed',
    punten: 2,
    eis: { soort: 'afdruk', passendBreed: 1, passendMaken: true },
    hint: 'Pagina-indeling › Aanpassen aan › Breedte 1 pagina.',
  },
];

export const afdrukRapportChecks: BestandCheck[] = [
  { ...LIGGEND, punten: 2 },
  {
    id: 'marges',
    omschrijving: 'Smalle marges',
    punten: 2,
    eis: { soort: 'afdruk', maxZijmarge: 0.5 },
    hint: 'Pagina-indeling › Marges › Smal.',
  },
  {
    id: 'passend',
    omschrijving: 'Eén pagina breed',
    punten: 2,
    eis: { soort: 'afdruk', passendBreed: 1, passendMaken: true },
    hint: 'Aanpassen aan › Breedte 1 pagina, Hoogte automatisch.',
  },
  {
    id: 'titelrijen',
    omschrijving: 'Titelrijen herhaald',
    punten: 2,
    eis: { soort: 'afdruk', titelrijen: true },
    hint: 'Pagina-indeling › Afdruktitels.',
  },
  {
    id: 'kopvoet',
    omschrijving: 'Koptekst en paginanummer',
    punten: 2,
    eis: { soort: 'afdruk', kopVoettekst: true, paginanummer: true },
    hint: 'Titel in de koptekst, Pagina &P van &N in de voettekst.',
  },
];
