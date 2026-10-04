# -*- coding: utf-8 -*-
"""Rekent alle antwoorden uit, precies zoals Excel het zou doen."""
import importlib.util
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


def maal(x, y, n=2):
    """x maal y, afgerond — maar exact gerekend, niet met floats.

    28,50 * 0,15 is in floats 4,2749999... en rondt dan af naar 4,27, terwijl
    het antwoord 4,28 hoort te zijn. Op een toets mag de sleutel daar niet van
    afhangen. controleer.py kijkt bovendien na dat geen enkele prijs in deze
    toets op zo'n dubbel geval valt.
    """
    exact = Decimal(str(x)) * Decimal(str(y))
    return float(exact.quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- blad 1: de selectie ----------------------------------------------
B1_ERVAREN = ['ja' if caps >= g.B1_ERVAREN else 'nee' for _, _, _, caps, _ in g.B1]
B1_CAPS = sum(caps for _, _, _, caps, _ in g.B1)
B1_DOELPUNTEN = sum(d for _, _, _, _, d in g.B1)
B1_LEEFTIJDEN = [leeftijd for _, _, leeftijd, _, _ in g.B1]
B1_GEM_LEEFTIJD = afronden(sum(B1_LEEFTIJDEN) / len(B1_LEEFTIJDEN), 1)
B1_OUDSTE = max(B1_LEEFTIJDEN)
B1_JONGSTE = min(B1_LEEFTIJDEN)
B1_AANTAL = len(g.B1)
B1_AANTAL_ERVAREN = B1_ERVAREN.count('ja')
B1_GEM_CAPS = sum(caps for _, _, _, caps, _ in g.B1) / len(g.B1)
B1_BOVEN_GEM = [naam for (naam, _, _, caps, _) in g.B1 if caps > B1_GEM_CAPS]
B1_OP_DE_GRENS = [naam for (naam, _, _, caps, _) in g.B1 if caps == g.B1_ERVAREN]

# --- blad 2: de wedstrijden -------------------------------------------
B2_SALDO = [voor - tegen for _, _, _, voor, tegen in g.B2]
B2_GEWONNEN = ['ja' if voor > tegen else 'nee' for _, _, _, voor, tegen in g.B2]
B2_VOOR = sum(voor for _, _, _, voor, _ in g.B2)
B2_TEGEN = sum(tegen for _, _, _, _, tegen in g.B2)
B2_SALDO_TOTAAL = sum(B2_SALDO)
B2_AANTAL_GEWONNEN = B2_GEWONNEN.count('ja')
B2_GEM_VOOR = afronden(B2_VOOR / len(g.B2), 3)
B2_MAX_SALDO = max(B2_SALDO)

# --- blad 3: clubdoelpunten -------------------------------------------
B3_AANTAL_PER = [sum(1 for _, pos, _, _ in g.B3 if pos == p) for p in g.POSITIES]
B3_DOELPUNTEN_PER = [sum(d for _, pos, d, _ in g.B3 if pos == p) for p in g.POSITIES]
B3_TOTAAL = sum(d for _, _, d, _ in g.B3)
B3_TOTAAL_PER = sum(B3_DOELPUNTEN_PER)
B3_BOVEN_DREMPEL = [naam for naam, _, d, _ in g.B3 if d >= g.B3_DREMPEL]

# --- blad 4: ticketprijzen --------------------------------------------
B4_KORTING = [maal(prijs, g.B4_KORTING) for _, prijs in g.B4]
B4_ABONNEE = [afronden(prijs - k) for (_, prijs), k in zip(g.B4, B4_KORTING)]
B4_SOM_NORMAAL = afronden(sum(p for _, p in g.B4))
B4_SOM_KORTING = afronden(sum(B4_KORTING))
B4_SOM_ABONNEE = afronden(sum(B4_ABONNEE))

# --- blad 5: het wedstrijdblad ----------------------------------------
B5_BASIS = []
for rugnummer, minuten in g.B5_BASIS:
    _, speler, positie = g.zoek(rugnummer)
    B5_BASIS.append((rugnummer, speler, positie, minuten))
B5_MINUTEN = sum(m for _, _, _, m in B5_BASIS)
B5_AANTAL_TELLEN = sum(1 for _, _, pos, _ in B5_BASIS if pos == g.B5_TELLEN)
B5_GEM_MINUTEN = afronden(B5_MINUTEN / len(B5_BASIS), 3)


if __name__ == '__main__':
    print('=== BLAD 1 — De selectie ===')
    for (naam, pos, leeftijd, caps, doelpunten), ervaren in zip(g.B1, B1_ERVAREN):
        print(f'   {naam:24s} {pos:14s} {leeftijd:3d} jaar  {caps:4d} caps  '
              f'{doelpunten:3d} dp   {ervaren}')
    print(f'   caps {B1_CAPS} | doelpunten {B1_DOELPUNTEN} | gem. leeftijd {B1_GEM_LEEFTIJD}')
    print(f'   oudste {B1_OUDSTE} | jongste {B1_JONGSTE} | aantal {B1_AANTAL} | '
          f'ervaren {B1_AANTAL_ERVAREN}')
    print(f'   precies op de grens ({g.B1_ERVAREN} caps): {", ".join(B1_OP_DE_GRENS)}')
    print(f'   boven het gemiddelde ({B1_GEM_CAPS:.1f} caps): {len(B1_BOVEN_GEM)} spelers')

    print('\n=== BLAD 2 — De wedstrijden ===')
    for (datum, tegen, waar, voor, tegen_n), saldo, gew in zip(g.B2, B2_SALDO, B2_GEWONNEN):
        print(f'   {datum}  {tegen:12s} {waar:5s} {voor}-{tegen_n}  saldo {saldo:+d}  {gew}')
    print(f'   totalen: voor {B2_VOOR} / tegen {B2_TEGEN} / saldo {B2_SALDO_TOTAAL}')
    print(f'   gewonnen {B2_AANTAL_GEWONNEN} | gemiddeld voor {B2_GEM_VOOR} | '
          f'grootste saldo {B2_MAX_SALDO}')
    print(f'   controle: {B2_VOOR} - {B2_TEGEN} = {B2_VOOR - B2_TEGEN}')

    print('\n=== BLAD 3 — Clubdoelpunten ===')
    for positie, aantal, doelpunten in zip(g.POSITIES, B3_AANTAL_PER, B3_DOELPUNTEN_PER):
        print(f'   {positie:14s} {aantal:3d} spelers  {doelpunten:4d} doelpunten')
    print(f'   controle: {B3_TOTAAL_PER} moet gelijk zijn aan {B3_TOTAAL}')
    print(f'   vanaf {g.B3_DREMPEL} doelpunten kleuren: {", ".join(B3_BOVEN_DREMPEL)}')

    print(f'\n=== BLAD 4 — Ticketprijzen (korting {g.B4_KORTING:.0%}) ===')
    for (vak, prijs), korting, abonnee in zip(g.B4, B4_KORTING, B4_ABONNEE):
        print(f'   {vak:24s} {prijs:7.2f} - {korting:6.2f} = {abonnee:7.2f}')
    print(f'   totalen: {B4_SOM_NORMAAL:.2f} / {B4_SOM_KORTING:.2f} / {B4_SOM_ABONNEE:.2f}')
    print(f'   controle: {B4_SOM_NORMAAL:.2f} - {B4_SOM_KORTING:.2f} = '
          f'{B4_SOM_NORMAAL - B4_SOM_KORTING:.2f}')

    print('\n=== BLAD 5 — Het wedstrijdblad ===')
    for rugnummer, speler, positie, minuten in B5_BASIS:
        print(f'   {rugnummer:3d}  {speler:24s} {positie:14s} {minuten:3d} min')
    print(f'   totaal {B5_MINUTEN} minuten | {g.B5_TELLEN.lower()}s in de basis '
          f'{B5_AANTAL_TELLEN} | gemiddeld {B5_GEM_MINUTEN}')
