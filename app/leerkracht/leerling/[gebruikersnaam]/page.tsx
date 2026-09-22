import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { ConfiguratieFout } from '@/lib/supabase';
import { leerlingGegevens, pogingenVan, verklaar, type PogingRij } from '@/lib/opslag';
import { vindOpgave } from '@/data/oefeningen';
import { isUpload } from '@/lib/werkblad-types';

export const dynamic = 'force-dynamic';

function kleur(p: PogingRij): string {
  if (!p.maxScore) return '';
  const verhouding = p.score / p.maxScore;
  return verhouding >= 0.8 ? 'goed' : verhouding >= 0.5 ? 'waarschuwing' : 'fout';
}

function tijdstip(iso: string): string {
  return new Date(iso).toLocaleString('nl-BE', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  });
}

export default async function LeerlingDetail({
  params,
}: {
  params: Promise<{ gebruikersnaam: string }>;
}) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) redirect('/');
  if (aangemeld.rol !== 'leerkracht') redirect('/oefenen');

  const { gebruikersnaam } = await params;
  const naamUitUrl = decodeURIComponent(gebruikersnaam);

  let leerling: Awaited<ReturnType<typeof leerlingGegevens>> = null;
  let pogingen: PogingRij[] = [];
  let fout: string | null = null;
  try {
    [leerling, pogingen] = await Promise.all([
      leerlingGegevens(naamUitUrl),
      pogingenVan(naamUitUrl),
    ]);
  } catch (e) {
    console.error('[leerkracht/leerling]', e);
    fout =
      e instanceof ConfiguratieFout ? e.message
      : e instanceof Error ? verklaar(e.message)
      : 'De pogingen konden niet geladen worden.';
  }

  if (!leerling && !fout) notFound();

  // Gegroepeerd per oefening, zodat de tabel niet één lange lijst wordt, en in
  // de volgorde van de leerlijn — niet in die van de laatste inzending.
  const perOefening = new Map<string, PogingRij[]>();
  for (const p of pogingen) {
    const lijst = perOefening.get(p.oefeningId) ?? [];
    lijst.push(p);
    perOefening.set(p.oefeningId, lijst);
  }

  const groepen = [...perOefening.entries()].sort(([a], [b]) => {
    const oa = vindOpgave(a);
    const ob = vindOpgave(b);
    // Oefeningen die niet meer in de catalogus staan, achteraan.
    if (!oa || !ob) return oa ? -1 : ob ? 1 : a.localeCompare(b);
    return oa.focusNummer - ob.focusNummer || oa.volgnummer - ob.volgnummer;
  });

  return (
    <main style={{ maxWidth: 1000, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>{leerling?.naam ?? naamUitUrl}</h1>
          <span className="gedempt">
            {naamUitUrl}
            {leerling?.klas ? ` · ${leerling.klas}` : ''} · {pogingen.length}{' '}
            {pogingen.length === 1 ? 'poging' : 'pogingen'}
          </span>
        </div>
        <Link href="/leerkracht">Terug naar het overzicht</Link>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      {!fout && pogingen.length === 0 && (
        <div className="kaart">
          <p className="gedempt" style={{ margin: 0 }}>
            Deze leerling heeft nog niets ingediend.
          </p>
        </div>
      )}

      {groepen.map(([oefeningId, lijst]) => {
        const opgave = vindOpgave(oefeningId);
        const beste = lijst.reduce((a, b) => (b.score > a.score ? b : a));
        return (
          <section className="kaart" key={oefeningId} style={{ marginBottom: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '1rem' }}>
              <div>
                <h2 style={{ margin: 0, fontSize: '1.05rem' }}>{opgave?.titel ?? oefeningId}</h2>
                <span className="gedempt" style={{ fontSize: '0.8rem' }}>
                  {opgave?.focus ?? oefeningId}
                  {opgave && isUpload(opgave) ? ' · in Excel gemaakt' : ''}
                </span>
              </div>
              <span className={`badge ${kleur(beste)}`}>
                beste {beste.score}/{beste.maxScore}
              </span>
            </div>

            <table style={{ marginTop: '0.8rem' }}>
              <thead>
                <tr>
                  <th>Poging</th>
                  <th>Score</th>
                  <th>Ingediend</th>
                  <th>Wat er misging</th>
                  <th>Werk</th>
                </tr>
              </thead>
              <tbody>
                {lijst
                  .slice()
                  .sort((a, b) => b.nummer - a.nummer)
                  .map((p) => {
                    const mis = p.resultaten.filter((r) => !r.behaald);
                    return (
                      <tr key={p.nummer}>
                        <td>{p.nummer}</td>
                        <td>
                          <span className={`badge ${kleur(p)}`}>{p.score}/{p.maxScore}</span>
                        </td>
                        <td className="gedempt">{tijdstip(p.ingediendOp)}</td>
                        <td className="gedempt" style={{ fontSize: '0.82rem' }}>
                          {mis.length === 0
                            ? 'Alles correct.'
                            : mis.map((r) => r.omschrijving).join(' · ')}
                        </td>
                        <td>
                          {p.bestandPad ? (
                            <a
                              href={`/api/leerkracht/inzending?leerling=${encodeURIComponent(naamUitUrl)}&pad=${encodeURIComponent(p.bestandPad)}`}
                            >
                              Bestand openen
                            </a>
                          ) : (
                            <span className="gedempt">in het portaal</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </section>
        );
      })}
    </main>
  );
}
