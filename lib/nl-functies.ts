/**
 * Nederlandse functienamen voor het werkblad.
 *
 * De cursus (ICT-vademecum, Focus 1-9) en het stagewerkveld gebruiken de
 * Nederlandse Excel-namen: SOM, ALS, VERT.ZOEKEN, AANTAL.ALS ...
 * De rekenmachine van Univer kent enkel de Engelse namen. We registreren de
 * Nederlandse namen daarom als echte functies, zodat een leerling letterlijk
 * typt wat in de cursus staat.
 */

type Waarde = number | string | boolean | null;
type Arg = Waarde | Waarde[] | Waarde[][];

/** Zet een bereik (2D), een rij (1D) of een losse waarde om naar een vlakke lijst. */
function vlak(arg: Arg): Waarde[] {
  if (Array.isArray(arg)) return arg.flat(2) as Waarde[];
  return [arg];
}

/**
 * Haalt één waarde uit een argument.
 *
 * De rekenmachine geeft ook een verwijzing naar één cel door als array — `A1`
 * komt binnen als [[42]]. Dat is onschuldig zolang je ermee rekent (Number()
 * verstaat het), maar niet bij een vergelijking of een waarheidswaarde: een
 * array is in JavaScript altijd waar, waardoor ALS steevast de ja-tak koos en
 * VERT.ZOEKEN nooit iets vond. Elk argument dat één waarde hoort te zijn, gaat
 * daarom eerst hierlangs.
 */
function enkel(arg: Arg): Waarde {
  if (!Array.isArray(arg)) return arg;
  const plat = arg.flat(2) as Waarde[];
  return plat.length > 0 ? plat[0] : null;
}

/** Enkel de cellen die echt een getal bevatten — lege cellen en tekst tellen niet mee. */
function getallen(args: Arg[]): number[] {
  return args
    .flatMap(vlak)
    .filter((w): w is number => typeof w === 'number' && !Number.isNaN(w));
}

/** Maakt van een bereik altijd een 2D-tabel, ook als het één rij of één cel is. */
function tabel(arg: Arg): Waarde[][] {
  if (!Array.isArray(arg)) return [[arg]];
  if (!Array.isArray(arg[0])) return [arg as Waarde[]];
  return arg as Waarde[][];
}

/**
 * Bootst het criterium van SOM.ALS / AANTAL.ALS na: ">100", "<=5", "<>x",
 * een exacte waarde, of tekst met jokertekens (* en ?).
 */
function voldoetAan(waarde: Waarde, criterium: Waarde): boolean {
  if (typeof criterium === 'string') {
    const m = criterium.match(/^(>=|<=|<>|>|<|=)\s*(.*)$/);
    if (m) {
      const [, operator, rest] = m;
      const rechts: Waarde = rest === '' ? '' : Number.isNaN(Number(rest)) ? rest : Number(rest);
      switch (operator) {
        case '>': return Number(waarde) > Number(rechts);
        case '<': return Number(waarde) < Number(rechts);
        case '>=': return Number(waarde) >= Number(rechts);
        case '<=': return Number(waarde) <= Number(rechts);
        case '<>': return String(waarde).toLowerCase() !== String(rechts).toLowerCase();
        case '=': return String(waarde).toLowerCase() === String(rechts).toLowerCase();
      }
    }
    if (criterium.includes('*') || criterium.includes('?')) {
      const patroon = new RegExp(
        '^' + criterium.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.') + '$',
        'i',
      );
      return patroon.test(String(waarde));
    }
    return String(waarde).toLowerCase() === criterium.toLowerCase();
  }
  return waarde === criterium;
}

function zoekInTabel(zoekwaarde: Waarde, rijen: Waarde[][], index: number, benaderend: boolean, horizontaal: boolean) {
  const lijnen = horizontaal ? rijen : rijen.map((_, i) => rijen[i]);
  const sleutels = horizontaal ? (rijen[0] ?? []) : rijen.map((r) => r[0]);

  if (!benaderend) {
    const pos = sleutels.findIndex((s) =>
      typeof s === 'string' && typeof zoekwaarde === 'string'
        ? s.toLowerCase() === zoekwaarde.toLowerCase()
        : s === zoekwaarde,
    );
    if (pos === -1) return '#N/B';
    return horizontaal ? (rijen[index - 1]?.[pos] ?? '#VERW!') : (lijnen[pos]?.[index - 1] ?? '#VERW!');
  }

  // Benaderend: grootste sleutel die niet groter is dan de zoekwaarde.
  let beste = -1;
  for (let i = 0; i < sleutels.length; i++) {
    if (Number(sleutels[i]) <= Number(zoekwaarde)) beste = i;
    else break;
  }
  if (beste === -1) return '#N/B';
  return horizontaal ? (rijen[index - 1]?.[beste] ?? '#VERW!') : (lijnen[beste]?.[index - 1] ?? '#VERW!');
}

export type NlFunctie = { naam: string; uitleg: string; fn: (...args: Arg[]) => Waarde | Waarde[][] };

