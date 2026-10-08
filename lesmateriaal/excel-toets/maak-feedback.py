# -*- coding: utf-8 -*-
"""Maakt de feedbackfiche van één leerling uit het resultaat van nakijken.py.

Gebruik:  python3 -I maak-feedback.py <resultaat.json>

De fiche is voor de leerling zelf: wat hij haalde, wat goed ging, en wat er
concreet misliep — met het celadres erbij, zodat hij het kan terugzoeken in
zijn eigen bestand.
"""
import json
import os
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.dont_write_bytecode = True

BLAUW = RGBColor(0x1F, 0x38, 0x64)
GROEN = RGBColor(0x1E, 0x6B, 0x3A)
ROOD = RGBColor(0xA0, 0x1B, 0x1B)
GRIJS = RGBColor(0x59, 0x59, 0x59)
FORMULE = re.compile(r'(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|=[A-Z$]+\d+(?:[*+\-/][A-Z$]*\d+)*)')


def getal(x):
    return f'{x:g}'.replace('.', ',')


def opzet(doc):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'
    s.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.4)
        sec.left_margin = sec.right_margin = Cm(1.8)


def kop(doc, tekst, niveau=1, kleur=BLAUW):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs:
        r.font.color.rgb = kleur
        r.font.size = Pt(13 if niveau == 2 else 16)
    return p


def zin(p, tekst):
    for stuk in FORMULE.split(tekst):
        if not stuk:
            continue
        r = p.add_run(stuk)
        if FORMULE.fullmatch(stuk):
            r.font.name = 'Consolas'
            r.font.size = Pt(9.5)
    return p


