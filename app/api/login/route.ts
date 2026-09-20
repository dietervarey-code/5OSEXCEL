import { NextResponse } from 'next/server';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { controleerWachtwoord, maakSessieCookie, COOKIE_NAAM, COOKIE_MAX_LEEFTIJD, type Sessie } from '@/lib/auth';

type Leerling = {
  gebruikersnaam: string;
  naam: string;
  klas: string;
  rol: 'leerling' | 'leerkracht';
  wachtwoordHash: string;
};

async function leerlingen(): Promise<Leerling[]> {
  const pad = path.join(process.cwd(), 'data', 'leerlingen.json');
  return JSON.parse(await fs.readFile(pad, 'utf8')) as Leerling[];
}

export async function POST(request: Request) {
  const { gebruikersnaam, wachtwoord } = (await request.json()) as {
    gebruikersnaam?: string;
    wachtwoord?: string;
  };

  if (!gebruikersnaam || !wachtwoord) {
    return NextResponse.json({ fout: 'Vul je gebruikersnaam en wachtwoord in.' }, { status: 400 });
  }

  const lijst = await leerlingen();
  const gevonden = lijst.find((l) => l.gebruikersnaam.toLowerCase() === gebruikersnaam.toLowerCase().trim());

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
