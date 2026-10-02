# -*- coding: utf-8 -*-
"""Bouwt het opdrachtbestand en de lerarensleutel van de tweede herhalingsbundel."""
import importlib.util
import sys

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal
import os
import re
from collections import Counter
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')

MAP = HIER + os.sep
BLAUW = RGBColor(0x1F, 0x38, 0x64)
GRIJS = RGBColor(0x59, 0x59, 0x59)
FORMULE = re.compile(r'(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|=[A-Z$]+\d+(?:[*+\-/][A-Z$]*\d+)*)')


def opzet(doc):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'
    s.font.size = Pt(11)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.6)
        sec.left_margin = sec.right_margin = Cm(2.0)


def kop(doc, tekst, niveau=1):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs:
        r.font.color.rgb = BLAUW
    return p


def zin(p, tekst):
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


def kader(doc, titel, regels):
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


# Hoe vaak komt elke functie terug? Dat is het punt van deze bundel.
# We tellen formules, niet bladen: op blad 7 staat VERT.ZOEKEN twee keer.
LANGSTE_EERST = sorted({fn for oef in o.OEFENINGEN for fn in oef['functies']},
                       key=len, reverse=True)
TELLING = Counter()
for oef in o.OEFENINGEN:
    for _, _, hoe in oef['maken']:
        for fn in LANGSTE_EERST:      # SOM.ALS vóór SOM, anders telt hij verkeerd
            if fn in hoe:
                TELLING[fn] += 1
                break
TELLING_HULP = Counter(h for oef in o.OEFENINGEN for h in oef['hulp'])

# =====================================================================
#  OPDRACHTBESTAND
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Excel — herhalingsbundel 2')
p = doc.add_paragraph()
r = p.add_run(f'{g.BEDRIJF} · zeven korte oefeningen · 40 minuten')
r.italic = True
r.font.color.rgb = GRIJS
doc.add_paragraph('Naam: ..........................................    Klas: ..............    '
                  'Datum: ..............')

kader(doc, 'Wat je gaat doen', [
    'Zeven korte oefeningen, elk op een eigen werkblad. Reken op vijf à zes minuten per blad.',
    '',
    'Dit is de tweede herhalingsbundel. Er zit geen nieuwe leerstof in: je gebruikt dezelfde',
    'tien functies en dezelfde opmaak als de vorige keren. Ander bedrijf, andere cijfers,',
    'dezelfde opbouw — zodat je ze nu echt vast krijgt.',
    '',
    f'Loop je vast bij een functie, pak dan de functiefiches erbij: {g.BASISBUNDEL}.',
    'Daar staat per functie hoe ze werkt, met een voorbeeld en een schermbeeld.',
    'De fiches zijn niet veranderd.',
    '',
    'Bij elke oefening hoort een stuk opmaak. Een blad dat klopt maar er slordig uitziet,',
    'is nog niet af.',
])

kop(doc, 'De zeven oefeningen', 2)
tabel(doc,
      ['Nr', 'Oefening', 'Werkblad', 'Functies', 'Duur'],
      [[oef['nr'], oef['titel'], oef['blad'], ', '.join(oef['functies']), oef['duur']]
       for oef in o.OEFENINGEN])

kop(doc, 'Welke functie kom je hoe vaak tegen', 2)
alinea(doc, 'Zo zie je meteen wat deze bundel wil: herhaling. De fiche bij elke functie staat '
            f'in {g.BASISBUNDEL}.')
tabel(doc, ['Functie', 'Aantal formules', 'Op welke bladen'],
      [[fn, TELLING[fn],
        ', '.join(str(oef['nr']) for oef in o.OEFENINGEN if fn in oef['functies'])]
       for fn, _ in TELLING.most_common()],
      stijl='Light List Accent 1')

kop(doc, 'En de opmaak', 2)
tabel(doc, ['Onderwerp', 'Aantal bladen', 'Op welke bladen'],
      [[h, TELLING_HULP[h],
        ', '.join(str(oef['nr']) for oef in o.OEFENINGEN if h in oef['hulp'])]
       for h, _ in TELLING_HULP.most_common()],
      stijl='Light List Accent 1')

