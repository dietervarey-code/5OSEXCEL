import Link from 'next/link';
import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { lijstLessen, vindLes, type Les } from '@/lib/lessen';
import { verklaar } from '@/lib/opslag';
import { ConfiguratieFout } from '@/lib/supabase';
import { OEFENINGEN } from '@/data/oefeningen';
import LessenBeheer from '@/components/LessenBeheer';

export const dynamic = 'force-dynamic';

export default async function LessenBeheerPagina({
  searchParams,
}: {
  searchParams: Promise<{ les?: string }>;
}) {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');
  if (sessie.rol !== 'leerkracht') redirect('/lessen');

  const { les: gekozen } = await searchParams;

  let lessen: Les[] = [];
  let huidige: Les | null = null;
  let fout: string | null = null;

  try {
    lessen = await lijstLessen(true);
    if (gekozen) huidige = await vindLes(gekozen, true);
  } catch (e) {
    fout = e instanceof ConfiguratieFout ? e.message : e instanceof Error ? verklaar(e.message) : 'Kon de lessen niet laden.';
  }

  const oefeningen = Object.values(OEFENINGEN).map((o) => ({ id: o.id, titel: o.titel }));

  return (
    <main style={{ maxWidth: 1000, margin: '0 auto', padding: '1.5rem' }}>
      <header className="balk" style={{ borderRadius: 10, border: '1px solid var(--rand)', marginBottom: '1.2rem' }}>
        <div>
          <h1 style={{ marginBottom: 0 }}>Lessen beheren</h1>
          <span className="gedempt">Theorie, voorbeelden en filmpjes</span>
        </div>
        <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center' }}>
          <Link href="/lessen">Zoals de leerling het ziet →</Link>
          <Link href="/leerkracht">Opvolging</Link>
        </div>
      </header>

      {fout && <div className="melding fout" style={{ marginBottom: '1rem' }}>{fout}</div>}

      {/*
        De key dwingt een verse editor af zodra je een andere les kiest.
        Zonder dat hergebruikt React het component en blijven de velden op de
        vorige les staan — je zou dan les B kunnen bewaren met de tekst van A.
      */}
      <LessenBeheer
        key={huidige?.id ?? 'nieuw'}
        lessen={lessen}
        huidige={huidige}
        oefeningen={oefeningen}
      />
    </main>
  );
}
