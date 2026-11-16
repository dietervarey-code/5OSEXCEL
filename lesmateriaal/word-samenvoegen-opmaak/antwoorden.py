# -*- coding: utf-8 -*-
"""Alle uitkomsten van de tweede samenvoegbundel.

De lijsten staan klaar, dus er valt in Excel niets uit te rekenen. Wat deze
module uitrekent, is wat WORD er straks van maakt: wat op een lidkaart komt,
wat op een envelop, wat in de tabel van de brief, en welke rijen in de
ploeglijst blijven staan na het filter.
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


def _een(lijst, wat):
    assert len(lijst) == 1, f'{wat}: {len(lijst)} in plaats van één ({lijst})'
    return lijst[0]


# ====================================================================
#  de ledenlijst, zoals ze in het startbestand staat
# ====================================================================
class Lid:
    def __init__(self, index, rij):
        (self.voornaam, self.achternaam, straat, nummer, postcode, gemeente,
         self.ploeg, self.geboortejaar, self.betaald) = rij
        trainer, dag, tijd, lidgeld, vervaldatum = g.ploeg(self.ploeg)
        self.lidnummer = g.lidnummer(index)
        self.adresregel = f'{straat} {nummer}'
        self.woonplaats = f'{postcode} {gemeente}'
        self.trainer = trainer
        self.trainingsdag = dag
        self.trainingsuur = g.uur(tijd)
        self.lidgeld = lidgeld
        self.lidgeld_tekst = g.euro(lidgeld)
        self.vervaldatum = vervaldatum
        self.vervaldatum_tekst = g.datum_lang(vervaldatum)

    @property
    def naam(self):
        return f'{self.voornaam} {self.achternaam}'

    def rij(self):
        """De vijftien kolommen, in de volgorde van de koprij."""
        return [self.lidnummer, self.voornaam, self.achternaam,
                self.adresregel, self.woonplaats, self.ploeg,
                self.geboortejaar, self.trainer, self.trainingsdag,
                self.trainingsuur, self.lidgeld, self.lidgeld_tekst,
                self.betaald, self.vervaldatum, self.vervaldatum_tekst]

    def veld(self, naam):
        """De waarde van één samenvoegveld, op naam van de kolom."""
        kolommen = dict(zip(g.LEDEN_KOP, self.rij()))
        if naam not in kolommen:
            raise ValueError(
                f'«{naam}» is geen kolom van {g.LEDEN_BLAD}. Word kent dat '
                f'veld dus niet. De kolommen zijn: '
                + ', '.join(g.LEDEN_KOP))
        return kolommen[naam]


LEDEN = [Lid(i, r) for i, r in enumerate(g.LEDEN_RUW)]
AANTAL_LEDEN = len(LEDEN)
PER_PLOEG = collections.Counter(l.ploeg for l in LEDEN)
NIET_BETAALD = [l for l in LEDEN if l.betaald == 'nee']
AANTAL_NIET_BETAALD = len(NIET_BETAALD)

# ====================================================================
#  stap 1 — de lidkaarten
# ====================================================================
ETIKET_BLADEN = math.ceil(AANTAL_LEDEN / g.ETIKET_PER_BLAD)
ETIKET_LAATSTE = AANTAL_LEDEN - (ETIKET_BLADEN - 1) * g.ETIKET_PER_BLAD
ETIKET_LEEG = g.ETIKET_PER_BLAD - ETIKET_LAATSTE
VOORBEELD = LEDEN[0]


def kaartregels(lid):
    """Wat er op de lidkaart van dit lid komt te staan, regel per regel."""
    uit = []
    for regel in g.LIDKAART:
        tekst = regel['inhoud']
        for veld in regel['velden']:
            tekst = tekst.replace(f'«{veld}»', str(lid.veld(veld)))
        uit.append(tekst)
    return uit


KAART_VOORBEELD = kaartregels(VOORBEELD)

# ====================================================================
#  stap 2 — de enveloppen
# ====================================================================
_veld, _waarde = g.ENVELOP_FILTER
ENVELOPPEN = [l for l in LEDEN if l.veld(_veld) == _waarde]
AANTAL_ENVELOPPEN = len(ENVELOPPEN)
AANTAL_ZONDER_FILTER = AANTAL_LEDEN
assert AANTAL_ENVELOPPEN == AANTAL_NIET_BETAALD, 'het filter filtert iets anders'


def adresblok(lid):
    return [' '.join(str(lid.veld(v)) for v in regel)
            for regel in g.ENVELOP_GEADRESSEERDE]


ENVELOP_VOORBEELD_LID = ENVELOPPEN[0]
ENVELOP_VOORBEELD = adresblok(ENVELOP_VOORBEELD_LID)
# de vraag gaat over de LAATSTE envelop, niet over het voorbeeld
ENVELOP_LAATSTE = ENVELOPPEN[-1]
assert ENVELOP_LAATSTE is not ENVELOP_VOORBEELD_LID, (
    'er is maar één envelop')
assert len([l for l in ENVELOPPEN
            if l.achternaam == ENVELOP_LAATSTE.achternaam]) == 1, (
    'de achternaam van de laatste envelop komt twee keer voor')

# ====================================================================
#  stap 3 — de brief
# ====================================================================
AANTAL_BRIEVEN = AANTAL_LEDEN
_rveld, _rwaarde = g.BRIEF_REGEL
MET_AANMANING = [l for l in LEDEN if l.veld(_rveld) == _rwaarde]
AANTAL_AANMANING = len(MET_AANMANING)


def brieftabel(lid):
    """De tabel in de brief: het opschrift links, de waarde rechts."""
    uit = []
    for opschrift, veld in g.BRIEF_TABEL:
        if veld is None:
            uit.append([opschrift, g.CLUB_REKENING])
        else:
            uit.append([opschrift, str(lid.veld(veld))])
    return uit


TABEL_VOORBEELD = brieftabel(VOORBEELD)
# de twee vragen over de brief gaan over ANDERE leden dan het voorbeeld
VOORBEELD_LIDGELD = _een([l for l in LEDEN if l.naam == 'Jonas Peeters'],
                         'het lid van de lidgeldvraag')
VOORBEELD_DAG = _een([l for l in LEDEN if l.naam == 'Bilal Claes'],
                     'het lid van de trainingsdagvraag')
assert VOORBEELD_LIDGELD.lidgeld_tekst != VOORBEELD.lidgeld_tekst, (
    'de lidgeldvraag gaat over hetzelfde bedrag als het voorbeeld')
assert VOORBEELD_DAG.trainingsdag != VOORBEELD.trainingsdag, (
    'de dagvraag gaat over dezelfde dag als het voorbeeld')

# ====================================================================
#  stap 4 — de ploeglijst
# ====================================================================
LIJST_LEDEN = sorted([l for l in LEDEN if l.ploeg == g.LIJST_BLAD_PLOEG],
                     key=lambda l: l.achternaam)
LIJST_RIJEN = [[str(l.veld(k)) for k in g.LIJST_KOLOMMEN] for l in LIJST_LEDEN]
AANTAL_LIJSTRIJEN = len(LIJST_RIJEN)
LIJST_EERSTE = LIJST_LEDEN[0]
# Het voorbeeld in de opdracht toont een ANDERE ploeg. Anders staan de twee
# antwoorden van deze stap (het aantal regels en de bovenste achternaam) al
# in de opdracht te lezen en hoeven ze de lijst niet te maken.
_andere = [p for p in g.PLOEGORDE
           if p != g.LIJST_BLAD_PLOEG
           and PER_PLOEG[p] != len([l for l in LEDEN
                                    if l.ploeg == g.LIJST_BLAD_PLOEG])]
assert _andere, 'geen andere ploeg om het lijstvoorbeeld mee te tonen'
VOORBEELD_LIJST_PLOEG = _andere[0]
VOORBEELD_LIJST_LEDEN = sorted(
    [l for l in LEDEN if l.ploeg == VOORBEELD_LIJST_PLOEG],
    key=lambda l: l.achternaam)
VOORBEELD_LIJST_RIJEN = [[str(l.veld(k)) for k in g.LIJST_KOLOMMEN]
                         for l in VOORBEELD_LIJST_LEDEN]
# de bovenste achternaam moet onbetwistbaar de eerste zijn, ook als Word
# spaties anders sorteert dan Python
assert all(LIJST_EERSTE.achternaam[0] < l.achternaam[0]
           for l in LIJST_LEDEN[1:]), (
    'de bovenste achternaam begint met dezelfde letter als een andere — dan '
    'hangt het antwoord af van hoe Word sorteert')
AANTAL_PLOEGEN = len(PER_PLOEG)

# ====================================================================
#  stap 5 — het tornooi
# ====================================================================
class Club:
    def __init__(self, rij):
        (self.club, self.aanspreking, self.voornaam, self.naam, straat,
         nummer, postcode, gemeente, self.categorie,
         self.aantal_ploegen) = rij
        self.adresregel = f'{straat} {nummer}'
        self.woonplaats = f'{postcode} {gemeente}'
        self.geld = self.aantal_ploegen * g.TORN_PER_PLOEG
        self.geld_tekst = g.euro(self.geld)
        self.extra_zin = self.aantal_ploegen >= g.TORN_GROOT

    def rij(self):
        return [self.club, self.aanspreking, self.voornaam, self.naam,
                self.adresregel, self.woonplaats, self.categorie,
                self.aantal_ploegen, self.geld, self.geld_tekst]


CLUBS = [Club(r) for r in g.TORNOOI_RUW]
AANTAL_CLUBS = len(CLUBS)
PER_CATEGORIE = collections.Counter(c.categorie for c in CLUBS)
CLUBS_EINDLIJST = [c for c in CLUBS if c.categorie == g.TORN_EIND_CATEGORIE]
AANTAL_EINDLIJST = len(CLUBS_EINDLIJST)
MET_EXTRA = [c for c in CLUBS if c.extra_zin]
AANTAL_EXTRA = len(MET_EXTRA)
TORN_TOTAAL = sum(c.geld for c in CLUBS)
TORN_TOTAAL_TEKST = g.euro(TORN_TOTAAL)
CLUB_VOORBEELD = CLUBS[0]

# ====================================================================
#  het antwoordblad
# ====================================================================
ANTWOORDBLAD = [
    # ---- stap 1, de lidkaarten
    (1, 'Hoeveel lidkaarten passen er op één blad?', g.ETIKET_PER_BLAD),
    (1, f'Hoeveel bladen heb je nodig voor {AANTAL_LEDEN} leden?',
     ETIKET_BLADEN),
    (1, 'Hoeveel kaarten blijven er leeg op het laatste blad?', ETIKET_LEEG),
    (1, 'Probeer het eens in de verkeerde volgorde: breng de opmaak pas ná '
        'Labels bijwerken aan. Op hoeveel kaarten staat de opmaak dan?', 1),
    # ---- stap 2, de enveloppen
    (2, 'Welke achternaam staat op de LAATSTE envelop?',
     ENVELOP_LAATSTE.achternaam),
    (2, f'Hoeveel enveloppen blijven er over met het filter op '
        f'{g.ENVELOP_FILTER[0]} = {g.ENVELOP_FILTER[1]}?', AANTAL_ENVELOPPEN),
    (2, 'Hoeveel enveloppen zou je krijgen zonder dat filter?',
     AANTAL_ZONDER_FILTER),
    # ---- stap 3, de brief
    (3, f'Welk lidgeld staat er in de tabel in de brief van '
        f'{VOORBEELD_LIDGELD.naam}?', VOORBEELD_LIDGELD.lidgeld_tekst),
    (3, f'Welke trainingsdag staat er in de brief van {VOORBEELD_DAG.naam}?',
     VOORBEELD_DAG.trainingsdag),
    (3, 'Hoeveel brieven krijgen de aanmaningszin?', AANTAL_AANMANING),
    # ---- stap 4, de ploeglijst
    (4, f'Hoeveel rijen staan er in de lijst van {g.LIJST_BLAD_PLOEG}?',
     AANTAL_LIJSTRIJEN),
    (4, f'Welke achternaam staat bovenaan als je op {g.LIJST_SORTEER} '
        'sorteert?', LIJST_EERSTE.achternaam),
    (4, 'Wat gebeurt er als je de koprij IN het hoofddocument zet in plaats '
        'van in het samengevoegde resultaat?',
     'hij komt bij elk lid opnieuw'),
    # ---- stap 5, het tornooi
    (5, f'Hoeveel clubs schrijven in voor categorie {g.TORN_EIND_CATEGORIE}?',
     AANTAL_EINDLIJST),
    (5, f'Hoeveel clubs krijgen de extra zin over {g.TORN_GROOT} ploegen?',
     AANTAL_EXTRA),
    (5, 'Wat is het totale inschrijvingsgeld van alle clubs samen?',
     TORN_TOTAAL_TEKST),
]
ANTW_BLAD = "Antwoorden"
ANTW_KOP = ["Stap", "Vraag", "Antwoord"]
ANTW_KOPRIJ = 1
ANTW_START = ANTW_KOPRIJ + 1
ANTW_EIND = ANTW_START + len(ANTWOORDBLAD) - 1


def _tabel(koppen, rijen):
    breed = [max([len(str(k))] + [len(str(r[i])) for r in rijen])
             for i, k in enumerate(koppen)]
    lijn = '  '.join(str(k).ljust(breed[i]) for i, k in enumerate(koppen))
    uit = [lijn, '-' * len(lijn)]
    for r in rijen:
        uit.append('  '.join(str(w).ljust(breed[i]) for i, w in enumerate(r)))
    return '\n'.join(uit)


if __name__ == '__main__':
    print('=' * 104); print(g.TITEL); print('=' * 104)

    print('\n--- de ledenlijst, zoals ze klaarstaat ------------------------')
    print(_tabel(g.LEDEN_KOP,
                 [[l.lidnummer, l.voornaam, l.achternaam, l.adresregel,
                   l.woonplaats, l.ploeg, l.geboortejaar, l.trainer,
                   l.trainingsdag, l.trainingsuur, int(l.lidgeld),
                   l.lidgeld_tekst, l.betaald, g.datum(l.vervaldatum),
                   l.vervaldatum_tekst] for l in LEDEN]))
    print(f'\n  {AANTAL_LEDEN} leden, '
          + '   '.join(f'{p} {PER_PLOEG[p]}' for p in g.PLOEGORDE)
          + f'   niet betaald: {AANTAL_NIET_BETAALD}')

    print('\n--- stap 1  de lidkaart --------------------------------------')
    print(f'  {g.ETIKET_SOORT}')
    print(f'  {AANTAL_LEDEN} kaarten = {ETIKET_BLADEN} bladen, '
          f'{ETIKET_LAATSTE} op het laatste, {ETIKET_LEEG} leeg')
    print(f'  de kaart van {VOORBEELD.naam}:')
    for i, (regel, tekst) in enumerate(zip(g.LIDKAART, KAART_VOORBEELD), 1):
        opmaak = f"{regel['grootte']} pt"
        if regel['vet']:
            opmaak += ', vet'
        if regel['cursief']:
            opmaak += ', cursief'
        if regel['kleur'] != 'zwart':
            opmaak += f", {regel['kleur']}"
        print(f'     regel {i}  {tekst:<42} {opmaak}, '
              f'{g.LIDKAART_UITLIJNING}')

    print('\n--- stap 2  de envelop ---------------------------------------')
    print(f'  formaat {g.ENVELOP_FORMAAT}')
    print(f'  afzender ({g.ENVELOP_AFZENDER_GROOTTE} pt): '
          + ' / '.join(g.ENVELOP_AFZENDER))
    print(f'  filter {g.ENVELOP_FILTER[0]} = {g.ENVELOP_FILTER[1]} -> '
          f'{AANTAL_ENVELOPPEN} van de {AANTAL_LEDEN} enveloppen')
    print(f'  de eerste ({ENVELOP_VOORBEELD_LID.naam}): '
          + ' / '.join(ENVELOP_VOORBEELD))

    print('\n--- stap 3  de brief -----------------------------------------')
    print(f'  {AANTAL_BRIEVEN} brieven, {AANTAL_AANMANING} met de '
          'aanmaningszin')
    print(f'  de tabel in de brief van {VOORBEELD.naam}:')
    print(_tabel(['Opschrift', 'Waarde'], TABEL_VOORBEELD))
    print(f'  rechtse tabstop voor de datum op {g.BRIEF_TABSTOP_CM:g} cm')

    print('\n--- stap 4  de ploeglijst ------------------------------------')
    print(f'  filter op ploeg {g.LIJST_BLAD_PLOEG}, gesorteerd op '
          f'{g.LIJST_SORTEER}')
    print(_tabel(g.LIJST_KOLOMMEN, LIJST_RIJEN))
    print(f'\n  {AANTAL_LIJSTRIJEN} rijen; bovenaan '
          f'{LIJST_EERSTE.achternaam}')

    print('\n--- stap 5  het tornooi (eindopdracht) ----------------------')
    print(_tabel(['Club', 'Aanhef', 'Adresregel', 'Woonplaats', 'Cat.',
                  'Ploegen', 'Geld', 'Extra zin'],
                 [[c.club, f'Geachte {c.aanspreking} {c.naam}', c.adresregel,
                   c.woonplaats, c.categorie, c.aantal_ploegen, c.geld_tekst,
                   'ja' if c.extra_zin else 'nee'] for c in CLUBS]))
    print(f'\n  {AANTAL_CLUBS} clubs, '
          + '   '.join(f'{k} {PER_CATEGORIE[k]}' for k in g.TORN_CATEGORIEEN)
          + f'   extra zin: {AANTAL_EXTRA}   totaal: {TORN_TOTAAL_TEKST}')

    print('\n--- het antwoordblad ----------------------------------------')
    print(_tabel(['Stap', 'Vraag', 'Antwoord'],
                 [[st, v[:66], a] for st, v, a in ANTWOORDBLAD]))
    print('\n' + g.WAARSCHUWING)
