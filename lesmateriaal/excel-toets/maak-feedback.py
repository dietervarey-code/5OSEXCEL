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
        uit.append(f'{len(goed)} van de {len(alles)} opdrachten staan juist, goed voor '
                   f"{getal(r['formulepunten'])} van de {r['formulemax']} formulepunten.")

    getypt = [x for b in r['bladen'] for x in b['regels'] if x['zonder_formule']]
    if not getypt:
        uit.append('In elke cel staat een echte formule. Nergens een getal dat je zelf '
                   'hebt uitgerekend en overgetypt — dat is precies waar het om ging.')

    functies = sorted({x['functie'] for b in r['bladen'] for x in b['regels']
                       if x['functie'] and x['punten'] == x['max']})
    if len(functies) >= 8:
        uit.append('Juist gebruikt: ' + ', '.join(functies) + '.')
    elif functies:
        uit.append('Juist gebruikt: ' + ', '.join(functies) + '.')

    matrix = [(b, x) for b in r['bladen'] for x in b['regels']
              if x.get('matrix') and x['punten'] == x['max']]
    if matrix:
        waar = ', '.join(f"blad {b['nr']} {x['waar']}" for b, x in matrix)
        uit.append(f'Je hebt matrixformules gebruikt ({waar}): één formule die het hele '
                   'bereik in één keer vult, zonder doorvoeren. Dat zat niet in de les. '
                   'Het werkt hier en het is knap, maar weet dat het alleen in recente '
                   'versies van Excel bestaat — op een toestel met een oudere versie '
                   'krijg je er een foutmelding mee.')

    # Wie weinig haalde, hoort toch te weten wat zijn stevigste antwoord was.
    zwaar = [(b, x) for b in r['bladen'] for x in b['regels']
             if x['punten'] == x['max'] and x['max'] >= 2]
    if zwaar and r['formulepunten'] < r['formulemax'] * 0.6:
        b, x = max(zwaar, key=lambda bx: bx[1]['max'])
        uit.append(f"Je zwaarst wegende juiste antwoord staat op blad {b['nr']}, "
                   f"{x['waar']} — {x['wat']} ({x['max']} punten). Dat is niet het "
                   'gemakkelijkste van de toets.')
    return uit


def werkpunten(r):
    """Wat er misliep, met het celadres erbij zodat hij het kan terugzoeken."""
    uit = []
    # Een blad dat helemaal niet gemaakt is, krijgt één regel in plaats van
    # zeven keer 'niet gemaakt'. Zijn het er meerdere, dan staan ze samen in
    # één zin: vier keer dezelfde mededeling leest als een verwijt.
    onaf = [b for b in r['bladen']
            if all(x['opmerking'].startswith('niet gemaakt') for x in b['regels'])]
    if len(onaf) == 1:
        b = onaf[0]
        uit.append(f"Blad {b['nr']} ({b['blad']}) is niet gemaakt. Daar liggen "
                   f"{b['formulemax'] + b['opmaakmax']} punten, de volledige waarde "
                   'van het blad. Je bent er wellicht niet aan toe gekomen.')
    elif onaf:
        namen = ', '.join(f"{b['nr']} ({b['blad'].split(' ', 1)[1]})" for b in onaf)
        samen = sum(b['formulemax'] + b['opmaakmax'] for b in onaf)
        uit.append(f'Deze werkbladen zijn niet gemaakt: {namen}. Samen is dat {samen} '
                   'van de 50 punten.')

    for b in r['bladen']:
        if b in onaf:
            continue
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
    """Dingen die geen punten kosten maar die hij wel moet weten."""
    uit = []
    for b in r['bladen']:
        for e in b['opmaak']:
            if e.get('opmerking'):
                uit.append(f"Blad {b['nr']}: {e['opmerking']}.")
        for x in b['regels']:
            if x.get('doorwerkend'):
                uit.append(f"Blad {b['nr']}, {x['waar']}: {x['opmerking']}.")
            if x.get('handmatig') and x['punten'] == x['max']:
                # Bij AANTAL.ALS en SOM.ALS komt het criterium uit een cel; bij
                # een gewone som voer je gewoon door. Twee verschillende raden.
                raad = ('Verwijs naar de cel ernaast als criterium, dan volstaat één '
                        'formule die je doorvoert.'
                        if x['functie'] in ('AANTAL.ALS', 'SOM.ALS')
                        else 'Typ ze één keer en sleep de vulgreep; dat kan ook '
                             'zijwaarts.')
                uit.append(
                    f"Blad {b['nr']}, {x['waar']}: je antwoord klopt, maar je hebt per "
                    'cel een aparte formule getypt in plaats van er één door te voeren. '
                    'Dat werkt, maar het is meer werk en bij elke tikfout gaat er stil '
                    'één cel mis. ' + raad)
            if x.get('schuift') and x['punten'] == x['max']:
                uit.append(
                    f"Blad {b['nr']}, {x['waar']}: je antwoord klopt, maar je bereik "
                    'staat niet vast met dollartekens. Het schuift mee bij het '
                    'doorvoeren, en hier kwam dat toevallig goed uit omdat de gegevens '
                    'netjes gegroepeerd stonden. Bij een andere volgorde loopt het mis.')
            if x.get('zonder_functie') and x['punten'] == x['max']:
                uit.append(
                    f"Blad {b['nr']}, {x['waar']}: het antwoord klopt, maar "
                    f"{x['functie']} staat niet in elke cel ({', '.join(x['zonder_functie'])}).")
            if x['zonder_formule'] and x['punten'] > 0:
                uit.append(f"Blad {b['nr']}, {x['waar']}: het antwoord klopt, maar er "
                           'staat een getal in plaats van een formule. Dat telt niet mee.')
    return uit


