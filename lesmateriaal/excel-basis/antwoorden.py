# -*- coding: utf-8 -*-
"""Rekent alle antwoorden uit, precies zoals Excel het zou doen.
   De lerarenuitleg gebruikt deze cijfers, zodat ze nooit uit elkaar lopen."""
import importlib.util
import os

HIER = os.path.dirname(os.path.abspath(__file__))

from decimal import Decimal, ROUND_HALF_UP

spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven, niet bankiersafronding."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- oefening 1 -------------------------------------------------------
O1_WAARDEN = [afronden(aantal * prijs) for _, _, aantal, prijs in g.O1]
O1_SOM = afronden(sum(O1_WAARDEN))

# --- oefening 2 -------------------------------------------------------
O2_NIEUW = [afronden(prijs * (1 + g.O2_PERCENTAGE)) for _, prijs in g.O2]
O2_VERSCHIL = [afronden(n - p) for n, (_, p) in zip(O2_NIEUW, g.O2)]

# --- oefening 3 -------------------------------------------------------
O3_TOTALEN = [jan + feb + mrt for _, jan, feb, mrt in g.O3]
O3_MAX = max(O3_TOTALEN)
O3_MIN = min(O3_TOTALEN)
O3_GEM = afronden(sum(O3_TOTALEN) / len(O3_TOTALEN))
O3_AANTAL = len(O3_TOTALEN)

# --- oefening 4 -------------------------------------------------------
O4_LEVERING = ['Gratis' if bedrag >= g.O4_DREMPEL else 'Betalend' for _, _, bedrag in g.O4]
O4_AANTAL_GRATIS = O4_LEVERING.count('Gratis')
O4_SOM_GRATIS = afronden(sum(b for (_, _, b), lev in zip(g.O4, O4_LEVERING) if lev == 'Gratis'))

# --- oefening 5 -------------------------------------------------------
O5_ANTWOORD = [(code, *g.zoek(code)[1:]) for code in g.O5_VRAAG]


if __name__ == '__main__':
    print('=== OEFENING 1 — Voorraad ===')
    for (code, oms, aantal, prijs), waarde in zip(g.O1, O1_WAARDEN):
        print(f'   {code:8s} {aantal:5d} x {prijs:6.2f} = {waarde:10.2f}')
    print(f'   TOTAAL (D{g.O1_TOTAAL}) = {O1_SOM:.2f}')

    print('\n=== OEFENING 2 — Prijslijst (+3,5%) ===')
    for (artikel, prijs), nieuw, versch in zip(g.O2, O2_NIEUW, O2_VERSCHIL):
        print(f'   {artikel:24s} {prijs:6.2f} -> {nieuw:6.2f}  (+{versch:.2f})')

    print('\n=== OEFENING 3 — Verkoop ===')
    for (naam, *_), t in zip(g.O3, O3_TOTALEN):
        print(f'   {naam:22s} {t:8d}')
    print(f'   MAX        = {O3_MAX}')
    print(f'   MIN        = {O3_MIN}')
    print(f'   GEMIDDELDE = {O3_GEM}')
    print(f'   AANTAL     = {O3_AANTAL}')

    print(f'\n=== OEFENING 4 — Bestellingen (grens {g.O4_DREMPEL}) ===')
    for (nr, klant, bedrag), lev in zip(g.O4, O4_LEVERING):
        print(f'   {nr}  {bedrag:8.2f}  {lev}')
    print(f'   AANTAL.ALS -> {O4_AANTAL_GRATIS} gratis leveringen')
    print(f'   SOM.ALS    -> {O4_SOM_GRATIS:.2f} euro')

    print('\n=== OEFENING 5 — Klanten ===')
    for code, naam, stad in O5_ANTWOORD:
        print(f'   {code}  {naam:24s} {stad}')
