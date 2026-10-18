# -*- coding: utf-8 -*-
"""Alle uitkomsten van de grafiekbundel.

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
B1_TOESCHOUWERS = {club: toe for club, _stad, toe in g.B1}
B1_HOOGSTE, B1_HOOGSTE_AANTAL = _enige(B1_TOESCHOUWERS, max)
B1_LAAGSTE, B1_LAAGSTE_AANTAL = _enige(B1_TOESCHOUWERS, min)
B1_VERSCHIL = B1_HOOGSTE_AANTAL - B1_LAAGSTE_AANTAL
B1_GESORTEERD = [r[0] for r in g.B1] == [
    c for c, _ in sorted(B1_TOESCHOUWERS.items(), key=lambda kv: -kv[1])]
B1_REEKSEN = 1

# ---------------------------------------------------------------- blad 2
B2_JAREN = [j for j, _ in g.B2]
B2_INWONERS = [i for _, i in g.B2]
B2_GROEI = [None] + [round(B2_INWONERS[i] - B2_INWONERS[i - 1], 1)
                     for i in range(1, len(B2_INWONERS))]
_sprongen = {g.B2[i][0]: v for i, v in enumerate(B2_GROEI) if v is not None}
B2_GROOTSTE_TOT, B2_GROOTSTE = _enige(_sprongen, max)
B2_GROOTSTE_VAN = B2_JAREN[B2_JAREN.index(B2_GROOTSTE_TOT) - 1]
B2_KLEINSTE_TOT, B2_KLEINSTE = _enige(_sprongen, min)
B2_KLEINSTE_VAN = B2_JAREN[B2_JAREN.index(B2_KLEINSTE_TOT) - 1]
B2_LAATSTE_STAP = B2_JAREN[-1] - B2_JAREN[-2]
B2_GEWONE_STAP = B2_JAREN[1] - B2_JAREN[0]

# ---------------------------------------------------------------- blad 3
B3_TOTAAL = sum(w for _, w in g.B3)
B3_AANDEEL = [round(w / B3_TOTAAL, 4) for _, w in g.B3]
B3_GROEP = {naam: w for naam, w in g.B3}
B3_GROOTSTE, B3_GROOTSTE_WAARDE = _enige(B3_GROEP, max)
B3_GROOTSTE_AANDEEL = B3_GROOTSTE_WAARDE / B3_TOTAAL
B3_DELEN = len(g.B3)
B3_BIJ_VEEL_DELEN = 'staafdiagram'

# ---------------------------------------------------------------- blad 4
B4_PER_LAND = {land: [rij[i + 1] for rij in g.B4]
               for i, land in enumerate(g.B4_LANDEN)}
_val2020 = {land: round(B4_PER_LAND[land][1] - B4_PER_LAND[land][0], 1)
            for land in g.B4_LANDEN}
B4_GROOTSTE_VAL, B4_GROOTSTE_VAL_BEDRAG = _enige(_val2020, min)
_laatste = {land: B4_PER_LAND[land][-1] for land in g.B4_LANDEN}
B4_HOOGSTE_LAATST, B4_HOOGSTE_LAATST_AANTAL = _enige(_laatste, max)
B4_REEKSEN = len(g.B4_LANDEN)
B4_VALJAAR = g.B4[1][0]

# ---------------------------------------------------------------- blad 5
B5_CLUB = [g.club(n)[0] for _, n, _ in g.B5]
B5_STAD = [g.club(n)[1] for _, n, _ in g.B5]
_doelpunten = {speler: dp for speler, _n, dp in g.B5}
B5_TOPSCORER, B5_TOPSCORER_DOELPUNTEN = _enige(_doelpunten, max)
B5_TOPSCORER_CLUB = g.club(
    next(n for s, n, _ in g.B5 if s == B5_TOPSCORER))[0]
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

    print('\n--- blad 1  Toeschouwers (staafdiagram) ------------------------')
    print(f'  {len(g.B1)} balken, gesorteerd van groot naar klein: {B1_GESORTEERD}')
    print(f'  langste: {B1_HOOGSTE} ({_getal(B1_HOOGSTE_AANTAL)})   '
          f'kortste: {B1_LAAGSTE} ({_getal(B1_LAAGSTE_AANTAL)})   '
          f'verschil: {_getal(B1_VERSCHIL)}')

    print('\n--- blad 2  Bevolking (lijndiagram) ----------------------------')
    print(_tabel(['Jaar', 'Miljoen', 'Groei'],
                 [[j, m, '' if B2_GROEI[i] is None else f'{B2_GROEI[i]:+g}']
                  for i, (j, m) in enumerate(g.B2)]))
    print(f'\n  grootste sprong: +{B2_GROOTSTE} tussen {B2_GROOTSTE_VAN} en '
          f'{B2_GROOTSTE_TOT}')
    print(f'  kleinste sprong: +{B2_KLEINSTE} tussen {B2_KLEINSTE_VAN} en '
          f'{B2_KLEINSTE_TOT} — maar dat is {B2_LAATSTE_STAP} jaar in plaats van '
          f'{B2_GEWONE_STAP}, dus die vergelijking gaat mank')

    print('\n--- blad 3  Export (cirkeldiagram) -----------------------------')
    print(_tabel(['Productgroep', 'Waarde', 'Aandeel'],
                 [[naam, w, f'{B3_AANDEEL[i]:.0%}']
                  for i, (naam, w) in enumerate(g.B3)]))
    print(f'\n  totaal {B3_TOTAAL}   grootste: {B3_GROOTSTE} '
          f'({B3_GROOTSTE_AANDEEL:.0%})   {B3_DELEN} delen, dus een cirkel mag')

    print('\n--- blad 4  Toerisme (drie reeksen) ----------------------------')
    print(_tabel(['Jaar'] + g.B4_LANDEN, [list(r) for r in g.B4]))
    print(f'\n  grootste terugval in {B4_VALJAAR}: {B4_GROOTSTE_VAL} '
          f'({B4_GROOTSTE_VAL_BEDRAG})   hoogste in {g.B4[-1][0]}: '
          f'{B4_HOOGSTE_LAATST} ({B4_HOOGSTE_LAATST_AANTAL})')

    print('\n--- blad 5  Topscorers (aanvullen, dan grafiek) ----------------')
    print(_tabel(['Speler', 'Code', 'Doelpunten', 'Club', 'Stad'],
                 [[s, g.clubcode(n), dp, B5_CLUB[i], B5_STAD[i]]
                  for i, (s, n, dp) in enumerate(g.B5)]))
    print(f'\n  topscorer: {B5_TOPSCORER} ({B5_TOPSCORER_DOELPUNTEN}) bij '
          f'{B5_TOPSCORER_CLUB}')
    print('\n' + g.WAARSCHUWING)
