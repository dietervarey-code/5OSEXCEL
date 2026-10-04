# -*- coding: utf-8 -*-
"""Bouwt het toetsblad voor de leerlingen en de verbetersleutel voor de leerkracht."""
import importlib.util
import os
import re
import sys
from collections import Counter
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

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
ROOD = RGBColor(0xA0, 0x1B, 0x1B)
GRIJS = RGBColor(0x59, 0x59, 0x59)
FORMULE = re.compile(r'(=[A-Z.]*\((?:[^()]|\([^()]*\))*\)|=[A-Z$]+\d+(?:[*+\-/][A-Z$]*\d+)*)')

FORMULEPUNTEN = sum(m['punten'] for oef in o.OEFENINGEN for m in oef['maken'])
OPMAAKPUNTEN = sum(n for oef in o.OEFENINGEN for _, n in oef['opmaak'])
TOTAAL = FORMULEPUNTEN + OPMAAKPUNTEN
MINUTEN = sum(int(oef['duur'].split()[0]) for oef in o.OEFENINGEN)


def punten(oef):
    return (sum(m['punten'] for m in oef['maken']), sum(n for _, n in oef['opmaak']))


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
    p.paragraph_format.space_after = Pt(2)
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


# =====================================================================
#  HET TOETSBLAD
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

kader(doc, 'Wat je gaat doen', [
    'Vijf werkbladen over de Rode Duivels. Op elk blad staat wat er moet uitkomen en met '
    'welke functie. Hoe de formule er precies uitziet, weet je zelf — dat is net wat deze '
    'toets nagaat.',
    '',
    'Bij een paar cellen staat zelfs niet welke functie je nodig hebt. Daar kies je zelf.',
    '',
    'Je gebruikt alleen functies die je kent uit de eerste bundel. Geen enkele formule heeft '
    'een functie binnen een functie nodig, en je hoeft nergens naar een ander blad te '
    'verwijzen.',
])

kader(doc, 'Lees dit eerst', [
    'Sla het bestand meteen op als  toets-jouwnaam.xlsx  en sla tijdens het werken '
    'regelmatig opnieuw op.',
    '',
    g.WAARSCHUWING,
], ROOD)

kop(doc, 'De vijf werkbladen', 2)
tabel(doc, ['Nr', 'Werkblad', 'Wat je doet', 'Duur', 'Punten'],
      [[oef['nr'], oef['blad'], oef['titel'], oef['duur'],
        f'{sum(punten(oef))}'] for oef in o.OEFENINGEN]
      + [['', '', '', f'{MINUTEN} minuten', f'{TOTAAL}']])

kop(doc, 'Spelregels', 2)
for r_ in [
    'Reken nooit iets uit met je rekenmachine om het daarna over te typen. Een ingetypt '
    'getal telt niet mee, ook niet als het juist is.',
    'Typ een formule één keer en voer ze door met de vulgreep.',
    'Controleer na het doorvoeren altijd de laatste rij van je kolom.',
    'Bij elk blad hoort opmaak. Die staat mee op de punten.',
    'Elk blad eindigt met een controle die je zelf kunt doen. Doe ze ook: ze vindt de meeste '
    'fouten voor je.',
    'Raak de tabellen die als "niet aanpassen" aangeduid staan niet aan.',
]:
    doc.add_paragraph(r_, style='List Bullet')

kop(doc, 'Hoe de punten verdeeld zijn', 2)
tabel(doc, ['Werkblad', 'Formules', 'Opmaak', 'Samen'],
      [[oef['blad'], punten(oef)[0], punten(oef)[1], sum(punten(oef))]
       for oef in o.OEFENINGEN]
      + [['Samen', FORMULEPUNTEN, OPMAAKPUNTEN, TOTAAL]],
      stijl='Light List Accent 1')
alinea(doc, 'Bij elke cel hieronder staat hoeveel ze waard is. Kom je tijd tekort, kijk dan '
            'waar de meeste punten liggen.')

