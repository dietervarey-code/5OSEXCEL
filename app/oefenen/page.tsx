import Link from 'next/link';
import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { oefeningenOpVolgorde } from '@/data/oefeningen';
import { scoresVan, verklaar } from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

function bolletjes(niveau: number) {
  return '●'.repeat(niveau) + '○'.repeat(5 - niveau);
}

export default async function Oefeningen() {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');

  const oefeningen = oefeningenOpVolgorde();

  let scores: Record<string, { besteScore: number; maxScore: number; pogingen: number }> = {};
  let fout: string | null = null;
  try {
    scores = await scoresVan(sessie.gebruikersnaam);
  } catch (e) {
    fout = e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : null;
  }

  const af = oefeningen.filter((o) => (scores[o.id]?.besteScore ?? 0) >= o.maxScore).length;

  return (
    <main style={{ maxWidth: 860, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Oefeningen</h1>
          <span className="gedempt">{af} van de {oefeningen.length} volledig opgelost</span>
        </div>
        <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center' }}>
          <Link href="/lessen">Lessen</Link>
          {sessie.rol === 'leerkracht' && <Link href="/leerkracht">Opvolging</Link>}
          <span className="gedempt">{sessie.naam}</span>
          <form action="/api/uitloggen" method="post">
            <button type="submit">Afmelden</button>
          </form>
        </div>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      <div style={{ display: 'grid', gap: '0.7rem' }}>
        {oefeningen.map((o, i) => {
          const score = scores[o.id];
          const volledig = (score?.besteScore ?? 0) >= o.maxScore;
          return (
            <Link key={o.id} href={`/oefenen/${o.id}`} className="leskaart">
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', alignItems: 'start' }}>
                <div style={{ minWidth: 0 }}>
                  <div className="gedempt" style={{ fontSize: '0.78rem' }}>
                    Oefening {i + 1} · {o.focus}
                  </div>
                  <strong>{o.titel}</strong>
                  <div className="gedempt" style={{ marginTop: '0.2rem' }}>{o.leerdoel}</div>
                </div>
                <div style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                  <div
                    className="gedempt"
                    style={{ fontSize: '0.8rem', letterSpacing: '0.1em' }}
                    title={`Moeilijkheidsgraad ${o.niveau} op 5`}
                  >
                    {bolletjes(o.niveau)}
                  </div>
                  {score ? (
                    <span className={`badge ${volledig ? 'goed' : 'waarschuwing'}`} style={{ marginTop: '0.3rem' }}>
                      {score.besteScore}/{score.maxScore}
                    </span>
                  ) : (
                    <span className="gedempt" style={{ fontSize: '0.8rem' }}>nog niet gemaakt</span>
                  )}
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </main>
  );
}
