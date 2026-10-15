# -*- coding: utf-8 -*-
"""Bouwt het startbestand van de streamingbundel.

Bewust kaal: de opmaak hoort bij de opdracht. Alleen de kolombreedtes staan
goed, zodat niemand tijd verliest met slepen.

De lijst op blad 2 is bron van allebei de draaitabellen. Daarom staat er geen
totaalrij onder, geen lege rij in, en staat het vragenblokje ERNAAST met één
lege kolom ertussen. Blad 3 volgt dezelfde discipline, zodat wie tijd over
heeft er ook een draaitabel van kan maken.

Er zit géén draaitabel in dit bestand: openpyxl kan die niet schrijven, en dat
komt goed uit — de leerling hoort ze zelf te maken.
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

UIT = os.path.join(HIER, 'streaming-startbestand.xlsx')
TITEL = Font(bold=True, size=13)
GROOT = Font(bold=True, size=16)
VET = Font(bold=True)
SCHUIN = Font(italic=True, size=10)

wb = Workbook()


def breedtes(ws, waarden, start=1):
    for i, b in enumerate(waarden, start=start):
        ws.column_dimensions[get_column_letter(i)].width = b


def koprij(ws, rij, koppen, kolom=1):
    for i, k in enumerate(koppen, start=kolom):
        ws.cell(row=rij, column=i, value=k)


def labels(ws, rij, teksten, kolom=1):
    for i, t in enumerate(teksten):
        ws.cell(row=rij + i, column=kolom, value=t)


def blad(naam, titel, ondertitel=None):
    ws = wb.create_sheet(naam)
    ws['A1'] = titel
    ws['A1'].font = TITEL
    if ondertitel:
        ws['A2'] = ondertitel
        ws['A2'].font = SCHUIN
    return ws


def vraagblok(ws, rij, kolom, vragen):
    ws.cell(row=rij, column=kolom, value='Vraag').font = VET
    ws.cell(row=rij, column=kolom + 1, value='Antwoord').font = VET
    labels(ws, rij + 1, vragen, kolom=kolom)


# ------------------------------------------------------------------- Start
ws = wb.active
ws.title = 'Start'
ws['A1'] = g.TITEL
ws['A1'].font = GROOT
labels(ws, 2, [
    g.ONDERTITEL,
    '',
    'Naam: ......................................    Klas: ..........',
    '',
    f'Vijf werkbladen, samen ongeveer {g.DUUR} minuten. Werk ze in volgorde af:',
    'blad 2 heeft blad 1 nodig, en blad 4 en 5 hebben blad 2 nodig.',
    '',
    'Blad 1  Genres        8 min   herhaling: rekenen, ALS, tellen',
    'Blad 2  Aanbod       12 min   herhaling: VERT.ZOEKEN uit de genretabel',
    'Blad 3  Schermtijd   10 min   herhaling: SOM, SOM.ALS, ALS',
    'Blad 4  Draaitabel   12 min   NIEUW: één lijst, twee draaitabellen',
    'Blad 5  Grafiek       8 min   NIEUW: een staafdiagram en een lijndiagram',
    '',
    'Wat je ernaast legt',
    f'  {g.FUNCTIEBUNDEL} — de functiefiches die je al kent, voor blad 1 tot 3.',
    f'  {g.THEORIEBUNDEL} — kaart 1 tot 9 voor blad 4, kaart 10 tot 14 voor blad 5.',
    '',
    'Twee regels over de lijsten',
    '  1. De lijst op blad 2 wordt de bron van allebei je draaitabellen. Voeg er',
    '     geen lege rij in en zet er geen totaalrij onder. De berekeningen staan',
    '     daarom ERNAAST, met een lege kolom ertussen. Hou dat zo.',
    '  2. Blad 4 en 5 hebben geen formules nodig. Daar wordt gesleept en getekend.',
    '',
    'Controleer jezelf',
    '  Onderaan elk blad in de opdrachtbundel staat een CONTROLEGETAL.',
    '  Komt jouw cel daarop uit, dan mag je verder. Typ het nooit zelf in.',
    '',
    'EERST DOEN: sla dit bestand op als  streaming-jouwnaam.xlsx',
    '',
    g.WAARSCHUWING,
])
for adres in ('A16', 'A20', 'A26'):
    ws[adres].font = VET
ws['A31'].font = SCHUIN
ws['A31'].alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[31].height = 86
breedtes(ws, [86])

# ----------------------------------------------------------------- 1 Genres
ws = blad('1 Genres', 'Lievelingsgenre: de peiling van 2024 en 2025',
          'Dit is ook de zoektabel voor blad 2. Verander er niets aan.')
ws[f'A{g.B1_KOPRIJ - 1}'] = g.B1_DREMPELTEKST
ws[f'B{g.B1_KOPRIJ - 1}'] = g.B1_DREMPEL
koprij(ws, g.B1_KOPRIJ, g.B1_KOP)
for r, (code, naam, oud, nieuw) in enumerate(g.B1, start=g.B1_START):
    ws.cell(row=r, column=1, value=code)
    ws.cell(row=r, column=2, value=naam)
    ws.cell(row=r, column=3, value=oud)
    ws.cell(row=r, column=4, value=nieuw)
labels(ws, g.B1_SAMENVATTING, [
    'Totale groei over alle genres',
    'Gemiddelde groei',
    'Sterkste groei',
    'Zwakste groei',
    'Aantal genres in de tabel',
    'Aantal sterk groeiende genres',
])
ws.cell(row=g.B1_SAMENVATTING + 7, column=1, value=g.B1_VOETNOOT).font = SCHUIN
breedtes(ws, [10, 17, 14, 14, 10, 15])

# ----------------------------------------------------------------- 2 Aanbod
ws = blad('2 Aanbod', 'Het aanbod: vijfendertig series en films', g.B2_VOETNOOT)
koprij(ws, g.B2_KOPRIJ, g.B2_KOP)
for r, (titel, soort, code, taal, jaar, kijkers) in enumerate(g.B2,
                                                              start=g.B2_START):
    ws.cell(row=r, column=1, value=titel)
    ws.cell(row=r, column=2, value=soort)
    ws.cell(row=r, column=3, value=code)
    ws.cell(row=r, column=4, value=taal)
    ws.cell(row=r, column=5, value=jaar)
    ws.cell(row=r, column=6, value=kijkers)
vraagblok(ws, g.B2_VRAAGRIJ, g.B2_VRAAGKOL, [
    'Gemiddeld aantal kijkers per titel',
    'Aantal titels in de lijst',
    f'Aantal titels van de soort {g.B2_TELSOORT}',
    f'Aantal {g.B2_TELTAAL}talige titels',
])
breedtes(ws, [34, 9, 12, 12, 8, 10, 16, 20, 15])
breedtes(ws, [3, 32, 12], start=g.B2_VRAAGKOL - 1)

# ------------------------------------------------------------- 3 Schermtijd
ws = blad('3 Schermtijd', 'De schermtijdenquête', g.B3_VOETNOOT)
ws[f'A{g.B3_KOPRIJ - 1}'] = g.B3_DREMPELTEKST
ws[f'B{g.B3_KOPRIJ - 1}'] = g.B3_DREMPEL
koprij(ws, g.B3_KOPRIJ, g.B3_KOP)
for r, (code, leeftijd, school, weekend) in enumerate(g.B3, start=g.B3_START):
    ws.cell(row=r, column=1, value=code)
    ws.cell(row=r, column=2, value=leeftijd)
    ws.cell(row=r, column=3, value=school)
    ws.cell(row=r, column=4, value=weekend)
vraagblok(ws, g.B3_VRAAGRIJ, g.B3_VRAAGKOL, [
    'Totale schermtijd van de groep',
    'Gemiddelde schermtijd per week',
    'Hoogste schermtijd',
    'Laagste schermtijd',
    'Aantal leerlingen met veel schermtijd',
    f'Schermtijd van alle {g.B3_LEEFTIJD}-jarigen samen',
    'Schermtijd van iedereen die veel kijkt',
])
breedtes(ws, [10, 10, 16, 18, 15, 9])
breedtes(ws, [3, 34, 12], start=g.B3_VRAAGKOL - 1)

# ------------------------------------------------------------- 4 Draaitabel
ws = blad('4 Draaitabel', 'Twee draaitabellen van dezelfde lijst')
v, k = g.B4_VRAAGRIJ, g.B4_VRAAGKOL
ws.cell(row=v - 1, column=k,
        value='Lees de antwoorden af van je eigen draaitabellen en typ ze hier.'
        ).font = SCHUIN
vraagblok(ws, v, k, [
    'Welk genre heeft de meeste titels?',
    'Welk genre bestaat alleen uit series, zonder één film?',
    'Welke taal haalt gemiddeld de meeste kijkers per titel?',
    'Welke taal heeft veruit de meeste titels, maar staat toch niet bovenaan '
    'bij het gemiddelde?',
])
for draai in (g.B4_DRAAI1, g.B4_DRAAI2):
    rij = int(draai['anker'][1:]) - 2
    ws.cell(row=rij, column=1, value=draai['titel']).font = VET
    ws.cell(row=rij + 1, column=1,
            value=f"(bron: blad '{draai['bron']}' — zet de linkerbovenhoek van je "
                  f"draaitabel in {draai['anker']})").font = SCHUIN
breedtes(ws, [17, 12, 12, 12, 12, 12, 12, 12, 12])
breedtes(ws, [3, 56, 18], start=k - 1)

# ---------------------------------------------------------------- 5 Grafiek
ws = blad('5 Grafiek', 'De schermtijd door de jaren', g.B5_BRONTEKST)
koprij(ws, g.B5_KOPRIJ, g.B5_KOP)
for r, (jaar, minuten) in enumerate(g.B5, start=g.B5_START):
    ws.cell(row=r, column=1, value=jaar)
    ws.cell(row=r, column=2, value=minuten)
vraagblok(ws, g.B5_VRAAGRIJ, g.B5_VRAAGKOL, [
    'Tussen welke twee jaren stijgt de schermtijd het sterkst?',
    'Hoeveel minuten per dag is die stijging?',
    'Welk grafiektype past bij een verloop in de tijd?',
    'Welke taal heeft de kortste balk in je staafdiagram?',
])
ws.cell(row=g.B5_EIND + 3, column=1,
        value='Zet je twee grafieken hieronder, naast elkaar.').font = SCHUIN
breedtes(ws, [10, 24, 22])
breedtes(ws, [3, 52, 20], start=g.B5_VRAAGKOL - 1)

wb.save(UIT)
print('geschreven:', UIT)
for ws in wb.worksheets:
    gevuld = sum(1 for rij in ws.iter_rows() for c in rij if c.value is not None)
    print(f'  {ws.title:<16} {gevuld} gevulde cellen')
