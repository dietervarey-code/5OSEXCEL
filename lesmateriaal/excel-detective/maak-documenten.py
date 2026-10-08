# -*- coding: utf-8 -*-
"""Bouwt de opdrachtbundel en de leerkrachtensleutel van de vijf detectivezaken."""
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
z = laad('z', 'zaken.py')
sl = laad('sl', 'sleutel.py')

MAP = HIER + os.sep
BLAUW = RGBColor(0x1F, 0x38, 0x64)
GRIJS = RGBColor(0x59, 0x59, 0x59)
GROEN = RGBColor(0x1E, 0x6B, 0x3A)
ROOD = RGBColor(0xA0, 0x1B, 0x1B)
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


def lijnen(doc, aantal=2, breedte=78):
    """Lege lijnen om met de hand op te schrijven."""
    for _ in range(aantal):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        r = p.add_run('.' * breedte)
        r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)


MINUTEN = sum(int(zaak['duur'].split()[0]) for zaak in z.ZAKEN)

# =====================================================================
#  DE OPDRACHTBUNDEL
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

kader(doc, 'Hoe elke zaak in elkaar zit', [
    'Vijf zaken die niets met elkaar te maken hebben. Elke zaak past in één les van '
    'ongeveer 25 minuten en staat op één werkblad.',
    '',
    'Zes of zeven GEWONE FORMULES zetten het dossier op orde. Die staan letterlijk in de '
    'stappen: typ ze over, voer ze door, en lees wat eruit komt.',
    '',
    'Daarna komt de SLEUTELFORMULE. Dat is er één met een functie BINNEN een functie, en '
    'daarvan krijg je alleen de vorm — de inhoud zoek je zelf uit. Die ene formule kraakt '
    'de zaak. Elke zaak heeft een ander soort sleutelformule.',
    '',
    'Bij elke zaak staat een PROEF: twee getallen die hetzelfde moeten geven, of een getal '
    'dat je op voorhand al weet. Komt het uit, dan heb je de zaak opgelost en kan je het '
    'antwoord opschrijven. Komt het niet uit, lees dan het lijstje "Loop je vast?".',
], GROEN)

kader(doc, 'Lees dit eerst', [
    'Sla het bestand meteen op als  detective-jouwnaam.xlsx  en sla tijdens het werken '
    'regelmatig opnieuw op (Ctrl+S).',
    '',
    'Je mag de zaken in eender welke volgorde doen, maar zaak 1 is de gemakkelijkste om '
    'mee te beginnen.',
    '',
    g.WAARSCHUWING,
])

kop(doc, 'De vijf zaken', 2)
tabel(doc, ['Nr', 'Zaak', 'Wat je moet uitzoeken', 'Sleutelformule', 'Duur'],
      [[zaak['nr'], zaak['titel'], zaak['vraag'], zaak['nesting'], zaak['duur']]
       for zaak in z.ZAKEN])
alinea(doc, 'In de kolom Sleutelformule zie je meteen dat het vijf keer iets anders is. Dat '
            'is met opzet: één trucje vijf keer herhalen leert je niets.')

kop(doc, 'Spelregels', 2)
for r_ in [
    'Reken nooit iets uit met je rekenmachine om het daarna over te typen. Twee cellen '
    'mag je wél zelf invullen — daar staat uitdrukkelijk bij dat het geen formule is.',
    'Typ een formule één keer en voer ze door met de vulgreep.',
    'Controleer na het doorvoeren altijd de LAATSTE rij van je kolom. Daar gaat het mis '
    'als er dollartekens ontbreken.',
    'Bouw de sleutelformule in twee stappen op: eerst het binnenste stuk apart in een lege '
    'cel, kijken of het klopt, en dan pas naar binnen schuiven. Wis die hulpcel achteraf.',
    'Raak de tabellen die als "niet aanpassen" aangeduid staan niet aan.',
    'Schrijf je antwoord op het antwoordblad achteraan. Dat is wat je afgeeft.',
]:
    doc.add_paragraph(r_, style='List Bullet')

