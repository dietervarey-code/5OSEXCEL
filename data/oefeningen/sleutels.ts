import 'server-only';
import { factuurChecks } from './factuur.sleutel';
import { voorraadChecks } from './01-voorraad.sleutel';
import { prijslijstChecks } from './02-prijslijst.sleutel';
import { verkoopChecks } from './03-verkoopcijfers.sleutel';
import { bestellingenChecks } from './04-bestellingen.sleutel';
import { klantenChecks } from './05-klanten.sleutel';
import { xzoekenChecks } from './06-xzoeken.sleutel';
import { genesteChecks } from './07-geneste.sleutel';
import { getalnotatieChecks } from './f1-01-getalnotatie.sleutel';
import { tabelChecks } from './f1-02-tabel.sleutel';
import { sorterenChecks } from './f1-03-sorteren.sleutel';
import { vastzettenChecks } from './f1-04-vastzetten.sleutel';
import { transponerenChecks } from './f1-05-transponeren.sleutel';
import {
  bladenOphalenChecks, bladenFiliaalChecks, bladenVerschilChecks,
  bladenGemiddeldeChecks, bladenZoekenChecks,
} from './f5-bladen.sleutel';
import {
  koppelenPrijzenChecks, koppelenZoekenChecks, koppelenConsoliderenChecks,
  koppelenHerstellenChecks, koppelenFactuurChecks,
} from './f6-koppelen.sleutel';
import { horizZoekenChecks, tekstChecks } from './f8-extra.sleutel';
import {
  afdrukStandChecks, afdrukPassendChecks, afdrukKopVoetChecks,
  afdrukTitelrijenChecks, afdrukRapportChecks,
} from './f3-afdrukken.sleutel';
import {
  staafChecks, lijnChecks, cirkelChecks, grafiekOpmaakChecks, tweeReeksenChecks,
} from './f4-grafieken.sleutel';
import {
  draaiEersteChecks, draaiKruistabelChecks, draaiFunctieChecks,
  draaiFilterChecks, draaiRapportChecks,
} from './f7-draaitabellen.sleutel';
import type { BestandCheck } from '@/lib/nakijken-bestand';
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

  'f1-getalnotatie': getalnotatieChecks,
  'f1-tabel-opmaken': tabelChecks,
  'f1-sorteren': sorterenChecks,
  'f1-vastzetten': vastzettenChecks,
  'f1-transponeren': transponerenChecks,

  'f5-bladen-ophalen': bladenOphalenChecks,
  'f5-bladen-filiaal': bladenFiliaalChecks,
  'f5-bladen-verschil': bladenVerschilChecks,
  'f5-bladen-gemiddelde': bladenGemiddeldeChecks,
  'f5-bladen-zoeken': bladenZoekenChecks,

  'f6-prijzen-koppelen': koppelenPrijzenChecks,
  'f6-koppelen-zoeken': koppelenZoekenChecks,
  'f6-consolideren': koppelenConsoliderenChecks,
  'f6-herstellen': koppelenHerstellenChecks,
  'f6-gekoppelde-factuur': koppelenFactuurChecks,

  'f8-horiz-zoeken': horizZoekenChecks,
  'f8-tekstfuncties': tekstChecks,
};

/** Sleutels voor de oefeningen die als .xlsx-bestand ingediend worden. */
export const BESTANDSLEUTELS: Record<string, BestandCheck[]> = {
  'f3-stand-en-marges': afdrukStandChecks,
  'f3-passend-maken': afdrukPassendChecks,
  'f3-kop-en-voettekst': afdrukKopVoetChecks,
  'f3-titelrijen': afdrukTitelrijenChecks,
  'f3-printklaar-rapport': afdrukRapportChecks,

  'f4-staafdiagram': staafChecks,
  'f4-lijndiagram': lijnChecks,
  'f4-cirkeldiagram': cirkelChecks,
  'f4-grafiek-opmaken': grafiekOpmaakChecks,
  'f4-twee-reeksen': tweeReeksenChecks,

  'f7-eerste-draaitabel': draaiEersteChecks,
  'f7-kruistabel': draaiKruistabelChecks,
  'f7-samenvattingsfunctie': draaiFunctieChecks,
  'f7-filteren': draaiFilterChecks,
  'f7-draairapport': draaiRapportChecks,
};
