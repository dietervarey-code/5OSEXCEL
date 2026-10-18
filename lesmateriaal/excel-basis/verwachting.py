# -*- coding: utf-8 -*-
"""Wat er in elke opdrachtcel van de basisbundel hoort te staan.

Eén bron voor het nakijken: per opdracht de verwachte waarden, de functie die
gevraagd werd en het gewicht. De opdrachten komen uit oefeningen.py en de
waarden uit antwoorden.py, zodat deze module nooit uit de pas kan lopen met de
bundel zelf.

Het gewicht is bewust simpel: elke opdracht uit 'maken' telt voor één eenheid
en elke opmaakeis telt voor één eenheid. Wie 37 van de 39 eenheden haalt,
krijgt 37/39 van de punten. Binnen één doorgevoerde kolom wordt wel met delen
gewerkt: elf van de twaalf juist is elf twaalfde.
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _laad('g', 'gegevens.py')
a = _laad('a', 'antwoorden.py')
o = _laad('o', 'oefeningen.py')


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


FOUTMELDING = '#N/B'      # de ene rij die bewust geen antwoord heeft

# --- de verwachte waarden en de gevraagde functie, per opdrachtcel -------
# De sleutel is "bladnummer:bereik".
WAARDEN = {
    '1:E4:E15': (a.O1_WAARDEN, None),
    '1:C17':    ([a.O1_STUKS], 'SOM'),
    '1:E17':    ([a.O1_SOM], 'SOM'),

    '2:C6:C15': (a.O2_NIEUW, 'AFRONDEN'),
    '2:D6:D15': (a.O2_VERSCHIL, None),
    '2:E6:E15': (a.O2_PROCENT, None),

    '3:E4:E11': (a.O3_TOTALEN, 'SOM'),
    '3:B13:E13': (a.O3_PER_MAAND + [a.O3_EINDTOTAAL], 'SOM'),
    '3:B16':    ([a.O3_MAX], 'MAX'),
    '3:B17':    ([a.O3_MIN], 'MIN'),
    '3:B18':    ([a.O3_GEM], 'GEMIDDELDE'),
    '3:B19':    ([a.O3_AANTAL], 'AANTAL'),

    '4:D6:D19': (a.O4_LEVERING, 'ALS'),
    '4:C21':    ([a.O4_AANTAL_GRATIS], 'AANTAL.ALS'),
    '4:C22':    ([a.O4_AANTAL_BETALEND], 'AANTAL.ALS'),
    '4:C23':    ([a.O4_SOM_GRATIS], 'SOM.ALS'),
    '4:C24':    ([a.O4_SOM_BETALEND], 'SOM.ALS'),

    '5:B4:B15': ([n for _, n, _ in a.O5_ANTWOORD], 'VERT.ZOEKEN'),
    '5:C4:C15': ([s for _, _, s in a.O5_ANTWOORD], 'VERT.ZOEKEN'),
    '5:E4':     (['Onbekend'], None),
    '5:F4':     ([c for c, n, _ in a.O5_ANTWOORD if n == FOUTMELDING], None),
}

# E4 en F4 op blad 5 moeten ze zelf intypen; daar hoort geen formule.
GETYPT = {'5:E4', '5:F4'}

# --- de opmaakeisen, uitgeschreven in deelcontroles ---------------------
# Elke eis is (omschrijving, [(naam van de deelcontrole, soort, bereik), ...]).
# De soorten worden in nakijken.py uitgevoerd.
OPMAAK = {
    1: [
        ('koprij 3 vet, met achtergrondkleur en gecentreerd', [
            ('koprij 3 vet', 'vet', 'A3:E3'),
            ('koprij 3 achtergrondkleur', 'vulling', 'A3:E3'),
            ('koprij 3 gecentreerd', 'gecentreerd', 'A3:E3')]),
        ('kolom D en E in valuta', [
            ('kolom D als valuta', 'valuta', 'D4:D15'),
            ('kolom E als valuta', 'valuta', 'E4:E15')]),
        ('totaalrij 17 vet met een bovenrand', [
            ('totaalrij 17 vet', 'vet', 'A17:E17'),
            ('bovenrand op rij 17', 'bovenrand', 'A17:E17')]),
    ],
    2: [
        ('B3 met de notatie percentage', [
            ('B3 als percentage', 'percentage', 'B3')]),
        ('kolom B, C en D in valuta', [
            ('kolom B als valuta', 'valuta', 'B6:B15'),
            ('kolom C als valuta', 'valuta', 'C6:C15'),
            ('kolom D als valuta', 'valuta', 'D6:D15')]),
        ('kolom E in percentage', [
            ('kolom E als percentage', 'percentage', 'E6:E15')]),
        ('koprij 5 vet met achtergrondkleur, en een rand rond A5:E15', [
            ('koprij 5 vet', 'vet', 'A5:E5'),
            ('koprij 5 achtergrondkleur', 'vulling', 'A5:E5'),
            ('rand rond A5:E15', 'rand_rond', 'A5:E15')]),
    ],
    3: [
        ('koprij 3 vet, met achtergrondkleur en gecentreerd', [
            ('koprij 3 vet', 'vet', 'A3:E3'),
            ('koprij 3 achtergrondkleur', 'vulling', 'A3:E3'),
            ('koprij 3 gecentreerd', 'gecentreerd', 'A3:E3')]),
        ('totaalrij 13 vet met een bovenrand', [
            ('totaalrij 13 vet', 'vet', 'A13:E13'),
            ('bovenrand op rij 13', 'bovenrand', 'A13:E13')]),
        ('samenvattingsblok A15:B19 met achtergrondkleur, A15 in het vet', [
            ('blok A15:B19 achtergrondkleur', 'vulling', 'A15:B19'),
            ('A15 vet', 'vet', 'A15')]),
        ('B16 tot B18 in valuta, B19 niet — dat is een aantal', [
            ('B16:B18 als valuta', 'valuta', 'B16:B18'),
            ('B19 niet als valuta', 'geen_valuta', 'B19')]),
    ],
    4: [
        ('voorwaardelijke opmaak op C6:C19, groen vanaf de grens', [
            ('voorwaardelijke opmaak op C6:C19', 'vw_opmaak', 'C6:C19')]),
        ('kolom C en de cellen C23 en C24 in valuta', [
            ('kolom C als valuta', 'valuta', 'C6:C19'),
            ('C23:C24 als valuta', 'valuta', 'C23:C24')]),
        ('koprij 5 vet met achtergrondkleur, labels B21:B24 in het vet', [
            ('koprij 5 vet', 'vet', 'A5:D5'),
            ('koprij 5 achtergrondkleur', 'vulling', 'A5:D5'),
            ('labels B21:B24 vet', 'vet', 'B21:B24')]),
    ],
    5: [
        ('een rand rond A3:C15', [
            ('rand rond A3:C15', 'rand_rond', 'A3:C15')]),
        ('koprij 3 vet met achtergrondkleur', [
            ('koprij 3 vet', 'vet', 'A3:C3'),
            ('koprij 3 achtergrondkleur', 'vulling', 'A3:C3')]),
        ('de koppen vastgezet, zodat ze bij het scrollen blijven staan', [
            ('koppen geblokkeerd', 'blokkade', '4')]),
        ('kolommen breed genoeg: geen enkele naam afgekapt', [
            ('kolom A breed genoeg', 'breed', 'A3:A15'),
            ('kolom B breed genoeg', 'breed', 'B3:B15'),
            ('kolom C breed genoeg', 'breed', 'C3:C15')]),
    ],
}

# --- alles samenbrengen per blad ----------------------------------------
PER_BLAD = {}
for _oef in o.OEFENINGEN:
    _nr = _oef['nr']
    _regels = []
    for _waar, _wat, _hoe in _oef['maken']:
        _sleutel = f'{_nr}:{_waar}'
        _waarden, _functie = WAARDEN[_sleutel]
        _cellen = cellen_van(_waar)
        assert len(_cellen) == len(_waarden), (
            f"{_oef['blad']} {_waar}: {len(_cellen)} cellen, "
            f'{len(_waarden)} waarden')
        _regels.append(dict(waar=_waar, cellen=_cellen, waarden=_waarden,
                            wat=_wat, hoe=_hoe, functie=_functie,
                            getypt=_sleutel in GETYPT))
    assert len(_oef['opmaak']) == len(OPMAAK[_nr]), (
        f"blad {_nr}: {len(_oef['opmaak'])} opmaakeisen in de opdracht, "
        f'{len(OPMAAK[_nr])} in deze module')
    PER_BLAD[_oef['blad']] = dict(nr=_nr, regels=_regels, opmaak=OPMAAK[_nr])

# Elke opdrachtcel moet precies één verwachting hebben, en omgekeerd.
GEBRUIKT = {f"{i['nr']}:{r['waar']}" for i in PER_BLAD.values() for r in i['regels']}
ONGEBRUIKT = sorted(set(WAARDEN) - GEBRUIKT)
assert not ONGEBRUIKT, f'verwachtingen zonder opdrachtcel: {ONGEBRUIKT}'

AANTAL_FORMULES = sum(len(i['regels']) for i in PER_BLAD.values())
AANTAL_OPMAAK = sum(len(i['opmaak']) for i in PER_BLAD.values())
AANTAL_EENHEDEN = AANTAL_FORMULES + AANTAL_OPMAAK

if __name__ == '__main__':
    for blad, info in PER_BLAD.items():
        print(f"blad {info['nr']}  {blad:<16} {len(info['regels'])} opdrachten, "
              f"{len(info['opmaak'])} opmaakeisen")
    print(f'\n{AANTAL_FORMULES} opdrachten + {AANTAL_OPMAAK} opmaakeisen '
          f'= {AANTAL_EENHEDEN} eenheden')
