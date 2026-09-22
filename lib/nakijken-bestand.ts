import 'server-only';
import type { Werkmap } from '@/lib/werkmap-lezen';
import type { CheckResultaat } from '@/lib/nakijken';

/**
 * Nakijken van een ingediend .xlsx-bestand.
 *
 * Dit is een apart soort controle dan die op het rekenblad in de browser: hier
 * kijken we naar dingen die alleen in een echt Excel-bestand bestaan —
 * grafieken, draaitabellen en afdrukinstellingen.
 */

export type BestandCheck = {
  id: string;
  omschrijving: string;
  punten: number;
  hint: string;
  eis:
    | {
        soort: 'grafiek';
        /** Toegestane grafiektypes, bv. ['barChart', 'bar3DChart']. */
        types?: string[];
        minAantal?: number;
        titelBevat?: string;
        /** Het gegevensbereik moet naar deze kolom of dit blad verwijzen. */
        bereikBevat?: string;
        minReeksen?: number;
      }
    | {
        soort: 'draaitabel';
        minAantal?: number;
        minRijvelden?: number;
        minKolomvelden?: number;
        minGegevensvelden?: number;
        veldenBevat?: string[];
        functie?: string;
      }
    | {
        soort: 'afdruk';
        liggend?: boolean;
        passendBreed?: number;
        passendMaken?: boolean;
        paginanummer?: boolean;
        kopVoettekst?: boolean;
        titelrijen?: boolean;
        rasterlijnen?: boolean;
        maxMarge?: number;
      };
};

function normaliseer(tekst: string): string {
  return tekst.toLowerCase().replace(/[\s_]/g, '');
}

function controleerGrafiek(eis: Extract<BestandCheck['eis'], { soort: 'grafiek' }>, w: Werkmap): string[] {
  const grafieken = w.grafieken;

  if (grafieken.length < (eis.minAantal ?? 1)) {
    return [
      grafieken.length === 0
        ? 'er staat nog geen grafiek in het bestand'
        : `er staan ${grafieken.length} grafieken in plaats van ${eis.minAantal}`,
    ];
  }

  /** Alles wat er aan één grafiek mis is. Leeg = die grafiek voldoet. */
  function bezwaren(g: Werkmap['grafieken'][number]): string[] {
    const lijst: string[] = [];
    if (eis.types && !eis.types.includes(g.soort)) {
      lijst.push(`het grafiektype klopt niet — gevonden: ${g.soort}`);
    }
    if (eis.titelBevat && !normaliseer(g.titel ?? '').includes(normaliseer(eis.titelBevat))) {
      lijst.push(
        g.titel
          ? `de titel is "${g.titel}" in plaats van "${eis.titelBevat}"`
          : `de grafiek heeft nog geen titel "${eis.titelBevat}"`,
      );
    }
    if (eis.bereikBevat && !g.bereiken.some((b) => normaliseer(b).includes(normaliseer(eis.bereikBevat!)))) {
      lijst.push(`de grafiek haalt zijn gegevens niet uit ${eis.bereikBevat}`);
    }
    if (eis.minReeksen && g.reeksen < eis.minReeksen) {
      lijst.push(
        g.reeksen === 1
          ? `er staat maar één gegevensreeks in de grafiek in plaats van ${eis.minReeksen}`
          : `er staan ${g.reeksen} gegevensreeksen in de grafiek in plaats van ${eis.minReeksen}`,
      );
    }
    return lijst;
  }

  // Eén grafiek moet aan álle eisen voldoen — niet elk aan een andere. Klopt er
  // geen enkele, dan tonen we wat er scheelt aan de grafiek die er het dichtst bij zit.
  const alle = grafieken.map(bezwaren);
  if (alle.some((b) => b.length === 0)) return [];

  const dichtst = alle.reduce((a, b) => (b.length < a.length ? b : a));
  return dichtst.length ? dichtst : ['de grafiek voldoet niet aan de opdracht'];
}

