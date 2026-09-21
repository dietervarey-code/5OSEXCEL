import 'server-only';
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

/**
 * Verbinding met Supabase — uitsluitend vanaf de server.
 *
 * We gebruiken de secret key. Die omzeilt Row Level Security, dus deze module
 * mag nooit in een client component belanden; de import van 'server-only'
 * bovenaan laat de build falen als dat toch gebeurt.
 *
 * De browser krijgt in dit ontwerp helemaal geen databanksleutel: alle lees- en
 * schrijfacties lopen via de route handlers in app/api.
 */

let client: SupabaseClient | null = null;

/** Wordt door /api/login en /status gebruikt om een vergeten instelling te herkennen. */
export class ConfiguratieFout extends Error {}

export function supabaseIsIngesteld(): boolean {
  return Boolean(process.env.SUPABASE_URL && process.env.SUPABASE_SECRET_KEY);
}

/**
 * Kijkt of SUPABASE_URL er goed uitziet, vóór we er een verzoek naartoe sturen.
 *
 * De klassieke misgreep is de URL uit de adresbalk van het dashboard kopiëren
 * (supabase.com/dashboard/project/...). Dat is een webpagina, geen API, en het
 * antwoord is dan een HTML-pagina in plaats van gegevens.
 */
export function controleerUrl(): { ok: boolean; boodschap: string } {
  const ruw = process.env.SUPABASE_URL;
  if (!ruw) return { ok: false, boodschap: 'SUPABASE_URL ontbreekt.' };

  let url: URL;
  try {
    url = new URL(ruw);
  } catch {
    return { ok: false, boodschap: `"${ruw}" is geen geldig adres. Verwacht https://xxxxxxxx.supabase.co` };
  }

  if (url.hostname === 'supabase.com' || url.hostname.endsWith('.supabase.com')) {
    return {
      ok: false,
      boodschap:
        'Dit is het adres van het dashboard, niet van de API. Neem de waarde uit ' +
        'Project Settings › Data API › Project URL — die eindigt op .supabase.co',
    };
  }

  if (url.pathname !== '/' && url.pathname !== '') {
    const restEndpoint = /^\/rest(\/v\d+)?\/?$/.test(url.pathname);
    return {
      ok: false,
      boodschap: restEndpoint
        ? 'Je gebruikt het "RESTful endpoint" in plaats van de Project URL. Laat ' +
          `"${url.pathname}" weg: enkel ${url.protocol}//${url.host} — de app zet /rest/v1 er zelf achter.`
        : `Er staat een pad achter het adres ("${url.pathname}"). Enkel ${url.protocol}//${url.host}, zonder pad.`,
    };
  }

  if (url.protocol !== 'https:' && url.hostname !== 'localhost') {
    return { ok: false, boodschap: 'Gebruik https, niet http.' };
  }

  return { ok: true, boodschap: 'Ziet er goed uit.' };
}

export function supabase(): SupabaseClient {
  if (client) return client;

  const url = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY;

  if (url && secret) {
    // Dezelfde controle als op /status, maar hier vóór het eerste verzoek. Anders
    // krijgt de leerkracht een gateway-fout ("Invalid path specified in request
    // URL") te zien in plaats van te horen wat er precies fout zit.
    const vorm = controleerUrl();
    if (!vorm.ok) throw new ConfiguratieFout(vorm.boodschap);
  }

  if (!url || !secret) {
    throw new ConfiguratieFout(
      'SUPABASE_URL of SUPABASE_SECRET_KEY ontbreekt. Zet ze in .env.local (lokaal) ' +
        'of bij Environment Variables in Vercel. Zie docs/backend-frontend.md.',
    );
  }

  client = createClient(url.trim().replace(/\/+$/, ''), secret.trim(), {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { headers: { 'x-application-name': '5osexcel' } },
  });

  return client;
}