kop(doc, 'Spelregels', 2)
for r_ in [
    'Reken nooit iets met je rekenmachine om het daarna over te typen. Laat Excel rekenen.',
    'Typ een formule één keer en voer ze door met de vulgreep.',
    'Controleer na het doorvoeren altijd de laatste rij van je kolom.',
    'Elke oefening eindigt met een controle die je zelf kunt doen. Doe ze ook.',
]:
    doc.add_paragraph(r_, style='List Bullet')

kop(doc, 'Waarop je beoordeeld wordt', 2)
tabel(doc, ['Wat', 'Punten'], [
    ['De formules kloppen en verwijzen naar cellen', '10'],
    ['De juiste functie gebruikt op de juiste plaats', '5'],
    ['Opmaak: getalnotatie, koptekst, randen en kleur', '5'],
], stijl='Light List Accent 1')

# --- per werkblad -----------------------------------------------------
for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Werkblad {oef['blad']}", 2)
    p = doc.add_paragraph()
    r = p.add_run(f"Oefening {oef['nr']} — {oef['titel']}    ·    {oef['duur']}")
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'Wat je moet bereiken', [oef['doel']])

    kop(doc, 'Wat er al op het blad staat', 3)
    tabel(doc, ['Waar', 'Wat'], [[waar, wat] for waar, wat in oef['gegeven']],
          stijl='Light List Accent 1')

    kop(doc, 'Wat jij moet maken', 3)
    tabel(doc, ['Waar', 'Wat', 'Waarmee'],
          [[waar, wat, hoe] for waar, wat, hoe in oef['maken']])

    kop(doc, 'Opmaak', 3)
    for regel in oef['opmaak']:
        alinea(doc, regel, style='List Bullet')

    kop(doc, 'Stap voor stap', 3)
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

    fiches = ', '.join(oef['functies'] + oef['hulp'])
    kader(doc, f'Fiches uit {g.BASISBUNDEL}', [fiches])
    kader(doc, 'Je bent klaar als', [oef['klaar']])
    kader(doc, 'Controleer jezelf', [oef['controle']])

doc.save(MAP + 'excel-herhaling-2-opdrachten.docx')
print('opdrachtbestand geschreven')

# =====================================================================
#  LERARENSLEUTEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Excel — herhalingsbundel 2 · lerarensleutel')
alinea(doc, 'Zeven korte oefeningen, samen 40 minuten. Geen nieuwe leerstof: dezelfde tien '
            'functies als in de basisbundel, in dezelfde volgorde als de eerste '
            'herhalingsbundel, maar met andere gegevens.')

kader(doc, 'Wat je uitdeelt', [
    'excel-herhaling-2-startbestand.xlsx — acht werkbladen, bewust kaal',
    'excel-herhaling-2-opdrachten.docx — het overzicht plus één pagina per werkblad',
    '',
    f'Deel er de functiefiches van de basisbundel bij uit ({g.BASISBUNDEL}). Die zijn niet',
    'veranderd; deze bundel verwijst ernaar in plaats van ze te herhalen. Hebben ze die',
    'fiches niet meer, dan lopen blad 6 en 7 vast.',
])

kader(doc, 'Voor wie dit bedoeld is', [
    'Voor wie na de eerste herhalingsbundel nog niet vlot werkt. De opbouw is met opzet',
    'identiek: blad 1 is opnieuw optellen in twee richtingen, blad 7 opnieuw VERT.ZOEKEN.',
    'Wie de vorige bundel af heeft, herkent elke stap en kan sneller door.',
    '',
    'Eén ding is wél anders: op blad 3 komt het percentage er nu BIJ in plaats van eraf.',
    'Wie op de automatische piloot werkt, typt =B5-C5 en krijgt een lagere nieuwe prijs.',
    'Dat is de bedoelde valkuil van dit blad.',
])

