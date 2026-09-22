import type { UploadOpgave } from '@/lib/werkblad-types';

/** Focus 7 — draaitabellen. Alleen echt Excel kan ze maken. */

const FILIALEN = ['Roeselare', 'Izegem', 'Kortrijk', 'Tielt'];
const MAANDEN = ['Januari', 'Februari', 'Maart'];
const GROEPEN = ['Ruwbouw', 'Sanitair', 'Isolatie', 'Dakwerk'];
const VERKOPERS = ['An Peeters', 'Bram De Smet', 'Cindy Vermeulen'];

/** Eén rij per verkooplijn: genoeg variatie om te kunnen draaien. */
function verkopen(): (string | number)[][] {
  const rijen: (string | number)[][] = [];
  let n = 0;
  for (const filiaal of FILIALEN) {
    for (const maand of MAANDEN) {
      for (const groep of GROEPEN) {
        n++;
        rijen.push([
          `V-${5000 + n}`,
          filiaal,
          maand,
          groep,
          VERKOPERS[n % VERKOPERS.length],
          8 + ((n * 5) % 40),
          Math.round((1200 + ((n * 317) % 4800)) * 100) / 100,
        ]);
      }
    }
  }
  return rijen;
}

const KOP = ['Ordernummer', 'Filiaal', 'Maand', 'Productgroep', 'Verkoper', 'Aantal', 'Omzet'];
const BREEDTES = [15, 14, 12, 16, 18, 10, 12];

function bron(titel: string) {
  return {
    bladnaam: 'Verkopen',
    breedtes: BREEDTES,
    rijen: [[titel], [], KOP, ...verkopen()],
  };
}

export const draaiEersteOpgave: UploadOpgave = {
  id: 'f7-eerste-draaitabel',
  titel: 'Je eerste draaitabel',
  focus: 'Focus 7 — een draaitabel maken',
  focusNummer: 7,
  volgnummer: 1,
  niveau: 2,
  soort: 'upload',
  leerdoel: 'Uit een lange lijst in enkele klikken een samenvatting halen.',
  stagecontext:
    'Achtenveertig verkooplijnen, en de vraag is simpel: hoeveel omzet per filiaal? ' +
    'Met SOM.ALS kan dat, maar een draaitabel doet het in vijf seconden.',
  opdrachten: [
    'Open het bestand in Excel en klik ergens in de tabel.',
    'Kies Invoegen › Draaitabel en plaats ze op een nieuw werkblad.',
    'Sleep Filiaal naar het gebied Rijen.',
    'Sleep Omzet naar het gebied Waarden.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: bron('Verkopen eerste kwartaal'),
};

export const draaiKruistabelOpgave: UploadOpgave = {
  id: 'f7-kruistabel',
  titel: 'Rijen en kolommen combineren',
  focus: 'Focus 7 — kruistabel',
  focusNummer: 7,
  volgnummer: 2,
  niveau: 3,
  soort: 'upload',
  leerdoel: 'Twee kenmerken tegelijk bekijken in één tabel.',
  stagecontext:
    'De zaakvoerder wil niet alleen de omzet per filiaal, maar per filiaal én per maand. ' +
    'Dat is precies waarvoor het kolomgebied bestaat.',
  opdrachten: [
    'Maak een draaitabel op een nieuw werkblad.',
    'Zet Filiaal in het gebied Rijen.',
    'Zet Maand in het gebied Kolommen.',
    'Zet Omzet in het gebied Waarden.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: bron('Verkopen eerste kwartaal — per filiaal en maand'),
};

export const draaiFunctieOpgave: UploadOpgave = {
  id: 'f7-samenvattingsfunctie',
  titel: 'Een andere samenvattingsfunctie',
  focus: 'Focus 7 — niet altijd optellen',
  focusNummer: 7,
  volgnummer: 3,
  niveau: 3,
  soort: 'upload',
  leerdoel: 'Kiezen wat de draaitabel met je cijfers doet: optellen, tellen of middelen.',
  stagecontext:
    'De vraag is niet hoeveel omzet er in totaal was, maar hoeveel orders er waren ' +
    'per productgroep. Dan moet je tellen in plaats van optellen.',
  opdrachten: [
    'Maak een draaitabel met Productgroep in de rijen.',
    'Zet Ordernummer in het gebied Waarden.',
    'Klik op het veld in Waarden en verander de functie naar Aantal.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: bron('Verkopen eerste kwartaal — aantal orders'),
};

export const draaiFilterOpgave: UploadOpgave = {
  id: 'f7-filteren',
  titel: 'Filteren in een draaitabel',
  focus: 'Focus 7 — filters',
  focusNummer: 7,
  volgnummer: 4,
  niveau: 4,
  soort: 'upload',
  leerdoel: 'Een deel van de gegevens bekijken zonder de brongegevens aan te raken.',
  stagecontext:
    'De verkoopleider wil het overzicht per verkoper kunnen bekijken, zonder telkens ' +
    'een nieuwe tabel te maken. Zet Verkoper in het filtergebied.',
  opdrachten: [
    'Maak een draaitabel met Productgroep in de rijen en Maand in de kolommen.',
    'Zet Omzet in het gebied Waarden.',
    'Zet Verkoper in het gebied Filters.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: bron('Verkopen eerste kwartaal — per verkoper'),
};

export const draaiRapportOpgave: UploadOpgave = {
  id: 'f7-draairapport',
  titel: 'Rapport met draaitabel en grafiek',
  focus: 'Focus 7 — alles samen',
  focusNummer: 7,
  volgnummer: 5,
  niveau: 5,
  soort: 'upload',
  leerdoel: 'Een volledig rapport bouwen: samenvatten, in beeld brengen, klaar om af te drukken.',
  stagecontext:
    'De eindproef. Uit deze ruwe verkooplijst maak je een rapport dat de zaakvoerder ' +
    'meteen begrijpt: een draaitabel met de cijfers, een grafiek erbij, en printklaar.',
  opdrachten: [
    'Maak een draaitabel met Filiaal in de rijen en Productgroep in de kolommen, en Omzet in de waarden.',
    'Voeg een grafiek toe op basis van die draaitabel (Invoegen › Draaigrafiek, of een gewone grafiek).',
    'Geef de grafiek de titel: Omzet per filiaal.',
    'Zet het blad met de draaitabel liggend en op één pagina breed.',
    'Sla op als .xlsx en laad het bestand hier op.',
  ],
  maxScore: 10,
  startbestand: bron('Verkopen eerste kwartaal — eindrapport'),
};
