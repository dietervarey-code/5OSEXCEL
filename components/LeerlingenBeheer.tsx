'use client';

import { useState } from 'react';
import type { LeerlingOverzicht } from '@/lib/opslag';

type NieuwAccount = { naam: string; gebruikersnaam: string; wachtwoord: string };

export default function LeerlingenBeheer({
  beginLijst,
  standaardKlas,
  ikZelf,
}: {
  beginLijst: LeerlingOverzicht[];
  standaardKlas: string;
  ikZelf: string;
}) {
  const [lijst, setLijst] = useState(beginLijst);
  const [namen, setNamen] = useState('');
  const [klas, setKlas] = useState(standaardKlas);
  const [bezig, setBezig] = useState(false);
  const [fout, setFout] = useState<string | null>(null);

  // Wachtwoorden komen hier één keer binnen en worden nergens bewaard.
  const [tonen, setTonen] = useState<NieuwAccount[]>([]);

  async function maakAan(e: React.FormEvent) {
    e.preventDefault();
    setBezig(true);
    setFout(null);

    try {
      const antwoord = await fetch('/api/leerkracht/leerlingen', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ namen, klas }),
      });
      const data = await antwoord.json();
      if (!antwoord.ok) {
        setFout(data.fout ?? 'Aanmaken mislukte.');
        return;
      }

      setTonen(data.aangemaakt);
      setNamen('');
      setLijst((huidig) => [
        ...huidig,
        ...data.aangemaakt.map((a: NieuwAccount) => ({
          gebruikersnaam: a.gebruikersnaam,
          naam: a.naam,
          klas,
          rol: 'leerling' as const,
          aangemaaktOp: Date.now(),
        })),
      ].sort((a, b) => a.naam.localeCompare(b.naam)));

      if (data.geweigerd?.length) {
        setFout(`Overgeslagen (geen bruikbare naam): ${data.geweigerd.join(', ')}`);
      }
    } catch {
      setFout('De server antwoordde niet.');
    } finally {
      setBezig(false);
    }
  }

  async function nieuwWachtwoord(gebruikersnaam: string, naam: string) {
    setFout(null);
    const antwoord = await fetch('/api/leerkracht/leerlingen', {
      method: 'PATCH',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ gebruikersnaam }),
    });
    const data = await antwoord.json();
    if (!antwoord.ok) {
      setFout(data.fout ?? 'Wachtwoord wijzigen mislukte.');
      return;
    }
    setTonen([{ naam, gebruikersnaam, wachtwoord: data.wachtwoord }]);
  }

  async function verwijder(gebruikersnaam: string, naam: string) {
    if (!confirm(`${naam} verwijderen? Ook alle scores en metingen van deze leerling verdwijnen. Dit kan niet ongedaan gemaakt worden.`)) {
      return;
    }
    setFout(null);
    const antwoord = await fetch('/api/leerkracht/leerlingen', {
      method: 'DELETE',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ gebruikersnaam }),
    });
    const data = await antwoord.json();
    if (!antwoord.ok) {
      setFout(data.fout ?? 'Verwijderen mislukte.');
      return;
    }
    setLijst((huidig) => huidig.filter((l) => l.gebruikersnaam !== gebruikersnaam));
  }

  function kopieer() {
    const tekst = tonen.map((a) => `${a.naam}\t${a.gebruikersnaam}\t${a.wachtwoord}`).join('\n');
    navigator.clipboard?.writeText(tekst);
  }

  return (
    <>
      {tonen.length > 0 && (
        <section className="kaart" style={{ marginBottom: '1.2rem', borderColor: 'var(--goed)' }}>
          <h2>Deel deze gegevens nu uit</h2>
          <p className="melding waarschuwing">
            Deze wachtwoorden zie je maar één keer. Ze worden versleuteld bewaard en zijn hierna
            niet meer op te vragen — wel opnieuw in te stellen.
          </p>

          <table>
            <thead>
              <tr><th>Naam</th><th>Gebruikersnaam</th><th>Wachtwoord</th></tr>
            </thead>
            <tbody>
              {tonen.map((a) => (
                <tr key={a.gebruikersnaam}>
                  <td>{a.naam}</td>
                  <td><code>{a.gebruikersnaam}</code></td>
                  <td><code><strong>{a.wachtwoord}</strong></code></td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ display: 'flex', gap: '0.6rem', marginTop: '0.9rem' }}>
            <button onClick={kopieer}>Kopieer naar klembord</button>
            <button onClick={() => window.print()}>Afdrukken</button>
            <button onClick={() => setTonen([])}>Ik heb ze genoteerd</button>
          </div>
        </section>
      )}

      <section className="kaart" style={{ marginBottom: '1.2rem' }}>
        <h2>Accounts aanmaken</h2>
        <form onSubmit={maakAan} style={{ display: 'grid', gap: '0.85rem' }}>
          <div>
            <label htmlFor="namen">Namen, één per lijn</label>
            <textarea
              id="namen"
              value={namen}
              onChange={(e) => setNamen(e.target.value)}
              rows={7}
              placeholder={'Lotte Desmet\nYoussef El Amrani\nNoor Vandenberghe'}
              required
              style={{
                width: '100%', padding: '0.55rem 0.7rem', border: '1px solid var(--rand)',
                borderRadius: 6, font: 'inherit', resize: 'vertical',
              }}
            />
            <span className="gedempt">
              Gebruikersnaam en wachtwoord worden automatisch gemaakt. Bestaat een naam al, dan
              krijgt de tweede een cijfer erachter.
            </span>
          </div>

          <div style={{ maxWidth: 200 }}>
            <label htmlFor="klas">Klas</label>
            <input id="klas" value={klas} onChange={(e) => setKlas(e.target.value)} required />
          </div>

          {fout && <div className="melding fout">{fout}</div>}

          <div>
            <button type="submit" className="primair" disabled={bezig}>
              {bezig ? 'Bezig…' : 'Accounts aanmaken'}
            </button>
          </div>
        </form>
      </section>

      <section className="kaart">
        <h2>Huidige accounts ({lijst.length})</h2>
        {lijst.length === 0 ? (
          <p className="gedempt" style={{ marginBottom: 0 }}>Nog geen accounts.</p>
        ) : (
          <table>
            <thead>
              <tr><th>Naam</th><th>Gebruikersnaam</th><th>Klas</th><th>Rol</th><th></th></tr>
            </thead>
            <tbody>
              {lijst.map((l) => (
                <tr key={l.gebruikersnaam}>
                  <td><strong>{l.naam}</strong></td>
                  <td><code>{l.gebruikersnaam}</code></td>
                  <td>{l.klas}</td>
                  <td>{l.rol === 'leerkracht' ? <span className="badge waarschuwing">leerkracht</span> : 'leerling'}</td>
                  <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                    <button onClick={() => nieuwWachtwoord(l.gebruikersnaam, l.naam)}>
                      Nieuw wachtwoord
                    </button>
                    {l.gebruikersnaam !== ikZelf && (
                      <button
                        onClick={() => verwijder(l.gebruikersnaam, l.naam)}
                        style={{ marginLeft: '0.4rem', color: 'var(--fout)' }}
                      >
                        Verwijderen
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  );
}
