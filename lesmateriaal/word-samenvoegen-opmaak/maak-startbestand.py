# -*- coding: utf-8 -*-
"""Bouwt het startbestand: drie lijsten die helemaal klaarstaan.

Er valt hier niets uit te rekenen. Dat is met opzet: deze bundel gaat over
Word, en elke minuut die aan een formule gaat, gaat niet naar de opmaak.

De bladen die Word leest bevatten NIETS boven of naast de lijst, en de koprij
staat op rij 1. Word neemt de eerste gebruikte rij van een werkblad als
kolomnamen; een titel erboven maakt de samenvoeging stuk.
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


def lijst(ws, koprij, koppen, rijen, oranje=()):
    for i, k in enumerate(koppen, start=1):
        c = ws.cell(row=koprij, column=i, value=k)
        c.font = TEMAKEN if k in oranje else VET
    for r, waarden in enumerate(rijen, start=koprij + 1):
        for i, w in enumerate(waarden, start=1):
            c = ws.cell(row=r, column=i, value=w)
            if hasattr(w, 'year') and not hasattr(w, 'hour'):
                c.number_format = g.DATUMNOTATIE


# ------------------------------------------------------------------- Start
ws = wb.active
ws.title = 'Start'
ws['A1'] = g.TITEL
ws['A1'].font = GROOT
KOP = 'Vier regels die altijd gelden'
regels = [
    g.ONDERTITEL, '',
    'Naam: ......................................    Klas: ..........', '',
    f'{g.LESUREN} lesuren, vijf stappen, allemaal in Word.',
    'In dit bestand hoef je NIETS uit te rekenen: de drie lijsten staan',
    'helemaal klaar. Elke minuut gaat naar Word en naar de opmaak.',
    '',
    f'De theorie staat in twee boekjes. {o.THEORIEBUNDEL} is nieuw en begint',
    f'bij fiche {14}. Het boekje van de vorige lessen',
    f'({g.VOORGANGER_THEORIE}) heb je ook nodig: daar staan de fiches 1 tot 13.',
    '',
]
for stap in o.STAPPEN:
    fiches = 'fiche ' + ', '.join(str(n) for n in stap['fiches'])
    regels.append(f"Stap {stap['nr']}  {stap['titel']:<26} "
                  f"{stap['soort']:<13} {stap['lesuren']} u   {fiches}")
regels += [
    '', KOP,
    '  1. Zet dit bestand en je Worddocumenten in DEZELFDE map, en laat ze',
    '     daar staan. Word onthoudt waar je lijst staat.',
    '  2. Werk nooit in het model dat je krijgt. Bestand, Opslaan als, met',
    '     je eigen naam erin.',
    '  3. Beoordeel opmaak NOOIT in de gewone weergave. Beeld,',
    '     Afdrukweergave, en zet de zoom op één volledige pagina.',
    '  4. Twee kolommen hebben een oranje titel: die bestaan alleen om in',
    '     Word te gebruiken. Het lidgeld en de vervaldatum staan er twee keer,',
    '     één keer als getal en één keer als tekst. Neem de tekstkolom.',
    '',
    'EERST DOEN: sla dit bestand op als  clubpost-jouwnaam.xlsx',
    '', g.WAARSCHUWING,
]
for i, r in enumerate(regels, start=3):
    ws.cell(row=i, column=1, value=r)
ws.cell(row=3 + regels.index(KOP), column=1).font = VET
rij_w = 3 + regels.index(g.WAARSCHUWING)
c = ws.cell(row=rij_w, column=1)
c.font = SCHUIN
c.alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[rij_w].height = 110
breedtes(ws, [104])

# -------------------------------------------------------------------- Leden
ws = wb.create_sheet(g.LEDEN_BLAD)
lijst(ws, g.LEDEN_KOPRIJ, g.LEDEN_KOP, [l.rij() for l in a.LEDEN],
      oranje=('Lidgeld in tekst', 'Vervaldatum in tekst'))
for i in range(len(a.LEDEN)):
    ws.cell(row=g.LEDEN_START + i, column=11).number_format = g.EURONOTATIE
breedtes(ws, [11, 11, 15, 22, 24, 8, 13, 15, 13, 12, 10, 15, 9, 13, 20])

# ------------------------------------------------------------------ Tornooi
ws = wb.create_sheet(g.TORN_BLAD)
lijst(ws, g.TORN_KOPRIJ, g.TORN_KOP, [c.rij() for c in a.CLUBS],
      oranje=('Inschrijvingsgeld in tekst',))
for i in range(len(a.CLUBS)):
    ws.cell(row=g.TORN_START + i, column=9).number_format = g.EURONOTATIE
breedtes(ws, [22, 13, 11, 13, 17, 24, 11, 15, 17, 24])

# --------------------------------------------------------------- Antwoorden
ws = wb.create_sheet(a.ANTW_BLAD)
for i, k in enumerate(a.ANTW_KOP, start=1):
    c = ws.cell(row=a.ANTW_KOPRIJ, column=i, value=k)
    c.font = TEMAKEN if i == len(a.ANTW_KOP) else VET
for i, (stap, vraag, _antwoord) in enumerate(a.ANTWOORDBLAD):
    r = a.ANTW_START + i
    ws.cell(row=r, column=1, value=stap)
    ws.cell(row=r, column=2, value=vraag)
breedtes(ws, [7, 78, 34])

wb.save(UIT)
print('geschreven:', UIT)
for ws in wb.worksheets:
    gevuld = sum(1 for rij in ws.iter_rows() for c in rij if c.value is not None)
    print(f'  {ws.title:<14} {gevuld:>4} gevulde cellen   {ws.dimensions}')