kop(doc, 'Tijdsindeling', 2)
tabel(doc, ['Minuten', 'Blad', 'Waar je op let'], [
    ['0-3', 'Intro', 'Bestand openen en opslaan onder eigen naam. Fiches klaarleggen.'],
    ['3-8', '1 Weekomzet', 'Naar rechts doorvoeren. Voor sommigen nog altijd nieuw.'],
    ['8-14', '2 Kwekers', 'Vijf keer hetzelfde bereik, vijf functies. Gaat vlot.'],
    ['14-20', '3 Prijsverhoging', 'Plus in plaats van min, en de dollartekens.'],
    ['20-25', '4 Bezoekers', 'Voorwaardelijke opmaak via Boven gemiddelde.'],
    ['25-31', '5 Snoeicursus', 'Aanhalingstekens, en >= tegenover >.'],
    ['31-37', '6 Leveranciers', 'Het criterium uit een cel halen. Het lastigste blad.'],
    ['37-40', '7 Zaden', 'Haalt niet iedereen. Zie hieronder.'],
])
kader(doc, 'Als je tijd tekort komt', [
    'Blad 7 is de uitsmijter. Wie tot en met blad 6 geraakt, heeft alle tien de functies',
    'minstens één keer gebruikt en de meeste twee of drie keer.',
    '',
    'Blad 7 is dan huiswerk, of het startpunt van de volgende les. Het staat los van de',
    'zes andere: er is niets uit de vorige bladen voor nodig.',
])

kop(doc, 'Hoe vaak komt elke functie terug', 2)
tabel(doc, ['Functie', 'Formules', 'Op welke bladen'],
      [[fn, TELLING[fn],
        ', '.join(str(oef['nr']) for oef in o.OEFENINGEN if fn in oef['functies'])]
       for fn, _ in TELLING.most_common()])

# --- oplossingen ------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Oplossingen')

kop(doc, 'Blad 1 — Weekomzet', 2)
formuleregel(doc, f'E4:  =SOM(B4:D4)        (doorvoeren tot E{g.B1_EIND})')
formuleregel(doc, f'B{g.B1_TOTAAL}: =SOM(B4:B{g.B1_EIND})      '
                  f'(naar rechts doorvoeren tot E{g.B1_TOTAAL})')
tabel(doc, ['Dag', 'Dagtotaal'],
      [[dag, f'{t:.2f}'] for (dag, *_), t in zip(g.B1, a.B1_DAGTOTAAL)])
alinea(doc, f'Kolomtotalen: {" / ".join(f"{x:.2f}" for x in a.B1_KOLOM)}. '
            f'Eindtotaal in E{g.B1_TOTAAL}: {a.B1_EINDTOTAAL:.2f}.')

kop(doc, 'Blad 2 — Kwekers', 2)
formuleregel(doc, f'E4:  =SOM(B4:D4)            (doorvoeren tot E{g.B2_EIND})')
for cel, f_ in [
    ('B13', f'=SOM(E4:E{g.B2_EIND})'), ('B14', f'=GEMIDDELDE(E4:E{g.B2_EIND})'),
    ('B15', f'=MAX(E4:E{g.B2_EIND})'), ('B16', f'=MIN(E4:E{g.B2_EIND})'),
    ('B17', f'=AANTAL(E4:E{g.B2_EIND})'),
    ('F4', f'=ALS(E4>={g.B2_GROOT};"ja";"nee")   (doorvoeren tot F{g.B2_EIND})'),
    ('B18', f'=AANTAL.ALS(F4:F{g.B2_EIND};"ja")'),
]:
    formuleregel(doc, f'{cel}: {f_}')
tabel(doc, ['Kweker', 'Totaal', 'Grote kweker?'],
      [[naam, t, grp] for (naam, *_), t, grp in zip(g.B2, a.B2_TOTAAL, a.B2_GROOT)])
tabel(doc, ['Antwoord', 'Waarde'], [
    ['Totaal planten', a.B2_SOM], ['Gemiddelde', a.B2_GEM],
    ['Hoogste', a.B2_MAX], ['Laagste', a.B2_MIN], ['Aantal kwekers', a.B2_AANTAL],
    ['Grote kwekers', a.B2_AANTAL_GROOT],
], stijl='Light List Accent 1')
kader(doc, 'Eén kweker om klassikaal bij stil te staan', [
    f'De Groene Hof komt op precies {g.B2_GROOT} planten — de grens zelf.',
    'Met >= staat er ja, met > staat er nee. Het is de enige rij waar dat verschil',
    f'zichtbaar wordt. Wie > gebruikt, krijgt in B18 een {a.B2_AANTAL_GROOT - 1} '
    f'in plaats van een {a.B2_AANTAL_GROOT}.',
])