def grootste_oorzaak(r):
    """Waar gingen de meeste punten verloren? Dat bepaalt de slotzin, zodat
       die over deze leerling gaat en niet over zijn cijfer."""
    verlies = {'opmaak': 0.0, 'getypt': 0.0, 'niet gemaakt': 0.0, 'formules': 0.0}
    for b in r['bladen']:
        # Een blad dat hij niet gehaald heeft, zegt niets over zijn werkwijze.
        # Dat staat al apart in de werkpunten; het advies moet gaan over wat
        # hij wél aanraakte.
        if all(x['opmerking'].startswith('niet gemaakt') for x in b['regels']):
            continue
        for e in b['opmaak']:
            verlies['opmaak'] += e['max'] - e['punten']
        for x in b['regels']:
            tekort = x['max'] - x['punten']
            if not tekort:
                continue
            if x['zonder_formule']:
                verlies['getypt'] += tekort
            elif x['opmerking'].startswith('niet gemaakt'):
                verlies['niet gemaakt'] += tekort
            else:
                verlies['formules'] += tekort
    grootste = max(verlies, key=verlies.get)
    return (grootste, verlies[grootste]) if verlies[grootste] > 0 else (None, 0)


RAAD = {
    'opmaak': ('Wat je nog laat liggen is de opmaak. Lees bij een volgende toets de '
               'opmaakeisen één voor één af als een checklist: het staat er allemaal '
               'letterlijk bij, en het zijn punten die je zo meeneemt.'),
    'getypt': ('Je grootste verlies zit niet in wat je kent, maar in hoe je het '
               'opschrijft: op een paar plaatsen heb je het antwoord zelf uitgerekend '
               'en ingetypt. Dat telt niet mee, ook al klopt het. Laat Excel rekenen — '
               'dan past het zich ook aan als er een cijfer verandert.'),
    'niet gemaakt': ('Je verliest de meeste punten aan werk dat niet af is. Kijk voor je '
                     'afgeeft nog eens de opdracht door en vink af: staat er in elke '
                     'gevraagde cel iets?'),
    'formules': ('Je verliest de meeste punten in de formules zelf. Kijk bij de '
                 'werkpunten hierboven welke cel het was en open ze in je eigen '
                 'bestand: meestal klopt de functie wel en is het het bereik dat '
                 'niet ver genoeg loopt of meeschuift.'),
}


def slotzin(r):
    deel = r['totaal'] / r['maximum']
    oorzaak, verlies = grootste_oorzaak(r)
    onaf = [b for b in r['bladen']
            if all(x['opmerking'].startswith('niet gemaakt') for x in b['regels'])]
    if len(onaf) == 1 and oorzaak:
        b = onaf[0]
        return (f'Blad {b["nr"]} heb je niet meer gehaald; dat verklaart een flink deel '
                f'van wat je mist. Op de bladen die je wél maakte, zit je verlies ergens '
                f'anders. ' + RAAD[oorzaak])
    if len(onaf) >= 2:
        gedaan = len(r['bladen']) - len(onaf)
        behaald = sum(b['formulepunten'] + b['opmaakpunten'] for b in r['bladen']
                      if b not in onaf)
        haalbaar = sum(b['formulemax'] + b['opmaakmax'] for b in r['bladen']
                       if b not in onaf)
        sterk_bezig = haalbaar and behaald / haalbaar >= 0.8
        kern = ('wat je maakte, maakte je grotendeels juist'
                if sterk_bezig
                else f'op de bladen die je wél maakte haalde je {getal(behaald)} van de '
                     f'{haalbaar} punten')
        return (f'Van de vijf werkbladen heb je er {gedaan} aangeraakt. Een flink deel van '
                f'wat je mist, mis je omdat je er niet aan toe gekomen bent: {kern}. '
                'Werk de herhalingsbundel nog eens door tot de formules er vlot uit '
                'komen — daarna haal je op dezelfde tijd veel meer bladen af.')
    # Een halve punt verlies is geen werkpunt. Dan hoort er geen raadgeving
    # bij alsof er iets scheelt.
    if verlies <= 1:
        oorzaak = None
    if deel >= 0.9 and oorzaak is None:
        return ('Uitstekend. Je beheerst de basisfuncties en je werkt netjes. Voor jou is '
                'de volgende stap: functies in elkaar zetten — dan kan je vragen '
                'beantwoorden waar één functie niet aan toe komt.')
    if deel >= 0.9:
        opening = ('Uitstekend. Je beheerst de basisfuncties en je werkt netjes. ')
    elif deel >= 0.8:
        opening = 'Sterk werk. De functies zitten goed. '
    elif deel >= 0.65:
        opening = 'Een goed resultaat. De basis staat er. '
    elif deel >= 0.5:
        opening = 'Je haalt het, maar er blijven punten liggen die binnen bereik lagen. '
    else:
        opening = ('Dit is nog niet goed genoeg, maar het is herstelbaar: de fouten '
                   'zitten in een paar dingen die terugkeren. ')
    return opening + RAAD.get(oorzaak, '')


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
