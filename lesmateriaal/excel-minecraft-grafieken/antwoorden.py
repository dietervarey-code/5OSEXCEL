# -*- coding: utf-8 -*-
"""Alle uitkomsten van de Minecraft-grafiekbundel.

Een grafiek kan openpyxl wel schrijven, maar het startbestand bevat er geen:
de leerling hoort ze zelf te maken. Deze module rekent uit wat er in de
hulpkolommen hoort te staan en wat de grafiek moet laten zien, zodat de
sleutel het ernaast kan leggen.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(_s); _s.loader.exec_module(g)


def _enige(waarden, kies):
    """De uitschieter, met een harde controle dat er maar één is."""
    beste = kies(waarden.values())
    winnaars = [k for k, v in waarden.items() if v == beste]
    assert len(winnaars) == 1, f'gedeelde uitschieter: {winnaars}'
    return winnaars[0], beste


# ---------------------------------------------------------------- blad 1
B1_LEVENSPUNTEN = {mob: lp for mob, _dim, lp in g.B1}
B1_HOOGSTE, B1_HOOGSTE_AANTAL = _enige(B1_LEVENSPUNTEN, max)
B1_LAAGSTE, B1_LAAGSTE_AANTAL = _enige(B1_LEVENSPUNTEN, min)
B1_VERSCHIL = B1_HOOGSTE_AANTAL - B1_LAAGSTE_AANTAL
B1_VERHOUDING = B1_HOOGSTE_AANTAL / B1_LAAGSTE_AANTAL
B1_GESORTEERD = [r[0] for r in g.B1] == [
    m for m, _ in sorted(B1_LEVENSPUNTEN.items(), key=lambda kv: -kv[1])]
B1_REEKSEN = 1

# ---------------------------------------------------------------- blad 2
B2_NIVEAUS = [y for y, _ in g.B2]
B2_DIAMANTEN = [d for _, d in g.B2]
B2_VERSCHIL = [None] + [B2_DIAMANTEN[i] - B2_DIAMANTEN[i - 1]
                        for i in range(1, len(B2_DIAMANTEN))]
_sprongen = {g.B2[i][0]: v for i, v in enumerate(B2_VERSCHIL) if v is not None}
B2_GROOTSTE_TOT, B2_GROOTSTE = _enige(_sprongen, max)
B2_GROOTSTE_VAN = B2_NIVEAUS[B2_NIVEAUS.index(B2_GROOTSTE_TOT) - 1]
B2_KLEINSTE_TOT, B2_KLEINSTE = _enige(_sprongen, min)
B2_KLEINSTE_VAN = B2_NIVEAUS[B2_NIVEAUS.index(B2_KLEINSTE_TOT) - 1]
B2_LAATSTE_STAP = abs(B2_NIVEAUS[-1] - B2_NIVEAUS[-2])
B2_GEWONE_STAP = abs(B2_NIVEAUS[1] - B2_NIVEAUS[0])
B2_SOM_VERSCHIL = B2_DIAMANTEN[-1] - B2_DIAMANTEN[0]
B2_PIEK, B2_PIEK_AANTAL = _enige(dict(g.B2), max)

# ---------------------------------------------------------------- blad 3
B3_TOTAAL = sum(w for _, w in g.B3)
B3_AANDEEL = [round(w / B3_TOTAAL, 4) for _, w in g.B3]
B3_SOORT = {naam: w for naam, w in g.B3}
B3_GROOTSTE, B3_GROOTSTE_WAARDE = _enige(B3_SOORT, max)
B3_GROOTSTE_AANDEEL = B3_GROOTSTE_WAARDE / B3_TOTAAL
B3_DELEN = len(g.B3)
B3_BIJ_VEEL_DELEN = 'staafdiagram'

# ---------------------------------------------------------------- blad 4
B4_PER_WAPEN = {wapen: [rij[i + 1] for rij in g.B4]
                for i, wapen in enumerate(g.B4_WAPENS)}
_winst = {wapen: B4_PER_WAPEN[wapen][-1] - B4_PER_WAPEN[wapen][0]
          for wapen in g.B4_WAPENS}
B4_MEESTE_WINST, B4_MEESTE_WINST_SCHADE = _enige(_winst, max)
_beste = {wapen: B4_PER_WAPEN[wapen][-1] for wapen in g.B4_WAPENS}
B4_HOOGSTE_LAATST, B4_HOOGSTE_LAATST_SCHADE = _enige(_beste, max)
B4_VLAK = [wapen for wapen in g.B4_WAPENS if len(set(B4_PER_WAPEN[wapen])) == 1]
B4_REEKSEN = len(g.B4_WAPENS)
B4_BESTE_MATERIAAL = g.B4[-1][0]

# ---------------------------------------------------------------- blad 5
B5_BEROEP = [g.beroep(n)[0] for _, n, _ in g.B5]
B5_WERKBLOK = [g.beroep(n)[1] for _, n, _ in g.B5]
_prijzen = {item: prijs for item, _n, prijs in g.B5}
B5_DUURSTE, B5_DUURSTE_PRIJS = _enige(_prijzen, max)
B5_GOEDKOOPSTE, B5_GOEDKOOPSTE_PRIJS = _enige(_prijzen, min)
B5_DUURSTE_BEROEP = g.beroep(
    next(n for item, n, _ in g.B5 if item == B5_DUURSTE))[0]
B5_REEKSEN = 1


def _getal(x):
    if isinstance(x, float) and x == int(x):
        x = int(x)
    if isinstance(x, int):
        return f'{x:,}'.replace(',', '.')
    return f'{x:.2f}'.rstrip('0').rstrip('.').replace('.', ',')


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


if __name__ == '__main__':
    print('=' * 74); print(g.TITEL); print('=' * 74)

    print('\n--- blad 1  Levenspunten (staafdiagram) ------------------------')
    print(f'  {len(g.B1)} balken, gesorteerd van hoog naar laag: {B1_GESORTEERD}')
    print(f'  langste: {B1_HOOGSTE} ({B1_HOOGSTE_AANTAL})   '
          f'kortste: {B1_LAAGSTE} ({B1_LAAGSTE_AANTAL})   '
          f'verschil: {B1_VERSCHIL}   verhouding: {B1_VERHOUDING:.1f} keer')

    print('\n--- blad 2  Diamanten per diepte (lijndiagram) -----------------')
    print(_tabel(['Y-niveau', 'Diamanten', 'Verschil'],
                 [[y, d, '' if B2_VERSCHIL[i] is None else f'{B2_VERSCHIL[i]:+d}']
                  for i, (y, d) in enumerate(g.B2)]))
    print(f'\n  grootste sprong: {B2_GROOTSTE:+d} tussen Y = {B2_GROOTSTE_VAN} en '
          f'Y = {B2_GROOTSTE_TOT}')
    print(f'  grootste val: {B2_KLEINSTE:+d} tussen Y = {B2_KLEINSTE_VAN} en '
          f'Y = {B2_KLEINSTE_TOT} — daar begint het grondgesteente')
    print(f'  piek bij Y = {B2_PIEK} ({B2_PIEK_AANTAL})   '
          f'som van de verschilkolom: {B2_SOM_VERSCHIL}')
    print(f'  let op: onderaan zitten er {B2_LAATSTE_STAP} niveaus tussen twee '
          f'metingen, bovenaan {B2_GEWONE_STAP}')

    print('\n--- blad 3  Ertsvondsten (cirkeldiagram) -----------------------')
    print(_tabel(['Erts', 'Gevonden', 'Aandeel'],
                 [[naam, w, f'{B3_AANDEEL[i]:.0%}']
                  for i, (naam, w) in enumerate(g.B3)]))
    print(f'\n  totaal {B3_TOTAAL}   grootste: {B3_GROOTSTE} '
          f'({B3_GROOTSTE_AANDEEL:.0%})   {B3_DELEN} delen, dus een cirkel mag')

    print('\n--- blad 4  Schade per slag (drie reeksen) ---------------------')
    print(_tabel(['Materiaal'] + g.B4_WAPENS, [list(r) for r in g.B4]))
    print(f'\n  wint het meest van {g.B4[0][0]} naar {B4_BESTE_MATERIAAL}: '
          f'{B4_MEESTE_WINST} (+{B4_MEESTE_WINST_SCHADE})   '
          f'hoogste bij {B4_BESTE_MATERIAAL}: {B4_HOOGSTE_LAATST} '
          f'({B4_HOOGSTE_LAATST_SCHADE})')
    print(f'  vlakke reeks: {", ".join(B4_VLAK)} — overal hetzelfde, wat je '
          'materiaal ook is')

    print('\n--- blad 5  Dorpelingenhandel (aanvullen, dan grafiek) ---------')
    print(_tabel(['Item', 'Code', 'Prijs', 'Beroep', 'Werkblok'],
                 [[item, g.beroepcode(n), prijs, B5_BEROEP[i], B5_WERKBLOK[i]]
                  for i, (item, n, prijs) in enumerate(g.B5)]))
    print(f'\n  duurste: {B5_DUURSTE} ({B5_DUURSTE_PRIJS}) bij de '
          f'{B5_DUURSTE_BEROEP.lower()}   goedkoopste: {B5_GOEDKOOPSTE} '
          f'({B5_GOEDKOOPSTE_PRIJS})')
    print('\n' + g.WAARSCHUWING)
