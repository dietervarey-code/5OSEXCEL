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


# --- blad 1: dagontvangsten -------------------------------------------
B1_DAGTOTAAL = [afronden(c + b + o) for _, c, b, o in g.B1]
B1_KOLOM = [afronden(sum(rij[i] for rij in g.B1)) for i in (1, 2, 3)]
B1_EINDTOTAAL = afronden(sum(B1_DAGTOTAAL))

# --- blad 2: werkuren --------------------------------------------------
B2_TOTAAL = [afronden(w1 + w2 + w3, 1) for _, w1, w2, w3 in g.B2]
B2_SOM = afronden(sum(B2_TOTAAL), 1)
B2_GEM = afronden(sum(B2_TOTAAL) / len(B2_TOTAAL), 1)
B2_MAX = max(B2_TOTAAL)
B2_MIN = min(B2_TOTAAL)
B2_AANTAL = len(B2_TOTAAL)
B2_VOLTIJDS = ['ja' if t >= g.B2_VOLTIJDS else 'nee' for t in B2_TOTAAL]
B2_AANTAL_VOLTIJDS = B2_VOLTIJDS.count('ja')

# --- blad 3: kortingen -------------------------------------------------
B3_KORTING = [afronden(prijs * g.B3_PERCENTAGE) for _, prijs in g.B3]
B3_NIEUW = [afronden(prijs - k) for (_, prijs), k in zip(g.B3, B3_KORTING)]
B3_SOM_PRIJS = afronden(sum(p for _, p in g.B3))
B3_SOM_KORTING = afronden(sum(B3_KORTING))
B3_SOM_NIEUW = afronden(sum(B3_NIEUW))

# --- blad 4: verbruik --------------------------------------------------
B4_WAARDEN = [v for _, v in g.B4]
B4_SOM = sum(B4_WAARDEN)
B4_GEM = afronden(sum(B4_WAARDEN) / len(B4_WAARDEN))
B4_MAX = max(B4_WAARDEN)
B4_MIN = min(B4_WAARDEN)
B4_AANTAL = len(B4_WAARDEN)
B4_BOVEN_GEM = [m for m, v in g.B4 if v > B4_GEM]
B4_BOVEN_DREMPEL = sum(1 for v in B4_WAARDEN if v > g.B4_DREMPEL)

# --- blad 5: inschrijvingen --------------------------------------------
B5_CATEGORIE = ['Volwassene' if leeftijd >= g.B5_GRENS else 'Jeugd' for _, leeftijd in g.B5]
B5_VOLWASSEN = B5_CATEGORIE.count('Volwassene')
B5_JEUGD = B5_CATEGORIE.count('Jeugd')
B5_GEM_LEEFTIJD = afronden(sum(l for _, l in g.B5) / len(g.B5), 1)
B5_AANTAL = len(g.B5)

# --- blad 6: verkoop per afdeling --------------------------------------
B6_AANTAL_PER = [sum(1 for _, a, _ in g.B6 if a == afd) for afd in g.B6_AFDELINGEN]
B6_BEDRAG_PER = [afronden(sum(b for _, a, b in g.B6 if a == afd)) for afd in g.B6_AFDELINGEN]
B6_TOTAAL_ALLES = afronden(sum(b for _, _, b in g.B6))
B6_TOTAAL_PER = afronden(sum(B6_BEDRAG_PER))

# --- blad 7: materiaalcodes --------------------------------------------
B7_REGELS = []
for code, aantal in g.B7_REGELS:
    _, oms, prijs = g.zoek(code)
    B7_REGELS.append((code, oms, prijs, aantal, afronden(prijs * aantal)))
B7_EINDTOTAAL = afronden(sum(r[4] for r in B7_REGELS))
B7_CEMENT = afronden(sum(r[4] for r in B7_REGELS if r[0] == 'M-01'))


if __name__ == '__main__':
    print('=== BLAD 1 — Dagontvangsten ===')
    for (dag, *_), t in zip(g.B1, B1_DAGTOTAAL):
        print(f'   {dag:12s} {t:9.2f}')
    print(f'   kolomtotalen B{g.B1_TOTAAL}:D{g.B1_TOTAAL} = {B1_KOLOM}')
    print(f'   eindtotaal   E{g.B1_TOTAAL} = {B1_EINDTOTAAL:.2f}')

    print('\n=== BLAD 2 — Werkuren ===')
    for (naam, *_), t in zip(g.B2, B2_TOTAAL):
        print(f'   {naam:22s} {t:6.1f}')
    print(f'   SOM {B2_SOM} | GEM {B2_GEM} | MAX {B2_MAX} | MIN {B2_MIN} | AANTAL {B2_AANTAL}')
    print(f'   voltijds (>= {g.B2_VOLTIJDS} u): {B2_AANTAL_VOLTIJDS} van {B2_AANTAL}')

    print(f'\n=== BLAD 3 — Kortingen ({g.B3_PERCENTAGE:.0%}) ===')
    for (art, prijs), k, n in zip(g.B3, B3_KORTING, B3_NIEUW):
        print(f'   {art:24s} {prijs:7.2f} - {k:6.2f} = {n:7.2f}')
    print(f'   totalen: {B3_SOM_PRIJS:.2f} / {B3_SOM_KORTING:.2f} / {B3_SOM_NIEUW:.2f}')
    print(f'   controle: {B3_SOM_PRIJS:.2f} - {B3_SOM_KORTING:.2f} = '
          f'{B3_SOM_PRIJS - B3_SOM_KORTING:.2f}')

    print('\n=== BLAD 4 — Verbruik ===')
    print(f'   SOM {B4_SOM} | GEM {B4_GEM} | MAX {B4_MAX} | MIN {B4_MIN} | AANTAL {B4_AANTAL}')
    print(f'   boven het gemiddelde ({B4_GEM}): {", ".join(B4_BOVEN_GEM)}')
    print(f'   boven {g.B4_DREMPEL} kWh: {B4_BOVEN_DREMPEL} maanden')

    print(f'\n=== BLAD 5 — Inschrijvingen (grens {g.B5_GRENS}) ===')
    for (naam, leeftijd), cat in zip(g.B5, B5_CATEGORIE):
        print(f'   {naam:20s} {leeftijd:3d}  {cat}')
    print(f'   volwassenen {B5_VOLWASSEN} | jeugd {B5_JEUGD} | '
          f'gemiddelde leeftijd {B5_GEM_LEEFTIJD}')

    print('\n=== BLAD 6 — Verkoop per afdeling ===')
    for afd, aantal, bedrag in zip(g.B6_AFDELINGEN, B6_AANTAL_PER, B6_BEDRAG_PER):
        print(f'   {afd:10s} {aantal:3d} bonnen  {bedrag:9.2f}')
    print(f'   controle: {B6_TOTAAL_PER:.2f} moet gelijk zijn aan {B6_TOTAAL_ALLES:.2f}')

    print('\n=== BLAD 7 — Materiaalcodes ===')
    for code, oms, prijs, aantal, bedrag in B7_REGELS:
        print(f'   {code}  {oms:20s} {prijs:6.2f} x {aantal:4d} = {bedrag:9.2f}')
    print(f'   eindtotaal E{g.B7_TOTAAL} = {B7_EINDTOTAAL:.2f}')
    print(f'   waarvan cement (M-01) = {B7_CEMENT:.2f}')
