import { NextResponse } from 'next/server';
import { timingSafeEqual } from 'node:crypto';
import { hashWachtwoord } from '@/lib/auth';
import { maakGebruikersnaam } from '@/lib/accounts.mjs';
import { bezetteGebruikersnamen, telLeerkrachten, voegLeerlingenToe } from '@/lib/opslag';

/**
 * Eerste leerkrachtaccount aanmaken.
 *
 * Twee sloten, allebei nodig:
 *  1. SETUP_SLEUTEL moet als omgevingsvariabele ingesteld zijn en kloppen.
 *  2. Er mag nog geen enkele leerkracht bestaan.
 *
 * Na gebruik haal je SETUP_SLEUTEL weg in Vercel; dan is deze route dood.
 */

function sleutelKlopt(gegeven: string): boolean {
  const verwacht = process.env.SETUP_SLEUTEL;
  if (!verwacht || verwacht.length < 8) return false;

  const a = Buffer.from(gegeven);
  const b = Buffer.from(verwacht);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

export async function POST(request: Request) {
  const { sleutel, naam, klas, wachtwoord } = (await request.json()) as {
    sleutel?: string;
    naam?: string;
    klas?: string;
    wachtwoord?: string;
  };

  if (!process.env.SETUP_SLEUTEL) {
    return NextResponse.json(
      { fout: 'Setup staat uit. Zet SETUP_SLEUTEL in Vercel en deploy opnieuw.' },
      { status: 403 },
    );
  }

  if (!sleutelKlopt(String(sleutel ?? ''))) {
    return NextResponse.json({ fout: 'De setupsleutel klopt niet.' }, { status: 401 });
  }

  if (!naam?.trim()) return NextResponse.json({ fout: 'Vul je naam in.' }, { status: 400 });
  if (!wachtwoord || wachtwoord.length < 8) {
    return NextResponse.json({ fout: 'Kies een wachtwoord van minstens 8 tekens.' }, { status: 400 });
  }

  try {
    if ((await telLeerkrachten()) > 0) {
      return NextResponse.json(
        { fout: 'Er bestaat al een leerkrachtaccount. Gebruik dat om aan te melden.' },
        { status: 409 },
      );
    }

    const gebruikersnaam = maakGebruikersnaam(naam, await bezetteGebruikersnamen());
    if (!gebruikersnaam) {
      return NextResponse.json({ fout: 'Uit die naam valt geen gebruikersnaam te maken.' }, { status: 400 });
    }

    await voegLeerlingenToe([
      {
        gebruikersnaam,
        naam: naam.trim(),
        klas: (klas ?? '5OS').trim() || '5OS',
        rol: 'leerkracht',
        wachtwoordHash: hashWachtwoord(wachtwoord),
      },
    ]);

    return NextResponse.json({ gebruikersnaam });
  } catch (e) {
    console.error('[setup]', e);
    return NextResponse.json(
      { fout: e instanceof Error ? e.message : 'Aanmaken mislukte.' },
      { status: 500 },
    );
  }
}
