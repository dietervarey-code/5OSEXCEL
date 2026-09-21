import 'server-only';
import type { Check } from '@/lib/nakijken';
import { FILIALEN, MAANDCIJFERS } from './f5-bladen';

const JAN = MAANDCIJFERS.Januari;
const FEB = MAANDCIJFERS.Februari;
const MRT = MAANDCIJFERS.Maart;
const totaal = (a: number[]) => a.reduce((s, n) => s + n, 0);

/** Elke formule moet naar een ander blad wijzen — dat is de kern van Focus 5. */
const BLADVERWIJZING = { patroon: "(Januari|Februari|Maart|'Januari'|'Februari'|'Maart')\\s*!", uitleg: 'verwijs naar het andere blad met bijvoorbeeld Januari!D10' };

export const bladenOphalenChecks: Check[] = [
  {
    id: 'maandtotalen',
    omschrijving: 'De drie maandtotalen van het juiste blad gehaald',
    punten: 6,
    cellen: ['B4', 'B5', 'B6'],
    verwachteWaarden: [totaal(JAN), totaal(FEB), totaal(MRT)],
    formulePatronen: [BLADVERWIJZING],
    hint: 'Typ in B4 de formule =Januari!D10. Je kunt ook = typen, op het tabblad Januari klikken, cel D10 aanklikken en op Enter drukken.',
  },
  {
    id: 'kwartaal',
    omschrijving: 'Kwartaaltotaal met SOM',
    punten: 4,
    cellen: ['B8'],
    verwachteWaarden: [totaal(JAN) + totaal(FEB) + totaal(MRT)],
    formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM over B4:B6' }],
    hint: 'Gebruik =SOM(B4:B6).',
  },
];

const KORTRIJK = FILIALEN.indexOf('Kortrijk');
const KORTRIJK_RIJ = 4 + KORTRIJK;
const KORTRIJK_CIJFERS = [JAN[KORTRIJK], FEB[KORTRIJK], MRT[KORTRIJK]];
const ALLES = totaal(JAN) + totaal(FEB) + totaal(MRT);

export const bladenFiliaalChecks: Check[] = [
  {
    id: 'per-maand',
    omschrijving: 'Omzet van Kortrijk per maand opgehaald',
    punten: 5,
    cellen: ['B4', 'B5', 'B6'],
    verwachteWaarden: KORTRIJK_CIJFERS,
    formulePatronen: [BLADVERWIJZING],
    hint: `Kortrijk staat op elk maandblad in rij ${KORTRIJK_RIJ}. Gebruik =Januari!D${KORTRIJK_RIJ}.`,
  },
  {
    id: 'totaal',
    omschrijving: 'Totaal van Kortrijk over het kwartaal',
    punten: 3,
    cellen: ['B8'],
    verwachteWaarden: [totaal(KORTRIJK_CIJFERS)],
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =SOM(B4:B6).',
  },
  {
    id: 'aandeel',
    omschrijving: 'Aandeel van Kortrijk in de totale omzet',
    punten: 2,
    cellen: ['B9'],
    verwachteWaarden: [totaal(KORTRIJK_CIJFERS) / ALLES],
    tolerantie: 0.002,
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Deel het totaal van Kortrijk door het totaal van alle filialen, en geef de cel de notatie percentage.',
  },
];

const VERSCHIL = FILIALEN.map((_, i) => MRT[i] - JAN[i]);
const GROEI = FILIALEN.map((_, i) => (MRT[i] - JAN[i]) / JAN[i]);
const cellen = (kolom: string) => FILIALEN.map((_, i) => `${kolom}${4 + i}`);