# --- per werkblad -----------------------------------------------------
for oef in o.OEFENINGEN:
    paginaeinde(doc)
    kop(doc, f"Werkblad {oef['blad']}", 1)
    p = doc.add_paragraph()
    r = p.add_run(f"Opdracht {oef['nr']} — {oef['titel']}    ·    {oef['duur']}    ·    "
                  f'{sum(punten(oef))} punten')
    r.italic = True
    r.font.color.rgb = GRIJS

    kader(doc, 'Wat je moet bereiken', [oef['doel']])

    kop(doc, 'Wat er al op het blad staat', 2)
    tabel(doc, ['Waar', 'Wat'], [[waar, wat] for waar, wat in oef['gegeven']],
          stijl='Light List Accent 1')

    kop(doc, f'Wat jij moet maken  ({punten(oef)[0]} punten)', 2)
    tabel(doc, ['Waar', 'Wat er moet uitkomen', 'Waarmee', 'Pt'],
          [[m['waar'], m['wat'], m['hoe'], m['punten']] for m in oef['maken']])

    kop(doc, f'Opmaak  ({punten(oef)[1]} punten)', 2)
    for eis, n in oef['opmaak']:
        alinea(doc, f'{eis}  ({n} pt)', style='List Bullet')

    kader(doc, 'Je bent klaar als', [oef['klaar']])
    kader(doc, 'Controleer jezelf', [oef['controle']], ROOD)

doc.save(MAP + 'rodeduivels-toets-opdracht.docx')
print(f'toetsblad geschreven ({TOTAAL} punten, {MINUTEN} minuten)')

# =====================================================================
#  VERBETERSLEUTEL
# =====================================================================
doc = Document()
opzet(doc)
kop(doc, f'{g.TITEL} · verbetersleutel')
alinea(doc, f'Synthesetoets op de basisbundel. Vijf werkbladen, {FORMULEPUNTEN} punten voor '
            f'de formules en {OPMAAKPUNTEN} voor de opmaak, samen {TOTAAL} punten voor '
            f'{MINUTEN} minuten.')

kader(doc, 'Wat je uitdeelt', [
    'rodeduivels-toets-startbestand.xlsx — zes werkbladen, bewust kaal',
    'rodeduivels-toets-opdracht.docx — het toetsblad, één pagina per werkblad',
    '',
    'De functiefiches NIET uitdelen: dit is een toets op wat ze kennen. Wil je er toch '
    f'een vangnet bij, deel dan alleen de inhoudsopgave van {g.BASISBUNDEL} uit, zodat ze '
    'de namen van de tien functies kunnen terugvinden zonder de uitleg.',
], ROOD)

kader(doc, 'Over de cijfers in het bestand', [
    'De spelersnamen zijn echt, de cijfers niet. Leeftijden, caps, doelpunten, uitslagen en '
    'ticketprijzen zijn verzonnen zodat de oefening sluit. Dat staat ook op het startbestand '
    'en op het toetsblad.',
    '',
    'Wil je echte cijfers gebruiken, dan hoef je alleen gegevens.py aan te passen en de drie '
    'bestanden opnieuw te maken: alle antwoorden en alle rijnummers schuiven mee.',
])

kop(doc, 'Tijdsindeling', 2)
tabel(doc, ['Minuten', 'Werkblad', 'Waar je op let'], [
    ['0-4', 'Intro', 'Bestand openen en opslaan onder eigen naam. Spelregels overlopen.'],
    ['4-17', '1 Selectie', 'De dollartekens in de ALS, en >= tegenover >. Zie hieronder.'],
    ['17-28', '2 Wedstrijden', 'Naar rechts doorvoeren. Een gelijkspel is geen overwinning.'],
    ['28-38', '3 Clubdoelpunten', 'Het criterium uit een cel halen. Het lastigste blad.'],
    ['38-46', '4 Tickets', 'De absolute verwijzing naar het percentage.'],
    ['46-54', '5 Wedstrijdblad', 'De zoektabel vastzetten. Haalt niet iedereen af.'],
])
kader(doc, 'Als je tijd tekort komt', [
    'De bladen staan los van elkaar: er is niets van blad 1 nodig op blad 5. Je kunt dus '
    'gerust zeggen dat wie niet rond geraakt, blad 5 laat vallen.',
    '',
    f'Wie tot en met blad 4 geraakt, heeft {TOTAAL - sum(punten(o.OEFENINGEN[4]))} van de '
    f'{TOTAAL} punten kunnen verdienen en negen van de tien functies gebruikt. Alleen '
    'VERT.ZOEKEN komt dan niet aan bod — overweeg om in dat geval op blad 5 te quoteren '
    'op wat er staat in plaats van op het geheel.',
])

