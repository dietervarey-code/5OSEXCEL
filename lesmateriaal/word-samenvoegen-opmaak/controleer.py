# -*- coding: utf-8 -*-
"""Kijkt na of gegevens, opdracht, theorie, sleutel en briefmodellen passen.

Deze bundel gaat over Word, dus er valt weinig te rekenen. Wat hier bewaakt
wordt, is daarom iets anders:

  1. elk veld dat in een opmaakvoorschrift genoemd wordt, moet een kolom zijn
     die echt in die lijst staat — anders stuurt de opdracht ze naar een veld
     dat Word niet kent;
  2. de briefmodellen moeten ECHT zonder opmaak zijn. Als er al een tabstop,
     een lettergrootte of een uitlijning in zit, is de opmaakoefening weg;
  3. de lessen moeten overeind blijven: een filter dat iets wegfiltert, een
     regel die niet voor iedereen geldt, en etiketbladen die niet precies
     vollopen.
"""
import collections
import datetime
import importlib.util
import os
import re
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')
f = laad('f', 'fiches.py')

FOUTEN, GETELD = [], collections.Counter()


def eis(voorwaarde, bericht):
    if not voorwaarde:
        FOUTEN.append(bericht)
    return bool(voorwaarde)


def doc_tekst(pad):
    d = Document(pad)
    stukken = [p.text for p in d.paragraphs]
    for t in d.tables:
        for rij in t.rows:
            stukken.extend(c.text for c in rij.cells)
    return '\n'.join(stukken)


# ======================================================================
#  1. de gegevens
# ======================================================================
for naam, (trainer, dag, tijd, lidgeld, vervaldatum) in g.PLOEGEN.items():
    eis(naam in g.PLOEGORDE, f'ploeg {naam!r} staat niet in PLOEGORDE')
    eis(trainer and dag, f'ploeg {naam}: onvolledig')
    eis(isinstance(tijd, datetime.time), f'ploeg {naam}: startuur geen tijd')
    eis(lidgeld > 0, f'ploeg {naam}: geen lidgeld')
    eis(isinstance(vervaldatum, datetime.date),
        f'ploeg {naam}: vervaldatum geen datum')
    eis(vervaldatum > g.BRIEFDATUM,
        f'ploeg {naam}: de vervaldatum ligt vóór de briefdatum')
    GETELD['ploegen nagerekend'] += 1
eis(set(g.PLOEGEN) == set(g.PLOEGORDE), 'PLOEGEN en PLOEGORDE lopen uiteen')
eis(len({p[3] for p in g.PLOEGEN.values()}) > 1,
    'elke ploeg heeft hetzelfde lidgeld — dan verschilt de tabel in de brief '
    'niet per lid en merkt niemand of het veld werkt')
eis(len({p[1] for p in g.PLOEGEN.values()}) > 1,
    'elke ploeg traint op dezelfde dag')
eis(any(p[2].minute for p in g.PLOEGEN.values()),
    'elk trainingsuur staat op een heel uur — dan maakt de vorm uu:mm niets '
    'uit op de lidkaart')

for l in a.LEDEN:
    _trainer, _dag, _tijd, _geld, _verval = g.ploeg(l.ploeg)
    eis(l.trainer == _trainer and l.trainingsdag == _dag,
        f'{l.naam}: trainer of dag klopt niet met de ploegtabel')
    eis(l.trainingsuur == g.uur(_tijd), f'{l.naam}: trainingsuur')
    eis(l.lidgeld == _geld and l.lidgeld_tekst == g.euro(_geld),
        f'{l.naam}: lidgeld')
    eis(l.vervaldatum == _verval, f'{l.naam}: vervaldatum')
    eis(l.betaald in ('ja', 'nee'), f'{l.naam}: betaald is {l.betaald!r}')
    eis(l.lidnummer.startswith('L-'), f'{l.naam}: lidnummer {l.lidnummer!r}')
    eis(re.fullmatch(r'\d{4} .+', l.woonplaats), f'{l.naam}: woonplaats')
    eis(l.lidgeld_tekst.startswith('€'), f'{l.naam}: lidgeld zonder euroteken')
    GETELD['leden nagerekend'] += 1
