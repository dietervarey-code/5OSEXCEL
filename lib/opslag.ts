import { promises as fs } from 'node:fs';
import path from 'node:path';

/**
 * TIJDELIJKE OPSLAG voor de technische proef: één JSON-bestand op schijf.
 *
 * Dit is bewust een dun laagje. In fase 2 vervangen we de body van elke functie
 * hieronder door een Supabase-query; de rest van de app verandert dan niet.
 * Let op: op Vercel is het bestandssysteem alleen-lezen/vluchtig, dus deze
 * implementatie werkt enkel lokaal.
 */

export type Poging = {
  id: string;
  gebruikersnaam: string;
  naam: string;
  klas: string;
  oefeningId: string;
  gestartOp: number;
  ingediendOp: number | null;
  score: number | null;
  maxScore: number | null;
  resultaten: { checkId: string; omschrijving: string; punten: number; behaald: boolean; feedback: string }[];
};

export type Gebeurtenis = {
  pogingId: string;
  gebruikersnaam: string;
  soort: 'verborgen' | 'zichtbaar' | 'focus_weg' | 'focus_terug' | 'hartslag' | 'geplakt' | 'gestart';
  tijdstip: number;
  /** Bij 'zichtbaar': hoeveel milliseconden het tabblad verborgen was. */
  duurMs?: number;
};

type Database = { pogingen: Poging[]; gebeurtenissen: Gebeurtenis[] };

const BESTAND = path.join(process.cwd(), 'data', 'opslag.json');
const LEEG: Database = { pogingen: [], gebeurtenissen: [] };

async function lees(): Promise<Database> {
  try {
    return JSON.parse(await fs.readFile(BESTAND, 'utf8')) as Database;
  } catch {
    return structuredClone(LEEG);
  }
}

async function schrijf(db: Database): Promise<void> {
  await fs.mkdir(path.dirname(BESTAND), { recursive: true });
  await fs.writeFile(BESTAND, JSON.stringify(db, null, 2));
}

export async function startPoging(
  invoer: Omit<Poging, 'id' | 'gestartOp' | 'ingediendOp' | 'score' | 'maxScore' | 'resultaten'>,
): Promise<Poging> {
  const db = await lees();
  const poging: Poging = {
    ...invoer,
    id: `p_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    gestartOp: Date.now(),
    ingediendOp: null,
    score: null,
    maxScore: null,
    resultaten: [],
  };
  db.pogingen.push(poging);
  await schrijf(db);
  return poging;
}

export async function bewaarResultaat(
  pogingId: string,
  score: number,
  maxScore: number,
  resultaten: Poging['resultaten'],
): Promise<void> {
  const db = await lees();
  const poging = db.pogingen.find((p) => p.id === pogingId);
  if (!poging) return;
  poging.ingediendOp = Date.now();
  poging.score = score;
  poging.maxScore = maxScore;
  poging.resultaten = resultaten;
  await schrijf(db);
}

export async function logGebeurtenissen(gebeurtenissen: Gebeurtenis[]): Promise<void> {
  const db = await lees();
  db.gebeurtenissen.push(...gebeurtenissen);
  await schrijf(db);
}

export async function allePogingen(): Promise<Poging[]> {
  return (await lees()).pogingen;
}

export async function alleGebeurtenissen(): Promise<Gebeurtenis[]> {
  return (await lees()).gebeurtenissen;
}
