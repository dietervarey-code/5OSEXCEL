import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { vindOpgave } from '@/data/oefeningen';
import { isUpload } from '@/lib/werkblad-types';
import { BESTANDSLEUTELS } from '@/data/oefeningen/sleutels';
import { kijkBestandNa } from '@/lib/nakijken-bestand';
import { leesWerkmap } from '@/lib/werkmap-lezen';
import { bewaarPoging, sessieHoortBij, verklaar } from '@/lib/opslag';
import { INZENDINGEN, OpslagFout, uploadBestand, veiligePadnaam } from '@/lib/bestanden';
import { ConfiguratieFout } from '@/lib/supabase';

/** 15 MB — ruim voor een werkmap met een draaitabel en een grafiek. */
const MAX_BYTES = 15 * 1024 * 1024;

export async function POST(request: Request) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const form = await request.formData();
  const oefeningId = String(form.get('oefeningId') ?? '');
  const sessieId = String(form.get('sessieId') ?? '');
  const bestand = form.get('bestand');

  const opgave = vindOpgave(oefeningId);
  const checks = BESTANDSLEUTELS[oefeningId];
  if (!opgave || !isUpload(opgave) || !checks) {
    return NextResponse.json({ fout: 'Onbekende oefening.' }, { status: 404 });
  }

  if (!(bestand instanceof File)) {
    return NextResponse.json({ fout: 'Er is geen bestand meegestuurd.' }, { status: 400 });
  }
  if (bestand.size > MAX_BYTES) {
    return NextResponse.json(
      { fout: `Dat bestand is te groot (max ${Math.round(MAX_BYTES / 1024 / 1024)} MB).` },
      { status: 400 },
    );
  }
  if (!bestand.name.toLowerCase().endsWith('.xlsx')) {
    return NextResponse.json(
      { fout: 'Sla je werk op als .xlsx. Een .xls of .ods kan ik niet nakijken.' },
      { status: 400 },
    );
  }

  const bytes = await bestand.arrayBuffer();

  // 1. Nakijken gebeurt altijd — ook als het bewaren straks mislukt.
  let resultaat;
  try {
    resultaat = kijkBestandNa(checks, leesWerkmap(new Uint8Array(bytes)));
  } catch (e) {
    return NextResponse.json(
      { fout: e instanceof Error ? e.message : 'Het bestand kon niet gelezen worden.' },
      { status: 400 },
    );
  }

  // 2. Bewaren: het bestand voor de leerkracht, de score voor het overzicht.
  const eigenSessie = sessieId && (await sessieHoortBij(sessieId, aangemeld.gebruikersnaam));
  if (!eigenSessie) {
    return NextResponse.json({ ...resultaat, pogingNummer: null, waarschuwing: 'Je resultaat kon niet bewaard worden.' });
  }

  // Het bestand opbergen is fijn voor de leerkracht, maar de score telt zwaarder.
  // Lukt het opbergen niet — bucket vergeten, opslag vol — dan bewaren we de
  // poging alsnog, zonder pad.
  let bestandPad: string | undefined;
  let opslagWaarschuwing: string | null = null;
  try {
    const pad = veiligePadnaam(`${aangemeld.gebruikersnaam}/${oefeningId}`, bestand.name);
    await uploadBestand(pad, bytes, bestand.type || 'application/octet-stream', INZENDINGEN);
    bestandPad = pad;
  } catch (e) {
    console.error('[indienen] bestand opbergen mislukte:', e);
    opslagWaarschuwing =
      e instanceof ConfiguratieFout || e instanceof OpslagFout ? e.message
      : e instanceof Error ? verklaar(e.message)
      : null;
  }

  try {
    const pogingNummer = await bewaarPoging({
      sessieId,
      gebruikersnaam: aangemeld.gebruikersnaam,
      oefeningId,
      score: resultaat.score,
      maxScore: resultaat.maxScore,
      resultaten: resultaat.resultaten,
      bestandPad,
    });
    return NextResponse.json({
      ...resultaat,
      pogingNummer,
      // De score staat genoteerd; alleen het bestand zelf ontbreekt.
      ...(opslagWaarschuwing
        ? { waarschuwing: `Je score is bewaard, maar je bestand niet: ${opslagWaarschuwing}` }
        : {}),
    });
  } catch (e) {
    console.error('[indienen]', e);
    const uitleg =
      e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : null;
    return NextResponse.json({
      ...resultaat,
      pogingNummer: null,
      waarschuwing: uitleg ?? 'Je resultaat kon niet bewaard worden.',
    });
  }
}