eis(len({l.naam for l in a.LEDEN}) == a.AANTAL_LEDEN, 'twee leden met dezelfde naam')
eis(len({l.lidnummer for l in a.LEDEN}) == a.AANTAL_LEDEN, 'dubbel lidnummer')
eis(len({l.voornaam for l in a.LEDEN}) == a.AANTAL_LEDEN,
    'twee leden met dezelfde voornaam — de aanhef "Beste X" is dan niet '
    'eenduidig')
eis(set(a.PER_PLOEG) == set(g.PLOEGORDE),
    f'niet elke ploeg heeft leden: {sorted(set(g.PLOEGORDE) - set(a.PER_PLOEG))}')

for c in a.CLUBS:
    eis(c.aanspreking in g.TORN_AANSPREKINGEN,
        f'{c.club}: onbekende aanspreking {c.aanspreking!r}')
    eis(c.categorie in g.TORN_CATEGORIEEN,
        f'{c.club}: onbekende categorie {c.categorie!r}')
    eis(c.aantal_ploegen > 0, f'{c.club}: geen ploegen')
    eis(c.geld == c.aantal_ploegen * g.TORN_PER_PLOEG, f'{c.club}: bedrag')
    eis(c.geld_tekst.startswith('€'), f'{c.club}: bedrag zonder euroteken')
    GETELD['clubs nagerekend'] += 1
eis(len({c.club for c in a.CLUBS}) == a.AANTAL_CLUBS, 'dubbele club')
eis(len({c.naam for c in a.CLUBS}) == a.AANTAL_CLUBS,
    'twee contactpersonen met dezelfde achternaam')
eis(len({c.aanspreking for c in a.CLUBS}) == 2,
    'niet beide aansprekingen komen voor — dan is de zakelijke aanhef altijd '
    'hetzelfde')
eis(set(a.PER_CATEGORIE) == set(g.TORN_CATEGORIEEN),
    'niet elke categorie komt voor')

# de hulpjes doen wat Excel doet
eis(g.euro(1250.0) == '€ 1.250,00', f'euro() geeft {g.euro(1250.0)!r}')
eis(g.uur(datetime.time(9, 30)) == '09:30', 'uur() vult niet aan')
eis(g.datum_lang(datetime.date(2027, 1, 15)) == '15 januari 2027',
    f'datum_lang() geeft {g.datum_lang(datetime.date(2027, 1, 15))!r}')

# ======================================================================
#  2. de lessen moeten overeind blijven
# ======================================================================
eis(0 < a.AANTAL_ENVELOPPEN < a.AANTAL_LEDEN,
    f'het filter {g.ENVELOP_FILTER[0]} = {g.ENVELOP_FILTER[1]} laat '
    f'{a.AANTAL_ENVELOPPEN} van de {a.AANTAL_LEDEN} over — dan is er niets '
    'aan te zien')
eis(0 < a.AANTAL_AANMANING < a.AANTAL_BRIEVEN,
    f'de regel geldt voor {a.AANTAL_AANMANING} van de {a.AANTAL_BRIEVEN} '
    'brieven — dan zegt Als…Dan…Anders niets')
eis(a.ETIKET_BLADEN > 1,
    'alle lidkaarten passen op één blad — dan valt er over bladen niets te '
    'vragen')
eis(a.ETIKET_LEEG > 0,
    'de etiketbladen lopen precies vol — dan is de vraag over de lege '
    'kaarten een nulletje')
eis(1 < a.AANTAL_LIJSTRIJEN < a.AANTAL_LEDEN,
    f'de lijst van {g.LIJST_BLAD_PLOEG} heeft {a.AANTAL_LIJSTRIJEN} regels — '
    'dan zegt het filter niets')
eis(0 < a.AANTAL_EXTRA < a.AANTAL_CLUBS,
    f'{a.AANTAL_EXTRA} van de {a.AANTAL_CLUBS} clubs halen de drempel — dan '
    'zegt de regel van de eindopdracht niets')
eis(1 < a.AANTAL_EINDLIJST < a.AANTAL_CLUBS,
    'de lijst van de eindopdracht filtert niets weg')

