# -*- coding: utf-8 -*-
"""Bouwt de opdrachtbundel en de lerarensleutel van de Ottomaanse bundel."""
import importlib.util
import os
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')

OPDRACHT = os.path.join(HIER, 'ottomaans-opdracht.docx')
SLEUTEL = os.path.join(HIER, 'ottomaans-lerarensleutel.docx')

BLAUW = RGBColor(0x1F, 0x38, 0x64)
ORANJE = RGBColor(0xB0, 0x4A, 0x00)
GRIJS = RGBColor(0x59, 0x59, 0x59)
GROEN = RGBColor(0x38, 0x76, 0x1D)

FORMULE = re.compile(r"(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|=[A-Z$]+\d+(?:[*+\-/]"
                     r"[A-Z$]*\d+)*)")


def opzet(doc):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'
    s.font.size = Pt(11)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.5)
        sec.left_margin = sec.right_margin = Cm(1.8)


def kop(doc, tekst, niveau=1, kleur=BLAUW):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs:
        r.font.color.rgb = kleur
    return p


def zin(p, tekst):
    """Zet formules in een vaste letter, zodat ze opvallen in lopende tekst."""
    for stuk in FORMULE.split(str(tekst)):
        if not stuk:
            continue
        r = p.add_run(stuk)
        if FORMULE.fullmatch(stuk):
            r.font.name = 'Consolas'
            r.font.size = Pt(10)
    return p


def alinea(doc, tekst, style=None, vet=False, schuin=False, kleur=None,
           grootte=None, na=None):
    p = doc.add_paragraph(style=style)
    if vet or schuin or kleur or grootte:
        r = p.add_run(str(tekst))
        r.bold, r.italic = vet, schuin
        if kleur:
            r.font.color.rgb = kleur
        if grootte:
            r.font.size = Pt(grootte)
    else:
        zin(p, tekst)
    if na is not None:
        p.paragraph_format.space_after = Pt(na)
    return p


def kader(doc, titel, regels, kleur=BLAUW):
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    c = t.rows[0].cells[0]
    r = c.paragraphs[0].add_run(titel)
    r.bold = True
    r.font.color.rgb = kleur
    for regel in regels:
        pp = c.add_paragraph()
        pp.paragraph_format.space_after = Pt(2)
        zin(pp, regel)
    doc.add_paragraph()
    return t


def tabel(doc, koppen, rijen, stijl='Light Grid Accent 1', breedtes=None):
    t = doc.add_table(rows=1, cols=len(koppen))
    t.style = stijl
    for i, k in enumerate(koppen):
        t.rows[0].cells[i].paragraphs[0].add_run(str(k)).bold = True
    for rij in rijen:
        cellen = t.add_row().cells
        for i, w in enumerate(rij):
            zin(cellen[i].paragraphs[0], w)
    if breedtes:
        for rij in t.rows:
            for i, b in enumerate(breedtes):
                rij.cells[i].width = Cm(b)
    doc.add_paragraph()
    return t