kop(doc, 'Welke functie waar aan bod komt', 2)
TELLING = Counter(m['functie'] for oef in o.OEFENINGEN for m in oef['maken'] if m['functie'])
tabel(doc, ['Functie', 'Aantal formules', 'Op welke bladen'],
      [[fn, n, ', '.join(str(oef['nr']) for oef in o.OEFENINGEN
                         if any(m['functie'] == fn for m in oef['maken']))]
       for fn, n in TELLING.most_common()], stijl='Light List Accent 1')
alinea(doc, 'Alle tien de functies van de basisbundel komen aan bod, en alle vijf de '
            'hulpfiches: absolute celverwijzing, getalnotatie, doorvoeren met de vulgreep, '
            'voorwaardelijke opmaak en beeld vastzetten.')

# --- oplossingen ------------------------------------------------------
paginaeinde(doc)
kop(doc, 'Oplossingen')
alinea(doc, 'Een leerling die een andere maar correcte formule schrijft, heeft gelijk: er is '
            'meer dan één weg. Wat niet mag, is een ingetypt getal.')

for oef in o.OEFENINGEN:
    f_pt, o_pt = punten(oef)
    kop(doc, f"Werkblad {oef['blad']}  ({f_pt} + {o_pt} punten)", 2)
    for cel, formule, antwoord, pt, opmerking in sl.SLEUTEL[oef['nr']]:
        formuleregel(doc, f'{cel}: {formule}')
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.4)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(f'→ {antwoord}   ({pt} pt)')
        r.italic = True
        r.font.color.rgb = GRIJS
        if opmerking:
            r2 = p.add_run('   ' + opmerking)
            r2.italic = True
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = GRIJS
    for eis, n in oef['opmaak']:
        p = doc.add_paragraph(style='List Bullet')
        zin(p, f'Opmaak: {eis}  ({n} pt)')

# --- de uitkomsten ----------------------------------------------------
paginaeinde(doc)
kop(doc, 'De uitkomsten om na te kijken')

kop(doc, 'Werkblad 1 — Selectie', 2)
tabel(doc, ['Speler', 'Positie', 'Leeftijd', 'Caps', 'Doelpunten', 'Ervaren?'],
      [[naam, pos, leeftijd, caps, dp, erv]
       for (naam, pos, leeftijd, caps, dp), erv in zip(g.B1, a.B1_ERVAREN)])
kader(doc, 'Eén speler om klassikaal bij stil te staan', [
    f'{a.B1_OP_DE_GRENS[0]} heeft precies {g.B1_ERVAREN} caps, de grens zelf. De '
    'omschrijving zegt "ervaren vanaf", dus hoort hij erbij. Wie > gebruikt in plaats van '
    f'>=, krijgt in B{sl.S1 + 6} een {a.B1_AANTAL_ERVAREN - 1} in plaats van een '
    f'{a.B1_AANTAL_ERVAREN}. Het is de enige rij waar dat verschil zichtbaar wordt.',
    '',
    f'Let ook op het verschil met de voorwaardelijke opmaak: {len(a.B1_BOVEN_GEM)} spelers '
    f'liggen boven het GEMIDDELDE aantal caps ({a.B1_GEM_CAPS:.1f}), maar er zijn er '
    f'{a.B1_AANTAL_ERVAREN} ervaren. Twee verschillende vragen, twee verschillende '
    'antwoorden.',
])

