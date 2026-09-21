import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { kijkNa } from '@/lib/nakijken';
import { SLEUTELS } from '@/data/oefeningen/sleutels';
import { bewaarPoging, sessieHoortBij } from '@/lib/opslag';
import type { BladInzending, CelInzending } from '@/lib/werkblad-types';

export async function POST(request: Request) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const { oefeningId, sessieId, inzending, blad } = (await request.json()) as {
    oefeningId: string;
    sessieId: string;
    inzending: CelInzending[];
    blad?: BladInzending;
  };

  const checks = SLEUTELS[oefeningId];
  if (!checks) return NextResponse.json({ fout: 'Onbekende oefening.' }, { status: 404 });

  // Een leerling mag alleen op zijn eigen sessie indienen.
  if (!sessieId || !(await sessieHoortBij(sessieId, aangemeld.gebruikersnaam))) {
    return NextResponse.json({ fout: 'Deze oefensessie is niet van jou.' }, { status: 403 });
  }

  const { score, maxScore, resultaten } = kijkNa(checks, inzending ?? [], blad);

  try {
    const pogingNummer = await bewaarPoging({
      sessieId,
      gebruikersnaam: aangemeld.gebruikersnaam,
      oefeningId,
      score,
      maxScore,
      resultaten,
    });
    return NextResponse.json({ score, maxScore, resultaten, pogingNummer });
  } catch (e) {
    console.error('[nakijken]', e);
    // De leerling ziet zijn feedback hoe dan ook; alleen het bewaren mislukte.
    return NextResponse.json(
      { score, maxScore, resultaten, pogingNummer: null, waarschuwing: 'Je resultaat kon niet bewaard worden.' },
      { status: 200 },
    );
  }
}
