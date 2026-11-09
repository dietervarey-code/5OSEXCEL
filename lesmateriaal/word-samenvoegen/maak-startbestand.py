# -*- coding: utf-8 -*-
"""Bouwt het startbestand: de lijsten die Word straks leest.

Elk blad is met opzet samenvoegklaar: één koprij op rij 3, geen samengevoegde
cellen, geen lege rij in de lijst en niets eronder. De peildatum staat op B1
van elk blad, zodat de formule van stap 1 er met $B$1 naar kan verwijzen.

De kolommen die de leerling maakt, blijven leeg. controleer.py kijkt dat na.
"""
import importlib.util
import os
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')

UIT = os.path.join(HIER, o.STARTBESTAND)
GROOT = Font(bold=True, size=16)
VET = Font(bold=True)
SCHUIN = Font(italic=True, size=10)
TEMAKEN = Font(bold=True, italic=True, color='B04A00')

wb = Workbook()


def breedtes(ws, waarden, start=1):
    for i, b in enumerate(waarden, start=start):
        ws.column_dimensions[get_column_letter(i)].width = b


def blad(naam):
    """Een blad met NIETS boven de koprij.

    Word neemt de eerste gebruikte rij van een werkblad als kolomnamen. Een
    titel of een voetnoot erboven maakt de hele samenvoeging stuk. Daarom
    staat op deze bladen alleen de lijst, en staat de peildatum op het blad
    Start — zie fiche 1.
    """
    return wb.create_sheet(naam)


def lijst(ws, koprij, koppen, rijen, klaar):
    """koppen tot `klaar` staan gevuld; de rest is de kolommen die zij maken."""
    for i, k in enumerate(koppen, start=1):
        c = ws.cell(row=koprij, column=i, value=k)
        c.font = VET if i <= klaar else TEMAKEN
    for r, waarden in enumerate(rijen, start=koprij + 1):
        for i, w in enumerate(waarden, start=1):
            c = ws.cell(row=r, column=i, value=w)
            if hasattr(w, 'year'):
                c.number_format = g.DATUMNOTATIE


# ------------------------------------------------------------------- Start
ws = wb.active
ws.title = g.START_BLAD
ws.cell(row=g.PEILRIJ, column=1, value=g.PEIL_LABEL).font = VET
c = ws.cell(row=g.PEILRIJ, column=g.PEILKOLOM, value=g.FESTIVALDAG)
c.number_format = g.DATUMNOTATIE
c.font = VET
ws['A3'] = g.TITEL
ws['A3'].font = GROOT
KOP = 'Vier regels die altijd gelden'
regels = [
    g.ONDERTITEL, '',
    'Naam: ......................................    Klas: ..........', '',
    f'De peildatum hierboven is de eerste festivaldag. In stap 1 verwijs je',
    f'er met {g.PEILCEL} naar. Hij staat op DIT blad en niet bij de lijst,',
    'want op een blad dat Word moet lezen, mag niets boven de koprij staan.',
    '',
    f'{g.LESUREN} lesuren, vijf stappen. De eerste in Excel, de drie daarna',
    'in Word, en de vijfde doe je zelf van begin tot eind.',
    'De uitleg staat in een apart boekje: ' + o.THEORIEBUNDEL + '.',
    'Bij elke stap staat welke fiches je nodig hebt.', '',
]
for stap in o.STAPPEN:
    fiches = 'fiche ' + ', '.join(str(n) for n in stap['fiches'])
    regels.append(f"Stap {stap['nr']}  {stap['titel']:<32} "
                  f"{stap['waar']:<15} {stap['lesuren']} u   {fiches}")
regels += [
    '', KOP,
    '  1. Zet dit Excelbestand en je Worddocumenten in DEZELFDE map. Word',
    '     onthoudt waar je lijst staat; verplaats je ze, dan vindt hij ze niet.',
    '  2. De oranje kolomtitels zijn de kolommen die jij maakt. De zwarte',
    '     staan klaar — daar verander je niets aan.',
    '  3. Je typt een formule één keer, in de bovenste cel, en voert ze door.',
    '  4. Wat je op je scherm ziet, is niet altijd wat er in de cel staat.',
    '     Een uur en een bedrag zijn getallen; de euro en de dubbele punt zijn',
    '     opmaak. Opmaak gaat NIET mee naar Word. Daarvoor bestaat TEKST.',
    '',
    f'EERST DOEN: sla dit bestand op als  samenvoegen-jouwnaam.xlsx',
    '', g.WAARSCHUWING,
]
for i, r in enumerate(regels, start=4):
    ws.cell(row=i, column=1, value=r)
ws.cell(row=4 + regels.index(KOP), column=1).font = VET
rij_w = 4 + regels.index(g.WAARSCHUWING)
c = ws.cell(row=rij_w, column=1)
c.font = SCHUIN
c.alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[rij_w].height = 100
breedtes(ws, [100, 14])

# ----------------------------------------------------------- Vrijwilligers
ws = blad(g.VRIJ_BLAD)
lijst(ws, g.VRIJ_KOPRIJ, g.VRIJ_KOP,
      [tuple(r) + (None,) * (len(g.VRIJ_KOP) - g.VRIJ_KLAAR)
       for r in g.VRIJWILLIGERS], g.VRIJ_KLAAR)
breedtes(ws, [12, 15, 20, 9, 10, 13, 15, 10,
              16, 22, 18, 17, 10, 12, 9, 12])

# ------------------------------------------------------------------ Taken
ws = blad(g.TAKEN_BLAD)
lijst(ws, g.TAKEN_KOPRIJ, g.TAKEN_KOP, g.TAKEN, len(g.TAKEN_KOP))
for i in range(len(g.TAKEN)):
    r = g.TAKEN_START + i
    ws.cell(row=r, column=4).number_format = g.UURNOTATIE
    ws.cell(row=r, column=5).number_format = g.EURONOTATIE
breedtes(ws, [11, 18, 13, 11, 13])

# ---------------------------------------------------------------- Sponsors
ws = blad(g.SPON_BLAD)
lijst(ws, g.SPON_KOPRIJ, g.SPON_KOP,
      [tuple(r) + (None,) * (len(g.SPON_KOP) - g.SPON_KLAAR)
       for r in g.SPONSORS], g.SPON_KLAAR)
for i in range(len(g.SPONSORS)):
    ws.cell(row=g.SPON_START + i, column=10).number_format = g.EURONOTATIE
breedtes(ws, [22, 12, 13, 14, 20, 9, 10, 13, 9, 11,
              26, 22, 18, 16])

# -------------------------------------------------------------- Antwoorden
ws = blad(a.ANTW_BLAD)
for i, k in enumerate(a.ANTW_KOP, start=1):
    c = ws.cell(row=a.ANTW_KOPRIJ, column=i, value=k)
    c.font = VET if i < len(a.ANTW_KOP) else TEMAKEN
for i, (stap, vraag, _antwoord) in enumerate(a.ANTWOORDBLAD):
    r = a.ANTW_START + i
    ws.cell(row=r, column=1, value=stap)
    ws.cell(row=r, column=2, value=vraag)
breedtes(ws, [7, 74, 34])

wb.save(UIT)
print('geschreven:', UIT)
for ws in wb.worksheets:
    gevuld = sum(1 for rij in ws.iter_rows() for c in rij if c.value is not None)
    print(f'  {ws.title:<16} {gevuld:>4} gevulde cellen   {ws.dimensions}')
