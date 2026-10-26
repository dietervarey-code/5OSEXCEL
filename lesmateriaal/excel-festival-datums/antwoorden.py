# -*- coding: utf-8 -*-
"""Alle uitkomsten van de datumbundel, blad per blad.

Alles wordt op de peildatum uitgerekend, niet op vandaag. Daardoor staat de
sleutel vast en kan controleer.py de twee naast elkaar leggen.
"""
import collections
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(_s); _s.loader.exec_module(g)


def _enige(paren, sleutel, kies=max):
    """Het enige element met de hoogste (of laagste) waarde. Faalt bij gelijkspel."""
    beste = kies(sleutel(p) for p in paren)
    winnaars = [p for p in paren if sleutel(p) == beste]
    assert len(winnaars) == 1, f'gedeelde uitschieter: {winnaars}'
    return winnaars[0], beste


def _dat(d):
    return d.strftime('%d/%m/%Y')


def _datums(waarden, waar):
    """Een datum moet een datum zijn. Een string die eruitziet als een datum
    rekent niet, en in Excel al evenmin."""
    for w in waarden:
        if not hasattr(w, 'toordinal'):
            raise TypeError(
                f'{waar}: {w!r} is geen datum maar een {type(w).__name__}. '
                'Zet het als datetime.date in gegevens.py, anders kan er '
                'niets mee gerekend worden — in Python niet en in Excel niet.')


_datums([d for _t, s, e in g.B1 for d in (s, e)], 'blad 1')
_datums([gb for _n, gb in g.B2], 'blad 2')
_datums([d for d, _t in g.B3], 'blad 3')
_datums([s for _t, s, _d in g.B4], 'blad 4')
_datums([d for d, _k, _t in g.B5], 'blad 5')
_datums([g.PEILDATUM], 'de peildatum')


# ---------------------------------------------------------------- blad 1
B1_DAGEN = [(einde - start).days for _, start, einde in g.B1]
(B1_LANGSTE, _s1, _e1), B1_LANGSTE_DAGEN = _enige(g.B1,
                                                  lambda r: (r[2] - r[1]).days)
B1_VROEGSTE_START = min(start for _, start, _ in g.B1)
B1_LAATSTE_EINDE = max(einde for _, _, einde in g.B1)
B1_SPANNE = (B1_LAATSTE_EINDE - B1_VROEGSTE_START).days
B1_TOTAAL_DAGEN = sum(B1_DAGEN)

# ---------------------------------------------------------------- blad 2
B2_LEEFTIJD = [g.leeftijd_op(geboorte, g.PEILDATUM) for _, geboorte in g.B2]
B2_MAG = ['ja' if lft >= g.B2_MEERDERJARIG else 'nee' for lft in B2_LEEFTIJD]
B2_AANTAL_MAG = B2_MAG.count('ja')
(B2_JONGSTE, _gb), B2_JONGSTE_LEEFTIJD = _enige(
    g.B2, lambda r: g.leeftijd_op(r[1], g.PEILDATUM), min)
(B2_OUDSTE, _gb2), B2_OUDSTE_LEEFTIJD = _enige(
    g.B2, lambda r: g.leeftijd_op(r[1], g.PEILDATUM), max)
# de twee die in de festivalweek jarig zijn: het scherpste voorbeeld
B2_NIPT = [(naam, g.leeftijd_op(geboorte, g.PEILDATUM))
           for naam, geboorte in g.B2
           if abs((geboorte.replace(year=g.PEILDATUM.year)
                   - g.PEILDATUM).days) <= 3]

# ---------------------------------------------------------------- blad 3
B3_MAAND = [d.month for d, _ in g.B3]
B3_WEEKDAG = [g.weekdagnummer(d) for d, _ in g.B3]
B3_SOORT = ['weekend' if g.is_weekend(d) else 'weekdag' for d, _ in g.B3]
B3_WEEKENDDAGEN = B3_SOORT.count('weekend')
(B3_DRUKSTE_DATUM, B3_DRUKSTE_TICKETS), _m = _enige(g.B3, lambda r: r[1])
B3_DRUKSTE_WEEKDAG = g.weekdagnummer(B3_DRUKSTE_DATUM)
B3_DRUKSTE_DAGNAAM = g.dagnaam(B3_DRUKSTE_DATUM)
B3_PER_MAAND = collections.Counter()
for _d, _t in g.B3:
    B3_PER_MAAND[_d.month] += _t
B3_TOTAAL = sum(B3_PER_MAAND.values())

# ---------------------------------------------------------------- blad 4
B4_KLAAR = [g.werkdag(start, dagen) for _, start, dagen in g.B4]
B4_WERKDAGEN_TOT = [g.netto_werkdagen(start, g.PEILDATUM)
                    for _, start, _ in g.B4]
B4_OP_TIJD = ['ja' if klaar <= g.PEILDATUM else 'nee' for klaar in B4_KLAAR]
B4_TE_LAAT = [taak for (taak, _s, _d), ok in zip(g.B4, B4_OP_TIJD) if ok == 'nee']
assert len(B4_TE_LAAT) == 1, f'niet precies één taak te laat: {B4_TE_LAAT}'
B4_TE_LAAT_TAAK = B4_TE_LAAT[0]
B4_TE_LAAT_KLAAR = B4_KLAAR[[r[0] for r in g.B4].index(B4_TE_LAAT_TAAK)]
(B4_ZWAARSTE, _s4, B4_ZWAARSTE_DAGEN), _m4 = _enige(g.B4, lambda r: r[2])
B4_MEESTE_WERKDAGEN = max(B4_WERKDAGEN_TOT)

