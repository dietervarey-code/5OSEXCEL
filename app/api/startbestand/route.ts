import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { vindOpgave } from '@/data/oefeningen';
import { isUpload } from '@/lib/werkblad-types';
import { maakStartbestand, startbestandNaam } from '@/lib/startbestand';

/** Levert het .xlsx-bestand waarmee de leerling in Excel begint. */
export async function GET(request: Request) {
  const sessie = await huidigeSessie();
  if (!sessie) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const id = new URL(request.url).searchParams.get('oefening') ?? '';
  const opgave = vindOpgave(id);
  if (!opgave || !isUpload(opgave)) {
    return NextResponse.json({ fout: 'Deze oefening heeft geen startbestand.' }, { status: 404 });
  }

  const bestand = maakStartbestand(opgave);
  return new NextResponse(bestand as unknown as BodyInit, {
    headers: {
      'content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'content-disposition': `attachment; filename="${startbestandNaam(opgave)}"`,
      'cache-control': 'no-store',
    },
  });
}