kop(doc, 'Werkblad 2 — Wedstrijden', 2)
tabel(doc, ['Datum', 'Tegenstander', 'Thuis/uit', 'Voor', 'Tegen', 'Saldo', 'Gewonnen?'],
      [[datum, tegenstander, waar, voor, tegen, f'{saldo:+d}', gew]
       for (datum, tegenstander, waar, voor, tegen), saldo, gew
       in zip(g.B2, a.B2_SALDO, a.B2_GEWONNEN)])
alinea(doc, f'Totalen: {a.B2_VOOR} voor, {a.B2_TEGEN} tegen, saldo {a.B2_SALDO_TOTAAL}. '
            f'Dat is meteen de controle die op het toetsblad gevraagd wordt.')
kader(doc, 'Twee gelijke spelen', [
    'Oekraïne en Denemarken eindigden gelijk. Wie in de ALS >= gebruikt in plaats van >, '
    f'rekent die twee als overwinningen mee en komt op {a.B2_AANTAL_GEWONNEN + 2} in plaats '
    f'van {a.B2_AANTAL_GEWONNEN}.',
])

kop(doc, 'Werkblad 3 — Clubdoelpunten', 2)
tabel(doc, ['Positie', 'Aantal spelers', 'Doelpunten'],
      [[positie, aantal, dp] for positie, aantal, dp
       in zip(g.POSITIES, a.B3_AANTAL_PER, a.B3_DOELPUNTEN_PER)]
      + [['Samen', sum(a.B3_AANTAL_PER), a.B3_TOTAAL]])
kader(doc, 'De doelmannen geven 0', [
    'Dat is geen fout en geen foutmelding: SOM.ALS over twee nullen geeft gewoon 0. '
    'Leerlingen die daarvan schrikken en hun formule gaan aanpassen, slopen meestal een '
    'werkende formule. Zeg het vooraf of laat het staan.',
])

kop(doc, 'Werkblad 4 — Tickets', 2)
tabel(doc, ['Vak', 'Normale prijs', 'Korting', 'Abonneeprijs'],
      [[vak, f'{prijs:.2f}', f'{korting:.2f}', f'{abonnee:.2f}']
       for (vak, prijs), korting, abonnee in zip(g.B4, a.B4_KORTING, a.B4_ABONNEE)]
      + [['Totaal', f'{a.B4_SOM_NORMAAL:.2f}', f'{a.B4_SOM_KORTING:.2f}',
          f'{a.B4_SOM_ABONNEE:.2f}']])
# Welke kortingen vallen op een halve cent? Afleiden, niet opschrijven:
# dan blijft deze zin kloppen als een prijs verandert.
from decimal import Decimal                                      # noqa: E402
HALVE_CENT = [(vak, Decimal(str(prijs)) * Decimal(str(g.B4_KORTING)))
              for vak, prijs in g.B4
              if str(Decimal(str(prijs)) * Decimal(str(g.B4_KORTING))).endswith('5')]
_vak, _ruw = HALVE_CENT[0]
alinea(doc, f'{len(HALVE_CENT)} kortingen vallen op een halve cent: '
            + ' en '.join(v for v, _ in HALVE_CENT)
            + f'. AFRONDEN legt ze naar boven: {str(_ruw).replace(".", ",")} wordt '
            + f'{a.B4_KORTING[[v for v, _ in g.B4].index(_vak)]:.2f}'.replace('.', ',')
            + '. Wie geen AFRONDEN gebruikt maar alleen een getalnotatie, ziet hetzelfde '
              'staan maar telt verderop anders op.')

kop(doc, 'Werkblad 5 — Wedstrijdblad', 2)
tabel(doc, ['Rugnummer', 'Speler', 'Positie', 'Minuten'],
      [[nr, speler, positie, minuten] for nr, speler, positie, minuten in a.B5_BASIS]
      + [['', '', 'Totaal', a.B5_MINUTEN]])
