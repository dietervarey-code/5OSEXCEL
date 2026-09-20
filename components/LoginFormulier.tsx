'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginFormulier() {
  const router = useRouter();
  const [gebruikersnaam, setGebruikersnaam] = useState('');
  const [wachtwoord, setWachtwoord] = useState('');
  const [fout, setFout] = useState<string | null>(null);
  const [bezig, setBezig] = useState(false);

  async function verstuur(e: React.FormEvent) {
    e.preventDefault();
    setBezig(true);
    setFout(null);

    const antwoord = await fetch('/api/login', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ gebruikersnaam, wachtwoord }),
    });

    if (!antwoord.ok) {
      const { fout: boodschap } = await antwoord.json();
      setFout(boodschap ?? 'Aanmelden lukte niet.');
      setBezig(false);
      return;
    }

    const { rol } = await antwoord.json();
    router.push(rol === 'leerkracht' ? '/leerkracht' : '/oefenen');
    router.refresh();
  }

  return (
    <form onSubmit={verstuur} style={{ display: 'grid', gap: '0.85rem' }}>
      <div>
        <label htmlFor="gebruikersnaam">Gebruikersnaam</label>
        <input
          id="gebruikersnaam"
          value={gebruikersnaam}
          onChange={(e) => setGebruikersnaam(e.target.value)}
          autoComplete="username"
          autoCapitalize="none"
          required
        />
      </div>
      <div>
        <label htmlFor="wachtwoord">Wachtwoord</label>
        <input
          id="wachtwoord"
          type="password"
          value={wachtwoord}
          onChange={(e) => setWachtwoord(e.target.value)}
          autoComplete="current-password"
          required
        />
      </div>

      {fout && <div className="melding fout">{fout}</div>}

      <button type="submit" className="primair" disabled={bezig}>
        {bezig ? 'Bezig…' : 'Aanmelden'}
      </button>
    </form>
  );
}
