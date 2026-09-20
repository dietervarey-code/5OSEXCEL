import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { kijkNa } from '@/lib/nakijken';
import { SLEUTELS } from '@/data/oefeningen/sleutels';
import { bewaarResultaat, startPoging, allePogingen } from '@/lib/opslag';
import type { CelInzending } from '@/lib/werkblad-types';

export async function POST(request: Request) {
  const sessie = await huidigeSessie();
  if (!sessie) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const { oefeningId, inzending } = (await request.json()) as {
    oefeningId: string;
    inzending: CelInzending[];
  };

  const checks = SLEUTELS[oefeningId];
  if (!checks) return NextResponse.json({ fout: 'Onbekende oefening.' }, { status: 404 });

  const { score, maxScore, resultaten } = kijkNa(checks, inzending ?? []);

  // Elke keer nakijken telt als een poging, zodat je ziet hoe vaak iemand
  // moest proberen voor het klopte.
  const poging = await startPoging({
    gebruikersnaam: sessie.gebruikersnaam,
    naam: sessie.naam,
    klas: sessie.klas,
    oefeningId,
  });
  await bewaarResultaat(poging.id, score, maxScore, resultaten);

  const pogingen = (await allePogingen()).filter(
    (p) => p.gebruikersnaam === sessie.gebruikersnaam && p.oefeningId === oefeningId,
  );

  return NextResponse.json({ score, maxScore, resultaten, pogingNummer: pogingen.length });
}
