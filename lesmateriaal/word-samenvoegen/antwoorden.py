# -*- coding: utf-8 -*-
"""Alle uitkomsten van de samenvoegbundel.

Wat de leerling in Excel met formules uitrekent en wat Word daarna in de
brieven zet, rekent deze module in Python uit. De sleutel drukt het af en
controleer.py legt de twee naast elkaar.
"""
import collections
import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(_s); _s.loader.exec_module(g)


def _enige(paren, sleutel, kies=max):
    beste = kies(sleutel(p) for p in paren)
    winnaars = [p for p in paren if sleutel(p) == beste]
    assert len(winnaars) == 1, f'gedeelde uitschieter: {winnaars}'
    return winnaars[0], beste


def _een(lijst, wat):
    assert len(lijst) == 1, f'{wat}: {len(lijst)} in plaats van één ({lijst})'
    return lijst[0]


# ====================================================================
#  stap 1 — de acht kolommen die ze in Excel maken
# ====================================================================
class Vrijwilliger:
    """Eén rij van de samenvoegbron, met alles wat de formules eruit halen."""

    def __init__(self, rij):
        (self.voornaam, self.achternaam, self.straat, self.nummer,
         self.postcode, self.gemeente, self.geboorte, self.taakcode) = rij
        _code, taaknaam, podium, startuur, vergoeding = g.taak(self.taakcode)
        self.aanhef = f'Beste {self.voornaam}'
        self.adresregel = f'{self.straat} {self.nummer}'
        self.woonplaats = f'{self.postcode} {self.gemeente}'
        self.taak = taaknaam
        self.podium = podium
        self.startuur = g.uur(startuur)
        self.vergoeding_getal = vergoeding
        self.vergoeding = g.euro(vergoeding)
        self.leeftijd = g.leeftijd_op(self.geboorte, g.FESTIVALDAG)
        self.begeleiding = 'ja' if self.leeftijd < g.MEERDERJARIG else 'nee'

    @property
    def naam(self):
        return f'{self.voornaam} {self.achternaam}'

    def gemaakt(self):
        """De acht kolommen die ze zelf maken, in de volgorde van de koprij."""
        return [self.aanhef, self.adresregel, self.woonplaats, self.taak,
                self.startuur, self.vergoeding, self.leeftijd,
                self.begeleiding]


VRIJ = [Vrijwilliger(r) for r in g.VRIJWILLIGERS]
VRIJ_OP_NAAM = {v.naam: v for v in VRIJ}
AANTAL_VRIJ = len(VRIJ)
MINDERJARIG = [v for v in VRIJ if v.begeleiding == 'ja']
AANTAL_MINDERJARIG = len(MINDERJARIG)
AANTAL_MEERDERJARIG = AANTAL_VRIJ - AANTAL_MINDERJARIG
PER_PODIUM = collections.Counter(v.podium for v in VRIJ)
PER_TAAK = collections.Counter(v.taak for v in VRIJ)
FILTER_AANTAL = PER_PODIUM[g.FILTER_PODIUM]
TOTALE_VERGOEDING = sum(v.vergoeding_getal for v in VRIJ)
TOTALE_VERGOEDING_TEKST = g.euro(TOTALE_VERGOEDING)

# de twee die nét wel en nét niet meerderjarig zijn op de festivaldag
NIPT = [v for v in VRIJ
        if abs((v.geboorte.replace(year=g.FESTIVALDAG.year)
                - g.FESTIVALDAG).days) <= 2]
assert len(NIPT) >= 2, 'niemand is vlak voor of na de festivaldag jarig'

# de vrijwilligers die in de vragen gebruikt worden
VOORBEELD_EERSTE = VRIJ[0]
VOORBEELD_UUR = _een([v for v in VRIJ if v.naam == 'Imane Bogaerts'],
                     'de vrijwilliger van de uurvraag')
VOORBEELD_OUDSTE, _oudste_leeftijd = _enige(VRIJ, lambda v: v.leeftijd)
VOORBEELD_DERDE = _een([v for v in VRIJ if v.naam == 'Amina De Smet'],
                       'de vrijwilliger van de vergoedingsvraag')

# ====================================================================
#  stap 2 — de etiketten
# ====================================================================
ETIKET_BLADEN = math.ceil(AANTAL_VRIJ / g.ETIKET_PER_BLAD)
ETIKET_LAATSTE_BLAD = AANTAL_VRIJ - (ETIKET_BLADEN - 1) * g.ETIKET_PER_BLAD
ETIKET_LEEG_OP_LAATSTE = g.ETIKET_PER_BLAD - ETIKET_LAATSTE_BLAD

