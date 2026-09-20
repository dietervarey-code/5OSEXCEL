import 'server-only';
import { supabase } from '@/lib/supabase';

/**
 * Alle databanktoegang van het portaal loopt hier langs.
 *
 * De rest van de app kent geen Supabase; als we ooit van databank veranderen
 * blijft de wijziging binnen dit bestand.
 */

export type Rol = 'leerling' | 'leerkracht';

export type Leerling = {
  gebruikersnaam: string;
  naam: string;
  klas: string;
  rol: Rol;
  wachtwoordHash: string;
};

export type CheckResultaat = {
  checkId: string;
  omschrijving: string;
  punten: number;
  behaald: boolean;
  feedback: string;
};

export type GebeurtenisSoort =
  | 'gestart' | 'verborgen' | 'zichtbaar' | 'focus_weg' | 'focus_terug' | 'hartslag' | 'geplakt';

export type Gebeurtenis = {
  sessieId: string;
  soort: GebeurtenisSoort;
  tijdstip: number;
  /** Bij 'zichtbaar': hoeveel milliseconden het tabblad verborgen was. */
  duurMs?: number;
};

/** Eén regel in het leerkrachtenoverzicht. */
export type OverzichtRij = {
  gebruikersnaam: string;
  naam: string;
  klas: string;
  pogingen: number;
  besteScore: number | null;
  maxScore: number | null;
  laatsteOp: number | null;
  keerWeg: number;
  wegMs: number;
  werktijdMs: number;
};

// --- Leerlingen -------------------------------------------------------

export async function vindLeerling(gebruikersnaam: string): Promise<Leerling | null> {
  const { data, error } = await supabase()
    .from('leerlingen')
    .select('gebruikersnaam, naam, klas, rol, wachtwoord_hash')
    .ilike('gebruikersnaam', gebruikersnaam.trim())
    .maybeSingle();

  if (error) throw new Error(`Leerling opzoeken mislukte: ${error.message}`);
  if (!data) return null;

  return {
    gebruikersnaam: data.gebruikersnaam,
    naam: data.naam,
    klas: data.klas,
    rol: data.rol as Rol,
    wachtwoordHash: data.wachtwoord_hash,
  };
}

// --- Sessies ----------------------------------------------------------

/** Eén rij per keer dat een leerling een oefening opent. */
export async function startSessie(gebruikersnaam: string, oefeningId: string): Promise<string> {
  const { data, error } = await supabase()
    .from('sessies')
    .insert({ gebruikersnaam, oefening_id: oefeningId })
    .select('id')
    .single();

  if (error) throw new Error(`Sessie starten mislukte: ${error.message}`);
  return data.id as string;
}

/** Controleert dat de sessie van deze leerling is — niet van een klasgenoot. */
export async function sessieHoortBij(sessieId: string, gebruikersnaam: string): Promise<boolean> {
  const { data, error } = await supabase()
    .from('sessies')
    .select('gebruikersnaam')
    .eq('id', sessieId)
    .maybeSingle();

  if (error || !data) return false;
  return data.gebruikersnaam === gebruikersnaam;
}

/** Houdt bij tot wanneer er in deze sessie gewerkt is (voor de werktijd). */
export async function raakSessieAan(sessieId: string): Promise<void> {
  const { error } = await supabase()
    .from('sessies')
    .update({ laatst_actief_op: new Date().toISOString() })
    .eq('id', sessieId);

  if (error) console.error('[opslag] sessie bijwerken mislukte:', error.message);
}

// --- Pogingen ---------------------------------------------------------

export async function bewaarPoging(invoer: {
  sessieId: string;
  gebruikersnaam: string;
  oefeningId: string;
  score: number;
  maxScore: number;
  resultaten: CheckResultaat[];
}): Promise<number> {
  const db = supabase();

  const { count, error: telFout } = await db
    .from('pogingen')
    .select('id', { count: 'exact', head: true })
    .eq('gebruikersnaam', invoer.gebruikersnaam)
    .eq('oefening_id', invoer.oefeningId);

  if (telFout) throw new Error(`Pogingen tellen mislukte: ${telFout.message}`);

  const nummer = (count ?? 0) + 1;

  const { error } = await db.from('pogingen').insert({
    sessie_id: invoer.sessieId,
    gebruikersnaam: invoer.gebruikersnaam,
    oefening_id: invoer.oefeningId,
    nummer,
    score: invoer.score,
    max_score: invoer.maxScore,
    resultaten: invoer.resultaten,
  });

  if (error) throw new Error(`Poging bewaren mislukte: ${error.message}`);
  return nummer;
}

// --- Schermgebruik ----------------------------------------------------

export async function logGebeurtenissen(
  gebruikersnaam: string,
  gebeurtenissen: Gebeurtenis[],
): Promise<number> {
  if (gebeurtenissen.length === 0) return 0;

  const rijen = gebeurtenissen.map((g) => ({
    sessie_id: g.sessieId,
    gebruikersnaam,
    soort: g.soort,
    tijdstip: new Date(g.tijdstip).toISOString(),
    duur_ms: g.duurMs ?? null,
  }));

  const { error } = await supabase().from('gebeurtenissen').insert(rijen);
  if (error) throw new Error(`Gebeurtenissen bewaren mislukte: ${error.message}`);

  return rijen.length;
}

