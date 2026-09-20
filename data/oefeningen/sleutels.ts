import 'server-only';
import { factuurChecks } from './factuur.sleutel';
import type { Check } from '@/lib/nakijken';

/** Antwoordsleutels — server-only. */
export const SLEUTELS: Record<string, Check[]> = {
  'factuur-basis': factuurChecks,
};
