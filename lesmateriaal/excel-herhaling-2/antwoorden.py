# -*- coding: utf-8 -*-
"""Rekent alle antwoorden uit, precies zoals Excel het zou doen."""
import importlib.util
import sys

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal
import os
from decimal import Decimal, ROUND_HALF_UP

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- blad 1: weekomzet -------------------------------------------------
B1_DAGTOTAAL = [afronden(p + t + ger) for _, p, t, ger in g.B1]
B1_KOLOM = [afronden(sum(rij[i] for rij in g.B1)) for i in (1, 2, 3)]
B1_EINDTOTAAL = afronden(sum(B1_DAGTOTAAL))

# --- blad 2: kwekers ---------------------------------------------------
B2_TOTAAL = [a + m + j for _, a, m, j in g.B2]
B2_SOM = sum(B2_TOTAAL)
B2_GEM = afronden(sum(B2_TOTAAL) / len(B2_TOTAAL), 1)
B2_MAX = max(B2_TOTAAL)
B2_MIN = min(B2_TOTAAL)
B2_AANTAL = len(B2_TOTAAL)
B2_GROOT = ['ja' if t >= g.B2_GROOT else 'nee' for t in B2_TOTAAL]
B2_AANTAL_GROOT = B2_GROOT.count('ja')

# --- blad 3: prijsverhoging --------------------------------------------
B3_VERHOGING = [afronden(prijs * g.B3_PERCENTAGE) for _, prijs in g.B3]
B3_NIEUW = [afronden(prijs + v) for (_, prijs), v in zip(g.B3, B3_VERHOGING)]
B3_SOM_OUD = afronden(sum(p for _, p in g.B3))
B3_SOM_VERHOGING = afronden(sum(B3_VERHOGING))
B3_SOM_NIEUW = afronden(sum(B3_NIEUW))

# --- blad 4: bezoekers -------------------------------------------------
B4_WAARDEN = [v for _, v in g.B4]
B4_SOM = sum(B4_WAARDEN)
B4_GEM = afronden(sum(B4_WAARDEN) / len(B4_WAARDEN))
B4_MAX = max(B4_WAARDEN)
B4_MIN = min(B4_WAARDEN)
B4_AANTAL = len(B4_WAARDEN)
B4_BOVEN_GEM = [m for m, v in g.B4 if v > B4_GEM]
B4_BOVEN_DREMPEL = sum(1 for v in B4_WAARDEN if v > g.B4_DREMPEL)

# --- blad 5: snoeicursus -----------------------------------------------
B5_RESULTAAT = ['Geslaagd' if p >= g.B5_GRENS else 'Niet geslaagd' for _, p in g.B5]
B5_GESLAAGD = B5_RESULTAAT.count('Geslaagd')
B5_NIET = B5_RESULTAAT.count('Niet geslaagd')
B5_GEM = afronden(sum(p for _, p in g.B5) / len(g.B5), 1)
B5_AANTAL = len(g.B5)

# --- blad 6: leveranciers ----------------------------------------------
B6_AANTAL_PER = [sum(1 for _, lev, _ in g.B6 if lev == naam) for naam in g.B6_LEVERANCIERS]
B6_BEDRAG_PER = [afronden(sum(b for _, lev, b in g.B6 if lev == naam))
                 for naam in g.B6_LEVERANCIERS]
B6_TOTAAL_ALLES = afronden(sum(b for _, _, b in g.B6))
B6_TOTAAL_PER = afronden(sum(B6_BEDRAG_PER))

# --- blad 7: zaadcodes -------------------------------------------------
B7_REGELS = []
for code, aantal in g.B7_REGELS:
    _, oms, prijs = g.zoek(code)
    B7_REGELS.append((code, oms, prijs, aantal, afronden(prijs * aantal)))
B7_EINDTOTAAL = afronden(sum(r[4] for r in B7_REGELS))
B7_DEELTOTAAL = afronden(sum(r[4] for r in B7_REGELS if r[0] == g.B7_DEELTOTAAL))


if __name__ == '__main__':
    print('=== BLAD 1 — Weekomzet ===')
    for (dag, *_), t in zip(g.B1, B1_DAGTOTAAL):
        print(f'   {dag:12s} {t:9.2f}')
    print(f'   kolomtotalen B{g.B1_TOTAAL}:D{g.B1_TOTAAL} = {B1_KOLOM}')
    print(f'   eindtotaal   E{g.B1_TOTAAL} = {B1_EINDTOTAAL:.2f}')

    print('\n=== BLAD 2 — Kwekers ===')
    for (naam, *_), t, grp in zip(g.B2, B2_TOTAAL, B2_GROOT):
        print(f'   {naam:24s} {t:6d}  {grp}')
    print(f'   SOM {B2_SOM} | GEM {B2_GEM} | MAX {B2_MAX} | MIN {B2_MIN} | AANTAL {B2_AANTAL}')
    print(f'   grote kwekers (>= {g.B2_GROOT}): {B2_AANTAL_GROOT} van {B2_AANTAL}')

    print(f'\n=== BLAD 3 — Prijsverhoging ({g.B3_PERCENTAGE:.0%}) ===')
    for (art, prijs), v, n in zip(g.B3, B3_VERHOGING, B3_NIEUW):
        print(f'   {art:28s} {prijs:7.2f} + {v:5.2f} = {n:7.2f}')
    print(f'   totalen: {B3_SOM_OUD:.2f} / {B3_SOM_VERHOGING:.2f} / {B3_SOM_NIEUW:.2f}')
    print(f'   controle: {B3_SOM_OUD:.2f} + {B3_SOM_VERHOGING:.2f} = '
          f'{B3_SOM_OUD + B3_SOM_VERHOGING:.2f}')

    print('\n=== BLAD 4 — Bezoekers ===')
    print(f'   SOM {B4_SOM} | GEM {B4_GEM} | MAX {B4_MAX} | MIN {B4_MIN} | AANTAL {B4_AANTAL}')
    print(f'   boven het gemiddelde ({B4_GEM}): {", ".join(B4_BOVEN_GEM)}')
    print(f'   boven {g.B4_DREMPEL} bezoekers: {B4_BOVEN_DREMPEL} maanden')

    print(f'\n=== BLAD 5 — Snoeicursus (grens {g.B5_GRENS}) ===')
    for (naam, punten), res in zip(g.B5, B5_RESULTAAT):
        print(f'   {naam:20s} {punten:3d}  {res}')
    print(f'   geslaagd {B5_GESLAAGD} | niet geslaagd {B5_NIET} | gemiddelde {B5_GEM}')

    print('\n=== BLAD 6 — Leveranciers ===')
    for lev, aantal, bedrag in zip(g.B6_LEVERANCIERS, B6_AANTAL_PER, B6_BEDRAG_PER):
        print(f'   {lev:12s} {aantal:3d} bonnen  {bedrag:9.2f}')
    print(f'   controle: {B6_TOTAAL_PER:.2f} moet gelijk zijn aan {B6_TOTAAL_ALLES:.2f}')

    print('\n=== BLAD 7 — Zaadbestelling ===')
    for code, oms, prijs, aantal, bedrag in B7_REGELS:
        print(f'   {code}  {oms:22s} {prijs:6.2f} x {aantal:4d} = {bedrag:9.2f}')
    print(f'   eindtotaal E{g.B7_TOTAAL} = {B7_EINDTOTAAL:.2f}')
    print(f'   waarvan {g.B7_DEELTOTAAL} = {B7_DEELTOTAAL:.2f}')
