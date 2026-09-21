/** Vorm van de startgegevens die naar de browser gaan. Bevat nooit de oplossing. */
export type Opgave = {
  id: string;
  titel: string;
  focus: string;
  stagecontext: string;
  opdrachten: string[];
  /** Cellen die de leerling niet mag wijzigen (gegeven materiaal). */
  vergrendeld: string[];
  werkmap: WerkmapData;
  maxScore: number;
};

export type CelData = {
  /** Waarde. */ v?: string | number | boolean;
  /** Formule, bv "=SUM(A1:A5)". */ f?: string;
  /** Opmaak-id. */ s?: string;
};

export type WerkmapData = {
  id: string;
  name: string;
  sheetOrder: string[];
  styles: Record<string, unknown>;
  sheets: Record<string, {
    id: string;
    name: string;
    rowCount: number;
    columnCount: number;
    cellData: Record<number, Record<number, CelData>>;
    columnData?: Record<number, { w: number }>;
  }>;
};

/** Wat de browser bij het nakijken terugstuurt: per cel de waarde, de formule en de opmaak. */
export type CelInzending = {
  cel: string;
  /** Wat op het scherm staat — met getalnotatie is dit tekst, bv. "$3,253.40 ". */
  waarde: string | number | boolean | null;
  /** De onderliggende waarde zonder opmaak. Ontbreekt bij oudere inzendingen. */
  ruweWaarde?: string | number | boolean | null;
  formule: string | null;
  opmaak: { vet?: boolean; getalnotatie?: string } | null;
};

/** Zet "E11" om naar { rij: 10, kolom: 4 } (nulgebaseerd). */
export function celNaarPositie(cel: string): { rij: number; kolom: number } {
  const m = cel.toUpperCase().match(/^([A-Z]+)(\d+)$/);
  if (!m) throw new Error(`Ongeldig celadres: ${cel}`);
  const [, letters, cijfers] = m;
  let kolom = 0;
  for (const letter of letters) kolom = kolom * 26 + (letter.charCodeAt(0) - 64);
  return { rij: Number(cijfers) - 1, kolom: kolom - 1 };
}

export function positieNaarCel(rij: number, kolom: number): string {
  let letters = '';
  let k = kolom + 1;
  while (k > 0) {
    const rest = (k - 1) % 26;
    letters = String.fromCharCode(65 + rest) + letters;
    k = Math.floor((k - 1) / 26);
  }
  return `${letters}${rij + 1}`;
}

/** Bouwt Univer-cellData op uit een leesbare { "A1": {...} }-tabel. */
export function bouwCellData(cellen: Record<string, CelData>): Record<number, Record<number, CelData>> {
  const resultaat: Record<number, Record<number, CelData>> = {};
  for (const [adres, data] of Object.entries(cellen)) {
    const { rij, kolom } = celNaarPositie(adres);
    resultaat[rij] ??= {};
    resultaat[rij][kolom] = data;
  }
  return resultaat;
}
