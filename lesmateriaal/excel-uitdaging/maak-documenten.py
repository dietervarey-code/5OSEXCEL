# -*- coding: utf-8 -*-
"""Bouwt de opdrachtbundel en de lerarensleutel van de uitdagingsopdracht."""
import importlib.util
import os
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from schermbeeld import teken                                    # noqa: E402


def laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')
u = laad('u', 'uitleg.py')

MAP = HIER + os.sep
BEELDMAP = os.path.join(HIER, 'beelden')
BLAUW = RGBColor(0x1F, 0x38, 0x64)
ORANJE = RGBColor(0xB0, 0x4A, 0x00)
GRIJS = RGBColor(0x59, 0x59, 0x59)
FORMULE = re.compile(r"(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|='[^']+'![A-Z$]+\d+"
                     r"|=[A-Z$]+\d+(?:[*+\-/][A-Z$]*\d+)*)")


def opzet(doc):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'
    s.font.size = Pt(11)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.6)
        sec.left_margin = sec.right_margin = Cm(2.0)


def kop(doc, tekst, niveau=1, kleur=BLAUW):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs:
        r.font.color.rgb = kleur
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
    r.font.size = Pt(10.5)
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


def beeld(doc, spec, breedte=4.6):
    pad_png = os.path.join(BEELDMAP, spec['bestand'] + '.png')
    teken(pad_png,
          kolommen=spec['kolommen'], rijen=spec['rijen'],
          formule=spec.get('formule') or None,
          geselecteerd=spec.get('geselecteerd'),
          gemarkeerd=spec.get('gemarkeerd', ()),
          rechts=spec.get('rechts', ()),
          vet_rij=spec.get('vet_rij'))
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(pad_png, width=Inches(breedte))
    po = doc.add_paragraph()
    po.paragraph_format.space_after = Pt(10)
    r = po.add_run(spec['onderschrift'])
    r.italic = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = GRIJS
    return pad_png


def uur(t):
    return t.strftime('%H:%M')


def komma(x, n=1):
    """Een getal in lopende tekst: met een komma, zoals het hoort."""
    return f'{x:.{n}f}'.replace('.', ',')


# =====================================================================
#  OPDRACHTBUNDEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, g.TITEL)
p = doc.add_paragraph()
r = p.add_run(f'{g.ONDERTITEL} · uitdagingsopdracht · 40 minuten')
r.italic = True
r.font.color.rgb = GRIJS
doc.add_paragraph('Naam: ..........................................    Klas: ..............    '
                  'Datum: ..............')

kader(doc, 'De situatie', [
    'Je bent coördinator van de Halloweennacht op Kasteel Ravenstein. De laatste bezoekers '
    'zijn buiten, de kaarsen uit. Er zijn twee dingen te doen.',
    '',
    'Eén: de avond afsluiten. Hoeveel volk is er geweest, welke attractie trok het meest, '
    'wat heeft de avond opgebracht en wat heeft ze gekost?',
    '',
    'Twee: er is een probleem. De Zilveren Pompoen, de trofee die elk jaar in de schatkamer '
    'staat, is weg. Ergens tussen tien en elf uur. Vijf mensen hebben iets gezien of '
    'geregistreerd; hun verklaringen staan bij werkblad 4. Met de gegevens in het '
    'startbestand kom je bij precies één naam.',
], ORANJE)

kader(doc, 'Wat dit anders maakt dan de vorige bundels', [
    'Hier staat NIET welke formule je moet typen. Er staat wat er moet uitkomen, en met '
    'welke functie. Hoe je ze in elkaar zet, zoek je zelf uit.',
    '',
    'Geneste functies mogen, en op sommige plaatsen moet het zelfs. Nieuwe functies ook: '
    'achteraan het hoofdstuk Nieuw gereedschap staat per functie een kaart met uitleg, '
    'voorbeelden en een schermbeeld. De voorbeelden daar gaan niet over deze opdracht.',
    '',
    'De tien functies van de basisbundel veronderstellen we gekend. Loop je daarop vast, '
    'pak dan je oude functiefiches erbij.',
])

