# -*- coding: utf-8 -*-
"""Wat er in elke cel van een ingeleverde toets hoort te staan.

Eén bron voor het nakijken: per cel de verwachte waarde en, waar het om een
doorgevoerde kolom gaat, de volledige lijst. De punten komen uit
oefeningen.py, de waarden uit antwoorden.py — zo kan deze module nooit uit de
pas lopen met de toets zelf.
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _laad('g', 'gegevens.py')
a = _laad('a', 'antwoorden.py')
o = _laad('o', 'oefeningen.py')
sl = _laad('sl', 'sleutel.py')


def cellen_van(verwijzing):
    """'E4:E15' -> alle cellen daartussen, kolom per kolom."""
    if ':' not in verwijzing:
        return [verwijzing]
    links, rechts = verwijzing.split(':')
    k1, r1 = re.match(r'([A-Z]+)(\d+)', links).groups()
    k2, r2 = re.match(r'([A-Z]+)(\d+)', rechts).groups()
    return [f'{chr(k)}{r}'
            for k in range(ord(k1), ord(k2) + 1)
            for r in range(int(r1), int(r2) + 1)]


# --- de verwachte waarden, per opdrachtcel -----------------------------
_GEM_LEEFTIJD = sum(l for _, _, l, _, _ in g.B1) / len(g.B1)
_GEM_VOOR = a.B2_VOOR / len(g.B2)
_GEM_MINUTEN = a.B5_MINUTEN / len(a.B5_BASIS)

# De sleutel is "bladnummer:cel". Blad 2 en blad 5 hebben allebei een B16 en
# een B17 met een heel ander antwoord; op celadres alleen zou de ene de andere
# overschrijven.
WAARDEN = {
    '1:F5:F26': a.B1_ERVAREN,
    '1:B28': [a.B1_CAPS],
    '1:B29': [a.B1_DOELPUNTEN],
    '1:B30': [_GEM_LEEFTIJD],
    '1:B31': [a.B1_OUDSTE],
    '1:B32': [a.B1_JONGSTE],
    '1:B33': [a.B1_AANTAL],
    '1:B34': [a.B1_AANTAL_ERVAREN],

    '2:F4:F11': a.B2_SALDO,
    '2:G4:G11': a.B2_GEWONNEN,
    '2:D13:F13': [a.B2_VOOR, a.B2_TEGEN, a.B2_SALDO_TOTAAL],
    '2:B15': [a.B2_AANTAL_GEWONNEN],
    '2:B16': [_GEM_VOOR],
    '2:B17': [a.B2_MAX_SALDO],

    '3:B22:B25': a.B3_AANTAL_PER,
    '3:C22:C25': a.B3_DOELPUNTEN_PER,
    '3:C27': [a.B3_TOTAAL],

    '4:C5:C12': a.B4_KORTING,
    '4:D5:D12': a.B4_ABONNEE,
    '4:B14:D14': [a.B4_SOM_NORMAAL, a.B4_SOM_KORTING, a.B4_SOM_ABONNEE],

    '5:B4:B14': [speler for _, speler, _, _ in a.B5_BASIS],
    '5:C4:C14': [positie for _, _, positie, _ in a.B5_BASIS],
    '5:B16': [a.B5_MINUTEN],
    '5:B17': [a.B5_AANTAL_TELLEN],
    '5:B18': [_GEM_MINUTEN],
}

PER_BLAD = {}
for _oef in o.OEFENINGEN:
    regels = []
    for _m in _oef['maken']:
        waar = _m['waar']
        waarden = WAARDEN[f"{_oef['nr']}:{waar}"]
        cellen = cellen_van(waar)
        assert len(cellen) == len(waarden), (f"{_oef['blad']} {waar}: {len(cellen)} "
                                             f'cellen, {len(waarden)} waarden')
        regels.append(dict(
            waar=waar, cellen=cellen, waarden=waarden,
            wat=_m['wat'], functie=_m['functie'], punten=_m['punten'],
            formule=next((f for c, f, _, _, _ in sl.SLEUTEL[_oef['nr']]
                          if c == cellen[0]), None),
        ))
    PER_BLAD[_oef['blad']] = dict(nr=_oef['nr'], regels=regels,
                                  opmaak=_oef['opmaak'])

# Elke opdrachtcel moet precies één verwachting hebben, en elke verwachting
# moet bij een opdrachtcel horen. Anders kijkt het script iets na dat niet
# gevraagd is, of net niet.
GEBRUIKT = {f"{i['nr']}:{r['waar']}" for i in PER_BLAD.values() for r in i['regels']}
ONGEBRUIKT = sorted(set(WAARDEN) - GEBRUIKT)
assert not ONGEBRUIKT, f'verwachtingen zonder opdrachtcel: {ONGEBRUIKT}'

# Voor het nakijken: alle verwachte waarden achter elkaar, per blad.
TOTAAL_PUNTEN = sum(r['punten'] for i in PER_BLAD.values() for r in i['regels'])
OPMAAK_PUNTEN = sum(n for i in PER_BLAD.values() for _, n in i['opmaak'])
