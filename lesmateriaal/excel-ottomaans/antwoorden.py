# -*- coding: utf-8 -*-
"""Alle uitkomsten van de Ottomaanse bundel, inclusief de twee draaitabellen.

Een draaitabel kan openpyxl niet schrijven — Excel bouwt die zelf. Daarom
rekenen we hier precies uit WAT er in die draaitabel hoort te staan. De
sleutel drukt dat af als tabel, zodat je het blad van een leerling er in één
oogopslag naast kan leggen.
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
B1_JAREN = [g.duur(b, e) for _, _, b, e in g.B1]
B1_LANG = ['ja' if j >= g.B1_DREMPEL else 'nee' for j in B1_JAREN]
B1_SOM = sum(B1_JAREN)                                   # 329
B1_GEMIDDELDE = B1_SOM / len(B1_JAREN)                    # 25,3077...
B1_MAX = max(B1_JAREN)                                    # 46
B1_MIN = min(B1_JAREN)                                    # 4
B1_AANTAL = len(g.B1)                                     # 13
B1_LANGE = B1_LANG.count('ja')                            # 9
B1_LANGSTE = g.B1[B1_JAREN.index(B1_MAX)][1]              # Süleyman I
B1_KORTSTE = g.B1[B1_JAREN.index(B1_MIN)][1]              # Mehmed VI
B1_GRENSGEVAL = [n for (_, n, b, e) in g.B1
                 if e - b == g.B1_DREMPEL]                # Osman I, precies 25

# ---------------------------------------------------------------- blad 2
B2_SULTAN = [g.sultan(c)[1] for *_, c in g.B2]
B2_JAREN = [g.regeringsjaren(c) for *_, c in g.B2]
B2_LANG = ['ja' if j >= g.B1_DREMPEL else 'nee' for j in B2_JAREN]
B2_EEUW = [g.eeuw(j) for j, *_ in g.B2]
B2_AANTAL = len(g.B2)                                     # 35
B2_TEL_SOORT = sum(1 for _, _, s, _, _ in g.B2 if s == g.B2_TELSOORT)   # 8
B2_TEL_REGIO = sum(1 for _, _, _, r, _ in g.B2 if r == g.B2_TELREGIO)   # 12
B2_TEL_EEUW = B2_EEUW.count(g.B2_TELEEUW)                               # 9

# ---------------------------------------------------------------- blad 3
B3_DUUR = [g.duur(b, e) for _, _, b, e, _ in g.B3]
B3_LANG = ['ja' if d >= g.B3_DREMPEL else 'nee' for d in B3_DUUR]
B3_SOM = sum(B3_DUUR)                                     # 171
B3_GEMIDDELDE = B3_SOM / len(B3_DUUR)                     # 9,5
B3_MAX = max(B3_DUUR)                                     # 42
B3_MIN = min(B3_DUUR)                                     # 0
B3_TEL = sum(1 for *_, u in g.B3 if u == g.B3_TELUITKOMST)              # 9
B3_SOMLAND = sum(d for d, (_, t, *_) in zip(B3_DUUR, g.B3)
                 if t == g.B3_SOMLAND)                                  # 16
B3_SOMUITKOMST = sum(d for d, (*_, u) in zip(B3_DUUR, g.B3)
                     if u == g.B3_SOMUITKOMST)                          # 42
B3_LANGSTE = g.B3[B3_DUUR.index(B3_MAX)][0]
B3_KORTSTE = g.B3[B3_DUUR.index(B3_MIN)][0]

# ---------------------------------------------------------------- blad 4
# Draaitabel 1: aantal gebeurtenissen, rijen = Soort, kolommen = Eeuw.
D1_RIJLABELS = sorted({s for _, _, s, _, _ in g.B2})
D1_KOLLABELS = sorted(set(B2_EEUW))
_t1 = collections.Counter((s, g.eeuw(j)) for j, _, s, _, _ in g.B2)
D1_CEL = {(r, k): _t1.get((r, k), 0) for r in D1_RIJLABELS for k in D1_KOLLABELS}
D1_RIJTOTAAL = {r: sum(D1_CEL[(r, k)] for k in D1_KOLLABELS) for r in D1_RIJLABELS}
D1_KOLTOTAAL = {k: sum(D1_CEL[(r, k)] for r in D1_RIJLABELS) for k in D1_KOLLABELS}
D1_EINDTOTAAL = sum(D1_RIJTOTAAL.values())                # 35
D1_TOPEEUW = max(D1_KOLTOTAAL, key=lambda k: D1_KOLTOTAAL[k])           # 16e eeuw
D1_TOPEEUW_AANTAL = D1_KOLTOTAAL[D1_TOPEEUW]                            # 9
D1_TOPSOORT = max(D1_RIJTOTAAL, key=lambda r: D1_RIJTOTAAL[r])          # Verovering
D1_TOPSOORT_AANTAL = D1_RIJTOTAAL[D1_TOPSOORT]                          # 8

# Draaitabel 2: som van de duur, rijen = Tegenstander.
_t2 = collections.defaultdict(int)
for d, (_, t, *_) in zip(B3_DUUR, g.B3):
    _t2[t] += d
D2 = dict(_t2)
D2_OPLOPEND = sorted(D2)                                  # zoals Excel ze eerst zet
D2_AFLOPEND = sorted(D2, key=lambda t: (-D2[t], t))       # na sorteren op waarde
D2_EINDTOTAAL = sum(D2.values())                          # 171
D2_TOP = D2_AFLOPEND[0]                                   # Habsburgers
D2_TOP_JAREN = D2[D2_TOP]                                 # 55

# ---------------------------------------------------------------- blad 5
B5_JAREN = [j for j, _ in g.B5]
B5_INWONERS = [n for _, n in g.B5]
B5_VERSCHIL = [None] + [B5_INWONERS[i] - B5_INWONERS[i - 1]
                        for i in range(1, len(B5_INWONERS))]
_dalingen = [(v, g.B5[i][0]) for i, v in enumerate(B5_VERSCHIL) if v is not None]
B5_GROOTSTE_DALING = min(_dalingen)                       # (-6, 1875)
B5_GROOTSTE_STIJGING = max(_dalingen)                     # (+16, 1600)
B5_DALING_VAN = g.B5[B5_JAREN.index(B5_GROOTSTE_DALING[1]) - 1][0]      # 1850
B5_DALING_TOT = B5_GROOTSTE_DALING[1]                                   # 1875
B5_DALING = abs(B5_GROOTSTE_DALING[0])                                  # 6
B5_HOOGSTE = max(B5_INWONERS)                                           # 35
B5_HOOGSTE_JAAR = B5_JAREN[B5_INWONERS.index(B5_HOOGSTE)]               # 1850
B5_SOORT_TIJD = 'lijndiagram'
B5_SOORT_VERGELIJK = 'staafdiagram'


def _tabel(koppen, rijen):
    breed = [max(len(str(k)), *(len(str(r[i])) for r in rijen)) if rijen
             else len(str(k)) for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


if __name__ == '__main__':
    print('=' * 72)
    print(g.TITEL, '—', g.ONDERTITEL)
    print('=' * 72)

    print('\n--- blad 1  De sultans ------------------------------------------')
    print(_tabel(['Code', 'Sultan', 'Van', 'Tot', 'Jaren', 'Lang?'],
                 [[c, n, b, e, B1_JAREN[i], B1_LANG[i]]
                  for i, (c, n, b, e) in enumerate(g.B1)]))
    print(f'\n  som {B1_SOM}   gemiddelde {B1_GEMIDDELDE:.2f}   max {B1_MAX} '
          f'({B1_LANGSTE})   min {B1_MIN} ({B1_KORTSTE})')
    print(f'  aantal {B1_AANTAL}   lange regeringen {B1_LANGE}   '
          f'grensgeval op precies {g.B1_DREMPEL} jaar: {", ".join(B1_GRENSGEVAL)}')

    print('\n--- blad 2  De gebeurtenissen -----------------------------------')
    print(f'  {B2_AANTAL} regels   {g.B2_TELSOORT}: {B2_TEL_SOORT}   '
          f'{g.B2_TELREGIO}: {B2_TEL_REGIO}   {g.B2_TELEEUW}: {B2_TEL_EEUW}')

    print('\n--- blad 3  De oorlogen -----------------------------------------')
    print(_tabel(['Oorlog', 'Tegenstander', 'Van', 'Tot', 'Duur', 'Uitkomst', 'Lang?'],
                 [[o, t, b, e, B3_DUUR[i], u, B3_LANG[i]]
                  for i, (o, t, b, e, u) in enumerate(g.B3)]))
    print(f'\n  som {B3_SOM}   gemiddelde {B3_GEMIDDELDE}   max {B3_MAX} '
          f'({B3_LANGSTE})   min {B3_MIN} ({B3_KORTSTE})')
    print(f'  {g.B3_TELUITKOMST}: {B3_TEL}   jaren tegen {g.B3_SOMLAND}: '
          f'{B3_SOMLAND}   jaren met uitkomst {g.B3_SOMUITKOMST}: {B3_SOMUITKOMST}')

    print('\n--- blad 4  Draaitabel 1  (aantal gebeurtenissen) ---------------')
    print(_tabel(['Soort'] + D1_KOLLABELS + ['Totaal'],
                 [[r] + [D1_CEL[(r, k)] or '' for k in D1_KOLLABELS]
                  + [D1_RIJTOTAAL[r]] for r in D1_RIJLABELS]
                 + [['Eindtotaal'] + [D1_KOLTOTAAL[k] for k in D1_KOLLABELS]
                    + [D1_EINDTOTAAL]]))
    print(f'\n  drukste eeuw: {D1_TOPEEUW} met {D1_TOPEEUW_AANTAL}   '
          f'meest voorkomende soort: {D1_TOPSOORT} met {D1_TOPSOORT_AANTAL}')

    print('\n--- blad 4  Draaitabel 2  (som van de duur) ---------------------')
    print(_tabel(['Tegenstander', 'Oorlogsjaren'],
                 [[t, D2[t]] for t in D2_AFLOPEND] + [['Eindtotaal', D2_EINDTOTAAL]]))

    print('\n--- blad 5  De inwoners -----------------------------------------')
    print(_tabel(['Jaar', 'Miljoen', 'Verschil'],
                 [[j, n, '' if B5_VERSCHIL[i] is None else f'{B5_VERSCHIL[i]:+d}']
                  for i, (j, n) in enumerate(g.B5)]))
    print(f'\n  grootste daling: {B5_DALING} miljoen tussen {B5_DALING_VAN} en '
          f'{B5_DALING_TOT}   hoogste schatting: {B5_HOOGSTE} in {B5_HOOGSTE_JAAR}')
    print('\n' + g.WAARSCHUWING)
