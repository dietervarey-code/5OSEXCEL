/**
 * Gebruikersnamen en wachtwoorden aanmaken.
 *
 * Bewust in .mjs zodat zowel de webapp (TypeScript) als het CLI-script
 * scripts/maak-leerlingen.mjs dezelfde regels gebruiken. Anders zou een leerling
 * via het script een andere gebruikersnaam krijgen dan via het portaal.
 */
import { randomInt } from 'node:crypto';

const WOORDEN = [
  'appel', 'brug', 'daver', 'eiland', 'fazant', 'gracht', 'haven', 'ijzer', 'kade', 'lantaarn',
  'molen', 'noord', 'oever', 'polder', 'rots', 'schans', 'toren', 'vaart', 'wilg', 'zolder',
];

/**
 * Drie losse woorden met een getal: makkelijk voor te lezen aan een klas en
 * makkelijk over te typen, in tegenstelling tot willekeurige tekens.
 */
export function maakWachtwoord() {
  const eerste = randomInt(WOORDEN.length);
  // Tweede woord verschuiven zodat je nooit "appel-appel-53" krijgt.
  const tweede = (eerste + 1 + randomInt(WOORDEN.length - 1)) % WOORDEN.length;
  return `${WOORDEN[eerste]}-${WOORDEN[tweede]}-${randomInt(10, 100)}`;
}

/**
 * "Youssef El Amrani" wordt "youssef.el.amrani".
 * Accenten verdwijnen, want die zijn lastig op een schoolklavier.
 * `bezet` bevat de namen die al in gebruik zijn; bij een dubbel krijgt de
 * tweede een cijfer (jan.peeters2).
 */
export function maakGebruikersnaam(naam, bezet = new Set()) {
  const basis = String(naam)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z\s]/g, '')
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .join('.');

  if (!basis) return '';

  let kandidaat = basis;
  let n = 2;
  while (bezet.has(kandidaat)) kandidaat = `${basis}${n++}`;
  return kandidaat;
}
