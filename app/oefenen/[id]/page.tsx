import { notFound, redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { vindOpgave } from '@/data/oefeningen';
import { isUpload } from '@/lib/werkblad-types';
import { startSessie } from '@/lib/opslag';
import { lesBijOefening } from '@/lib/lessen';
import OefeningWerkruimte from '@/components/OefeningWerkruimte';
import UploadWerkruimte from '@/components/UploadWerkruimte';

export const dynamic = 'force-dynamic';

export default async function Oefening({ params }: { params: Promise<{ id: string }> }) {
  const aangemeld = await huidigeSessie();
  if (!aangemeld) redirect('/');

  const { id } = await params;
  const opgave = vindOpgave(id);
  if (!opgave) notFound();

  let sessieId: string | null = null;
  let fout: string | null = null;
  try {
    sessieId = await startSessie(aangemeld.gebruikersnaam, opgave.id);
  } catch (e) {
    console.error('[oefenen]', e);
    fout = 'De databank is niet bereikbaar, dus je werk wordt nu niet bewaard.';
  }

  const les = await lesBijOefening(opgave.id);

  // Grafieken, draaitabellen en afdrukken gebeuren in echt Excel en komen als
  // bestand binnen; de rest maakt de leerling in het rekenblad hiernaast.
  if (isUpload(opgave)) {
    return (
      <UploadWerkruimte
        opgave={opgave}
        naam={aangemeld.naam}
        sessieId={sessieId}
        opslagFout={fout}
        les={les}
      />
    );
  }

  return (
    <OefeningWerkruimte
      opgave={opgave}
      naam={aangemeld.naam}
      sessieId={sessieId}
      opslagFout={fout}
      les={les}
    />
  );
}
