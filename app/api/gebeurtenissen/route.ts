import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { logGebeurtenissen, raakSessieAan, sessieHoortBij, type Gebeurtenis, type GebeurtenisSoort } from '@/lib/opslag';

const TOEGESTAAN = new Set<GebeurtenisSoort>([
  'gestart', 'verborgen', 'zichtbaar', 'focus_weg', 'focus_terug', 'hartslag', 'geplakt',
]);

export async function POST(request: Request) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const { gebeurtenissen } = (await request.json()) as { gebeurtenissen: Gebeurtenis[] };
  if (!Array.isArray(gebeurtenissen) || gebeurtenissen.length === 0) {
    return NextResponse.json({ ok: true, aantal: 0 });
  }

  // Alles komt uit één oefensessie; die moet van deze leerling zijn.
  const sessieId = String(gebeurtenissen[0]?.sessieId ?? '');
  if (!sessieId || !(await sessieHoortBij(sessieId, aangemeld.gebruikersnaam))) {
    return NextResponse.json({ fout: 'Deze oefensessie is niet van jou.' }, { status: 403 });
  }

  // De gebruikersnaam komt uit de sessiecookie, nooit uit de request-body:
  // anders kan een leerling gebeurtenissen op naam van iemand anders posten.
  const opgeschoond: Gebeurtenis[] = gebeurtenissen
    .filter((g) => TOEGESTAAN.has(g.soort) && g.sessieId === sessieId)
    .slice(0, 200)
    .map((g) => ({
      sessieId,
      soort: g.soort,
      tijdstip: Number(g.tijdstip) || Date.now(),
      duurMs: Number.isFinite(Number(g.duurMs)) ? Number(g.duurMs) : undefined,
    }));

  try {
    const aantal = await logGebeurtenissen(aangemeld.gebruikersnaam, opgeschoond);
    await raakSessieAan(sessieId);
    return NextResponse.json({ ok: true, aantal });
  } catch (e) {
    console.error('[gebeurtenissen]', e);
    // Telemetrie mag het oefenen nooit blokkeren.
    return NextResponse.json({ ok: false }, { status: 200 });
  }
}