# ======================================================================
#  3. de opmaakvoorschriften
# ======================================================================
LIJSTKOPPEN = {g.LEDEN_BLAD: g.LEDEN_KOP, g.TORN_BLAD: g.TORN_KOP}

# elk veld in een voorschrift moet een kolom zijn die echt bestaat
def keur_velden(velden, waar, koppen):
    for veld in velden:
        eis(veld in koppen,
            f'{waar}: «{veld}» is geen kolom van die lijst — dat veld bestaat '
            f'straks niet in Word. De kolommen zijn {koppen}')
        GETELD['velden gekeurd'] += 1


for i, regel in enumerate(g.LIDKAART, 1):
    keur_velden(regel['velden'], f'lidkaart regel {i}', g.LEDEN_KOP)
    eis(regel['grootte'] >= 8,
        f'lidkaart regel {i}: {regel["grootte"]} punten is op papier niet '
        'leesbaar (fiche 20 zegt 8 als minimum)')
    eis(regel['inhoud'], f'lidkaart regel {i}: geen inhoud')
    eis(regel['hoe'], f'lidkaart regel {i}: er staat niet wat erin moet komen')
    for veld in regel['velden']:
        eis(f'«{veld}»' in regel['inhoud'],
            f'lidkaart regel {i}: {veld} staat in velden maar niet in de '
            'inhoud')
eis(len(g.LIDKAART) >= 3,
    'minder dan drie regels op de lidkaart — dan is er geen opmaak te doen')
eis(len({r['grootte'] for r in g.LIDKAART}) > 1,
    'alle regels van de lidkaart hebben dezelfde lettergrootte — dan valt er '
    'niets op te maken')
eis(any(r['vet'] for r in g.LIDKAART) and not all(r['vet'] for r in g.LIDKAART),
    'de lidkaart is helemaal vet of helemaal niet vet')
eis(sum(r['grootte'] for r in g.LIDKAART) <= 48,
    f'de vier regels tellen {sum(r["grootte"] for r in g.LIDKAART)} punten '
    'samen; op 38 mm hoogte past dat niet meer')

for i, regel in enumerate(g.ENVELOP_GEADRESSEERDE, 1):
    keur_velden(regel, f'envelop, geadresseerde regel {i}', g.LEDEN_KOP)
eis(g.ENVELOP_AFZENDER_GROOTTE < g.ENVELOP_GEADRESSEERDE_GROOTTE,
    'de afzender op de envelop staat even groot als of groter dan de '
    'geadresseerde')
eis(g.ENVELOP_AFZENDER_GROOTTE >= 8, 'de afzender is kleiner dan 8 punten')
eis(len(g.ENVELOP_AFZENDER) >= 2, 'de afzender is geen adres')
eis(g.ENVELOP_FILTER[0] in g.LEDEN_KOP,
    f'het envelopfilter staat op {g.ENVELOP_FILTER[0]!r}, dat geen kolom is')

keur_velden(g.BRIEF_MARKERS, 'de ledenbrief', g.LEDEN_KOP)
keur_velden([v for _o, v in g.BRIEF_TABEL if v], 'de tabel in de brief',
            g.LEDEN_KOP)
eis(g.BRIEF_REGEL[0] in g.LEDEN_KOP,
    f'de regel van de brief vergelijkt met {g.BRIEF_REGEL[0]!r}, dat geen '
    'kolom is')
eis(any(v and 'tekst' in v for _o, v in g.BRIEF_TABEL),
    'in de tabel van de brief staat geen enkele tekstkolom — dan komt er een '
    'kommagetal in de brief en is de les van het eerste boekje weg')
eis(10 <= g.BRIEF_TABSTOP_CM <= 17,
    f'een tabstop op {g.BRIEF_TABSTOP_CM} cm valt buiten een A4 met gewone '
    'marges')

keur_velden(g.LIJST_KOLOMMEN, 'de ploeglijst', g.LEDEN_KOP)
eis(g.LIJST_SORTEER in g.LEDEN_KOP,
    f'er wordt gesorteerd op {g.LIJST_SORTEER!r}, dat geen kolom is')
eis(g.LIJST_BLAD_PLOEG in g.PLOEGORDE,
    f'de lijstoefening filtert op ploeg {g.LIJST_BLAD_PLOEG!r}, die niet '
    'bestaat')
