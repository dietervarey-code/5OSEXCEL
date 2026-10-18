# -*- coding: utf-8 -*-
"""Alle uitkomsten van de draaitabelbundel, draaitabel per draaitabel.

openpyxl kan geen draaitabel schrijven; Excel bouwt die zelf. Daarom rekent
deze module precies uit WAT erin hoort te staan, zodat de sleutel het als
tabel kan afdrukken en je het blad van een leerling ernaast kan leggen.
"""
import collections
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(_s); _s.loader.exec_module(g)


def _telling(paren):
    """[(rij, kolom), ...] -> kruistabel met rand- en eindtotalen."""
    rijen = sorted({r for r, _ in paren})
    kollen = sorted({k for _, k in paren})
    tel = collections.Counter(paren)
    cel = {(r, k): tel.get((r, k), 0) for r in rijen for k in kollen}
    rijtotaal = {r: sum(cel[(r, k)] for k in kollen) for r in rijen}
    koltotaal = {k: sum(cel[(r, k)] for r in rijen) for k in kollen}
    return rijen, kollen, cel, rijtotaal, koltotaal, sum(rijtotaal.values())


def _top(d):
    """De sleutel met de hoogste waarde. Faalt luid bij een gedeelde eerste plaats."""
    beste = max(d.values())
    winnaars = [k for k, v in d.items() if v == beste]
    assert len(winnaars) == 1, f'gedeelde eerste plaats: {winnaars}'
    return winnaars[0], beste


# ---------------------------------------------------------------- blad 1
D1 = dict(collections.Counter(r[2] for r in g.B1))
D1_LABELS = sorted(D1)
D1_TOTAAL = sum(D1.values())
D1_TOP, D1_TOP_AANTAL = _top(D1)
D1_MINST = min(D1, key=lambda k: (D1[k], k))

# ---------------------------------------------------------------- blad 2
D2_RIJEN, D2_KOLLEN, D2_CEL, D2_RIJTOT, D2_KOLTOT, D2_TOTAAL = _telling(
    [(r[1], r[3]) for r in g.B2])
_pittig = {r: D2_CEL[(r, 'ja')] for r in D2_RIJEN}
D2_TOP_PITTIG, D2_TOP_PITTIG_AANTAL = _top(_pittig)
D2_NAGERECHT_NIET = D2_CEL[('Nagerecht', 'nee')]
D2_ZONDER_PITTIG = [r for r in D2_RIJEN if D2_CEL[(r, 'ja')] == 0]

# ---------------------------------------------------------------- blad 3
_inw = collections.defaultdict(int)
for _, regio, inwoners, _, _ in g.B3:
    _inw[regio] += inwoners
D3 = dict(_inw)
D3_AFLOPEND = sorted(D3, key=lambda r: (-D3[r], r))
D3_TOTAAL = sum(D3.values())
D3_TOP, D3_TOP_INWONERS = _top(D3)
D3_LAAGSTE = D3_AFLOPEND[-1]
D3_AANDEEL_TOP = D3_TOP_INWONERS / D3_TOTAAL

# ---------------------------------------------------------------- blad 4
_per_tien = collections.defaultdict(list)
for serie, genre, jaar, seizoenen, afl, kijkers in g.B4:
    _per_tien[g.decennium(jaar)].append(kijkers)
D4_LABELS = sorted(_per_tien)
D4_AANTAL = {d: len(v) for d, v in _per_tien.items()}
D4_GEMIDDELD = {d: sum(v) / len(v) for d, v in _per_tien.items()}
D4_TOTAAL_AANTAL = sum(D4_AANTAL.values())
D4_TOTAAL_GEMIDDELD = sum(r[5] for r in g.B4) / len(g.B4)
D4_DRUKSTE, D4_DRUKSTE_AANTAL = _top(D4_AANTAL)
D4_HOOGSTE_GEM, D4_HOOGSTE_GEM_WAARDE = _top(D4_GEMIDDELD)
D4_FILTER_GENRE = 'Historisch'
D4_FILTER_AANTAL = sum(1 for r in g.B4 if r[1] == D4_FILTER_GENRE)

