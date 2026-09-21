import { factuurOpgave } from './factuur.opgave';
import { voorraadOpgave } from './01-voorraad';
import { prijslijstOpgave } from './02-prijslijst';
import { verkoopOpgave } from './03-verkoopcijfers';
import { bestellingenOpgave } from './04-bestellingen';
import { klantenOpgave } from './05-klanten';
import { xzoekenOpgave } from './06-xzoeken';
import { genesteOpgave } from './07-geneste';
import type { Opgave } from '@/lib/werkblad-types';

/**
 * Publieke catalogus: veilig om naar de browser te sturen.
 * De reeks bouwt op in moeilijkheid; `volgnummer` bepaalt de volgorde.
 */
const ALLE = [
  voorraadOpgave,      // 1 — vermenigvuldigen en SOM
  prijslijstOpgave,    // 2 — absolute verwijzing en AFRONDEN
  factuurOpgave,       // 3 — beide samen op een echte factuur
  verkoopOpgave,       // 4 — MAX, MIN, GEMIDDELDE, AANTAL(ARG)
  bestellingenOpgave,  // 5 — ALS, AANTAL.ALS, SOM.ALS
  klantenOpgave,       // 6 — VERT.ZOEKEN
  xzoekenOpgave,       // 7 — X.ZOEKEN met terugvalwaarde
  genesteOpgave,       // 8 — VERT.ZOEKEN en ALS in één formule
];

export const OEFENINGEN: Record<string, Opgave> = Object.fromEntries(ALLE.map((o) => [o.id, o]));

/** In de volgorde waarin leerlingen ze horen te maken. */
export function oefeningenOpVolgorde(): Opgave[] {
  return [...ALLE].sort((a, b) => a.volgnummer - b.volgnummer);
}

export function vindOpgave(id: string): Opgave | undefined {
  return OEFENINGEN[id];
}