eis(len(g.LIJST_KOLOMMEN) >= 3, 'de ploeglijst heeft te weinig kolommen')
eis(a.VOORBEELD_LIJST_PLOEG != g.LIJST_BLAD_PLOEG,
    'het voorbeeld in de opdracht toont dezelfde ploeg als de oefening')
eis(len(a.VOORBEELD_LIJST_RIJEN) != a.AANTAL_LIJSTRIJEN,
    'de voorbeeldploeg heeft even veel leden als de oefenploeg — dan is het '
    'antwoord op de vraag naar het aantal regels gratis')
eis(a.VOORBEELD_LIJST_LEDEN[0].achternaam != a.LIJST_EERSTE.achternaam,
    'de bovenste achternaam van het voorbeeld is dezelfde als die van de '
    'oefening')

# ======================================================================
#  4. de opdracht
# ======================================================================
eis(o.TOTAAL == 100, f'de bundel staat op {o.TOTAAL} punten in plaats van 100')
eis(o.LESUREN == g.LESUREN,
    f'de stappen tellen op tot {o.LESUREN} lesuren, gegevens.py zegt '
    f'{g.LESUREN}')
eis([s['nr'] for s in o.STAPPEN] == list(range(1, len(o.STAPPEN) + 1)),
    'de stappen zijn niet doorlopend genummerd')
eis(o.PUNTEN_OPMAAK >= o.TOTAAL // 4,
    f'maar {o.PUNTEN_OPMAAK} van de {o.TOTAAL} punten staan op de opmaak — '
    'en daar gaat deze bundel over')

SOORTEN = {'Etiketten', 'Enveloppen', 'Brieven', 'Lijst', 'Alles samen'}
for stap in o.STAPPEN:
    eis(stap['soort'] in SOORTEN,
        f"stap {stap['nr']}: onbekende soort {stap['soort']!r}")
    eis(stap['lijst'] in LIJSTKOPPEN,
        f"stap {stap['nr']}: lijst {stap['lijst']!r} bestaat niet")
    eis(stap['lesuren'] >= 1, f"stap {stap['nr']}: geen lesuur")
    eis(stap.get('stappen'), f"stap {stap['nr']}: er valt niets samen te voegen")
    eis(stap.get('opmaak'), f"stap {stap['nr']}: er valt niets op te maken")
    for naam, hoe, punten in stap['opmaak']:
        eis(punten > 0, f"stap {stap['nr']}: opmaak {naam!r} zonder punten")
        eis(len(hoe) > 40,
            f"stap {stap['nr']}: het opmaakvoorschrift {naam!r} is te vaag "
            f'({hoe!r}) — er moet in staan hoe precies')
    for n in stap['fiches']:
        eis(f.FICHE_START <= n < f.FICHE_START + len(f.FICHES),
            f"stap {stap['nr']}: fiche {n} staat niet in dit boekje")
    for n in stap['fiches_eerste']:
        eis(n in f.EERSTE,
            f"stap {stap['nr']}: fiche {n} van het eerste boekje is onbekend")
        eis(1 <= n <= f.FICHES_EERSTE_BOEKJE,
            f"stap {stap['nr']}: fiche {n} ligt buiten het eerste boekje")
    GETELD['stappen gekeurd'] += 1

eis(SOORTEN <= {s['soort'] for s in o.STAPPEN},
    f'niet elke soort komt aan bod: '
    f'{sorted(SOORTEN - {s["soort"] for s in o.STAPPEN})}')

verwezen = {n for stap in o.STAPPEN for n in stap['fiches']}
alle = set(range(f.FICHE_START, f.FICHE_START + len(f.FICHES)))
eis(verwezen == alle,
    f'niet naar elke fiche wordt verwezen: {sorted(alle - verwezen)}')
for i, kaart in enumerate(f.FICHES):
    eis(kaart['deel'] in f.DELEN, f"onbekend deel bij {kaart['naam']}")
    eis(kaart.get('wat') and kaart.get('fout'),
        f"fiche {f.nummer(i)} is niet volledig")
    eis(kaart.get('stappen') or kaart.get('uitleg'),
        f"fiche {f.nummer(i)} zegt niet hoe het moet")
    GETELD['fiches gekeurd'] += 1