kop(doc, 'De vijf werkbladen', 2)
tabel(doc, ['Nr', 'Werkblad', 'Wat je doet', 'Duur'],
      [[oef['nr'], oef['blad'], oef['titel'], oef['duur']] for oef in o.OEFENINGEN])
alinea(doc, 'De bladen hangen aan elkaar: werkblad 4 heeft de einduren van werkblad 3 nodig, '
            'en werkblad 5 haalt cijfers van werkblad 1 én 3. Werk ze dus in volgorde af.')

kop(doc, 'Spelregels', 2)
for r_ in [
    'Geen enkel getal overtypen. Staat een cijfer al ergens, dan verwijs je ernaar — ook '
    'over de bladen heen.',
    'Geen rekenmachine. Komt er iets niet uit, dan is de formule het probleem.',
    'Bouw een geneste formule in stappen op: eerst de binnenste functie in een lege cel, '
    'kijken of die klopt, dan naar binnen schuiven.',
    'Elk blad eindigt met een controle die je zelf kunt doen. Doe ze, vooral op werkblad 4: '
    'daar is de controle je bewijs.',
    'Bij elke opdracht hoort opmaak. Een blad dat klopt maar er slordig uitziet, is niet af.',
]:
    doc.add_paragraph(r_, style='List Bullet')

kop(doc, 'Waarop je beoordeeld wordt', 2)
tabel(doc, ['Wat', 'Punten'], [
    ['De formules kloppen en verwijzen naar cellen, nergens een overgetypt getal', '10'],
    ['De juiste functie op de juiste plaats, ook de nieuwe', '6'],
    ['De dader is gevonden, met de formule als bewijs en niet met het oog', '4'],
    ['Opmaak: getalnotatie, tijdnotatie, koptekst, randen en voorwaardelijke opmaak', '5'],
], stijl='Light List Accent 1')

# --- nieuw gereedschap ------------------------------------------------
paginaeinde(doc)
kop(doc, 'Nieuw gereedschap')
alinea(doc, 'Tien kaarten. Lees er niet tien achter elkaar: de opdracht zegt bij elk '
            'werkblad welke je nodig hebt. Pak die kaart erbij op het moment dat je ze '
            'nodig hebt.')
alinea(doc, 'De voorbeelden op deze kaarten gaan NIET over deze opdracht. Ze spelen in een '
            'eigen wereldje — een rapport, een fruithandel, een uurrooster — met andere '
            'cellen en andere cijfers. Je leert er de functie kennen en past ze daarna zelf '
            'toe op je eigen gegevens.')
tabel(doc, ['Kaart', 'Nodig op werkblad'],
      [[k['naam'], ', '.join(str(oef['nr']) for oef in o.OEFENINGEN
                             if k['naam'] in oef['kaarten']) or '—']
       for k in u.KAARTEN], stijl='Light List Accent 1')

for d in u.KAARTEN:
    paginaeinde(doc)
    p = doc.add_paragraph()
    r = p.add_run('NIEUW GEREEDSCHAP')
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

    for spec in d.get('beelden', []):
        beeld(doc, spec)

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

# --- per werkblad -----------------------------------------------------
for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Werkblad {oef['blad']}", 1)
    p = doc.add_paragraph()
    r = p.add_run(f"Opdracht {oef['nr']} — {oef['titel']}    ·    {oef['duur']}")
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'Wat je moet bereiken', [oef['doel']])

    if oef.get('verklaringen'):
        kop(doc, 'De vijf verklaringen', 2)
        alinea(doc, 'Elke verklaring is één voorwaarde. Samen laten ze precies één naam '
                    'overeind. Zet ze om in één formule — niet vijf losse kolommen.')
        tabel(doc, ['Wie', 'Wat die zegt'],
              [[wie, wat] for wie, wat in oef['verklaringen']])

    kop(doc, 'Wat er al op het blad staat', 2)
    tabel(doc, ['Waar', 'Wat'], [[waar, wat] for waar, wat in oef['gegeven']],
          stijl='Light List Accent 1')

    kop(doc, 'Wat jij moet maken', 2)
    tabel(doc, ['Waar', 'Wat er moet uitkomen', 'Waarmee'],
          [[waar, wat, hoe] for waar, wat, hoe in oef['maken']])

    kop(doc, 'Opmaak', 2)
    for regel in oef['opmaak']:
        alinea(doc, regel, style='List Bullet')

    kop(doc, 'Hints', 2)
    alinea(doc, 'Lees ze pas als je vastloopt. Ze geven de formule niet, ze geven de richting.')
    for regel in oef['hints']:
        alinea(doc, regel, style='List Bullet')

    kader(doc, 'Kaarten die je hier nodig hebt', [' · '.join(oef['kaarten'])])
    kader(doc, 'Je bent klaar als', [oef['klaar']])
    kader(doc, 'Controleer jezelf', [oef['controle']], ORANJE)

