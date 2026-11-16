# -*- coding: utf-8 -*-
"""Bouwt de vijf documenten van de tweede samenvoegbundel.

  samenvoegen-opmaak-opdracht.docx          de vijf stappen
  samenvoegen-opmaak-theorie.docx           fiche 14 tot 21
  samenvoegen-opmaak-lerarensleutel.docx    alles uitgeschreven
  samenvoegen-opmaak-brief-leden.docx       de brief, met markers en zonder
                                            opmaak - die is hun werk
  samenvoegen-opmaak-brief-tornooi.docx     de eindopdracht, zonder markers

De twee briefmodellen zijn met opzet lelijk: alles links, een lettergrootte,
geen tabel, geen voettekst. De opmaak is de oefening.
"""
import importlib.util
import os
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')
f = laad('f', 'fiches.py')

OPDRACHT = os.path.join(HIER, 'samenvoegen-opmaak-opdracht.docx')
THEORIE = os.path.join(HIER, o.THEORIEBUNDEL)
SLEUTEL = os.path.join(HIER, 'samenvoegen-opmaak-lerarensleutel.docx')
BRIEF_LEDEN = os.path.join(HIER, g.BRIEF_LEDEN)
BRIEF_TORNOOI = os.path.join(HIER, g.BRIEF_TORNOOI)
ANTW_KOLOM = chr(64 + len(a.ANTW_KOP))   # de kolom waarin ze antwoorden

BLAUW = RGBColor(0x1F, 0x38, 0x64)
ORANJE = RGBColor(0xB0, 0x4A, 0x00)
GRIJS = RGBColor(0x59, 0x59, 0x59)
GROEN = RGBColor(0x38, 0x76, 0x1D)

FORMULE = re.compile(r'(=[A-Z][A-Z.]*\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)'
                     r'(?:&(?:"[^"]*"|[A-Z]+\d+))*'
                     r'|=[A-Z]+\d+(?:&(?:"[^"]*"|[A-Z]+\d+))+)')


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
    """Formules in een vaste letter, zodat ze opvallen in lopende tekst."""
    for stuk in FORMULE.split(str(tekst)):
        if not stuk:
            continue
        r = p.add_run(stuk)
        if FORMULE.fullmatch(stuk):
            r.font.name = 'Consolas'
            r.font.size = Pt(10)
    return p


def vast(p, tekst):
    """Een heel stuk in de vaste letter, voor formules en voorbeelden."""
    r = p.add_run(str(tekst))
    r.font.name = 'Consolas'
    r.font.size = Pt(10)
    return r


def alinea(doc, tekst, vetgedrukt=False, schuin=False, kleur=None,
           grootte=None, na=None):
    p = doc.add_paragraph()
    if vetgedrukt or schuin or kleur or grootte:
        r = p.add_run(str(tekst))
        r.bold, r.italic = vetgedrukt, schuin
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


def tabel(doc, koppen, rijen, stijl='Light Grid Accent 1', breedtes=None,
          vaste_kolommen=()):
    t = doc.add_table(rows=1, cols=len(koppen))
    t.style = stijl
    for i, k in enumerate(koppen):
        t.rows[0].cells[i].paragraphs[0].add_run(str(k)).bold = True
    for rij in rijen:
        cellen = t.add_row().cells
        for i, w in enumerate(rij):
            if i in vaste_kolommen:
                vast(cellen[i].paragraphs[0], w)
            else:
                zin(cellen[i].paragraphs[0], w)
    if breedtes:
        for rij in t.rows:
            for i, b in enumerate(breedtes):
                rij.cells[i].width = Cm(b)
    doc.add_paragraph()
    return t