# ---------------------------------------------------------------- blad 5
B5_PER_MAAND = collections.Counter()
for _d, _k, _t in g.B5:
    B5_PER_MAAND[_d.month] += _t
B5_MAANDEN = sorted(B5_PER_MAAND)
B5_TOTAAL = sum(B5_PER_MAAND.values())
_top = max(B5_PER_MAAND.values())
assert list(B5_PER_MAAND.values()).count(_top) == 1, 'twee even sterke maanden'
B5_TOPMAAND_NUMMER = next(m for m, v in B5_PER_MAAND.items() if v == _top)
B5_TOPMAAND = g.maandnaam(B5_TOPMAAND_NUMMER)
B5_TOPMAAND_TICKETS = _top
B5_TIJDLIJN_TICKETS = B5_PER_MAAND[g.B5_TIJDLIJN_MAANDNUMMER]
B5_PER_KANAAL = collections.Counter()
for _d, _k, _t in g.B5:
    B5_PER_KANAAL[_k] += _t


def _getal(x):
    return f'{x:,}'.replace(',', '.') if isinstance(x, int) else str(x)


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


if __name__ == '__main__':
    print('=' * 78); print(g.TITEL); print('=' * 78)
    print(f'peildatum: {_dat(g.PEILDATUM)} ({g.dagnaam(g.PEILDATUM)})')

    print('\n--- blad 1  een datum is een getal -----------------------------')
    print(_tabel(['Taak', 'Start', 'Einde', 'Dagen'],
                 [[taak, _dat(s), _dat(e), B1_DAGEN[i]]
                  for i, (taak, s, e) in enumerate(g.B1)]))
    print(f'\n  langste taak: {B1_LANGSTE} ({B1_LANGSTE_DAGEN} dagen)   '
          f'van {_dat(B1_VROEGSTE_START)} tot {_dat(B1_LAATSTE_EINDE)} is '
          f'{B1_SPANNE} dagen')

    print('\n--- blad 2  leeftijd op de peildatum ---------------------------')
    print(_tabel(['Vrijwilliger', 'Geboren', 'Leeftijd', 'Achter de bar?'],
                 [[naam, _dat(gb), B2_LEEFTIJD[i], B2_MAG[i]]
                  for i, (naam, gb) in enumerate(g.B2)]))
    print(f'\n  {B2_AANTAL_MAG} van de {len(g.B2)} mogen achter de bar   '
          f'jongste: {B2_JONGSTE} ({B2_JONGSTE_LEEFTIJD})   '
          f'oudste: {B2_OUDSTE} ({B2_OUDSTE_LEEFTIJD})')
    for naam, lft in B2_NIPT:
        print(f'  nipt: {naam} is {lft} op de peildatum')

    print('\n--- blad 3  uit een datum halen --------------------------------')
    print(_tabel(['Datum', 'Tickets', 'Maand', 'Weekdag', 'Soort'],
                 [[_dat(d), t, B3_MAAND[i], B3_WEEKDAG[i], B3_SOORT[i]]
                  for i, (d, t) in enumerate(g.B3)]))
    print(f'\n  {B3_WEEKENDDAGEN} van de {len(g.B3)} verkoopdagen vielen in '
          f'het weekend')
    print(f'  drukste dag: {_dat(B3_DRUKSTE_DATUM)} '
          f'({B3_DRUKSTE_DAGNAAM}, weekdagnummer {B3_DRUKSTE_WEEKDAG}) met '
          f'{_getal(B3_DRUKSTE_TICKETS)} tickets')

    print('\n--- blad 4  werkdagen ------------------------------------------')
    print(_tabel(['Opbouwtaak', 'Start', 'Werkdagen', 'Klaar op', 'Tot fest.',
                  'Op tijd?'],
                 [[taak, _dat(s), d, _dat(B4_KLAAR[i]), B4_WERKDAGEN_TOT[i],
                   B4_OP_TIJD[i]] for i, (taak, s, d) in enumerate(g.B4)]))
    print(f'\n  te laat: {B4_TE_LAAT_TAAK} (klaar op '
          f'{_dat(B4_TE_LAAT_KLAAR)}, het festival begint '
          f'{_dat(g.PEILDATUM)})')
    print(f'  zwaarste taak: {B4_ZWAARSTE} ({B4_ZWAARSTE_DAGEN} werkdagen)   '
          f'meeste werkdagen tot het festival: {B4_MEESTE_WERKDAGEN}')

    print('\n--- blad 5  draaitabel per maand, grafiek, tijdlijn ------------')
    print(_tabel(['Maand', 'Tickets'],
                 [[g.maandnaam(m), _getal(B5_PER_MAAND[m])] for m in B5_MAANDEN]
                 + [['Eindtotaal', _getal(B5_TOTAAL)]]))
    print(f'\n  beste maand: {B5_TOPMAAND} ({_getal(B5_TOPMAAND_TICKETS)})   '
          f'met de tijdlijn op {g.B5_TIJDLIJN_MAAND}: '
          f'{_getal(B5_TIJDLIJN_TICKETS)}')
    print(f'  per kanaal: ' + '   '.join(
        f'{k} {_getal(v)}' for k, v in sorted(B5_PER_KANAAL.items())))
    print('\n' + g.WAARSCHUWING)
