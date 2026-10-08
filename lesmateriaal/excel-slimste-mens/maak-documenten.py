# -*- coding: utf-8 -*-
"""Bouwt de opdrachtbundel en de lerarensleutel van de zelfstudiebundel."""
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
sl = laad('sl', 'sleutel.py')

MAP = HIER + os.sep
BLAUW = RGBColor(0x1F, 0x38, 0x64)
GRIJS = RGBColor(0x59, 0x59, 0x59)
GROEN = RGBColor(0x1E, 0x6B, 0x3A)
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


def kader(doc, titel, regels, kleur=BLAUW):
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    c = t.rows[0].cells[0]
    p = c.paragraphs[0]
    r = p.add_run(titel)
    r.bold = True
    r.font.color.rgb = kleur
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
MINUTEN = sum(int(oef['duur'].split()[0]) for oef in o.OEFENINGEN)

# =====================================================================
#  OPDRACHTBUNDEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, g.TITEL)
p = doc.add_paragraph()
r = p.add_run(g.ONDERTITEL)
r.italic = True
r.font.color.rgb = GRIJS
doc.add_paragraph('Naam: ..........................................    Klas: ..............    '
                  'Datum: ..............')

kader(doc, 'Je werkt alleen — zo pak je het aan', [
    f'Vijf werkbladen, samen {MINUTEN} minuten. Werk ze in volgorde af: ze worden telkens '
    'een beetje moeilijker.',
    '',
    'Bij elke stap staat precies wat je moet typen. Je hoeft dus niets te verzinnen — je '
    'moet het begrijpen en juist uitvoeren. Lees elke stap helemaal voor je iets typt.',
    '',
    'Onderaan elk blad staat een CONTROLEGETAL. Dat is het getal dat in één bepaalde cel '
    'hoort te staan als je alles goed gedaan hebt. Komt jouw cel op datzelfde getal uit, '
    'dan zit je goed en mag je naar het volgende blad.',
    '',
    'Komt het niet uit, lees dan het lijstje "Loop je vast?" onderaan dat blad. Daar staan '
    'de drie fouten die het vaakst gemaakt worden en wat je eraan doet. Typ het '
    'controlegetal NOOIT zelf in: dan klopt de rest van je blad niet meer.',
], GROEN)

kader(doc, 'Lees dit eerst', [
    'Sla het bestand meteen op als  slimste-jouwnaam.xlsx  en sla tijdens het werken '
    'regelmatig opnieuw op (Ctrl+S).',
    '',
    g.WAARSCHUWING,
])

kop(doc, 'De vijf werkbladen', 2)
tabel(doc, ['Nr', 'Werkblad', 'Wat je doet', 'Functies', 'Duur'],
      [[oef['nr'], oef['blad'], oef['titel'], ', '.join(oef['functies']), oef['duur']]
       for oef in o.OEFENINGEN])

kop(doc, 'Welke functie kom je hoe vaak tegen', 2)
alinea(doc, 'De drie waar het vaakst op vastgelopen wordt — SOM, AANTAL.ALS en '
            f'VERT.ZOEKEN — komen het meest terug. De fiche bij elke functie staat in '
            f'{g.BASISBUNDEL}. Pak die erbij als je wil weten waarom iets werkt; voor '
            'deze bundel heb je ze niet nodig.')
tabel(doc, ['Functie', 'Aantal formules', 'Op welke bladen'],
      [[fn, TELLING[fn],
        ', '.join(str(oef['nr']) for oef in o.OEFENINGEN if fn in oef['functies'])]
       for fn, _ in TELLING.most_common()],
      stijl='Light List Accent 1')

kop(doc, 'Spelregels', 2)
for r_ in [
    'Reken nooit iets uit met je rekenmachine om het daarna over te typen. Laat Excel '
    'rekenen: dat is net wat je hier oefent.',
    'Typ een formule één keer en voer ze door met de vulgreep — het kleine blokje '
    'rechtsonder in de cel.',
    'Controleer na het doorvoeren altijd de LAATSTE rij van je kolom. Daar gaat het mis '
    'als er dollartekens ontbreken.',
    'Bij elk blad hoort opmaak. Een blad dat klopt maar er slordig uitziet, is nog niet af.',
    'Raak de tabellen die als "niet aanpassen" aangeduid staan niet aan.',
]:
    doc.add_paragraph(r_, style='List Bullet')

