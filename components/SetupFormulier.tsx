'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function SetupFormulier() {
  const [sleutel, setSleutel] = useState('');
  const [naam, setNaam] = useState('');
  const [klas, setKlas] = useState('5OS');
  const [wachtwoord, setWachtwoord] = useState('');
  const [fout, setFout] = useState<string | null>(null);
  const [bezig, setBezig] = useState(false);
  const [gelukt, setGelukt] = useState<string | null>(null);

  async function verstuur(e: React.FormEvent) {
    e.preventDefault();
    setBezig(true);
    setFout(null);

    try {
      const antwoord = await fetch('/api/setup', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ sleutel, naam, klas, wachtwoord }),
      });
      const data = await antwoord.json();
      if (!antwoord.ok) {
        setFout(data.fout ?? 'Aanmaken mislukte.');
        return;
      }
      setGelukt(data.gebruikersnaam);
    } catch {
      setFout('De server antwoordde niet.');
    } finally {
      setBezig(false);
    }
  }

  if (gelukt) {
    return (
      <div className="kaart">
        <div className="melding goed" style={{ marginBottom: '1rem' }}>Je account is aangemaakt.</div>
        <p style={{ marginTop: 0 }}>
          Je gebruikersnaam is <strong>{gelukt}</strong>. Meld je aan met het wachtwoord dat je
          net koos.
        </p>
        <p className="melding waarschuwing">
          Haal nu <code>SETUP_SLEUTEL</code> weg in Vercel en doe een Redeploy. Deze pagina hoort
          niet open te blijven staan.
        </p>
        <Link href="/">→ Naar het aanmeldscherm</Link>
      </div>
    );
  }

  return (
    <form onSubmit={verstuur} className="kaart" style={{ display: 'grid', gap: '0.85rem' }}>
      <div>
        <label htmlFor="sleutel">Setupsleutel</label>
        <input id="sleutel" value={sleutel} onChange={(e) => setSleutel(e.target.value)} required />
        <span className="gedempt">De waarde die je in Vercel bij SETUP_SLEUTEL zette.</span>
      </div>
      <div>
        <label htmlFor="naam">Je naam</label>
        <input id="naam" value={naam} onChange={(e) => setNaam(e.target.value)} placeholder="Dieter Varey" required />
      </div>
      <div>
        <label htmlFor="klas">Klas</label>
        <input id="klas" value={klas} onChange={(e) => setKlas(e.target.value)} required />
      </div>
      <div>
        <label htmlFor="wachtwoord">Kies een wachtwoord</label>
        <input
          id="wachtwoord"
          type="password"
          value={wachtwoord}
          onChange={(e) => setWachtwoord(e.target.value)}
          autoComplete="new-password"
          minLength={8}
          required
        />
        <span className="gedempt">Minstens 8 tekens.</span>
      </div>

      {fout && <div className="melding fout">{fout}</div>}

      <button type="submit" className="primair" disabled={bezig}>
        {bezig ? 'Bezig…' : 'Account aanmaken'}
      </button>
    </form>
  );
}
