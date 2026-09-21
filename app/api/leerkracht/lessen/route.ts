import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { maakLes, wijzigLes, verwijderLes } from '@/lib/lessen';
import { verklaar } from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';

async function leerkrachtOfNiets() {
  const sessie = await huidigeSessie();
  if (!sessie) return { fout: NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 }) };
  if (sessie.rol !== 'leerkracht') return { fout: NextResponse.json({ fout: 'Geen toegang.' }, { status: 403 }) };
  return { sessie };
}

function foutAntwoord(e: unknown, standaard: string) {
  console.error('[lessen]', e);
  return NextResponse.json(
    {
      fout:
        e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : standaard,
    },
    { status: 500 },
  );
}

export async function POST(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const body = (await request.json()) as {
    focus?: number;
    titel?: string;
    samenvatting?: string;
    inhoud?: string;
    oefeningId?: string | null;
    volgnummer?: number;
  };

  const focus = Number(body.focus);
  if (!Number.isInteger(focus) || focus < 1 || focus > 9) {
    return NextResponse.json({ fout: 'Kies een focus tussen 1 en 9.' }, { status: 400 });
  }
  if (!body.titel?.trim()) {
    return NextResponse.json({ fout: 'Geef de les een titel.' }, { status: 400 });
  }

  try {
    const id = await maakLes({
      focus,
      titel: body.titel.trim(),
      samenvatting: (body.samenvatting ?? '').trim(),
      inhoud: body.inhoud ?? '',
      oefeningId: body.oefeningId?.trim() || null,
      volgnummer: Number(body.volgnummer) || 0,
    });
    return NextResponse.json({ id });
  } catch (e) {
    return foutAntwoord(e, 'Les aanmaken mislukte.');
  }
}

export async function PATCH(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { id, ...velden } = (await request.json()) as { id?: string } & Record<string, unknown>;
  if (!id) return NextResponse.json({ fout: 'Geen les opgegeven.' }, { status: 400 });

  if (velden.focus !== undefined) {
    const focus = Number(velden.focus);
    if (!Number.isInteger(focus) || focus < 1 || focus > 9) {
      return NextResponse.json({ fout: 'Kies een focus tussen 1 en 9.' }, { status: 400 });
    }
    velden.focus = focus;
  }

  try {
    const gelukt = await wijzigLes(id, velden as Parameters<typeof wijzigLes>[1]);
    if (!gelukt) return NextResponse.json({ fout: 'Onbekende les.' }, { status: 404 });
    return NextResponse.json({ ok: true });
  } catch (e) {
    return foutAntwoord(e, 'Les bijwerken mislukte.');
  }
}

export async function DELETE(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { id } = (await request.json()) as { id?: string };
  if (!id) return NextResponse.json({ fout: 'Geen les opgegeven.' }, { status: 400 });

  try {
    const gelukt = await verwijderLes(id);
    if (!gelukt) return NextResponse.json({ fout: 'Onbekende les.' }, { status: 404 });
    return NextResponse.json({ ok: true });
  } catch (e) {
    return foutAntwoord(e, 'Les verwijderen mislukte.');
  }
}
