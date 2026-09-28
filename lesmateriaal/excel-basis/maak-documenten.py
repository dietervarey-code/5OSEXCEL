# -*- coding: utf-8 -*-
"""Bouwt de vier documenten uit één bron, zodat stappenplan, fiches en
   lerarenuitleg nooit uit elkaar lopen."""
import os
import importlib.util
import re
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


import sys
sys.path.insert(0, HIER)
from schermbeeld import teken

g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
f = laad('f', 'fiches.py')
o = laad('o', 'oefeningen.py')

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
    'De opdrachtomschrijving: per werkblad wat er al staat en wat jij moet maken.',
    'Het stappenplan: daar staat stap voor stap hoe je het aanpakt.',
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
#  1b. OPDRACHTOMSCHRIJVING — één pagina per werkblad
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, 'Opdrachtomschrijving per werkblad')
alinea(doc, 'Per werkblad staat hier wat er al ingevuld is, wat jij moet maken en welke '
            'opmaak erbij hoort. Dit is het overzicht: wíl je weten hoe je het aanpakt, '
            'gebruik dan het stappenplan.')
alinea(doc, 'Weet je een functie niet meer? Op de functiefiches staat per functie hoe ze '
            'werkt, met voorbeelden.')

for i, oef in enumerate(o.OEFENINGEN):
    if i:
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

    kop(doc, 'Functies die je nodig hebt', 3)
    p = doc.add_paragraph()
    for n, naam in enumerate(oef['functies']):
        if n:
            p.add_run('   ·   ')
        r = p.add_run(naam)
        r.font.name = 'Consolas'
        r.bold = True

    kader(doc, 'Je bent klaar als', [oef['klaar']])
    if oef.get('controle'):
        kader(doc, 'Controleer jezelf', [oef['controle']])

doc.save(MAP + 'excel-opdrachtomschrijving.docx')
print('opdrachtomschrijving geschreven')

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
    if oef.get('controle'):
        kader(doc, 'Controleer jezelf', [oef['controle']])

doc.save(MAP + 'excel-stappenplan.docx')
print('stappenplan geschreven')

# =====================================================================
#  3. FUNCTIEBLADEN
# =====================================================================
from docx.shared import Inches

BEELDMAP = os.path.join(HIER, 'beelden')


def rendeer_beeld(spec):
    """Tekent één schermbeeld en geeft het pad terug."""
    pad_png = os.path.join(BEELDMAP, spec['bestand'] + '.png')
    teken(
        pad_png,
        kolommen=spec['kolommen'],
        rijen=spec['rijen'],
        formule=spec.get('formule') or None,
        geselecteerd=spec.get('geselecteerd'),
        gemarkeerd=spec.get('gemarkeerd', ()),
        rechts=spec.get('rechts', ()),
        vet_rij=spec.get('vet_rij'),
    )
    return pad_png


doc = Document()
opzet(doc)
kop(doc, 'Functiefiches')
alinea(doc, 'Eén blad per functie. Elke fiche staat op zichzelf: loop je vast, pak ze erbij '
            'en je kunt verder.')
alinea(doc, 'De voorbeelden op deze fiches gaan NIET over je oefening. Ze spelen in een eigen '
            'wereldje — punten van een toets, temperaturen, uitgaven van een uitstap — zodat je '
            'de functie leert kennen en ze daarna zelf toepast op jouw gegevens. De cellen die '
            'je hier ziet zijn dus andere cellen dan die in je opdracht.')
