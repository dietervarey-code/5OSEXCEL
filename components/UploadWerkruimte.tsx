'use client';

import { useState } from 'react';
import Link from 'next/link';
import type { UploadOpgave } from '@/lib/werkblad-types';
import { useTelemetrie } from '@/lib/telemetrie';

type Resultaat = {
  score: number;
  maxScore: number;
  pogingNummer: number | null;
  waarschuwing?: string;
  resultaten: { checkId: string; omschrijving: string; punten: number; behaald: boolean; feedback: string }[];
};

export default function UploadWerkruimte({
  opgave,
  naam,
  sessieId,
  opslagFout,
  les,
}: {
  opgave: UploadOpgave;
  naam: string;
  sessieId: string | null;
  opslagFout: string | null;
  les: { id: string; titel: string } | null;
}) {
  const [bezig, setBezig] = useState(false);
  const [fout, setFout] = useState<string | null>(null);
  const [resultaat, setResultaat] = useState<Resultaat | null>(null);
  const [bestandsnaam, setBestandsnaam] = useState<string | null>(null);

  // De meting loopt ook hier; ze wordt niet aan de leerling getoond.
  useTelemetrie(sessieId, true);

  async function dien(bestand: File) {
    setBezig(true);
    setFout(null);
    setBestandsnaam(bestand.name);

    const form = new FormData();
    form.append('oefeningId', opgave.id);
    if (sessieId) form.append('sessieId', sessieId);
    form.append('bestand', bestand);

    try {
      const antwoord = await fetch('/api/indienen', { method: 'POST', body: form });
      const data = await antwoord.json();
      if (!antwoord.ok) {
        setFout(data.fout ?? 'Nakijken lukte niet.');
        return;
      }
      setResultaat(data);
    } catch {
      setFout('De server antwoordde niet. Probeer opnieuw.');
    } finally {
      setBezig(false);
    }
  }

  return (
    <main style={{ maxWidth: 780, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <strong>{opgave.titel}</strong>
          <div className="gedempt">{opgave.focus}</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Link href="/oefenen" className="gedempt">Alle oefeningen</Link>
          <Link href="/lessen" className="gedempt">Lessen</Link>
          <span className="gedempt">{naam}</span>
          <form action="/api/uitloggen" method="post">
            <button type="submit">Afmelden</button>
          </form>
        </div>
      </header>

      <div className="melding waarschuwing" style={{ marginBottom: '1.2rem' }}>
        Deze oefening maak je in <strong>Excel zelf</strong>. Grafieken, draaitabellen en
        afdrukinstellingen bestaan niet in het rekenblad hier in de browser — en op stage
        werk je ook met het echte programma.
      </div>

      <section className="kaart" style={{ marginBottom: '1.2rem' }}>
        <h2>Opdracht</h2>
        <p style={{ marginTop: 0 }}>{opgave.stagecontext}</p>
        <ol style={{ paddingLeft: '1.1rem', display: 'grid', gap: '0.45rem' }}>
          {opgave.opdrachten.map((o) => <li key={o}>{o}</li>)}
        </ol>
        {les && (
          <a href={`/lessen/${les.id}`} target="_blank" rel="noopener noreferrer"
             style={{ display: 'inline-block', marginTop: '0.6rem', fontSize: '0.88rem' }}>
            Theorie herlezen: {les.titel}
          </a>
        )}
      </section>

      <section className="kaart" style={{ marginBottom: '1.2rem' }}>
        <h2>1 · Haal het startbestand op</h2>
        <p className="gedempt" style={{ marginTop: 0 }}>
          Open het in Excel, voer de opdracht uit en sla het op als <code>.xlsx</code>.
        </p>
        <a href={`/api/startbestand?oefening=${opgave.id}`} download>
          <button className="primair">Startbestand downloaden</button>
        </a>
      </section>

      <section className="kaart">
        <h2>2 · Laad je bestand op</h2>
        {opslagFout && <div className="melding waarschuwing" style={{ marginBottom: '0.8rem' }}>{opslagFout}</div>}

        <input
          type="file"
          accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          disabled={bezig}
          onChange={(e) => { const b = e.target.files?.[0]; if (b) void dien(b); e.target.value = ''; }}
        />
        {bestandsnaam && <div className="gedempt" style={{ marginTop: '0.4rem' }}>Laatst ingediend: {bestandsnaam}</div>}
        {bezig && <div className="gedempt" style={{ marginTop: '0.5rem' }}>Bezig met nakijken…</div>}
        {fout && <div className="melding fout" style={{ marginTop: '0.8rem' }}>{fout}</div>}

        {resultaat && (
          <div style={{ marginTop: '1.2rem' }}>
            <h3>
              {resultaat.pogingNummer ? `Poging ${resultaat.pogingNummer} — ` : ''}
              {resultaat.score} / {resultaat.maxScore}
            </h3>
            {resultaat.waarschuwing && <div className="melding waarschuwing">{resultaat.waarschuwing}</div>}
            <div style={{ display: 'grid', gap: '0.5rem', marginTop: '0.6rem' }}>
              {resultaat.resultaten.map((r) => (
                <div key={r.checkId} className={`melding ${r.behaald ? 'goed' : 'fout'}`}>
                  <strong>{r.behaald ? '✓' : '✗'} {r.omschrijving}</strong>
                  <span className="badge" style={{ marginLeft: '0.4rem' }}>{r.behaald ? r.punten : 0}/{r.punten}</span>
                  {!r.behaald && <div style={{ marginTop: '0.3rem' }}>{r.feedback}</div>}
                </div>
              ))}
            </div>
            <p className="gedempt" style={{ marginTop: '0.8rem', fontSize: '0.82rem' }}>
              Je mag opnieuw indienen zo vaak je wil. Je leerkracht ziet je beste score.
            </p>
          </div>
        )}
      </section>

      <p className="gedempt" style={{ marginTop: '1.5rem', fontSize: '0.78rem' }}>
        Je leerkracht volgt je werk aan deze oefening op.
      </p>
    </main>
  );
}