def paginaeinde(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def genummerd(doc, regels, kleur=BLAUW):
    for i, regel in enumerate(regels, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f'{i}.  ')
        r.bold = True
        r.font.color.rgb = kleur
        zin(p, regel)


# ==========================================================================
#  1. de opdrachtbundel
# ==========================================================================
doc = Document()
opzet(doc)

kop(doc, g.TITEL, 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=4)
alinea(doc, 'Naam: ......................................    Klas: ..........',
       na=14)

alinea(doc,
       f'Vijf werkbladen, samen ongeveer {g.DUUR} minuten. De eerste drie zijn '
       'herhaling: functies die je al kent, op gegevens uit de geschiedenis van het '
       'Ottomaanse Rijk. Blad 4 en 5 zijn nieuw. Daar typ je geen formules meer, '
       'maar sleep je een lijst in elkaar tot een overzicht en maak je er een '
       'grafiek van.', na=8)
alinea(doc,
       'Werk in volgorde. Blad 2 haalt gegevens uit blad 1, en blad 4 vat blad 2 en '
       '3 samen. Sla een blad over en je loopt vast.', na=12)

tabel(doc, ['Blad', 'Wat', 'Duur', 'Waarmee'],
      [[f"{oef['nr']}  {oef['blad'][2:]}", oef['titel'], oef['duur'],
        ', '.join(dict.fromkeys(
            r['hoe'] for r in oef['regels']
            if r['hoe'] not in (o.LEZEN,)))]
       for oef in o.OEFENINGEN],
      breedtes=[3.4, 4.6, 2.2, 7.0])

kader(doc, 'Wat je erbij nodig hebt', [
    f'{g.FUNCTIEBUNDEL} — de functiefiches die je al kent. Voor blad 1 tot 3.',
    f'{g.THEORIEBUNDEL} — de nieuwe theoriebundel. Kaart 1 tot 9 voor blad 4, '
    'kaart 10 tot 14 voor blad 5.',
], BLAUW)

kader(doc, 'Drie regels die op deze bundel anders zijn', [
    '1.  De lijsten op blad 2 en 3 worden straks de bron van een draaitabel. Voeg er '
    'geen lege rij in, zet er geen totaalrij onder en verwijder er niets uit. De '
    'tellingen staan daarom ERNAAST, met een lege kolom ertussen.',
    '2.  Op blad 4 en 5 typ je geen formules. Je sleept, je kiest een grafiektype en '
    'je leest af.',
    '3.  Een draaitabel rekent niet automatisch mee. Verander je iets aan blad 2 of '
    '3, vernieuw dan je draaitabel (rechtsklik erin, Vernieuwen).',
], ORANJE)

kader(doc, 'Over de cijfers', [g.WAARSCHUWING], GRIJS)

for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Blad {oef['nr']} — {oef['titel']}", 1)
    alinea(doc, f"werkblad '{oef['blad']}'  ·  {oef['duur']}", schuin=True,
           kleur=GRIJS, na=8)
    for regel in oef['inleiding']:
        alinea(doc, regel, na=4)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

    kop(doc, 'Wat je maakt', 2, GRIJS)
    tabel(doc, ['Waar', 'Wat', 'Waarmee'],
          [[r['waar'], r['wat'], r['hoe']] for r in oef['regels']],
          breedtes=[3.2, 8.4, 5.6])

    toelichtingen = [(r['waar'], r['toelichting']) for r in oef['regels']
                     if r.get('toelichting')]
    if toelichtingen:
        kop(doc, 'Waar je op moet letten', 2, GRIJS)
        for waar, tekst in toelichtingen:
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(f'{waar}  —  ')
            r.bold = True
            r.font.color.rgb = BLAUW
            zin(p, tekst)
        doc.add_paragraph().paragraph_format.space_after = Pt(0)

    kop(doc, 'Opmaak', 2, GRIJS)
    for tekst, _ in oef['opmaak']:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        zin(p, tekst)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

    kader(doc, 'Je blad is af als…', [oef['klaar'], '', 'CONTROLE  ·  ' +
                                      oef['controle']], GROEN)
    kader(doc, 'Loop je vast?', oef['vast'], ORANJE)

paginaeinde(doc)
kop(doc, 'Helemaal klaar?', 1)
alinea(doc, 'Loop dit lijstje af voor je indient.', schuin=True, kleur=GRIJS, na=8)
for regel in [
    'Elk controlegetal klopt.',
    'Nergens staat #N/B, #WAARDE! of #DEEL/0!.',
    'Je hebt elke formule één keer getypt en doorgevoerd — nergens met de hand '
    'een getal ingevuld.',
    'Je twee draaitabellen zijn vernieuwd (rechtsklik, Vernieuwen).',
    'Het eindtotaal van draaitabel 2 is hetzelfde getal als de SOM op blad 3.',
    'Beide grafieken hebben een titel die zegt wat je ziet.',
    'Je bestand heet ottomaans-jouwnaam.xlsx.',
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run('☐   ')
    r.font.size = Pt(13)
    zin(p, regel)

doc.save(OPDRACHT)
print('geschreven:', OPDRACHT)


# ==========================================================================
#  2. de lerarensleutel
# ==========================================================================
doc = Document()
opzet(doc)

kop(doc, g.TITEL + ' — lerarensleutel', 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=12)

kop(doc, 'In het kort', 2, GRIJS)
alinea(doc,
       f'Vijf werkbladen, {g.DUUR} minuten. Blad 1 tot 3 zijn herhaling op '
       f'{sum(1 for oef in o.OEFENINGEN[:3] for _ in oef["regels"])} formules; '
       'blad 4 en 5 brengen de draaitabel en de grafiek binnen. Er zit geen enkele '
       'geneste functie in: wat nieuw is, is nieuw genoeg.', na=6)
alinea(doc,
       f'{o.TOTAAL} punten voor het werk en {o.TOTAAL_OPMAAK} voor de opmaak, samen '
       f'{o.TOTAAL_ALLES}. Twee derde daarvan geeft een score op 50.', na=10)

tabel(doc, ['Blad', 'Duur', 'Werk', 'Opmaak', 'Samen'],
      [[f"{oef['nr']}  {oef['blad'][2:]}", oef['duur'],
        sum(r['punten'] for r in oef['regels']),
        sum(p for _, p in oef['opmaak']),
        sum(r['punten'] for r in oef['regels']) + sum(p for _, p in oef['opmaak'])]
       for oef in o.OEFENINGEN]
      + [['Samen', f'{g.DUUR} minuten', o.TOTAAL, o.TOTAAL_OPMAAK, o.TOTAAL_ALLES]],
      breedtes=[4.6, 3.0, 2.6, 2.6, 2.6])

kader(doc, 'Wat je zelf moet weten voor je dit uitdeelt', [
    'Een draaitabel kan niet in het startbestand zitten: de bibliotheek waarmee deze '
    'bestanden gemaakt worden, kan er geen schrijven. Dat komt goed uit — de leerling '
    'hoort ze zelf te maken. In deze sleutel staat wél precies WAT er in hun '
    'draaitabel moet staan, cel per cel, zodat je het blad ernaast kan leggen.',
    'De bevolkingscijfers op blad 5 zijn ruwe schattingen. Dat staat op het '
    'startblad, in de opdracht en hieronder. Voor het Ottomaanse Rijk bestaan er geen '
    'betrouwbare tellingen van vóór 1831, en de getallen in de literatuur lopen fors '
    'uiteen. Ze dienen om te rekenen en te tekenen.',
    g.B1_VOETNOOT,
    g.B3_VOETNOOT,
], ORANJE)

kader(doc, 'De drie dingen waar het mis gaat', [
    '1.  Op blad 2 vergeten ze de dollartekens rond de zoektabel. Onderaan kolom G '
    'staat dan #N/B. Dat is dezelfde fout als in de vorige bundels; ze is hier alleen '
    'zichtbaarder omdat de lijst 35 rijen telt.',
    '2.  Op blad 4 staat hun draaitabel op Aantal in plaats van Som. Herkenbaar aan '
    'het eindtotaal: staat er 18 in plaats van 171, dan telt ze de oorlogen in plaats '
    'van de jaren. Laat ze naar het kopje van de draaitabel kijken.',
    '3.  Op blad 5 nemen ze de kolom Jaar mee als reeks in het lijndiagram. Ze krijgen '
    'dan twee lijnen, waarvan één die van 1520 naar 1914 klimt en de andere plat ligt.',
], ORANJE)

for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Blad {oef['nr']} — {oef['titel']}", 1)
    alinea(doc, f"werkblad '{oef['blad']}'  ·  {oef['duur']}  ·  "
                f"{sum(r['punten'] for r in oef['regels'])} + "
                f"{sum(p for _, p in oef['opmaak'])} punten",
           schuin=True, kleur=GRIJS, na=8)

    rijen = []
    for r in oef['regels']:
        if r.get('formule'):
            antwoord = r['formule']
        elif r.get('antwoord') is not None:
            antwoord = str(r['antwoord'])
        else:
            antwoord = '(zie hieronder)'
        rijen.append([r['waar'], antwoord, r['punten']])
    tabel(doc, ['Waar', 'Formule of antwoord', 'Pt'], rijen,
          breedtes=[3.4, 11.6, 1.4])

    if oef['nr'] == 1:
        kop(doc, 'De uitkomsten', 2, GRIJS)
        tabel(doc, ['Code', 'Sultan', 'Van', 'Tot', 'Jaren', 'Lang?'],
              [[c, n, b, e, a.B1_JAREN[i], a.B1_LANG[i]]
               for i, (c, n, b, e) in enumerate(g.B1)], 'Light List Accent 1')
        tabel(doc, ['Cel', 'Uitkomst'],
              [[f'B{g.B1_SAMENVATTING}', f'{a.B1_SOM} jaar samen'],
               [f'B{g.B1_SAMENVATTING + 1}',
                f'{a.B1_GEMIDDELDE:.4f} — toon op één decimaal: '
                f'{a.B1_GEMIDDELDE:.1f}'],
               [f'B{g.B1_SAMENVATTING + 2}', f'{a.B1_MAX} ({a.B1_LANGSTE})'],
               [f'B{g.B1_SAMENVATTING + 3}', f'{a.B1_MIN} ({a.B1_KORTSTE})'],
               [f'B{g.B1_SAMENVATTING + 4}', a.B1_AANTAL],
               [f'B{g.B1_SAMENVATTING + 5}', a.B1_LANGE]])
        kader(doc, 'De val op dit blad', [
            f'{", ".join(a.B1_GRENSGEVAL)} regeerde precies {g.B1_DREMPEL} jaar, de '
            'grens zelf. Wie > typt in plaats van >= krijgt daar "nee" en komt op '
            f'{a.B1_LANGE - len(a.B1_GRENSGEVAL)} in plaats van {a.B1_LANGE}. Dat is '
            'het enige verschil in hun hele blad, dus het valt alleen op in de laatste '
            'cel.',
            f'B{g.B1_SAMENVATTING + 4} vraagt AANTAL. Richten ze dat op de namen in '
            'kolom B, dan krijgen ze 0 — AANTAL telt alleen getallen. Kolom C of D '
            'werkt wel.',
        ], GROEN)

    if oef['nr'] == 2:
        kop(doc, 'Steekproef op de uitkomsten', 2, GRIJS)
        proef = [0, 7, 19, len(g.B2) - 1]
        tabel(doc, ['Rij', 'Jaar', 'Code', 'G (sultan)', 'H (jaren)', 'I (lang?)'],
              [[g.B2_START + i, g.B2[i][0], g.B2[i][4], a.B2_SULTAN[i],
                a.B2_JAREN[i], a.B2_LANG[i]] for i in proef],
              'Light List Accent 1')
        tabel(doc, ['Cel', 'Uitkomst'],
              [[f'{o._kol(g.B2_VRAAGKOL + 1)}{g.B2_VRAAGRIJ + 1}', a.B2_AANTAL],
               [f'{o._kol(g.B2_VRAAGKOL + 1)}{g.B2_VRAAGRIJ + 2}', a.B2_TEL_SOORT],
               [f'{o._kol(g.B2_VRAAGKOL + 1)}{g.B2_VRAAGRIJ + 3}', a.B2_TEL_REGIO],
               [f'{o._kol(g.B2_VRAAGKOL + 1)}{g.B2_VRAAGRIJ + 4}', a.B2_TEL_EEUW]])

    if oef['nr'] == 3:
        kop(doc, 'De uitkomsten', 2, GRIJS)
        tabel(doc, ['Oorlog', 'Tegenstander', 'Duur', 'Uitkomst', 'Lang?'],
              [[n, t, a.B3_DUUR[i], u, a.B3_LANG[i]]
               for i, (n, t, _, _, u) in enumerate(g.B3)], 'Light List Accent 1')
        tabel(doc, ['Cel', 'Uitkomst'],
              [[f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 1}', a.B3_SOM],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 2}',
                f'{a.B3_GEMIDDELDE:g}'],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 3}',
                f'{a.B3_MAX} ({a.B3_LANGSTE})'],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 4}',
                f'{a.B3_MIN} ({a.B3_KORTSTE} — begon en eindigde in hetzelfde jaar)'],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 5}', a.B3_TEL],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 6}', a.B3_SOMLAND],
               [f'{o._kol(g.B3_VRAAGKOL + 1)}{g.B3_VRAAGRIJ + 7}', a.B3_SOMUITKOMST]])
        kader(doc, 'De val op dit blad', [
            f'De Tweede Balkanoorlog duurde 0 jaar: begin en einde liggen in {g.B3[16][2]}. '
            'Wie dat voor een fout houdt, gaat het "verbeteren" naar 1 en klopt zijn '
            'MIN en zijn SOM aan diggelen. Zeg erbij dat 0 mag.',
            'Bij SOM.ALS wisselen ze het zoekbereik en het optelbereik om. Ze krijgen '
            'dan 0 of een foutmelding. Anders dan bij SOMMEN.ALS komt het zoekbereik '
            'hier EERST.',
        ], GROEN)

    if oef['nr'] == 4:
        kop(doc, 'Draaitabel 1 — zo moet ze eruitzien', 2, GRIJS)
        alinea(doc, f"Bron: blad '{g.B4_DRAAI1['bron']}', bereik "
                    f"A{g.B2_KOPRIJ}:{o._kol(len(g.B2_KOP))}{g.B2_EIND}. "
                    f"Rijen = {g.B4_DRAAI1['rijen']}, "
                    f"Kolommen = {g.B4_DRAAI1['kolommen']}, "
                    f"Waarden = Aantal van {g.B4_DRAAI1['waarden']}.",
               schuin=True, kleur=GRIJS, na=6)
        tabel(doc, ['Aantal'] + a.D1_KOLLABELS + ['Eindtotaal'],
              [[r] + [a.D1_CEL[(r, k)] or '' for k in a.D1_KOLLABELS]
               + [a.D1_RIJTOTAAL[r]] for r in a.D1_RIJLABELS]
              + [['Eindtotaal'] + [a.D1_KOLTOTAAL[k] for k in a.D1_KOLLABELS]
                 + [a.D1_EINDTOTAAL]], 'Light List Accent 1')
        alinea(doc,
               f'De {g.B2[0][0]} valt nog in de {a.D1_KOLLABELS[0]} — eeuwen beginnen '
               'op 01 en eindigen op 00. Die kolom met één gebeurtenis erin is dus '
               'juist, en een mooi bruggetje naar de geschiedenisles.', na=10)

        kop(doc, 'Draaitabel 2 — zo moet ze eruitzien', 2, GRIJS)
        alinea(doc, f"Bron: blad '{g.B4_DRAAI2['bron']}', bereik "
                    f"A{g.B3_KOPRIJ}:{o._kol(len(g.B3_KOP))}{g.B3_EIND}. "
                    f"Rijen = {g.B4_DRAAI2['rijen']}, "
                    f"Waarden = Som van {g.B4_DRAAI2['waarden']}, aflopend gesorteerd.",
               schuin=True, kleur=GRIJS, na=6)
        tabel(doc, ['Tegenstander', 'Som van de duur'],
              [[t, a.D2[t]] for t in a.D2_AFLOPEND]
              + [['Eindtotaal', a.D2_EINDTOTAAL]], 'Light List Accent 1',
              breedtes=[6.0, 5.0])
        kader(doc, 'Waar je naar kijkt bij het verbeteren', [
            f'Eindtotaal van draaitabel 1 = {a.D1_EINDTOTAAL}. Staat er iets anders, '
            'dan zit er een rij te veel of te weinig in de bron.',
            f'Eindtotaal van draaitabel 2 = {a.D2_EINDTOTAAL}. Dat is hetzelfde getal '
            f'als de SOM die ze op blad 3 al berekenden. Staat er {len(g.B3)}, dan '
            'staat hun waardeveld op Aantal in plaats van Som.',
            f'{a.D2_AFLOPEND[3]} en {a.D2_AFLOPEND[4]} staan allebei op '
            f'{a.D2[a.D2_AFLOPEND[3]]}, en {a.D2_AFLOPEND[-2]} en {a.D2_AFLOPEND[-1]} '
            'allebei op 1. De volgorde tussen die twee paren mag dus anders zijn dan '
            'hierboven.',
            'Of ze de tabel op de juiste cel gezet hebben, is bijzaak. Of ze ze '
            'gesorteerd hebben, niet: dat is wat de vraag erna leesbaar maakt.',
        ], GROEN)

    if oef['nr'] == 5:
        kop(doc, 'De verschilkolom', 2, GRIJS)
        tabel(doc, ['Jaar', 'Miljoen', 'Verschil'],
              [[j, n, '' if a.B5_VERSCHIL[i] is None else f'{a.B5_VERSCHIL[i]:+d}']
               for i, (j, n) in enumerate(g.B5)], 'Light List Accent 1',
              breedtes=[3.0, 3.6, 3.6])
        kader(doc, 'Wat je van de grafieken verwacht', [
            f'Grafiek 1 is een staafdiagram (of draaigrafiek) van draaitabel 2. '
            f'{a.D2_TOP} heeft de langste balk met {a.D2_TOP_JAREN} jaar. Er hoort '
            'geen balk voor het eindtotaal in te staan.',
            f'Grafiek 2 is een lijndiagram van A{g.B5_KOPRIJ}:B{g.B5_EIND}. Eén lijn, '
            f'die piekt in {a.B5_HOOGSTE_JAAR} op {a.B5_HOOGSTE} en daarna daalt.',
            'Twee lijnen in grafiek 2 betekent dat ze de kolom Jaar als reeks hebben '
            'meegenomen.',
            'De metingen liggen niet even ver uit elkaar (80, 100, 50, 25, 25 en 14 '
            'jaar) en een gewoon lijndiagram zet ze toch op gelijke afstand. Dat staat '
            'op kaart 14 van de theoriebundel. Een leerling die dat zelf opmerkt, '
            'verdient een pluim.',
        ], GROEN)

    if oef['opmaak']:
        kop(doc, 'Opmaak', 2, GRIJS)
        tabel(doc, ['Wat', 'Pt'], [[t, p] for t, p in oef['opmaak']],
              breedtes=[14.0, 1.4])

