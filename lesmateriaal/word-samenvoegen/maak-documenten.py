# -*- coding: utf-8 -*-
"""Bouwt de vijf documenten van de samenvoegbundel.

  samenvoegen-opdracht.docx               de vijf stappen
  samenvoegen-theorie.docx                de fiches, apart boekje
  samenvoegen-lerarensleutel.docx         alles uitgeschreven
  samenvoegen-brief-vrijwilligers.docx    de brief met markers, voor stap 3
  samenvoegen-brief-sponsors.docx         de brief zonder markers, voor stap 5

Er komt geen samenvoegveld in de briefmodellen. Een MERGEFIELD kan python-docx
wel schrijven, maar de verwijzing naar de gegevensbron is een pad op één
bepaalde computer. Dat overleeft het uitdelen niet, en de velden invoegen is
bovendien net de oefening.
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

OPDRACHT = os.path.join(HIER, 'samenvoegen-opdracht.docx')
THEORIE = os.path.join(HIER, o.THEORIEBUNDEL)
SLEUTEL = os.path.join(HIER, 'samenvoegen-lerarensleutel.docx')
BRIEF_VRIJ = os.path.join(HIER, o.BRIEF_VRIJ)
BRIEF_SPON = os.path.join(HIER, o.BRIEF_SPON)
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
        stukken = [f"{i} {kaart['naam']}"
                   for i, kaart in enumerate(f.FICHES, 1)
                   if kaart['deel'] == deel]
        rijen.append([deel, '   ·   '.join(stukken)])
    tabel(doc, ['Deel', 'Fiches'], rijen, breedtes=[5.0, 11.4])


def punten_tabel(doc):
    tabel(doc, ['Stap', 'Wat je doet', 'Waar', 'Lesuren', 'Fiches', 'Pt'],
          [[stap['nr'], stap['titel'], stap['waar'], stap['lesuren'],
            ', '.join(str(n) for n in stap['fiches']), o.punten_van(stap)]
           for stap in o.STAPPEN]
          + [['', 'Samen', '', o.LESUREN, '', o.TOTAAL]],
          breedtes=[1.4, 5.6, 3.0, 2.0, 2.6, 1.4])


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
doc = Document()
opzet(doc)
kop(doc, g.TITEL, 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=4)
alinea(doc, 'Naam: ......................................    Klas: ..........',
       na=14)

alinea(doc,
       f'{g.LESUREN} lesuren, vijf stappen. Je maakt uit één Excellijst '
       f'{a.AANTAL_VRIJ} brieven en twee bladen etiketten, zonder één brief te '
       'hertypen. Dat heet afdruk samenvoegen, en het is waarschijnlijk het '
       'nuttigste wat Word kan.', na=8)
alinea(doc,
       'Stap 1 is Excel: de lijst zo klaarmaken dat Word ermee kan werken. '
       'Stap 2, 3 en 4 zijn Word. Stap 5 is de eindopdracht: dan doe je het '
       'helemaal zelf, op een lijst die je nog niet gezien hebt.', na=8)
alinea(doc,
       f'In deze bundel staat geen theorie. Die staat in {o.THEORIEBUNDEL}, '
       f'{len(f.FICHES)} fiches in drie delen. Bij elke stap staat welke je '
       'nodig hebt.', na=12)

punten_tabel(doc)
fiche_index(doc, f'De fiches staan in {o.THEORIEBUNDEL}:')

kader(doc, 'Vier regels die altijd gelden', [
    '1.  Zet je Excelbestand en je Worddocumenten in DEZELFDE map, en laat ze '
    'daar staan. Word onthoudt waar je lijst staat; verplaats of hernoem je ze '
    'achteraf, dan vindt Word je lijst niet meer terug.',
    '2.  Werk nooit in het model dat je krijgt. Bestand, Opslaan als, en zet je '
    'eigen naam in de bestandsnaam. Zo kan je altijd opnieuw beginnen.',
    '3.  Wat je op je scherm ziet, is niet altijd wat er in de cel staat. Een '
    'uur en een bedrag zijn getallen; het euroteken en de dubbele punt zijn '
    'opmaak. Opmaak gaat NIET mee naar Word. Daarvoor bestaat TEKST.',
    '4.  Typ de punthaken van een samenvoegveld nooit zelf. Een echt veld '
    'wordt grijs als je erop klikt; getypte punthaken doen niets.',
], ORANJE)

kader(doc, 'Wat je NIET zelf typt', [
    'Bij elke kolom in stap 1 en 5 staat precies wat erin moet komen, en wat '
    'er in de eerste rij hoort te staan als het klopt. Houd je daaraan: Word '
    'neemt letterlijk over wat er in de cel staat.',
    'Je typt nergens zelf een aanspreking. In de vrijwilligerslijst staat geen '
    'geslacht, dus daar is de aanhef "Beste" plus de voornaam — en niets '
    'anders. In de sponsorlijst staat de aanspreking wél in een kolom (heer of '
    'mevrouw); die plak je erbij, je bedenkt ze niet.',
    'Je typt ook nooit zelf een naam, een adres, een uur of een bedrag in een '
    'brief. Alles wat per persoon verschilt, komt uit de lijst. Zie je jezelf '
    'iets intypen wat in de lijst staat, dan doe je het verkeerd.',
    'En je typt de punthaken « » van een samenvoegveld niet zelf. Die horen '
    'bij het veld en komen mee als je het invoegt.',
], ORANJE)

kader(doc, 'Wat je indient', [
    'samenvoegen-jouwnaam.xlsx — met de kolommen van stap 1 en 5, en het '
    'antwoordblad ingevuld.',
    'etiketten-jouwnaam.docx — het samengevoegde etiketvel van stap 2.',
    'brieven-gesorteerd-jouwnaam.docx — de samengevoegde brieven van stap 4, '
    'met de extra zin erin.',
    'sponsorbrief-jouwnaam.docx en sponsoretiketten-jouwnaam.docx — de '
    'eindopdracht.',
    'Hou ook je HOOFDdocumenten bij (brief-jouwnaam.docx). Daar zitten de '
    'velden in; het samengevoegde resultaat is gewone tekst.',
], GROEN)

kader(doc, 'Over de gegevens', [g.WAARSCHUWING], GRIJS)

for stap in o.STAPPEN:
    paginaeinde(doc)
    kop(doc, f"Stap {stap['nr']} — {stap['titel']}", 1)
    uren = 'lesuur' if stap['lesuren'] == 1 else 'lesuren'
    waar = (f"werkblad '{stap['blad']}'" if stap.get('blad')
            else 'in Word')
    alinea(doc, f"{stap['waar']}  ·  {waar}  ·  {stap['lesuren']} {uren}  ·  "
                f"{punten_van(stap)} punten", schuin=True, kleur=GRIJS, na=4)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(f'Fiches uit {o.THEORIEBUNDEL}:  ')
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = GRIJS
    r = p.add_run(' · '.join(f"{n} — {f.FICHES[n - 1]['naam']}"
                             for n in stap['fiches']))
    r.font.size = Pt(10); r.font.color.rgb = ORANJE

    for regel in stap['inleiding']:
        alinea(doc, regel, na=4)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

    if stap.get('vullen'):
        rij1, wie, waarden = a.RIJ1[stap['blad']]
        kop(doc, 'In Excel', 2, GRIJS)
        alinea(doc,
               f'Je typt elke formule ÉÉN keer, in rij {rij1}, en voert ze '
               f'door tot onderaan. De laatste kolom hieronder laat zien wat '
               f'er in rij {rij1} hoort te staan — dat is de rij van {wie}. '
               'Komt er bij jou iets anders te staan, dan weet je meteen dat '
               'het nog niet klopt.', na=8)
        tabel(doc, ['Kolom', 'Naam', 'Wat erin komt', f'In rij {rij1} staat',
                    'Pt'],
              [[kolom, naam, wat, waarden[naam], punten]
               for kolom, naam, wat, _formule, punten in stap['vullen']],
              breedtes=[1.4, 2.8, 7.6, 3.4, 1.2])

    if stap.get('stappen'):
        kop(doc, 'In Word', 2, GRIJS)
        tabel(doc, ['Wat', 'Hoe', 'Pt'],
              [[naam, hoe, punten] for naam, hoe, punten in stap['stappen']],
              breedtes=[4.4, 10.6, 1.4])

    if stap.get('etiket'):
        v = a.VRIJ[0]
        velden = {'Voornaam': v.voornaam, 'Achternaam': v.achternaam,
                  'Adresregel': v.adresregel, 'Woonplaats': v.woonplaats}
        kop(doc, 'Zo ziet het eerste etiket eruit', 2, GRIJS)
        tabel(doc, ['Wat je in het etiket zet',
                    'Wat er na Voorbeeld van resultaten staat'],
              [[' '.join(f'«{naam}»' for naam in regel),
                ' '.join(velden[naam] for naam in regel)]
               for regel in stap['etiket']],
              'Light List Accent 1', [7.0, 8.0])
        alinea(doc, 'Drie regels onder elkaar, dus Enter na elke regel. Geen '
                    'komma tussen de voornaam en de achternaam, wel een '
                    'spatie.', schuin=True, kleur=GRIJS, na=10)

    vragen = [(i, v, antw) for i, (st, v, antw) in enumerate(a.ANTWOORDBLAD, 1)
              if st == stap['nr']]
    if vragen:
        kop(doc, f"Op het werkblad {a.ANTW_BLAD}", 2, GRIJS)
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
alinea(doc, 'Loop dit lijstje af voor je indient.', schuin=True, kleur=GRIJS,
       na=8)
for regel in [
    f'In de kolom Vergoeding staat overal een euroteken, en in Startuur overal '
    'een uur met een dubbele punt.',
    'Nergens staat #N/B of #WAARDE! in je Excelbestand.',
    'Op je etiketvel staat op elk etiket een ANDERE naam.',
    f'Er zijn {a.AANTAL_BRIEVEN} brieven, en in {a.AANTAL_MINDERJARIG} ervan '
    'staat de extra zin over de toelating.',
    'In geen enkele brief staat nog een kommagetal waar een uur of een bedrag '
    'hoort.',
    'Je filter staat AF, behalve waar het gevraagd werd.',
    f'Het werkblad {a.ANTW_BLAD} is helemaal ingevuld.',
    'Je hoofddocumenten én je samengevoegde documenten zijn bewaard, onder '
    'verschillende namen.',
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
#  2. de theoriebundel
# ==========================================================================
doc = Document()
opzet(doc)
kop(doc, 'Afdruk samenvoegen — ' + str(len(f.FICHES)) + ' fiches', 0)
alinea(doc, 'Van een Excellijst naar brieven en etiketten', schuin=True,
       kleur=GRIJS, na=12)
alinea(doc,
       'Dit boekje hoort bij de opdrachtbundel. Daar staat wat je maakt, hier '
       'staat hoe het werkt. Elke fiche staat op een eigen pagina, zodat je '
       'ze kan openleggen naast je scherm.', na=8)
alinea(doc,
       'Deel 1 gaat over je lijst in Excel. Deel 2 over het samenvoegen in '
       'Word. Deel 3 gaat over wat er misgaat — en dat gebeurt bij iedereen, '
       'dus sla het niet over.', na=12)
fiche_index(doc, 'De fiches')
kader(doc, 'De namen in het lint', [
    'De namen hieronder zijn die van het Nederlandstalige Word (Microsoft 365 '
    'en 2021). Werk je in een Engelse Word, dan heet het tabblad Mailings in '
    'plaats van Verzendlijsten, en Samenvoegveld invoegen heet Insert Merge '
    'Field.',
    'Staat een knop bij jou ergens anders? De namen kloppen wel. Zoek op de '
    'naam, niet op de plaats.',
], BLAUW)

vorig_deel = None
for nummer, kaart in enumerate(f.FICHES, 1):
    paginaeinde(doc)
    if kaart['deel'] != vorig_deel:
        kop(doc, kaart['deel'], 1)
        vorig_deel = kaart['deel']
    fiche_uit(doc, nummer, kaart)

paginanummers(doc, 'theorie')
doc.save(THEORIE)
print('geschreven:', THEORIE)


# ==========================================================================
#  3. de twee briefmodellen
# ==========================================================================
def briefhoofd(doc):
    alinea(doc, g.FESTIVAL + ' vzw', vetgedrukt=True, grootte=15, na=0)
    alinea(doc, f'Festivalweg 1  ·  2000 Antwerpen  ·  info@{g.DOMEIN}',
           schuin=True, kleur=GRIJS, grootte=9, na=18)


def briefvoet(doc, extra=None):
    briefregel(doc, 'Met vriendelijke groeten', na=24)
    briefregel(doc, 'Dieter Varey', na=0)
    alinea(doc, g.FESTIVAL + ' vzw', schuin=True, kleur=GRIJS, grootte=9,
           na=0)


# ------------------------------------------- de vrijwilligersbrief (stap 3)
doc = Document()
opzet(doc)
briefhoofd(doc)
briefregel(doc, '[[Voornaam]] [[Achternaam]]')
briefregel(doc, '[[Adresregel]]')
briefregel(doc, '[[Woonplaats]]', na=18)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_after = Pt(18)
p.add_run(f'Antwerpen, {g.datum_lang(g.BRIEFDATUM)}')
briefregel(doc, '[[Aanhef]],', na=12)
briefregel(doc,
           f'Goed nieuws: je bent ingeschreven als vrijwilliger voor '
           f'{g.FESTIVAL} {g.EDITIE}. Het festival loopt van vrijdag '
           f'{g.FESTIVALDAG.day} tot en met zondag {g.FESTIVALDAG.day + 2} '
           f'{g.MAANDNAMEN[g.FESTIVALDAG.month - 1]} {g.EDITIE}.', na=12)
briefregel(doc,
           'Jouw taak is [[Taak]]. We verwachten je op de eerste dag om '
           '[[Startuur]]. Voor een volledige dag krijg je een vergoeding van '
           '[[Vergoeding]].', na=12)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run('— hier komt in stap 4 de regel Als…Dan…Anders —')
r.italic = True
r.font.size = Pt(10)
r.font.color.rgb = ORANJE
briefregel(doc,
           'Breng je identiteitskaart mee. Bij aankomst krijg je een bandje, '
           'een T-shirt en bonnetjes voor eten en drinken. Kan je toch niet '
           f'komen, laat het dan vóór 1 juni weten via info@{g.DOMEIN}.',
           na=12)
briefregel(doc, 'Tot in juli!', na=18)
briefvoet(doc)
doc.add_paragraph()
kader(doc, 'Voor de leerling — lees dit eerst', [
    'Sla dit document eerst op onder je eigen naam: Bestand, Opslaan als, '
    'brief-jouwnaam.docx.',
    'Elke oranje marker tussen dubbele haken vervang je door een '
    'samenvoegveld met dezelfde naam. Verwijder de marker en voeg het veld in '
    'de plaats ervan in. Typ de punthaken van het veld NIET zelf.',
    'De oranje regel in het midden laat je eerst staan. In stap 4 vervang je '
    'die door de regel Als…Dan…Anders.',
    'Dit kader hoort niet in de brief. Verwijder het voor je samenvoegt.',
], ORANJE)
paginanummers(doc, 'briefmodel vrijwilligers')
doc.save(BRIEF_VRIJ)
print('geschreven:', BRIEF_VRIJ)

# ----------------------------------------------- de sponsorbrief (stap 5)
doc = Document()
opzet(doc)
briefhoofd(doc)
for _ in range(3):
    briefregel(doc, '', na=2)
doc.add_paragraph().paragraph_format.space_after = Pt(6)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_after = Pt(18)
p.add_run(f'Antwerpen, {g.datum_lang(g.BRIEFDATUM)}')
briefregel(doc, 'Betreft: uw steun aan ' + g.FESTIVAL + ' ' + str(g.EDITIE),
           na=18, markers=False, vetgedrukt=True)
briefregel(doc, '', na=12)
briefregel(doc,
           f'Dankzij uw steun kan {g.FESTIVAL} ook in {g.EDITIE} doorgaan. '
           'Wij willen u daar graag voor bedanken, en u laten weten wat uw '
           'bijdrage dit jaar mogelijk maakt.', na=12, markers=False)
briefregel(doc,
           'U steunt ons dit jaar met een bijdrage in het pakket dat u gekozen '
           'hebt. Uw naam komt op de affiche, op de schermen naast het podium '
           'en op onze website.', na=12, markers=False)
briefregel(doc, '', na=12)
briefregel(doc,
           'Wij kijken ernaar uit u op het festival te mogen begroeten. Heeft '
           'u vragen over uw pakket, dan mag u ons altijd bellen.',
           na=18, markers=False)
briefvoet(doc)
doc.add_paragraph()
kader(doc, 'Voor de leerling — dit is de eindopdracht', [
    'Sla dit document eerst op onder je eigen naam: sponsorbrief-jouwnaam.docx.',
    'Er staan GEEN markers in. Jij beslist waar de samenvoegvelden horen. '
    'Deze velden moeten er in elk geval in: '
    + ', '.join(o.BRIEF_SPON_VELDEN) + '.',
    'De lege regels bovenaan zijn voor het adres, en de lege regel onder de '
    'betreftregel is voor de aanhef. De twee lege regels in de tekst zijn voor '
    'de zinnen waarin het pakket en het bedrag voorkomen.',
    f'Eén zin komt er alleen bij wie {g.euro(g.SPON_DREMPEL)} of meer geeft: '
    'een uitnodiging voor de sponsoravond. Die zet je met Als…Dan…Anders.',
    'Dit kader hoort niet in de brief. Verwijder het voor je samenvoegt.',
], ORANJE)
paginanummers(doc, 'briefmodel sponsors')
doc.save(BRIEF_SPON)
print('geschreven:', BRIEF_SPON)


# ==========================================================================
#  4. de lerarensleutel
# ==========================================================================
doc = Document()
opzet(doc)
kop(doc, g.TITEL + ' — lerarensleutel', 0)
alinea(doc, g.ONDERTITEL, schuin=True, kleur=GRIJS, na=12)

kop(doc, 'In het kort', 2, GRIJS)
alinea(doc,
       f'Vijf stappen, {g.LESUREN} lesuren, {o.TOTAAL} punten. Eén lesuur per '
       'stap, twee voor de eindopdracht. Stap 1 is Excel, stap 2 tot 4 zijn '
       'Word, stap 5 is allebei.', na=6)
alinea(doc,
       'Nieuw aan Excelkant is er maar één functie: TEKST. De rest is '
       'herhaling — plakken met &, VERT.ZOEKEN, DATUMVERSCHIL en ALS kennen '
       'ze al. Nieuw aan Wordkant is alles.', na=6)
alinea(doc,
       f'De theorie zit in een apart boekje ({o.THEORIEBUNDEL}), zoals bij de '
       f'draaitabellen. Deel dat uit bij stap 1 en laat het liggen: ze hebben '
       'het alle vijf de stappen nodig.', na=10)

punten_tabel(doc)

kader(doc, 'Hoeveel lesuren echt?', [
    f'Op papier {g.LESUREN}. Met deze groep zou ik er {g.LESUREN + 1} voor '
    'inschrijven, en dan is stap 4 het uur dat je kan laten vallen als het '
    'krap wordt: filteren en sorteren is nuttig maar niet nodig om de '
    'eindopdracht te kunnen.',
    'Wat je NIET mag laten vallen is stap 1. Elk probleem in stap 3 komt '
    'daarvandaan. Wie zijn kolom Vergoeding zonder TEKST maakt, krijgt in zijn '
    'brief een kaal getal en begint opnieuw.',
    'Stap 2 is met opzet de eerste Wordstap en niet de brief. Een etiketvel is '
    'korter, de fout is zichtbaarder (alleen het eerste etiket gevuld) en ze '
    'hebben binnen twintig minuten iets af. Dat scheelt voor de moed.',
], BLAUW)

kader(doc, 'Waar het bij iedereen misgaat', [
    '1.  De opmaak van een cel verwarren met de inhoud. In de takentabel staat '
    f'netjes {g.uur(g.TAKEN[0][3])} en {g.euro(g.TAKEN[0][4])}; voeg je die '
    'cel samen, dan staat er in de brief een kommagetal en een kaal getal. Dat '
    'is de hele reden dat stap 1 bestaat. Zet het één keer klassikaal op het '
    'bord en je bespaart jezelf twintig vragen.',
    '2.  Labels bijwerken vergeten in stap 2. Dan is alleen het eerste etiket '
    'gevuld en denken ze dat de lijst niet gelezen is.',
    '3.  De punthaken zelf typen. Het ziet er identiek uit en doet niets. '
    'Herkenbaar: bij Voorbeeld van resultaten verandert er niets. Laat ze erop '
    'klikken — een echt veld wordt grijs.',
    '4.  Het Excelbestand verplaatsen nadat ze het gekoppeld hebben. Zeg bij '
    'het begin van elke les: allebei de bestanden in dezelfde map.',
    '5.  Het filter van stap 4 laten staan. In de eindopdracht komen er dan '
    f'{a.FILTER_AANTAL} brieven uit in plaats van {a.AANTAL_SPON}.',
], ORANJE)

kader(doc, 'Wat je niet automatisch kan nakijken', [
    'De Excelkolommen van stap 1 en 5 kan je cel per cel nalezen; die staan '
    'hieronder volledig uitgeschreven.',
    'De Wordstappen moet je zien. Vraag om het HOOFDdocument én het '
    'samengevoegde document. In het hoofddocument zie je of er echte velden '
    'in zitten (klik erin, het wordt grijs, of druk Alt+F9); in het '
    'samengevoegde document zie je of het resultaat klopt.',
    'Snelle test voor stap 4: zoek in het samengevoegde document op het woord '
    f'"toelating". Dat moet {a.AANTAL_MINDERJARIG} keer voorkomen.',
], BLAUW)

# ------------------------------------------------------------ per stap
for stap in o.STAPPEN:
    paginaeinde(doc)
    uren = 'lesuur' if stap['lesuren'] == 1 else 'lesuren'
    kop(doc, f"Stap {stap['nr']} — {stap['titel']}", 1)
    alinea(doc, f"{stap['waar']}  ·  {stap['lesuren']} {uren}  ·  "
                f"{punten_van(stap)} punten  ·  fiche "
                f"{', '.join(str(n) for n in stap['fiches'])}",
           schuin=True, kleur=GRIJS, na=8)

    if stap.get('vullen'):
        kop(doc, 'De formules', 2, GRIJS)
        tabel(doc, ['Kolom', 'Formule', 'Pt'],
              [[f'{kolom}{g.VRIJ_START if stap["nr"] == 1 else g.SPON_START}',
                formule, punten]
               for kolom, _naam, _wat, formule, punten in stap['vullen']],
              breedtes=[2.0, 13.0, 1.4], vaste_kolommen={1})
        alinea(doc, 'Alleen de bovenste cel hoort getypt te zijn; de rest is '
                    'doorgevoerd. Staat in elke cel hetzelfde rijnummer, dan '
                    'is er gekopieerd in plaats van doorgevoerd en klopt enkel '
                    'de eerste regel.', schuin=True, kleur=GRIJS, na=10)

    if stap.get('stappen'):
        kop(doc, 'De stappen in Word', 2, GRIJS)
        tabel(doc, ['Wat', 'Hoe', 'Pt'],
              [[naam, hoe, punten] for naam, hoe, punten in stap['stappen']],
              breedtes=[4.0, 11.0, 1.4])

    nr = stap['nr']
    if nr == 1:
        kop(doc, 'De acht kolommen, uitgeschreven', 2, GRIJS)
        tabel(doc, ['Naam', 'Aanhef', 'Adresregel', 'Woonplaats', 'Taak',
                    'Uur', 'Vergoeding', 'Lft', 'Beg.'],
              [[v.naam] + v.gemaakt() for v in a.VRIJ], 'Light List Accent 1')
        nipt = '; '.join(f'{v.naam} ({g.datum(v.geboorte)}) is {v.leeftijd}'
                         for v in a.NIPT)
        alinea(doc, f'{a.AANTAL_MINDERJARIG} van de {a.AANTAL_VRIJ} zijn op de '
                    f'festivaldag nog geen {g.MEERDERJARIG}. Twee zitten er '
                    f'bovenop: {nipt}. Eén dag scheelt daar een heel jaar, en '
                    'in stap 4 scheelt het een zin in hun brief.',
               schuin=True, kleur=GRIJS, na=4)
        alinea(doc, f'Totaal aan vergoedingen: {a.TOTALE_VERGOEDING_TEKST}.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 2:
        kop(doc, 'Wat je op het etiketvel verwacht', 2, GRIJS)
        tabel(doc, ['Wat', 'Hoeveel'],
              [['etiketten per blad', g.ETIKET_PER_BLAD],
               ['adressen in de lijst', a.AANTAL_VRIJ],
               ['bladen', a.ETIKET_BLADEN],
               ['gevuld op het laatste blad', a.ETIKET_LAATSTE_BLAD],
               ['leeg op het laatste blad', a.ETIKET_LEEG_OP_LAATSTE]],
              'Light List Accent 1', [8.0, 4.0])
        alinea(doc, f'Het etiketformaat is {g.ETIKET_SOORT}. Staat dat niet in '
                    'hun Word, dan is elk formaat met evenveel etiketten per '
                    'blad goed; laat het dan wel opschrijven, anders kloppen '
                    'de twee eerste antwoorden niet meer.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 3:
        kop(doc, f'Brief 1 — {a.VOORBEELD_EERSTE.naam}', 2, GRIJS)
        tabel(doc, ['Veld', 'Wat erin komt'],
              [[o.marker(m), {
                  'Voornaam': a.VOORBEELD_EERSTE.voornaam,
                  'Achternaam': a.VOORBEELD_EERSTE.achternaam,
                  'Aanhef': a.VOORBEELD_EERSTE.aanhef,
                  'Adresregel': a.VOORBEELD_EERSTE.adresregel,
                  'Woonplaats': a.VOORBEELD_EERSTE.woonplaats,
                  'Taak': a.VOORBEELD_EERSTE.taak,
                  'Startuur': a.VOORBEELD_EERSTE.startuur,
                  'Vergoeding': a.VOORBEELD_EERSTE.vergoeding,
              }[m]] for m in o.BRIEF_VRIJ_MARKERS],
              'Light List Accent 1', [5.0, 10.0])
        alinea(doc, f'Met de RUWE kolommen uit de takentabel zou daar '
                    f'{a.RUW_UUR_TEKST} en {a.RUW_GELD_TEKST} staan. Hoeveel '
                    'cijfers Word achter de komma zet, verschilt per versie; '
                    'het antwoord op het antwoordblad is daarom "een '
                    'kommagetal rond 0,58".', schuin=True, kleur=GRIJS, na=10)
    elif nr == 4:
        kop(doc, 'Wie krijgt de extra zin?', 2, GRIJS)
        tabel(doc, ['Vrijwilliger', 'Leeftijd', 'Begeleiding', 'Podium'],
              [[v.naam, v.leeftijd, v.begeleiding, v.podium] for v in a.VRIJ],
              'Light List Accent 1', [6.0, 2.6, 3.2, 4.2])
        tabel(doc, ['Podium', 'Vrijwilligers'],
              [[p, a.PER_PODIUM[p]] for p in sorted(a.PER_PODIUM)]
              + [['Samen', a.AANTAL_VRIJ]], 'Light List Accent 1',
              [6.0, 4.0])
        alinea(doc, f'Het filter op {g.FILTER_PODIUM} laat '
                    f'{a.FILTER_AANTAL} brieven over. De extra zin staat in '
                    f'{a.AANTAL_MINDERJARIG} brieven.',
               schuin=True, kleur=GRIJS, na=10)
    elif nr == 5:
        kop(doc, 'De vier kolommen en de twaalf brieven', 2, GRIJS)
        tabel(doc, ['Bedrijf', 'Aanhef', 'Adresregel', 'Woonplaats', 'Pakket',
                    'Bedrag', 'Extra zin'],
              [[s.bedrijf, s.aanhef, s.adresregel, s.woonplaats, s.pakket,
                s.bedrag_tekst, 'ja' if s.extra_zin else 'nee']
               for s in a.SPON], 'Light List Accent 1')
        alinea(doc, f'{a.AANTAL_SPON_EXTRA} van de {a.AANTAL_SPON} krijgen de '
                    f'extra zin (bedrag vanaf {g.euro(g.SPON_DREMPEL)}). '
                    f'Totaal: {a.SPON_TOTAAL_TEKST}.',
               schuin=True, kleur=GRIJS, na=4)
        alinea(doc, 'Een vergelijking op een BEDRAG is in Word onbetrouwbaar: '
                    'hij vergelijkt soms als tekst, en dan is "750" groter dan '
                    '"2000". Wie dat tegenkomt, los je op zoals in stap 4: een '
                    'hulpkolom in Excel met ja of nee, en de regel daarop. '
                    'Reken dat niet aan als een fout — het is de betere '
                    'oplossing.', schuin=True, kleur=GRIJS, na=10)

    vragen = [(i, v, antw) for i, (st, v, antw)
              in enumerate(a.ANTWOORDBLAD, 1) if st == nr]
    if vragen:
        kop(doc, 'De antwoorden op het antwoordblad', 2, GRIJS)
        tabel(doc, ['Cel', 'Vraag', 'Antwoord', 'Pt'],
              [[f'{ANTW_KOLOM}{a.ANTW_START + i - 1}', v, antw, 1]
               for i, v, antw in vragen],
              breedtes=[1.6, 8.4, 5.0, 1.4])
    kader(doc, 'Waar je naar kijkt', [stap['controle']], GROEN)

# ------------------------------------------------------------ tijdsindeling
paginaeinde(doc)
kop(doc, 'De zes lesuren', 1)
tabel(doc, ['Lesuur', 'Wat', 'Waar je op let'],
      [['1', 'Stap 1 — de lijst klaarmaken',
        'De kolommen Startuur en Vergoeding. Loop rond en kijk of er een '
        'euroteken staat. Wie dat mist, loopt in lesuur 3 vast.'],
       ['2', 'Stap 2 — etiketten',
        'Labels bijwerken. Doe de eerste samenvoeging klassikaal mee op het '
        'bord; daarna gaat het alleen.'],
       ['3', 'Stap 3 — de brief',
        'Hier valt het kwartje over opmaak tegenover inhoud. Laat één leerling '
        'met opzet het verkeerde veld nemen en toon wat eruit komt.'],
       ['4', 'Stap 4 — regels en filters',
        'Als…Dan…Anders. Vergelijk met de kolom Begeleiding, niet met '
        'Leeftijd. En het filter achteraf weer AF.'],
       ['5', 'Stap 5 — eindopdracht, eerste uur',
        'De vier Excelkolommen en de brief. Wie hier klaar is, heeft het '
        'tweede uur voor de etiketten.'],
       ['6', 'Stap 5 — eindopdracht, tweede uur',
        'De regel, de etiketten en het sorteren. Laat de laatste tien minuten '
        'indienen en nakijken.']],
      breedtes=[1.6, 5.4, 9.4])

kader(doc, 'Differentiëren', [
    'TE SNEL — laat ze de brieven als e-mail samenvoegen in plaats van als '
    'document. Daar heb je een kolom met e-mailadressen voor nodig, en die '
    f'kunnen ze zelf maken: voornaam, punt, achternaam, @{g.DOMEIN}. Dat is '
    'precies de oefening uit de festivalbundel over tekstfuncties. Laat ze '
    'niets echt versturen.',
    'TE SNEL, korter — laat ze een tweede regel toevoegen: wie op het podium '
    'werkt, krijgt een zin over gehoorbescherming.',
    'TE TRAAG — laat stap 4 vallen en ga meteen naar de eindopdracht, zonder '
    'de regel. Dan is het nog altijd een volwaardige samenvoeging: lijst, '
    'brief, velden, etiketten.',
    'TE TRAAG, erger — doe stap 1 klassikaal en deel de afgewerkte lijst uit. '
    'Dan verliezen ze het Excelstuk, maar halen ze wel het Wordstuk, en dat '
    'was hier het doel.',
], BLAUW)

kader(doc, 'Waar dit op voortbouwt', [
    f'Dit is de derde bundel rond {g.FESTIVAL}. In '
    f'{g.ZUSTERBUNDELS[0]} kuisten ze de line-up op met tekstfuncties, in '
    f'{g.ZUSTERBUNDELS[1]} rekenden ze met de planning. Hier gebruiken ze de '
    'lijst waar lijsten voor gemaakt zijn.',
    'Plakken met & komt uit de eerste bundel, DATUMVERSCHIL uit de tweede. Als '
    'ze daar vastlopen, liggen die fiches er nog.',
], BLAUW)

paginanummers(doc, 'lerarensleutel')
doc.save(SLEUTEL)
print('geschreven:', SLEUTEL)