doc.save(MAP + 'halloween-opdracht.docx')
print(f'opdrachtbundel geschreven ({len(u.KAARTEN)} kaarten, '
      f'{sum(len(k.get("beelden", [])) for k in u.KAARTEN)} schermbeelden)')

# =====================================================================
#  LERARENSLEUTEL
# =====================================================================
sl = laad('sl', 'sleutel.py')
E, A1, T = sl.E, sl.A1, sl.T
P, S, V, R = sl.P, sl.S, sl.V, sl.R
SLEUTEL = sl.SLEUTEL

doc = Document()
opzet(doc)
kop(doc, f'{g.TITEL} · lerarensleutel')
alinea(doc, 'Uitdagingsopdracht voor leerlingen die de basisbundel en de herhaling vlot '
            'afwerken. Vijf werkbladen, 36 formules, 40 minuten. Nieuwe functies, geneste '
            'formules en verwijzingen over de bladen heen.')

kader(doc, 'Wat je uitdeelt', [
    'halloween-startbestand.xlsx — zes werkbladen, bewust kaal',
    'halloween-opdracht.docx — de situatie, tien kaarten Nieuw gereedschap, en één '
    'pagina per werkblad',
    '',
    'De functiefiches van de basisbundel hoeven er niet bij, maar laat ze wel beschikbaar: '
    'de tien basisfuncties worden hier als gekend beschouwd.',
], ORANJE)

kader(doc, 'Voor wie dit is, en voor wie niet', [
    'Dit is geen zwaardere versie van de herhaling. Het is een ander soort opdracht: er '
    'staat nergens welke formule ze moeten typen, alleen wat er moet uitkomen.',
    '',
    'Leerlingen die de basisbundel nog niet vlot afwerken, lopen hier vast op werkblad 1 en '
    'komen niet verder. Voor hen is er de herhalingsbundel.',
    '',
    'Wie het wél aankan, heeft 40 minuten geen vraag nodig. Reken erop dat ze zelf de '
    'kaarten erbij pakken; dat is precies waarvoor ze er zijn.',
])

kop(doc, 'Tijdsindeling', 2)
tabel(doc, ['Minuten', 'Werkblad', 'Waar je op let'], [
    ['0-3', 'Intro', 'Verhaal voorlezen. De Zilveren Pompoen is weg. Daarna zelf aan de slag.'],
    ['3-15', '1 Boekingen', 'Benaderend zoeken, en de volgorde van SOMMEN.ALS. Hier gaat de '
                            'meeste tijd in.'],
    ['15-22', '2 Attracties', 'INDEX met VERGELIJKEN, ook zijwaarts. Het eerste echte '
                              'denkwerk.'],
    ['22-30', '3 Ploegen', 'Tijden maal 24, en een ALS met vijf... nee, twee voorwaarden.'],
    ['30-37', '4 Verdachten', 'De ontknoping. Hier willen ze naartoe.'],
    ['37-40', '5 Afrekening', 'Mechanisch werk, maar de controle is de beste van de bundel.'],
])

kader(doc, 'Als je tijd tekort komt', [
    'De ruggengraat is 1 → 3 → 4. Werkblad 4 heeft alleen werkblad 3 nodig, en werkblad 4 '
    'is de ontknoping: laat dat nooit vallen.',
    '',
    'Werkblad 2 staat helemaal los: dat kan weg of huiswerk worden. Werkblad 5 heeft '
    'werkblad 1 en 3 nodig en is mechanisch — als finale leuk, als huiswerk even goed.',
    '',
    'Wie vroeg klaar is: laat hen op werkblad 4 één verklaring veranderen (een andere kleur '
    'in B3, of een ander uur in B2) en kijken wie er dan overblijft. Dat is de beste test of '
    'ze echt naar de cellen verwezen hebben in plaats van de waarden in te typen.',
])

