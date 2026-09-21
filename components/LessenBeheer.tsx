'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Lesinhoud from '@/components/Lesinhoud';
import type { Les } from '@/lib/lessen';

const VOORBEELD = `## Wat je moet kunnen

Leg hier kort uit wat de leerling na deze les kan.

## Uitleg

Een formule begint altijd met een isgelijkteken: \`=SOM(E12:E16)\`.

| Cel | Formule | Resultaat |
|-----|---------|-----------|
| E18 | \`=SOM(E12:E16)\` | 3253,40 |

> Let op: gebruik \`$B$21\` als je de formule wil doorvoeren.
`;

type Oefening = { id: string; titel: string };

export default function LessenBeheer({
  lessen,
  huidige,
  oefeningen,
}: {
  lessen: Les[];
  huidige: Les | null;
  oefeningen: Oefening[];
}) {
  const router = useRouter();
  const [fout, setFout] = useState<string | null>(null);
  const [bezig, setBezig] = useState(false);

  // Bewerkvelden
  const [focus, setFocus] = useState(huidige?.focus ?? 1);
  const [titel, setTitel] = useState(huidige?.titel ?? '');
  const [samenvatting, setSamenvatting] = useState(huidige?.samenvatting ?? '');
  const [inhoud, setInhoud] = useState(huidige?.inhoud ?? '');
  const [oefeningId, setOefeningId] = useState(huidige?.oefeningId ?? '');
  const [volgnummer, setVolgnummer] = useState(huidige?.volgnummer ?? 0);
  const [voorbeeld, setVoorbeeld] = useState(false);

  // Media
  const [videoTitel, setVideoTitel] = useState('');
  const [videoUrl, setVideoUrl] = useState('');

  async function stuur(methode: string, body: unknown, pad = '/api/leerkracht/lessen') {
    setBezig(true);
    setFout(null);
    try {
      const antwoord = await fetch(pad, {
        method: methode,
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await antwoord.json();
      if (!antwoord.ok) {
        setFout(data.fout ?? 'Er ging iets mis.');
        return null;
      }
      return data;
    } catch {
      setFout('De server antwoordde niet.');
      return null;
    } finally {
      setBezig(false);
    }
  }

  async function nieuweLes() {
    const data = await stuur('POST', {
      focus,
      titel: titel || 'Nieuwe les',
      samenvatting,
      inhoud: inhoud || VOORBEELD,
      oefeningId: oefeningId || null,
      volgnummer,
    });
    if (data?.id) router.push(`/leerkracht/lessen?les=${data.id}`);
  }

  async function bewaar() {
    if (!huidige) return;
    const ok = await stuur('PATCH', {
      id: huidige.id, focus, titel, samenvatting, inhoud,
      oefeningId: oefeningId || null, volgnummer,
    });
    if (ok) router.refresh();
  }

  async function zetPublicatie(gepubliceerd: boolean) {
    if (!huidige) return;
    if (await stuur('PATCH', { id: huidige.id, gepubliceerd })) router.refresh();
  }

  async function wisLes() {
    if (!huidige) return;
    if (!confirm(`"${huidige.titel}" verwijderen? Ook de filmpjes en bestanden bij deze les verdwijnen.`)) return;
    if (await stuur('DELETE', { id: huidige.id })) router.push('/leerkracht/lessen');
  }

  async function voegVideoToe(e: React.FormEvent) {
    e.preventDefault();
    if (!huidige) return;
    const ok = await stuur('POST', { lesId: huidige.id, titel: videoTitel, url: videoUrl }, '/api/leerkracht/lessen/media');
    if (ok) { setVideoTitel(''); setVideoUrl(''); router.refresh(); }
  }

  async function uploadBestand(e: React.ChangeEvent<HTMLInputElement>) {
    if (!huidige || !e.target.files?.[0]) return;
    const form = new FormData();
    form.append('lesId', huidige.id);
    form.append('bestand', e.target.files[0]);

    setBezig(true);
    setFout(null);
    try {
      const antwoord = await fetch('/api/leerkracht/lessen/media', { method: 'POST', body: form });
      const data = await antwoord.json();
      if (!antwoord.ok) setFout(data.fout ?? 'Opladen mislukte.');
      else router.refresh();
    } catch {
      setFout('De server antwoordde niet.');
    } finally {
      setBezig(false);
      e.target.value = '';
    }
  }

  async function wisMedia(id: string) {
    if (await stuur('DELETE', { id }, '/api/leerkracht/lessen/media')) router.refresh();
  }

  const invoerStijl = {
    width: '100%', padding: '0.55rem 0.7rem', border: '1px solid var(--rand)',
    borderRadius: 6, font: 'inherit',
  } as const;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(220px, 280px) 1fr', gap: '1.2rem', alignItems: 'start' }}>
      {/* --- Lijst --- */}
      <aside className="kaart">
        <h2>Lessen ({lessen.length})</h2>
        <div style={{ display: 'grid', gap: '0.35rem', marginBottom: '0.9rem' }}>
          {lessen.map((l) => (
            <Link
              key={l.id}
              href={`/leerkracht/lessen?les=${l.id}`}
              style={{
                padding: '0.45rem 0.6rem', borderRadius: 6, textDecoration: 'none', color: 'inherit',
                background: huidige?.id === l.id ? '#eef2f8' : 'transparent',
                border: '1px solid ' + (huidige?.id === l.id ? 'var(--rand)' : 'transparent'),
              }}
            >
              <div style={{ fontSize: '0.75rem', color: 'var(--gedempt)' }}>Focus {l.focus}</div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{l.titel}</div>
              {!l.gepubliceerd && <span className="badge waarschuwing">concept</span>}
            </Link>
          ))}
          {lessen.length === 0 && <span className="gedempt">Nog geen lessen.</span>}
        </div>
        <Link href="/leerkracht/lessen"><button style={{ width: '100%' }}>+ Nieuwe les</button></Link>
      </aside>

      {/* --- Editor --- */}
      <section style={{ display: 'grid', gap: '1.2rem' }}>
        <div className="kaart">
          <h2>{huidige ? 'Les bewerken' : 'Nieuwe les'}</h2>

          <div style={{ display: 'grid', gridTemplateColumns: '100px 1fr 100px', gap: '0.8rem', marginBottom: '0.8rem' }}>
            <div>
              <label htmlFor="focus">Focus</label>
              <input id="focus" type="number" min={1} max={9} value={focus}
                     onChange={(e) => setFocus(Number(e.target.value))} />
            </div>
            <div>
              <label htmlFor="titel">Titel</label>
              <input id="titel" value={titel} onChange={(e) => setTitel(e.target.value)}
                     placeholder="Formules met absolute celverwijzing" />
            </div>
            <div>
              <label htmlFor="volgnummer">Volgorde</label>
              <input id="volgnummer" type="number" value={volgnummer}
                     onChange={(e) => setVolgnummer(Number(e.target.value))} />
            </div>
          </div>

          <div style={{ marginBottom: '0.8rem' }}>
            <label htmlFor="samenvatting">In het kort</label>
            <input id="samenvatting" value={samenvatting} onChange={(e) => setSamenvatting(e.target.value)}
                   placeholder="Eén zin die bovenaan de les komt." />
          </div>

          <div style={{ marginBottom: '0.8rem' }}>
            <label htmlFor="oefening">Hoort bij de oefening</label>
            <select id="oefening" value={oefeningId} onChange={(e) => setOefeningId(e.target.value)} style={invoerStijl}>
              <option value="">— geen —</option>
              {oefeningen.map((o) => <option key={o.id} value={o.id}>{o.titel}</option>)}
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end' }}>
            <label htmlFor="inhoud" style={{ marginBottom: 0 }}>Theorie</label>
            <button type="button" onClick={() => setVoorbeeld((v) => !v)} style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem' }}>
              {voorbeeld ? 'Bewerken' : 'Voorbeeld bekijken'}
            </button>
          </div>

          {voorbeeld ? (
            <div className="kaart" style={{ marginTop: '0.4rem', minHeight: 260 }}>
              <Lesinhoud markdown={inhoud} />
            </div>
          ) : (
            <textarea id="inhoud" value={inhoud} onChange={(e) => setInhoud(e.target.value)} rows={18}
                      placeholder={VOORBEELD}
                      style={{ ...invoerStijl, marginTop: '0.4rem', fontFamily: 'ui-monospace, Menlo, Consolas, monospace', fontSize: '0.85rem', resize: 'vertical' }} />
          )}
          <span className="gedempt">
            Opmaak met Markdown: <code>## Kop</code>, <code>**vet**</code>, <code>`=SOM(A1:A5)`</code>,
            lijsten met <code>-</code>, en tabellen met <code>|</code>.
          </span>

          {fout && <div className="melding fout" style={{ marginTop: '0.8rem' }}>{fout}</div>}

          <div style={{ display: 'flex', gap: '0.6rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            {huidige ? (
              <>
                <button className="primair" onClick={bewaar} disabled={bezig}>{bezig ? 'Bezig…' : 'Bewaren'}</button>
                <button onClick={() => zetPublicatie(!huidige.gepubliceerd)} disabled={bezig}>
                  {huidige.gepubliceerd ? 'Terug naar concept' : 'Publiceren voor de klas'}
                </button>
                <Link href={`/lessen/${huidige.id}`}><button type="button">Bekijken</button></Link>
                <button onClick={wisLes} disabled={bezig} style={{ color: 'var(--fout)', marginLeft: 'auto' }}>Verwijderen</button>
              </>
            ) : (
              <button className="primair" onClick={nieuweLes} disabled={bezig}>{bezig ? 'Bezig…' : 'Les aanmaken'}</button>
            )}
          </div>
        </div>

        {/* --- Media --- */}
        {huidige && (
          <div className="kaart">
            <h2>Filmpjes en bestanden</h2>

            {huidige.media.length > 0 && (
              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 1rem' }}>
                {huidige.media.map((m) => (
                  <li key={m.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                          padding: '0.45rem 0', borderBottom: '1px solid var(--rand)' }}>
                    <span>
                      <span className="badge">{m.soort}</span>{' '}
                      <strong>{m.titel}</strong>
                      <div className="gedempt" style={{ fontSize: '0.78rem' }}>{m.bron}</div>
                    </span>
                    <button onClick={() => wisMedia(m.id)} style={{ color: 'var(--fout)' }}>Verwijderen</button>
                  </li>
                ))}
              </ul>
            )}

            <form onSubmit={voegVideoToe} style={{ display: 'grid', gap: '0.6rem', marginBottom: '1.2rem' }}>
              <strong>Filmpje toevoegen</strong>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr auto', gap: '0.6rem' }}>
                <input value={videoTitel} onChange={(e) => setVideoTitel(e.target.value)} placeholder="Titel" />
                <input value={videoUrl} onChange={(e) => setVideoUrl(e.target.value)}
                       placeholder="https://youtu.be/..." required />
                <button type="submit" disabled={bezig}>Toevoegen</button>
              </div>
              <span className="gedempt">
                Zet je filmpje op YouTube of Vimeo als <strong>verborgen</strong> of <strong>niet-vermeld</strong> en
                plak de link hier. Zo vindt niemand het via een zoekmachine, en je verbruikt geen opslag.
              </span>
            </form>

            <div style={{ display: 'grid', gap: '0.5rem' }}>
              <strong>Bestand opladen</strong>
              <input type="file" onChange={uploadBestand} disabled={bezig}
                     accept=".xlsx,.xls,.pdf,.png,.jpg,.jpeg,.webp" />
              <span className="gedempt">
                Voor een voorbeeldwerkmap, een pdf of een schermafbeelding. Maximaal 20 MB.
                Filmpjes horen hier niet: die vreten je gratis opslag en verkeer op.
              </span>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
