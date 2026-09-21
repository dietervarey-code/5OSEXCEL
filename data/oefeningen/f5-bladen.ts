import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { CelData, Opgave } from '@/lib/werkblad-types';

/**
 * Focus 5 — meerdere werkbladen. De maandbladen hebben allemaal dezelfde
 * opbouw, zodat een verwijzing naar D10 op elk blad hetzelfde betekent.
 */

export const FILIALEN = ['Roeselare', 'Izegem', 'Kortrijk', 'Tielt'];

export const MAANDCIJFERS: Record<string, number[]> = {
  Januari: [24500, 18700, 31200, 14900],
  Februari: [21870, 19450, 28960, 16240],
  Maart: [26340, 22110, 33480, 15870],
};

/** Bouwt één maandblad: filialen met omzet en een totaal in D10. */
function maandblad(maand: string): Record<string, CelData> {
  const cijfers = MAANDCIJFERS[maand];
  return samen(
    { A1: { v: `Omzet ${maand}`, s: 'titel' } },
    rij(3, 'A', ['Filiaal', 'Aantal orders', 'Gemiddelde order', 'Omzet'], 'kop'),
    ...FILIALEN.map((f, i) =>
      rij(4 + i, 'A', [f, 40 + i * 7, Math.round((cijfers[i] / (40 + i * 7)) * 100) / 100, cijfers[i]]),
    ),
    { C10: { v: 'Totaal', s: 'nadruk' }, D10: { v: cijfers.reduce((s, n) => s + n, 0), s: 'totaal' } },
  );
}

const MAANDBLADEN = Object.keys(MAANDCIJFERS).map((m) => ({ naam: m, cellen: maandblad(m) }));

// --- Oefening 1 -------------------------------------------------------

