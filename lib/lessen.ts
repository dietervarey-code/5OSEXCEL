import 'server-only';
import { supabase } from '@/lib/supabase';

/** Alle databanktoegang voor de lessen. */

export type MediaSoort = 'video' | 'bestand';

export type Lesmedia = {
  id: string;
  soort: MediaSoort;
  titel: string;
  /** Bij een video de insluit-URL, bij een bestand het pad in Storage. */
  bron: string;
  volgnummer: number;
};

export type Les = {
  id: string;
  focus: number;
  volgnummer: number;
  titel: string;
  samenvatting: string;
  inhoud: string;
  oefeningId: string | null;
  gepubliceerd: boolean;
  media: Lesmedia[];
};

type Rij = {
  id: string;
  focus: number;
  volgnummer: number;
  titel: string;
  samenvatting: string;
  inhoud: string;
  oefening_id: string | null;
  gepubliceerd: boolean;
};

function naarLes(rij: Rij, media: Lesmedia[] = []): Les {
  return {
    id: rij.id,
    focus: rij.focus,
    volgnummer: rij.volgnummer,
    titel: rij.titel,
    samenvatting: rij.samenvatting,
    inhoud: rij.inhoud,
    oefeningId: rij.oefening_id,
    gepubliceerd: rij.gepubliceerd,
    media,
  };
}

const VELDEN = 'id, focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd';

/** Lijst voor het overzicht. `allesTonen` is voor de leerkracht: ook concepten. */
export async function lijstLessen(allesTonen = false): Promise<Les[]> {
  let query = supabase().from('lessen').select(VELDEN).order('focus').order('volgnummer');
  if (!allesTonen) query = query.eq('gepubliceerd', true);

  const { data, error } = await query;
  if (error) throw new Error(`Lessen ophalen mislukte: ${error.message}`);
  return (data ?? []).map((r) => naarLes(r as Rij));
}

export async function vindLes(id: string, allesTonen = false): Promise<Les | null> {
  const db = supabase();

  const { data, error } = await db.from('lessen').select(VELDEN).eq('id', id).maybeSingle();
  if (error) throw new Error(`Les ophalen mislukte: ${error.message}`);
  if (!data) return null;

  const rij = data as Rij;
  if (!rij.gepubliceerd && !allesTonen) return null;

  const { data: media, error: mediaFout } = await db
    .from('lesmedia')
    .select('id, soort, titel, bron, volgnummer')
    .eq('les_id', id)
    .order('volgnummer');

  if (mediaFout) throw new Error(`Media ophalen mislukte: ${mediaFout.message}`);
  return naarLes(rij, (media ?? []) as Lesmedia[]);
}

/** De gepubliceerde les die bij een oefening hoort, voor de knop "Theorie herhalen". */
export async function lesBijOefening(oefeningId: string): Promise<{ id: string; titel: string } | null> {
  const { data, error } = await supabase()
    .from('lessen')
    .select('id, titel')
    .eq('oefening_id', oefeningId)
    .eq('gepubliceerd', true)
    .order('volgnummer')
    .limit(1);

  if (error) {
    console.error('[lessen] les bij oefening ophalen mislukte:', error.message);
    return null;
  }
  return (data ?? [])[0] ?? null;
}

// --- Beheer ------------------------------------------------------------

export async function maakLes(invoer: {
  focus: number;
  titel: string;
  samenvatting: string;
  inhoud: string;
  oefeningId: string | null;
  volgnummer: number;
}): Promise<string> {
  const { data, error } = await supabase()
    .from('lessen')
    .insert({
      focus: invoer.focus,
      titel: invoer.titel,
      samenvatting: invoer.samenvatting,
      inhoud: invoer.inhoud,
      oefening_id: invoer.oefeningId,
      volgnummer: invoer.volgnummer,
    })
    .select('id')
    .single();

  if (error) throw new Error(`Les aanmaken mislukte: ${error.message}`);
  return data.id as string;
}

export async function wijzigLes(
  id: string,
  velden: Partial<{
    focus: number;
    titel: string;
    samenvatting: string;
    inhoud: string;
    oefeningId: string | null;
    volgnummer: number;
    gepubliceerd: boolean;
  }>,
): Promise<boolean> {
  const rij: Record<string, unknown> = { gewijzigd_op: new Date().toISOString() };
  if (velden.focus !== undefined) rij.focus = velden.focus;
  if (velden.titel !== undefined) rij.titel = velden.titel;
  if (velden.samenvatting !== undefined) rij.samenvatting = velden.samenvatting;
  if (velden.inhoud !== undefined) rij.inhoud = velden.inhoud;
  if (velden.oefeningId !== undefined) rij.oefening_id = velden.oefeningId;
  if (velden.volgnummer !== undefined) rij.volgnummer = velden.volgnummer;
  if (velden.gepubliceerd !== undefined) rij.gepubliceerd = velden.gepubliceerd;

  const { data, error } = await supabase().from('lessen').update(rij).eq('id', id).select('id');
  if (error) throw new Error(`Les bijwerken mislukte: ${error.message}`);
  return (data ?? []).length > 0;
}

export async function verwijderLes(id: string): Promise<boolean> {
  const { data, error } = await supabase().from('lessen').delete().eq('id', id).select('id');
  if (error) throw new Error(`Les verwijderen mislukte: ${error.message}`);
  return (data ?? []).length > 0;
}

export async function voegMediaToe(invoer: {
  lesId: string;
  soort: MediaSoort;
  titel: string;
  bron: string;
}): Promise<void> {
  const { error } = await supabase().from('lesmedia').insert({
    les_id: invoer.lesId,
    soort: invoer.soort,
    titel: invoer.titel,
    bron: invoer.bron,
  });
  if (error) throw new Error(`Media toevoegen mislukte: ${error.message}`);
}

export async function verwijderMedia(id: string): Promise<{ soort: MediaSoort; bron: string } | null> {
  const { data, error } = await supabase().from('lesmedia').delete().eq('id', id).select('soort, bron');
  if (error) throw new Error(`Media verwijderen mislukte: ${error.message}`);
  const rij = (data ?? [])[0];
  return rij ? { soort: rij.soort as MediaSoort, bron: rij.bron as string } : null;
}
