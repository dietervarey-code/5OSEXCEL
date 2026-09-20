import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import { vindOpgave } from '@/data/oefeningen';
import OefeningWerkruimte from '@/components/OefeningWerkruimte';

export default async function Oefenen() {
  const sessie = await huidigeSessie();
  if (!sessie) redirect('/');

  // Technische proef: één oefening. In fase 2 komt hier een overzicht per Focus.
  const opgave = vindOpgave('factuur-basis');
  if (!opgave) redirect('/');

  return <OefeningWerkruimte opgave={opgave} naam={sessie.naam} />;
}