# ====================================================================
#  stap 3 en 4 — de brieven
# ====================================================================
AANTAL_BRIEVEN = AANTAL_VRIJ
# wat er in de brief van de eerste vrijwilliger komt te staan
BRIEF_VOORBEELD = {
    'Aanhef': VOORBEELD_EERSTE.aanhef,
    'Taak': VOORBEELD_EERSTE.taak,
    'Podium': VOORBEELD_EERSTE.podium,
    'Startuur': VOORBEELD_EERSTE.startuur,
    'Vergoeding': VOORBEELD_EERSTE.vergoeding,
}
# wat Word toont als ze de ruwe kolom uit de takentabel samenvoegen in plaats
# van de tekstkolom: de kale getallen waarmee Excel rekent
RUW_UUR = round(
    (g.taak(VOORBEELD_EERSTE.taakcode)[3].hour * 60
     + g.taak(VOORBEELD_EERSTE.taakcode)[3].minute) / 1440, 10)
RUW_UUR_TEKST = f'{RUW_UUR:.10f}'.rstrip('0').replace('.', ',')
# hoeveel decimalen Word toont, verschilt per versie — daarom staat dit in de
# sleutel als "een kommagetal rond 0,58" en niet als een exact antwoord
RUW_UUR_RUWEG = f'{RUW_UUR:.2f}'.replace('.', ',')
RUW_GELD_TEKST = f'{VOORBEELD_EERSTE.vergoeding_getal:g}'.replace('.', ',')

# ====================================================================
#  stap 5 — de sponsors
# ====================================================================
class Sponsor:
    def __init__(self, rij):
        (self.bedrijf, self.voornaam, self.naam, self.aanspreking,
         self.straat, self.nummer, self.postcode, self.gemeente,
         self.pakket, self.bedrag) = rij
        self.aanhef = f'Geachte {self.aanspreking} {self.naam}'
        self.adresregel = f'{self.straat} {self.nummer}'
        self.woonplaats = f'{self.postcode} {self.gemeente}'
        self.bedrag_tekst = g.euro(self.bedrag)
        self.extra_zin = self.bedrag >= g.SPON_DREMPEL

    def gemaakt(self):
        return [self.aanhef, self.adresregel, self.woonplaats,
                self.bedrag_tekst]


SPON = [Sponsor(r) for r in g.SPONSORS]
AANTAL_SPON = len(SPON)
SPON_MET_EXTRA = [s for s in SPON if s.extra_zin]
AANTAL_SPON_EXTRA = len(SPON_MET_EXTRA)
SPON_PER_PAKKET = collections.Counter(s.pakket for s in SPON)
SPON_TOTAAL = sum(s.bedrag for s in SPON)
SPON_TOTAAL_TEKST = g.euro(SPON_TOTAAL)
SPON_VOORBEELD = SPON[0]

# ====================================================================
#  de vragen van het antwoordblad, met hun antwoord
# ====================================================================
# (stap, vraag, antwoord)   het antwoord is None als het niet te controleren is
ANTWOORDBLAD = [
    # ---- stap 1, in Excel
    (1, f'Hoeveel vrijwilligers zijn op {g.datum(g.FESTIVALDAG)} nog geen '
        f'{g.MEERDERJARIG}?', AANTAL_MINDERJARIG),
    (1, f'Wat staat er in de kolom Startuur bij {VOORBEELD_UUR.naam}?',
     VOORBEELD_UUR.startuur),
    (1, f'Wat staat er in de kolom Vergoeding bij {VOORBEELD_OUDSTE.naam}?',
     VOORBEELD_OUDSTE.vergoeding),
    (1, 'Wat is het totaal van alle vergoedingen?', TOTALE_VERGOEDING_TEKST),
    # ---- stap 2, de etiketten
    (2, 'Hoeveel etiketten passen er op één blad?', g.ETIKET_PER_BLAD),
    (2, f'Hoeveel bladen heb je nodig voor {AANTAL_VRIJ} vrijwilligers?',
     ETIKET_BLADEN),
    (2, 'Hoeveel etiketten blijven er leeg op het laatste blad?',
     ETIKET_LEEG_OP_LAATSTE),
    (2, 'Wat zie je als je "Labels bijwerken" vergeet?',
     'alleen het eerste etiket is gevuld'),
    # ---- stap 3, de brief
    (3, 'Hoeveel brieven maakt Word?', AANTAL_BRIEVEN),
    (3, f'Welke taak staat er in de brief van {VOORBEELD_EERSTE.naam}?',
     VOORBEELD_EERSTE.taak),
    (3, f'Welke vergoeding staat er in de brief van {VOORBEELD_DERDE.naam}?',
     VOORBEELD_DERDE.vergoeding),
    (3, 'Wat staat er in de brief als je het startuur uit de takentabel '
        'samenvoegt in plaats van jouw tekstkolom?',
     'een kommagetal rond 0,58 in plaats van een uur'),
    # ---- stap 4, regels en filters
    (4, f'Hoeveel brieven blijven er over met het filter op podium '
        f'{g.FILTER_PODIUM}?', FILTER_AANTAL),
    (4, 'Hoeveel vrijwilligers krijgen de extra zin over begeleiding?',
     AANTAL_MINDERJARIG),
    (4, f'Staat die extra zin in de brief van {VOORBEELD_OUDSTE.naam}?',
     'nee'),
    # ---- stap 5, de eindopdracht
    (5, 'Hoeveel sponsors krijgen de zin over het grote pakket?',
     AANTAL_SPON_EXTRA),
    (5, 'Wat is het totaal van alle sponsorbedragen?', SPON_TOTAAL_TEKST),
]
ANTW_BLAD = "Antwoorden"
ANTW_KOPRIJ = 1
ANTW_START = ANTW_KOPRIJ + 1
ANTW_EIND = ANTW_START + len(ANTWOORDBLAD) - 1
ANTW_KOP = ["Stap", "Vraag", "Antwoord"]


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


