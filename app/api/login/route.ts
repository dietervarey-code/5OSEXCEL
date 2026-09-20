import { NextResponse } from 'next/server';
import { controleerWachtwoord, maakSessieCookie, COOKIE_NAAM, COOKIE_MAX_LEEFTIJD, type Sessie } from '@/lib/auth';
import { vindLeerling } from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';

export async function POST(request: Request) {
  const { gebruikersnaam, wachtwoord } = (await request.json()) as {
    gebruikersnaam?: string;
    wachtwoord?: string;
  };

  if (!gebruikersnaam || !wachtwoord) {
    return NextResponse.json({ fout: 'Vul je gebruikersnaam en wachtwoord in.' }, { status: 400 });
  }

  let gevonden;
  try {
    gevonden = await vindLeerling(gebruikersnaam);
  } catch (e) {
    console.error('[login]', e);

    // Een vergeten instelling is iets heel anders dan een databank die plat ligt.
    // Door dat te onderscheiden zoekt de leerkracht niet op de verkeerde plaats.
    if (e instanceof ConfiguratieFout) {
      return NextResponse.json(
        { fout: 'Het portaal is nog niet volledig ingesteld. Kijk op /status.' },
        { status: 503 },
      );
    }
    return NextResponse.json(
      { fout: 'De databank is niet bereikbaar. Verwittig je leerkracht.' },
      { status: 503 },
    );
  }

  // Bewust dezelfde boodschap voor "bestaat niet" en "fout wachtwoord",
  // anders kun je uitvissen welke gebruikersnamen bestaan.
  if (!gevonden || !controleerWachtwoord(wachtwoord, gevonden.wachtwoordHash)) {
    return NextResponse.json({ fout: 'Gebruikersnaam of wachtwoord klopt niet.' }, { status: 401 });
  }

  const sessie: Sessie = {
    gebruikersnaam: gevonden.gebruikersnaam,
    naam: gevonden.naam,
    rol: gevonden.rol,
    klas: gevonden.klas,
    verlooptOp: Date.now() + COOKIE_MAX_LEEFTIJD * 1000,
  };

  const antwoord = NextResponse.json({ rol: gevonden.rol, naam: gevonden.naam });
  antwoord.cookies.set(COOKIE_NAAM, maakSessieCookie(sessie), {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    path: '/',
    maxAge: COOKIE_MAX_LEEFTIJD,
  });
  return antwoord;
}
