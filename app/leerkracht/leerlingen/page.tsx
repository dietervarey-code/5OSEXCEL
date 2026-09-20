import Link from 'next/link';
import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { lijstLeerlingen, type LeerlingOverzicht } from '@/lib/opslag';
import LeerlingenBeheer from '@/components/LeerlingenBeheer';

export const dynamic = 'force-dynamic';

export default async function Leerlingen() {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');
  if (sessie.rol !== 'leerkracht') redirect('/oefenen');

  let leerlingen: LeerlingOverzicht[] = [];
  let fout: string | null = null;
  try {
    leerlingen = await lijstLeerlingen();
  } catch (e) {
    fout = e instanceof Error ? e.message : 'De lijst kon niet geladen worden.';
  }

  return (
    <main style={{ maxWidth: 900, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Leerlingen</h1>
          <span className="gedempt">Accounts aanmaken en wachtwoorden opnieuw instellen</span>
        </div>
        <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
          <Link href="/leerkracht">← Opvolging</Link>
          <form action="/api/uitloggen" method="post">
            <button type="submit">Afmelden</button>
          </form>
        </div>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      <LeerlingenBeheer
        beginLijst={leerlingen}
        standaardKlas={sessie.klas}
        ikZelf={sessie.gebruikersnaam}
      />
    </main>
  );
}
