import 'server-only';
import type { BestandCheck } from '@/lib/nakijken-bestand';

const BESTAAT: BestandCheck = {
  id: 'draaitabel',
  omschrijving: 'Er staat een draaitabel in het bestand',
  punten: 4,
  eis: { soort: 'draaitabel', minAantal: 1 },
  hint: 'Klik in de tabel en kies Invoegen › Draaitabel.',
};

export const draaiEersteChecks: BestandCheck[] = [
  { ...BESTAAT, punten: 5 },
  {
    id: 'rijveld',
    omschrijving: 'Filiaal staat in het rijgebied',
    punten: 3,
    eis: { soort: 'draaitabel', minRijvelden: 1, veldenBevat: ['Filiaal'] },
    hint: 'Sleep het veld Filiaal naar het gebied Rijen.',
  },
  {
    id: 'waarde',
    omschrijving: 'Omzet staat in het waardengebied',
    punten: 2,
    eis: { soort: 'draaitabel', minGegevensvelden: 1 },
    hint: 'Sleep het veld Omzet naar het gebied Waarden.',
  },
];

export const draaiKruistabelChecks: BestandCheck[] = [
  { ...BESTAAT, punten: 3 },
  {
    id: 'rij',
    omschrijving: 'Filiaal in de rijen',
    punten: 2,
    eis: { soort: 'draaitabel', minRijvelden: 1 },
    hint: 'Sleep Filiaal naar Rijen.',
  },
  {
    id: 'kolom',
    omschrijving: 'Maand in de kolommen',
    punten: 3,
    eis: { soort: 'draaitabel', minKolomvelden: 1 },
    hint: 'Sleep Maand naar het gebied Kolommen — niet naar Rijen.',
  },
  {
    id: 'waarde',
    omschrijving: 'Omzet in de waarden',
    punten: 2,
    eis: { soort: 'draaitabel', minGegevensvelden: 1 },
    hint: 'Sleep Omzet naar Waarden.',
  },
];

export const draaiFunctieChecks: BestandCheck[] = [
  { ...BESTAAT, punten: 3 },
  {
    id: 'rij',
    omschrijving: 'Productgroep in de rijen',
    punten: 2,
    eis: { soort: 'draaitabel', minRijvelden: 1, veldenBevat: ['Productgroep'] },
    hint: 'Sleep Productgroep naar Rijen.',
  },
  {
    id: 'telfunctie',
    omschrijving: 'De functie staat op Aantal in plaats van Som',
    punten: 5,
    eis: { soort: 'draaitabel', functie: 'count' },
    hint: 'Klik op het veld in Waarden, kies Waardeveldinstellingen en zet de functie op Aantal.',
  },
];

export const draaiFilterChecks: BestandCheck[] = [
  { ...BESTAAT, punten: 2 },
  {
    id: 'rij-kolom',
    omschrijving: 'Productgroep in de rijen en Maand in de kolommen',
    punten: 4,
    eis: { soort: 'draaitabel', minRijvelden: 1, minKolomvelden: 1 },
    hint: 'Sleep Productgroep naar Rijen en Maand naar Kolommen.',
  },
  {
    id: 'waarde',
    omschrijving: 'Omzet in de waarden',
    punten: 2,
    eis: { soort: 'draaitabel', minGegevensvelden: 1 },
    hint: 'Sleep Omzet naar Waarden.',
  },
  {
    id: 'bron-compleet',
    omschrijving: 'Alle velden uit de brontabel zitten in de draaitabel',
    punten: 2,
    eis: { soort: 'draaitabel', veldenBevat: ['Verkoper', 'Filiaal', 'Maand'] },
    hint: 'Selecteer bij het maken de volledige tabel, zodat ook Verkoper als veld beschikbaar is.',
  },
];

export const draaiRapportChecks: BestandCheck[] = [
  {
    id: 'draaitabel',
    omschrijving: 'Draaitabel met Filiaal in de rijen en Productgroep in de kolommen',
    punten: 4,
    eis: { soort: 'draaitabel', minRijvelden: 1, minKolomvelden: 1, minGegevensvelden: 1 },
    hint: 'Filiaal naar Rijen, Productgroep naar Kolommen, Omzet naar Waarden.',
  },
  {
    id: 'grafiek',
    omschrijving: 'Er staat een grafiek bij',
    punten: 3,
    eis: { soort: 'grafiek', minAantal: 1 },
    hint: 'Klik in de draaitabel en kies Invoegen › Draaigrafiek.',
  },
  {
    id: 'grafiektitel',
    omschrijving: 'De grafiek heet "Omzet per filiaal"',
    punten: 2,
    eis: { soort: 'grafiek', titelBevat: 'Omzet per filiaal' },
    hint: 'Klik op de grafiektitel en pas hem aan.',
  },
  {
    id: 'printklaar',
    omschrijving: 'Liggend en op één pagina breed',
    punten: 1,
    eis: { soort: 'afdruk', liggend: true, passendBreed: 1 },
    hint: 'Pagina-indeling › Liggend, en Aanpassen aan › Breedte 1 pagina.',
  },
];
