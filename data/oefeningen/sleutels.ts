import 'server-only';
import { factuurChecks } from './factuur.sleutel';
import { voorraadChecks } from './01-voorraad.sleutel';
import { prijslijstChecks } from './02-prijslijst.sleutel';
import { verkoopChecks } from './03-verkoopcijfers.sleutel';
import { bestellingenChecks } from './04-bestellingen.sleutel';
import { klantenChecks } from './05-klanten.sleutel';
import { xzoekenChecks } from './06-xzoeken.sleutel';
import { genesteChecks } from './07-geneste.sleutel';
import type { Check } from '@/lib/nakijken';

/** Antwoordsleutels — server-only. */
export const SLEUTELS: Record<string, Check[]> = {
  'voorraad-basis': voorraadChecks,
  'prijslijst-verhoging': prijslijstChecks,
  'factuur-basis': factuurChecks,
  'verkoopcijfers': verkoopChecks,
  'bestellingen-als': bestellingenChecks,
  'klanten-vertzoeken': klantenChecks,
  'xzoeken-artikelen': xzoekenChecks,
  'geneste-functies': genesteChecks,
};