alinea(doc, 'Achteraan staan vijf fiches over dingen die geen functie zijn, maar die je wel '
            'nodig hebt.')


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

    kop(doc, 'Zo schrijf je ze', 2)
    formuleregel(doc, d['schrijf'])
    for naam, uitleg in d['argumenten']:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(naam)
        r.font.name = 'Consolas'
        r.bold = True
        zin(p, f' — {uitleg}')

    kop(doc, 'Hoe het werkt', 2)
    for regel in d['uitleg']:
        alinea(doc, regel)

    for spec in d['beelden']:
        png = rendeer_beeld(spec)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.add_run().add_picture(png, width=Inches(4.6))
        po = doc.add_paragraph()
        po.paragraph_format.space_after = Pt(10)
        r = po.add_run(spec['onderschrift'])
        r.italic = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = GRIJS

    if d.get('varianten'):
        kop(doc, 'Varianten', 2)
        t = doc.add_table(rows=0, cols=2)
        t.style = 'Light Grid Accent 1'
        for formule, uitleg in d['varianten']:
            c = t.add_row().cells
            rr = c[0].paragraphs[0].add_run(formule)
            rr.font.name = 'Consolas'
            rr.font.size = Pt(9.5)
            zin(c[1].paragraphs[0], uitleg)
        doc.add_paragraph()

    kop(doc, 'Wat je moet weten', 2)
    for regel in d['weten']:
        alinea(doc, regel, style='List Bullet')

    kader(doc, 'De fout die het vaakst gemaakt wordt', [d['fout']])
    if d.get('zelf'):
        kader(doc, 'Probeer het zelf', [d['zelf']])


for d in f.FUNCTIES:
    fiche(doc, d, 'FUNCTIE')
for d in f.HULP:
    fiche(doc, d, 'GEEN FUNCTIE, WEL NODIG')

doc.save(MAP + 'excel-functiebladen.docx')
print(f'functiebladen geschreven ({len(f.FUNCTIES)} functies + {len(f.HULP)} hulpfiches, '
      f'{sum(len(x["beelden"]) for x in f.FUNCTIES + f.HULP)} schermbeelden)')

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
    'excel-opdrachtomschrijving.docx — per werkblad wat gegeven is en wat ze moeten maken',
    'excel-stappenplan.docx — dezelfde vijf oefeningen, maar stap voor stap',
    'excel-functiebladen.docx — vijftien fiches met schermbeelden',
    '',
    'De omschrijving en het stappenplan overlappen bewust. Wie het snapt, werkt met de',
    'omschrijving alleen; wie vastloopt, pakt het stappenplan erbij. Deel ze allebei uit.',
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
formuleregel(doc, f'E4:  =C4*D4            (doorvoeren tot E{g.O1_EIND})')
formuleregel(doc, f'E{g.O1_TOTAAL}: =SOM(E4:E{g.O1_EIND})')
formuleregel(doc, f'C{g.O1_TOTAAL}: =SOM(C4:C{g.O1_EIND})')
alinea(doc, f'Totaal aantal stuks: {a.O1_STUKS}. Totale waarde: {a.O1_SOM:.2f}.')
tabel(doc, ['Artikel', 'Aantal', 'Prijs', 'Waarde'],
      [[code, aantal, f'{prijs:.2f}', f'{w:.2f}']
       for (code, _, aantal, prijs), w in zip(g.O1, a.O1_WAARDEN)])

kop(doc, 'Oefening 2 — Prijslijst', 2)
formuleregel(doc, f'C6:  =AFRONDEN(B6*(1+$B$3);2)   (doorvoeren tot C{g.O2_EIND})')
formuleregel(doc, f'D6:  =C6-B6                     (doorvoeren tot D{g.O2_EIND})')
formuleregel(doc, f'E6:  =D6/B6                     (doorvoeren tot E{g.O2_EIND}, notatie percentage)')
tabel(doc, ['Artikel', 'Huidig', 'Nieuw', 'Verschil', 'In %'],
      [[art, f'{p_:.2f}', f'{n:.2f}', f'{v:.2f}', f'{pr:.2%}']
       for (art, p_), n, v, pr in zip(g.O2, a.O2_NIEUW, a.O2_VERSCHIL, a.O2_PROCENT)])