paginaeinde(doc)
kop(doc, 'Tijdsindeling en tips', 1)
tabel(doc, ['Wanneer', 'Wat'],
      [['0 - 5 min', 'Bestand openen en opslaan onder hun eigen naam. Theoriebundel '
                     'uitdelen. Zeg dat blad 4 en 5 nieuw zijn en dat ze daar niets '
                     'hoeven te typen.'],
       ['5 - 30 min', 'Blad 1 tot 3 zelfstandig. Dit is herhaling; loop rond en kijk '
                      'vooral naar de dollartekens op blad 2.'],
       ['30 - 32 min', 'Kort klassikaal moment. Toon één keer hoe je een draaitabel '
                       'invoegt en de velden sleept. Niet meer dan dat — de rest staat '
                       'op de kaarten.'],
       ['32 - 44 min', 'Blad 4. Hier zit de leerwinst. Verwacht dat de helft eerst '
                       'Aantal krijgt waar Som hoort.'],
       ['44 - 50 min', 'Blad 5. Wie niet aan de tweede grafiek komt, heeft de les toch '
                       'gehad.']],
      breedtes=[3.4, 13.0])

kader(doc, 'Als je weinig tijd hebt', [
    'Laat blad 3 vallen en begin na blad 2 meteen aan de draaitabel. Draaitabel 1 '
    f'(uit blad 2) volstaat om alles te tonen; dan vervalt ook de tweede draaitabel '
    'en maken ze hun staafdiagram van draaitabel 1 in plaats van 2.',
    'Blad 5 kan ook als apart lesje van tien minuten op een andere dag. De '
    'bevolkingsgrafiek staat los van de rest.',
], BLAUW)

kader(doc, 'Waar dit op aansluit', [
    'De functies op blad 1 tot 3 zijn exact die van de basisbundel en de twee '
    'herhalingsbundels. Er komt geen enkele nieuwe functie bij.',
    f'De theoriebundel {g.THEORIEBUNDEL} staat los van deze opdracht en is herbruikbaar: '
    'de voorbeelden spelen in de schoolbibliotheek en de kantine, niet in het '
    'Ottomaanse Rijk.',
    'Wie hier vlot doorkomt, kan dezelfde draaitabeloefening op eender welke lijst: '
    'de ledenlijst van een club, de resultaten van een enquête, hun eigen '
    'uurrooster.',
], BLAUW)

doc.save(SLEUTEL)
print('geschreven:', SLEUTEL)
