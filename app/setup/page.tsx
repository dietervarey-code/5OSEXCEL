import Link from 'next/link';
import { supabaseIsIngesteld, ConfiguratieFout } from '@/lib/supabase';
import { telLeerkrachten, verklaar } from '@/lib/opslag';
import SetupFormulier from '@/components/SetupFormulier';

export const dynamic = 'force-dynamic';

export default async function Setup() {
  const sleutelIngesteld = Boolean(process.env.SETUP_SLEUTEL);

  let alLeerkracht = false;
  let databankFout: string | null = null;

  if (supabaseIsIngesteld()) {
    try {
      alLeerkracht = (await telLeerkrachten()) > 0;
    } catch (e) {
      databankFout = e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : 'De databank is niet bereikbaar.';
    }
  }

  return (
    <main style={{ maxWidth: 520, margin: '0 auto', padding: '2rem 1.5rem' }}>
      <h1>Eerste leerkrachtaccount</h1>

      {!supabaseIsIngesteld() && (
        <div className="melding fout">
          Supabase is nog niet ingesteld. Kijk eerst op <Link href="/status">/status</Link>.
        </div>
      )}

      {databankFout && <div className="melding fout">{databankFout}</div>}

      {supabaseIsIngesteld() && !databankFout && alLeerkracht && (
        <div className="melding goed">
          Er bestaat al een leerkrachtaccount. Meld je <Link href="/">aan</Link> en beheer de rest
          via Leerlingen. Haal <code>SETUP_SLEUTEL</code> nu weg in Vercel.
        </div>
      )}

      {supabaseIsIngesteld() && !databankFout && !alLeerkracht && !sleutelIngesteld && (
        <div className="kaart">
          <p style={{ marginTop: 0 }}>Deze pagina staat uit. Om ze eenmalig te openen:</p>
          <ol style={{ paddingLeft: '1.1rem' }}>
            <li>Zet in Vercel een variabele <code>SETUP_SLEUTEL</code> met een zelfgekozen waarde van minstens 8 tekens.</li>
            <li>Deployments → drie puntjes → <strong>Redeploy</strong>.</li>
            <li>Kom terug op deze pagina en vul die waarde in.</li>
          </ol>
          <p className="gedempt" style={{ marginBottom: 0 }}>
            Haal de variabele daarna weer weg. Zonder die sleutel kan niemand langs deze weg
            een leerkrachtaccount aanmaken.
          </p>
        </div>
      )}

      {supabaseIsIngesteld() && !databankFout && !alLeerkracht && sleutelIngesteld && (
        <SetupFormulier />
      )}
    </main>
  );
}