export const NL_FUNCTIES: NlFunctie[] = [
  // --- Focus 1: gegevens herschikken ---
  // Het rekenblad in de browser kent geen "Plakken speciaal > Transponeren";
  // dat zit alleen in echt Excel. Met deze functie kan de leerling hier
  // hetzelfde bereiken. Ze geeft een tabel terug, die over de cellen eronder
  // en ernaast uitvloeit.
  { naam: 'TRANSPONEREN', uitleg: 'Kantelt een bereik: rijen worden kolommen.', fn: (bereik) => {
      const t = tabel(bereik);
      const kolommen = Math.max(0, ...t.map((r) => r.length));
      return Array.from({ length: kolommen }, (_, k) =>
        Array.from({ length: t.length }, (_, r) => t[r]?.[k] ?? null),
      );
    } },

  // --- Focus 2: rekenen ---
  { naam: 'SOM', uitleg: 'Telt alle getallen in een bereik op.', fn: (...a) => getallen(a).reduce((s, n) => s + n, 0) },
  { naam: 'GEMIDDELDE', uitleg: 'Berekent het rekenkundig gemiddelde.', fn: (...a) => { const g = getallen(a); return g.length ? g.reduce((s, n) => s + n, 0) / g.length : '#DEEL/0!'; } },
  { naam: 'MAX', uitleg: 'Geeft het grootste getal.', fn: (...a) => { const g = getallen(a); return g.length ? Math.max(...g) : 0; } },
  { naam: 'MIN', uitleg: 'Geeft het kleinste getal.', fn: (...a) => { const g = getallen(a); return g.length ? Math.min(...g) : 0; } },
  { naam: 'AANTAL', uitleg: 'Telt hoeveel cellen een getal bevatten.', fn: (...a) => getallen(a).length },
  { naam: 'AANTALARG', uitleg: 'Telt hoeveel cellen niet leeg zijn.', fn: (...a) => a.flatMap(vlak).filter((w) => w !== null && w !== '' && w !== undefined).length },
  { naam: 'AFRONDEN', uitleg: 'Rondt af op een aantal decimalen.', fn: (g, d) => { const f = 10 ** Number(enkel(d) ?? 0); return Math.round(Number(enkel(g)) * f) / f; } },
  { naam: 'ALS', uitleg: 'Geeft de ene waarde als de voorwaarde waar is, anders de andere.', fn: (v, waar, onwaar) => (enkel(v) ? enkel(waar) ?? true : enkel(onwaar) ?? false) },
  { naam: 'AANTAL.ALS', uitleg: 'Telt de cellen die aan een voorwaarde voldoen.', fn: (bereik, criterium) => vlak(bereik).filter((w) => voldoetAan(w, enkel(criterium))).length },
  { naam: 'SOM.ALS', uitleg: 'Telt de cellen op die aan een voorwaarde voldoen.', fn: (bereik, criterium, optelBereik) => {
      const sleutels = vlak(bereik);
      const waarden = optelBereik === undefined ? sleutels : vlak(optelBereik);
      const crit = enkel(criterium);
      return sleutels.reduce<number>((som, s, i) => (voldoetAan(s, crit) && typeof waarden[i] === 'number' ? som + (waarden[i] as number) : som), 0);
    } },

  // --- Focus 2 + 8: zoekfuncties ---
  { naam: 'VERT.ZOEKEN', uitleg: 'Zoekt een waarde in de eerste kolom en geeft een waarde uit dezelfde rij.', fn: (z, t, i, b) => zoekInTabel(enkel(z), tabel(t), Number(enkel(i)), b === undefined ? true : Boolean(enkel(b)), false) },
  { naam: 'HORIZ.ZOEKEN', uitleg: 'Zoekt een waarde in de eerste rij en geeft een waarde uit dezelfde kolom.', fn: (z, t, i, b) => zoekInTabel(enkel(z), tabel(t), Number(enkel(i)), b === undefined ? true : Boolean(enkel(b)), true) },
  { naam: 'X.ZOEKEN', uitleg: 'Zoekt een waarde en geeft het overeenkomstige resultaat terug.', fn: (z, zoekBereik, resultaatBereik, alsLeeg) => {
      const sleutels = vlak(zoekBereik);
      const resultaten = vlak(resultaatBereik);
      const zoek = enkel(z);
      const pos = sleutels.findIndex((s) =>
        typeof s === 'string' && typeof zoek === 'string' ? s.toLowerCase() === zoek.toLowerCase() : s === zoek,
      );
      if (pos === -1) return enkel(alsLeeg) ?? '#N/B';
      return resultaten[pos] ?? '#N/B';
    } },

  // --- Focus 8: datum en tekst ---
  { naam: 'VANDAAG', uitleg: 'Geeft de datum van vandaag.', fn: () => Math.floor(Date.now() / 86400000) + 25569 },
  { naam: 'JAAR', uitleg: 'Geeft het jaartal van een datum.', fn: (d) => new Date((Number(enkel(d)) - 25569) * 86400000).getUTCFullYear() },
  { naam: 'MAAND', uitleg: 'Geeft de maand van een datum.', fn: (d) => new Date((Number(enkel(d)) - 25569) * 86400000).getUTCMonth() + 1 },
  { naam: 'DAG', uitleg: 'Geeft de dag van een datum.', fn: (d) => new Date((Number(enkel(d)) - 25569) * 86400000).getUTCDate() },
  { naam: 'LINKS', uitleg: 'Geeft de eerste tekens van een tekst.', fn: (t, n) => String(enkel(t)).slice(0, Number(enkel(n) ?? 1)) },
  { naam: 'RECHTS', uitleg: 'Geeft de laatste tekens van een tekst.', fn: (t, n) => String(enkel(t)).slice(-Number(enkel(n) ?? 1)) },
  { naam: 'LENGTE', uitleg: 'Geeft het aantal tekens in een tekst.', fn: (t) => String(enkel(t) ?? '').length },
  { naam: 'EN', uitleg: 'Waar als alle voorwaarden waar zijn.', fn: (...a) => a.flatMap(vlak).every(Boolean) },
  { naam: 'OF', uitleg: 'Waar als minstens één voorwaarde waar is.', fn: (...a) => a.flatMap(vlak).some(Boolean) },
  { naam: 'NIET', uitleg: 'Keert waar en onwaar om.', fn: (v) => !enkel(v) },
];
