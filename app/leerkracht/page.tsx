import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { allePogingen, alleGebeurtenissen } from '@/lib/opslag';

export const dynamic = 'force-dynamic';

function duur(ms: number): string {
  if (!ms) return '—';
  const m = Math.floor(ms / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

export default async function Leerkracht() {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');
  if (sessie.rol !== 'leerkracht') redirect('/oefenen');

  const [pogingen, gebeurtenissen] = await Promise.all([allePogingen(), alleGebeurtenissen()]);

  // Per leerling samenvatten: beste score, aantal pogingen, weggeklikt, tijd weg.
  const perLeerling = new Map<string, {
    naam: string;
    klas: string;
    pogingen: number;
    besteScore: number | null;
    maxScore: number | null;
    laatsteOp: number | null;
    keerWeg: number;
    wegMs: number;
  }>();

  for (const p of pogingen) {
    const rij = perLeerling.get(p.gebruikersnaam) ?? {
      naam: p.naam, klas: p.klas, pogingen: 0, besteScore: null, maxScore: null,
      laatsteOp: null, keerWeg: 0, wegMs: 0,
    };
    rij.pogingen += 1;
    if (p.score !== null) rij.besteScore = Math.max(rij.besteScore ?? 0, p.score);
    rij.maxScore = p.maxScore;
    rij.laatsteOp = Math.max(rij.laatsteOp ?? 0, p.ingediendOp ?? p.gestartOp);
    perLeerling.set(p.gebruikersnaam, rij);
  }

  for (const g of gebeurtenissen) {
    const rij = perLeerling.get(g.gebruikersnaam);
    if (!rij) continue;
    if (g.soort === 'verborgen') rij.keerWeg += 1;
    if (g.soort === 'zichtbaar' && g.duurMs) rij.wegMs += g.duurMs;
  }

  const rijen = [...perLeerling.entries()].sort((a, b) => a[1].naam.localeCompare(b[1].naam));

  return (
    <main style={{ maxWidth: 1100, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Opvolging 5OS Excel</h1>
          <span className="gedempt">Oefening: Factuur vervolledigen</span>
        </div>
        <form action="/api/uitloggen" method="post">
          <button type="submit">Afmelden</button>
        </form>
      </header>

      <div className="kaart">
        {rijen.length === 0 ? (
          <p className="gedempt" style={{ margin: 0 }}>
            Nog geen resultaten. Zodra een leerling op Nakijken klikt, verschijnt die hier.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Leerling</th>
                <th>Klas</th>
                <th>Beste score</th>
                <th>Pogingen</th>
                <th>Weggeklikt</th>
                <th>Tijd weg</th>
                <th>Laatst actief</th>
              </tr>
            </thead>
            <tbody>
              {rijen.map(([gebruikersnaam, r]) => {
                const verhouding = r.besteScore !== null && r.maxScore ? r.besteScore / r.maxScore : 0;
                const kleur = verhouding >= 0.8 ? 'goed' : verhouding >= 0.5 ? 'waarschuwing' : 'fout';
                return (
                  <tr key={gebruikersnaam}>
                    <td><strong>{r.naam}</strong></td>
                    <td>{r.klas}</td>
                    <td>
                      {r.besteScore === null ? '—' : (
                        <span className={`badge ${kleur}`}>{r.besteScore}/{r.maxScore}</span>
                      )}
                    </td>
                    <td>{r.pogingen}</td>
                    <td>{r.keerWeg === 0 ? '—' : `${r.keerWeg}×`}</td>
                    <td>{duur(r.wegMs)}</td>
                    <td className="gedempt">
                      {r.laatsteOp ? new Date(r.laatsteOp).toLocaleTimeString('nl-BE', { hour: '2-digit', minute: '2-digit' }) : '—'}
                    </td>
                  </tr>
                );
              })}
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