alinea(doc, 'Hier gaat het het vaakst mis. Wie de dollartekens vergeet, ziet dat pas vanaf '
            'de tweede rij: B3 wordt dan B4, en die cel is leeg. De nieuwe prijs is dan gelijk '
            'aan de oude, en het verschil wordt 0.')
alinea(doc, 'Kolom E is een ingebouwde controle: alle percentages horen rond 3,5 % te liggen. '
            'Eén die eruit springt, wijst rechtstreeks naar de foute rij. Laat ze dat zelf zien.')

kop(doc, 'Oefening 3 — Verkoopcijfers', 2)
formuleregel(doc, f'E4:  =SOM(B4:D4)          (doorvoeren tot E{g.O3_EIND})')
formuleregel(doc, f'B{g.O3_MAANDTOTAAL}: =SOM(B4:B{g.O3_EIND})         (naar rechts doorvoeren tot E{g.O3_MAANDTOTAAL})')
formuleregel(doc, f'B{g.O3_SAMENVATTING}: =MAX(E4:E{g.O3_EIND})')
formuleregel(doc, f'B{g.O3_SAMENVATTING + 1}: =MIN(E4:E{g.O3_EIND})')
formuleregel(doc, f'B{g.O3_SAMENVATTING + 2}: =GEMIDDELDE(E4:E{g.O3_EIND})')
formuleregel(doc, f'B{g.O3_SAMENVATTING + 3}: =AANTAL(E4:E{g.O3_EIND})')
tabel(doc, ['Verkoper', 'Kwartaaltotaal'],
      [[naam, t] for (naam, *_), t in zip(g.O3, a.O3_TOTALEN)])
tabel(doc, ['Maandtotalen', 'Januari', 'Februari', 'Maart', 'Eindtotaal'],
      [[f'rij {g.O3_MAANDTOTAAL}'] + [str(x) for x in a.O3_PER_MAAND] + [str(a.O3_EINDTOTAAL)]],
      stijl='Light List Accent 1')
tabel(doc, ['Samenvatting', 'Antwoord'], [
    ['Hoogste (MAX)', a.O3_MAX],
    ['Laagste (MIN)', a.O3_MIN],
    ['Gemiddelde', f'{a.O3_GEM:.0f}'],
    ['Aantal verkopers', a.O3_AANTAL],
], stijl='Light List Accent 1')
alinea(doc, f'Het eindtotaal {a.O3_EINDTOTAAL} moet langs twee wegen kloppen: als som van de '
            f'acht kwartaaltotalen én als som van de drie maandtotalen. Dat is de controle '
            f'die in stap 3 gevraagd wordt.')

kop(doc, 'Oefening 4 — Bestellingen', 2)
formuleregel(doc, f'D6:  =ALS(C6>=$B$3;"Gratis";"Betalend")      (doorvoeren tot D{g.O4_EIND})')
formuleregel(doc, f'C{g.O4_ANTWOORD}: =AANTAL.ALS(D6:D{g.O4_EIND};"Gratis")')
formuleregel(doc, f'C{g.O4_ANTWOORD + 1}: =AANTAL.ALS(D6:D{g.O4_EIND};"Betalend")')
formuleregel(doc, f'C{g.O4_ANTWOORD + 2}: =SOM.ALS(D6:D{g.O4_EIND};"Gratis";C6:C{g.O4_EIND})')
formuleregel(doc, f'C{g.O4_ANTWOORD + 3}: =SOM.ALS(D6:D{g.O4_EIND};"Betalend";C6:C{g.O4_EIND})')
tabel(doc, ['Bestelnr', 'Bedrag', 'Levering'],
      [[nr, f'{bedrag:.2f}', lev] for (nr, _, bedrag), lev in zip(g.O4, a.O4_LEVERING)])
