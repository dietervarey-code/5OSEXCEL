# -*- coding: utf-8 -*-
"""Alle uitkomsten van de streamingbundel, inclusief de twee draaitabellen.

Een draaitabel kan openpyxl niet schrijven — Excel bouwt die zelf. Daarom
rekenen we hier precies uit WAT erin hoort te staan, zodat de sleutel het als
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


# ---------------------------------------------------------------- blad 1
B1_GROEI = [g.groei(c) for c, *_ in g.B1]
B1_STERK = ['ja' if x >= g.B1_DREMPEL else 'nee' for x in B1_GROEI]
B1_SOM = sum(B1_GROEI)                                    # 108
B1_GEMIDDELDE = B1_SOM / len(B1_GROEI)                    # 12
B1_MAX = max(B1_GROEI)                                    # 25
B1_MIN = min(B1_GROEI)                                    # -2
B1_AANTAL = len(g.B1)                                     # 9
B1_STERKE = B1_STERK.count('ja')                          # 5
B1_SNELST = g.B1[B1_GROEI.index(B1_MAX)][1]               # Thriller
B1_TRAAGST = g.B1[B1_GROEI.index(B1_MIN)][1]              # Avontuur
B1_GRENSGEVAL = [n for i, (_, n, _, _) in enumerate(g.B1)
                 if B1_GROEI[i] == g.B1_DREMPEL]          # precies op de grens

# ---------------------------------------------------------------- blad 2
B2_GENRE = [g.genre(r[2])[1] for r in g.B2]
B2_GROEI = [g.groei(r[2]) for r in g.B2]
B2_STERK = ['ja' if x >= g.B1_DREMPEL else 'nee' for x in B2_GROEI]
B2_AANTAL = len(g.B2)                                     # 35
B2_GEMIDDELD = sum(r[5] for r in g.B2) / len(g.B2)        # 136
B2_TOTAAL_KIJKERS = sum(r[5] for r in g.B2)               # 4760
B2_TEL_SOORT = sum(1 for r in g.B2 if r[1] == g.B2_TELSOORT)     # 17
B2_TEL_TAAL = sum(1 for r in g.B2 if r[3] == g.B2_TELTAAL)       # 4

# ---------------------------------------------------------------- blad 3
B3_WEEK = [g.per_week(c, d) for _, _, c, d in g.B3]
B3_VEEL = ['ja' if x >= g.B3_DREMPEL else 'nee' for x in B3_WEEK]
B3_SOM = sum(B3_WEEK)                                     # 26500
B3_GEMIDDELDE = B3_SOM / len(B3_WEEK)                     # 1325
B3_MAX = max(B3_WEEK)                                     # 2040
B3_MIN = min(B3_WEEK)                                     # 540
B3_TEL = B3_VEEL.count('ja')                              # 8
B3_SOMLEEFTIJD = sum(w for w, (_, lft, _, _) in zip(B3_WEEK, g.B3)
                     if lft == g.B3_LEEFTIJD)             # 6610
B3_SOMVEEL = sum(w for w, v in zip(B3_WEEK, B3_VEEL) if v == 'ja')   # 13815
B3_GRENSGEVAL = [c for c, w in zip([r[0] for r in g.B3], B3_WEEK)
                 if w == g.B3_DREMPEL]
B3_PER_DAG = B3_GEMIDDELDE / 7                            # ≈ 189 min

# ---------------------------------------------------------------- blad 4
# Draaitabel 1: aantal titels, rijen = Genre, kolommen = Soort.
D1_RIJLABELS = sorted({g.genre(r[2])[1] for r in g.B2})
D1_KOLLABELS = sorted({r[1] for r in g.B2})
_t1 = collections.Counter((g.genre(r[2])[1], r[1]) for r in g.B2)
D1_CEL = {(r, k): _t1.get((r, k), 0) for r in D1_RIJLABELS for k in D1_KOLLABELS}
D1_RIJTOTAAL = {r: sum(D1_CEL[(r, k)] for k in D1_KOLLABELS) for r in D1_RIJLABELS}
D1_KOLTOTAAL = {k: sum(D1_CEL[(r, k)] for r in D1_RIJLABELS) for k in D1_KOLLABELS}
D1_EINDTOTAAL = sum(D1_RIJTOTAAL.values())                # 35
D1_TOPGENRE = max(D1_RIJLABELS, key=lambda r: (D1_RIJTOTAAL[r], r))
D1_TOPGENRE_AANTAL = D1_RIJTOTAAL[D1_TOPGENRE]
# het genre waarvan er alleen series bestaan en geen enkele film
D1_ALLEEN_SERIES = [r for r in D1_RIJLABELS
                    if D1_CEL[(r, 'Film')] == 0 and D1_CEL[(r, 'Serie')] > 0]

# Draaitabel 2: rijen = Taal, twee waardevelden (aantal titels en gemiddelde).
_per_taal = collections.defaultdict(list)
for r in g.B2:
    _per_taal[r[3]].append(r[5])
D2_AANTAL = {t: len(v) for t, v in _per_taal.items()}
D2_GEMIDDELD = {t: sum(v) / len(v) for t, v in _per_taal.items()}
D2_OPLOPEND = sorted(D2_AANTAL)
D2_AFLOPEND = sorted(D2_AANTAL, key=lambda t: (-D2_GEMIDDELD[t], t))
D2_EINDTOTAAL_AANTAL = sum(D2_AANTAL.values())            # 35
D2_EINDTOTAAL_GEMIDDELD = B2_GEMIDDELD                    # 136
D2_TOPTAAL = D2_AFLOPEND[0]                               # Koreaans
D2_TOPTAAL_GEMIDDELD = D2_GEMIDDELD[D2_TOPTAAL]           # 245
D2_LAAGSTE = D2_AFLOPEND[-1]                              # Noors
D2_MEESTE_TITELS = max(D2_AANTAL, key=lambda t: (D2_AANTAL[t], t))   # Engels

# ---------------------------------------------------------------- blad 5
B5_JAREN = [j for j, _ in g.B5]
B5_MINUTEN = [m for _, m in g.B5]
B5_VERSCHIL = [None] + [B5_MINUTEN[i] - B5_MINUTEN[i - 1]
                        for i in range(1, len(B5_MINUTEN))]
_stappen = [(v, g.B5[i][0]) for i, v in enumerate(B5_VERSCHIL) if v is not None]
B5_GROOTSTE_STIJGING = max(_stappen)
B5_STIJGING_TOT = B5_GROOTSTE_STIJGING[1]
B5_STIJGING_VAN = B5_JAREN[B5_JAREN.index(B5_STIJGING_TOT) - 1]
B5_STIJGING = B5_GROOTSTE_STIJGING[0]
B5_GROOTSTE_DALING = min(_stappen)
B5_DALING_TOT = B5_GROOTSTE_DALING[1]
B5_DALING_VAN = B5_JAREN[B5_JAREN.index(B5_DALING_TOT) - 1]
B5_HOOGSTE = max(B5_MINUTEN)
B5_HOOGSTE_JAAR = B5_JAREN[B5_MINUTEN.index(B5_HOOGSTE)]
B5_SOORT_TIJD = 'lijndiagram'
B5_SOORT_VERGELIJK = 'staafdiagram'


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


def _getal(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.').replace('.', ',')


if __name__ == '__main__':
    print('=' * 74)
    print(g.TITEL, '—', g.ONDERTITEL)
    print('=' * 74)

    print('\n--- blad 1  De genres -------------------------------------------')
    print(_tabel(['Code', 'Genre', '2024', '2025', 'Groei', 'Sterk?'],
                 [[c, n, o, nw, B1_GROEI[i], B1_STERK[i]]
                  for i, (c, n, o, nw) in enumerate(g.B1)]))
    print(f'\n  som {B1_SOM}   gemiddelde {_getal(B1_GEMIDDELDE)}   '
          f'max {B1_MAX} ({B1_SNELST})   min {B1_MIN} ({B1_TRAAGST})')
    print(f'  aantal {B1_AANTAL}   sterke groeiers {B1_STERKE}   '
          f'precies op de grens van {g.B1_DREMPEL}: {", ".join(B1_GRENSGEVAL)}')

    print('\n--- blad 2  Het aanbod ------------------------------------------')
    print(f'  {B2_AANTAL} titels   {B2_TOTAAL_KIJKERS} kijkers samen   '
          f'gemiddeld {_getal(B2_GEMIDDELD)} per titel')
    print(f'  {g.B2_TELSOORT}: {B2_TEL_SOORT}   {g.B2_TELTAAL}: {B2_TEL_TAAL}')

    print('\n--- blad 3  De schermtijd ---------------------------------------')
    print(_tabel(['Code', 'Lft', 'School', 'Weekend', 'Per week', 'Veel?'],
                 [[c, l, s, w, B3_WEEK[i], B3_VEEL[i]]
                  for i, (c, l, s, w) in enumerate(g.B3)]))
    print(f'\n  som {B3_SOM}   gemiddelde {_getal(B3_GEMIDDELDE)}   '
          f'max {B3_MAX}   min {B3_MIN}   veel: {B3_TEL}')
    print(f'  som voor {g.B3_LEEFTIJD}-jarigen: {B3_SOMLEEFTIJD}   '
          f'som van wie veel kijkt: {B3_SOMVEEL}')
    print(f'  precies op de grens van {g.B3_DREMPEL}: '
          f'{", ".join(B3_GRENSGEVAL)}')
    print(f'  {_getal(B3_GEMIDDELDE)} min per week is {B3_PER_DAG:.0f} min per dag')

    print('\n--- blad 4  Draaitabel 1  (aantal titels) -----------------------')
    print(_tabel(['Genre'] + D1_KOLLABELS + ['Eindtotaal'],
                 [[r] + [D1_CEL[(r, k)] or '' for k in D1_KOLLABELS]
                  + [D1_RIJTOTAAL[r]] for r in D1_RIJLABELS]
                 + [['Eindtotaal'] + [D1_KOLTOTAAL[k] for k in D1_KOLLABELS]
                    + [D1_EINDTOTAAL]]))
    print(f'\n  grootste genre: {D1_TOPGENRE} met {D1_TOPGENRE_AANTAL}   '
          f'alleen series, geen film: {", ".join(D1_ALLEEN_SERIES)}')

    print('\n--- blad 4  Draaitabel 2  (kijkers per taal) --------------------')
    print(_tabel(['Taal', 'Aantal titels', 'Gemiddeld aantal kijkers'],
                 [[t, D2_AANTAL[t], _getal(D2_GEMIDDELD[t])]
                  for t in D2_AFLOPEND]
                 + [['Eindtotaal', D2_EINDTOTAAL_AANTAL,
                     _getal(D2_EINDTOTAAL_GEMIDDELD)]]))
    print(f'\n  hoogste gemiddelde: {D2_TOPTAAL} '
          f'({_getal(D2_TOPTAAL_GEMIDDELD)})   meeste titels: '
          f'{D2_MEESTE_TITELS} ({D2_AANTAL[D2_MEESTE_TITELS]}), maar die staat '
          f'pas op plaats {D2_AFLOPEND.index(D2_MEESTE_TITELS) + 1}')

    print('\n--- blad 5  De schermtijd door de jaren -------------------------')
    print(_tabel(['Jaar', 'Min/dag', 'Verschil'],
                 [[j, m, '' if B5_VERSCHIL[i] is None else f'{B5_VERSCHIL[i]:+d}']
                  for i, (j, m) in enumerate(g.B5)]))
    print(f'\n  grootste stijging: +{B5_STIJGING} tussen {B5_STIJGING_VAN} en '
          f'{B5_STIJGING_TOT}   grootste daling: {B5_GROOTSTE_DALING[0]} tussen '
          f'{B5_DALING_VAN} en {B5_DALING_TOT}')
    print(f'  hoogste punt: {B5_HOOGSTE} in {B5_HOOGSTE_JAAR}')
    print('\n' + g.WAARSCHUWING)