// --- Overzicht voor de leerkracht -------------------------------------

export async function overzicht(klas?: string): Promise<OverzichtRij[]> {
  const db = supabase();

  let leerlingenQuery = db.from('leerlingen').select('gebruikersnaam, naam, klas').eq('rol', 'leerling');
  if (klas) leerlingenQuery = leerlingenQuery.eq('klas', klas);

  const [{ data: leerlingen, error: f1 }, { data: pogingen, error: f2 }, { data: sessies, error: f3 }, { data: gebeurtenissen, error: f4 }] =
    await Promise.all([
      leerlingenQuery,
      db.from('pogingen').select('gebruikersnaam, score, max_score, ingediend_op'),
      db.from('sessies').select('gebruikersnaam, gestart_op, laatst_actief_op'),
      db.from('gebeurtenissen').select('gebruikersnaam, soort, duur_ms'),
    ]);

  const fout = f1 ?? f2 ?? f3 ?? f4;
  if (fout) throw new Error(`Overzicht ophalen mislukte: ${fout.message}`);

  const rijen = new Map<string, OverzichtRij>(
    (leerlingen ?? []).map((l) => [
      l.gebruikersnaam,
      {
        gebruikersnaam: l.gebruikersnaam,
        naam: l.naam,
        klas: l.klas,
        pogingen: 0,
        besteScore: null,
        maxScore: null,
        laatsteOp: null,
        keerWeg: 0,
        wegMs: 0,
        werktijdMs: 0,
      },
    ]),
  );

  for (const p of pogingen ?? []) {
    const rij = rijen.get(p.gebruikersnaam);
    if (!rij) continue;
    rij.pogingen += 1;
    rij.besteScore = Math.max(rij.besteScore ?? 0, Number(p.score));
    rij.maxScore = Number(p.max_score);
    const op = new Date(p.ingediend_op).getTime();
    rij.laatsteOp = Math.max(rij.laatsteOp ?? 0, op);
  }

  for (const s of sessies ?? []) {
    const rij = rijen.get(s.gebruikersnaam);
    if (!rij) continue;
    rij.werktijdMs += new Date(s.laatst_actief_op).getTime() - new Date(s.gestart_op).getTime();
  }

  for (const g of gebeurtenissen ?? []) {
    const rij = rijen.get(g.gebruikersnaam);
    if (!rij) continue;
    if (g.soort === 'verborgen') rij.keerWeg += 1;
    if (g.soort === 'zichtbaar' && g.duur_ms) rij.wegMs += g.duur_ms;
  }

  return [...rijen.values()].sort((a, b) => a.naam.localeCompare(b.naam));
}

// --- Zelfcontrole ------------------------------------------------------

export type Controle = { naam: string; ok: boolean; boodschap: string };

/**
 * Controleert of de databank bereikbaar is en het schema aanwezig.
 * Gebruikt door /status, zodat je na een deploy in één oogopslag ziet
 * wat er nog ontbreekt.
 */
export async function controleerDatabank(): Promise<Controle[]> {
  const controles: Controle[] = [];

  try {
    const { count, error } = await supabase()
      .from('leerlingen')
      .select('gebruikersnaam', { count: 'exact', head: true });

    if (error) {
      controles.push({ naam: 'Tabellen', ok: false, boodschap: verklaar(error.message, error.code) });
      return controles;
    }

    controles.push({ naam: 'Tabellen', ok: true, boodschap: 'Schema aanwezig en bereikbaar.' });
    controles.push({
      naam: 'Accounts',
      ok: (count ?? 0) > 0,
      boodschap:
        (count ?? 0) > 0
          ? `${count} account(s) aangemaakt.`
          : 'Nog geen accounts. Draai: node scripts/maak-leerlingen.mjs klas.csv',
    });
  } catch (e) {
    controles.push({
      naam: 'Verbinding',
      ok: false,
      boodschap: e instanceof Error ? verklaar(e.message) : 'Onbekende fout bij het verbinden.',
    });
  }

  return controles;
}

/** Vertaalt een technische foutboodschap naar iets waar je mee verder kunt. */
function verklaar(boodschap: string, code?: string): string {
  // PGRST205: PostgREST kent de tabel niet — het schema is nog niet uitgevoerd.
  if (code === 'PGRST205' || /does not exist|schema cache/i.test(boodschap)) {
    return 'De tabel "leerlingen" bestaat niet. Voer supabase/schema.sql uit in de SQL Editor van Supabase.';
  }
  if (/fetch failed|ENOTFOUND|EAI_AGAIN|getaddrinfo/i.test(boodschap)) {
    return 'Het project is niet bereikbaar. Controleer SUPABASE_URL op een typfout, en kijk in Supabase of het project niet gepauzeerd staat — gratis projecten pauzeren na een week zonder activiteit.';
  }
  if (/Invalid API key|JWT|401|403/i.test(boodschap)) {
    return 'De sleutel wordt geweigerd. Gebruik je wel de secret key (sb_secret_...) en niet de publishable key?';
  }
  return `Databankfout: ${boodschap}`;
}
