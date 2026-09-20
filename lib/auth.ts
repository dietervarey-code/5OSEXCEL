import { scryptSync, randomBytes, timingSafeEqual, createHmac } from 'node:crypto';
import { cookies } from 'next/headers';

/**
 * Wachtwoorden worden door de leerkracht aangemaakt (zie scripts/maak-leerlingen.mjs).
 * We slaan nooit een wachtwoord in klare tekst op, enkel een scrypt-hash met salt.
 */

const COOKIE = '5os_sessie';
const MAX_LEEFTIJD = 60 * 60 * 8; // 8 uur — één schooldag

export const GEHEIM_MINIMUM = 16;

/** Of SESSIE_GEHEIM bruikbaar is. Gebruikt door /status om dit te melden. */
export function geheimIsIngesteld(): boolean {
  const geheim = process.env.SESSIE_GEHEIM;
  return Boolean(geheim && geheim.length >= GEHEIM_MINIMUM);
}

function sessieGeheim(): string {
  const geheim = process.env.SESSIE_GEHEIM;
  if (!geheim || geheim.length < GEHEIM_MINIMUM) {
    throw new Error(
      `SESSIE_GEHEIM ontbreekt of is korter dan ${GEHEIM_MINIMUM} tekens. ` +
        'Zet een willekeurige waarde in .env.local (lokaal) of bij Environment Variables in Vercel.',
    );
  }
  return geheim;
}

export function hashWachtwoord(wachtwoord: string): string {
  const salt = randomBytes(16).toString('hex');
  const hash = scryptSync(wachtwoord, salt, 64).toString('hex');
  return `scrypt$${salt}$${hash}`;
}

export function controleerWachtwoord(wachtwoord: string, opgeslagen: string): boolean {
  const [algoritme, salt, hash] = opgeslagen.split('$');
  if (algoritme !== 'scrypt' || !salt || !hash) return false;
  const kandidaat = scryptSync(wachtwoord, salt, 64);
  const bewaard = Buffer.from(hash, 'hex');
  if (kandidaat.length !== bewaard.length) return false;
  return timingSafeEqual(kandidaat, bewaard);
}

export type Sessie = {
  gebruikersnaam: string;
  naam: string;
  rol: 'leerling' | 'leerkracht';
  klas: string;
  verlooptOp: number;
};

function onderteken(payload: string): string {
  return createHmac('sha256', sessieGeheim()).update(payload).digest('base64url');
}

export function maakSessieCookie(sessie: Sessie): string {
  const payload = Buffer.from(JSON.stringify(sessie)).toString('base64url');
  return `${payload}.${onderteken(payload)}`;
}

export function leesSessieCookie(waarde: string | undefined): Sessie | null {
  if (!waarde) return null;
  const [payload, handtekening] = waarde.split('.');
  if (!payload || !handtekening) return null;

  // Ontbreekt het geheim, dan behandelen we de cookie als ongeldig in plaats van
  // de pagina te laten crashen. Anders krijgt een bezoeker met een oude cookie
  // een serverfout te zien in plaats van het aanmeldscherm.
  if (!geheimIsIngesteld()) {
    console.error('[auth] SESSIE_GEHEIM ontbreekt; bestaande sessies zijn ongeldig.');
    return null;
  }

  // Vergelijking in constante tijd, zodat de handtekening niet te raden valt.
  const verwacht = Buffer.from(onderteken(payload));
  const gekregen = Buffer.from(handtekening);
  if (verwacht.length !== gekregen.length || !timingSafeEqual(verwacht, gekregen)) return null;

  try {
    const sessie = JSON.parse(Buffer.from(payload, 'base64url').toString()) as Sessie;
    if (sessie.verlooptOp < Date.now()) return null;
    return sessie;
  } catch {
    return null;
  }
}

export const COOKIE_NAAM = COOKIE;
export const COOKIE_MAX_LEEFTIJD = MAX_LEEFTIJD;

/** Leest de huidige sessie in een server component of route handler. */
export async function huidigeSessie(): Promise<Sessie | null> {
  const jar = await cookies();
  return leesSessieCookie(jar.get(COOKIE)?.value);
}
