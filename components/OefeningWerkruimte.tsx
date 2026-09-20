'use client';

import { useCallback, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import type { Opgave, CelInzending } from '@/lib/werkblad-types';
import { useTelemetrie } from '@/lib/telemetrie';

// Univer rendert op een canvas en kan niet server-side gerenderd worden.
const Werkblad = dynamic(() => import('@/components/Werkblad'), {
  ssr: false,
  loading: () => <div style={{ display: 'grid', placeItems: 'center', height: '100%' }} className="gedempt">Rekenblad laden…</div>,
});

type Resultaat = {
  score: number;
  maxScore: number;
  pogingNummer: number | null;
  waarschuwing?: string;
  resultaten: { checkId: string; omschrijving: string; punten: number; behaald: boolean; feedback: string }[];
};

function duur(ms: number): string {
  const minuten = Math.floor(ms / 60000);
  const seconden = Math.floor((ms % 60000) / 1000);
  return minuten > 0 ? `${minuten} min ${seconden}s` : `${seconden}s`;
}

export default function OefeningWerkruimte({
  opgave,
  naam,
  sessieId,
  opslagFout,
}: {
  opgave: Opgave;
  naam: string;
  sessieId: string | null;
  opslagFout: string | null;
}) {
  const lezer = useRef<(() => CelInzending[]) | null>(null);
  const [resultaat, setResultaat] = useState<Resultaat | null>(null);
  const [bezig, setBezig] = useState(false);
  const [fout, setFout] = useState<string | null>(null);

  const meting = useTelemetrie(sessieId, true);

  const opGereed = useCallback((lees: () => CelInzending[]) => {
    lezer.current = lees;
  }, []);

  async function kijkNa() {
    if (!lezer.current) return;
    setBezig(true);
    setFout(null);
    try {
      const antwoord = await fetch('/api/nakijken', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ oefeningId: opgave.id, sessieId, inzending: lezer.current() }),
      });
      if (!antwoord.ok) throw new Error('Nakijken lukte niet. Ben je nog aangemeld?');
      setResultaat(await antwoord.json());
    } catch (e) {
      setFout(e instanceof Error ? e.message : 'Er ging iets mis.');
    } finally {
      setBezig(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <header className="balk">
        <div>
          <strong>{opgave.titel}</strong>
          <div className="gedempt">{opgave.focus}</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {/* Bewust zichtbaar: leerlingen horen te weten dat dit meegeteld wordt. */}
          <span className="gedempt" title="Je leerkracht ziet hoe lang dit scherm openstond.">
            {duur(meting.actiefMs)} bezig · {meting.keerWeg}× weggeklikt
          </span>
          <span className="gedempt">{naam}</span>
          <form action="/api/uitloggen" method="post">
            <button type="submit" formAction="/api/uitloggen">Afmelden</button>
          </form>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 360px) 1fr', flex: 1, minHeight: 0 }}>
        <aside style={{ borderRight: '1px solid var(--rand)', overflowY: 'auto', padding: '1.1rem', background: '#fff' }}>
          <h2>Opdracht</h2>
          <p style={{ marginTop: 0 }}>{opgave.stagecontext}</p>

          <ol style={{ paddingLeft: '1.1rem', display: 'grid', gap: '0.5rem' }}>
            {opgave.opdrachten.map((o) => <li key={o}>{o}</li>)}
          </ol>

          <button className="primair" onClick={kijkNa} disabled={bezig} style={{ width: '100%', marginTop: '0.5rem' }}>
            {bezig ? 'Nakijken…' : 'Nakijken'}
          </button>

          {opslagFout && <div className="melding waarschuwing" style={{ marginTop: '0.8rem' }}>{opslagFout}</div>}
          {fout && <div className="melding fout" style={{ marginTop: '0.8rem' }}>{fout}</div>}

          {resultaat && (
            <section style={{ marginTop: '1.2rem' }}>
              <h3>
                {resultaat.pogingNummer ? `Poging ${resultaat.pogingNummer} — ` : ''}
                {resultaat.score} / {resultaat.maxScore}
              </h3>
              {resultaat.waarschuwing && (
                <div className="melding waarschuwing">{resultaat.waarschuwing}</div>
              )}
              <div style={{ display: 'grid', gap: '0.5rem', marginTop: '0.6rem' }}>
                {resultaat.resultaten.map((r) => (
                  <div key={r.checkId} className={`melding ${r.behaald ? 'goed' : 'fout'}`}>
                    <strong>{r.behaald ? '✓' : '✗'} {r.omschrijving}</strong>
                    <span className="badge" style={{ marginLeft: '0.4rem' }}>{r.behaald ? r.punten : 0}/{r.punten}</span>
                    {!r.behaald && <div style={{ marginTop: '0.3rem' }}>{r.feedback}</div>}
                  </div>
                ))}
              </div>
            </section>
          )}

          <p className="gedempt" style={{ marginTop: '1.5rem', fontSize: '0.78rem' }}>
            Tijdens deze oefening registreren we hoe lang je aan de oefening werkt, hoe vaak je
            het scherm wegklikt en hoeveel pogingen je doet. Je leerkracht ziet dat. We kijken
            niet mee in andere vensters of programma&apos;s.
          </p>
        </aside>

        <div style={{ minWidth: 0, minHeight: 0 }}>
          <Werkblad werkmap={opgave.werkmap} opGereed={opGereed} />
        </div>
      </div>
    </div>
  );
}
