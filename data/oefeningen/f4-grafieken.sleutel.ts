import 'server-only';
import type { BestandCheck } from '@/lib/nakijken-bestand';

const KOLOM = ['barChart', 'bar3DChart'];
const LIJN = ['lineChart', 'line3DChart'];
const CIRKEL = ['pieChart', 'pie3DChart', 'doughnutChart'];

export const staafChecks: BestandCheck[] = [
  {
    id: 'grafiek',
    omschrijving: 'Er staat een grafiek in het bestand',
    punten: 4,
    eis: { soort: 'grafiek', minAantal: 1 },
    hint: 'Selecteer de gegevens en kies Invoegen › Kolom.',
  },
  {
    id: 'type',
    omschrijving: 'Het is een kolom- of staafdiagram',
    punten: 3,
    eis: { soort: 'grafiek', types: KOLOM },
    hint: 'Een lijn of een cirkel is hier niet gevraagd. Kies Invoegen › Kolom.',
  },
  {
    id: 'titel',
    omschrijving: 'De grafiek heeft de gevraagde titel',
    punten: 3,
    eis: { soort: 'grafiek', titelBevat: 'Omzet per maand' },
    hint: 'Klik op de grafiektitel en typ: Omzet per maand.',
  },
];

export const lijnChecks: BestandCheck[] = [
  {
    id: 'type',
    omschrijving: 'Het is een lijndiagram',
    punten: 6,
    eis: { soort: 'grafiek', types: LIJN },
    hint: 'Een verloop in de tijd toon je met een lijn: Invoegen › Lijn.',
  },
  {
    id: 'titel',
    omschrijving: 'De grafiek heet "Verloop van de omzet"',
    punten: 4,
    eis: { soort: 'grafiek', types: LIJN, titelBevat: 'Verloop van de omzet' },
    hint: 'Klik op de titel van de grafiek en pas hem aan.',
  },
];

export const cirkelChecks: BestandCheck[] = [
  {
    id: 'type',
    omschrijving: 'Het is een cirkeldiagram',
    punten: 6,
    eis: { soort: 'grafiek', types: CIRKEL },
    hint: 'Aandelen van één geheel toon je met een cirkel: Invoegen › Cirkel.',
  },
  {
    id: 'titel',
    omschrijving: 'De grafiek heet "Aandeel per filiaal"',
    punten: 4,
    eis: { soort: 'grafiek', types: CIRKEL, titelBevat: 'Aandeel per filiaal' },
    hint: 'Klik op de titel van de grafiek en pas hem aan.',
  },
];

export const grafiekOpmaakChecks: BestandCheck[] = [
  {
    id: 'type',
    omschrijving: 'Kolomdiagram',
    punten: 3,
    eis: { soort: 'grafiek', types: KOLOM },
    hint: 'Invoegen › Kolom.',
  },
  {
    id: 'titel',
    omschrijving: 'Titel "Omzet eerste halfjaar 2026"',
    punten: 4,
    eis: { soort: 'grafiek', titelBevat: 'Omzet eerste halfjaar 2026' },
    hint: 'Klik op de grafiektitel en typ de gevraagde tekst.',
  },
  {
    id: 'gegevens',
    omschrijving: 'De grafiek haalt zijn cijfers uit de kolom Omzet',
    punten: 3,
    eis: { soort: 'grafiek', bereikBevat: '$B$' },
    hint: 'Selecteer bij het maken van de grafiek de kolom met de omzet, niet alleen de maanden.',
  },
];

export const tweeReeksenChecks: BestandCheck[] = [
  {
    id: 'type',
    omschrijving: 'Kolomdiagram',
    punten: 2,
    eis: { soort: 'grafiek', types: KOLOM },
    hint: 'Invoegen › Kolom.',
  },
  {
    id: 'twee-reeksen',
    omschrijving: 'Beide reeksen staan in de grafiek',
    punten: 5,
    eis: { soort: 'grafiek', minReeksen: 2 },
    hint: 'Selecteer bij het maken A3:C9, dus de maanden, de omzet én de kosten.',
  },
  {
    id: 'titel',
    omschrijving: 'Titel "Omzet tegenover kosten"',
    punten: 3,
    eis: { soort: 'grafiek', titelBevat: 'Omzet tegenover kosten' },
    hint: 'Klik op de grafiektitel en pas hem aan.',
  },
];