kop(doc, 'Blad 3 — Prijsverhoging', 2)
formuleregel(doc, f'C5:  =AFRONDEN(B5*$B$2;2)   (doorvoeren tot C{g.B3_EIND})')
formuleregel(doc, f'D5:  =B5+C5                 (doorvoeren tot D{g.B3_EIND})')
formuleregel(doc, f'B{g.B3_TOTAAL}: =SOM(B5:B{g.B3_EIND})          '
                  f'(naar rechts doorvoeren tot D{g.B3_TOTAAL})')
tabel(doc, ['Artikel', 'Oude prijs', 'Verhoging', 'Nieuwe prijs'],
      [[art, f'{p_:.2f}', f'{v:.2f}', f'{n:.2f}']
       for (art, p_), v, n in zip(g.B3, a.B3_VERHOGING, a.B3_NIEUW)])
alinea(doc, f'Totalen: {a.B3_SOM_OUD:.2f} + {a.B3_SOM_VERHOGING:.2f} = '
            f'{a.B3_SOM_NIEUW:.2f}. Dat is meteen de controle die in de opdracht '
            'gevraagd wordt.')
kader(doc, 'De valkuil van dit blad', [
    'Vorige bundel ging het percentage eraf, nu komt het erbij. Wie uit gewoonte =B5-C5',
    'typt, krijgt een nieuwe prijs die LAGER is dan de oude. De controle vangt dat:',
    f'{a.B3_SOM_OUD:.2f} min {a.B3_SOM_VERHOGING:.2f} geeft '
    f'{a.B3_SOM_OUD - a.B3_SOM_VERHOGING:.2f}, en dat is niet wat er in D{g.B3_TOTAAL} hoort.',
])

kop(doc, 'Blad 4 — Bezoekers', 2)
for cel, f_ in [('B17', f'=SOM(B4:B{g.B4_EIND})'), ('B18', f'=GEMIDDELDE(B4:B{g.B4_EIND})'),
                ('B19', f'=MAX(B4:B{g.B4_EIND})'), ('B20', f'=MIN(B4:B{g.B4_EIND})'),
                ('B21', f'=AANTAL(B4:B{g.B4_EIND})'),
                ('B22', f'=AANTAL.ALS(B4:B{g.B4_EIND};">{g.B4_DREMPEL}")')]:
    formuleregel(doc, f'{cel}: {f_}')
tabel(doc, ['Antwoord', 'Waarde'], [
    ['Totaal', a.B4_SOM], ['Gemiddelde', a.B4_GEM],
    ['Drukste maand', a.B4_MAX], ['Rustigste maand', a.B4_MIN],
    ['Aantal maanden', a.B4_AANTAL],
    [f'Boven {g.B4_DREMPEL}', a.B4_BOVEN_DREMPEL],
], stijl='Light List Accent 1')
alinea(doc, f'Boven het gemiddelde ({a.B4_GEM}) liggen {len(a.B4_BOVEN_GEM)} maanden: '
            f'{", ".join(a.B4_BOVEN_GEM)}. Die horen gekleurd te zijn.')
alinea(doc, f'Let op het verschil: {len(a.B4_BOVEN_GEM)} maanden liggen boven het GEMIDDELDE '
            f'({a.B4_GEM}), maar maar {a.B4_BOVEN_DREMPEL} maanden liggen boven de '
            f'{g.B4_DREMPEL} van B22. Dat zijn twee verschillende vragen. Laat ze dat zelf '
            'vaststellen.')

kop(doc, 'Blad 5 — Snoeicursus', 2)
formuleregel(doc, f'C5:  =ALS(B5>=$B$2;"Geslaagd";"Niet geslaagd")   '
                  f'(doorvoeren tot C{g.B5_EIND})')