# ---------------------------------------------------------------- blad 5
B5_CLUB = [g.club(n)[0] for _, _, n, _ in g.B5]
B5_STAD = [g.club(n)[1] for _, _, n, _ in g.B5]
B5_REGIO = [g.club(n)[2] for _, _, n, _ in g.B5]
_bedrag = collections.defaultdict(float)
for (_, _, n, bedrag) in g.B5:
    _bedrag[g.club(n)[2]] += bedrag
D5 = {k: round(v, 2) for k, v in _bedrag.items()}
D5_AFLOPEND = sorted(D5, key=lambda r: (-D5[r], r))
D5_TOTAAL = round(sum(D5.values()), 2)
D5_TOP, D5_TOP_BEDRAG = _top(D5)

# na de extra rij die ze er zelf bij typen (kaart 9)
_extra_regio = g.club(g.B5_EXTRA[2])[2]
D5_NA = dict(D5)
D5_NA[_extra_regio] = round(D5_NA[_extra_regio] + g.B5_EXTRA[3], 2)
D5_NA_TOTAAL = round(D5_TOTAAL + g.B5_EXTRA[3], 2)
D5_EXTRA_CLUB = g.club(g.B5_EXTRA[2])[0]


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

    print('\n--- blad 1  Süper Lig: aantal clubs per regio -------------------')
    print(_tabel(['Regio', 'Aantal clubs'],
                 [[r, D1[r]] for r in D1_LABELS] + [['Eindtotaal', D1_TOTAAL]]))
    print(f'\n  meeste clubs: {D1_TOP} ({D1_TOP_AANTAL})   minste: {D1_MINST}')

    print('\n--- blad 2  Keuken: soort tegenover pittig ----------------------')
    print(_tabel(['Soort'] + D2_KOLLEN + ['Eindtotaal'],
                 [[r] + [D2_CEL[(r, k)] or '' for k in D2_KOLLEN] + [D2_RIJTOT[r]]
                  for r in D2_RIJEN]
                 + [['Eindtotaal'] + [D2_KOLTOT[k] for k in D2_KOLLEN]
                    + [D2_TOTAAL]]))
    print(f'\n  meeste pittige: {D2_TOP_PITTIG} ({D2_TOP_PITTIG_AANTAL})   '
          f'niet-pittige nagerechten: {D2_NAGERECHT_NIET}   '
          f'geen enkel pittig gerecht: {", ".join(D2_ZONDER_PITTIG)}')

    print('\n--- blad 3  Provincies: inwoners per regio ----------------------')
    print(_tabel(['Regio', 'Inwoners'],
                 [[r, _getal(D3[r])] for r in D3_AFLOPEND]
                 + [['Eindtotaal', _getal(D3_TOTAAL)]]))
    print(f'\n  grootste: {D3_TOP} met {_getal(D3_TOP_INWONERS)} '
          f'({D3_AANDEEL_TOP:.1%} van het totaal)   kleinste: {D3_LAAGSTE}')

    print('\n--- blad 4  Series: per decennium -------------------------------')
    print(_tabel(['Decennium', 'Aantal series', 'Gemiddeld aantal kijkers'],
                 [[d, D4_AANTAL[d], _getal(D4_GEMIDDELD[d])] for d in D4_LABELS]
                 + [['Eindtotaal', D4_TOTAAL_AANTAL, _getal(D4_TOTAAL_GEMIDDELD)]]))
    print(f'\n  drukste decennium: {D4_DRUKSTE} ({D4_DRUKSTE_AANTAL} series)   '
          f'hoogste gemiddelde: {D4_HOOGSTE_GEM} '
          f'({_getal(D4_HOOGSTE_GEM_WAARDE)}, uit maar '
          f'{D4_AANTAL[D4_HOOGSTE_GEM]} series)')
    print(f'  met filter {D4_FILTER_GENRE}: {D4_FILTER_AANTAL} series')

    print('\n--- blad 5  Transfers: bedrag per regio -------------------------')
    print(_tabel(['Regio', 'Bedrag (milj.)', 'Na de extra transfer'],
                 [[r, _getal(D5[r]), _getal(D5_NA[r])] for r in D5_AFLOPEND]
                 + [['Eindtotaal', _getal(D5_TOTAAL), _getal(D5_NA_TOTAAL)]]))
    print(f'\n  grootste: {D5_TOP} ({_getal(D5_TOP_BEDRAG)})   '
          f'de extra transfer gaat naar {D5_EXTRA_CLUB} ({_extra_regio})')
    print('\n' + g.WAARSCHUWING)
