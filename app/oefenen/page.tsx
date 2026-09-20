import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { vindOpgave } from '@/data/oefeningen';
import { startSessie } from '@/lib/opslag';
import OefeningWerkruimte from '@/components/OefeningWerkruimte';

export const dynamic = 'force-dynamic';

export default async function Oefenen() {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) redirect('/');

  // Technische proef: één oefening. In fase 2 komt hier een overzicht per Focus.
  const opgave = vindOpgave('factuur-basis');
  if (!opgave) redirect('/');

  let sessieId: string | null = null;
  let fout: string | null = null;
  try {
    sessieId = await startSessie(aangemeld.gebruikersnaam, opgave.id);
  } catch (e) {
    console.error('[oefenen]', e);
    fout = 'De databank is niet bereikbaar, dus je werk wordt nu niet bewaard.';
  }

  return (
    <OefeningWerkruimte
      opgave={opgave}
      naam={aangemeld.naam}
      sessieId={sessieId}
      opslagFout={fout}
    />
  );
}
