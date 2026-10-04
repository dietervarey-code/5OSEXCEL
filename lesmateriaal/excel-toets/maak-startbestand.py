# -*- coding: utf-8 -*-
"""Bouwt het startbestand van de toets. Bewust kaal: de opmaak hoort bij de
   opdracht. Alleen de kolommen staan breed genoeg en de twee brontabellen
   hebben een vette kop, zodat duidelijk is dat ze niet aangepast mogen worden."""
import importlib.util
import os
import sys
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

UIT = os.path.join(HIER, 'rodeduivels-toets-startbestand.xlsx')
TITELFONT = Font(bold=True, size=13)
VET = Font(bold=True)

wb = Workbook()


def breedtes(ws, waarden):
    for i, b in enumerate(waarden, start=1):
        ws.column_dimensions[get_column_letter(i)].width = b


def koprij(ws, rij, koppen, start_kolom=1):
    for i, k in enumerate(koppen, start=start_kolom):
        ws.cell(row=rij, column=i, value=k)


def labels(ws, start_rij, teksten, kolom=1):
    for i, t in enumerate(teksten):
        ws.cell(row=start_rij + i, column=kolom, value=t)


def blad(naam, titel):
    ws = wb.create_sheet(naam)
    ws['A1'] = titel
    ws['A1'].font = TITELFONT
    return ws


# ------------------------------------------------------------------ Start
ws = wb.active
ws.title = 'Start'
ws['A1'] = g.TITEL
ws['A1'].font = Font(bold=True, size=16)
for i, r in enumerate([
    g.ONDERTITEL,
    '',
    'Naam: ......................................    Klas: ..........',
    '',
    'Vijf werkbladen, samen 50 minuten en 50 punten. Werk ze in volgorde af.',
    'Op elk blad staat wat er moet uitkomen. Hoe je de formule maakt, weet je zelf.',
    '',
    'Blad 1 Selectie        13 min   12 punten',
    'Blad 2 Wedstrijden     11 min   10 punten',
    'Blad 3 Clubdoelpunten  10 min    9 punten',
    'Blad 4 Tickets          8 min    9 punten',
    'Blad 5 Wedstrijdblad    8 min   10 punten',
    '',
    'Spelregels',
    '  1. Reken nooit iets uit met je rekenmachine om het daarna over te typen.',
    '     Een ingetypt getal telt niet mee, ook niet als het juist is.',
    '  2. Typ een formule één keer en voer ze door met de vulgreep.',
    '  3. Controleer na het doorvoeren altijd de laatste rij van je kolom.',
    '  4. Bij elk blad hoort opmaak. Die staat mee op de punten.',
    '  5. Elk blad eindigt met een controle die je zelf kunt doen. Doe ze ook.',
    '',
    'EERST DOEN: sla dit bestand op als  toets-jouwnaam.xlsx',
    '',
    g.WAARSCHUWING,
], start=2):
    ws.cell(row=i, column=1, value=r)
ws['A15'].font = VET
ws['A23'].font = VET
ws['A25'].font = Font(italic=True)
breedtes(ws, [84])

# ------------------------------------------------------------- 1 Selectie
ws = blad('1 Selectie', 'De selectie van de Rode Duivels')
ws['A2'] = 'Ervaren vanaf (caps)'
ws['B2'] = g.B1_ERVAREN
koprij(ws, g.B1_KOPRIJ, g.B1_KOP)
for r, (speler, positie, leeftijd, caps, doelpunten) in enumerate(g.B1, start=g.B1_START):
    ws.cell(row=r, column=1, value=speler)
    ws.cell(row=r, column=2, value=positie)
    ws.cell(row=r, column=3, value=leeftijd)
    ws.cell(row=r, column=4, value=caps)
    ws.cell(row=r, column=5, value=doelpunten)
labels(ws, g.B1_SAMENVATTING, [
    'Totaal aantal caps',
    'Totaal aantal doelpunten',
    'Gemiddelde leeftijd',
    'Leeftijd oudste speler',
    'Leeftijd jongste speler',
    'Aantal spelers',
    'Aantal ervaren spelers',
])
breedtes(ws, [25, 14, 10, 8, 12, 11])

# ---------------------------------------------------------- 2 Wedstrijden
ws = blad('2 Wedstrijden', 'De acht wedstrijden van dit seizoen')
koprij(ws, g.B2_KOPRIJ, g.B2_KOP)
for r, (datum, tegenstander, waar, voor, tegen) in enumerate(g.B2, start=g.B2_START):
    ws.cell(row=r, column=1, value=datum)
    ws.cell(row=r, column=2, value=tegenstander)
    ws.cell(row=r, column=3, value=waar)
    ws.cell(row=r, column=4, value=voor)
    ws.cell(row=r, column=5, value=tegen)
