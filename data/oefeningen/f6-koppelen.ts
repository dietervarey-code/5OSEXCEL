import { bouwWerkmap, rij, samen } from './bouwstenen';
import type { CelData, Opgave } from '@/lib/werkblad-types';

/**
 * Focus 6 — koppelen. Eén centrale bron, meerdere bladen die eruit putten.
 * Wijzigt de bron, dan wijzigt alles mee: dat is het hele punt.
 */

export const ARTIKELEN: [string, string, number][] = [
  ['SB-190', 'Snelbouwsteen 19 cm', 0.84],
  ['CM-225', 'Cement CEM II 25 kg', 7.95],
  ['IS-060', 'Isolatieplaat PIR 60 mm', 28.4],
  ['WN-150', 'Wapeningsnet 150/150', 42.5],
  ['GP-125', 'Gipsplaat 12,5 mm', 11.2],
  ['DZ-300', 'Dakgoot zink 3 m', 58],
];

const PRIJSLIJSTBLAD = {
  naam: 'Prijslijst',
  cellen: samen(
    { A1: { v: 'Centrale prijslijst', s: 'titel' } },
    { A2: { v: 'Wijzig hier een prijs en alles wat eraan gekoppeld is, volgt.' } },
    rij(3, 'A', ['Artikelcode', 'Omschrijving', 'Prijs'], 'kop'),
    ...ARTIKELEN.map(([code, oms, prijs], i) => rij(4 + i, 'A', [code, oms, prijs])),
  ) as Record<string, CelData>,
};

export const FILIALEN = ['Roeselare', 'Izegem', 'Kortrijk'];
export const FILIAALOMZET: Record<string, number[]> = {
  Roeselare: [12400, 13850, 11960],
  Izegem: [8700, 9240, 10110],
  Kortrijk: [15300, 14780, 16120],
};

const FILIAALBLADEN = FILIALEN.map((f) => ({
  naam: f,
  cellen: samen(
    { A1: { v: `Filiaal ${f}`, s: 'titel' } },
    rij(3, 'A', ['Maand', 'Omzet'], 'kop'),
    ...['Januari', 'Februari', 'Maart'].map((m, i) => rij(4 + i, 'A', [m, FILIAALOMZET[f][i]])),
    { A8: { v: 'Totaal', s: 'nadruk' }, B8: { v: FILIAALOMZET[f].reduce((s, n) => s + n, 0), s: 'totaal' } },
  ) as Record<string, CelData>,
}));

// --- 1 ---------------------------------------------------------------

