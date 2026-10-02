# -*- coding: utf-8 -*-
"""Bouwt het startbestand van de uitdagingsopdracht.

Bewust kaal: de opmaak hoort bij de opdracht. Alleen de kolombreedtes staan
goed, en de twee brontabellen (de tarievenstaffel en het grensblok) hebben
een vette kop zodat meteen duidelijk is dat ze niet aangepast mogen worden.
"""
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

UIT = os.path.join(HIER, 'halloween-startbestand.xlsx')
TITELFONT = Font(bold=True, size=13)
VET = Font(bold=True)
TIJD = 'hh:mm'

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
    'Je bent de coördinator van de Halloweennacht op Kasteel Ravenstein.',
    'De avond is voorbij, de laatste bezoekers zijn buiten, en er zijn twee',
    'dingen te doen.',
    '',
    'Eén: de avond afsluiten. Hoeveel volk is er geweest, welke attractie',
    'trok het meest, wat heeft het opgebracht, wat heeft het gekost?',
    '',
    'Twee: er is een probleem. De Zilveren Pompoen, de trofee die elk jaar',
    'in de schatkamer staat, is weg. Tussen tien en elf uur \'s avonds.',
    'Vijf mensen hebben iets gezien of geregistreerd. Hun verklaringen staan',
    'in je opdrachtbundel. Met de gegevens in dit bestand kom je bij één naam.',
    '',
    'Blad 1 Boekingen    — de ticketverkoop, met een staffelprijs',
    'Blad 2 Attracties   — bezoekers per attractie per uur',
    'Blad 3 Ploegen      — wie werkte van wanneer tot wanneer',
    'Blad 4 Verdachten   — de acht mensen die in aanmerking komen',
    'Blad 5 Afrekening   — opbrengst, kosten en winst van de avond',
    '',
    'De bladen hangen aan elkaar. Blad 4 heeft blad 3 nodig, blad 5 heeft',
    'blad 1 én blad 3 nodig. Typ nooit een getal over van het ene blad naar',
    'het andere: verwijs ernaar.',
    '',
    'Sla het bestand eerst op onder je eigen naam.',
], start=2):
    ws.cell(row=i, column=1, value=r)
breedtes(ws, [92])

# ------------------------------------------------------------ 1 Boekingen
ws = blad('1 Boekingen', 'Boekingen voor de Halloweennacht')
koprij(ws, 3, g.B1_KOP)
for r, (nr, groep, personen, slot, kanaal) in enumerate(g.B1, start=g.B1_START):
    ws.cell(row=r, column=1, value=nr)
    ws.cell(row=r, column=2, value=groep)
    ws.cell(row=r, column=3, value=personen)
    ws.cell(row=r, column=4, value=slot)
    ws.cell(row=r, column=5, value=kanaal)
labels(ws, g.B1_ANTWOORD, [
    'Totaal aantal bezoekers',
    'Totale ticketomzet',
    f'Omzet online vanaf {g.B1_GROOT} personen',
    f'Kassaboekingen onder {g.B1_KLEIN} personen',
    'Gemiddelde groep online',
    'Grootste groep (personen)',
    'Grootste groep (naam)',
])
ws['I2'] = 'Tarievenstaffel — niet aanpassen'
ws['I2'].font = VET
koprij(ws, 3, g.B1_TARIEFKOP, start_kolom=9)
for r, (vanaf, omschrijving, prijs) in enumerate(g.B1_TARIEVEN, start=g.B1_TAR_START):
    ws.cell(row=r, column=9, value=vanaf)
    ws.cell(row=r, column=10, value=omschrijving)
    ws.cell(row=r, column=11, value=prijs)
breedtes(ws, [10, 24, 11, 10, 10, 11, 11, 3, 8, 22, 11])

# ----------------------------------------------------------- 2 Attracties
ws = blad('2 Attracties', 'Bezoekers per attractie per uurblok')
koprij(ws, 3, ['Attractie'] + g.B2_UREN + ['Totaal'])
for r, (naam, waarden) in enumerate(g.B2, start=g.B2_START):
    ws.cell(row=r, column=1, value=naam)
    for k, aantal in enumerate(waarden, start=2):
        ws.cell(row=r, column=k, value=aantal)
ws.cell(row=g.B2_TOTAALRIJ, column=1, value='Totaal per uurblok')
labels(ws, g.B2_ANTWOORD, [
    'Drukste attractie',
    'Drukste uurblok',
    'Op één na drukste attractie',
    'Aandeel van de drukste attractie',
])
breedtes(ws, [30, 9, 9, 9, 9, 9, 10])

# -------------------------------------------------------------- 3 Ploegen
ws = blad('3 Ploegen', 'Ploegen van 31 oktober')
koprij(ws, 3, g.B3_KOP)
for r, (naam, rol, post, start, einde) in enumerate(g.B3, start=g.B3_START):
    ws.cell(row=r, column=1, value=naam)
    ws.cell(row=r, column=2, value=rol)
    ws.cell(row=r, column=3, value=post)
    c = ws.cell(row=r, column=4, value=start)
    c.number_format = TIJD
    c = ws.cell(row=r, column=5, value=einde)
    c.number_format = TIJD