export const bladenVerschilChecks: Check[] = [
  {
    id: 'januari',
    omschrijving: 'Omzet van januari per filiaal opgehaald',
    punten: 3,
    cellen: cellen('B'),
    verwachteWaarden: JAN,
    formulePatronen: [BLADVERWIJZING],
    hint: 'Gebruik =Januari!D4 en voer door.',
  },
  {
    id: 'maart',
    omschrijving: 'Omzet van maart per filiaal opgehaald',
    punten: 3,
    cellen: cellen('C'),
    verwachteWaarden: MRT,
    formulePatronen: [BLADVERWIJZING],
    hint: 'Gebruik =Maart!D4 en voer door.',
  },
  {
    id: 'verschil',
    omschrijving: 'Verschil tussen maart en januari',
    punten: 2,
    cellen: cellen('D'),
    verwachteWaarden: VERSCHIL,
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =C4-B4.',
  },
  {
    id: 'groei',
    omschrijving: 'Groei in procent ten opzichte van januari',
    punten: 2,
    cellen: cellen('E'),
    verwachteWaarden: GROEI,
    tolerantie: 0.002,
    formulePatronen: [{ patroon: '^=', uitleg: 'reken dit uit met een formule' }],
    hint: 'Gebruik =(C4-B4)/B4 en geef de kolom de notatie percentage.',
  },
];

const GEMIDDELDEN = FILIALEN.map((_, i) => (JAN[i] + FEB[i] + MRT[i]) / 3);
const BESTE = FILIALEN.map((_, i) => Math.max(JAN[i], FEB[i], MRT[i]));
const ZWAKSTE = FILIALEN.map((_, i) => Math.min(JAN[i], FEB[i], MRT[i]));

export const bladenGemiddeldeChecks: Check[] = [
  {
    id: 'gemiddelde',
    omschrijving: 'Gemiddelde maandomzet per filiaal',
    punten: 4,
    cellen: cellen('B'),
    verwachteWaarden: GEMIDDELDEN,
    tolerantie: 0.5,
    formulePatronen: [
      { patroon: '^=\\s*GEMIDDELDE\\s*\\(', uitleg: 'gebruik GEMIDDELDE' },
      BLADVERWIJZING,
    ],
    hint: 'Gebruik =GEMIDDELDE(Januari!D4;Februari!D4;Maart!D4).',
  },
  {
    id: 'beste',
    omschrijving: 'Beste maand met MAX',
    punten: 3,
    cellen: cellen('C'),
    verwachteWaarden: BESTE,
    formulePatronen: [{ patroon: '^=\\s*MAX\\s*\\(', uitleg: 'gebruik MAX' }, BLADVERWIJZING],
    hint: 'Gebruik =MAX(Januari!D4;Februari!D4;Maart!D4).',
  },
  {
    id: 'zwakste',
    omschrijving: 'Zwakste maand met MIN',
    punten: 3,
    cellen: cellen('D'),
    verwachteWaarden: ZWAKSTE,
    formulePatronen: [{ patroon: '^=\\s*MIN\\s*\\(', uitleg: 'gebruik MIN' }, BLADVERWIJZING],
    hint: 'Gebruik =MIN(Januari!D4;Februari!D4;Maart!D4).',
  },
];

const ORDERS = FILIALEN.map((_, i) => 40 + i * 7);
const GEMIDDELDE_ORDER = FILIALEN.map((_, i) => Math.round((MRT[i] / ORDERS[i]) * 100) / 100);

export const bladenZoekenChecks: Check[] = [
  {
    id: 'orders',
    omschrijving: 'Aantal orders opgehaald met VERT.ZOEKEN van het blad Maart',
    punten: 5,
    cellen: cellen('B'),
    verwachteWaarden: ORDERS,
    formulePatronen: [
      { patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' },
      BLADVERWIJZING,
    ],
    hint: 'Gebruik =VERT.ZOEKEN(A4;Maart!$A$4:$D$7;2;ONWAAR).',
  },
  {
    id: 'gemiddelde-order',
    omschrijving: 'Gemiddelde order opgehaald uit dezelfde tabel',
    punten: 5,
    cellen: cellen('C'),
    verwachteWaarden: GEMIDDELDE_ORDER,
    tolerantie: 0.02,
    formulePatronen: [
      { patroon: 'VERT\\.ZOEKEN\\s*\\(', uitleg: 'gebruik VERT.ZOEKEN' },
      { patroon: '\\$A\\$4\\s*:\\s*\\$D\\$7|\\$A\\$\\d+\\s*:\\s*\\$D\\$\\d+', uitleg: 'verwijs absoluut naar de tabel op het blad Maart' },
    ],
    hint: 'Zelfde formule, maar met kolomnummer 3.',
  },
];
