import { factuurOpgave } from './factuur.opgave';
import type { Opgave } from '@/lib/werkblad-types';

/** Publieke catalogus: veilig om naar de browser te sturen. */
export const OEFENINGEN: Record<string, Opgave> = {
  [factuurOpgave.id]: factuurOpgave,
};

export function vindOpgave(id: string): Opgave | undefined {
  return OEFENINGEN[id];
}