# --- per werkblad -----------------------------------------------------
for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Werkblad {oef['blad']}", 1)
    p = doc.add_paragraph()
    r = p.add_run(f"Oefening {oef['nr']} — {oef['titel']}    ·    {oef['duur']}")
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'Wat je moet bereiken', [oef['doel']])

    kop(doc, 'Wat er al op het blad staat', 2)
    tabel(doc, ['Waar', 'Wat'], [[waar, wat] for waar, wat in oef['gegeven']],
          stijl='Light List Accent 1')

    kop(doc, 'Wat jij moet maken', 2)
    tabel(doc, ['Waar', 'Wat', 'Waarmee'],
          [[waar, wat, hoe] for waar, wat, hoe in oef['maken']])

    kop(doc, 'Opmaak', 2)
    for regel in oef['opmaak']:
        alinea(doc, regel, style='List Bullet')

    kop(doc, 'Stap voor stap', 2)
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

    cel, waarde = sl.CONTROLE[oef['nr']]
    kader(doc, f'CONTROLEGETAL — in {cel} hoort {waarde} te staan', [
        oef['controle'],
        '',
        f'Klopt het? Vink blad {oef["nr"]} af op de afvinklijst achteraan en ga verder.',
        'Klopt het niet? Lees dan hieronder.',
    ], GROEN)

    kop(doc, 'Loop je vast?', 2)
    tabel(doc, ['Wat je ziet', 'Wat je eraan doet'],
          [[wat, hoe] for wat, hoe in oef['vastgelopen']])

    kader(doc, 'Je bent klaar als', [oef['klaar']])

# --- afvinklijst ------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Afvinklijst')
alinea(doc, 'Vul hier na elk blad in welk getal je kreeg. Zo zie je zelf hoe ver je staat, '
            'en kan je leerkracht achteraf in één oogopslag zien waar het misliep.')
tabel(doc, ['Blad', 'Cel', 'Dit getal hoort erin te staan', 'Wat ik kreeg', 'Klopt?'],
      [[f"{oef['nr']} — {oef['blad']}", sl.CONTROLE[oef['nr']][0],
        sl.CONTROLE[oef['nr']][1], '', ''] for oef in o.OEFENINGEN])
alinea(doc, 'Klaar met alle vijf? Kijk dan nog eens naar de opmaak: staat bij elk blad de '
            'koprij in het vet, zijn de getallen leesbaar, en staan de randen waar ze '
            'moeten staan?')

doc.save(MAP + 'slimste-mens-opdracht.docx')
print('opdrachtbundel geschreven')

# =====================================================================
#  LERARENSLEUTEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, f'{g.TITEL} · lerarensleutel')
alinea(doc, f'Zelfstudiebundel, {MINUTEN} minuten, te maken zonder begeleiding. Geen nieuwe '
            'leerstof: dezelfde tien functies als in de basisbundel, met de nadruk op SOM, '
            'AANTAL.ALS en VERT.ZOEKEN. Geen geneste functies.')

kader(doc, 'Wat je uitdeelt', [
    'slimste-mens-startbestand.xlsx — zes werkbladen, bewust kaal',
    'slimste-mens-opdracht.docx — het overzicht, één pagina per werkblad, en een '
    'afvinklijst achteraan',
    '',
    f'De functiefiches van de basisbundel ({g.BASISBUNDEL}) hoeven er niet bij: de stappen '
    'geven elke formule letterlijk. Leg ze wel klaar voor wie wil weten waarom iets werkt.',
])

