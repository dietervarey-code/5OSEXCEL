# -*- coding: utf-8 -*-
"""Bouwt de vier documenten uit één bron, zodat stappenplan, fiches en
   lerarenuitleg nooit uit elkaar lopen."""
import importlib.util
import os

HIER = os.path.dirname(os.path.abspath(__file__))

import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT


def laad(naam, pad):
    spec = importlib.util.spec_from_file_location(naam, pad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', os.path.join(HIER, 'gegevens.py'))
a = laad('a', os.path.join(HIER, 'antwoorden.py'))
f = laad('f', os.path.join(HIER, 'fiches.py'))
o = laad('o', os.path.join(HIER, 'oefeningen.py'))

MAP = HIER + os.sep
BLAUW = RGBColor(0x1F, 0x38, 0x64)
GRIJS = RGBColor(0x59, 0x59, 0x59)

# Herkent een formule in een lopende zin, zodat die in een vaste breedte komt.
FORMULE = re.compile(r'(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|=[A-Z$]+\d+(?:[*+\-/][A-Z$]*\d+)*)')


def opzet(doc, marge=2.0):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'
    s.font.size = Pt(11)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.6)
        sec.left_margin = sec.right_margin = Cm(marge)


def kop(doc, tekst, niveau=1):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs:
        r.font.color.rgb = BLAUW
    return p


def zin(p, tekst):
    """Zet tekst in een alinea, met formules in een vaste breedte."""
    for stuk in FORMULE.split(tekst):
        if not stuk:
            continue
        r = p.add_run(stuk)
        if FORMULE.fullmatch(stuk):
            r.font.name = 'Consolas'
            r.font.size = Pt(10.5)
    return p


def alinea(doc, tekst, style=None):
    p = doc.add_paragraph(style=style)
    zin(p, tekst)
    return p


def formuleregel(doc, tekst):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(tekst)
    r.font.name = 'Consolas'
    r.font.size = Pt(11)
    r.bold = True
    return p


def kader(doc, titel, regels, breed=True):
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    c = t.rows[0].cells[0]
    p = c.paragraphs[0]
    r = p.add_run(titel)
    r.bold = True
    r.font.color.rgb = BLAUW
    for regel in regels:
        pp = c.add_paragraph()
        pp.paragraph_format.space_after = Pt(2)
        zin(pp, regel)
    doc.add_paragraph()
    return t


def tabel(doc, koppen, rijen, stijl='Light Grid Accent 1'):
    t = doc.add_table(rows=1, cols=len(koppen))
    t.style = stijl
    for i, k in enumerate(koppen):
        t.rows[0].cells[i].paragraphs[0].add_run(k).bold = True
    for rij in rijen:
        cellen = t.add_row().cells
        for i, w in enumerate(rij):
            zin(cellen[i].paragraphs[0], str(w))
    doc.add_paragraph()
    return t


