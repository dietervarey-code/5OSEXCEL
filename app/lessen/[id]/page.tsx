import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { vindLes } from '@/lib/lessen';
import { tijdelijkeLink } from '@/lib/bestanden';
import Lesinhoud from '@/components/Lesinhoud';

export const dynamic = 'force-dynamic';

export default async function LesPagina({ params }: { params: Promise<{ id: string }> }) {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');

  const { id } = await params;
  const leerkracht = sessie.rol === 'leerkracht';

  const les = await vindLes(id, leerkracht);
  if (!les) notFound();

  const videos = les.media.filter((m) => m.soort === 'video');
  const bestanden = les.media.filter((m) => m.soort === 'bestand');

  // Links naar bestanden vervallen na een uur; we maken ze hier vers aan.
  const downloads = await Promise.all(
    bestanden.map(async (b) => ({ ...b, link: await tijdelijkeLink(b.bron) })),
  );

  return (
    <main style={{ maxWidth: 780, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <span className="gedempt">Focus {les.focus}</span>
          <h1 style={{ marginBottom: 0 }}>{les.titel}</h1>
        </div>
        <Link href="/lessen">← Alle lessen</Link>
      </header>

      {!les.gepubliceerd && (
        <div className="melding waarschuwing" style={{ marginBottom: '1rem' }}>
          Dit is een concept. Leerlingen zien deze les nog niet.
        </div>
      )}

      {les.samenvatting && (
        <div className="kaart" style={{ marginBottom: '1.2rem', background: '#f4f7fc' }}>
          <strong>In het kort</strong>
          <p style={{ margin: '0.35rem 0 0' }}>{les.samenvatting}</p>
        </div>
      )}

      {videos.length > 0 && (
        <section style={{ marginBottom: '1.5rem', display: 'grid', gap: '1rem' }}>
          {videos.map((v) => (
            <div key={v.id}>
              <h2 style={{ fontSize: '0.95rem' }}>{v.titel}</h2>
              <div className="videokader">
                <iframe
                  src={v.bron}
                  title={v.titel}
                  allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  referrerPolicy="strict-origin-when-cross-origin"
                  allowFullScreen
                />
              </div>
            </div>
          ))}
        </section>
      )}

      <article className="kaart">
        <Lesinhoud markdown={les.inhoud} />
      </article>

      {downloads.length > 0 && (
        <section className="kaart" style={{ marginTop: '1.2rem' }}>
          <h2>Bestanden</h2>
          <ul style={{ paddingLeft: '1.1rem', margin: 0 }}>
            {downloads.map((b) => (
              <li key={b.id} style={{ margin: '0.35rem 0' }}>
                {b.link ? (
                  <a href={b.link} target="_blank" rel="noopener noreferrer">{b.titel}</a>
                ) : (
                  <span className="gedempt">{b.titel} — link kon niet gemaakt worden</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {les.oefeningId && (
        <div style={{ marginTop: '1.5rem' }}>
          <Link href="/oefenen">
            <button className="primair">Naar de oefening →</button>
          </Link>
        </div>
      )}
    </main>
  );
}