tabel(doc, ['Vraag', 'Antwoord'], [
    ['Aantal gratis', a.O4_AANTAL_GRATIS],
    ['Aantal betalend', a.O4_AANTAL_BETALEND],
    ['Bedrag gratis', f'{a.O4_SOM_GRATIS:.2f}'],
    ['Bedrag betalend', f'{a.O4_SOM_BETALEND:.2f}'],
    ['Controle: samen', f'{a.O4_SOM_ALLES:.2f}'],
], stijl='Light List Accent 1')
kader(doc, 'Twee bestellingen om klassikaal bij stil te staan', [
    'B-2104 staat op 489,90 — net onder de grens, dus Betalend.',
    'B-2108 staat op 501,00 — net erboven, dus Gratis.',
    'Wie > gebruikt in plaats van >=, ziet geen verschil: bij geen enkele bestelling staat',
    'precies 500. Vraag hen wat er zou gebeuren als er wél een bestelling van 500 was.',
])

kop(doc, 'Oefening 5 — Klantenbestand', 2)
formuleregel(doc, f'B4:  =VERT.ZOEKEN(A4;$G$4:$I${g.O5_TAB_EIND};2;ONWAAR)   (doorvoeren tot B{g.O5_EIND})')
formuleregel(doc, f'C4:  =VERT.ZOEKEN(A4;$G$4:$I${g.O5_TAB_EIND};3;ONWAAR)   (doorvoeren tot C{g.O5_EIND})')
tabel(doc, ['Rij', 'Code', 'Naam', 'Stad'],
      [[g.O5_START + i, code, naam, stad] for i, (code, naam, stad) in enumerate(a.O5_ANTWOORD)])
onbekend_rij = g.O5_START + g.O5_VRAAG.index(g.O5_ONBEKEND)
kader(doc, 'De rij die #N/B geeft', [
    f'Code {g.O5_ONBEKEND} op rij {onbekend_rij} staat niet in de zoektabel. Die geeft #N/B, '
    'en dat hoort zo.',
    '',
    'Dat is bewust ingebouwd. Leerlingen denken bij een foutmelding meestal dat ze zelf iets '
    'verkeerd deden. Hier leren ze het verschil: #N/B betekent dat de waarde niet bestaat, '
    'niet dat hun formule fout is.',
    '',
    'Krijgen ze méér dan één #N/B, dan is er wél iets mis: bijna altijd de dollartekens, '
    'waardoor de zoektabel is meegeschoven.',
])

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
    ['1', f'C{g.O1_TOTAAL} en E{g.O1_TOTAAL}', f'{a.O1_STUKS} stuks en {a.O1_SOM:.2f}'],
    ['2', f'C{g.O2_EIND} en E{g.O2_EIND}', f'{a.O2_NIEUW[-1]:.2f} en {a.O2_PROCENT[-1]:.2%}'],
    ['3', f'E{g.O3_MAANDTOTAAL} en B{g.O3_SAMENVATTING} tot B{g.O3_SAMENVATTING + 3}',
     f'{a.O3_EINDTOTAAL} / {a.O3_MAX} / {a.O3_MIN} / {a.O3_GEM:.0f} / {a.O3_AANTAL}'],
    ['4', f'C{g.O4_ANTWOORD} tot C{g.O4_ANTWOORD + 3}',
     f'{a.O4_AANTAL_GRATIS} / {a.O4_AANTAL_BETALEND} / {a.O4_SOM_GRATIS:.2f} / {a.O4_SOM_BETALEND:.2f}'],
    ['5', f'B{g.O5_EIND} en één rij met #N/B', f'{a.O5_ANTWOORD[-1][1]}, rij {onbekend_rij} geeft #N/B'],
], stijl='Light List Accent 1')
alinea(doc, 'Staat in E13 het juiste totaal, dan kloppen de acht regels erboven ook. '
            'Hetzelfde geldt voor de laatste rij van elke doorgevoerde kolom: die is de '
            'snelste controle, want daar komen de fouten met celverwijzingen bovendrijven.')

doc.save(MAP + 'excel-lerarenuitleg.docx')
print('lerarenuitleg geschreven')