# --- per zaak ---------------------------------------------------------
for zaak in z.ZAKEN:
    paginaeinde(doc)
    kop(doc, f"Zaak {zaak['nr']} — {zaak['titel']}", 1)
    p = doc.add_paragraph()
    r = p.add_run(f"werkblad {zaak['blad']}    ·    {zaak['duur']}    ·    "
                  f"sleutelformule: {zaak['nesting']}")
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'Het dossier', zaak['dossier'], ROOD)

    if zaak.get('grafiek'):
        kader(doc, f"Eerst kijken: de grafiek «{zaak['grafiek']['titel']}»", [
            zaak['grafiek']['vraag'],
            '',
            'Mijn vermoeden: ................................................................',
        ])

    kop(doc, 'Wat er op het blad staat', 2)
    tabel(doc, ['Waar', 'Wat'], [[waar, wat] for waar, wat in zaak['gegeven']],
          stijl='Light List Accent 1')

    kop(doc, 'Stap voor stap', 2)
    nr = 0
    sleutel_stap = None
    for m in zaak['maken']:
        if m.get('genest'):
            sleutel_stap = m
            continue
        nr += 1
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f'Stap {nr}. ')
        r.bold = True
        r.font.color.rgb = BLAUW
        r2 = p.add_run(f"{m['waar']} — {m['wat']}")
        r2.bold = True
        if m.get('formule'):
            formuleregel(doc, m['formule'])
        if m.get('stap'):
            pp = doc.add_paragraph()
            pp.paragraph_format.left_indent = Cm(0.9)
            pp.paragraph_format.space_after = Pt(8)
            zin(pp, m['stap'])
        else:
            doc.add_paragraph().paragraph_format.space_after = Pt(4)

    kader(doc, f"DE SLEUTELFORMULE — {sleutel_stap['waar']}: {sleutel_stap['wat']}",
          [f"Dit is de enige formule die je niet kant-en-klaar krijgt. De vorm is:",
           '',
           f"     {sleutel_stap['vorm']}",
           '',
           'De puntjes moet je zelf invullen.',
           ''] + sleutel_stap['hulp']
          + (['', sleutel_stap['stap']] if sleutel_stap.get('stap') else []), ROOD)

    kop(doc, 'Opmaak', 2)
    for regel in zaak['opmaak']:
        alinea(doc, regel, style='List Bullet')

    kader(doc, 'DE PROEF — hiermee weet je of je de zaak hebt', [zaak['proef']], GROEN)

    kop(doc, 'Je antwoord', 2)
    alinea(doc, zaak['vraag'])
    lijnen(doc, 3)

    kop(doc, 'Loop je vast?', 2)
    tabel(doc, ['Wat je ziet', 'Wat je eraan doet'],
          [[wat, hoe] for wat, hoe in zaak['vastgelopen']])

# --- antwoordblad -----------------------------------------------------
paginaeinde(doc)
kop(doc, 'Antwoordblad')
alinea(doc, 'Vul dit in terwijl je werkt. Dit blad geef je af. Het bestand bewaar je zelf: '
            'je leerkracht kijkt achteraf na of er in elke cel een formule staat en niet '
            'alleen een getal.')
for zaak in z.ZAKEN:
    kop(doc, f"Zaak {zaak['nr']} — {zaak['titel']}", 2)
    alinea(doc, zaak['vraag'])
    lijnen(doc, 2)
    p = doc.add_paragraph()
    r = p.add_run('De proef klopte:    ja  /  nee          '
                  'Mijn sleutelformule:  ..............................................')
    r.font.size = Pt(10)
    r.font.color.rgb = GRIJS

doc.save(MAP + 'detective-opdracht.docx')
print(f'opdrachtbundel geschreven ({len(z.ZAKEN)} zaken, {MINUTEN} minuten)')

# =====================================================================
#  DE LEERKRACHTENSLEUTEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, f'{g.TITEL} · leerkrachtensleutel')
alinea(doc, f'Vijf losse zaken van ongeveer 25 minuten, samen {MINUTEN} minuten. Voor '
            'leerlingen die de basisbundel vlot afwerken en toe zijn aan iets meer, maar '
            'voor wie de Halloweenopdracht te veel ineens was.')

kader(doc, 'Wat je uitdeelt', [
    'detective-startbestand.xlsx — zes werkbladen, één per zaak, met twee grafieken erin',
    'detective-opdracht.docx — één hoofdstuk per zaak, met achteraan een antwoordblad',
    '',
    'De functiefiches van de basisbundel mogen erbij. Alles behalve de sleutelformule is '
    'gewoon herhaling.',
])

kader(doc, 'Waarom dit lichter is dan de Halloweenopdracht', [
    'Bij Halloween stond er nergens een formule: ze moesten alles zelf bedenken, vijf '
    'werkbladen aan één stuk, met tien nieuwe functies.',
    '',
    'Hier is de moeilijkheid op één plaats geconcentreerd. Zes of zeven formules staan '
    'letterlijk uitgeschreven — dat is routinewerk dat vlot loopt. Alleen de '
    'sleutelformule moeten ze zelf maken, en daarvan krijgen ze de vorm, een uitleg per '
    'stuk, en de raad om ze in twee stappen op te bouwen.',
    '',
    'Bovendien duurt een zaak maar 25 minuten en staat ze volledig los van de andere. Wie '
    'er één niet rond krijgt, begint de week daarop gewoon met een propere lei.',
], GROEN)

kop(doc, 'De vijf sleutelformules', 2)
alinea(doc, 'Elke zaak heeft een andere soort nesting. Samen dekken ze de vier manieren '
            'waarop een functie in een andere kan zitten: in de voorwaarde van een ALS, in '
            'het antwoord van een ALS, als zoekwaarde, en als samengestelde voorwaarde.')
