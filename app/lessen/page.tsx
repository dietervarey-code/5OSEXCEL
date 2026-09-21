import Link from 'next/link';
import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { ConfiguratieFout } from '@/lib/supabase';
import { lijstLessen, type Les } from '@/lib/lessen';
import { verklaar } from '@/lib/opslag';

export const dynamic = 'force-dynamic';

const FOCUSNAMEN: Record<number, string> = {
  1: 'Rekenblad gebruiken en opmaken',
  2: 'Formules en functies',
  3: 'Afdrukken',
  4: 'Grafieken',
  5: 'Meerdere werkbladen',
  6: 'Koppelen',
  7: 'Draaitabellen',
  8: 'Geavanceerde functies',
  9: 'Databank bevragen',
};

export default async function Lessen() {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');

  const leerkracht = sessie.rol === 'leerkracht';

  let lessen: Les[] = [];
  let fout: string | null = null;
  try {
    lessen = await lijstLessen(leerkracht);
  } catch (e) {
    fout = e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : 'Kon de lessen niet laden.';
  }

  const perFocus = new Map<number, Les[]>();
  for (const les of lessen) {
    if (!perFocus.has(les.focus)) perFocus.set(les.focus, []);
    perFocus.get(les.focus)!.push(les);
  }

  return (
    <main style={{ maxWidth: 820, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Lessen</h1>
          <span className="gedempt">Theorie en voorbeelden om te herlezen</span>
        </div>
        <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center' }}>
          <Link href="/oefenen">Oefenen →</Link>
          {leerkracht && <Link href="/leerkracht/lessen">Lessen beheren</Link>}
          <form action="/api/uitloggen" method="post">
            <button type="submit">Afmelden</button>
          </form>
        </div>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      {!fout && lessen.length === 0 && (
        <div className="kaart">
          <p className="gedempt" style={{ margin: 0 }}>
            Er staan nog geen lessen klaar.
            {leerkracht && <> Voeg er een toe via <Link href="/leerkracht/lessen">Lessen beheren</Link>.</>}
          </p>
        </div>
      )}

      {[...perFocus.entries()].map(([focus, groep]) => (
        <section key={focus} style={{ marginBottom: '1.8rem' }}>
          <h2 style={{ fontSize: '0.82rem', textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--gedempt)' }}>
            Focus {focus} · {FOCUSNAMEN[focus] ?? ''}
          </h2>
          <div style={{ display: 'grid', gap: '0.7rem' }}>
            {groep.map((les) => (
              <Link key={les.id} href={`/lessen/${les.id}`} className="leskaart">
                <strong>{les.titel}</strong>
                {!les.gepubliceerd && <span className="badge waarschuwing" style={{ marginLeft: '0.5rem' }}>concept</span>}
                {les.samenvatting && <div className="gedempt" style={{ marginTop: '0.25rem' }}>{les.samenvatting}</div>}
              </Link>
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}
