#!/usr/bin/env node
/**
 * Maakt de accounts voor een klas aan in Supabase.
 *
 *   node scripts/maak-leerlingen.mjs klas.csv
 *   node scripts/maak-leerlingen.mjs klas.csv --reset   (nieuwe wachtwoorden voor wie al bestaat)
 *
 * Verwacht een CSV met kolommen: naam,klas,rol
 * (rol is optioneel en is standaard "leerling"; gebruik "leerkracht" voor jezelf)
 *
 * Wachtwoorden worden als scrypt-hash bewaard en één keer in de terminal
 * getoond zodat je ze kunt uitdelen. Daarna zijn ze onherroepelijk weg.
 */
import { scryptSync, randomBytes } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { createClient } from '@supabase/supabase-js';
import { maakGebruikersnaam, maakWachtwoord } from '../lib/accounts.mjs';

// .env.local inlezen zonder extra afhankelijkheid.
try {
  for (const regel of readFileSync('.env.local', 'utf8').split(/\r?\n/)) {
    const m = regel.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
} catch { /* geen .env.local, dan moeten de variabelen al gezet zijn */ }

const URL = process.env.SUPABASE_URL;
const SECRET = process.env.SUPABASE_SECRET_KEY;

if (!URL || !SECRET) {
  console.error('SUPABASE_URL of SUPABASE_SECRET_KEY ontbreekt. Zet ze in .env.local.');
  process.exit(1);
}

const csvPad = process.argv[2];
const reset = process.argv.includes('--reset');

if (!csvPad) {
  console.error('Gebruik: node scripts/maak-leerlingen.mjs klas.csv [--reset]');
  console.error('CSV-kolommen: naam,klas,rol');
  process.exit(1);
}

const hash = (w) => {
  const salt = randomBytes(16).toString('hex');
  return `scrypt$${salt}$${scryptSync(w, salt, 64).toString('hex')}`;
};

const db = createClient(URL, SECRET, { auth: { persistSession: false } });

// Wie zit er al in de databank?
const { data: bestaande, error: leesFout } = await db.from('leerlingen').select('gebruikersnaam');
if (leesFout) {
  console.error('Kon de tabel "leerlingen" niet lezen:', leesFout.message);
  console.error('Heb je supabase/schema.sql al uitgevoerd in de SQL Editor?');
  process.exit(1);
}

const bezet = new Set((bestaande ?? []).map((r) => r.gebruikersnaam));
const alAanwezig = new Set(bezet);

const regels = readFileSync(csvPad, 'utf8').trim().split(/\r?\n/);
const kop = regels[0].toLowerCase().split(',').map((k) => k.trim());
const kolom = (naam) => kop.indexOf(naam);

if (kolom('naam') === -1) {
  console.error('De CSV heeft geen kolom "naam". Verwachte kolommen: naam,klas,rol');
  process.exit(1);
}

const nieuwe = [];
const uitDelen = [];
const overgeslagen = [];

for (const regel of regels.slice(1)) {
  if (!regel.trim()) continue;
  const velden = regel.split(',').map((v) => v.trim());
  const naam = velden[kolom('naam')];
  if (!naam) continue;

  const klas = (kolom('klas') !== -1 && velden[kolom('klas')]) || '5OS';
  const rol = (kolom('rol') !== -1 && velden[kolom('rol')]) || 'leerling';

  // Bestaat deze leerling al? Dan niet zomaar overschrijven.
  const voorspeld = maakGebruikersnaam(naam);
  if (alAanwezig.has(voorspeld) && !reset) {
    overgeslagen.push(voorspeld);
    continue;
  }

  const gebruikersnaam = alAanwezig.has(voorspeld) ? voorspeld : maakGebruikersnaam(naam, bezet);
  const wachtwoord = maakWachtwoord();

  nieuwe.push({ gebruikersnaam, naam, klas, rol, wachtwoord_hash: hash(wachtwoord) });
  uitDelen.push({ naam, gebruikersnaam, wachtwoord, klas, rol });
}

if (nieuwe.length === 0) {
  console.log('Niets te doen.');
  if (overgeslagen.length) {
    console.log(`${overgeslagen.length} account(s) bestonden al. Gebruik --reset voor nieuwe wachtwoorden.`);
  }
  process.exit(0);
}

const { error: schrijfFout } = await db
  .from('leerlingen')
  .upsert(nieuwe, { onConflict: 'gebruikersnaam' });

if (schrijfFout) {
  console.error('Wegschrijven mislukte:', schrijfFout.message);
  process.exit(1);
}

console.log(`\n${nieuwe.length} account(s) aangemaakt of bijgewerkt.`);
if (overgeslagen.length) {
  console.log(`${overgeslagen.length} bestonden al en bleven ongewijzigd: ${overgeslagen.join(', ')}`);
}
console.log('\nDeel deze gegevens uit — ze worden nergens bewaard en zijn hierna onherstelbaar:\n');
console.table(uitDelen);