# --- de ontknoping -----------------------------------------------------
paginaeinde(doc)
kop(doc, 'De ontknoping')
kader(doc, f'De dader is {a.B4_DADER}', [
    f'{a.B4_DADER}, gids in het doolhof. Haar dienst liep van 19:30 tot 23:00, ze badgde '
    'één keer aan de schatkamer tussen tien en elf, ze droeg zwart, ze had een tas bij, en '
    'niemand bevestigde haar alibi.',
    '',
    'Van de acht verdachten valt iedereen af op minstens één verklaring. De tabel hieronder '
    'geeft per naam de reden. Precies één naam blijft over, en de formule in '
    f'B{g.B4_ANTWOORD} bewijst dat: daar moet 1 staan.',
], ORANJE)

tabel(doc, ['Verdachte', 'Oordeel', 'Waarom die afvalt'],
      [[naam, oordeel, '; '.join(redenen) if redenen
        else 'alle vijf de verklaringen passen'] for naam, oordeel, redenen in a.B4_REDEN])

kader(doc, 'De val die er met opzet in zit', [
    'Op werkblad 3 maken ze een kolom Nachtploeg. Die kolom vraagt twee dingen: later '
    f'gestopt dan {uur(g.B3_GRENS_TIJD)} én minstens {g.B3_GRENS_UREN} uur gewerkt.',
    '',
    f'{a.B4_DADER} haalt dat tweede niet: ze werkte '
    f'{komma(a.B3_UREN[[n for n, *_ in g.B3].index(a.B4_DADER)])} uur. '
    'Ze staat dus NIET in de nachtploeg — en toch is zij het.',
    '',
    'Wie de nachtploeglijst als verdachtenlijst gebruikt, sluit net de dader uit en '
    'houdt niemand over. '
    'De eerste verklaring gaat over het EINDE van de dienst, niet over de lengte. Dat is '
    'het verschil tussen lezen en snellezen.',
])

# --- oplossingen -------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Alle formules')
alinea(doc, 'Per werkblad de formule en wat ze oplevert. Een leerling die een andere maar '
            'correcte formule schrijft, heeft gelijk: er is meer dan één weg. Wat niet mag, '
            'is een ingetypt getal.')

for oef in o.OEFENINGEN:
    kop(doc, f"Werkblad {oef['blad']}", 2)
    for cel, formule, uitkomst in SLEUTEL[oef['nr']]:
        formuleregel(doc, f'{cel}: {formule}')
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.4)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run('→ ' + uitkomst)
        r.italic = True
        r.font.color.rgb = GRIJS

# --- de uitkomsten in tabelvorm ---------------------------------------
paginaeinde(doc)
kop(doc, 'De uitkomsten om na te kijken')

kop(doc, 'Werkblad 1 — Boekingen', 2)
tabel(doc, ['Boeking', 'Groep', 'Personen', 'Prijs p.p.', 'Bedrag'],
      [[nr, groep, personen, f'{prijs:.2f}', f'{bedrag:.2f}']
       for (nr, groep, personen, _, _), prijs, bedrag
       in zip(g.B1, a.B1_PRIJS, a.B1_BEDRAG)])
alinea(doc, 'Alle vier de schijven van de staffel komen voor. Zie je in kolom F maar drie '
            'verschillende prijzen, dan zit er een fout in het benaderend zoeken.')

kop(doc, 'Werkblad 2 — Attracties', 2)
tabel(doc, ['Attractie'] + g.B2_UREN + ['Totaal'],
      [[naam] + waarden + [totaal]
       for (naam, waarden), totaal in zip(g.B2, a.B2_RIJTOTAAL)])
alinea(doc, 'Per uurblok: ' + ' · '.join(f'{uurblok} = {totaal}' for uurblok, totaal
                                         in zip(g.B2_UREN, a.B2_UURTOTAAL)) +
            f'. Alles samen {a.B2_ALLES}.')