kader(doc, 'Waarom deze bundel er anders uitziet', [
    'Deze bundel is gemaakt om alleen af te werken. Drie dingen zijn daarom anders dan in '
    'de gewone herhalingsbundels:',
    '',
    '1. De stappen geven de formule LETTERLIJK. Zonder leerkracht in de buurt mag niemand '
    'vastlopen op iets routineus; de winst zit in het juist uitvoeren en begrijpen.',
    '',
    '2. Elk blad heeft een CONTROLEGETAL. Dat staat in de opdracht, zodat ze zelf weten of '
    'ze verder mogen. Het staat bij een cel die van bijna het hele blad afhangt.',
    '',
    '3. Elk blad heeft een lijstje "Loop je vast?" met de drie fouten die het vaakst '
    'gemaakt worden, en wat ze er dan zelf aan doen.',
    '',
    'De afvinklijst achteraan vullen ze zelf in. Je ziet daar meteen op welk blad iemand '
    'is blijven steken.',
], GROEN)

kop(doc, 'De controlegetallen', 2)
tabel(doc, ['Blad', 'Cel', 'Getal', 'Wat het afdekt'],
      [[f"{oef['nr']} — {oef['blad']}", sl.CONTROLE[oef['nr']][0],
        sl.CONTROLE[oef['nr']][1], oef['controle'][:90] + '…']
       for oef in o.OEFENINGEN], stijl='Light List Accent 1')

kop(doc, 'Tijdsindeling', 2)
tabel(doc, ['Minuten', 'Blad', 'Waar ze op vastlopen'], [
    ['0-3', 'Intro', 'Bestand openen en opslaan onder eigen naam.'],
    ['3-8', '1 Kijkcijfers', 'Naar rechts doorvoeren in plaats van naar beneden.'],
    ['8-18', '2 Deelnemers', 'De dollartekens rond B2, en >= tegenover >.'],
    ['18-27', '3 Themas', 'Het bereik vastzetten maar het criterium niet. Het lastigste '
                          'blad.'],
    ['27-36', '4 Rondes', 'De zoektabel vastzetten. Zonder dollartekens volgt #N/B.'],
    ['36-43', '5 Finaleweek', 'Dezelfde VERT.ZOEKEN als blad 4, nu zelfstandig.'],
])
kader(doc, 'Als iemand niet rond geraakt', [
    'De bladen staan los van elkaar: er is niets van blad 1 nodig op blad 5. Wie halverwege '
    'strandt, heeft niets verloren.',
    '',
    'Blad 3 is het lastigste (criterium uit een cel). Blad 4 en 5 zijn allebei VERT.ZOEKEN: '
    'wie blad 4 af heeft, kan blad 5 meestal vlot. Wie op blad 3 vastloopt, laat je beter '
    'doorgaan naar blad 4 dan blijven ploeteren.',
])

# --- oplossingen ------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Oplossingen')
for oef in o.OEFENINGEN:
    cel, waarde = sl.CONTROLE[oef['nr']]
    kop(doc, f"Blad {oef['nr']} — {oef['blad']}   (controlegetal {cel} = {waarde})", 2)
    for c, formule, antwoord in sl.SLEUTEL[oef['nr']]:
        formuleregel(doc, f'{c}: {formule}')
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.4)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run('→ ' + antwoord)
        r.italic = True
        r.font.color.rgb = GRIJS

# --- de uitkomsten ----------------------------------------------------
paginaeinde(doc)
kop(doc, 'De uitkomsten om na te kijken')

kop(doc, 'Blad 2 — Deelnemers', 2)
tabel(doc, ['Deelnemer', 'Afleveringen', 'Overwinningen', 'Seconden', 'Finaleweek?'],
      [[naam, afl, ow, sec, fin]
       for (naam, _, afl, ow, sec), fin in zip(g.B2, a.B2_FINALIST)])
kader(doc, 'Twee namen om bij stil te staan', [
    f'{" en ".join(a.B2_OP_DE_GRENS)} hebben allebei precies {g.B2_FINALIST} overwinningen, '
    'de grens zelf. De opdracht zegt "vanaf", dus horen ze erbij. Wie > gebruikt in plaats '
    f'van >=, krijgt in B{sl.S2 + 6} een {a.B2_AANTAL_FINALIST - 2} in plaats van een '
    f'{a.B2_AANTAL_FINALIST}.',
    '',
    'Het zijn de enige twee rijen waar dat verschil zichtbaar wordt. Stap 2 van het blad '
    'wijst hen met naam aan, zodat wie alleen werkt het zelf kan vaststellen.',
])

