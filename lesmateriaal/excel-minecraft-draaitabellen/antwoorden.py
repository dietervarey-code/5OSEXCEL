# -*- coding: utf-8 -*-
"""Alle uitkomsten van de Minecraft-draaitabelbundel, draaitabel per draaitabel.

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


def _enige(lijst, wat):
    """Het enige element van een lijst. Faalt luid als het er geen of twee zijn."""
    assert len(lijst) == 1, f'{wat}: {len(lijst)} antwoorden in plaats van één ({lijst})'
    return lijst[0]


# ---------------------------------------------------------------- blad 1
D1 = dict(collections.Counter(r[2] for r in g.B1))
D1_LABELS = sorted(D1)
D1_TOTAAL = sum(D1.values())
D1_TOP, D1_TOP_AANTAL = _top(D1)
D1_MINST = min(D1, key=lambda k: (D1[k], k))

# ---------------------------------------------------------------- blad 2
D2_RIJEN, D2_KOLLEN, D2_CEL, D2_RIJTOT, D2_KOLTOT, D2_TOTAAL = _telling(
    [(r[1], r[2]) for r in g.B2])
D2_VEELST_GEREEDSCHAP, D2_VEELST_AANTAL = _top(D2_KOLTOT)
D2_SCHEP = 'Schep'
D2_NATUURLIJK = 'Natuurlijk'
if (D2_NATUURLIJK, D2_SCHEP) not in D2_CEL:
    raise KeyError(
        f'de kruistabel heeft geen vakje {D2_NATUURLIJK}/{D2_SCHEP}: de rijen zijn '
        f'{D2_RIJEN} en de kolommen {D2_KOLLEN} — de tweede vraag van blad 2 '
        'bestaat dan niet meer')
D2_NATUURLIJK_SCHEP = D2_CEL[(D2_NATUURLIJK, D2_SCHEP)]
# de categorie waarin élk blok hetzelfde gereedschap vraagt: precies één
# gevuld vakje op die rij
D2_EEN_GEREEDSCHAP = _enige(
    [r for r in D2_RIJEN
     if sum(1 for k in D2_KOLLEN if D2_CEL[(r, k)]) == 1],
    'categorie met maar één gereedschap')
D2_LEGE_VAKJES = sum(1 for r in D2_RIJEN for k in D2_KOLLEN if not D2_CEL[(r, k)])

# ---------------------------------------------------------------- blad 3
_duur = collections.defaultdict(int)
for _, materiaal, _, duurzaamheid in g.B3:
    _duur[materiaal] += duurzaamheid
D3 = dict(_duur)
D3_AFLOPEND = sorted(D3, key=lambda m: (-D3[m], m))
D3_TOTAAL = sum(D3.values())
D3_TOP, D3_TOP_DUURZAAMHEID = _top(D3)
D3_LAAGSTE = D3_AFLOPEND[-1]
D3_AANDEEL_TOP = D3_TOP_DUURZAAMHEID / D3_TOTAAL

# ---------------------------------------------------------------- blad 4
_per_periode = collections.defaultdict(list)
for versie, naam, jaar, thema, blokken in g.B4:
    _per_periode[g.periode(jaar)].append(blokken)
D4_LABELS = sorted(_per_periode)
D4_AANTAL = {p: len(v) for p, v in _per_periode.items()}
D4_GEMIDDELD = {p: sum(v) / len(v) for p, v in _per_periode.items()}
D4_TOTAAL_AANTAL = sum(D4_AANTAL.values())
D4_TOTAAL_GEMIDDELD = sum(r[4] for r in g.B4) / len(g.B4)
D4_DRUKSTE, D4_DRUKSTE_AANTAL = _top(D4_AANTAL)
D4_HOOGSTE_GEM, D4_HOOGSTE_GEM_WAARDE = _top(D4_GEMIDDELD)
D4_FILTER_THEMA = g.B4_FILTER
D4_FILTER_AANTAL = sum(1 for r in g.B4 if r[3] == D4_FILTER_THEMA)

# ---------------------------------------------------------------- blad 5
B5_BEROEP = [g.beroep(n)[0] for _, n, _ in g.B5]
B5_WERKBLOK = [g.beroep(n)[1] for _, n, _ in g.B5]
B5_CATEGORIE = [g.beroep(n)[2] for _, n, _ in g.B5]
_aanbod = collections.defaultdict(int)
for (_, n, aanbiedingen) in g.B5:
    _aanbod[g.beroep(n)[2]] += aanbiedingen
D5 = dict(_aanbod)
D5_AFLOPEND = sorted(D5, key=lambda c: (-D5[c], c))
D5_TOTAAL = sum(D5.values())
D5_TOP, D5_TOP_AANBIEDINGEN = _top(D5)

# na de extra dorpeling die ze er zelf bij typen (kaart 9)
_extra_categorie = g.beroep(g.B5_EXTRA[1])[2]
D5_NA = dict(D5)
D5_NA[_extra_categorie] += g.B5_EXTRA[2]
D5_NA_TOTAAL = D5_TOTAAL + g.B5_EXTRA[2]
D5_EXTRA_BEROEP = g.beroep(g.B5_EXTRA[1])[0]
D5_EXTRA_CATEGORIE = _extra_categorie


def _getal(x):
    if isinstance(x, float) and x == int(x):
        x = int(x)
    if isinstance(x, int):
        return f'{x:,}'.replace(',', '.')
    return f'{x:.2f}'.replace('.', ',')


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

    print('\n--- blad 1  Mobs: aantal per dimensie --------------------------')
    print(_tabel(['Dimensie', 'Aantal mobs'],
                 [[d, D1[d]] for d in D1_LABELS] + [['Eindtotaal', D1_TOTAAL]]))
    print(f'\n  meeste mobs: {D1_TOP} ({D1_TOP_AANTAL})   minste: {D1_MINST}')

    print('\n--- blad 2  Blokken: categorie tegenover gereedschap -----------')
    print(_tabel(['Categorie'] + D2_KOLLEN + ['Eindtotaal'],
                 [[r] + [D2_CEL[(r, k)] or '' for k in D2_KOLLEN] + [D2_RIJTOT[r]]
                  for r in D2_RIJEN]
                 + [['Eindtotaal'] + [D2_KOLTOT[k] for k in D2_KOLLEN]
                    + [D2_TOTAAL]]))
    print(f'\n  meest gebruikte gereedschap: {D2_VEELST_GEREEDSCHAP} '
          f'({D2_VEELST_AANTAL})   natuurlijk met schep: {D2_NATUURLIJK_SCHEP}   '
          f'maar één gereedschap nodig: {D2_EEN_GEREEDSCHAP}')
    print(f'  {D2_LEGE_VAKJES} lege vakjes — die combinaties komen niet voor')

    print('\n--- blad 3  Gereedschap: duurzaamheid per materiaal ------------')
    print(_tabel(['Materiaal', 'Som van duurzaamheid'],
                 [[m, _getal(D3[m])] for m in D3_AFLOPEND]
                 + [['Eindtotaal', _getal(D3_TOTAAL)]]))
    print(f'\n  hoogste: {D3_TOP} met {_getal(D3_TOP_DUURZAAMHEID)} '
          f'({D3_AANDEEL_TOP:.1%} van het totaal)   laagste: {D3_LAAGSTE}')
    print(f'  met Aantal in plaats van Som geeft elke rij {len(g.B3_SOORTEN)} — '
          'daar zie je niets aan')

    print('\n--- blad 4  Updates: per periode van vijf jaar -----------------')
    print(_tabel(['Periode', 'Aantal updates', 'Gemiddeld nieuwe blokken'],
                 [[p, D4_AANTAL[p], _getal(D4_GEMIDDELD[p])] for p in D4_LABELS]
                 + [['Eindtotaal', D4_TOTAAL_AANTAL,
                     _getal(D4_TOTAAL_GEMIDDELD)]]))
    print(f'\n  drukste periode: {D4_DRUKSTE} ({D4_DRUKSTE_AANTAL} updates)   '
          f'hoogste gemiddelde: {D4_HOOGSTE_GEM} '
          f'({_getal(D4_HOOGSTE_GEM_WAARDE)}, uit maar '
          f'{D4_AANTAL[D4_HOOGSTE_GEM]} updates)')
    print(f'  met filter {D4_FILTER_THEMA}: {D4_FILTER_AANTAL} updates')

    print('\n--- blad 5  Dorpelingen: aanbiedingen per categorie ------------')
    print(_tabel(['Categorie', 'Aanbiedingen', 'Na de extra dorpeling'],
                 [[c, _getal(D5[c]), _getal(D5_NA[c])] for c in D5_AFLOPEND]
                 + [['Eindtotaal', _getal(D5_TOTAAL), _getal(D5_NA_TOTAAL)]]))
    print(f'\n  grootste: {D5_TOP} ({_getal(D5_TOP_AANBIEDINGEN)})   '
          f'de extra dorpeling is {D5_EXTRA_BEROEP} ({D5_EXTRA_CATEGORIE})')
    print('\n' + g.WAARSCHUWING)
