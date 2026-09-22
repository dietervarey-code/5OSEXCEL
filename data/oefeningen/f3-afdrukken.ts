import type { UploadOpgave } from '@/lib/werkblad-types';

/** Focus 3 — afdrukken. In echt Excel, want een browser kent geen pagina's. */

const KLANTEN = ['Maes', 'Verbeke', 'Six', 'Lievens', 'Vandaele', 'Dobbels', 'Groen', 'Top'];
const ARTIKELEN = ['Snelbouwsteen', 'Cement', 'Isolatieplaat', 'Wapeningsnet', 'Gipsplaat', 'Dakgoot'];

/** Een lange, brede lijst: alleen dan heeft afdrukken betekenis. */
function leveringen(aantal: number): (string | number)[][] {
  return Array.from({ length: aantal }, (_, i) => [
    `L-${4100 + i}`,
    KLANTEN[i % KLANTEN.length],
    ARTIKELEN[i % ARTIKELEN.length],
    `2026-09-${String((i % 28) + 1).padStart(2, '0')}`,
    12 + ((i * 7) % 90),
    Math.round((7.95 + (i % 9) * 4.3) * 100) / 100,
    Math.round((12 + ((i * 7) % 90)) * (7.95 + (i % 9) * 4.3) * 100) / 100,
  ]);
}

const KOP = ['Leveringsnummer', 'Klant', 'Artikel', 'Datum', 'Aantal', 'Eenheidsprijs', 'Bedrag'];
const BREEDTES = [18, 14, 18, 12, 10, 15, 14];

function lijst(titel: string, aantal: number) {
  return {
    bladnaam: 'Leveringen',
    breedtes: BREEDTES,
    rijen: [[titel], [], KOP, ...leveringen(aantal)],
  };
}

export const afdrukStandOpgave: UploadOpgave = {
  id: 'f3-stand-en-marges',
  titel: 'Staand of liggend, en de marges',
  focus: 'Focus 3 — afdrukstand en marges',
  focusNummer: 3,
  volgnummer: 1,
  niveau: 1,
  soort: 'upload',
  leerdoel: 'Een brede tabel zo instellen dat ze niet half naast de pagina valt.',
  stagecontext:
    'De zaakvoerder wil deze lijst op papier. Zoals ze nu staat, valt de kolom Bedrag ' +
    'op een tweede pagina. Zet het blad liggend en maak de marges smaller.',
  opdrachten: [
    'Open het bestand in Excel.',
    'Zet het blad in liggende stand (Pagina-indeling › Afdrukstand › Liggend).',
    'Zet de marges op Smal (Pagina-indeling › Marges › Smal).',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: lijst('Leveringen september — af te drukken', 30),
};

export const afdrukPassendOpgave: UploadOpgave = {
  id: 'f3-passend-maken',
  titel: 'Alles op één pagina breed',
  focus: 'Focus 3 — schalen en passend maken',
  focusNummer: 3,
  volgnummer: 2,
  niveau: 2,
  soort: 'upload',
  leerdoel: 'Een tabel laten krimpen tot ze in de breedte past, zonder kolommen te verbergen.',
  stagecontext:
    'Liggend zetten volstaat niet: de tabel is te breed. Zorg dat alle kolommen op één ' +
    'pagina breed komen, maar laat het in de hoogte over meerdere pagina’s lopen.',
  opdrachten: [
    'Zet het blad liggend.',
    'Ga naar Pagina-indeling › Aanpassen aan.',
    'Zet "Breedte" op 1 pagina en laat "Hoogte" op Automatisch staan.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: lijst('Leveringen september — passend maken', 45),
};

export const afdrukKopVoetOpgave: UploadOpgave = {
  id: 'f3-kop-en-voettekst',
  titel: 'Kop- en voettekst met paginanummer',
  focus: 'Focus 3 — kop- en voettekst',
  focusNummer: 3,
  volgnummer: 3,
  niveau: 2,
  soort: 'upload',
  leerdoel: 'Elke afgedrukte pagina voorzien van een titel en een paginanummer.',
  stagecontext:
    'Een rapport van tien pagina’s dat op de grond valt, moet te sorteren zijn. ' +
    'Zet er een koptekst en een paginanummer op.',
  opdrachten: [
    'Zet in de koptekst in het midden: Leveringen september.',
    'Zet in de voettekst rechts het paginanummer, met het totaal aantal pagina’s (Pagina &P van &N).',
    'Zet het blad liggend.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: lijst('Leveringen september — rapport', 40),
};

export const afdrukTitelrijenOpgave: UploadOpgave = {
  id: 'f3-titelrijen',
  titel: 'Titelrijen op elke pagina herhalen',
  focus: 'Focus 3 — titels herhalen',
  focusNummer: 3,
  volgnummer: 4,
  niveau: 3,
  soort: 'upload',
  leerdoel: 'De koptekst op elke afgedrukte pagina laten terugkomen.',
  stagecontext:
    'Op pagina drie van de afdruk weet niemand nog welke kolom het aantal was en welke ' +
    'de prijs. Laat de koprij op elke pagina terugkomen.',
  opdrachten: [
    'Ga naar Pagina-indeling › Afdruktitels.',
    'Stel in dat rij 3 boven aan elke pagina herhaald wordt.',
    'Zet het blad liggend en alles op één pagina breed.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: lijst('Leveringen september — titels herhalen', 60),
};

export const afdrukRapportOpgave: UploadOpgave = {
  id: 'f3-printklaar-rapport',
  titel: 'Een printklaar rapport',
  focus: 'Focus 3 — alles samen',
  focusNummer: 3,
  volgnummer: 5,
  niveau: 4,
  soort: 'upload',
  leerdoel: 'Een lijst volledig klaarmaken om af te drukken en door te geven.',
  stagecontext:
    'De eindproef van dit blok. Deze lijst moet morgen op de vergadering liggen. ' +
    'Zorg dat ze er verzorgd uitkomt, op elke pagina leesbaar, en met paginanummers.',
  opdrachten: [
    'Zet het blad liggend, met smalle marges.',
    'Maak alles passend op één pagina breed.',
    'Herhaal rij 3 boven aan elke pagina.',
    'Zet een koptekst met de titel en een voettekst met Pagina &P van &N.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: lijst('Leveringen september — eindrapport', 75),
};