volgorde = [k['deel'] for k in f.FICHES]
eis(volgorde == sorted(volgorde, key=f.DELEN.index),
    'de fiches van de delen staan door elkaar')
eis(f.FICHE_START == f.FICHES_EERSTE_BOEKJE + 1,
    'de nummering van het tweede boekje sluit niet aan op het eerste')

# elke vraag hoort bij een stap, en geen tekstantwoord staat in de opdracht
_nrs = {s['nr'] for s in o.STAPPEN}
for stap_nr, vraag, antwoord in a.ANTWOORDBLAD:
    eis(stap_nr in _nrs, f'vraag bij stap {stap_nr}, die niet bestaat')
    eis(vraag.endswith('?'), f'geen vraagteken: {vraag!r}')
    eis(antwoord is not None and antwoord != '', f'geen antwoord op {vraag!r}')
    GETELD['vragen gekeurd'] += 1

for stap in o.STAPPEN:
    bronnen = list(stap['inleiding']) + [stap['klaar'], stap['controle']]
    bronnen += list(stap['vast'])
    bronnen += [h for _n, h, _p in stap['stappen']]
    bronnen += [h for _n, h, _p in stap['opmaak']]
    if stap['nr'] == 1:
        bronnen += a.KAART_VOORBEELD
    if stap['nr'] == 2:
        bronnen += a.ENVELOP_VOORBEELD
    if stap['nr'] == 3:
        bronnen += [w for _o, w in a.TABEL_VOORBEELD]
    if stap['nr'] == 4:
        bronnen += [w for rij in a.VOORBEELD_LIJST_RIJEN for w in rij]
        bronnen.append(a.VOORBEELD_LIJST_PLOEG)
    tekst_stap = ' '.join(str(b) for b in bronnen).lower()
    for st, vraag, antwoord in a.ANTWOORDBLAD:
        if st != stap['nr'] or not isinstance(antwoord, str):
            continue
        eis(antwoord.lower() not in tekst_stap,
            f"stap {stap['nr']}: het antwoord {antwoord!r} staat al in de "
            'opdracht zelf te lezen — dan is de vraag gratis')
        GETELD['antwoorden op lekken gekeurd'] += 1

_tekst = collections.defaultdict(list)
for i, (st, vraag, antwoord) in enumerate(a.ANTWOORDBLAD, 1):
    if isinstance(antwoord, str):
        _tekst[antwoord].append(f'rij {a.ANTW_START + i - 1}')
for antwoord, plekken in _tekst.items():
    eis(len(plekken) == 1,
        f'het antwoord {antwoord!r} staat op {len(plekken)} plaatsen: '
        f'{", ".join(plekken)}')

# ======================================================================
#  5. het startbestand
# ======================================================================
WERKBOEK = os.path.join(HIER, o.STARTBESTAND)
LIJSTEN = [
    (g.LEDEN_BLAD, g.LEDEN_KOPRIJ, g.LEDEN_START, g.LEDEN_EIND, g.LEDEN_KOP),
    (g.TORN_BLAD, g.TORN_KOPRIJ, g.TORN_START, g.TORN_EIND, g.TORN_KOP),
    (a.ANTW_BLAD, a.ANTW_KOPRIJ, a.ANTW_START, a.ANTW_EIND, a.ANTW_KOP),
]
eis(os.path.exists(WERKBOEK), 'het startbestand bestaat niet — draai eerst '
                              'maak-startbestand.py')
