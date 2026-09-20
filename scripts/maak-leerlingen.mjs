#!/usr/bin/env node
/**
 * Maakt de leerlingentabel aan met gebruikersnamen en wachtwoorden.
 *
 *   node scripts/maak-leerlingen.mjs klas.csv
 *
 * Verwacht een CSV met kolommen: naam,klas,rol
 * (rol is optioneel en is standaard "leerling"; gebruik "leerkracht" voor jezelf)
 *
 * Schrijft data/leerlingen.json met scrypt-hashes, en print één keer de
 * wachtwoorden in klare tekst zodat je ze kunt uitdelen. Daarna zijn ze weg.
 */
import { scryptSync, randomBytes, randomInt } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';

const WOORDEN = ['appel', 'brug', 'daver', 'eiland', 'fazant', 'gracht', 'haven', 'ijzer', 'kade', 'lantaarn', 'molen', 'noord', 'oever', 'polder', 'rots', 'schans', 'toren', 'vaart', 'wilg', 'zolder'];

function hash(wachtwoord) {
  const salt = randomBytes(16).toString('hex');
  return `scrypt$${salt}$${scryptSync(wachtwoord, salt, 64).toString('hex')}`;
}

function maakWachtwoord() {
  return `${WOORDEN[randomInt(WOORDEN.length)]}-${WOORDEN[randomInt(WOORDEN.length)]}-${randomInt(10, 100)}`;
}

function gebruikersnaam(naam, bestaande) {
  const basis = naam.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z\s]/g, '').trim().split(/\s+/).join('.');
  let kandidaat = basis;
  let n = 2;
  while (bestaande.has(kandidaat)) kandidaat = `${basis}${n++}`;
  bestaande.add(kandidaat);
  return kandidaat;
}

const csvPad = process.argv[2];
if (!csvPad) {
  console.error('Gebruik: node scripts/maak-leerlingen.mjs klas.csv');
  console.error('CSV-kolommen: naam,klas,rol');
  process.exit(1);
}

const regels = readFileSync(csvPad, 'utf8').trim().split(/\r?\n/);
const kop = regels[0].toLowerCase().split(',').map((k) => k.trim());
const kolom = (naam) => kop.indexOf(naam);

const gebruikt = new Set();
const leerlingen = [];
const uitDelen = [];

for (const regel of regels.slice(1)) {
  if (!regel.trim()) continue;
  const velden = regel.split(',').map((v) => v.trim());
  const naam = velden[kolom('naam')];
  if (!naam) continue;
  const klas = velden[kolom('klas')] ?? '5OS';
  const rol = velden[kolom('rol')] || 'leerling';
  const wachtwoord = maakWachtwoord();
  const gn = gebruikersnaam(naam, gebruikt);

  leerlingen.push({ gebruikersnaam: gn, naam, klas, rol, wachtwoordHash: hash(wachtwoord) });
  uitDelen.push({ naam, gebruikersnaam: gn, wachtwoord, klas, rol });
}

writeFileSync('data/leerlingen.json', JSON.stringify(leerlingen, null, 2));

console.log(`\n${leerlingen.length} accounts aangemaakt in data/leerlingen.json\n`);
console.log('Deel deze gegevens uit — ze worden nergens bewaard en zijn hierna onherstelbaar:\n');
console.table(uitDelen);
