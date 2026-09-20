import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { logGebeurtenissen, type Gebeurtenis } from '@/lib/opslag';

const TOEGESTAAN = new Set<Gebeurtenis['soort']>([
  'verborgen', 'zichtbaar', 'focus_weg', 'focus_terug', 'hartslag', 'geplakt', 'gestart',
]);

export async function POST(request: Request) {
  const sessie = await huidigeSessie();
  if (!sessie) return NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 });

  const { gebeurtenissen } = (await request.json()) as { gebeurtenissen: Gebeurtenis[] };
  if (!Array.isArray(gebeurtenissen)) {
    return NextResponse.json({ fout: 'Ongeldige gegevens.' }, { status: 400 });
  }

  // De gebruikersnaam komt uit de sessie, nooit uit de request-body:
  // anders kan een leerling gebeurtenissen op naam van iemand anders posten.
  const opgeschoond = gebeurtenissen
    .filter((g) => TOEGESTAAN.has(g.soort))
    .slice(0, 200)
    .map((g) => ({
      pogingId: String(g.pogingId ?? '').slice(0, 64),
      gebruikersnaam: sessie.gebruikersnaam,
      soort: g.soort,
      tijdstip: Number(g.tijdstip) || Date.now(),
      duurMs: Number.isFinite(Number(g.duurMs)) ? Number(g.duurMs) : undefined,
    }));

  await logGebeurtenissen(opgeschoond);
  return NextResponse.json({ ok: true, aantal: opgeschoond.length });
}
