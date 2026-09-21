import { bouwCellData, type CelData, type WerkmapData } from '@/lib/werkblad-types';

/** Gedeelde opmaak en bouwhulp voor alle oefeningen. */

export const OPMAAK = {
  titel: { bl: 1, fs: 15 },
  kop: { bl: 1, bg: { rgb: '#E8EEF7' } },
  nadruk: { bl: 1 },
  invoer: { bg: { rgb: '#FFFBEA' } },
  totaal: { bl: 1, bd: { t: { s: 1, cl: { rgb: '#000000' } } } },
} as const;

/** Standaardbreedtes: brede eerste kolom voor omschrijvingen. */
const BREEDTES: Record<number, { w: number }> = {
  0: { w: 200 }, 1: { w: 130 }, 2: { w: 110 }, 3: { w: 120 },
  4: { w: 120 }, 5: { w: 120 }, 6: { w: 140 }, 7: { w: 180 }, 8: { w: 120 },
};

export function bouwWerkmap(
  id: string,
  bladnaam: string,
  cellen: Record<string, CelData>,
  opties: { rijen?: number; kolommen?: number; extraBladen?: { naam: string; cellen: Record<string, CelData> }[] } = {},
): WerkmapData {
  const hoofdId = 'blad1';
  const werkmap: WerkmapData = {
    id,
    name: bladnaam,
    sheetOrder: [hoofdId],
    styles: OPMAAK,
    sheets: {
      [hoofdId]: {
        id: hoofdId,
        name: bladnaam,
        rowCount: opties.rijen ?? 40,
        columnCount: opties.kolommen ?? 12,
        columnData: BREEDTES,
        cellData: bouwCellData(cellen),
      },
    },
  };

  opties.extraBladen?.forEach((blad, i) => {
    const bladId = `blad${i + 2}`;
    werkmap.sheetOrder.push(bladId);
    werkmap.sheets[bladId] = {
      id: bladId,
      name: blad.naam,
      rowCount: 40,
      columnCount: 12,
      columnData: BREEDTES,
      cellData: bouwCellData(blad.cellen),
    };
  });

  return werkmap;
}

/** Zet een rij naast elkaar neer: rij(4, 'A', ['x', 12, 3.5]) → A4, B4, C4. */
export function rij(
  nummer: number,
  startKolom: string,
  waarden: (string | number | null)[],
  stijl?: string,
): Record<string, CelData> {
  const resultaat: Record<string, CelData> = {};
  const start = startKolom.toUpperCase().charCodeAt(0);
  waarden.forEach((waarde, i) => {
    if (waarde === null) return;
    resultaat[`${String.fromCharCode(start + i)}${nummer}`] = stijl ? { v: waarde, s: stijl } : { v: waarde };
  });
  return resultaat;
}

/** Voegt meerdere celgroepen samen tot één tabel. */
export function samen(...groepen: Record<string, CelData>[]): Record<string, CelData> {
  return Object.assign({}, ...groepen);
}

/** De getalnotatie-controle: twee decimalen en een valutateken, welk dan ook. */
export const VALUTA_PATROON = '^(?=.*0\\.00)(?=.*(€|\\$|£|EUR|\\[\\$)).*$';
