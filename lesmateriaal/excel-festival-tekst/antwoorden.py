# -*- coding: utf-8 -*-
"""Alle uitkomsten van de tekstbundel, blad per blad.

Wat de leerling met formules uitrekent, rekent deze module in Python uit. De
sleutel drukt het af, en controleer.py legt de twee naast elkaar.
"""
import collections
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(_s); _s.loader.exec_module(g)


def _top(d, kies=max):
    """De sleutel met de hoogste (of laagste) waarde. Faalt bij een gelijkspel."""
    beste = kies(d.values())
    winnaars = [k for k, v in d.items() if v == beste]
    assert len(winnaars) == 1, f'gedeelde eerste plaats: {winnaars}'
    return winnaars[0], beste


def _enige_grootste(paren, sleutel):
    """Het enige element met de hoogste waarde van sleutel()."""
    beste = max(sleutel(p) for p in paren)
    winnaars = [p for p in paren if sleutel(p) == beste]
    assert len(winnaars) == 1, f'gedeelde langste: {winnaars}'
    return winnaars[0], beste


# ---------------------------------------------------------------- blad 1
B1_CODE = [g.artiestcode(land, jaar) for _, land, jaar in g.B1]
B1_LAND = [land for _, land, _ in g.B1]
B1_JAAR_TEKST = [str(jaar) for _, _, jaar in g.B1]
B1_JAAR_GETAL = [jaar for _, _, jaar in g.B1]
B1_PER_LAND = dict(collections.Counter(B1_LAND))
B1_MEESTE_LAND, B1_MEESTE_AANTAL = _top(B1_PER_LAND)
B1_VROEGSTE = min(B1_JAAR_GETAL)
B1_VROEGSTE_ARTIEST = next(a for a, _, j in g.B1 if j == B1_VROEGSTE)
B1_CODELENGTE = len(B1_CODE[0])

# ---------------------------------------------------------------- blad 2
B2_REGEL = [g.systeemregel(p, a) for p, a in g.B2]
B2_PODIUM = [p for p, _ in g.B2]
B2_ARTIEST = [a for _, a in g.B2]
B2_LENGTE = [len(a) for a in B2_ARTIEST]
B2_PER_PODIUM = dict(collections.Counter(B2_PODIUM))
B2_MEESTE_PODIUM, B2_MEESTE_AANTAL = _top(B2_PER_PODIUM)
B2_TELPODIUM = 'Klub C'
if B2_TELPODIUM not in B2_PER_PODIUM:
    raise KeyError(
        f'de tweede vraag van blad 2 gaat over {B2_TELPODIUM!r}, en dat podium '
        f'staat niet in de lijst — de podia zijn {sorted(B2_PER_PODIUM)}')
B2_TELPODIUM_AANTAL = B2_PER_PODIUM[B2_TELPODIUM]
(B2_LANGSTE_PODIUM, B2_LANGSTE), B2_LANGSTE_LENGTE = _enige_grootste(
    g.B2, lambda r: len(r[1]))

# ---------------------------------------------------------------- blad 3
B3_CODE = [g.boekingscode(d, p, v) for d, p, v in g.B3]
B3_DAG = [d for d, _, _ in g.B3]
B3_PODIUMCODE = [p for _, p, _ in g.B3]
B3_VOLGNUMMER = [v for _, _, v in g.B3]
B3_PER_DAG = dict(collections.Counter(B3_DAG))
B3_DRUKSTE_DAG, B3_DRUKSTE_AANTAL = _top(B3_PER_DAG)
B3_PER_PODIUM = dict(collections.Counter(B3_PODIUMCODE))
B3_MINSTE_PODIUM, B3_MINSTE_AANTAL = _top(B3_PER_PODIUM, min)
B3_HOOGSTE_VOLGNUMMER = max(B3_VOLGNUMMER)
B3_CODELENGTE = len(B3_CODE[0])
# waar elk stuk begint, zodat de opdracht geen hard getal hoeft te bevatten
B3_POS_DAG = len(g.B3_VOORVOEGSEL) + 2
B3_LEN_DAG = len(g.B3_DAGEN[0])
B3_POS_PODIUM = B3_POS_DAG + B3_LEN_DAG + 1
B3_LEN_PODIUM = len(g.B3_PODIUMCODES[0])
B3_LEN_VOLGNUMMER = 3

# ---------------------------------------------------------------- blad 4
B4_NAAM = [g.nette_naam(a, v) for a, v in g.B4]
B4_MAIL = [g.mailadres(a, v) for a, v in g.B4]
B4_MAILLENGTE = [len(m) for m in B4_MAIL]
B4_LANGSTE_MAIL = max(B4_MAIL, key=len)
B4_LANGSTE_LENGTE = len(B4_LANGSTE_MAIL)
assert B4_MAILLENGTE.count(B4_LANGSTE_LENGTE) == 1, 'twee even lange adressen'
B4_LANGSTE_NAAM = B4_NAAM[B4_MAIL.index(B4_LANGSTE_MAIL)]

