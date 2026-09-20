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

export function supabase(): SupabaseClient {
  if (client) return client;

  const url = process.env.SUPABASE_URL;
  const secret = process.env.SUPABASE_SECRET_KEY;

  if (!url || !secret) {
    throw new ConfiguratieFout(
      'SUPABASE_URL of SUPABASE_SECRET_KEY ontbreekt. Zet ze in .env.local (lokaal) ' +
        'of bij Environment Variables in Vercel. Zie docs/backend-frontend.md.',
    );
  }

  client = createClient(url, secret, {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { headers: { 'x-application-name': '5osexcel' } },
  });

  return client;
}
