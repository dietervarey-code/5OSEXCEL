/** Vorm van de startgegevens die naar de browser gaan. Bevat nooit de oplossing. */
/** Wat elke oefening gemeen heeft, of ze nu in de browser of in Excel gebeurt. */
export type OpgaveBasis = {
  id: string;
  titel: string;
  focus: string;
  /** Het Focus-blok uit de cursus (1 t.e.m. 9). Groepeert het overzicht. */
  focusNummer: number;
  /** Plaats in de reeks; bepaalt de volgorde in het overzicht. */
  volgnummer: number;
  /** 1 = eenvoudig, 5 = pittig. Wordt als bolletjes getoond. */
  niveau: 1 | 2 | 3 | 4 | 5;
  /** Wat de leerling na deze oefening kan. */
  leerdoel: string;
  stagecontext: string;
  opdrachten: string[];
  maxScore: number;
};

/** Een oefening die in het rekenblad in de browser gemaakt wordt. */
export type Opgave = OpgaveBasis & {
  soort?: 'werkblad';
  /** Cellen die de leerling niet mag wijzigen (gegeven materiaal). */
  vergrendeld: string[];
  werkmap: WerkmapData;
};

/**
 * Een oefening die de leerling in écht Excel maakt en daarna indient.
 *
 * Voor grafieken, draaitabellen en afdrukinstellingen: die bestaan niet in het
 * rekenblad in de browser, en ze horen bij wat een leerling op stage doet.
 */
export type UploadOpgave = OpgaveBasis & {
  soort: 'upload';
  /** Het bestand dat de leerling downloadt om mee te beginnen. */
  startbestand: {
    bladnaam: string;
    rijen: (string | number | null)[][];
    /** Kolombreedtes in tekens, zodat het bestand er meteen netjes uitziet. */
    breedtes?: number[];
  };
};

export type EenOpgave = Opgave | UploadOpgave;

export function isUpload(opgave: EenOpgave): opgave is UploadOpgave {
  return opgave.soort === 'upload';
}

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
  opmaak: {
    vet?: boolean;
    cursief?: boolean;
    onderstreept?: boolean;
    achtergrond?: string;
    uitlijning?: string;
    getalnotatie?: string;
  } | null;
};

/** Toestand van het blad als geheel, naast de cellen. */
export type BladInzending = {
  /** Aantal vastgezette rijen en kolommen (Beeld › Titels blokkeren). */
  vastgezetteRijen: number;
  vastgezetteKolommen: number;
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
