/**
 * Video's insluiten van YouTube of Vimeo.
 *
 * Alleen die twee hosts worden aanvaard. Zonder die beperking zou een link in
 * een les een willekeurige pagina in een iframe kunnen laden, en dat is een
 * open deur op een portaal waar leerlingen aangemeld zijn.
 */

export type Insluiting = { ok: true; url: string; aanbieder: 'youtube' | 'vimeo' } | { ok: false; fout: string };

export function insluitURL(ruw: string): Insluiting {
  const tekst = ruw.trim();
  if (!tekst) return { ok: false, fout: 'Geen adres opgegeven.' };

  let url: URL;
  try {
    url = new URL(tekst);
  } catch {
    return { ok: false, fout: 'Dat is geen geldig adres. Plak de volledige link, met https:// ervoor.' };
  }

  if (url.protocol !== 'https:') {
    return { ok: false, fout: 'Gebruik een https-adres.' };
  }

  const host = url.hostname.replace(/^www\./, '');

  // --- YouTube ---
  if (host === 'youtu.be') {
    const id = url.pathname.slice(1).split('/')[0];
    return geldigeYoutubeId(id)
      ? { ok: true, url: `https://www.youtube-nocookie.com/embed/${id}`, aanbieder: 'youtube' }
      : { ok: false, fout: 'Uit die YouTube-link kan ik geen filmpje halen.' };
  }

  if (host === 'youtube.com' || host === 'm.youtube.com' || host === 'youtube-nocookie.com') {
    const id = url.pathname.startsWith('/embed/')
      ? url.pathname.split('/')[2]
      : (url.searchParams.get('v') ?? '');
    return geldigeYoutubeId(id)
      ? { ok: true, url: `https://www.youtube-nocookie.com/embed/${id}`, aanbieder: 'youtube' }
      : { ok: false, fout: 'Uit die YouTube-link kan ik geen filmpje halen.' };
  }

  // --- Vimeo ---
  if (host === 'vimeo.com' || host === 'player.vimeo.com') {
    const delen = url.pathname.split('/').filter(Boolean);
    const id = delen.find((d) => /^\d+$/.test(d));
    if (!id) return { ok: false, fout: 'Uit die Vimeo-link kan ik geen filmpje halen.' };
    // Een privélink heeft een hash: vimeo.com/123456789/abcdef123
    const hash = delen[delen.indexOf(id) + 1];
    const query = hash && /^[a-z0-9]+$/i.test(hash) ? `?h=${hash}` : '';
    return { ok: true, url: `https://player.vimeo.com/video/${id}${query}`, aanbieder: 'vimeo' };
  }

  return {
    ok: false,
    fout: 'Alleen YouTube en Vimeo worden ondersteund. Zet je filmpje daar als "verborgen" of "niet-vermeld" en plak die link hier.',
  };
}

function geldigeYoutubeId(id: string): boolean {
  return /^[A-Za-z0-9_-]{11}$/.test(id);
}