export const koppelenPrijzenOpgave: Opgave = {
  id: 'f6-prijzen-koppelen',
  titel: 'Prijzen koppelen aan de centrale lijst',
  focus: 'Focus 6 — koppelen aan een bronblad',
  focusNummer: 6,
  volgnummer: 1,
  niveau: 2,
  leerdoel: 'Een prijs één keer bijhouden en overal laten meebewegen.',
  stagecontext:
    'De prijzen staan op het tabblad Prijslijst. In je bestelbon typ je ze niet over: je koppelt ' +
    'eraan. Wijzigt de leverancier zijn prijs, dan klopt je bon vanzelf nog.',
  opdrachten: [
    'Haal in C4 tot en met C9 de prijs op uit het blad Prijslijst. Let op: de artikelen staan in dezelfde volgorde.',
    'Bereken in D4 tot en met D9 het bedrag (aantal × prijs).',
    'Bereken in D11 het totaal met SOM.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f6-prijzen-koppelen', 'Bestelbon', samen(
    { A1: { v: 'Bestelbon 2026-118', s: 'titel' } },
    rij(3, 'A', ['Artikelcode', 'Aantal', 'Prijs', 'Bedrag'], 'kop'),
    ...ARTIKELEN.map(([code], i) => rij(4 + i, 'A', [code, [240, 80, 35, 12, 60, 8][i]])),
    { C11: { v: 'Totaal', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 8, extraBladen: [PRIJSLIJSTBLAD] }),
};

// --- 2 ---------------------------------------------------------------

export const koppelenZoekenOpgave: Opgave = {
  id: 'f6-koppelen-zoeken',
  titel: 'Koppelen met VERT.ZOEKEN',
  focus: 'Focus 6 — koppeling die blijft kloppen',
  focusNummer: 6,
  volgnummer: 2,
  niveau: 3,
  leerdoel: 'Koppelen op basis van de code in plaats van op de positie in de lijst.',
  stagecontext:
    'Deze bestelbon staat in een andere volgorde dan de prijslijst. Een gewone koppeling per rij ' +
    'gaat dus mis. Zoek op de artikelcode.',
  opdrachten: [
    'Haal in B4 tot en met B9 de omschrijving op met VERT.ZOEKEN naar het blad Prijslijst.',
    'Haal in C4 tot en met C9 de prijs op met VERT.ZOEKEN.',
    'Verwijs absoluut naar de tabel op het blad Prijslijst.',
    'Bereken in E4 tot en met E9 het bedrag.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f6-koppelen-zoeken', 'Bestelbon', samen(
    { A1: { v: 'Bestelbon 2026-119', s: 'titel' } },
    { A2: { v: 'De volgorde wijkt af van de prijslijst.' } },
    rij(3, 'A', ['Artikelcode', 'Omschrijving', 'Prijs', 'Aantal', 'Bedrag'], 'kop'),
    ...['DZ-300', 'SB-190', 'GP-125', 'CM-225', 'WN-150', 'IS-060'].map((code, i) =>
      rij(4 + i, 'A', [code, null, null, [6, 500, 40, 25, 10, 18][i]]),
    ),
  ), { rijen: 25, kolommen: 10, extraBladen: [PRIJSLIJSTBLAD] }),
};

// --- 3 ---------------------------------------------------------------

export const koppelenConsoliderenOpgave: Opgave = {
  id: 'f6-consolideren',
  titel: 'Drie filialen samenbrengen',
  focus: 'Focus 6 — consolideren',
  focusNummer: 6,
  volgnummer: 3,
  niveau: 3,
  leerdoel: 'Cijfers van meerdere bladen samenbrengen in één overzicht.',
  stagecontext:
    'Elk filiaal houdt zijn eigen tabblad bij. Maak het overzicht waarmee de zaakvoerder ' +
    'naar de bank gaat.',
  opdrachten: [
    'Haal in B4 tot en met D6 de maandomzet van elk filiaal op uit de drie filiaalbladen.',
    'Bereken in E4 tot en met E6 het kwartaaltotaal per filiaal.',
    'Bereken in B7 tot en met E7 de totalen per maand en het eindtotaal.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f6-consolideren', 'Consolidatie', samen(
    { A1: { v: 'Omzet per filiaal — eerste kwartaal', s: 'titel' } },
    rij(3, 'A', ['Filiaal', 'Januari', 'Februari', 'Maart', 'Kwartaal'], 'kop'),
    ...FILIALEN.map((f, i) => rij(4 + i, 'A', [f])),
    { A7: { v: 'Alle filialen', s: 'totaal' } },
  ), { rijen: 25, kolommen: 8, extraBladen: FILIAALBLADEN }),
};

// --- 4 ---------------------------------------------------------------

export const koppelenHerstellenOpgave: Opgave = {
  id: 'f6-herstellen',
  titel: 'Een kapotte koppeling herstellen',
  focus: 'Focus 6 — koppelingen controleren',
  focusNummer: 6,
  volgnummer: 4,
  niveau: 4,
  leerdoel: 'Herkennen waarom een koppeling misgaat, en ze repareren.',
  stagecontext:
    'Een collega heeft dit overzicht gemaakt, maar er klopt iets niet. Drie cellen verwijzen ' +
    'naar de verkeerde plaats. Zoek ze en zet ze recht.',
  opdrachten: [
    'Controleer in B4 tot en met B6 of elke cel de omzet van het juiste filiaal ophaalt.',
    'Herstel de verwijzingen die fout staan. Het totaal van elk filiaal staat in cel B8 van zijn blad.',
    'Bereken in B8 het totaal van de drie filialen.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f6-herstellen', 'Overzicht', samen(
    { A1: { v: 'Overzicht filialen — nakijken', s: 'titel' } },
    { A2: { v: 'Er zitten fouten in de verwijzingen.' } },
    rij(3, 'A', ['Filiaal', 'Kwartaalomzet'], 'kop'),
    // Bewust fout: verwijst naar B4 (één maand) in plaats van B8 (het totaal),
    // en het derde filiaal wijst naar het verkeerde blad.
    { A4: { v: 'Roeselare' }, B4: { f: '=Roeselare!B4' } },
    { A5: { v: 'Izegem' }, B5: { f: '=Izegem!B5' } },
    { A6: { v: 'Kortrijk' }, B6: { f: '=Izegem!B8' } },
    { A8: { v: 'Totaal', s: 'nadruk' } },
  ), { rijen: 25, kolommen: 8, extraBladen: FILIAALBLADEN }),
};

// --- 5 ---------------------------------------------------------------

export const koppelenFactuurOpgave: Opgave = {
  id: 'f6-gekoppelde-factuur',
  titel: 'Een volledig gekoppelde factuur',
  focus: 'Focus 6 — alles samen',
  focusNummer: 6,
  volgnummer: 5,
  niveau: 5,
  leerdoel: 'Een factuur bouwen waarin geen enkel gegeven dubbel staat.',
  stagecontext:
    'De eindproef van dit blok. Bouw een factuur die haar omschrijvingen en prijzen uit de ' +
    'prijslijst haalt, korting toekent vanaf een drempel, en btw berekent. Niets overtypen.',
  opdrachten: [
    'Haal in B5 tot en met B9 de omschrijving op uit het blad Prijslijst, met VERT.ZOEKEN.',
    'Haal in C5 tot en met C9 de prijs op.',
    'Bereken in E5 tot en met E9 het bedrag per lijn (aantal × prijs).',
    'Bereken in E11 het subtotaal met SOM.',
    'Bereken in E12 de korting: 5% als het subtotaal boven 1000 ligt, anders niets.',
    'Bereken in E13 de btw op het bedrag na korting, met het tarief uit B15.',
    'Bereken in E14 het totaal te betalen.',
  ],
  vergrendeld: [],
  maxScore: 10,
  werkmap: bouwWerkmap('f6-gekoppelde-factuur', 'Factuur', samen(
    { A1: { v: 'Factuur 2026-0203', s: 'titel' } },
    rij(4, 'A', ['Artikelcode', 'Omschrijving', 'Prijs', 'Aantal', 'Bedrag'], 'kop'),
    ...['SB-190', 'CM-225', 'IS-060', 'GP-125', 'DZ-300'].map((code, i) =>
      rij(5 + i, 'A', [code, null, null, [600, 45, 22, 80, 9][i]]),
    ),
    { D11: { v: 'Subtotaal', s: 'kop' } },
    { D12: { v: 'Korting', s: 'kop' } },
    { D13: { v: 'Btw', s: 'kop' } },
    { D14: { v: 'Totaal te betalen', s: 'totaal' } },
    { A15: { v: 'Btw-tarief' }, B15: { v: 0.21, s: 'invoer' } },
    { A16: { v: 'Kortingsdrempel' }, B16: { v: 1000, s: 'invoer' } },
    { A17: { v: 'Kortingspercentage' }, B17: { v: 0.05, s: 'invoer' } },
  ), { rijen: 30, kolommen: 10, extraBladen: [PRIJSLIJSTBLAD] }),
};
