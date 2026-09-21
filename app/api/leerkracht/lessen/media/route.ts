import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { voegMediaToe, verwijderMedia } from '@/lib/lessen';
import {
  MAX_BYTES,
  bestandstypeToegestaan,
  toegestaneTypes,
  uploadBestand,
  veiligePadnaam,
  verwijderBestand,
} from '@/lib/bestanden';
import { insluitURL } from '@/lib/video';
import { verklaar } from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';

async function leerkrachtOfNiets() {
  const sessie = await huidigeSessie();
  if (!sessie) return { fout: NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 }) };
  if (sessie.rol !== 'leerkracht') return { fout: NextResponse.json({ fout: 'Geen toegang.' }, { status: 403 }) };
  return { sessie };
}

/**
 * Een video-link toevoegen (JSON), of een bestand opladen (multipart).
 */
export async function POST(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const type = request.headers.get('content-type') ?? '';

  try {
    // --- Bestand ---
    if (type.includes('multipart/form-data')) {
      const form = await request.formData();
      const lesId = String(form.get('lesId') ?? '');
      const bestand = form.get('bestand');

      if (!lesId) return NextResponse.json({ fout: 'Geen les opgegeven.' }, { status: 400 });
      if (!(bestand instanceof File)) {
        return NextResponse.json({ fout: 'Geen bestand meegestuurd.' }, { status: 400 });
      }
      if (bestand.size > MAX_BYTES) {
        return NextResponse.json(
          { fout: `Dat bestand is te groot (max ${Math.round(MAX_BYTES / 1024 / 1024)} MB).` },
          { status: 400 },
        );
      }
      if (!bestandstypeToegestaan(bestand.type)) {
        return NextResponse.json(
          { fout: `Dit bestandstype gaat niet. Toegestaan: ${toegestaneTypes()}.` },
          { status: 400 },
        );
      }

      const pad = veiligePadnaam(lesId, bestand.name);
      await uploadBestand(pad, await bestand.arrayBuffer(), bestand.type);
      await voegMediaToe({
        lesId,
        soort: 'bestand',
        titel: String(form.get('titel') ?? '').trim() || bestand.name,
        bron: pad,
      });
      return NextResponse.json({ ok: true });
    }

    // --- Video-link ---
    const { lesId, titel, url } = (await request.json()) as {
      lesId?: string;
      titel?: string;
      url?: string;
    };

    if (!lesId) return NextResponse.json({ fout: 'Geen les opgegeven.' }, { status: 400 });

    const insluiting = insluitURL(String(url ?? ''));
    if (!insluiting.ok) return NextResponse.json({ fout: insluiting.fout }, { status: 400 });

    await voegMediaToe({
      lesId,
      soort: 'video',
      titel: titel?.trim() || 'Filmpje',
      bron: insluiting.url,
    });
    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error('[lesmedia]', e);
    return NextResponse.json(
      {
        fout:
          e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : 'Toevoegen mislukte.',
      },
      { status: 500 },
    );
  }
}

export async function DELETE(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { id } = (await request.json()) as { id?: string };
  if (!id) return NextResponse.json({ fout: 'Niets opgegeven.' }, { status: 400 });

  try {
    const weg = await verwijderMedia(id);
    if (!weg) return NextResponse.json({ fout: 'Onbekend item.' }, { status: 404 });

    // Bij een bestand ook het bestand zelf opruimen, anders blijft het
    // plaatsnemen in de gratis gigabyte.
    if (weg.soort === 'bestand') await verwijderBestand(weg.bron);

    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error('[lesmedia]', e);
    return NextResponse.json({ fout: 'Verwijderen mislukte.' }, { status: 500 });
  }
}