function controleerDraaitabel(eis: Extract<BestandCheck['eis'], { soort: 'draaitabel' }>, w: Werkmap): string[] {
  const tabellen = w.draaitabellen;

  if (tabellen.length < (eis.minAantal ?? 1)) {
    return ['er staat nog geen draaitabel in het bestand'];
  }

  /** Alles wat er aan één draaitabel mis is. Leeg = die tabel voldoet. */
  function bezwaren(d: Werkmap['draaitabellen'][number]): string[] {
    const lijst: string[] = [];
    if (eis.minRijvelden && d.rijvelden < eis.minRijvelden) {
      lijst.push(
        d.rijvelden === 0
          ? 'er staat nog niets in het rijgebied van de draaitabel'
          : `er staan ${d.rijvelden} velden in het rijgebied in plaats van ${eis.minRijvelden}`,
      );
    }
    if (eis.minKolomvelden && d.kolomvelden < eis.minKolomvelden) {
      lijst.push('er staat nog niets in het kolomgebied van de draaitabel');
    }
    if (eis.minGegevensvelden && d.gegevensvelden < eis.minGegevensvelden) {
      lijst.push('er staat nog geen veld in het gegevensgebied');
    }
    if (eis.veldenBevat) {
      const ontbreekt = eis.veldenBevat.filter(
        (v) => !d.velden.some((veld) => normaliseer(veld) === normaliseer(v)),
      );
      if (ontbreekt.length) lijst.push(`deze velden ontbreken nog: ${ontbreekt.join(', ')}`);
    }
    if (eis.functie && !d.functies.some((f) => normaliseer(f) === normaliseer(eis.functie!))) {
      lijst.push(`de samenvattingsfunctie klopt niet — gevonden: ${d.functies.join(', ') || 'som'}`);
    }
    return lijst;
  }

  const alle = tabellen.map(bezwaren);
  if (alle.some((b) => b.length === 0)) return [];

  const dichtst = alle.reduce((a, b) => (b.length < a.length ? b : a));
  return dichtst.length ? dichtst : ['de draaitabel is niet opgebouwd zoals gevraagd'];
}

function controleerAfdruk(eis: Extract<BestandCheck['eis'], { soort: 'afdruk' }>, w: Werkmap): string[] {
  const fouten: string[] = [];
  const a = w.afdruk;
  if (!a) return ['de afdrukinstellingen konden niet gelezen worden'];

  if (eis.liggend !== undefined && a.liggend !== eis.liggend) {
    fouten.push(`het blad staat ${a.liggend ? 'liggend' : 'staand'} in plaats van ${eis.liggend ? 'liggend' : 'staand'}`);
  }
  if (eis.passendMaken && !a.passendMaken) {
    fouten.push('de optie om het blad passend te maken staat nog uit');
  }
  if (eis.passendBreed !== undefined && a.passendBreed !== eis.passendBreed) {
    fouten.push(`"pagina's breed" staat op ${a.passendBreed ?? 'niets'} in plaats van ${eis.passendBreed}`);
  }
  if (eis.kopVoettekst && !a.kopVoettekst) fouten.push('er is nog geen kop- of voettekst ingesteld');
  if (eis.paginanummer && !a.paginanummer) fouten.push('er staat nog geen paginanummer in de kop- of voettekst');
  if (eis.titelrijen && !a.titelrijenHerhalen) fouten.push('de titelrijen worden nog niet op elke pagina herhaald');
  if (eis.rasterlijnen && !a.rasterlijnenAfdrukken) fouten.push('de rasterlijnen worden nog niet mee afgedrukt');
  if (eis.maxMarge !== undefined && a.marges) {
    const tegroot = Object.entries(a.marges).filter(([, v]) => (v ?? 0) > eis.maxMarge!);
    if (tegroot.length) {
      fouten.push(`de marges zijn nog te breed (${tegroot.map(([k]) => k).join(', ')})`);
    }
  }
  return fouten;
}

export function kijkBestandNa(checks: BestandCheck[], werkmap: Werkmap) {
  const resultaten: CheckResultaat[] = checks.map((check) => {
    const fouten =
      check.eis.soort === 'grafiek' ? controleerGrafiek(check.eis, werkmap)
      : check.eis.soort === 'draaitabel' ? controleerDraaitabel(check.eis, werkmap)
      : controleerAfdruk(check.eis, werkmap);

    return {
      checkId: check.id,
      omschrijving: check.omschrijving,
      punten: check.punten,
      behaald: fouten.length === 0,
      feedback: fouten.length === 0 ? 'Correct.' : `${fouten.slice(0, 3).join('; ')}. ${check.hint}`,
    };
  });

  const score = resultaten.filter((r) => r.behaald).reduce((s, r) => s + r.punten, 0);
  const maxScore = checks.reduce((s, c) => s + c.punten, 0);
  return { score, maxScore, resultaten };
}
