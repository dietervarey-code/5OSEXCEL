# -*- coding: utf-8 -*-
"""Rekent alle antwoorden uit, precies zoals Excel het zou doen.
   De lerarenuitleg gebruikt deze cijfers, zodat ze nooit uit elkaar lopen."""
import importlib.util
import os
from decimal import Decimal, ROUND_HALF_UP

HIER = os.path.dirname(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven, niet bankiersafronding."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- oefening 1 -------------------------------------------------------
O1_WAARDEN = [afronden(aantal * prijs) for _, _, aantal, prijs in g.O1]
O1_SOM = afronden(sum(O1_WAARDEN))
O1_STUKS = sum(aantal for _, _, aantal, _ in g.O1)

# --- oefening 2 -------------------------------------------------------
O2_NIEUW = [afronden(prijs * (1 + g.O2_PERCENTAGE)) for _, prijs in g.O2]
O2_VERSCHIL = [afronden(n - p) for n, (_, p) in zip(O2_NIEUW, g.O2)]
# Het verschil in procent: verschil gedeeld door de oude prijs.
O2_PROCENT = [v / p for v, (_, p) in zip(O2_VERSCHIL, g.O2)]

# --- oefening 3 -------------------------------------------------------
O3_TOTALEN = [jan + feb + mrt for _, jan, feb, mrt in g.O3]
O3_PER_MAAND = [sum(rij[i] for rij in g.O3) for i in (1, 2, 3)]
O3_EINDTOTAAL = sum(O3_TOTALEN)
O3_MAX = max(O3_TOTALEN)
O3_MIN = min(O3_TOTALEN)
O3_GEM = afronden(sum(O3_TOTALEN) / len(O3_TOTALEN))
O3_AANTAL = len(O3_TOTALEN)

# --- oefening 4 -------------------------------------------------------
O4_LEVERING = ['Gratis' if bedrag >= g.O4_DREMPEL else 'Betalend' for _, _, bedrag in g.O4]
O4_AANTAL_GRATIS = O4_LEVERING.count('Gratis')
O4_AANTAL_BETALEND = O4_LEVERING.count('Betalend')
O4_SOM_GRATIS = afronden(sum(b for (_, _, b), lev in zip(g.O4, O4_LEVERING) if lev == 'Gratis'))
O4_SOM_BETALEND = afronden(sum(b for (_, _, b), lev in zip(g.O4, O4_LEVERING) if lev == 'Betalend'))
O4_SOM_ALLES = afronden(sum(b for _, _, b in g.O4))

# --- oefening 5 -------------------------------------------------------
# De code die niet bestaat geeft #N/B. Dat is geen fout van de leerling.
O5_ANTWOORD = []
for code in g.O5_VRAAG:
    rij = g.zoek(code)
    O5_ANTWOORD.append((code, rij[1], rij[2]) if rij else (code, '#N/B', '#N/B'))


if __name__ == '__main__':
    print('=== OEFENING 1 — Voorraad ===')
    for (code, _, aantal, prijs), waarde in zip(g.O1, O1_WAARDEN):
        print(f'   {code:8s} {aantal:5d} x {prijs:6.2f} = {waarde:10.2f}')
    print(f'   C{g.O1_TOTAAL} totaal stuks  = {O1_STUKS}')
    print(f'   E{g.O1_TOTAAL} totale waarde = {O1_SOM:.2f}')

    print(f'\n=== OEFENING 2 — Prijslijst (+{g.O2_PERCENTAGE:.1%}) ===')
    for (artikel, prijs), nieuw, versch, proc in zip(g.O2, O2_NIEUW, O2_VERSCHIL, O2_PROCENT):
        print(f'   {artikel:24s} {prijs:6.2f} -> {nieuw:6.2f}  (+{versch:5.2f}  {proc:6.2%})')

    print('\n=== OEFENING 3 — Verkoop ===')
    for (naam, *_), t in zip(g.O3, O3_TOTALEN):
        print(f'   {naam:22s} {t:8d}')
    print(f'   maandtotalen B{g.O3_MAANDTOTAAL}:D{g.O3_MAANDTOTAAL} = {O3_PER_MAAND}')
    print(f'   eindtotaal   E{g.O3_MAANDTOTAAL} = {O3_EINDTOTAAL}')
    print(f'   MAX = {O3_MAX} | MIN = {O3_MIN} | GEMIDDELDE = {O3_GEM} | AANTAL = {O3_AANTAL}')

    print(f'\n=== OEFENING 4 — Bestellingen (grens {g.O4_DREMPEL}) ===')
    for (nr, _, bedrag), lev in zip(g.O4, O4_LEVERING):
        print(f'   {nr}  {bedrag:8.2f}  {lev}')
    print(f'   gratis:   {O4_AANTAL_GRATIS} stuks, {O4_SOM_GRATIS:.2f} euro')
    print(f'   betalend: {O4_AANTAL_BETALEND} stuks, {O4_SOM_BETALEND:.2f} euro')
    print(f'   controle: samen {O4_SOM_GRATIS + O4_SOM_BETALEND:.2f} = {O4_SOM_ALLES:.2f}')

    print('\n=== OEFENING 5 — Klanten ===')
    for code, naam, stad in O5_ANTWOORD:
        merk = '   <- bestaat niet' if naam == '#N/B' else ''
        print(f'   {code}  {naam:24s} {stad}{merk}')