tabel(doc, ['Zaak', 'Nesting', 'De sleutelformule', 'Waar ze zit'],
      [[zaak['nr'], zaak['nesting'],
        next(f for c, f, _ in sl.SLEUTEL[zaak['nr']]
             if f and any(m.get('genest') and m['waar'].startswith(c)
                          for m in zaak['maken'])),
        next(m['waar'] for m in zaak['maken'] if m.get('genest'))]
       for zaak in z.ZAKEN])

kop(doc, 'De antwoorden in het kort', 2)
tabel(doc, ['Zaak', 'De vraag', 'Het antwoord'],
      [[zaak['nr'], zaak['vraag'], sl.OPLOSSING[zaak['nr']]] for zaak in z.ZAKEN],
      stijl='Light List Accent 1')

kop(doc, 'De proef per zaak', 2)
alinea(doc, 'Hiermee weet een leerling die alleen werkt of hij goed zit, zonder dat jij '
            'het moet bevestigen. Vraag het na: wie de proef niet gedaan heeft, heeft de '
            'zaak niet af.')
tabel(doc, ['Zaak', 'De proef'],
      [[zaak['nr'], zaak['proef']] for zaak in z.ZAKEN])

# --- per zaak ---------------------------------------------------------
for zaak in z.ZAKEN:
    paginaeinde(doc)
    kop(doc, f"Zaak {zaak['nr']} — {zaak['titel']}", 1)
    p = doc.add_paragraph()
    r = p.add_run(f"werkblad {zaak['blad']}    ·    {zaak['duur']}    ·    "
                  f"sleutelformule: {zaak['nesting']}")
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'De afloop', [zaak['afloop']], ROOD)

    if zaak.get('grafiek'):
        kader(doc, f"De grafiek «{zaak['grafiek']['titel']}»", [
            zaak['grafiek']['vraag'],
            '',
            'De grafiek staat kant-en-klaar in het startbestand: ze moeten ze lezen, niet '
            'maken. Ze geeft het antwoord al half weg, en dat is de bedoeling — de formule '
            'is het bewijs, de grafiek is het vermoeden.',
        ])

    kop(doc, 'Alle formules', 2)
    for cel, formule, antwoord in sl.SLEUTEL[zaak['nr']]:
        if formule is None:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(f'{cel}: geen formule — zelf in te typen')
            r.bold = True
            r.font.name = 'Consolas'
            r.font.size = Pt(10.5)
        else:
            formuleregel(doc, f'{cel}: {formule}')
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.4)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run('→ ' + antwoord)
        r.italic = True
        r.font.color.rgb = GRIJS

    kop(doc, 'Waar ze op vastlopen', 2)
    tabel(doc, ['Wat ze zien', 'Wat jij zegt (staat ook in hun bundel)'],
          [[wat, hoe] for wat, hoe in zaak['vastgelopen']])

# --- nakijkblad -------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Nakijkblad')
alinea(doc, 'Eén regel per zaak. De eerste kolom is wat op hun antwoordblad hoort te staan, '
            'de tweede wat je in het bestand controleert.')
tabel(doc, ['Zaak', 'Op het antwoordblad', 'In het bestand'],
      [[zaak['nr'], sl.OPLOSSING[zaak['nr']],
        f"{next(m['waar'] for m in zaak['maken'] if m.get('genest'))} bevat een formule "
        f"met een functie binnen een functie"] for zaak in z.ZAKEN])

kop(doc, 'Wat je het vaakst zult tegenkomen', 2)
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Hoe erg'], [
    ['De sleutelformule is opgesplitst in twee cellen.',
     'Ze hebben het binnenste stuk in een hulpcel laten staan.',
     'Half goed. Ze begrijpen het, maar de laatste stap ontbreekt. Laat ze de hulpcel '
     'binnenschuiven en wissen.'],
    ['#N/B in een VERT.ZOEKEN-kolom.', 'Dollartekens rond de zoektabel vergeten.',
     'Staat in hun bundel. Zelf op te lossen.'],
    ['De proef komt niet uit maar het antwoord wel.',
     'Toeval, of een cel die ze overgetypt hebben.',
     'Kijken. Een antwoord zonder kloppende proef is geen antwoord.'],
    ['Alles klopt, maar er staat een getal in plaats van een formule.',
     'Uitgerekend en overgetypt.',
     'Dat is het enige wat de proef niet vangt. Klik de cel aan en lees de formulebalk.'],
    ['Ze vinden de dader door gewoon te kijken.',
     'Dat kan bij zaak 1, 3 en 5 inderdaad met het oog.',
     'Geen ramp — de formule is het bewijs. Vraag hen hoe ze het zouden doen met duizend '
     'rijen.'],
])

doc.save(MAP + 'detective-leerkrachtensleutel.docx')
print('leerkrachtensleutel geschreven')
for zaak in z.ZAKEN:
    print(f"  zaak {zaak['nr']}: {sl.OPLOSSING[zaak['nr']][:70]}")