kop(doc, 'Blad 3 — Themas', 2)
tabel(doc, ['Thema', 'Aantal vragen', 'Seconden'],
      [[thema, aantal, sec] for thema, aantal, sec
       in zip(g.B3_THEMAS, a.B3_AANTAL_PER, a.B3_SECONDEN_PER)]
      + [['Samen', sum(a.B3_AANTAL_PER), a.B3_TOTAAL]])
alinea(doc, 'Muziek en Film & TV hebben allebei vijf vragen, maar Muziek levert meer '
            'seconden op. De voorwaardelijke opmaak zet alleen Muziek in de kleur: dat is '
            'een goede gelegenheid om te vragen waarom.')

kop(doc, 'Blad 4 — Rondes', 2)
tabel(doc, ['Code', 'Ronde', 'Sec. per antwoord', 'Juist', 'Gewonnen seconden'],
      [[code, naam, per, juist, sec] for code, naam, per, juist, sec in a.B4_REGELS]
      + [['', '', 'Totaal', a.B4_JUIST, a.B4_SECONDEN]])

kop(doc, 'Blad 5 — Finaleweek', 2)
tabel(doc, ['Startnr', 'Deelnemer', 'R1', 'R2', 'R3', 'Totaal', 'Door?'],
      [[nr, naam, r1, r2, r3, totaal, door]
       for nr, naam, r1, r2, r3, totaal, door in a.B5_RIJEN])
kader(doc, 'Nog een grensgeval', [
    f'{a.B5_OP_DE_GRENS[0]} komt op precies {g.B5_DOOR} seconden. Met >= gaat hij door, met '
    f'> niet. Wie > gebruikt, krijgt in B{sl.A5} een {a.B5_AANTAL_DOOR - 1} in plaats van '
    f'een {a.B5_AANTAL_DOOR} — en dat is net het controlegetal van dit blad, dus ze merken '
    'het zelf.',
])

# --- fouten -----------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Wat er het vaakst misgaat')
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Staat het in de bundel?'], [
    ['######', 'De kolom is te smal.', 'Ja, blad 1.'],
    ['#NAAM?', 'Tekst zonder aanhalingstekens in een ALS.', 'Ja, blad 2.'],
    ['#N/B op blad 4 of 5', 'De dollartekens rond de zoektabel ontbreken.',
     'Ja, blad 4 en 5.'],
    ['Zes keer hetzelfde getal op blad 3', 'Ook het criterium vastgezet ($A$30).',
     'Ja, blad 3.'],
    ['Kolomtotaal klopt niet op blad 1', 'Naar beneden doorgevoerd in plaats van naar '
                                         'rechts.', 'Ja, blad 1.'],
    ['Overal ja of overal nee in kolom F', 'B2 niet vastgezet op blad 2.', 'Ja, blad 2.'],
    ['Het controlegetal staat erin maar de rest niet',
     'Het getal overgetypt in plaats van berekend.',
     'Nee — daar moet jij naar kijken.'],
])
alinea(doc, 'Zes van de zeven staan letterlijk in het lijstje "Loop je vast?" bij het '
            'betrokken blad. De zevende niet: dat is het enige dat je achteraf zelf moet '
            'nagaan. Klik de controlecel aan en kijk of er een formule in staat.')

kop(doc, 'Verbetersleutel in het kort', 2)
tabel(doc, ['Blad', 'Controleer', 'Antwoord'],
      [[oef['nr'], sl.CONTROLE[oef['nr']][0], sl.CONTROLE[oef['nr']][1]]
       for oef in o.OEFENINGEN], stijl='Light List Accent 1')
alinea(doc, 'Staan die vijf getallen er, en staat er in elke cel een formule in plaats van '
            'een getal, dan is de bundel af.')

doc.save(MAP + 'slimste-mens-lerarensleutel.docx')
print('lerarensleutel geschreven')
print(f'functies: {dict(TELLING)}')
