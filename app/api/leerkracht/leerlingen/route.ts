import { NextResponse } from 'next/server';
import { huidigeSessie } from '@/lib/auth';
import { hashWachtwoord } from '@/lib/auth';
import { maakGebruikersnaam, maakWachtwoord } from '@/lib/accounts.mjs';
import {
  bezetteGebruikersnamen,
  voegLeerlingenToe,
  zetWachtwoord,
  verwijderLeerling,
  verklaar,
  type Rol,
} from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';

/** Alleen een aangemelde leerkracht mag hier iets doen. */
async function leerkrachtOfNiets() {
  const sessie = await huidigeSessie();
  if (!sessie) return { fout: NextResponse.json({ fout: 'Niet aangemeld.' }, { status: 401 }) };
  if (sessie.rol !== 'leerkracht') {
    return { fout: NextResponse.json({ fout: 'Geen toegang.' }, { status: 403 }) };
  }
  return { sessie };
}

/** Nieuwe accounts aanmaken uit een lijst namen. */
export async function POST(request: Request) {
  const { sessie, fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { namen, klas, rol } = (await request.json()) as {
    namen?: string;
    klas?: string;
    rol?: Rol;
  };

  const lijst = String(namen ?? '')
    .split('\n')
    .map((n) => n.trim())
    .filter(Boolean);

  if (lijst.length === 0) {
    return NextResponse.json({ fout: 'Geef minstens één naam op.' }, { status: 400 });
  }
  if (lijst.length > 200) {
    return NextResponse.json({ fout: 'Maximaal 200 namen per keer.' }, { status: 400 });
  }

  const doelKlas = String(klas ?? sessie!.klas).trim() || sessie!.klas;
  const doelRol: Rol = rol === 'leerkracht' ? 'leerkracht' : 'leerling';

  try {
    const bezet = await bezetteGebruikersnamen();
    const rijen = [];
    const uitDelen = [];
    const geweigerd: string[] = [];

    for (const naam of lijst) {
      const gebruikersnaam = maakGebruikersnaam(naam, bezet);
      if (!gebruikersnaam) {
        geweigerd.push(naam);
        continue;
      }
      bezet.add(gebruikersnaam);

      const wachtwoord = maakWachtwoord();
      rijen.push({
        gebruikersnaam,
        naam,
        klas: doelKlas,
        rol: doelRol,
        wachtwoordHash: hashWachtwoord(wachtwoord),
      });
      uitDelen.push({ naam, gebruikersnaam, wachtwoord });
    }

    await voegLeerlingenToe(rijen);

    // De wachtwoorden gaan hier één keer naar het scherm en worden nergens
    // bewaard. Wie ze mist, moet een nieuw wachtwoord laten instellen.
    return NextResponse.json({ aangemaakt: uitDelen, geweigerd });
  } catch (e) {
    console.error('[leerlingen POST]', e);
    return NextResponse.json(
      // Een verkeerd ingestelde SUPABASE_URL is geen 'aanmaken mislukte':
      // geef de leerkracht de uitleg mee in plaats van de rauwe fout.
      {
        fout:
          e instanceof ConfiguratieFout
            ? e.message
            : e instanceof Error
              ? verklaar(e.message)
              : 'Aanmaken mislukte.',
      },
      { status: 500 },
    );
  }
}

/** Nieuw wachtwoord voor één leerling. */
export async function PATCH(request: Request) {
  const { fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { gebruikersnaam } = (await request.json()) as { gebruikersnaam?: string };
  if (!gebruikersnaam) {
    return NextResponse.json({ fout: 'Geen gebruikersnaam opgegeven.' }, { status: 400 });
  }

  try {
    const wachtwoord = maakWachtwoord();
    const gelukt = await zetWachtwoord(gebruikersnaam, hashWachtwoord(wachtwoord));
    if (!gelukt) return NextResponse.json({ fout: 'Onbekende leerling.' }, { status: 404 });

    return NextResponse.json({ gebruikersnaam, wachtwoord });
  } catch (e) {
    console.error('[leerlingen PATCH]', e);
    return NextResponse.json({ fout: 'Wachtwoord wijzigen mislukte.' }, { status: 500 });
  }
}

/** Account en alle bijbehorende gegevens verwijderen. */
export async function DELETE(request: Request) {
  const { sessie, fout } = await leerkrachtOfNiets();
  if (fout) return fout;

  const { gebruikersnaam } = (await request.json()) as { gebruikersnaam?: string };
  if (!gebruikersnaam) {
    return NextResponse.json({ fout: 'Geen gebruikersnaam opgegeven.' }, { status: 400 });
  }

  // Jezelf verwijderen zou je buitensluiten uit je eigen portaal.
  if (gebruikersnaam === sessie!.gebruikersnaam) {
    return NextResponse.json({ fout: 'Je kunt je eigen account niet verwijderen.' }, { status: 400 });
  }

  try {
    const gelukt = await verwijderLeerling(gebruikersnaam);
    if (!gelukt) return NextResponse.json({ fout: 'Onbekende leerling.' }, { status: 404 });
    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error('[leerlingen DELETE]', e);
    return NextResponse.json({ fout: 'Verwijderen mislukte.' }, { status: 500 });
  }
}