def paginaeinde(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def veld(alinea, code):
    """Een Word-veld, bijvoorbeeld PAGE. Word vult het zelf in bij het openen."""
    r = alinea.add_run()
    begin = OxmlElement('w:fldChar')
    begin.set(qn('w:fldCharType'), 'begin')
    instructie = OxmlElement('w:instrText')
    instructie.set(qn('xml:space'), 'preserve')
    instructie.text = f' {code} '
    einde = OxmlElement('w:fldChar')
    einde.set(qn('w:fldCharType'), 'end')
    for stuk in (begin, instructie, einde):
        r._r.append(stuk)
    return r


def paginanummers(doc, titel):
    """Onderaan elke pagina: waar je bent, en in welk boekje."""
    for sec in doc.sections:
        p = sec.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(titel + '    ·    blz. ')
        r.font.size = Pt(9)
        r.font.color.rgb = GRIJS
        veld(p, 'PAGE').font.size = Pt(9)
        r = p.add_run(' van ')
        r.font.size = Pt(9)
        r.font.color.rgb = GRIJS
        veld(p, 'NUMPAGES').font.size = Pt(9)
        for run in p.runs:
            run.font.color.rgb = GRIJS
            run.font.size = Pt(9)


def fiche_index(doc, waar):
    """Het lijstje waarmee je een fiche in het theorieboekje terugvindt."""
    alinea(doc, waar, vetgedrukt=True, na=6)
    rijen = []
    for deel in f.DELEN:
        stukken = [f"{f.nummer(i)} {kaart['naam']}"
                   for i, kaart in enumerate(f.FICHES)
                   if kaart['deel'] == deel]
        rijen.append([deel, '   ·   '.join(stukken)])
    tabel(doc, ['Deel', 'Fiches'], rijen, breedtes=[5.6, 10.8])


def punten_tabel(doc):
    tabel(doc, ['Stap', 'Wat je maakt', 'Soort', 'Uren', 'Fiches', 'Pt'],
          [[stap['nr'], stap['titel'], stap['soort'], stap['lesuren'],
            ', '.join(str(n) for n in stap['fiches']), o.punten_van(stap)]
           for stap in o.STAPPEN]
          + [['', 'Samen', '', o.LESUREN, '', o.TOTAAL]],
          breedtes=[1.3, 5.3, 3.0, 1.6, 3.0, 1.2])


def marker_run(alinea_of_cel, tekst):
    """Een [[marker]] valt op, zodat niemand hem over het hoofd ziet."""
    r = alinea_of_cel.add_run(tekst)
    r.bold = True
    r.font.color.rgb = ORANJE
    return r


def briefregel(doc, tekst, na=2, markers=True, vetgedrukt=False):
    """Eén regel van een briefmodel, met de markers in het oranje."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(na)
    stukken = re.split(r'(\[\[[^\]]+\]\])', tekst) if markers else [tekst]
    for stuk in stukken:
        if not stuk:
            continue
        if markers and stuk.startswith('[['):
            marker_run(p, stuk)
        else:
            r = p.add_run(stuk)
            r.bold = vetgedrukt
    return p


def punten_van(stap):
    return o.punten_van(stap)


def fiche_uit(doc, nummer, kaart):
    """Eén fiche: wat het is, hoe je het schrijft, en de fout die iedereen maakt."""
    kop(doc, f"Fiche {nummer} — {kaart['naam']}", 2)
    alinea(doc, kaart['wat'], schuin=True, kleur=GRIJS, na=6)

    if kaart.get('schrijf'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        p.paragraph_format.space_after = Pt(6)
        vast(p, kaart['schrijf']).bold = True
        if kaart.get('argumenten'):
            tabel(doc, ['Stuk', 'Wat het is'],
                  [[stuk, uitleg] for stuk, uitleg in kaart['argumenten']],
                  'Light List Accent 1', [4.0, 12.0], vaste_kolommen={0})

    if kaart.get('stappen'):
        for i, stap in enumerate(kaart['stappen'], 1):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(f'{i}.  ')
            r.bold = True
            r.font.color.rgb = BLAUW
            zin(p, stap)
        doc.add_paragraph().paragraph_format.space_after = Pt(0)

    for regel in kaart.get('uitleg', ()):
        alinea(doc, regel, na=4)

    if kaart.get('voorbeeld'):
        v = kaart['voorbeeld']
        breed = {2: [5.4, 10.6], 3: [3.6, 5.6, 6.8]}[len(v['koppen'])]
        # alleen bij een formulefiche hoort de vaste letter: in een
        # menufiche staat er gewone tekst in de kolommen
        vast_k = set(range(len(v['koppen']))) if kaart.get('schrijf') else set()
        tabel(doc, v['koppen'], v['rijen'], 'Light List Accent 1', breed,
              vaste_kolommen=vast_k)

    if kaart.get('weten'):
        kader(doc, 'Goed om te weten', kaart['weten'], BLAUW)
    kader(doc, 'De fout die iedereen één keer maakt', [kaart['fout']], ORANJE)



# ==========================================================================
#  1. de opdrachtbundel
# ==========================================================================
def voorbeeldblok(doc, stap):
    """Zo hoort het eruit te zien: met echte gegevens uit de lijst."""
    nr = stap['nr']
    if nr == 1:
        kop(doc, f'Zo ziet de kaart van {a.VOORBEELD.naam} eruit', 2, GRIJS)
        tabel(doc, ['Regel', 'Wat erop komt', 'Opmaak'],
              [[i, tekst,
                ', '.join(filter(None, [
                    f"{regel['grootte']} pt",
                    'vet' if regel['vet'] else '',
                    'cursief' if regel['cursief'] else '',
                    '' if regel['kleur'] == 'zwart' else regel['kleur'],
                    g.LIDKAART_UITLIJNING]))]
               for i, (regel, tekst) in enumerate(
                   zip(g.LIDKAART, a.KAART_VOORBEELD), 1)],
              'Light List Accent 1', [1.4, 8.0, 6.6])
    elif nr == 2:
        kop(doc, f'Zo ziet de envelop van {a.ENVELOP_VOORBEELD_LID.naam} '
                 'eruit', 2, GRIJS)
        tabel(doc, ['Waar', 'Wat erop komt'],
              [['linksboven, ' + str(g.ENVELOP_AFZENDER_GROOTTE) + ' pt',
                '  ·  '.join(g.ENVELOP_AFZENDER)],
               ['rechtsonder, ' + str(g.ENVELOP_GEADRESSEERDE_GROOTTE) + ' pt',
                '  ·  '.join(a.ENVELOP_VOORBEELD)]],
              'Light List Accent 1', [4.6, 11.4])
    elif nr == 3:
        kop(doc, 'De tabel: wat links staat en wat rechts', 2, GRIJS)
        tabel(doc, ['Links (typ je zelf)', 'Rechts',
                    f'Bij {a.VOORBEELD.naam} staat er'],
              [[opschrift,
                f'«{veld}»' if veld else 'vaste tekst: ' + g.CLUB_REKENING,
                waarde]
               for (opschrift, veld), (_o, waarde)
               in zip(g.BRIEF_TABEL, a.TABEL_VOORBEELD)],
              'Light List Accent 1', [4.2, 5.8, 6.0])
    elif nr == 4:
        kop(doc, f'Zo zou de lijst van {a.VOORBEELD_LIJST_PLOEG} eruitzien',
            2, GRIJS)
        tabel(doc, g.LIJST_KOLOMMEN, a.VOORBEELD_LIJST_RIJEN,
              'Light List Accent 1')
        alinea(doc, f'Let op: dit is {a.VOORBEELD_LIJST_PLOEG}, als '
                    f'voorbeeld. Jij maakt de lijst van '
                    f'{g.LIJST_BLAD_PLOEG}, die er anders uitziet. De koprij '
                    'hierboven staat er ÉÉN keer, boven alle regels samen. '
                    'In je hoofddocument staat alleen de ene tabelrij met de '
                    f'{len(g.LIJST_KOLOMMEN)} velden.',
               schuin=True, kleur=GRIJS, na=10)


doc = Document()
opzet(doc)
kop(doc, g.TITEL, 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=4)
alinea(doc, 'Naam: ......................................    Klas: ..........',
       na=14)

alinea(doc,
       f'{g.LESUREN} lesuren, vijf stappen, allemaal in Word. Je maakt vier '
       'van de vijf soorten samenvoegdocumenten die Word kent: etiketten, '
       'enveloppen, brieven en een lijst. En bij elk van de vier maak je het '
       'ook op.', na=8)
alinea(doc,
       f'In het Excelbestand hoef je NIETS uit te rekenen. De drie lijsten '
       'staan helemaal klaar — dat is met opzet, zodat elke minuut naar Word '
       f'gaat. Van de {o.TOTAAL} punten staan er {o.PUNTEN_OPMAAK} op de '
       'opmaak alleen.', na=8)
alinea(doc,
       f'De theorie staat in twee boekjes. {o.THEORIEBUNDEL} is nieuw en '
       f'begint bij fiche {f.FICHE_START}. Het boekje van de vorige lessen, '
       f'{g.VOORGANGER_THEORIE}, heb je ook nodig: daar staan de fiches 1 tot '
       f'{f.FICHES_EERSTE_BOEKJE}, en die blijven gelden.', na=12)

punten_tabel(doc)
fiche_index(doc, f'De nieuwe fiches, in {o.THEORIEBUNDEL}:')

kader(doc, 'Vier regels die altijd gelden', [
    '1.  Zet het Excelbestand en je Worddocumenten in DEZELFDE map, en laat ze '
    'daar staan. Word onthoudt waar je lijst staat; verplaats of hernoem je ze, '
    'dan vindt hij ze niet meer.',
    '2.  Werk nooit in het model dat je krijgt. Bestand, Opslaan als, met je '
    'eigen naam in de bestandsnaam.',
    '3.  Beoordeel opmaak NOOIT in de gewone weergave. Beeld, Afdrukweergave, '
    'en zet de zoom op één volledige pagina. De helft van alles wat misgaat, '
    'zie je anders niet.',
    '4.  Maak altijd het HOOFDdocument op, nooit het samengevoegde resultaat. '
    'Het resultaat erft alles; wat je daar aanpast, ben je kwijt zodra je '
    'opnieuw samenvoegt.',
], ORANJE)

kader(doc, 'Twee kolommen staan er twee keer', [
    f'In het werkblad {g.LEDEN_BLAD} staat het lidgeld twee keer: '
    f'{g.LEDEN_KOP[10]} en {g.LEDEN_KOP[11]}. En de vervaldatum ook: '
    f'{g.LEDEN_KOP[13]} en {g.LEDEN_KOP[14]}. De twee kolommen met "in tekst" '
    'hebben een oranje titel.',
    'Gebruik altijd de tekstkolom. Voeg de andere één keer samen en kijk wat '
    'er in je brief staat — dan weet je waarom ze er staat. Dat is fiche '
    f'{12} uit het eerste boekje.',
], GRIJS)

kader(doc, 'Wat je indient', [
    'lidkaarten-jouwnaam.docx  ·  enveloppen-jouwnaam.docx',
    'brief-jouwnaam.docx (het hoofddocument) én het samengevoegde resultaat',
    f'ploeglijst-{g.LIJST_BLAD_PLOEG.lower()}-jouwnaam.docx',
    'tornooibrief-, tornooienveloppen- en '
    f'tornooilijst-{g.TORN_EIND_CATEGORIE.lower()}-jouwnaam.docx',
    f'clubpost-jouwnaam.xlsx, met het werkblad {a.ANTW_BLAD} ingevuld',
], GROEN)

kader(doc, 'Over de gegevens', [g.WAARSCHUWING], GRIJS)

for stap in o.STAPPEN:
    paginaeinde(doc)
    kop(doc, f"Stap {stap['nr']} — {stap['titel']}", 1)
    uren = 'lesuur' if stap['lesuren'] == 1 else 'lesuren'
    werk = sum(p for *_, p in stap.get('stappen', []))
    opm = sum(p for *_, p in stap.get('opmaak', []))
    alinea(doc, f"soort: {stap['soort']}  ·  lijst: {stap['lijst']}  ·  "
                f"{stap['lesuren']} {uren}  ·  {o.punten_van(stap)} punten "
                f"(waarvan {opm} op de opmaak)",
           schuin=True, kleur=GRIJS, na=4)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run('Fiches:  ')
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = GRIJS
    stukken = [f"{n} — {f.FICHES[n - f.FICHE_START]['naam']}"
               for n in stap['fiches']]
    stukken += [f"{n} — {f.EERSTE[n]} (eerste boekje)"
                for n in stap['fiches_eerste']]
    r = p.add_run(' · '.join(stukken))
    r.font.size = Pt(10); r.font.color.rgb = ORANJE

    for regel in stap['inleiding']:
        alinea(doc, regel, na=4)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

    kop(doc, f'Het samenvoegen ({werk} punten)', 2, GRIJS)
    tabel(doc, ['Wat', 'Hoe', 'Pt'],
          [[naam, hoe, punten] for naam, hoe, punten in stap['stappen']],
          breedtes=[4.0, 11.0, 1.4])

    kop(doc, f'De opmaak ({opm} punten)', 2, GRIJS)
    tabel(doc, ['Wat', 'Hoe precies', 'Pt'],
          [[naam, hoe, punten] for naam, hoe, punten in stap['opmaak']],
          breedtes=[4.0, 11.0, 1.4])

    voorbeeldblok(doc, stap)

    vragen = o.vragen_van(stap)
    if vragen:
        kop(doc, f'Op het werkblad {a.ANTW_BLAD}', 2, GRIJS)
        tabel(doc, ['Cel', 'Vraag', 'Pt'],
              [[f'{ANTW_KOLOM}{a.ANTW_START + i - 1}', v, 1]
               for i, v, _antw in vragen],
              breedtes=[1.8, 13.2, 1.4])

    kader(doc, 'Je stap is af als…', [stap['klaar'], '',
                                      'CONTROLE  ·  ' + stap['controle']],
          GROEN)
    kader(doc, 'Loop je vast?', stap['vast'], ORANJE)

paginaeinde(doc)
kop(doc, 'Helemaal klaar?', 1)
alinea(doc, 'Loop dit lijstje af in de AFDRUKWEERGAVE, met de zoom op één '
            'volledige pagina.', schuin=True, kleur=GRIJS, na=8)
for regel in [
    f'Op je etiketvel staan alle {g.ETIKET_PER_BLAD} kaarten van het eerste '
    'blad identiek opgemaakt, met alleen andere namen.',
    'Op elke lidkaart staan vier regels. Niet drie.',
    f'Je hebt {a.AANTAL_ENVELOPPEN} enveloppen, niet {a.AANTAL_LEDEN}.',
    'De datum in je brief staat tegen de rechtermarge, en je hebt er geen '
    'spaties voor gebruikt.',
    'De tabel in je brief heeft geen randen en staat niet over de volle '
    'breedte.',
    'Je voettekst staat in de voettekst, en het paginanummer is een veld.',
    f'In je ploeglijst staat de koprij één keer, niet {a.AANTAL_LIJSTRIJEN} '
    'keer.',
    'Nergens staat een kommagetal waar een bedrag, een uur of een datum hoort.',
    f'Het werkblad {a.ANTW_BLAD} is helemaal ingevuld.',
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(4)
    p.add_run('☐   ').font.size = Pt(13)
    zin(p, regel)

paginanummers(doc, 'opdracht')
doc.save(OPDRACHT)
print('geschreven:', OPDRACHT)


# ==========================================================================
#  2. het tweede theorieboekje
# ==========================================================================
doc = Document()
opzet(doc)
kop(doc, f'Samenvoegen en opmaak — fiche {f.FICHE_START} tot '
         f'{f.nummer(len(f.FICHES) - 1)}', 0)
alinea(doc, 'Het tweede boekje: enveloppen, lijsten, en de opmaak',
       schuin=True, kleur=GRIJS, na=12)
alinea(doc,
       f'Dit is het vervolg op {f.EERSTE_BOEKJE}. Dat eerste boekje heeft '
       f'{f.FICHES_EERSTE_BOEKJE} fiches en legt het mechanisme uit: '
       'hoofddocument, gegevensbron, velden invoegen, etiketten, voorbeeld en '
       'voltooien, Als…Dan…Anders, filteren en sorteren. Dat blijft gelden en '
       'staat hier niet opnieuw.', na=8)
alinea(doc,
       f'De nummering loopt door. Fiche {f.FICHE_START} is de eerste van dit '
       'boekje, zodat een fichenummer in allebei de boekjes hetzelfde '
       'betekent. Houd ze dus samen.', na=12)
fiche_index(doc, 'De fiches in dit boekje')
kader(doc, 'De namen in het lint', [
    'De namen hieronder zijn die van het Nederlandstalige Word (Microsoft 365 '
    'en 2021). In een Engelse Word heet Verzendlijsten Mailings, en de soort '
    'Lijst heet Directory.',
    'Staat een knop bij jou ergens anders? De namen kloppen wel. Zoek op de '
    'naam, niet op de plaats.',
], BLAUW)

vorig_deel = None
for i, kaart in enumerate(f.FICHES):
    paginaeinde(doc)
    if kaart['deel'] != vorig_deel:
        kop(doc, kaart['deel'], 1)
        vorig_deel = kaart['deel']
    fiche_uit(doc, f.nummer(i), kaart)

paginanummers(doc, 'theorie, tweede boekje')
doc.save(THEORIE)
print('geschreven:', THEORIE)


# ==========================================================================
#  3. de twee briefmodellen — met opzet zonder enige opmaak
# ==========================================================================
def wenk(doc, tekst, na=12):
    """Een grijze aanwijzing in de brief die zij moeten vervangen."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(na)
    r = p.add_run(tekst)
    r.italic = True
    r.font.color.rgb = GRIJS
    return p


# ------------------------------------------------- de ledenbrief (stap 3)
doc = Document()
opzet(doc)
briefregel(doc, g.CLUB)
briefregel(doc, f'{g.CLUB_ADRES}, {g.CLUB_POSTCODE} {g.CLUB_GEMEENTE}, '
                f'{g.CLUB_MAIL}', na=12)
briefregel(doc, '[[Voornaam]] [[Achternaam]]')
briefregel(doc, '[[Adresregel]]')
briefregel(doc, '[[Woonplaats]]', na=12)
briefregel(doc, f'{g.CLUB_GEMEENTE}, {g.datum_lang(g.BRIEFDATUM)}', na=12)
briefregel(doc, 'Beste [[Voornaam]],', na=12)
briefregel(doc,
           'Het seizoen is begonnen en we zijn blij dat je er weer bij bent. '
           'Hieronder vind je de gegevens van je ploeg en van je lidgeld.',
           na=12)
briefregel(doc,
           'Je speelt dit seizoen bij [[Ploeg]]. Je trainer is [[Trainer]], '
           'en jullie trainen elke [[Trainingsdag]] om [[Trainingsuur]] op '
           'het terrein achter de kantine.', na=12)
wenk(doc, '— hier komt de tabel met het overzicht —')
wenk(doc, '— hier komt de zin met Als…Dan…Anders —')
briefregel(doc,
           'Heb je vragen, spreek dan je trainer aan of mail naar '
           f'{g.CLUB_MAIL}.', na=12)
briefregel(doc, 'Sportieve groeten', na=24)
briefregel(doc, 'Het bestuur', na=0)
briefregel(doc, g.CLUB, na=0)
doc.add_paragraph()
kader(doc, 'Voor de leerling — lees dit eerst', [
    'Sla dit document eerst op onder je eigen naam: Bestand, Opslaan als, '
    'brief-jouwnaam.docx.',
    'Deze brief is met OPZET lelijk. Alles staat links, alles is dezelfde '
    'letter, er is geen tabel en er is geen voettekst. De opmaak is jouw werk, '
    'en er staan punten op.',
    'Elke oranje marker tussen dubbele haken vervang je door het '
    'samenvoegveld met dezelfde naam. Verwijder de marker en voeg het veld in '
    'de plaats ervan in. Typ de punthaken van het veld niet zelf.',
    'De twee grijze regels in het midden vervang je: de eerste door de tabel, '
    'de tweede door de zin met Als…Dan…Anders.',
    'Dit kader hoort niet in de brief. Verwijder het voor je samenvoegt.',
], ORANJE)
paginanummers(doc, 'briefmodel leden')
doc.save(BRIEF_LEDEN)
print('geschreven:', BRIEF_LEDEN)

# ---------------------------------------------- de tornooibrief (stap 5)
doc = Document()
opzet(doc)
briefregel(doc, g.CLUB)
briefregel(doc, f'{g.CLUB_ADRES}, {g.CLUB_POSTCODE} {g.CLUB_GEMEENTE}, '
                f'{g.CLUB_MAIL}', na=12)
for _ in range(4):
    briefregel(doc, '', na=2)
briefregel(doc, f'{g.CLUB_GEMEENTE}, {g.datum_lang(g.BRIEFDATUM)}', na=12)
briefregel(doc, 'Betreft: uitnodiging voor het jeugdtornooi', na=12)
briefregel(doc, '', na=12)
briefregel(doc,
           f'{g.CLUB} organiseert dit voorjaar opnieuw haar jeugdtornooi, en '
           'wij zijn blij dat uw club erbij wil zijn. Met deze brief '
           'bevestigen wij uw inschrijving.', na=12)
briefregel(doc, '', na=12)
briefregel(doc,
           'Het inschrijvingsgeld schrijft u over op rekeningnummer '
           f'{g.CLUB_REKENING}, met de naam van uw club als mededeling. De '
           'wedstrijdkalender bezorgen wij u drie weken voor het tornooi.',
           na=12)
briefregel(doc, '', na=12)
briefregel(doc,
           'Hebt u vragen over de inschrijving, dan mag u ons altijd '
           f'contacteren via {g.CLUB_MAIL}.', na=12)
briefregel(doc, 'Met sportieve groeten', na=24)
briefregel(doc, 'Het tornooicomité', na=0)
briefregel(doc, g.CLUB, na=0)
doc.add_paragraph()
kader(doc, 'Voor de leerling — dit is de eindopdracht', [
    'Sla dit document eerst op onder je eigen naam: '
    'tornooibrief-jouwnaam.docx.',
    'Er staan GEEN markers in, en de opmaak is er met opzet uitgelaten. Jij '
    'beslist zelf waar de velden horen, en de hele lay-out van deze brief is '
    'jouw werk: de marges, de datum tegen de rechtermarge, de witruimte en de '
    'tekening van de alinea\'s.',
    'Deze velden moeten er in elk geval in: Club, de aanhef (Geachte, de '
    'aanspreking, de naam), Adresregel, Woonplaats, Categorie, Aantal ploegen '
    'en Inschrijvingsgeld in tekst.',
    'De lege regels bovenaan zijn voor het adres; de lege regel onder de '
    'betreftregel is voor de aanhef. De drie lege regels in de tekst zijn '
    'voor de zinnen met de categorie, het aantal ploegen en het bedrag.',
    f'Eén zin komt er alleen bij wie met {g.TORN_GROOT} ploegen of meer komt: '
    'een eigen kleedkamer. Die zet je met Als…Dan…Anders.',
    'Dit kader hoort niet in de brief. Verwijder het voor je samenvoegt.',
], ORANJE)
paginanummers(doc, 'briefmodel tornooi')
doc.save(BRIEF_TORNOOI)
print('geschreven:', BRIEF_TORNOOI)


# ==========================================================================
#  4. de lerarensleutel
# ==========================================================================
doc = Document()
opzet(doc)
kop(doc, g.TITEL + ' — lerarensleutel', 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=12)

kop(doc, 'In het kort', 2, GRIJS)
alinea(doc,
       f'Vijf stappen, {g.LESUREN} lesuren, {o.TOTAAL} punten, waarvan '
       f'{o.PUNTEN_OPMAAK} op de OPMAAK alleen. Alles in Word: in het '
       'Excelbestand valt niets uit te rekenen, en dat is met opzet.', na=6)
alinea(doc,
       'Word kent vijf soorten samenvoegdocumenten. Hier maken ze er vier: '
       'etiketten, enveloppen, brieven en een lijst. E-mail laten we liggen; '
       'daar valt in een lokaal niets zinnigs mee te doen, en ze zouden het '
       'ook echt versturen.', na=6)
alinea(doc,
       f'De twee nieuwe soorten zijn de ENVELOP (stap 2) en de LIJST (stap '
       '4). Die lijst is de soort die niemand kent en die ze later het '
       'vaakst nodig hebben: een ploeglijst, een deelnemerslijst, een '
       'inventaris.', na=6)
alinea(doc,
       f'De theorie staat in twee boekjes. Dit is de tweede bundel: '
       f'{o.THEORIEBUNDEL} begint bij fiche {f.FICHE_START}, en '
       f'{g.VOORGANGER_THEORIE} uit de vorige lessen blijft gelden. Deel ze '
       'samen uit.', na=10)

punten_tabel(doc)

kader(doc, 'Hoeveel lesuren echt?', [
    f'Op papier {g.LESUREN}, één per stap. Stap 1 tot 4 halen ze in een uur '
    'als je de eerste samenvoeging klassikaal meedoet; stap 5 is krap in één '
    'uur. Reken er zes als je de eindopdracht ook degelijk wil quoteren.',
    'Stap 2 is het uur dat je kan laten vallen. Een envelop is de makkelijkste '
    'van de vier en voegt na de etiketten weinig nieuws toe. Stap 4 zou ik '
    'NIET laten vallen: dat is de enige soort die ze nergens anders '
    'tegenkomen.',
], BLAUW)

kader(doc, 'De drie dingen die je klassikaal moet voordoen', [
    '1.  LABELS BIJWERKEN KOMT LAATST. Opmaken, dan Labels bijwerken. Doen ze '
    'het omgekeerd, dan is alleen de eerste kaart mooi. Laat het één keer '
    'fout zien op het bord — dat onthouden ze beter dan de regel.',
    '2.  DE TWEE KADERS OP EEN ENVELOP. Afzender linksboven, geadresseerde '
    'rechtsonder. Ze klikken bijna allemaal eerst in het verkeerde.',
    '3.  BIJ EEN LIJST HERHAALT WORD HET HELE DOCUMENT. Niet een bladzijde per '
    'record, maar alles. Zetten ze een koprij in het hoofddocument, dan staat '
    f'die er {a.AANTAL_LIJSTRIJEN} keer. Dit is de enige valkuil in stap 4, '
    'en het kost een heel uur als ze hem niet kennen.',
], ORANJE)

kader(doc, 'Opmaak quoteren zonder discussie', [
    f'Er staan {o.PUNTEN_OPMAAK} punten op de opmaak, en bij elke stap staat '
    'in de opdracht precies wat er verwacht wordt: welke lettergrootte, vet '
    'of niet, welke uitlijning, welke tabstop. Niet "mooi" maar "9 punten, '
    'cursief, gecentreerd". Zo is er niets te betwisten.',
    'Kijk opmaak na in de AFDRUKWEERGAVE met de zoom op één volledige pagina. '
    'In de gewone weergave zie je de helft niet — geen voettekst, geen '
    'paginaranden, geen tabstops.',
    'Snelle test voor de tabstop in stap 3: zet de cursor in de datumregel en '
    'kijk in de lintlijn boven het document. Staat er een tabstopteken op '
    f'{g.BRIEF_TABSTOP_CM:g} cm, dan is het goed; staat er niets, dan heeft '
    'die leerling spaties gebruikt.',
], GROEN)

kader(doc, 'Wat je niet automatisch kan nakijken', [
    'Niets van deze bundel. Alles is Word, dus alles is met het oog.',
    'Vraag bij stap 3 om het HOOFDdocument én het samengevoegde document. In '
    'het eerste zie je of er echte velden en een echte voettekst in zitten '
    '(Alt+F9 toont de velden); in het tweede of het resultaat klopt.',
    f'Het werkblad {a.ANTW_BLAD} in hun Excelbestand is wel gewoon na te '
    f'lezen: {len(a.ANTWOORDBLAD)} vragen, één punt per stuk, en de '
    'antwoorden staan hieronder per stap.',
], BLAUW)

for stap in o.STAPPEN:
    paginaeinde(doc)
    uren = 'lesuur' if stap['lesuren'] == 1 else 'lesuren'
    werk = sum(p for *_, p in stap.get('stappen', []))
    opm = sum(p for *_, p in stap.get('opmaak', []))
    kop(doc, f"Stap {stap['nr']} — {stap['titel']}", 1)
    alinea(doc, f"soort {stap['soort']}  ·  lijst {stap['lijst']}  ·  "
                f"{stap['lesuren']} {uren}  ·  {o.punten_van(stap)} punten "
                f"({werk} samenvoegen + {opm} opmaak + "
                f"{len(o.vragen_van(stap))} vragen)",
           schuin=True, kleur=GRIJS, na=8)

    kop(doc, 'Het samenvoegen', 2, GRIJS)
    tabel(doc, ['Wat', 'Hoe', 'Pt'],
          [[naam, hoe, punten] for naam, hoe, punten in stap['stappen']],
          breedtes=[3.8, 11.2, 1.4])
    kop(doc, 'De opmaak', 2, GRIJS)
    tabel(doc, ['Wat', 'Hoe precies', 'Pt'],
          [[naam, hoe, punten] for naam, hoe, punten in stap['opmaak']],
          breedtes=[3.8, 11.2, 1.4])

    nr = stap['nr']
    if nr == 1:
        kop(doc, f'De kaart van {a.VOORBEELD.naam}', 2, GRIJS)
        tabel(doc, ['Regel', 'Wat erop staat', 'Opmaak'],
              [[i, tekst, ', '.join(filter(None, [
                  f"{regel['grootte']} pt",
                  'vet' if regel['vet'] else '',
                  'cursief' if regel['cursief'] else '',
                  '' if regel['kleur'] == 'zwart' else regel['kleur'],
                  g.LIDKAART_UITLIJNING]))]
               for i, (regel, tekst) in enumerate(
                   zip(g.LIDKAART, a.KAART_VOORBEELD), 1)],
              'Light List Accent 1', [1.4, 8.0, 6.6])
        alinea(doc, f'{g.ETIKET_SOORT}. {a.AANTAL_LEDEN} kaarten geeft '
                    f'{a.ETIKET_BLADEN} bladen: {g.ETIKET_PER_BLAD} op het '
                    f'eerste, {a.ETIKET_LAATSTE} op het tweede, '
                    f'{a.ETIKET_LEEG} leeg.', schuin=True, kleur=GRIJS, na=10)
    elif nr == 2:
        kop(doc, f'De envelop van {a.ENVELOP_VOORBEELD_LID.naam}', 2, GRIJS)
        tabel(doc, ['Waar', 'Wat erop staat'],
              [[f'linksboven, {g.ENVELOP_AFZENDER_GROOTTE} pt',
                '  ·  '.join(g.ENVELOP_AFZENDER)],
               [f'rechtsonder, {g.ENVELOP_GEADRESSEERDE_GROOTTE} pt',
                '  ·  '.join(a.ENVELOP_VOORBEELD)]],
              'Light List Accent 1', [4.6, 11.4])
        alinea(doc, f'Formaat {g.ENVELOP_FORMAAT}. Het filter '
                    f'{g.ENVELOP_FILTER[0]} = {g.ENVELOP_FILTER[1]} laat '
                    f'{a.AANTAL_ENVELOPPEN} van de {a.AANTAL_LEDEN} '
                    'enveloppen over. Dat zijn: '
                    + ', '.join(l.naam for l in a.ENVELOPPEN) + '.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 3:
        kop(doc, f'De tabel in de brief van {a.VOORBEELD.naam}', 2, GRIJS)
        tabel(doc, ['Links', 'Rechts', 'Wat er dan staat'],
              [[opschrift,
                f'«{veld}»' if veld else 'vaste tekst',
                waarde]
               for (opschrift, veld), (_o, waarde)
               in zip(g.BRIEF_TABEL, a.TABEL_VOORBEELD)],
              'Light List Accent 1', [4.2, 5.8, 6.0])
        alinea(doc, f'{a.AANTAL_BRIEVEN} brieven, waarvan '
                    f'{a.AANTAL_AANMANING} met de aanmaningszin. Dat zijn de '
                    f'leden met {g.BRIEF_REGEL[0]} = {g.BRIEF_REGEL[1]}: '
                    + ', '.join(l.naam for l in a.MET_AANMANING) + '.',
               schuin=True, kleur=GRIJS, na=4)
        alinea(doc, 'Snelle test: zoek in het samengevoegde document op het '
                    f'woord "betaald". Dat hoort {a.AANTAL_AANMANING} keer '
                    'voor te komen in de aanmaningszin.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 4:
        kop(doc, f'De lijst van {g.LIJST_BLAD_PLOEG}', 2, GRIJS)
        tabel(doc, g.LIJST_KOLOMMEN, a.LIJST_RIJEN, 'Light List Accent 1')
        alinea(doc, f'{a.AANTAL_LIJSTRIJEN} regels, gesorteerd op '
                    f'{g.LIJST_SORTEER}, met {a.LIJST_EERSTE.achternaam} '
                    'bovenaan. De koprij hoort er ÉÉN keer te staan, in het '
                    'samengevoegde document.',
               schuin=True, kleur=GRIJS, na=4)
        alinea(doc, 'Wie de koprij in het hoofddocument gezet heeft, ziet ze '
                    f'{a.AANTAL_LIJSTRIJEN} keer terug. Laat die leerling '
                    'niet opnieuw beginnen: de koprij uit het hoofddocument '
                    'halen en opnieuw samenvoegen is één minuut werk.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 5:
        kop(doc, 'De veertien clubs', 2, GRIJS)
        tabel(doc, ['Club', 'Aanhef', 'Adresregel', 'Woonplaats', 'Cat.',
                    'Ploegen', 'Bedrag', 'Extra zin'],
              [[c.club, f'Geachte {c.aanspreking} {c.naam}', c.adresregel,
                c.woonplaats, c.categorie, c.aantal_ploegen, c.geld_tekst,
                'ja' if c.extra_zin else 'nee'] for c in a.CLUBS],
              'Light List Accent 1')
        alinea(doc, f'{a.AANTAL_CLUBS} brieven, {a.AANTAL_EXTRA} met de extra '
                    f'zin (vanaf {g.TORN_GROOT} ploegen), totaal '
                    f'{a.TORN_TOTAAL_TEKST}. De lijst van '
                    f'{g.TORN_EIND_CATEGORIE} heeft '
                    f'{a.AANTAL_EINDLIJST} regels.',
               schuin=True, kleur=GRIJS, na=4)
        alinea(doc, 'Hier mag je streng zijn op de opmaak. Ze hebben het vier '
                    'uur gedaan met de stappen ernaast; nu moeten ze het '
                    'zonder kunnen. Alles links en in dezelfde letter is '
                    f'{sum(p for *_, p in stap["opmaak"])} punten kwijt.',
               schuin=True, kleur=GRIJS, na=10)

    vragen = o.vragen_van(stap)
    if vragen:
        kop(doc, 'De antwoorden', 2, GRIJS)
        tabel(doc, ['Cel', 'Vraag', 'Antwoord', 'Pt'],
              [[f'{ANTW_KOLOM}{a.ANTW_START + i - 1}', v, antw, 1]
               for i, v, antw in vragen],
              breedtes=[1.6, 8.4, 5.0, 1.4])
    kader(doc, 'Waar je naar kijkt', [stap['controle']], GROEN)

paginaeinde(doc)
kop(doc, 'De vijf lesuren', 1)
tabel(doc, ['Lesuur', 'Wat', 'Waar je op let'],
      [['1', 'Stap 1 — lidkaarten',
        'Labels bijwerken komt LAATST. Doe het eerste etiket klassikaal mee, '
        'inclusief de opmaak, en klik dan samen op Labels bijwerken.'],
       ['2', 'Stap 2 — enveloppen',
        'Het juiste kader, en het filter. Laat ze het aantal ontvangers '
        'voorlezen voor ze samenvoegen.'],
       ['3', 'Stap 3 — de brief',
        'Het zwaarste uur: twaalf van de vijfentwintig punten staan op de '
        'opmaak. Doe de tabstop klassikaal; de tabel en de voettekst kunnen '
        'ze zelf.'],
       ['4', 'Stap 4 — de ploeglijst',
        'Zeg VOORAF dat het hele document herhaald wordt. Zeg het twee keer. '
        'Daarna gaat dit uur vlot.'],
       ['5', 'Stap 5 — het tornooi',
        'Krap in één uur. Laat ze beginnen met de brief; wie die rond heeft, '
        'doet de enveloppen en dan de lijst.']],
      breedtes=[1.6, 5.4, 9.4])

kader(doc, 'Differentiëren', [
    'TE SNEL — laat ze de vijfde soort erbij doen: E-mailberichten. Daar '
    'hebben ze een kolom met e-mailadressen voor nodig, en die kunnen ze zelf '
    'maken met de tekstfuncties uit de festivalbundel. Niets echt versturen.',
    'TE SNEL, korter — laat ze de ploeglijst voor alle '
    f'{a.AANTAL_PLOEGEN} ploegen maken in plaats van voor één. Vier keer '
    'hetzelfde hoofddocument, vier keer een ander filter.',
    'TE TRAAG — laat stap 2 vallen en geef dat uur aan stap 3. De opmaak van '
    'de brief is het nuttigste stuk van de hele bundel.',
    'TE TRAAG, erger — laat in stap 3 de tabel vallen en houd de tabstop en '
    'de voettekst. Dan heeft die leerling nog altijd twee opmaaktechnieken '
    'geleerd die hij overal nodig heeft.',
], BLAUW)

kader(doc, 'Waar dit op voortbouwt', [
    f'Dit is de vervolgbundel op {g.VOORGANGER}. Daar lag het gewicht op '
    'Excel: de lijst samenvoegklaar maken met formules, en de les dat de '
    'opmaak van een cel niet meekomt naar Word.',
    'Die les ligt hier klaar: het lidgeld en de vervaldatum staan twee keer in '
    'de ledenlijst, één keer als getal en één keer als tekst, met een oranje '
    'kolomtitel op de tekstkolom. Laat ze de verkeerde één keer gebruiken.',
    'Wie de eerste bundel niet gedaan heeft, kan deze toch maken. Het eerste '
    f'theorieboekje ({g.VOORGANGER_THEORIE}) is dan wel verplichte lectuur.',
], BLAUW)

paginanummers(doc, 'lerarensleutel')
doc.save(SLEUTEL)
print('geschreven:', SLEUTEL)