def paginaeinde(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# =====================================================================
#  1. OPDRACHTFICHE
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Excel — vijf basisoefeningen')
p = doc.add_paragraph()
r = p.add_run(f'{g.BEDRIJF} · vijf oefeningen van tien minuten')
r.italic = True
r.font.color.rgb = GRIJS
doc.add_paragraph('Naam: ..........................................    Klas: ..............    Datum: ..............')

kader(doc, 'Wat je gaat doen', [
    'Je werkt vijf korte oefeningen af in een echt Excel-bestand. Elke oefening staat op',
    'een eigen werkblad en duurt ongeveer tien minuten.',
    '',
    'Bij elke oefening hoort een stappenplan. Loop je vast bij een functie, pak dan de',
    'functiefiche erbij: daar staat wat de functie doet, hoe je ze schrijft, een voorbeeld',
    'met de cijfers uit jouw oefening, en de fout die het vaakst gemaakt wordt.',
    '',
    'Bij elke oefening hoort ook een stuk opmaak. Een blad dat klopt maar er slordig',
    'uitziet, is nog niet af.',
])

kop(doc, 'De vijf oefeningen', 2)
tabel(doc,
      ['Nr', 'Oefening', 'Werkblad', 'Functies', 'Duur'],
      [[oef['nr'], oef['titel'], oef['blad'], ', '.join(oef['functies']), oef['duur']]
       for oef in o.OEFENINGEN])

kop(doc, 'Wat je nodig hebt', 2)
for r_ in [
    'Het bestand excel-startbestand.xlsx. Sla het eerst op onder je eigen naam.',
    'Het stappenplan: daar staat per oefening wat je moet doen.',
    'De functiefiches: één blad per functie, om bij te pakken als je twijfelt.',
]:
    doc.add_paragraph(r_, style='List Bullet')

kop(doc, 'Spelregels', 2)
for r_ in [
    'Reken nooit iets met je rekenmachine om het daarna over te typen. Laat Excel rekenen.',
    'Gebruik de vulgreep om formules door te voeren. Eén formule typen volstaat.',
    'Controleer na het doorvoeren altijd de laatste rij: daar zie je of je verwijzingen kloppen.',
    'Krijg je een foutmelding, lees ze dan. Elke code zegt iets anders — dat staat op de fiches.',
]:
    doc.add_paragraph(r_, style='List Bullet')

kop(doc, 'Waarop je beoordeeld wordt', 2)
tabel(doc, ['Wat', 'Punten'], [
    ['De formules kloppen en verwijzen naar cellen', '10'],
    ['De juiste functie gebruikt op de juiste plaats', '5'],
    ['Opmaak: getalnotatie, koptekst, randen en kleur', '5'],
], stijl='Light List Accent 1')
doc.save(MAP + 'excel-opdrachtfiche.docx')
print('opdrachtfiche geschreven')

# =====================================================================
#  2. STAPPENPLAN
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Stappenplan')
alinea(doc, 'Werk de oefeningen in volgorde af. Elke stap is één handeling.')

for i, oef in enumerate(o.OEFENINGEN):
    if i:
        paginaeinde(doc)
    kop(doc, f"Oefening {oef['nr']} — {oef['titel']}", 2)
    p = doc.add_paragraph()
    r = p.add_run(f"Werkblad: {oef['blad']}    ·    {oef['duur']}")
    r.italic = True
    r.font.color.rgb = GRIJS
    alinea(doc, oef['situatie'])

    nodig = [f"Functiefiche {n}" for n in oef['functies']] + [f"Fiche {n}" for n in oef['hulp']]
    kader(doc, 'Fiches die je hierbij nodig hebt', nodig)

    for nr, (titel, uitleg) in enumerate(oef['stappen'], start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f'Stap {nr}. ')
        r.bold = True
        r.font.color.rgb = BLAUW
        r2 = p.add_run(titel)
        r2.bold = True
        pp = doc.add_paragraph()
        pp.paragraph_format.left_indent = Cm(0.9)
        pp.paragraph_format.space_after = Pt(8)
        zin(pp, uitleg)

    kader(doc, 'Je bent klaar als', [oef['klaar']])

doc.save(MAP + 'excel-stappenplan.docx')
print('stappenplan geschreven')

# =====================================================================
#  3. FUNCTIEBLADEN
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Functiefiches')
alinea(doc, 'Eén blad per functie. Loop je vast, pak dan de fiche erbij: ze staat op zichzelf.')
alinea(doc, 'Achteraan staan vijf fiches over dingen die geen functie zijn, maar die je '
            'wel nodig hebt om de oefeningen af te werken.')

def fiche(doc, d, soort='FUNCTIE'):
    paginaeinde(doc)
    p = doc.add_paragraph()
    r = p.add_run(soort)
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = GRIJS
    kop(doc, d['naam'], 1)
    p = doc.add_paragraph()
    r = p.add_run(d['wat'])
    r.bold = True
    r.font.size = Pt(12)
    p2 = doc.add_paragraph()
    r = p2.add_run(f"Je hebt ze nodig in {d['gebruik']}.")
    r.italic = True
    r.font.color.rgb = GRIJS

    kop(doc, 'Zo schrijf je ze', 2)
    formuleregel(doc, d['schrijf'])
    if d['argumenten']:
        for naam, uitleg in d['argumenten']:
            p = doc.add_paragraph(style='List Bullet')
            r = p.add_run(naam)
            r.font.name = 'Consolas'
            r.bold = True
            zin(p, f' — {uitleg}')

    kop(doc, 'Voorbeeld', 2)
    for regel in d['voorbeeld']:
        if regel.startswith('='):
            formuleregel(doc, regel)
        else:
            alinea(doc, regel)

    kop(doc, 'Wat je moet weten', 2)
    for regel in d['weten']:
        alinea(doc, regel, style='List Bullet')

    kader(doc, 'De fout die het vaakst gemaakt wordt', [d['fout']])


for d in f.FUNCTIES:
    fiche(doc, d, 'FUNCTIE')
for d in f.HULP:
    fiche(doc, d, 'GEEN FUNCTIE, WEL NODIG')

doc.save(MAP + 'excel-functiebladen.docx')
print(f'functiebladen geschreven ({len(f.FUNCTIES)} functies + {len(f.HULP)} hulpfiches)')

# =====================================================================
#  4. LERARENUITLEG
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Excel — vijf basisoefeningen · lerarenuitleg')
alinea(doc, 'Vijf oefeningen van tien minuten, samen één lesuur. Geen geneste functies: '
            'elke formule gebruikt hoogstens één functie, zodat een leerling die vastloopt '
            'maar één ding tegelijk hoeft op te zoeken.')

kader(doc, 'Wat je uitdeelt', [
    'excel-startbestand.xlsx — zes werkbladen, bewust kaal want de opmaak hoort bij de opdracht',
    'excel-opdrachtfiche.docx — één blad met het overzicht en de beoordeling',
    'excel-stappenplan.docx — de vijf oefeningen, stap voor stap',
    'excel-functiebladen.docx — vijftien fiches, om bij te pakken als ze vastlopen',
])

kop(doc, 'Tijdsindeling', 2)
tabel(doc, ['Minuten', 'Wat'], [
    ['0-5', 'Bestand openen, opslaan onder eigen naam, opdrachtfiche overlopen.'],
    ['5-15', 'Oefening 1 — vermenigvuldigen, SOM, valuta. Hier leren ze de vulgreep.'],
    ['15-25', 'Oefening 2 — AFRONDEN en de dollartekens. Het moeilijkste stuk van de reeks.'],
    ['25-35', 'Oefening 3 — MAX, MIN, GEMIDDELDE, AANTAL. Gaat meestal vlot.'],
    ['35-45', 'Oefening 4 — ALS, AANTAL.ALS, SOM.ALS. Let op de aanhalingstekens.'],
    ['45-55', 'Oefening 5 — VERT.ZOEKEN. Plan hier de meeste hulp in.'],
    ['55-60', 'Klassikaal overlopen, bestanden indienen.'],
])
alinea(doc, 'Loop je uit, laat oefening 5 dan als huiswerk. Ze staat los van de vier andere.')

kop(doc, 'Welke fiche hoort bij welke oefening', 2)
tabel(doc, ['Oefening', 'Functiefiches', 'Hulpfiches'],
      [[f"{oef['nr']}. {oef['titel']}", ', '.join(oef['functies']), ', '.join(oef['hulp'])]
       for oef in o.OEFENINGEN])

# --- de oplossingen ---------------------------------------------------
paginaeinde(doc)
kop(doc, 'Oplossingen')

kop(doc, 'Oefening 1 — Voorraadlijst', 2)
formuleregel(doc, 'E4:  =C4*D4        (doorvoeren tot E11)')
formuleregel(doc, 'E13: =SOM(E4:E11)')
alinea(doc, f'Het totaal is {a.O1_SOM:.2f}. De acht waarden:')
tabel(doc, ['Artikel', 'Aantal', 'Prijs', 'Waarde'],
      [[code, aantal, f'{prijs:.2f}', f'{w:.2f}']
       for (code, _, aantal, prijs), w in zip(g.O1, a.O1_WAARDEN)])

kop(doc, 'Oefening 2 — Prijslijst', 2)
formuleregel(doc, 'C6:  =AFRONDEN(B6*(1+$B$3);2)   (doorvoeren tot C12)')
formuleregel(doc, 'D6:  =C6-B6                     (doorvoeren tot D12)')
tabel(doc, ['Artikel', 'Huidig', 'Nieuw', 'Verschil'],
      [[art, f'{p_:.2f}', f'{n:.2f}', f'{v:.2f}']
       for (art, p_), n, v in zip(g.O2, a.O2_NIEUW, a.O2_VERSCHIL)])
alinea(doc, 'Hier gaat het het vaakst mis. Wie de dollartekens vergeet, ziet dat pas vanaf '
            'rij 7: B3 wordt dan B4, en die cel is leeg. De nieuwe prijs is dan gelijk aan '
            'de oude. Laat ze C12 aanklikken en in de formulebalk kijken.')

kop(doc, 'Oefening 3 — Verkoopcijfers', 2)
formuleregel(doc, 'E4:  =SOM(B4:D4)       (doorvoeren tot E9)')
formuleregel(doc, 'B12: =MAX(E4:E9)')
formuleregel(doc, 'B13: =MIN(E4:E9)')
formuleregel(doc, 'B14: =GEMIDDELDE(E4:E9)')
formuleregel(doc, 'B15: =AANTAL(E4:E9)')
tabel(doc, ['Verkoper', 'Kwartaaltotaal'],
      [[naam, t] for (naam, *_), t in zip(g.O3, a.O3_TOTALEN)])
tabel(doc, ['Samenvatting', 'Antwoord'], [
    ['Hoogste (MAX)', a.O3_MAX],
    ['Laagste (MIN)', a.O3_MIN],
    ['Gemiddelde', f'{a.O3_GEM:.0f}'],
    ['Aantal verkopers', a.O3_AANTAL],
], stijl='Light List Accent 1')

kop(doc, 'Oefening 4 — Bestellingen', 2)
formuleregel(doc, 'D6:  =ALS(C6>=$B$3;"Gratis";"Betalend")   (doorvoeren tot D15)')
formuleregel(doc, 'C17: =AANTAL.ALS(D6:D15;"Gratis")')
formuleregel(doc, 'C18: =SOM.ALS(D6:D15;"Gratis";C6:C15)')
tabel(doc, ['Bestelnr', 'Bedrag', 'Levering'],
      [[nr, f'{bedrag:.2f}', lev] for (nr, _, bedrag), lev in zip(g.O4, a.O4_LEVERING)])
alinea(doc, f'Antwoorden: {a.O4_AANTAL_GRATIS} gratis leveringen, samen {a.O4_SOM_GRATIS:.2f} euro.')
kader(doc, 'Twee bestellingen om klassikaal bij stil te staan', [
    'B-2104 staat op 489,90 — net onder de grens, dus Betalend.',
    'B-2108 staat op 501,00 — net erboven, dus Gratis.',
    'Wie > gebruikt in plaats van >=, ziet geen verschil: bij geen enkele bestelling staat',
    'precies 500. Vraag hen wat er zou gebeuren als er wél een bestelling van 500 was.',
])

kop(doc, 'Oefening 5 — Klantenbestand', 2)
formuleregel(doc, 'B4:  =VERT.ZOEKEN(A4;$G$4:$I$11;2;ONWAAR)   (doorvoeren tot B11)')
formuleregel(doc, 'C4:  =VERT.ZOEKEN(A4;$G$4:$I$11;3;ONWAAR)   (doorvoeren tot C11)')
tabel(doc, ['Code', 'Naam', 'Stad'], [list(r_) for r_ in a.O5_ANTWOORD])

# --- fouten -----------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Wat er het vaakst misgaat')
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Wat je zegt'], [
    ['######', 'De kolom is te smal.',
     'Geen fout. Sleep de kolomrand breder of dubbelklik erop.'],
    ['#NAAM?', 'Typfout in de functienaam, of tekst zonder aanhalingstekens.',
     'Laat ze de formule voorlezen. Meestal horen ze het zelf.'],
    ['#N/B', 'VERT.ZOEKEN vindt niets.',
     'Kijk eerst of de dollartekens er nog staan, dan of de code in de zoektabel bestaat.'],
    ['#WAARDE!', 'Er wordt gerekend met een cel waar tekst in staat.',
     'Getallen staan rechts uitgelijnd, tekst links. Dat verraadt het meteen.'],
    ['Overal hetzelfde getal', 'Alle verwijzingen absoluut gemaakt.',
     'F4 blijft wisselen tussen vier vormen. Ze zijn één tik te ver gegaan.'],
    ['Vanaf rij 2 fout', 'De dollartekens vergeten.',
     'De eerste rij klopt bijna altijd. Laat ze altijd rij twee controleren.'],
    ['SOM.ALS geeft 0', 'Zoekbereik en optelbereik omgewisseld.',
     'Eerst waar je zoekt, dan wat je zoekt, dan wat je optelt.'],
])

kop(doc, 'Verbetersleutel in het kort', 2)
tabel(doc, ['Oefening', 'Controleer', 'Antwoord'], [
    ['1', 'E13', f'{a.O1_SOM:.2f}'],
    ['2', 'C12 en D12', f'{a.O2_NIEUW[-1]:.2f} en {a.O2_VERSCHIL[-1]:.2f}'],
    ['3', 'B12 tot B15', f'{a.O3_MAX} / {a.O3_MIN} / {a.O3_GEM:.0f} / {a.O3_AANTAL}'],
    ['4', 'C17 en C18', f'{a.O4_AANTAL_GRATIS} en {a.O4_SOM_GRATIS:.2f}'],
    ['5', 'B11 en C11', f'{a.O5_ANTWOORD[-1][1]} / {a.O5_ANTWOORD[-1][2]}'],
], stijl='Light List Accent 1')
alinea(doc, 'Staat in E13 het juiste totaal, dan kloppen de acht regels erboven ook. '
            'Hetzelfde geldt voor de laatste rij van elke doorgevoerde kolom: die is de '
            'snelste controle, want daar komen de fouten met celverwijzingen bovendrijven.')

doc.save(MAP + 'excel-lerarenuitleg.docx')
print('lerarenuitleg geschreven')
