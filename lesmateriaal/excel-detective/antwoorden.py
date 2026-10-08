# -*- coding: utf-8 -*-
"""Rekent de vijf zaken uit, precies zoals Excel het zou doen."""
import importlib.util
import os
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


def deel(teller, noemer, n=3):
    """Een deling, exact gerekend en dan pas afgerond."""
    exact = Decimal(str(teller)) / Decimal(str(noemer))
    return float(exact.quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- zaak 1: de verdwenen avonden -------------------------------------
Z1_HANDELAAR = [g.handelaar(code)[1] for _, _, _, _, code in g.Z1]
Z1_OORDEEL = [g.Z1_LEUGEN if (zei == 'overwerk' and minuten < g.Z1_GRENS) else g.Z1_KLOPT
              for _, zei, minuten, _, _ in g.Z1]
Z1_AANTAL_LEUGEN = Z1_OORDEEL.count(g.Z1_LEUGEN)
Z1_BEDRAG_LEUGEN = afronden(sum(bedrag for (_, _, _, bedrag, _), oordeel
                                in zip(g.Z1, Z1_OORDEEL) if oordeel == g.Z1_LEUGEN))
Z1_BEDRAG_DADER = afronden(sum(bedrag for _, _, _, bedrag, code in g.Z1
                               if code == g.Z1_DADERCODE))
Z1_TOTAAL = afronden(sum(bedrag for _, _, _, bedrag, _ in g.Z1))
Z1_GROOTSTE = max(bedrag for _, _, _, bedrag, _ in g.Z1)
Z1_DADER = g.handelaar(g.Z1_DADERCODE)[1]
Z1_DATA_LEUGEN = [datum for (datum, *_), oordeel in zip(g.Z1, Z1_OORDEEL)
                  if oordeel == g.Z1_LEUGEN]

# --- zaak 2: de Mercedes van de Koning --------------------------------
Z2_AFSTAND = [aan - vert for _, _, _, _, vert, aan, _ in g.Z2]
Z2_TOTAAL = sum(Z2_AFSTAND)
Z2_LANGSTE = max(Z2_AFSTAND)
Z2_LANGSTE_RIT = g.Z2[Z2_AFSTAND.index(Z2_LANGSTE)]
Z2_GEM = afronden(Z2_TOTAAL / len(g.Z2), 1)
Z2_HOOGSTE_STAND = max(aan for _, _, _, _, _, aan, _ in g.Z2)
Z2_LAAGSTE_STAND = min(vert for _, _, _, _, vert, _, _ in g.Z2)
Z2_PROEF = Z2_HOOGSTE_STAND - Z2_LAAGSTE_STAND
Z2_LAATSTE = next(rij for rij in g.Z2 if rij[5] == Z2_HOOGSTE_STAND)
Z2_BESTEMMING = Z2_LAATSTE[6]
Z2_AANTAL_PER = [sum(1 for _, _, ch, _, _, _, _ in g.Z2 if ch == c)
                 for c in g.Z2_CHAUFFEURS]
Z2_KM_PER = [sum(afst for (_, _, ch, _, _, _, _), afst in zip(g.Z2, Z2_AFSTAND)
                 if ch == c) for c in g.Z2_CHAUFFEURS]

# --- zaak 3: de museumroof --------------------------------------------
Z3_ZAAL = [g.zaal(code)[1] for _, _, code, _ in g.Z3]
Z3_STATUS = [g.Z3_AANWEZIG if nr in g.Z3_TELLING else g.Z3_GESTOLEN
             for nr, _, _, _ in g.Z3]
Z3_AANTAL_GESTOLEN = Z3_STATUS.count(g.Z3_GESTOLEN)
Z3_BUIT = sum(waarde for (_, _, _, waarde), st in zip(g.Z3, Z3_STATUS)
              if st == g.Z3_GESTOLEN)
Z3_COLLECTIE = sum(waarde for _, _, _, waarde in g.Z3)
Z3_DUURSTE = max(waarde for _, _, _, waarde in g.Z3)
Z3_GEM = afronden(Z3_COLLECTIE / len(g.Z3), 0)
Z3_WEG = [(nr, stuk, g.zaal(code)[1], waarde)
          for (nr, stuk, code, waarde), st in zip(g.Z3, Z3_STATUS)
          if st == g.Z3_GESTOLEN]
Z3_ZALEN_WEG = sorted({z for _, _, z, _ in Z3_WEG})

# --- zaak 4: het gelekte examen ---------------------------------------
Z4_PER_GEBRUIKER = []
for code, naam, functie in g.Z4_GEBRUIKERS:
    logins = sum(1 for _, c, _, _, _ in g.Z4 if c == code)
    bestanden = sum(n for _, c, _, _, n in g.Z4 if c == code)
    oordeel = g.Z4_VERDACHT if bestanden > g.Z4_GRENS else g.Z4_VRIJ
    Z4_PER_GEBRUIKER.append((code, naam, functie, logins, bestanden, oordeel))
Z4_TOTAAL = sum(n for _, _, _, _, n in g.Z4)
Z4_GROOTSTE = max(n for _, _, _, _, n in g.Z4)
Z4_AANTAL_VERDACHT = sum(1 for r in Z4_PER_GEBRUIKER if r[5] == g.Z4_VERDACHT)
Z4_DADER = next((r for r in Z4_PER_GEBRUIKER if r[5] == g.Z4_VERDACHT), None)
Z4_NIPT = sorted((r for r in Z4_PER_GEBRUIKER if r[5] == g.Z4_VRIJ),
                 key=lambda r: -r[4])[0]

# --- zaak 5: de sabotage ----------------------------------------------
Z5_AFKEUR = [deel(afgekeurd, geproduceerd) for _, _, _, geproduceerd, afgekeurd in g.Z5]
Z5_TECHNICUS = [g.machine(code)[2] if pct > g.Z5_GRENS else g.Z5_GEEN
                for (_, code, _, _, _), pct in zip(g.Z5, Z5_AFKEUR)]
Z5_SLECHT = [(batch, code, pct, g.machine(code)[1], g.machine(code)[2])
             for (batch, code, _, _, _), pct in zip(g.Z5, Z5_AFKEUR)
             if pct > g.Z5_GRENS]
Z5_DADER = Counter(t for _, _, _, _, t in Z5_SLECHT).most_common(1)[0][0]
Z5_AANTAL_DADER = sum(1 for t in Z5_TECHNICUS if t == Z5_DADER)
Z5_GEPRODUCEERD = sum(p for _, _, _, p, _ in g.Z5)
Z5_AFGEKEURD = sum(a for _, _, _, _, a in g.Z5)
Z5_HOOGSTE = max(Z5_AFKEUR)
Z5_GEM = deel(sum(Z5_AFKEUR), len(Z5_AFKEUR), 4)
Z5_MACHINES_WEG = sorted({m for _, _, _, m, _ in Z5_SLECHT})


if __name__ == '__main__':
    print('=== ZAAK 1 — De verdwenen avonden ===')
    for (datum, zei, minuten, bedrag, code), hand, oordeel in zip(
            g.Z1, Z1_HANDELAAR, Z1_OORDEEL):
        print(f'   {datum}  {zei:9s} {minuten:4d} min  {bedrag:6.2f}  {hand:24s} {oordeel}')
    print(f'   leugenavonden: {Z1_AANTAL_LEUGEN} ({", ".join(Z1_DATA_LEUGEN)})')
    print(f'   bedrag op die avonden: {Z1_BEDRAG_LEUGEN:.2f}')
    print(f'   bedrag bij {g.Z1_DADERCODE} ({Z1_DADER}): {Z1_BEDRAG_DADER:.2f}')
    print(f'   PROEF: die twee moeten gelijk zijn — '
          f'{"ja" if Z1_BEDRAG_LEUGEN == Z1_BEDRAG_DADER else "NEE"}')
    print(f'   totaal uitgegeven {Z1_TOTAAL:.2f} | grootste bedrag {Z1_GROOTSTE:.2f}')

    print('\n=== ZAAK 2 — De Mercedes van de Koning ===')
    for (rit, datum, ch, vertrek, kv, ka, best), afst in zip(g.Z2, Z2_AFSTAND):
        print(f'   rit {rit:2d}  {datum}  {ch:10s} {vertrek:10s} -> {best:18s} '
              f'{kv} -> {ka}  ({afst} km)')
    print(f'   totaal {Z2_TOTAAL} km | langste rit {Z2_LANGSTE} km '
          f'(rit {Z2_LANGSTE_RIT[0]} naar {Z2_LANGSTE_RIT[6]}) | gemiddeld {Z2_GEM}')
    print(f'   PROEF: {Z2_HOOGSTE_STAND} - {Z2_LAAGSTE_STAND} = {Z2_PROEF} '
          f'({"klopt" if Z2_PROEF == Z2_TOTAAL else "KLOPT NIET"})')
    print(f'   hoogste kilometerstand {Z2_HOOGSTE_STAND} -> LAATST GEZIEN IN: '
          f'{Z2_BESTEMMING} (rit {Z2_LAATSTE[0]})')
    for c, n, km in zip(g.Z2_CHAUFFEURS, Z2_AANTAL_PER, Z2_KM_PER):
        print(f'   {c:10s} {n} ritten  {km} km')

    print('\n=== ZAAK 3 — De museumroof ===')
    for nr, stuk, zaal_, waarde in Z3_WEG:
        print(f'   WEG: {nr}  {stuk:34s} {zaal_:20s} {waarde:>8,}'.replace(',', '.'))
    print(f'   aantal gestolen {Z3_AANTAL_GESTOLEN} | buit {Z3_BUIT:,}'.replace(',', '.'))
    print(f'   collectie {Z3_COLLECTIE:,} | duurste stuk {Z3_DUURSTE:,} | '
          f'gemiddeld {Z3_GEM:,.0f}'.replace(',', '.'))
    print(f'   alle gestolen stukken komen uit: {", ".join(Z3_ZALEN_WEG)}')

    print('\n=== ZAAK 4 — Het gelekte examen ===')
    for code, naam, functie, logins, bestanden, oordeel in Z4_PER_GEBRUIKER:
        print(f'   {code}  {naam:20s} {functie:22s} {logins} logins  '
              f'{bestanden:3d} bestanden  {oordeel}')
    print(f'   totaal {Z4_TOTAAL} bestanden | grootste in één keer {Z4_GROOTSTE}')
    print(f'   verdacht: {Z4_AANTAL_VERDACHT} -> {Z4_DADER[1]} ({Z4_DADER[2]})')
    print(f'   net eronder: {Z4_NIPT[1]} met {Z4_NIPT[4]} bestanden')

    print('\n=== ZAAK 5 — De sabotage ===')
    for (batch, code, ploeg, prod, afg), pct, tech in zip(g.Z5, Z5_AFKEUR, Z5_TECHNICUS):
        vlag = '  <<<' if tech != g.Z5_GEEN else ''
        print(f'   {batch}  {code}  ploeg {ploeg}  {prod:4d} / {afg:4d} = {pct:.3f}  '
              f'{tech}{vlag}')
    print(f'   slechte batches: {len(Z5_SLECHT)} | allemaal nagekeken door {Z5_DADER}')
    print(f'   machines: {", ".join(Z5_MACHINES_WEG)}')
    print(f'   geproduceerd {Z5_GEPRODUCEERD} | afgekeurd {Z5_AFGEKEURD} | '
          f'hoogste afkeur {Z5_HOOGSTE:.3f} | gemiddeld {Z5_GEM:.4f}')