ws.cell(row=g.B2_TOTAAL, column=1, value='Totaal')
labels(ws, g.B2_ANTWOORD, [
    'Aantal gewonnen wedstrijden',
    'Gemiddeld gescoord per match',
    'Grootste doelpuntensaldo',
])
breedtes(ws, [29, 15, 13, 8, 8, 9, 12])

# ------------------------------------------------------- 3 Clubdoelpunten
ws = blad('3 Clubdoelpunten', 'Doelpunten bij hun club dit seizoen')
koprij(ws, g.B3_KOPRIJ, g.B3_KOP)
for r, (speler, positie, doelpunten, assists) in enumerate(g.B3, start=g.B3_START):
    ws.cell(row=r, column=1, value=speler)
    ws.cell(row=r, column=2, value=positie)
    ws.cell(row=r, column=3, value=doelpunten)
    ws.cell(row=r, column=4, value=assists)
# De vier posities staan er al: die dienen als criterium in de formules.
koprij(ws, g.B3_SAMENVATTING, ['Positie', 'Aantal spelers', 'Doelpunten'])
for i, positie in enumerate(g.POSITIES):
    ws.cell(row=g.B3_PER_POSITIE + i, column=1, value=positie)
ws.cell(row=g.B3_CONTROLE, column=1, value='Controle: alle doelpunten samen')
breedtes(ws, [24, 15, 13, 10])

# -------------------------------------------------------------- 4 Tickets
ws = blad('4 Tickets', 'Ticketprijzen voor een thuiswedstrijd')
ws['A2'] = 'Korting voor abonnees'
ws['B2'] = g.B4_KORTING
koprij(ws, g.B4_KOPRIJ, g.B4_KOP)
for r, (vak, prijs) in enumerate(g.B4, start=g.B4_START):
    ws.cell(row=r, column=1, value=vak)
    ws.cell(row=r, column=2, value=prijs)
ws.cell(row=g.B4_TOTAAL, column=1, value='Totaal')
breedtes(ws, [26, 15, 13, 15])

# --------------------------------------------------------- 5 Wedstrijdblad
ws = blad('5 Wedstrijdblad', 'Wedstrijdblad België - Portugal')
koprij(ws, g.B5_KOPRIJ, g.B5_KOP)
for r, (rugnummer, minuten) in enumerate(g.B5_BASIS, start=g.B5_START):
    ws.cell(row=r, column=1, value=rugnummer)
    ws.cell(row=r, column=4, value=minuten)
labels(ws, g.B5_ANTWOORD, [
    'Totaal gespeelde minuten',
    'Verdedigers in de basiself',
    'Gemiddeld aantal minuten',
])
ws['F2'] = 'Spelerslijst — niet aanpassen'
ws['F2'].font = VET
koprij(ws, g.B5_KOPRIJ, g.B5_ZOEKKOP, start_kolom=6)
for r, (rugnummer, speler, positie) in enumerate(g.B5_TABEL, start=g.B5_TAB_START):
    ws.cell(row=r, column=6, value=rugnummer)
    ws.cell(row=r, column=7, value=speler)
    ws.cell(row=r, column=8, value=positie)
breedtes(ws, [27, 24, 14, 10, 3, 12, 24, 14])

wb.save(UIT)
print('geschreven:', UIT)
print('bladen:', wb.sheetnames)
print(f'  blad 1 selectie       rij {g.B1_START}-{g.B1_EIND}, '
      f'samenvatting {g.B1_SAMENVATTING}-{g.B1_SAMENVATTING + 6}')
print(f'  blad 2 wedstrijden    rij {g.B2_START}-{g.B2_EIND}, totaalrij {g.B2_TOTAAL}, '
      f'antwoorden {g.B2_ANTWOORD}-{g.B2_ANTWOORD + 2}')
print(f'  blad 3 clubdoelpunten rij {g.B3_START}-{g.B3_EIND}, '
      f'blokje {g.B3_SAMENVATTING}-{g.B3_PER_POSITIE + len(g.POSITIES) - 1}, '
      f'controle {g.B3_CONTROLE}')
print(f'  blad 4 tickets        rij {g.B4_START}-{g.B4_EIND}, totaalrij {g.B4_TOTAAL}')
print(f'  blad 5 wedstrijdblad  rij {g.B5_START}-{g.B5_EIND}, '
      f'antwoorden {g.B5_ANTWOORD}-{g.B5_ANTWOORD + 2}, '
      f'spelerslijst rij {g.B5_TAB_START}-{g.B5_TAB_EIND}')
