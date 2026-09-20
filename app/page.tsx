import { redirect } from 'next/navigation';
import { huidigeSessie } from '@/lib/auth';
import LoginFormulier from '@/components/LoginFormulier';

export default async function Aanmelden() {
  const sessie = await huidigeSessie();
  if (sessie) redirect(sessie.rol === 'leerkracht' ? '/leerkracht' : '/oefenen');

  return (
    <main style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', padding: '1.5rem' }}>
      <div className="kaart" style={{ width: '100%', maxWidth: 380 }}>
        <h1>5OS Excel</h1>
        <p className="gedempt" style={{ marginTop: 0 }}>
          Meld je aan met de gegevens die je van je leerkracht kreeg.
        </p>
        <LoginFormulier />
      </div>
    </main>
  );
}
