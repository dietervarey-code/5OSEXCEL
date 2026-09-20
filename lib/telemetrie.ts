'use client';

import { useEffect, useRef, useState } from 'react';

export type Samenvatting = {
  /** Hoe vaak het tabblad uit beeld ging. */
  keerWeg: number;
  /** Totale tijd dat het tabblad niet zichtbaar was, in milliseconden. */
  wegMs: number;
  /** Tijd sinds de start van de oefening. */
  actiefMs: number;
};

type Uitgaand = { sessieId: string; soort: string; tijdstip: number; duurMs?: number };

const HARTSLAG_MS = 30_000;
const VERSTUUR_MS = 10_000;

/**
 * Meet of de leerling het oefenscherm open heeft staan.
 *
 * Wat dit WEL ziet: dat dit tabblad verborgen of niet-actief is, hoe lang en
 * hoe vaak. Wat dit NIET ziet: wat er in een ander venster gebeurt, of wat er
 * op een tweede scherm of gsm staat. Het is dus een indicatie, geen bewijs.
 */
export function useTelemetrie(sessieId: string | null, actief: boolean) {
  const [samenvatting, setSamenvatting] = useState<Samenvatting>({ keerWeg: 0, wegMs: 0, actiefMs: 0 });
  const wachtrij = useRef<Uitgaand[]>([]);
  const verborgenSinds = useRef<number | null>(null);
  const gestartOp = useRef<number>(Date.now());

  useEffect(() => {
    if (!actief || !sessieId) return;

    // In een const, zodat TypeScript de smallere typering ook binnen de
    // hieronder gedeclareerde functies behoudt.
    const sessie = sessieId;

    gestartOp.current = Date.now();
    wachtrij.current.push({ sessieId: sessie, soort: 'gestart', tijdstip: Date.now() });

    function opVisibility() {
      if (document.hidden) {
        verborgenSinds.current = Date.now();
        wachtrij.current.push({ sessieId: sessie, soort: 'verborgen', tijdstip: Date.now() });
        setSamenvatting((s) => ({ ...s, keerWeg: s.keerWeg + 1 }));
      } else {
        const duurMs = verborgenSinds.current ? Date.now() - verborgenSinds.current : 0;
        verborgenSinds.current = null;
        wachtrij.current.push({ sessieId: sessie, soort: 'zichtbaar', tijdstip: Date.now(), duurMs });
        setSamenvatting((s) => ({ ...s, wegMs: s.wegMs + duurMs }));
      }
    }

    function opBlur() {
      wachtrij.current.push({ sessieId: sessie, soort: 'focus_weg', tijdstip: Date.now() });
    }
    function opFocus() {
      wachtrij.current.push({ sessieId: sessie, soort: 'focus_terug', tijdstip: Date.now() });
    }
    function opPaste() {
      wachtrij.current.push({ sessieId: sessie, soort: 'geplakt', tijdstip: Date.now() });
    }

    document.addEventListener('visibilitychange', opVisibility);
    window.addEventListener('blur', opBlur);
    window.addEventListener('focus', opFocus);
    window.addEventListener('paste', opPaste);

    const hartslag = setInterval(() => {
      if (!document.hidden) wachtrij.current.push({ sessieId: sessie, soort: 'hartslag', tijdstip: Date.now() });
      setSamenvatting((s) => ({ ...s, actiefMs: Date.now() - gestartOp.current }));
    }, HARTSLAG_MS);

    async function spoel() {
      if (wachtrij.current.length === 0) return;
      const batch = wachtrij.current.splice(0, wachtrij.current.length);
      try {
        await fetch('/api/gebeurtenissen', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ gebeurtenissen: batch }),
          keepalive: true,
        });
      } catch {
        // Netwerk even weg: terug in de wachtrij, volgende ronde opnieuw.
        wachtrij.current.unshift(...batch);
      }
    }

    const spoelen = setInterval(spoel, VERSTUUR_MS);

    // Laatste batch nog wegschrijven als het tabblad sluit.
    const opUnload = () => {
      if (wachtrij.current.length === 0) return;
      navigator.sendBeacon?.(
        '/api/gebeurtenissen',
        new Blob([JSON.stringify({ gebeurtenissen: wachtrij.current })], { type: 'application/json' }),
      );
    };
    window.addEventListener('pagehide', opUnload);

    return () => {
      document.removeEventListener('visibilitychange', opVisibility);
      window.removeEventListener('blur', opBlur);
      window.removeEventListener('focus', opFocus);
      window.removeEventListener('paste', opPaste);
      window.removeEventListener('pagehide', opUnload);
      clearInterval(hartslag);
      clearInterval(spoelen);
      void spoel();
    };
  }, [sessieId, actief]);

  return samenvatting;
}
