import type { UploadOpgave } from '@/lib/werkblad-types';

/** Focus 4 — grafieken. In echt Excel gemaakt en hier nagekeken. */

const MAANDEN = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni'];
const OMZET = [24500, 21870, 26340, 23180, 27960, 25410];
const KOSTEN = [19800, 18900, 20400, 19100, 21300, 20050];

export const staafOpgave: UploadOpgave = {
  id: 'f4-staafdiagram',
  titel: 'Een staafdiagram maken',
  focus: 'Focus 4 — je eerste grafiek',
  focusNummer: 4,
  volgnummer: 1,
  niveau: 1,
  soort: 'upload',
  leerdoel: 'Van een tabel een grafiek maken, met de juiste gegevens erin.',
  stagecontext:
    'De zaakvoerder wil de omzet per maand in beeld. Een tabel met cijfers leest hij niet; ' +
    'een grafiek wel.',
  opdrachten: [
    'Open het bestand in Excel.',
    'Selecteer A3:B9, dus de maanden én de omzet, met de koptekst erbij.',
    'Voeg een kolomdiagram in (Invoegen › Kolom).',
    'Geef de grafiek de titel: Omzet per maand.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: {
    bladnaam: 'Omzet',
    breedtes: [14, 14, 14],
    rijen: [['Omzet eerste halfjaar'], [], ['Maand', 'Omzet'], ...MAANDEN.map((m, i) => [m, OMZET[i]])],
  },
};

export const lijnOpgave: UploadOpgave = {
  id: 'f4-lijndiagram',
  titel: 'Het juiste type kiezen: verloop in de tijd',
  focus: 'Focus 4 — grafiektype',
  focusNummer: 4,
  volgnummer: 2,
  niveau: 2,
  soort: 'upload',
  leerdoel: 'Weten wanneer een lijn beter is dan een staaf.',
  stagecontext:
    'De vraag is niet meer "hoeveel per maand" maar "gaat het de goede kant op". ' +
    'Dan hoort er een lijndiagram, want een lijn toont een verloop.',
  opdrachten: [
    'Selecteer de maanden en de omzet.',
    'Voeg een lijndiagram in (Invoegen › Lijn).',
    'Geef de grafiek de titel: Verloop van de omzet.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: {
    bladnaam: 'Omzet',
    breedtes: [14, 14],
    rijen: [['Omzet eerste halfjaar'], [], ['Maand', 'Omzet'], ...MAANDEN.map((m, i) => [m, OMZET[i]])],
  },
};

export const cirkelOpgave: UploadOpgave = {
  id: 'f4-cirkeldiagram',
  titel: 'Verhoudingen tonen met een cirkeldiagram',
  focus: 'Focus 4 — verhoudingen',
  focusNummer: 4,
  volgnummer: 3,
  niveau: 2,
  soort: 'upload',
  leerdoel: 'Een cirkeldiagram gebruiken waar het thuishoort: delen van één geheel.',
  stagecontext:
    'De zaakvoerder wil zien hoe de omzet verdeeld is over de vier filialen. ' +
    'Het gaat om aandelen van één totaal, en daar is een cirkeldiagram voor.',
  opdrachten: [
    'Selecteer de filialen en hun omzet.',
    'Voeg een cirkeldiagram in (Invoegen › Cirkel).',
    'Geef de grafiek de titel: Aandeel per filiaal.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: {
    bladnaam: 'Filialen',
    breedtes: [16, 14],
    rijen: [
      ['Omzet per filiaal — eerste kwartaal'], [], ['Filiaal', 'Omzet'],
      ['Roeselare', 72600], ['Izegem', 53400], ['Kortrijk', 91200], ['Tielt', 38700],
    ],
  },
};

export const grafiekOpmaakOpgave: UploadOpgave = {
  id: 'f4-grafiek-opmaken',
  titel: 'Een grafiek afwerken',
  focus: 'Focus 4 — titel en leesbaarheid',
  focusNummer: 4,
  volgnummer: 4,
  niveau: 3,
  soort: 'upload',
  leerdoel: 'Een grafiek zo afwerken dat ze zonder uitleg te begrijpen is.',
  stagecontext:
    'Een grafiek zonder titel zegt niets. Deze gaat mee in een rapport naar de bank, ' +
    'dus alles moet erop staan wat een buitenstaander nodig heeft.',
  opdrachten: [
    'Maak een kolomdiagram van de omzet per maand.',
    'Geef het de titel: Omzet eerste halfjaar 2026.',
    'Zorg dat de maanden onder de staven staan als categorieën, niet als een tweede reeks.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: {
    bladnaam: 'Omzet',
    breedtes: [14, 14],
    rijen: [['Omzet eerste halfjaar 2026'], [], ['Maand', 'Omzet'], ...MAANDEN.map((m, i) => [m, OMZET[i]])],
  },
};

export const tweeReeksenOpgave: UploadOpgave = {
  id: 'f4-twee-reeksen',
  titel: 'Twee reeksen in één grafiek',
  focus: 'Focus 4 — vergelijken',
  focusNummer: 4,
  volgnummer: 5,
  niveau: 4,
  soort: 'upload',
  leerdoel: 'Twee gegevensreeksen naast elkaar tonen om ze te vergelijken.',
  stagecontext:
    'Omzet alleen zegt weinig zolang je de kosten er niet naast legt. Zet beide in ' +
    'één grafiek, zodat je ziet waar de marge krimpt.',
  opdrachten: [
    'Selecteer de maanden, de omzet én de kosten.',
    'Voeg een kolomdiagram in met beide reeksen.',
    'Geef het de titel: Omzet tegenover kosten.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: {
    bladnaam: 'Resultaat',
    breedtes: [14, 14, 14],
    rijen: [
      ['Omzet en kosten eerste halfjaar'], [], ['Maand', 'Omzet', 'Kosten'],
      ...MAANDEN.map((m, i) => [m, OMZET[i], KOSTEN[i]]),
    ],
  },
};
