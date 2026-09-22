import 'server-only';
import { unzipSync, strFromU8 } from 'fflate';

/**
 * Leest een ingediend .xlsx-bestand uit.
 *
 * Een .xlsx is een zipbestand met XML erin. Grafieken, draaitabellen en
 * afdrukinstellingen zitten in aparte onderdelen die het rekenblad in de
 * browser niet kan maken — daarom laten we die drie onderwerpen in echt Excel
 * doen en kijken we het ingediende bestand hier na.
 */

export type Grafiek = {
  /** barChart, lineChart, pieChart … */
  soort: string;
  titel: string | null;
  /** De bereiken waar de grafiek zijn gegevens haalt, bv. Omzet!$B$2:$B$5. */
  bereiken: string[];
  /** Het aantal gegevensreeksen (<c:ser>) in de grafiek. */
  reeksen: number;
};

export type Draaitabel = {
  naam: string | null;
  /** Veldnamen uit de brongegevens. */
  velden: string[];
  /** Welke assen gebruikt zijn: rij, kolom, gegevens, filter. */
  rijvelden: number;
  kolomvelden: number;
  gegevensvelden: number;
  /** De gebruikte samenvattingsfuncties, bv. sum, count, average. */
  functies: string[];
};

export type Afdruk = {
  liggend: boolean;
  passendBreed: number | null;
  passendHoog: number | null;
  passendMaken: boolean;
  kopVoettekst: boolean;
  koptekst: string;
  voettekst: string;
  paginanummer: boolean;
  titelrijenHerhalen: boolean;
  marges: { boven?: number; onder?: number; links?: number; rechts?: number } | null;
  rasterlijnenAfdrukken: boolean;
};

export type Werkmap = {
  bladnamen: string[];
  grafieken: Grafiek[];
  draaitabellen: Draaitabel[];
  afdruk: Afdruk | null;
  /** Celwaarden per blad, als "Blad!A1" → waarde. Alleen wat nodig is voor checks. */
  cellen: Record<string, string>;
};

/**
 * Niet elk programma schrijft dezelfde naamruimte. Excel gebruikt <c:title>,
 * andere hulpmiddelen schrijven gewoon <title>. We aanvaarden beide, anders
 * lezen we een bestand van de ene bron wel en van de andere niet.
 */
const MET_OF_ZONDER = '(?:c:)?';

const SOORTEN = [
  'barChart', 'bar3DChart', 'lineChart', 'line3DChart', 'pieChart', 'pie3DChart',
  'scatterChart', 'areaChart', 'doughnutChart', 'radarChart', 'bubbleChart',
];

function alleTreffers(xml: string, patroon: RegExp): string[] {
  return [...xml.matchAll(patroon)].map((m) => m[1]);
}

export function leesWerkmap(inhoud: Uint8Array): Werkmap {
  let bestanden: Record<string, Uint8Array>;
  try {
    bestanden = unzipSync(inhoud);
  } catch {
    throw new Error('Dit is geen geldig .xlsx-bestand. Sla op als "Excel-werkmap (*.xlsx)".');
  }

  const tekst = (naam: string) =>
    bestanden[naam] ? strFromU8(bestanden[naam]) : '';

  const namen = Object.keys(bestanden);

  // --- Bladnamen ---
  const werkboek = tekst('xl/workbook.xml');
  const bladnamen = alleTreffers(werkboek, /<sheet[^>]*name="([^"]+)"/g);

  // --- Grafieken ---
  const grafieken: Grafiek[] = [];
  for (const naam of namen.filter((n) => /^xl\/charts\/chart\d+\.xml$/.test(n))) {
    const xml = tekst(naam);
    const soort = SOORTEN.find((s) => new RegExp(`<${MET_OF_ZONDER}${s}[\\s>]`).test(xml)) ?? 'onbekend';
    const titel =
      xml.match(new RegExp(`<${MET_OF_ZONDER}title>[\\s\\S]*?<a:t>([^<]*)</a:t>`))?.[1] ?? null;
    const bereiken = alleTreffers(xml, new RegExp(`<${MET_OF_ZONDER}f>([^<]+)</${MET_OF_ZONDER}f>`, 'g'));
    const reeksen = (xml.match(new RegExp(`<${MET_OF_ZONDER}ser[\\s>]`, 'g')) ?? []).length;
    grafieken.push({ soort, titel, bereiken, reeksen });
  }

  // --- Draaitabellen ---
  const draaitabellen: Draaitabel[] = [];
  const cacheVelden = namen
    .filter((n) => /^xl\/pivotCache\/pivotCacheDefinition\d+\.xml$/.test(n))
    .flatMap((n) => alleTreffers(tekst(n), /<cacheField[^>]*name="([^"]+)"/g));

  for (const naam of namen.filter((n) => /^xl\/pivotTables\/pivotTable\d+\.xml$/.test(n))) {
    const xml = tekst(naam);
    const assen = alleTreffers(xml, /<pivotField[^>]*axis="([^"]+)"/g);
    draaitabellen.push({
      naam: xml.match(/<pivotTableDefinition[^>]*name="([^"]+)"/)?.[1] ?? null,
      velden: cacheVelden,
      rijvelden: assen.filter((a) => a === 'axisRow').length,
      kolomvelden: assen.filter((a) => a === 'axisCol').length,
      gegevensvelden: (xml.match(/<dataField[\s/>]/g) ?? []).length,
      functies: alleTreffers(xml, /<dataField[^>]*subtotal="([^"]+)"/g),
    });
  }

  // --- Afdrukinstellingen van het eerste blad ---
  const eersteBlad = namen.filter((n) => /^xl\/worksheets\/sheet\d+\.xml$/.test(n)).sort()[0];
  let afdruk: Afdruk | null = null;
  if (eersteBlad) {
    const xml = tekst(eersteBlad);
    const ps = xml.match(/<pageSetup[^>]*>/)?.[0] ?? '';
    const marges = xml.match(/<pageMargins[^>]*>/)?.[0] ?? '';
    const getal = (bron: string, veld: string) => {
      const m = bron.match(new RegExp(`${veld}="([\\d.]+)"`));
      return m ? Number(m[1]) : undefined;
    };
    const koptekst = xml.match(/<oddHeader>([\s\S]*?)<\/oddHeader>/)?.[1] ?? '';
    const voettekst = xml.match(/<oddFooter>([\s\S]*?)<\/oddFooter>/)?.[1] ?? '';

    afdruk = {
      liggend: /orientation="landscape"/.test(ps),
      passendBreed: getal(ps, 'fitToWidth') ?? null,
      passendHoog: getal(ps, 'fitToHeight') ?? null,
      passendMaken: /fitToPage="(1|true)"/.test(xml),
      kopVoettekst: xml.includes('<headerFooter'),
      koptekst,
      voettekst,
      // &P is het paginanummer in de opmaakcode van een kop- of voettekst.
      paginanummer: /&amp;P|&P/.test(koptekst + voettekst),
      titelrijenHerhalen: /_xlnm\.Print_Titles/.test(werkboek),
      marges: marges
        ? {
            boven: getal(marges, 'top'),
            onder: getal(marges, 'bottom'),
            links: getal(marges, 'left'),
            rechts: getal(marges, 'right'),
          }
        : null,
      rasterlijnenAfdrukken: /<printOptions[^>]*gridLines="(1|true)"/.test(xml),
    } as Afdruk;
  }

  return { bladnamen, grafieken, draaitabellen, afdruk, cellen: {} };
}
