import Link from 'next/link';
import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { ConfiguratieFout } from '@/lib/supabase';
import { overzicht, verklaar, type OverzichtRij } from '@/lib/opslag';

export const dynamic = 'force-dynamic';

function duur(ms: number): string {
  if (!ms || ms < 1000) return '—';
  const m = Math.floor(ms / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

function scoreKleur(rij: OverzichtRij): string {
  if (rij.besteScore === null || !rij.maxScore) return '';
  const verhouding = rij.besteScore / rij.maxScore;
  return verhouding >= 0.8 ? 'goed' : verhouding >= 0.5 ? 'waarschuwing' : 'fout';
}

export default async function Leerkracht() {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) redirect('/');
  if (aangemeld.rol !== 'leerkracht') redirect('/oefenen');

  let rijen: OverzichtRij[] = [];
  let fout: string | null = null;
  try {
    rijen = await overzicht(aangemeld.klas);
  } catch (e) {
    console.error('[leerkracht]', e);
    fout = e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : 'Het overzicht kon niet geladen worden.';
  }

  const metWerk = rijen.filter((r) => r.pogingen > 0);

  return (
    <main style={{ maxWidth: 1100, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Opvolging {aangemeld.klas} Excel</h1>
          <span className="gedempt">
            Oefening: Factuur vervolledigen · {metWerk.length} van {rijen.length} leerlingen begonnen
          </span>
        </div>
        <div style={{ display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
          <Link href="/leerkracht/leerlingen">Leerlingen beheren →</Link>
          <form action="/api/uitloggen" method="post">
            <button type="submit">Afmelden</button>
          </form>
        </div>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      <div className="kaart">
        {rijen.length === 0 && !fout ? (
          <p className="gedempt" style={{ margin: 0 }}>
            Nog geen leerlingen in deze klas. Maak ze aan met{' '}
            <code>node scripts/maak-leerlingen.mjs klas.csv</code>.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Leerling</th>
                <th>Beste score</th>
                <th>Pogingen</th>
                <th>Werktijd</th>
                <th>Weggeklikt</th>
                <th>Tijd weg</th>
                <th>Laatst actief</th>
              </tr>
            </thead>
            <tbody>
              {rijen.map((r) => (
                <tr key={r.gebruikersnaam}>
                  <td>
                    <strong>{r.naam}</strong>
                    {r.pogingen === 0 && <span className="gedempt"> · nog niet begonnen</span>}
                    {/* De gebruikersnaam erbij, anders zijn twee gelijknamige
                        leerlingen in deze tabel niet uit elkaar te houden. */}
                    <div className="gedempt" style={{ fontSize: '0.78rem' }}>{r.gebruikersnaam}</div>
                  </td>
                  <td>
                    {r.besteScore === null ? '—' : (
                      <span className={`badge ${scoreKleur(r)}`}>{r.besteScore}/{r.maxScore}</span>
                    )}
                  </td>
                  <td>{r.pogingen || '—'}</td>
                  <td>{duur(r.werktijdMs)}</td>
                  <td>{r.keerWeg === 0 ? '—' : `${r.keerWeg}×`}</td>
                  <td>{duur(r.wegMs)}</td>
                  <td className="gedempt">
                    {r.laatsteOp
                      ? new Date(r.laatsteOp).toLocaleTimeString('nl-BE', { hour: '2-digit', minute: '2-digit' })
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <p className="gedempt" style={{ marginTop: '1rem', fontSize: '0.8rem' }}>
        &ldquo;Weggeklikt&rdquo; telt hoe vaak het oefenvenster uit beeld ging en hoe lang.
        Dat zegt niets over wat er ondertussen op het scherm stond, en een tweede scherm of
        gsm valt er sowieso buiten. Gebruik het als gespreksaanleiding, niet als bewijs.
      </p>
    </main>
  );
}