def alinea(doc, tekst, style=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(3)
    zin(p, tekst)
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
        pp.paragraph_format.space_after = Pt(1)
        zin(pp, regel)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def tabel(doc, koppen, rijen, stijl='Light Grid Accent 1'):
    t = doc.add_table(rows=1, cols=len(koppen))
    t.style = stijl
    for i, k in enumerate(koppen):
        r = t.rows[0].cells[i].paragraphs[0].add_run(k)
        r.bold = True
        r.font.size = Pt(9.5)
    for rij in rijen:
        cellen = t.add_row().cells
        for i, w in enumerate(rij):
            p = cellen[i].paragraphs[0]
            zin(p, str(w))
            for run in p.runs:
                run.font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ---------------------------------------------------------- de tekstjes
def sterk(r):
    """Wat er goed ging — afgeleid uit het resultaat, niet uit de duim."""
    uit = []
    vol = [b for b in r['bladen']
           if b['formulepunten'] + b['opmaakpunten'] == b['formulemax'] + b['opmaakmax']]
    if len(vol) == len(r['bladen']):
        uit.append('Alle vijf de werkbladen staan volledig juist. Formules én opmaak.')
    elif vol:
        namen = ', '.join(f"blad {b['nr']}" for b in vol)
        uit.append(f'Helemaal juist, formules en opmaak samen: {namen}.')

    if r['formulepunten'] == r['formulemax']:
        uit.append(f"Alle {r['formulemax']} punten op de formules. Je hebt de tien "
                   'functies van de bundel alle tien juist ingezet.')
    else:
        goed = [x for b in r['bladen'] for x in b['regels'] if x['punten'] == x['max']]
        alles = [x for b in r['bladen'] for x in b['regels']]
        uit.append(f'{len(goed)} van de {len(alles)} opdrachtcellen staan juist, goed voor '
                   f"{getal(r['formulepunten'])} van de {r['formulemax']} formulepunten.")

    getypt = [x for b in r['bladen'] for x in b['regels'] if x['zonder_formule']]
    if not getypt:
        uit.append('In elke cel staat een echte formule. Nergens een getal dat je zelf '
                   'hebt uitgerekend en overgetypt — dat is precies waar het om ging.')

    functies = sorted({x['functie'] for b in r['bladen'] for x in b['regels']
                       if x['functie'] and x['punten'] == x['max']})
    if len(functies) >= 8:
        uit.append('Juist gebruikt: ' + ', '.join(functies) + '.')
    return uit


def werkpunten(r):
    """Wat er misliep, met het celadres erbij zodat hij het kan terugzoeken."""
    uit = []
    for b in r['bladen']:
        for x in b['regels']:
            if x['punten'] == x['max']:
                continue
            uit.append(f"Blad {b['nr']} ({b['blad']}), {x['waar']} — {x['wat']}: "
                       f"{x['opmerking']}. ({getal(x['punten'])} van de {x['max']})")
        for e in b['opmaak']:
            if e['punten'] == e['max']:
                continue
            uit.append(f"Blad {b['nr']} ({b['blad']}), opmaak: nog te doen — "
                       f"{', '.join(e['gemist'])}. ({getal(e['punten'])} van de "
                       f"{e['max']})")
    return uit


def opmerkingen(r):
    uit = []
    for b in r['bladen']:
        for e in b['opmaak']:
            if e.get('opmerking'):
                uit.append(f"Blad {b['nr']}: {e['opmerking']}.")
        for x in b['regels']:
            if x['zonder_formule'] and x['punten'] > 0:
                uit.append(f"Blad {b['nr']}, {x['waar']}: het antwoord klopt, maar er "
                           'staat een getal in plaats van een formule. Dat telt niet mee.')
    return uit


def slotzin(r):
    deel = r['totaal'] / r['maximum']
    if deel >= 0.9:
        return ('Uitstekend. Je beheerst de basisfuncties en je werkt netjes. Voor jou is '
                'de volgende stap: functies in elkaar zetten — dan kan je vragen '
                'beantwoorden waar één functie niet aan toe komt.')
    if deel >= 0.8:
        return ('Sterk werk. De functies zitten goed; wat je nog laat liggen is detailwerk. '
                'Lees bij een volgende toets de opmaakeisen één voor één af als een '
                'checklist.')
    if deel >= 0.65:
        return ('Een goed resultaat. De basis staat er. Kijk de werkpunten hierboven na in '
                'je eigen bestand: je ziet meteen wat er anders moest.')
    if deel >= 0.5:
        return ('Je haalt het, maar er blijven punten liggen die je met wat meer controle '
                'binnenhaalt. Gebruik de controle die bij elk blad staat — die vindt de '
                'meeste fouten voor je.')
    return ('Dit is nog niet goed genoeg, maar het is wel herstelbaar: de meeste fouten '
            'zitten in dezelfde twee of drie dingen. Werk de herhalingsbundel opnieuw '
            'door en kom daarna langs met je vragen.')


# ------------------------------------------------------------------ main
def fiche(r, pad):
    doc = Document()
    opzet(doc)

    kop(doc, 'Excel-toets — De Rode Duivels in cijfers')
    p = doc.add_paragraph()
    rr = p.add_run(f"{r['naam']}    ·    synthese van de basisfuncties    ·    "
                   f"50 minuten")
    rr.italic = True
    rr.font.color.rgb = GRIJS

    deel = r['totaal'] / r['maximum']
    kleur = GROEN if deel >= 0.65 else (BLAUW if deel >= 0.5 else ROOD)
    kader(doc, f"TOTAAL   {getal(r['totaal'])} / {r['maximum']}", [
        f"Formules: {getal(r['formulepunten'])} van de {r['formulemax']}    ·    "
        f"Opmaak: {getal(r['opmaakpunten'])} van de {r['opmaakmax']}",
    ], kleur)

    kop(doc, 'Per werkblad', 2)
    tabel(doc, ['Werkblad', 'Formules', 'Opmaak', 'Samen'],
          [[f"{b['nr']} — {b['blad'].split(' ', 1)[1]}",
            f"{getal(b['formulepunten'])} / {b['formulemax']}",
            f"{getal(b['opmaakpunten'])} / {b['opmaakmax']}",
            f"{getal(b['formulepunten'] + b['opmaakpunten'])} / "
            f"{b['formulemax'] + b['opmaakmax']}"] for b in r['bladen']]
          + [['Samen', f"{getal(r['formulepunten'])} / {r['formulemax']}",
              f"{getal(r['opmaakpunten'])} / {r['opmaakmax']}",
              f"{getal(r['totaal'])} / {r['maximum']}"]])

    kop(doc, 'Wat goed ging', 2)
    for regel in sterk(r):
        alinea(doc, regel, style='List Bullet')

    punten = werkpunten(r)
    kop(doc, 'Wat er nog beter kan', 2)
    if punten:
        for regel in punten:
            alinea(doc, regel, style='List Bullet')
    else:
        alinea(doc, 'Niets. Er valt op deze toets niets aan te merken.',
               style='List Bullet')

    rest = opmerkingen(r)
    if rest:
        kop(doc, 'Nog dit', 2)
        for regel in rest:
            alinea(doc, regel, style='List Bullet')

    doc.add_paragraph()
    kader(doc, 'Tot slot', [slotzin(r)], kleur)

    doc.save(pad)
    return pad


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('gebruik: python3 -I maak-feedback.py <resultaat.json>')
    with open(sys.argv[1], encoding='utf-8') as fh:
        resultaat = json.load(fh)
    naam = re.sub(r'\W+', '-', resultaat['naam'].lower()).strip('-')
    uit = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),
                       f'feedback-{naam}.docx')
    print('geschreven:', fiche(resultaat, uit))