if os.path.exists(WERKBOEK):
    wb = load_workbook(WERKBOEK)
    eis({x[0] for x in LIJSTEN} <= set(wb.sheetnames),
        f'ontbrekende bladen: '
        f'{sorted({x[0] for x in LIJSTEN} - set(wb.sheetnames))}')

    for ws in wb.worksheets:
        eis(not list(ws.merged_cells.ranges),
            f'{ws.title}: samengevoegde cellen '
            f'({[str(r) for r in ws.merged_cells.ranges][:3]}) — dan kan Word '
            'de lijst niet lezen')
        eis(not list(ws.tables),
            f'{ws.title}: er staat al een tabel in het startbestand')

    for blad, koprij, start, eind, koppen in LIJSTEN:
        if blad not in wb.sheetnames:
            continue
        ws = wb[blad]
        eis(koprij == 1,
            f'{blad}: de koprij staat op rij {koprij}. Word neemt de eerste '
            'gebruikte rij als kolomnamen, dus ze hoort op rij 1')
        for i, titel in enumerate(koppen, start=1):
            eis(ws.cell(row=koprij, column=i).value == titel,
                f'{blad}: koprij verschilt in kolom {get_column_letter(i)} '
                f'({ws.cell(row=koprij, column=i).value!r} in plaats van '
                f'{titel!r})')
        eis(len(set(koppen)) == len(koppen),
            f'{blad}: twee kolommen heten hetzelfde')
        for titel in koppen:
            eis(re.fullmatch(r'[A-Za-z][A-Za-z0-9 ]*', titel),
                f'{blad}: kolomnaam {titel!r} bevat tekens waar Word over '
                'struikelt')
        buiten = [f'{c.coordinate}={c.value!r}' for rij in ws.iter_rows()
                  for c in rij
                  if c.value is not None
                  and not (koprij <= c.row <= eind
                           and 1 <= c.column <= len(koppen))]
        eis(not buiten,
            f'{blad}: er staat iets buiten de lijst ({buiten[:3]}) — dan '
            'leest Word een kolom of een rij mee die er niet bij hoort')
        for rij in range(start, eind + 1):
            eis(ws.cell(row=rij, column=1).value is not None,
                f'{blad}: rij {rij} begint leeg')
        GETELD['lijsten gekeurd'] += 1

    # de ledenlijst staat VOLLEDIG klaar: geen enkele lege cel
    ws = wb[g.LEDEN_BLAD]
    for i, lid in enumerate(a.LEDEN):
        rij = g.LEDEN_START + i
        for k, verwacht in enumerate(lid.rij(), start=1):
            gevonden = ws.cell(row=rij, column=k).value
            if isinstance(verwacht, datetime.date):
                gevonden = gevonden.date() if gevonden else gevonden
            eis(gevonden == verwacht,
                f'{g.LEDEN_BLAD} {get_column_letter(k)}{rij}: {gevonden!r} in '
                f'plaats van {verwacht!r}')
            GETELD['ledencellen nagekeken'] += 1
    # en de ruwe geldkolom is opgemaakt, zodat het verschil met de tekstkolom
    # te zien is
    kol_geld = g.LEDEN_KOP.index('Lidgeld') + 1
    for i in range(len(a.LEDEN)):
        eis(ws.cell(row=g.LEDEN_START + i,
                    column=kol_geld).number_format == g.EURONOTATIE,
            f'{g.LEDEN_BLAD} rij {g.LEDEN_START + i}: de kolom Lidgeld heeft '
            'geen euronotatie — dan ziet de leerling het verschil met de '
            'tekstkolom niet')

    ws = wb[a.ANTW_BLAD]
    kol_antwoord = len(a.ANTW_KOP)
    for i, (stap_nr, vraag, _antwoord) in enumerate(a.ANTWOORDBLAD):
        rij = a.ANTW_START + i
        eis(ws.cell(row=rij, column=1).value == stap_nr,
            f'{a.ANTW_BLAD} rij {rij}: verkeerd stapnummer')
        eis(ws.cell(row=rij, column=2).value == vraag,
            f'{a.ANTW_BLAD} rij {rij}: de vraag wijkt af van antwoorden.py')
        eis(ws.cell(row=rij, column=kol_antwoord).value is None,
            f'{a.ANTW_BLAD} rij {rij}: de antwoordcel is niet leeg')
        GETELD['antwoordcellen leeg'] += 1

# ======================================================================
#  6. de documenten
# ======================================================================
DOCUMENTEN = ['samenvoegen-opmaak-opdracht.docx', o.THEORIEBUNDEL,
              'samenvoegen-opmaak-lerarensleutel.docx',
              g.BRIEF_LEDEN, g.BRIEF_TORNOOI]