kop(doc, 'Werkblad 3 — Ploegen', 2)
tabel(doc, ['Medewerker', 'Rol', 'Post', 'Van', 'Tot', 'Uren', 'Nachtploeg?'],
      [[naam, rol, post, uur(start), uur(einde), f'{uren:.2f}', nacht]
       for (naam, rol, post, start, einde), uren, nacht
       in zip(g.B3, a.B3_UREN, a.B3_NACHT)])
# Wie zit er precies op de twee grenzen? Dat leiden we af, zodat deze uitleg
# blijft kloppen als de gegevens veranderen.
OP_TIJDSGRENS = [naam for (naam, _, _, _, einde) in g.B3 if einde == g.B3_GRENS_TIJD]
OP_URENGRENS = [naam for (naam, *_), uren in zip(g.B3, a.B3_UREN)
                if uren == g.B3_GRENS_UREN]
TE_VEEL = sum(1 for naam, uren in zip([n for n, *_ in g.B3], a.B3_UREN)
              if naam in OP_TIJDSGRENS and uren >= g.B3_GRENS_UREN)
kader(doc, 'De twee grensgevallen', [
    f'{" en ".join(OP_TIJDSGRENS)} stoppen om precies {uur(g.B3_GRENS_TIJD)}, de grens '
    'zelf. De omschrijving zegt LATER dan die grens, dus horen ze er niet bij. Wie >= '
    f'gebruikt in plaats van >, krijgt er {TE_VEEL} te veel: '
    f'{a.B3_AANTAL_NACHT + TE_VEEL} in plaats van {a.B3_AANTAL_NACHT}.',
    '',
    f'{" en ".join(OP_URENGRENS)} werkt precies {g.B3_GRENS_UREN} uur, maar stopt om '
    f'{uur([e for n, _, _, _, e in g.B3 if n in OP_URENGRENS][0])}. De urenvoorwaarde '
    'haalt hij wél, de tijdvoorwaarde niet. Hij toont dus waarom het EN moet zijn en '
    'geen OF: met OF zou hij er wél in zitten.',
])

kop(doc, 'Werkblad 5 — Afrekening', 2)
tabel(doc, ['Regel', 'Bedrag'], [
    ['Ticketomzet', f'{a.B5_TICKETS:.2f}'],
    ['Baromzet', f'{g.B5_BAROMZET:.2f}'],
    ['Totale opbrengst', f'{a.B5_OPBRENGST:.2f}'],
    [f'Loonkost ({a.B5_UREN} u × {g.B5_UURLOON:.2f})', f'{a.B5_LOONKOST:.2f}'],
    ['Decor en techniek', f'{g.B5_DECOR:.2f}'],
    ['Catering', f'{g.B5_CATERING:.2f}'],
    ['Totale kosten', f'{a.B5_KOSTEN:.2f}'],
    ['Winst', f'{a.B5_WINST:.2f}'],
    ['Winstmarge', f'{a.B5_MARGE:.2%}'],
    ['Opbrengst per bezoeker', f'{a.B5_PER_BEZOEKER:.2f}'],
], stijl='Light List Accent 1')