formuleregel(doc, f'B18: =AANTAL.ALS(C5:C{g.B5_EIND};"Geslaagd")')
formuleregel(doc, f'B19: =AANTAL.ALS(C5:C{g.B5_EIND};"Niet geslaagd")')
formuleregel(doc, f'B20: =GEMIDDELDE(B5:B{g.B5_EIND})')
tabel(doc, ['Cursist', 'Punten', 'Resultaat'],
      [[naam, punten, res] for (naam, punten), res in zip(g.B5, a.B5_RESULTAAT)])
alinea(doc, f'{a.B5_GESLAAGD} geslaagd, {a.B5_NIET} niet geslaagd, gemiddelde {a.B5_GEM}.')
kader(doc, 'Eén naam om klassikaal bij stil te staan', [
    f'Cédric Dhaene heeft precies {g.B5_GRENS}, de grens zelf. Met >= is hij geslaagd,',
    'met > niet.',
    '',
    f'Het is de enige rij waar dat verschil zichtbaar wordt. Wie > gebruikt, krijgt '
    f'{a.B5_GESLAAGD - 1} en {a.B5_NIET + 1}',
    f'in plaats van {a.B5_GESLAAGD} en {a.B5_NIET} — en merkt dat zelf niet zonder de '
    'controle.',
])

kop(doc, 'Blad 6 — Leveranciers', 2)
formuleregel(doc, f'B20: =AANTAL.ALS($B$4:$B${g.B6_EIND};A20)              (doorvoeren tot B22)')
formuleregel(doc, f'C20: =SOM.ALS($B$4:$B${g.B6_EIND};A20;$C$4:$C${g.B6_EIND})   '
                  f'(doorvoeren tot C22)')
formuleregel(doc, f'C{g.B6_CONTROLE}: =SOM(C4:C{g.B6_EIND})')
tabel(doc, ['Leverancier', 'Aantal bonnen', 'Totaal bedrag'],
      [[lev, n, f'{b:.2f}'] for lev, n, b in
       zip(g.B6_LEVERANCIERS, a.B6_AANTAL_PER, a.B6_BEDRAG_PER)])
alinea(doc, f'De drie bedragen samen geven {a.B6_TOTAAL_PER:.2f}, en dat is precies wat '
            f'C{g.B6_CONTROLE} toont: {a.B6_TOTAAL_ALLES:.2f}.')
kader(doc, 'Waarom het criterium uit een cel komt', [
    'Ze zouden ook drie keer "Floralux", "Terra Nova" en "Groenwerk" kunnen intypen. Door',
    'naar A20 te verwijzen volstaat één formule die ze doorvoeren.',
    '',
    f'Dat is meteen de moeilijkheid: het bereik moet vast ($B$4:$B${g.B6_EIND}), het',
    'criterium juist niet (A20). Wie alles vastzet, krijgt drie keer hetzelfde getal. Wie',
    'niets vastzet, krijgt vanaf de tweede rij onzin. Laat ze B21 aanklikken en de',
    'formulebalk lezen.',
])

kop(doc, 'Blad 7 — Zaden', 2)
formuleregel(doc, f'B4:  =VERT.ZOEKEN(A4;$G$4:$I${g.B7_TAB_EIND};2;ONWAAR)   '
                  f'(doorvoeren tot B{g.B7_EIND})')
formuleregel(doc, f'C4:  =VERT.ZOEKEN(A4;$G$4:$I${g.B7_TAB_EIND};3;ONWAAR)   '
                  f'(doorvoeren tot C{g.B7_EIND})')
formuleregel(doc, f'E4:  =AFRONDEN(C4*D4;2)                      '
                  f'(doorvoeren tot E{g.B7_EIND})')
formuleregel(doc, f'E{g.B7_TOTAAL}: =SOM(E4:E{g.B7_EIND})')
formuleregel(doc, f'E{g.B7_DEEL}: =SOM.ALS(A4:A{g.B7_EIND};"{g.B7_DEELTOTAAL}";'
                  f'E4:E{g.B7_EIND})')