for naam in DOCUMENTEN:
    eis(os.path.exists(os.path.join(HIER, naam)),
        f'{naam} bestaat niet — draai eerst maak-documenten.py')

MARKER = re.compile(r'\[\[([^\]]+)\]\]')


def keur_briefmodel(pad, verwachte_markers, naam):
    """Een briefmodel moet markers op de juiste plaats hebben en GEEN opmaak."""
    d = Document(pad)
    tekst = doc_tekst(pad)
    gevonden = set(MARKER.findall(tekst))
    eis(gevonden == set(verwachte_markers),
        f'{naam}: de markers in de brief zijn {sorted(gevonden)}, verwacht '
        f'{sorted(verwachte_markers)}')
    for m in sorted(gevonden):
        eis(m in g.LEDEN_KOP,
            f'{naam}: [[{m}]] is geen kolom van {g.LEDEN_BLAD}')
        GETELD['markers gekeurd'] += 1
    # de brief zelf (niet het kader, dat in een tabel staat) moet kaal zijn
    for i, p in enumerate(d.paragraphs, 1):
        eis(p.alignment in (None, WD_ALIGN_PARAGRAPH.LEFT),
            f'{naam}: alinea {i} is al uitgelijnd — de uitlijning is hun werk')
        eis('\t' not in p.text,
            f'{naam}: alinea {i} bevat al een tab — de tabstop is hun werk')
        for r in p.runs:
            eis(r.font.size is None,
                f'{naam}: alinea {i} heeft al een lettergrootte '
                f'({r.font.size.pt if r.font.size else "?"} pt) — de opmaak '
                'is hun werk')
    eis(not d.tables or len(d.tables) == 1,
        f'{naam}: er staat al een tabel in de brief (buiten het kader) — die '
        'moeten ze zelf maken')
    eis(g.datum_lang(g.BRIEFDATUM) in tekst,
        f'{naam}: de briefdatum staat er niet in')
    eis('opzet' in tekst.lower() or 'zelf' in tekst.lower(),
        f'{naam}: er staat niet bij dat de opmaak hun werk is')
    return tekst


pad = os.path.join(HIER, g.BRIEF_LEDEN)
if os.path.exists(pad):
    keur_briefmodel(pad, g.BRIEF_MARKERS, g.BRIEF_LEDEN)

pad = os.path.join(HIER, g.BRIEF_TORNOOI)
if os.path.exists(pad):
    tekst = keur_briefmodel(pad, [], g.BRIEF_TORNOOI)
    for veld in ['Club', 'Adresregel', 'Woonplaats', 'Categorie',
                 'Aantal ploegen', 'Inschrijvingsgeld in tekst']:
        eis(veld in g.TORN_KOP,
            f'de eindopdracht vraagt veld {veld!r}, dat niet in '
            f'{g.TORN_BLAD} staat')
        eis(veld in tekst,
            f'{g.BRIEF_TORNOOI}: het gevraagde veld {veld!r} staat nergens in '
            'de uitleg bij de brief')
        GETELD['tornooivelden gekeurd'] += 1

pad = os.path.join(HIER, 'samenvoegen-opmaak-opdracht.docx')
if os.path.exists(pad):
    tekst = doc_tekst(pad)
    for naam in (o.STARTBESTAND, o.THEORIEBUNDEL, g.BRIEF_LEDEN,
                 g.BRIEF_TORNOOI, g.VOORGANGER_THEORIE):
        eis(naam in tekst, f'de opdracht noemt {naam} nergens')
        GETELD['verwijzingen gekeurd'] += 1
    eis(str(o.TOTAAL) in tekst, 'de opdracht noemt het totaal niet')
    eis(str(o.PUNTEN_OPMAAK) in tekst,
        'de opdracht zegt niet hoeveel punten er op de opmaak staan')

# ======================================================================
print('=' * 72)
for naam, hoeveel in sorted(GETELD.items()):
    print(f'  {hoeveel:>5}  {naam}')
print('=' * 72)
if FOUTEN:
    print(f'{len(FOUTEN)} PROBLEMEN:')
    for fout in FOUTEN:
        print('  !', fout)
    sys.exit(1)
print('alles past bij elkaar.')