if __name__ == '__main__':
    print('=' * 100); print(g.TITEL); print('=' * 100)
    print(f'{g.FESTIVAL} {g.EDITIE}, eerste festivaldag '
          f'{g.datum_lang(g.FESTIVALDAG)}   brief van '
          f'{g.datum_lang(g.BRIEFDATUM)}')

    print('\n--- stap 1  de acht kolommen die ze in Excel maken -------------')
    print(_tabel(['Naam', 'Aanhef', 'Adresregel', 'Woonplaats', 'Taak',
                  'Uur', 'Vergoeding', 'Lft', 'Beg.'],
                 [[v.naam] + v.gemaakt() for v in VRIJ]))
    print(f'\n  {AANTAL_MINDERJARIG} van de {AANTAL_VRIJ} zijn op '
          f'{g.datum(g.FESTIVALDAG)} nog geen {g.MEERDERJARIG}')
    for v in NIPT:
        print(f'  nipt: {v.naam}, geboren {g.datum(v.geboorte)}, is '
              f'{v.leeftijd} — begeleiding: {v.begeleiding}')
    print(f'  totaal aan vergoedingen: {TOTALE_VERGOEDING_TEKST}')

    print('\n--- stap 2  de etiketten ---------------------------------------')
    print(f'  {g.ETIKET_SOORT}')
    print(f'  {AANTAL_VRIJ} etiketten = {ETIKET_BLADEN} bladen, '
          f'{ETIKET_LAATSTE_BLAD} op het laatste, '
          f'{ETIKET_LEEG_OP_LAATSTE} blijven leeg')

    print('\n--- stap 3  de brief ------------------------------------------')
    print(f'  {AANTAL_BRIEVEN} brieven')
    print(f'  brief 1 ({VOORBEELD_EERSTE.naam}):')
    for veld, waarde in BRIEF_VOORBEELD.items():
        print(f'      «{veld}» -> {waarde}')
    print(f'  met de RUWE kolommen uit de takentabel zou daar staan: '
          f'{RUW_UUR_TEKST} en {RUW_GELD_TEKST}')

    print('\n--- stap 4  regels en filters ---------------------------------')
    print(_tabel(['Podium', 'Vrijwilligers'],
                 [[p, PER_PODIUM[p]] for p in sorted(PER_PODIUM)]
                 + [['Samen', AANTAL_VRIJ]]))
    print(f'\n  filter op {g.FILTER_PODIUM}: {FILTER_AANTAL} brieven')
    print(f'  extra zin over begeleiding: {AANTAL_MINDERJARIG} brieven')

    print('\n--- stap 5  de sponsors (eindopdracht) ------------------------')
    print(_tabel(['Bedrijf', 'Aanhef', 'Adresregel', 'Woonplaats', 'Pakket',
                  'Bedrag', 'Extra zin'],
                 [[s.bedrijf, s.aanhef, s.adresregel, s.woonplaats, s.pakket,
                   s.bedrag_tekst, 'ja' if s.extra_zin else 'nee']
                  for s in SPON]))
    print(f'\n  {AANTAL_SPON} brieven, waarvan {AANTAL_SPON_EXTRA} met de '
          f'extra zin (bedrag vanaf {g.euro(g.SPON_DREMPEL)})')
    print(f'  totaal: {SPON_TOTAAL_TEKST}')

    print('\n--- het antwoordblad ------------------------------------------')
    print(_tabel(['Stap', 'Vraag', 'Antwoord'],
                 [[st, v[:62], a] for st, v, a in ANTWOORDBLAD]))
    print('\n' + g.WAARSCHUWING)
