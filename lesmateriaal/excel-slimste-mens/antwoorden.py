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


# --- blad 1: kijkcijfers ----------------------------------------------
B1_RIJTOTAAL = [live + uitg + online for _, live, uitg, online in g.B1]
B1_KOLOM = [sum(rij[i] for rij in g.B1) for i in (1, 2, 3)]
B1_EINDTOTAAL = sum(B1_RIJTOTAAL)

# --- blad 2: de deelnemers --------------------------------------------
B2_FINALIST = ['ja' if ow >= g.B2_FINALIST else 'nee' for _, _, _, ow, _ in g.B2]
B2_AFLEVERINGEN = sum(afl for _, _, afl, _, _ in g.B2)
B2_OVERWINNINGEN = sum(ow for _, _, _, ow, _ in g.B2)
B2_GEM_AFLEVERINGEN = afronden(B2_AFLEVERINGEN / len(g.B2), 1)
B2_MEESTE = max(ow for _, _, _, ow, _ in g.B2)
B2_MINSTE = min(ow for _, _, _, ow, _ in g.B2)
B2_AANTAL = len(g.B2)
B2_AANTAL_FINALIST = B2_FINALIST.count('ja')
B2_OP_DE_GRENS = [naam for naam, _, _, ow, _ in g.B2 if ow == g.B2_FINALIST]
B2_GEM_SECONDEN = sum(s for _, _, _, _, s in g.B2) / len(g.B2)
B2_BOVEN_GEM = [naam for naam, _, _, _, s in g.B2 if s > B2_GEM_SECONDEN]

# --- blad 3: vragen per thema -----------------------------------------
B3_AANTAL_PER = [sum(1 for _, th, _, _ in g.B3 if th == t) for t in g.B3_THEMAS]
B3_SECONDEN_PER = [sum(s for _, th, _, s in g.B3 if th == t) for t in g.B3_THEMAS]
B3_TOTAAL = sum(s for _, _, _, s in g.B3)
B3_TOTAAL_PER = sum(B3_SECONDEN_PER)
B3_VRAGEN = len(g.B3)

# --- blad 4: één aflevering uitgewerkt --------------------------------
B4_REGELS = []
for code, juist in g.B4_REGELS:
    _, naam, per_antwoord = g.zoek_ronde(code)
    B4_REGELS.append((code, naam, per_antwoord, juist, per_antwoord * juist))
B4_JUIST = sum(r[3] for r in B4_REGELS)
B4_SECONDEN = sum(r[4] for r in B4_REGELS)
B4_GEMIDDELDE = afronden(B4_SECONDEN / B4_JUIST, 1)

# --- blad 5: de finaleweek --------------------------------------------
B5_RIJEN = []
for startnr, r1, r2, r3 in g.B5_UITSLAG:
    _, naam = g.zoek_deelnemer(startnr)
    totaal = r1 + r2 + r3
    B5_RIJEN.append((startnr, naam, r1, r2, r3, totaal,
                     'ja' if totaal >= g.B5_DOOR else 'nee'))
B5_AANTAL_DOOR = sum(1 for r in B5_RIJEN if r[6] == 'ja')
B5_GEM_TOTAAL = afronden(sum(r[5] for r in B5_RIJEN) / len(B5_RIJEN), 1)
B5_HOOGSTE = max(r[5] for r in B5_RIJEN)
B5_WINNAAR = next(r[1] for r in B5_RIJEN if r[5] == B5_HOOGSTE)
B5_OP_DE_GRENS = [r[1] for r in B5_RIJEN if r[5] == g.B5_DOOR]


if __name__ == '__main__':
    print('=== BLAD 1 — Kijkcijfers ===')
    for (afl, *_), totaal in zip(g.B1, B1_RIJTOTAAL):
        print(f'   aflevering {afl:2d}  {totaal:>9,}'.replace(',', '.'))
    print(f'   kolomtotalen: {B1_KOLOM}')
    print(f'   EINDTOTAAL E{g.B1_TOTAAL} = {B1_EINDTOTAAL:,}'.replace(',', '.'))

    print('\n=== BLAD 2 — De deelnemers ===')
    for (naam, beroep, afl, ow, sec), fin in zip(g.B2, B2_FINALIST):
        print(f'   {naam:20s} {beroep:16s} {afl:3d} afl  {ow:2d} ow  {sec:4d} sec  {fin}')
    print(f'   afleveringen {B2_AFLEVERINGEN} | overwinningen {B2_OVERWINNINGEN} | '
          f'gemiddeld {B2_GEM_AFLEVERINGEN}')
    print(f'   meeste {B2_MEESTE} | minste {B2_MINSTE} | aantal {B2_AANTAL} | '
          f'finaleweek {B2_AANTAL_FINALIST}')
    print(f'   precies op de grens ({g.B2_FINALIST} overwinningen): '
          f'{", ".join(B2_OP_DE_GRENS)}')

    print('\n=== BLAD 3 — Vragen per thema ===')
    for thema, aantal, sec in zip(g.B3_THEMAS, B3_AANTAL_PER, B3_SECONDEN_PER):
        print(f'   {thema:16s} {aantal:3d} vragen  {sec:4d} seconden')
    print(f'   controle: {B3_TOTAAL_PER} moet gelijk zijn aan {B3_TOTAAL}')
    print(f'   samen {sum(B3_AANTAL_PER)} vragen van de {B3_VRAGEN}')

    print('\n=== BLAD 4 — Eén aflevering ===')
    for code, naam, per, juist, sec in B4_REGELS:
        print(f'   {code}  {naam:22s} {per:3d} x {juist:2d} = {sec:4d}')
    print(f'   juiste antwoorden {B4_JUIST} | gewonnen seconden {B4_SECONDEN}')
    print(f'   gemiddeld per juist antwoord: {B4_GEMIDDELDE}')

    print('\n=== BLAD 5 — De finaleweek ===')
    for startnr, naam, r1, r2, r3, totaal, door in B5_RIJEN:
        print(f'   {startnr}  {naam:20s} {r1:3d} {r2:3d} {r3:3d}  = {totaal:3d}  {door}')
    print(f'   door {B5_AANTAL_DOOR} | gemiddelde {B5_GEM_TOTAAL} | '
          f'hoogste {B5_HOOGSTE} ({B5_WINNAAR})')
    print(f'   precies op de grens ({g.B5_DOOR}): {B5_OP_DE_GRENS or "niemand"}')