# --- fouten ------------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Wat er het vaakst misgaat')
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Wat je zegt'], [
    ['Kolom F op blad 1 geeft drie keer dezelfde prijs',
     'De staffel niet vastgezet met dollartekens.',
     'Laat F23 aanklikken: waar wijst de tabel naar?'],
    ['#N/B in kolom F op blad 1',
     'De staffel begint niet bij het laagste mogelijke getal, of ONWAAR gebruikt.',
     'Benaderend zoeken wil WAAR, en een eerste drempel die laag genoeg ligt.'],
    ['0 of een onzinnig getal bij SOMMEN.ALS',
     'De volgorde van SOM.ALS gebruikt: het optelbereik hoort vooraan.',
     'Twee van de drie .ALS-functies beginnen met het bereik, SOMMEN.ALS niet.'],
    ['Kolom F op blad 3 geeft 0,19 in plaats van 4,50',
     'De *24 vergeten.',
     'Geen fout: dat is 4,5 uur uitgedrukt in dagen.'],
    ['Kolom F op blad 3 geeft iets als 04:30',
     'De cel heeft de notatie Tijd in plaats van Getal.',
     'Notatie, niet de formule.'],
    ['Nachtploeg geeft vijf in plaats van vier',
     '>= gebruikt waar de omschrijving LATER DAN zegt.',
     'Kijk naar wie precies op de grens stopt.'],
    ['Kolom F op blad 4 geeft 0,958333',
     'De notatie uu:mm ontbreekt.',
     'De formule is juist. Geef de cel de tijdnotatie.'],
    ['#VERW! op blad 4 of 5',
     'De bladnaam handmatig getypt, zonder de enkele aanhalingstekens.',
     'Een bladnaam met een spatie of cijfer hoort tussen enkele aanhalingstekens.'],
    [f'B{g.B4_ANTWOORD} geeft 0 op blad 4',
     'Eén voorwaarde te streng, meestal >= waar > hoort of omgekeerd.',
     'Haal er één voorwaarde af en kijk welke knelt.'],
    [f'B{g.B4_ANTWOORD} geeft 2 of meer op blad 4',
     'Een verklaring nog niet gebruikt.',
     'Vijf verklaringen, vijf voorwaarden. Tel ze na in je EN.'],
    ['De naam naast de hoogste waarde is net de verkeerde',
     'De twee bereiken van INDEX en VERGELIJKEN beginnen niet op dezelfde rij.',
     'Even lang, zelfde beginrij. Dat is de hele regel.'],
    ['Blad 5 verandert niet mee als je blad 3 aanpast',
     'Een getal overgetypt in plaats van verwezen.',
     'Dat is precies wat de controle van blad 5 moet aantonen.'],
])

kop(doc, 'Verbetersleutel in het kort', 2)
tabel(doc, ['Blad', 'Controleer', 'Antwoord'], [
    ['1', f'C{A1} tot C{A1 + 6}',
     f'{a.B1_BEZOEKERS} / {a.B1_OMZET:.2f} / {a.B1_OMZET_ONLINE_GROOT:.2f} / '
     f'{a.B1_KASSA_KLEIN} / {a.B1_GEM_ONLINE} / {a.B1_GROOTSTE} / {a.B1_GROOTSTE_NAAM}'],
    ['2', f'G{g.B2_TOTAALRIJ} en B{g.B2_ANTWOORD} tot B{g.B2_ANTWOORD + 3}',
     f'{a.B2_ALLES} / {a.B2_DRUKSTE_NAAM} / {a.B2_DRUKSTE_UUR} / {a.B2_TWEEDE_NAAM} / '
     f'{a.B2_AANDEEL:.2%}'],
    ['3', f'B{S} tot B{S + 6}',
     f'{a.B3_AANTAL_ROL} / {a.B3_AANTAL_NACHT} / {a.B3_KRUIS} / {a.B3_TOTAAL_UREN} / '
     f'{a.B3_GEM_ROL} / {a.B3_LANGSTE} / {a.B3_LANGSTE_NAAM}'],
    ['4', f'B{g.B4_ANTWOORD} en B{g.B4_ANTWOORD + 1}',
     f'{a.B4_AANTAL_OVER} / {a.B4_DADER}'],
    ['5', f'B{R["winst"]} tot B{R["per_bezoeker"]}',
     f'{a.B5_WINST:.2f} / {a.B5_MARGE:.2%} / {a.B5_PER_BEZOEKER:.2f}'],
], stijl='Light List Accent 1')
alinea(doc, f'Twee cellen dekken bijna alles af. Staat er in B{g.B4_ANTWOORD} van blad 4 een '
            f'1 en in B{R["winst"]} van blad 5 {a.B5_WINST:.2f}, dan klopt vrijwel zeker '
            'alles wat eronder ligt: beide hangen af van bijna elk ander blad. Dat is je '
            'snelste verbetering.')

doc.save(MAP + 'halloween-lerarensleutel.docx')
print('lerarensleutel geschreven')
print(f'dader: {a.B4_DADER} · winst: {a.B5_WINST:.2f} · '
      f'{sum(len(SLEUTEL[k]) for k in SLEUTEL)} formules in de sleutel')
