import { geheimIsIngesteld, GEHEIM_MINIMUM } from '@/lib/auth';
import { supabaseIsIngesteld } from '@/lib/supabase';
import { controleerDatabank, type Controle } from '@/lib/opslag';

export const dynamic = 'force-dynamic';

/**
 * Controlepagina na een deploy.
 *
 * Toont bewust geen enkele waarde van een instelling — alleen of ze er staat.
 * Zo kun je de pagina open laten zonder iets te lekken.
 */
export default async function Status() {
  const controles: Controle[] = [
    {
      naam: 'SESSIE_GEHEIM',
      ok: geheimIsIngesteld(),
      boodschap: geheimIsIngesteld()
        ? 'Ingesteld.'
        : `Ontbreekt of is korter dan ${GEHEIM_MINIMUM} tekens. Zonder deze waarde kan niemand aanmelden.`,
    },
    {
      naam: 'SUPABASE_URL en SUPABASE_SECRET_KEY',
      ok: supabaseIsIngesteld(),
      boodschap: supabaseIsIngesteld() ? 'Beide ingesteld.' : 'Een van beide ontbreekt.',
    },
  ];

  if (supabaseIsIngesteld()) {
    controles.push(...(await controleerDatabank()));
  }

  const allesOk = controles.every((c) => c.ok);

  return (
    <main style={{ maxWidth: 640, margin: '0 auto', padding: '2rem 1.5rem' }}>
      <h1>Status van het portaal</h1>

      <div className={`melding ${allesOk ? 'goed' : 'fout'}`} style={{ margin: '1rem 0 1.5rem' }}>
        {allesOk
          ? 'Alles staat klaar. Leerlingen kunnen aanmelden en oefenen.'
          : 'Er ontbreekt nog iets — zie hieronder.'}
      </div>

      <div className="kaart">
        <table>
          <tbody>
            {controles.map((c) => (
              <tr key={c.naam}>
                <td style={{ width: 28 }}>
                  <span className={`badge ${c.ok ? 'goed' : 'fout'}`}>{c.ok ? '✓' : '✗'}</span>
                </td>
                <td>
                  <strong>{c.naam}</strong>
                  <div className="gedempt">{c.boodschap}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!allesOk && (
        <div className="kaart" style={{ marginTop: '1rem' }}>
          <h2>Na het aanpassen van een variabele</h2>
          <p className="gedempt" style={{ marginBottom: 0 }}>
            Vercel pikt nieuwe omgevingsvariabelen <strong>niet</strong> op in een bestaande build.
            Ga naar Deployments, klik op de drie puntjes bij de laatste deployment en kies
            Redeploy. Pas daarna verandert deze pagina.
          </p>
        </div>
      )}

      <p className="gedempt" style={{ marginTop: '1.5rem', fontSize: '0.8rem' }}>
        Deze pagina toont nooit de waarde van een instelling, enkel of ze aanwezig is.
      </p>
    </main>
  );
}