tabel(doc, ['Code', 'Omschrijving', 'Prijs', 'Aantal', 'Bedrag'],
      [[c, oms, f'{p_:.2f}', aant, f'{b:.2f}'] for c, oms, p_, aant, b in a.B7_REGELS])
alinea(doc, f'Eindtotaal in E{g.B7_TOTAAL}: {a.B7_EINDTOTAAL:.2f}. Daarvan is '
            f'{a.B7_DEELTOTAAL:.2f} bloemenmengsel (code {g.B7_DEELTOTAAL}, die twee keer '
            'voorkomt).')

# --- fouten -----------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Wat er het vaakst misgaat')
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Wat je zegt'], [
    ['######', 'De kolom is te smal.', 'Geen fout. Kolomrand breder slepen.'],
    ['#NAAM?', 'Typfout, of tekst zonder aanhalingstekens.',
     'Laat de formule voorlezen. Meestal horen ze het zelf.'],
    ['Nieuwe prijs lager dan de oude op blad 3', 'Min gebruikt in plaats van plus.',
     'Vorige bundel ging de korting eraf. Nu komt de verhoging erbij.'],
    ['#N/B op blad 7', 'De dollartekens rond de zoektabel ontbreken.',
     'Laat B13 aanklikken: is de tabel meegeschoven?'],
    ['Drie keer hetzelfde getal op blad 6', 'Ook het criterium vastgezet ($A$20).',
     'Het bereik staat vast, het criterium niet.'],
    [f'{a.B5_GESLAAGD - 1} en {a.B5_NIET + 1} op blad 5', '> gebruikt in plaats van >=.',
     f'Kijk naar Cédric Dhaene, precies {g.B5_GRENS}.'],
    ['Verhoging gelijk voor elk artikel op blad 3', 'B2 niet vastgezet.',
     'Vanaf rij 6 wijst hij naar een lege cel.'],
    ['Kolomtotaal klopt niet op blad 1', 'Naar beneden doorgevoerd in plaats van naar rechts.',
     'De vulgreep kan ook zijwaarts.'],
])

kop(doc, 'Verbetersleutel in het kort', 2)
tabel(doc, ['Blad', 'Controleer', 'Antwoord'], [
    ['1', f'E{g.B1_TOTAAL}', f'{a.B1_EINDTOTAAL:.2f}'],
    ['2', 'B13 tot B18',
     f'{a.B2_SOM} / {a.B2_GEM} / {a.B2_MAX} / {a.B2_MIN} / {a.B2_AANTAL} / '
     f'{a.B2_AANTAL_GROOT}'],
    ['3', f'B{g.B3_TOTAAL} tot D{g.B3_TOTAAL}',
     f'{a.B3_SOM_OUD:.2f} / {a.B3_SOM_VERHOGING:.2f} / {a.B3_SOM_NIEUW:.2f}'],
    ['4', 'B17 tot B22',
     f'{a.B4_SOM} / {a.B4_GEM} / {a.B4_MAX} / {a.B4_MIN} / {a.B4_AANTAL} / '
     f'{a.B4_BOVEN_DREMPEL}'],
    ['5', 'B18 tot B20', f'{a.B5_GESLAAGD} / {a.B5_NIET} / {a.B5_GEM}'],
    ['6', f'C20 tot C22 en C{g.B6_CONTROLE}',
     ' / '.join(f'{x:.2f}' for x in a.B6_BEDRAG_PER) + f' → {a.B6_TOTAAL_ALLES:.2f}'],
    ['7', f'E{g.B7_TOTAAL} en E{g.B7_DEEL}',
     f'{a.B7_EINDTOTAAL:.2f} / {a.B7_DEELTOTAAL:.2f}'],
], stijl='Light List Accent 1')
alinea(doc, 'Elk blad heeft een eindtotaal dat de rest van het blad afdekt. Klopt dat getal, '
            'dan kloppen de regels erboven ook. Dat is je snelste verbetering.')

doc.save(MAP + 'excel-herhaling-2-lerarensleutel.docx')
print('lerarensleutel geschreven')
print(f'functies: {dict(TELLING)}')
