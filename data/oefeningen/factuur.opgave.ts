import { bouwCellData, type Opgave } from '@/lib/werkblad-types';

/**
 * PUBLIEKE opgave — deze data gaat naar de browser.
 * De oplossing staat in factuur.sleutel.ts en blijft op de server.
 *
 * Stagetaak: een uitgaande factuur vervolledigen. Raakt Focus 1 (getalnotatie,
 * celopmaak) en Focus 2 (SOM, absolute celverwijzing, BTW-berekening).
 */

const OPMAAK = {
  titel: { bl: 1, fs: 16 },
  kop: { bl: 1, bg: { rgb: '#E8EEF7' } },
  totaal: { bl: 1, bd: { t: { s: 1, cl: { rgb: '#000000' } } } },
} as const;

export const factuurOpgave: Opgave = {
  id: 'factuur-basis',
  titel: 'Factuur vervolledigen',
  focus: 'Focus 1 & 2 — getalnotatie, SOM, absolute celverwijzing',
  stagecontext:
    'Je loopt stage bij een groothandel in bouwmaterialen. De boekhouder heeft de ' +
    'factuurgegevens ingevoerd, maar de berekeningen ontbreken nog. Werk de factuur af ' +
    'zodat ze naar de klant kan.',
  opdrachten: [
    'Bereken in E12 tot en met E16 het bedrag per lijn (aantal × eenheidsprijs).',
    'Bereken in E18 het subtotaal met de functie SOM.',
    'Bereken in E19 de btw. Verwijs absoluut naar het btw-tarief in B21, zodat je de formule kunt doorvoeren.',
    'Bereken in E20 het totaal te betalen bedrag.',
    'Geef E12 tot en met E20 de getalnotatie valuta met twee decimalen.',
  ],
  vergrendeld: ['A1', 'A3', 'A4', 'A5', 'A7', 'B7', 'A21', 'B21'],
  maxScore: 10,
  werkmap: {
    id: 'factuur-basis',
    name: 'Factuur 2026-0147',
    sheetOrder: ['factuur'],
    styles: OPMAAK,
    sheets: {
      factuur: {
        id: 'factuur',
        name: 'Factuur',
        rowCount: 40,
        columnCount: 12,
        columnData: { 0: { w: 190 }, 1: { w: 130 }, 2: { w: 80 }, 3: { w: 110 }, 4: { w: 120 } },
        cellData: bouwCellData({
          A1: { v: 'Bouwmaterialen De Vlieger bv', s: 'titel' },
          A2: { v: 'Nijverheidslaan 42, 8800 Roeselare · BE 0123.456.789' },

          A4: { v: 'Factuurnummer' }, B4: { v: '2026-0147' },
          A5: { v: 'Factuurdatum' }, B5: { v: '2026-09-18' },
          A6: { v: 'Klant' }, B6: { v: 'Aannemingen Verbeke bvba' },

          A9: { v: 'Omschrijving', s: 'kop' },
          B9: { v: 'Artikelcode', s: 'kop' },
          C9: { v: 'Aantal', s: 'kop' },
          D9: { v: 'Eenheidsprijs', s: 'kop' },
          E9: { v: 'Bedrag', s: 'kop' },

          A12: { v: 'Snelbouwsteen 19 cm' }, B12: { v: 'SB-190' }, C12: { v: 480 }, D12: { v: 0.84 },
          A13: { v: 'Cement CEM II 32,5 (25 kg)' }, B13: { v: 'CM-225' }, C13: { v: 64 }, D13: { v: 7.95 },
          A14: { v: 'Isolatieplaat PIR 60 mm' }, B14: { v: 'IS-060' }, C14: { v: 35 }, D14: { v: 28.4 },
          A15: { v: 'Wapeningsnet 150/150' }, B15: { v: 'WN-150' }, C15: { v: 18 }, D15: { v: 42.5 },
          A16: { v: 'Gipsplaat 12,5 mm 260x120' }, B16: { v: 'GP-125' }, C16: { v: 52 }, D16: { v: 11.2 },

          D18: { v: 'Subtotaal', s: 'kop' },
          D19: { v: 'Btw', s: 'kop' },
          D20: { v: 'Totaal te betalen', s: 'totaal' },

          A21: { v: 'Btw-tarief' }, B21: { v: 0.21 },
        }),
      },
    },
  },
};
