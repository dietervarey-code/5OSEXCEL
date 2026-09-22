import 'server-only';
import { supabase } from '@/lib/supabase';

/**
 * Voorbeeldbestanden bij een les: een .xlsx om mee te oefenen, een pdf, een
 * schermafbeelding. Ze staan in een afgeschermde Storage-bucket; de leerling
 * krijgt een link die na een uur vervalt.
 *
 * Video's horen hier NIET thuis — zie supabase/schema.sql voor waarom.
 */

/**
 * Een fout bij het opbergen van een bestand, met een boodschap die al uitlegt
 * wat er te doen valt. Die mag ongewijzigd op het scherm.
 */
export class OpslagFout extends Error {}

export const BUCKET = 'lesmateriaal';

/** Waar het ingediende werk van leerlingen terechtkomt. */
export const INZENDINGEN = 'inzendingen';

/** 20 MB. Ruim voor een werkmap of een pdf, klein genoeg voor de gratis 1 GB. */
export const MAX_BYTES = 20 * 1024 * 1024;

const TOEGESTAAN: Record<string, string> = {
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
  'application/vnd.ms-excel': 'xls',
  'application/pdf': 'pdf',
  'image/png': 'png',
  'image/jpeg': 'jpg',
  'image/webp': 'webp',
};

export function bestandstypeToegestaan(type: string): boolean {
  return type in TOEGESTAAN;
}

export function toegestaneTypes(): string {
  return [...new Set(Object.values(TOEGESTAAN))].join(', ');
}

/**
 * Maakt een veilige bestandsnaam: geen paden, geen rare tekens.
 *
 * De map komt van ons (een les-id, of gebruikersnaam/oefening-id uit de sessie
 * en de catalogus); alleen de bestandsnaam komt van de gebruiker en wordt hier
 * geschrobd.
 */
export function veiligePadnaam(map: string, naam: string): string {
  const schoon = naam
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-zA-Z0-9._-]/g, '-')
    .replace(/-+/g, '-')
    .slice(-80);
  return `${map}/${Date.now()}-${schoon}`;
}

export async function uploadBestand(
  pad: string,
  bestand: ArrayBuffer,
  type: string,
  bucket: string = BUCKET,
): Promise<void> {
  const { error } = await supabase()
    .storage.from(bucket)
    .upload(pad, bestand, { contentType: type, upsert: false });

  if (error) {
    if (/bucket not found/i.test(error.message)) {
      throw new OpslagFout(
        `De bucket "${bucket}" bestaat nog niet. Maak ze aan in Supabase › Storage (private).`,
      );
    }
    throw new Error(`Uploaden mislukte: ${error.message}`);
  }
}

/** Tijdelijke link naar een bestand. Vervalt na een uur. */
export async function tijdelijkeLink(pad: string, bucket: string = BUCKET): Promise<string | null> {
  const { data, error } = await supabase().storage.from(bucket).createSignedUrl(pad, 3600);
  if (error) {
    console.error('[bestanden] link maken mislukte:', error.message);
    return null;
  }
  return data?.signedUrl ?? null;
}

export async function verwijderBestand(pad: string): Promise<void> {
  const { error } = await supabase().storage.from(BUCKET).remove([pad]);
  if (error) console.error('[bestanden] verwijderen mislukte:', error.message);
}
