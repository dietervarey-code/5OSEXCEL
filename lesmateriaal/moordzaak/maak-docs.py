# -*- coding: utf-8 -*-
import importlib.util
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT

spec = importlib.util.spec_from_file_location('m','/tmp/ctrl/moordzaak-data.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

MAP = '/home/user/5OSEXCEL/lesmateriaal/moordzaak/'
BLAUW = RGBColor(0x1F, 0x38, 0x64)

# Bereiken in het startbestand (gegevens beginnen op rij 4).
R_BADGES = f"Badgehouders!$A$4:$C${3 + len(m.BADGES)}"
R_LOG_EIND = 3 + len(m.LOGBOEK)
R_PERS_EIND = 3 + len(m.PERSONEEL)

def opzet(doc):
    s = doc.styles['Normal']
    s.font.name = 'Calibri'; s.font.size = Pt(11)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(1.8)
        sec.left_margin = sec.right_margin = Cm(2.0)

def kop(doc, tekst, niveau=1):
    p = doc.add_heading(tekst, level=niveau)
    for r in p.runs: r.font.color.rgb = BLAUW
    return p

def kader(doc, titel, regels):
    t = doc.add_table(rows=1, cols=1); t.style = 'Table Grid'
    c = t.rows[0].cells[0]
    p = c.paragraphs[0]; r = p.add_run(titel); r.bold = True; r.font.color.rgb = BLAUW
    for regel in regels:
        pp = c.add_paragraph(regel); pp.paragraph_format.space_after = Pt(2)
    doc.add_paragraph()
    return t

# =====================================================================
#  OPGAVE
# =====================================================================
doc = Document(); opzet(doc)
kop(doc, 'Moord in Hotel Astrid')
p = doc.add_paragraph(); r = p.add_run('Zaak 2026-0315 — nacht van 14 op 15 maart 2026')
r.italic = True
doc.add_paragraph('Naam: ............................................    Klas: ..............    Duur: 50 minuten')

kader(doc, 'De zaak', [
    'Om 06:40 vindt kamermeisje Sofie Groen de deur van kamer 312 op een kier.',
    f'In de kamer ligt {m.SLACHTOFFER}, zakenman, overleden.',
    '',
    'Het hotel registreert alles: wie er sliep, wie er werkte, welke deuren opengingen,',
    'welke telefoons gebeld hebben. Dat staat in het startbestand.',
    '',
    'Maar een dossier is meer dan een databank. Op zes momenten vraag je bij je leerkracht',
    'een DOSSIERKAART op. Daarop staan dingen die geen enkel systeem registreert: wat de',
    'wetsdokter vaststelde, wat getuigen zagen, hoe het personeel gekleed gaat.',
    '',
    'Zonder de kaarten geraak je er niet. Zonder Excel ook niet.',
])

kop(doc, 'Fase 1 — Het toneel opbouwen', 2)
doc.add_paragraph('Open moordzaak-startbestand.xlsx en lees het blad Zaakdossier.')
for t in [
    'Sorteer het blad Toegangslogboek chronologisch op Tijdstip, van vroeg naar laat. '
    'Let op: de nacht loopt over middernacht. Daarom staat er een datum bij.',
    'Zet in kolom D de kop "Houder". Haal met VERT.ZOEKEN bij elke badge de naam op uit het blad Badgehouders.',
    'Zet in kolom E de kop "Soort" en haal daar op of het om een gast, personeel of een masterbadge gaat.',
    'Zet rij 3 vast, zodat de koppen in beeld blijven terwijl je scrolt.',
]:
    doc.add_paragraph(t, style='List Number')
kader(doc, '→ Vraag nu KAART A aan je leerkracht', ['Het verslag van de wetsdokter.'])

kop(doc, 'Fase 2 — Wie was er boven?', 2)
for t in [
    'Kaart A geeft je een tijdvak. Zoek alle deuropeningen op de 3e verdieping binnen dat tijdvak. '
    'Gebruik een filter, of markeer ze met voorwaardelijke opmaak.',
    'Noteer op je antwoordblad welke badges dat zijn, en bij wie ze horen.',
    'Eén van die badges hoort bij geen enkele persoon. Welke?',
    'Tel met AANTAL.ALS hoe vaak die badge die nacht in totaal gebruikt is.',
]:
    doc.add_paragraph(t, style='List Number')
kader(doc, '→ Vraag nu KAART B en KAART C', ['Wat er over de kleding geweten is, en het logboek van de portier.'])

kop(doc, 'Fase 3 — Wie had die badge in handen?', 2)
for t in [
    'Kaart C zegt wanneer de masterbadge verdween. Zoek in het toegangslogboek wie in die minuten '
    'de deur van de receptie achterkamer opende.',
    'Noteer alle namen die je vindt. Meer dan één, en dat hoort zo.',
]:
    doc.add_paragraph(t, style='List Number')
kader(doc, '→ Vraag nu KAART D', ['Een alibi. Controleer het zelf in het telefoonlogboek voor je het gelooft.'])

kop(doc, 'Fase 4 — Wie is groot genoeg?', 2)
for t in [
    'Sorteer het blad Personeel op lengte, van groot naar klein.',
    'Kaart A zei hoe groot de dader minstens is. Wie blijft over?',
    'Eén van hen lijkt de beste kandidaat, maar kijk eerst waar zijn badge die nacht was. '
    'Zoek in het logboek wat die badge deed tijdens het tijdvak.',
]:
    doc.add_paragraph(t, style='List Number')
kader(doc, '→ Vraag nu KAART E en KAART F', ['De laatste twee stukken.'])

kop(doc, 'Fase 5 — Het bewijs rondmaken', 2)
for t in [
    'Zoek in het telefoonlogboek het gesprek met kamer 312 van die avond. Wie belde, en hoe lang?',
    'Welke voorwerpen op het blad Voorwerpen wijzen naar jouw verdachte? Er zijn er drie.',
    'Personeel moet badgen om buiten te gaan. Leg het blad Personeel naast het logboek: '
    'wiens shift was al afgelopen, terwijl die persoon nergens bij een uitgang te zien is? '
    'Let op: wie nog aan het werk was, hoort er nog te zijn — en één iemand legt het uit in zijn verklaring.',
    'Vul het Antwoordblad volledig in en noteer je drie sterkste bewijsstukken.',
    'Werk je blad af: geef de beslissende rijen een kleur, maak de kolommen breed genoeg, '
    'zet het blad liggend en zorg dat het op één pagina breed past. Zo geef je het door aan de procureur.',
]:
    doc.add_paragraph(t, style='List Number')

doc.add_paragraph()
kader(doc, 'Waarop je beoordeeld wordt', [
    'Je dader en je bewijs  —  8 punten',
    'Juist gebruik van VERT.ZOEKEN, AANTAL.ALS, sorteren en filteren  —  8 punten',
    'Een verzorgd, printklaar blad  —  4 punten',
])
doc.save(MAP + 'moordzaak-opgave.docx')
print('opgave geschreven')

# =====================================================================
#  LEERKRACHT
# =====================================================================
doc = Document(); opzet(doc)
kop(doc, 'Moord in Hotel Astrid — leerkrachtenbundel')
doc.add_paragraph('Zaak 2026-0315. Werkvorm van 50 minuten, individueel of per twee.')

kader(doc, 'De dader', [
    f'{m.DADER}, hotelmanager.',
    '',
    'Ze belde om 21:38 vanaf toestel 100 (directie) zeven minuten met kamer 312 — een ruzie.',
    'Om 22:03 nam ze de masterbadge uit de receptie achterkamer. Om 23:52 ging ze met die badge',
    'naar de 3e verdieping, om 23:55 kamer 312 binnen, en om 00:04 weer weg.',
    'Ze liet de badge achter onder de kast (V4), verloor een knoop van haar blazer (V1)',
    'en haar agenda in de linnenkast (V3). Ze heeft die nacht nooit uitgebadgd.',
])

kop(doc, 'Tijdsindeling', 2)
t = doc.add_table(rows=1, cols=3); t.style = 'Light Grid Accent 1'
for i, k in enumerate(['Minuten', 'Fase', 'Wat er gebeurt']):
    t.rows[0].cells[i].paragraphs[0].add_run(k).bold = True
for rij in [
    ('0-5',   'Intro',   'Zaak voorstellen, bestand openen, Zaakdossier lezen.'),
    ('5-15',  'Fase 1',  'Sorteren + twee keer VERT.ZOEKEN. Hier zit het meeste Excel-werk.'),
    ('15-25', 'Fase 2',  'Filteren op tijdvak en verdieping. KAART A, dan B en C.'),
    ('25-35', 'Fase 3',  'Wie nam de badge. KAART D, alibi natrekken in het telefoonlogboek.'),
    ('35-43', 'Fase 4',  'Sorteren op lengte. KAART E en F.'),
    ('43-50', 'Fase 5',  'Bewijs rondmaken, antwoordblad, opmaak. Klassikaal ontknopen.'),
]:
    c = t.add_row().cells
    for i, w in enumerate(rij): c[i].text = w
doc.add_paragraph()

kop(doc, 'De bewijsketen, stap voor stap', 2)
for n, (titel, uitleg) in enumerate([
    ('Wie was er op de 3e verdieping tussen 23:40 en 00:20?',
     'B-308 (Ans Vermeulen), B-304 (Karel Six), B-315 (Bram De Smet) en drie keer P-001, de masterbadge.'),
    ('Kaart B sluit de gasten uit.',
     'De donkerblauwe knoop hoort bij directie of receptie. Gasten dragen geen uniform. Blijft: de masterbadge.'),
    ('Kaart C zegt dat die badge gestolen was.',
     'Laatst gebruikt door de portier om 21:58, als vermist gemeld om 22:15. Iemand nam hem daartussen.'),
    ('Wie opende de receptie achterkamer tussen 21:58 en 22:15?',
     'Greet Coucke (22:03), Ilse Verbeke (22:07) en Wim Deprez (22:11).'),
    ('Kaart D schrapt Ilse Verbeke.',
     'Zij stond aan de balie. Te controleren in het telefoonlogboek: kamer 304 belt om 23:50, kamer 210 om 00:10, '
     'allebei beantwoord. De verklaringen bevestigen het.'),
    ('Kaart A schrapt Wim Deprez.',
     'De dader is minstens 1m85. Wim Deprez is 1m74. Greet Coucke is 1m87 — zij blijft over.'),
    ('Tom Vandaele lijkt verdacht (1m91), maar valt af.',
     'Zijn eigen badge P-004 opent om 23:55 en 00:02 de technische ruimte in de kelder. Hij kan niet boven zijn.'),
    ('Kaart E en F bevestigen.',
     'Alleen Greet Coucke en Rachid El Amrani zijn linkshandig; Rachid zat de hele nacht in de kelder.'),
], start=1):
    p = doc.add_paragraph(style='List Number')
    r = p.add_run(titel); r.bold = True
    doc.add_paragraph(uitleg)

kop(doc, 'Bevestigend bewijs in de werkmap', 2)
for r in [
    'Telefoon 21:38 — toestel 100 (directie) belt kamer 312, zeven minuten.',
    'V1 — donkerblauwe knoop in kamer 312.',
    'V3 — zakagenda met initialen G.C. in de linnenkast van de 3e verdieping.',
    'V4 — de masterbadge P-001 zelf, onder de kast in kamer 312.',
    'Vier personeelsleden badgen niet uit, maar drie ervan verklaren zich: Ilse Verbeke werkte tot 06:00, '
    'Sofie Groen kwam pas om 06:02 toe, Wim Deprez zegt in zijn verklaring dat hij bleef opruimen. '
    'Blijft over: Greet Coucke, wier shift om 22:30 eindigde en die daarna nooit meer geregistreerd wordt '
    'bij een uitgang. Ze is het gebouw nooit uit geweest.',
]:
    doc.add_paragraph(r, style='List Bullet')

kop(doc, 'Valse sporen (bewust ingebouwd)', 2)
for r in [
    'Bram De Smet komt om 00:07 binnen en om 00:09 zijn kamer in — hij was naar de nachtwinkel, bonnetje V7 om 00:03.',
    'Karel Six gaat om 23:43 nog eens buiten en komt terug — hij belde om 23:50 de receptie voor een deken.',
    'Ans Vermeulen komt om 23:36 binnen, gewoon naar bed.',
    'Tom Vandaele is de langste van het personeel en zijn masterbadge is gebruikt. Zijn alibi zit in het logboek.',
]:
    doc.add_paragraph(r, style='List Bullet')

kop(doc, 'Formules die de leerlingen nodig hebben', 2)
t = doc.add_table(rows=1, cols=2); t.style = 'Light Grid Accent 1'
for i, k in enumerate(['Waarvoor', 'Formule']):
    t.rows[0].cells[i].paragraphs[0].add_run(k).bold = True
for waarvoor, formule in [
    ('Naam bij de badge (kolom D)', f'=VERT.ZOEKEN(B4;{R_BADGES};2;ONWAAR)'),
    ('Soort badge (kolom E)', f'=VERT.ZOEKEN(B4;{R_BADGES};3;ONWAAR)'),
    ('Hoe vaak is de masterbadge gebruikt', f'=AANTAL.ALS($B$4:$B${R_LOG_EIND};"P-001")'),
    ('Hoe vaak komt een naam voor', f'=AANTAL.ALS($D$4:$D${R_LOG_EIND};"Greet Coucke")'),
    ('Groter dan 1m85 aanduiden', f'=ALS(F4>=185;"verdacht";"")   (blad Personeel, F4:F{R_PERS_EIND})'),
]:
    c = t.add_row().cells
    c[0].text = waarvoor
    p = c[1].paragraphs[0]; r = p.add_run(formule); r.font.name = 'Consolas'; r.font.size = Pt(9)
doc.add_paragraph()
doc.add_paragraph('Het antwoord op vraag 1 van het antwoordblad: '
                  f'{len(m.LOGBOEK)} deuropeningen. De masterbadge P-001 is '
                  f'{sum(1 for _, b, _ in m.LOGBOEK if b == "P-001")} keer gebruikt.')

# --- De kaarten, op een eigen pagina ---------------------------------
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
kop(doc, 'Dossierkaarten — afdrukken en uitknippen')
doc.add_paragraph('Geef elke kaart pas op het moment dat de opgave erom vraagt. '
                  'Dat is wat de spanning erin houdt.')

KAARTEN = [
    ('KAART A — Verslag van de wetsdokter', [
        'Tijdstip van overlijden: tussen 23:40 en 00:20.',
        'De slag kwam van boven naar beneden. De dader is minstens 1 m 85.',
        'Aan de hoek van de slag te zien hield de dader het voorwerp in de LINKERhand.',
    ]),
    ('KAART B — Kleding', [
        'De donkerblauwe knoop uit kamer 312 komt van een uniformblazer.',
        'In Hotel Astrid dragen alleen de directie en de receptie donkerblauw.',
        'Gasten dragen geen uniform. Keuken en technische dienst dragen grijs.',
    ]),
    ('KAART C — Logboek van de portier', [
        'Tom Vandaele gebruikte de masterbadge die avond voor het laatst om 21:58.',
        'Om 22:15 meldde hij aan de receptie dat de badge weg was.',
        'De badge lag tot dan in de receptie achterkamer, in de lade.',
    ]),
    ('KAART D — Alibi van de receptie', [
        'Ilse Verbeke verliet de balie tussen 22:00 en 00:30 geen enkel moment.',
        'Twee gasten bevestigen dat: ze belden de receptie en kregen haar meteen aan de lijn.',
        'Controleer dat zelf in het telefoonlogboek voor je haar schrapt.',
    ]),
    ('KAART E — Wat een getuige zag', [
        'Een gast zag die avond iemand van het personeel een glas vasthouden met de linkerhand.',
        'Van het voltallige personeel zijn er maar twee linkshandig:',
        'Greet Coucke en Rachid El Amrani.',
    ]),
    ('KAART F — Werkbriefje technische dienst', [
        'Rachid El Amrani werkte die nacht aan de verwarmingsketel in de kelder.',
        'Hij kwam er tussen 23:00 en 01:00 niet weg.',
        'Zijn badge komt die nacht op geen enkele verdieping voor.',
    ]),
]
for titel, regels in KAARTEN:
    kader(doc, titel, regels)

doc.save(MAP + 'moordzaak-leerkracht.docx')
print('leerkrachtenbundel geschreven')