export const bladenOphalenOpgave: Opgave = {
  id: 'f5-bladen-ophalen',
  titel: 'Cijfers van een ander blad ophalen',
  focus: 'Focus 5 — verwijzen naar een ander werkblad',
  focusNummer: 5,
  volgnummer: 1,
  niveau: 2,
  leerdoel: 'Een verwijzing schrijven die over de bladgrens heen kijkt.',
  stagecontext:
    'Elke maand heeft een eigen tabblad. Op het overzichtsblad wil de zaakvoerder de drie ' +
    'maandtotalen naast elkaar zien, zonder ze over te typen.',
  opdrachten: [
    'Haal in B4 het maandtotaal van januari op. Dat staat in cel D10 van het blad Januari.',
    'Doe hetzelfde in B5 voor februari en in B6 voor maart.',
    'Bereken in B8 het kwartaaltotaal met SOM.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f5-bladen-ophalen', 'Overzicht', samen(
    { A1: { v: 'Kwartaaloverzicht', s: 'titel' } },
    { A2: { v: 'De cijfers staan op de tabbladen Januari, Februari en Maart.' } },
    rij(3, 'A', ['Maand', 'Omzet'], 'kop'),
    { A4: { v: 'Januari' }, A5: { v: 'Februari' }, A6: { v: 'Maart' } },
    { A8: { v: 'Kwartaaltotaal', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 8, extraBladen: MAANDBLADEN }),
};

// --- Oefening 2 -------------------------------------------------------

export const bladenFiliaalOpgave: Opgave = {
  id: 'f5-bladen-filiaal',
  titel: 'Eén filiaal over drie maanden volgen',
  focus: 'Focus 5 — dezelfde cel op meerdere bladen',
  focusNummer: 5,
  volgnummer: 2,
  niveau: 3,
  leerdoel: 'Dezelfde positie op verschillende bladen optellen en vergelijken.',
  stagecontext:
    'Het filiaal Kortrijk draait goed. De zaakvoerder wil per maand zien wat het opbracht, ' +
    'en wat het aandeel is in de totale omzet.',
  opdrachten: [
    'Haal in B4 tot en met B6 de omzet van Kortrijk op uit de drie maandbladen. Kortrijk staat telkens in rij 6.',
    'Bereken in B8 de totale omzet van Kortrijk over het kwartaal.',
    'Bereken in B9 het aandeel van Kortrijk in het kwartaaltotaal van alle filialen, als percentage.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f5-bladen-filiaal', 'Kortrijk', samen(
    { A1: { v: 'Filiaal Kortrijk — kwartaal', s: 'titel' } },
    rij(3, 'A', ['Maand', 'Omzet Kortrijk'], 'kop'),
    { A4: { v: 'Januari' }, A5: { v: 'Februari' }, A6: { v: 'Maart' } },
    { A8: { v: 'Totaal Kortrijk', s: 'nadruk' } },
    { A9: { v: 'Aandeel in alle filialen', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 8, extraBladen: MAANDBLADEN }),
};

// --- Oefening 3 -------------------------------------------------------

export const bladenVerschilOpgave: Opgave = {
  id: 'f5-bladen-verschil',
  titel: 'Twee maanden met elkaar vergelijken',
  focus: 'Focus 5 — rekenen met cellen van verschillende bladen',
  focusNummer: 5,
  volgnummer: 3,
  niveau: 3,
  leerdoel: 'Twee bladen in één formule combineren en de groei uitrekenen.',
  stagecontext:
    'Februari was een zwakke maand. Zet per filiaal naast elkaar wat januari en maart opbrachten, ' +
    'en hoeveel het verschil is.',
  opdrachten: [
    'Haal in B4 tot en met B7 de omzet van januari per filiaal op.',
    'Haal in C4 tot en met C7 de omzet van maart per filiaal op.',
    'Bereken in D4 tot en met D7 het verschil tussen maart en januari.',
    'Bereken in E4 tot en met E7 de groei in procent ten opzichte van januari.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f5-bladen-verschil', 'Vergelijking', samen(
    { A1: { v: 'Januari tegenover maart', s: 'titel' } },
    rij(3, 'A', ['Filiaal', 'Januari', 'Maart', 'Verschil', 'Groei'], 'kop'),
    ...FILIALEN.map((f, i) => rij(4 + i, 'A', [f])),
  ), { rijen: 25, kolommen: 8, extraBladen: MAANDBLADEN }),
};

// --- Oefening 4 -------------------------------------------------------

export const bladenGemiddeldeOpgave: Opgave = {
  id: 'f5-bladen-gemiddelde',
  titel: 'Gemiddelde en uitschieters over drie bladen',
  focus: 'Focus 5 — functies over meerdere bladen',
  focusNummer: 5,
  volgnummer: 4,
  niveau: 3,
  leerdoel: 'MAX, MIN en GEMIDDELDE gebruiken op cellen die op verschillende bladen staan.',
  stagecontext:
    'Voor de evaluatie wil de zaakvoerder per filiaal het gemiddelde, de beste en de slechtste ' +
    'maand kennen.',
  opdrachten: [
    'Bereken in B4 tot en met B7 de gemiddelde maandomzet per filiaal, over de drie maandbladen.',
    'Bereken in C4 tot en met C7 de beste maand met MAX.',
    'Bereken in D4 tot en met D7 de zwakste maand met MIN.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f5-bladen-gemiddelde', 'Analyse', samen(
    { A1: { v: 'Analyse per filiaal', s: 'titel' } },
    rij(3, 'A', ['Filiaal', 'Gemiddelde', 'Beste maand', 'Zwakste maand'], 'kop'),
    ...FILIALEN.map((f, i) => rij(4 + i, 'A', [f])),
  ), { rijen: 25, kolommen: 8, extraBladen: MAANDBLADEN }),
};

// --- Oefening 5 -------------------------------------------------------

export const bladenZoekenOpgave: Opgave = {
  id: 'f5-bladen-zoeken',
  titel: 'Opzoeken op een ander werkblad',
  focus: 'Focus 5 & 8 — VERT.ZOEKEN over de bladgrens',
  focusNummer: 5,
  volgnummer: 5,
  niveau: 4,
  leerdoel: 'Een zoektabel op een ander blad aanspreken, zodat je hoofdblad overzichtelijk blijft.',
  stagecontext:
    'Je overzicht moet netjes blijven, dus de gegevens staan op aparte bladen. Haal met ' +
    'VERT.ZOEKEN het aantal orders en de gemiddelde order van maart op.',
  opdrachten: [
    'Haal in B4 tot en met B7 het aantal orders van maart op met VERT.ZOEKEN naar het blad Maart.',
    'Haal in C4 tot en met C7 de gemiddelde order van maart op, uit dezelfde tabel.',
    'Verwijs absoluut naar de tabel op het blad Maart.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f5-bladen-zoeken', 'Maartrapport', samen(
    { A1: { v: 'Rapport maart', s: 'titel' } },
    { A2: { v: 'De brongegevens staan op het tabblad Maart, in A4:D7.' } },
    rij(3, 'A', ['Filiaal', 'Aantal orders', 'Gemiddelde order'], 'kop'),
    ...FILIALEN.map((f, i) => rij(4 + i, 'A', [f])),
  ), { rijen: 25, kolommen: 8, extraBladen: MAANDBLADEN }),
};
