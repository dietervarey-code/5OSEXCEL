import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { pogingenVan } from '@/lib/opslag';
import { INZENDINGEN, tijdelijkeLink } from '@/lib/bestanden';

/**
 * Stuurt de leerkracht door naar het werk dat een leerling indiende.
 *
 * Het pad komt uit de zoekbalk, dus we vertrouwen het niet: we kijken eerst na
 * dat er echt een poging van die leerling met dat pad bestaat. Zo kan niemand
 * met een gefabriceerd pad in de bucket rondneuzen.
 */
export async function GET(request: Request) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld || aangemeld.rol !== 'leerkracht') {
    return NextResponse.json({ fout: 'Geen toegang.' }, { status: 403 });
  }

  const params = new URL(request.url).searchParams;
  const leerling = params.get('leerling') ?? '';
  const pad = params.get('pad') ?? '';
  if (!leerling || !pad) {
    return NextResponse.json({ fout: 'Leerling of pad ontbreekt.' }, { status: 400 });
  }

  const pogingen = await pogingenVan(leerling);
  if (!pogingen.some((p) => p.bestandPad === pad)) {
    return NextResponse.json({ fout: 'Dat bestand hoort niet bij deze leerling.' }, { status: 404 });
  }

  const link = await tijdelijkeLink(pad, INZENDINGEN);
  if (!link) {
    return NextResponse.json({ fout: 'De link naar het bestand kon niet gemaakt worden.' }, { status: 502 });
  }
  return NextResponse.redirect(link);
}