# ---------------------------------------------------------------- blad 5
B5_DUBBELE_REGELS = len(g.B5_EXPORT) - len(g.B5_SCHOON)
B5_NA_OPKUISEN = len(g.B5_SCHOON)
B5_PER_PODIUM = dict(collections.Counter(r[2] for r in g.B5_SCHOON))
B5_MEESTE_PODIUM, B5_MEESTE_AANTAL = _top(B5_PER_PODIUM)
B5_PER_GENRE = dict(collections.Counter(r[3] for r in g.B5_SCHOON))
B5_SLICER_AANTAL = B5_PER_GENRE[g.B5_SLICER_KEUZE]
B5_DUBBELE_NAMEN = sorted({g.B5_SCHOON[i][0] for i in g.B5_DUBBEL})
# de draaitabel zoals ze na het opkuisen hoort te zijn
B5_DRAAI = dict(B5_PER_PODIUM)
B5_DRAAI_LABELS = sorted(B5_DRAAI)
B5_DRAAI_TOTAAL = sum(B5_DRAAI.values())
# en wat de slicer ervan overlaat
B5_DRAAI_GEFILTERD = dict(collections.Counter(
    r[2] for r in g.B5_SCHOON if r[3] == g.B5_SLICER_KEUZE))
B5_GEFILTERD_LABELS = sorted(B5_DRAAI_GEFILTERD)


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


def _zichtbaar(tekst):
    """Spaties zichtbaar maken, anders zie je in de sleutel niet wat er mis is."""
    return tekst.replace(' ', '·')


if __name__ == '__main__':
    print('=' * 78); print(g.TITEL); print('=' * 78)

    print('\n--- blad 1  LINKS en RECHTS ------------------------------------')
    print(_tabel(['Artiest', 'Code', 'Land', 'Jaar (tekst)', 'Jaar (getal)'],
                 [[a, B1_CODE[i], B1_LAND[i], B1_JAAR_TEKST[i], B1_JAAR_GETAL[i]]
                  for i, (a, _, _) in enumerate(g.B1)]))
    print(f'\n  meeste acts: {B1_MEESTE_LAND} ({B1_MEESTE_AANTAL})   '
          f'vroegste jaar: {B1_VROEGSTE} ({B1_VROEGSTE_ARTIEST})')
    print(f'  elke code telt {B1_CODELENGTE} tekens — daarom werkt LINKS/RECHTS')

    print('\n--- blad 2  VIND.ALLES en LENGTE -------------------------------')
    print(_tabel(['Regel', 'Podium', 'Artiest', 'Lengte'],
                 [[B2_REGEL[i], B2_PODIUM[i], B2_ARTIEST[i], B2_LENGTE[i]]
                  for i in range(len(g.B2))]))
    print(f'\n  meeste acts: {B2_MEESTE_PODIUM} ({B2_MEESTE_AANTAL})   '
          f'{B2_TELPODIUM}: {B2_TELPODIUM_AANTAL}   '
          f'langste naam: {B2_LANGSTE} ({B2_LANGSTE_LENGTE} tekens)')

    print('\n--- blad 3  DEEL -----------------------------------------------')
    print(_tabel(['Boekingscode', 'Dag', 'Podium', 'Volgnummer'],
                 [[B3_CODE[i], B3_DAG[i], B3_PODIUMCODE[i], B3_VOLGNUMMER[i]]
                  for i in range(len(g.B3))]))
    print(f'\n  drukste dag: {B3_DRUKSTE_DAG} ({B3_DRUKSTE_AANTAL})   '
          f'minste acts: {B3_MINSTE_PODIUM} ({B3_MINSTE_AANTAL})   '
          f'hoogste volgnummer: {B3_HOOGSTE_VOLGNUMMER}')
    print(f'  de dag begint op teken {B3_POS_DAG}, het podium op '
          f'{B3_POS_PODIUM} — altijd, want elke code telt {B3_CODELENGTE} tekens')

    print('\n--- blad 4  SPATIES.WISSEN, BEGINLETTERS en & ------------------')
    print(_tabel(['Achternaam (ruw)', 'Voornaam (ruw)', 'Naam', 'E-mailadres',
                  'Lengte'],
                 [[_zichtbaar(a), _zichtbaar(v), B4_NAAM[i], B4_MAIL[i],
                   B4_MAILLENGTE[i]] for i, (a, v) in enumerate(g.B4)]))
    print(f'\n  (· staat voor een spatie)   langste adres: {B4_LANGSTE_MAIL} '
          f'({B4_LANGSTE_LENGTE} tekens, {B4_LANGSTE_NAAM})')

    print('\n--- blad 5  opkuisen, tabel, draaitabel, grafiek, slicer -------')
    print(f'  de export telt {len(g.B5_EXPORT)} regels, '
          f'{B5_DUBBELE_REGELS} daarvan zijn dubbel: '
          f'{", ".join(B5_DUBBELE_NAMEN)}')
    print(f'  na Duplicaten verwijderen blijven er {B5_NA_OPKUISEN} over\n')
    print(_tabel(['Podium', 'Aantal acts', f'Alleen {g.B5_SLICER_KEUZE}'],
                 [[p, B5_DRAAI[p], B5_DRAAI_GEFILTERD.get(p, 0)]
                  for p in B5_DRAAI_LABELS]
                 + [['Eindtotaal', B5_DRAAI_TOTAAL, B5_SLICER_AANTAL]]))
    print(f'\n  meeste acts: {B5_MEESTE_PODIUM} ({B5_MEESTE_AANTAL})   '
          f'met de slicer op {g.B5_SLICER_KEUZE}: {B5_SLICER_AANTAL} acts')
    print('\n' + g.WAARSCHUWING)