labels(ws, g.B3_SAMENVATTING, [
    f'Aantal {g.B3_ROL_TELLEN.lower()}en',
    'Aantal in de nachtploeg',
    f'{g.B3_ROL_KRUIS[0]} op de {g.B3_ROL_KRUIS[1].lower()}',
    'Totaal gewerkte uren',
    f'Gemiddelde dienst van de {g.B3_ROL_TELLEN.lower()}en',
    'Langste dienst (uren)',
    'Wie werkte het langst',
])
ws['I2'] = 'Nachtploeg — niet aanpassen'
ws['I2'].font = VET
ws['I3'] = 'Gestopt later dan'
ws['J3'] = g.B3_GRENS_TIJD
ws['J3'].number_format = TIJD
ws['I4'] = 'En minstens (uren)'
ws['J4'] = g.B3_GRENS_UREN
breedtes(ws, [30, 11, 14, 9, 9, 9, 13, 3, 19, 10])

# ----------------------------------------------------------- 4 Verdachten
ws = blad('4 Verdachten', 'De acht verdachten')
ws['A2'] = 'Dief nog aan het werk na'
ws['B2'] = g.B4_TIJDSTIP
ws['B2'].number_format = TIJD
ws['A3'] = 'Kleur van de schim'
ws['B3'] = g.B4_KLEUR
koprij(ws, g.B4_KOPRIJ, g.B4_KOP)
for r, (naam, badge, kostuum, tas, alibi) in enumerate(g.B4, start=g.B4_START):
    ws.cell(row=r, column=1, value=naam)
    ws.cell(row=r, column=2, value=badge)
    ws.cell(row=r, column=3, value=kostuum)
    ws.cell(row=r, column=4, value=tas)
    ws.cell(row=r, column=5, value=alibi)
labels(ws, g.B4_ANTWOORD, [
    'Hoeveel blijven er over',
    'Naam van de dader',
])
breedtes(ws, [26, 18, 11, 10, 20, 13, 13])

# ---------------------------------------------------------- 5 Afrekening
ws = blad('5 Afrekening', 'Afrekening van de avond')
R = g.B5_RIJ
ws['A3'] = 'Opbrengsten'
ws['A3'].font = VET
ws.cell(row=R['ticket'], column=1, value='Ticketomzet (blad 1)')
ws.cell(row=R['bar'], column=1, value='Baromzet')
ws.cell(row=R['bar'], column=2, value=g.B5_BAROMZET)
ws.cell(row=R['opbrengst'], column=1, value='Totale opbrengst')
ws['A8'] = 'Kosten'
ws['A8'].font = VET
ws.cell(row=R['uren'], column=1, value='Gewerkte uren (blad 3)')
ws.cell(row=R['uurloon'], column=1, value='Uurloon')
ws.cell(row=R['uurloon'], column=2, value=g.B5_UURLOON)
ws.cell(row=R['loonkost'], column=1, value='Loonkost')
ws.cell(row=R['decor'], column=1, value='Decor en techniek')
ws.cell(row=R['decor'], column=2, value=g.B5_DECOR)
ws.cell(row=R['catering'], column=1, value='Catering')
ws.cell(row=R['catering'], column=2, value=g.B5_CATERING)
ws.cell(row=R['kosten'], column=1, value='Totale kosten')
ws['A16'] = 'Resultaat'
ws['A16'].font = VET
ws.cell(row=R['winst'], column=1, value='Winst van de avond')
ws.cell(row=R['marge'], column=1, value='Winstmarge')
ws.cell(row=R['per_bezoeker'], column=1, value='Opbrengst per bezoeker')
breedtes(ws, [28, 14])

wb.save(UIT)
print('geschreven:', UIT)
print('bladen:', wb.sheetnames)
print(f'  blad 1 boekingen   rij {g.B1_START}-{g.B1_EIND}, '
      f'antwoorden {g.B1_ANTWOORD}-{g.B1_ANTWOORD + 6}, staffel '
      f'rij {g.B1_TAR_START}-{g.B1_TAR_EIND}')
print(f'  blad 2 attracties  rij {g.B2_START}-{g.B2_EIND}, '
      f'totaalrij {g.B2_TOTAALRIJ}, antwoorden {g.B2_ANTWOORD}-{g.B2_ANTWOORD + 3}')
print(f'  blad 3 ploegen     rij {g.B3_START}-{g.B3_EIND}, '
      f'antwoorden {g.B3_SAMENVATTING}-{g.B3_SAMENVATTING + 6}')
print(f'  blad 4 verdachten  rij {g.B4_START}-{g.B4_EIND}, '
      f'antwoorden {g.B4_ANTWOORD}-{g.B4_ANTWOORD + 1}')
print(f'  blad 5 afrekening  {g.B5_RIJ}')