alinea(doc, f'{a.B5_AANTAL_TELLEN} verdedigers in de basiself, gemiddeld '
            f'{a.B5_GEM_MINUTEN:.1f} minuten per speler.')

# --- verbeterschema ---------------------------------------------------
paginaeinde(doc)
kop(doc, 'Verbeterschema')
alinea(doc, 'Eén regel per cel. Klopt het getal, dan kloppen de rijen erboven meestal ook — '
            'zeker bij een totaal of een telling.')
for oef in o.OEFENINGEN:
    f_pt, o_pt = punten(oef)
    tabel(doc, [f"Blad {oef['nr']} — {oef['blad']}", 'Antwoord', 'Pt'],
          [[cel, antwoord, pt] for cel, _, antwoord, pt, _ in sl.SLEUTEL[oef['nr']]]
          + [['Opmaak (zie de eisen op het toetsblad)', '', o_pt]]
          + [['Samen', '', f_pt + o_pt]],
          stijl='Light List Accent 1')

kop(doc, 'Wat er het vaakst misgaat', 2)
tabel(doc, ['Wat je ziet', 'Wat eraan scheelt', 'Hoeveel aftrek'], [
    ['######', 'De kolom is te smal.', 'Geen fout. Kolomrand breder slepen.'],
    ['#NAAM?', 'Typfout in de functienaam, of tekst zonder aanhalingstekens.',
     'Formulepunt weg, opmaak blijft tellen.'],
    ['#N/B op blad 5', 'De dollartekens rond de spelerslijst ontbreken.',
     'De eerste rijen kloppen vaak nog: geef dan de helft.'],
    [f'B{sl.S1 + 6} geeft {a.B1_AANTAL_ERVAREN - 1} op blad 1',
     '> gebruikt in plaats van >= in de ALS.',
     'De ALS is fout, de telling erna klopt wel. Eén punt weg.'],
    [f'B{sl.A2} geeft {a.B2_AANTAL_GEWONNEN + 2} op blad 2',
     '>= gebruikt waar > hoort: gelijkspelen meegeteld.', 'Zelfde redenering.'],
    ['Vier keer hetzelfde getal op blad 3', 'Ook het criterium vastgezet ($A$22).',
     'Het bereik staat vast, het criterium niet. Formulepunten weg.'],
    ['Korting gelijk voor elk vak op blad 4', 'B2 niet vastgezet.',
     'Vanaf rij 6 wijst de verwijzing naar een lege cel.'],
    ['Kolomtotaal klopt niet op blad 2 of 4',
     'Naar beneden doorgevoerd in plaats van naar rechts.',
     'De vulgreep kan ook zijwaarts.'],
    ['Een juist getal zonder formule in de cel', 'Uitgerekend en overgetypt.',
     'Geen punten. Dat staat zo in de spelregels.'],
])

kop(doc, 'Advies voor de quotering', 2)
for r_ in [
    f'{FORMULEPUNTEN} punten op de formules en {OPMAAKPUNTEN} op de opmaak. Wie alles juist '
    'berekent maar niets opmaakt, haalt een voldoende maar geen onderscheiding — dat is de '
    'bedoeling.',
    'Klik elke antwoordcel aan en lees de formulebalk. Een getal zonder isgelijkteken is '
    'overgetypt en telt niet mee, hoe juist het ook is.',
    'Een doorgevoerde kolom beoordeel je op de eerste én de laatste rij. Wie alleen de '
    'eerste rij nakijkt, mist precies de fout die het doorvoeren maakt.',
    'Een fout die doorwerkt (een verkeerd saldo dat het totaal meesleept) reken je één keer '
    'aan, niet twee keer.',
]:
    doc.add_paragraph(r_, style='List Bullet')

doc.save(MAP + 'rodeduivels-toets-verbetersleutel.docx')
print('verbetersleutel geschreven')
print(f'functies: {dict(TELLING)}')
