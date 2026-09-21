/**
 * De cursus schrijft functies met puntkomma's: =ALS(B5>100;"ja";"nee").
 * De rekenmachine van het werkblad verwacht komma's.
 *
 * Erger dan een foutmelding: met puntkomma's geeft ze géén fout maar een
 * verkeerd antwoord. =SOM(1;2;3) levert 0 op. Een leerling ziet niet wat er
 * scheelt. Daarom zetten we de puntkomma's om voor de formule bij de
 * rekenmachine terechtkomt.
 */

/** De Nederlandse waarheidswaarden uit de cursus. */
const WAARHEDEN: Record<string, string> = { WAAR: 'TRUE', ONWAAR: 'FALSE' };

/**
 * Vervangt puntkomma's door komma's en WAAR/ONWAAR door TRUE/FALSE, maar laat
 * alles binnen aanhalingstekens met rust: =ALS(A1>0;"ja; zeker";"nee") houdt
 * zijn tekst intact, en ook de tekst "ONWAAR" blijft staan.
 */
export function vertaalScheidingstekens(formule: string): string {
  if (!formule.startsWith('=')) return formule;
  if (!formule.includes(';') && !/\b(WAAR|ONWAAR)\b/i.test(formule)) return formule;

  let resultaat = '';
  let inTekst = false;

  for (let i = 0; i < formule.length; i++) {
    const teken = formule[i];

    if (teken === '"') {
      // Twee aanhalingstekens na elkaar zijn een ontsnapt aanhalingsteken.
      if (inTekst && formule[i + 1] === '"') {
        resultaat += '""';
        i++;
        continue;
      }
      inTekst = !inTekst;
      resultaat += teken;
      continue;
    }

    resultaat += teken === ';' && !inTekst ? ',' : teken;
  }

  // WAAR/ONWAAR alleen als los woord, en nooit binnen een tekst. Daarom werken
  // we op de stukken tussen de aanhalingstekens.
  return resultaat
    .split(/("(?:[^"]|"")*")/)
    .map((stuk, i) =>
      i % 2 === 1
        ? stuk
        : stuk.replace(/\b(WAAR|ONWAAR)\b/gi, (m) => WAARHEDEN[m.toUpperCase()] ?? m),
    )
    .join('');
}

/** Of er iets te vertalen viel. Gebruikt om onnodig herschrijven te vermijden. */
export function heeftPuntkommas(formule: string): boolean {
  return vertaalScheidingstekens(formule) !== formule;
}
