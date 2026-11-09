# -*- coding: utf-8 -*-
"""Kijkt na of gegevens, opdracht, theorie, sleutel en briefmodellen passen.

Twee dingen krijgen hier extra aandacht:
  1. het startbestand moet SAMENVOEGKLAAR zijn — één koprij, geen
     samengevoegde cellen, geen lege rij in een lijst. Zonder dat werkt de
     hele bundel niet;
  2. elke [[marker]] in het briefmodel moet een kolom zijn die echt in de
     lijst staat, en elke marker uit de opdracht moet echt in de brief staan.
     Anders stuurt de opdracht ze naar een veld dat niet bestaat.
"""
import collections
import datetime
import importlib.util
import os
import re
import sys
from docx import Document
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
    """Alle tekst van een docx op één hoop: alinea's én tabelcellen."""
    d = Document(pad)
    stukken = [p.text for p in d.paragraphs]
    for t in d.tables:
        for rij in t.rows:
            stukken.extend(c.text for c in rij.cells)
    return '\n'.join(stukken)


# ======================================================================
#  1. de gegevens
# ======================================================================
eis(g.FESTIVALDAG.weekday() == 4,
    f'de eerste festivaldag {g.FESTIVALDAG} is geen vrijdag maar een '
    f'{["ma", "di", "wo", "do", "vr", "za", "zo"][g.FESTIVALDAG.weekday()]}dag')
eis(g.BRIEFDATUM < g.FESTIVALDAG,
    'de brief is gedateerd na het festival waarvoor ze uitnodigt')

_codes = [r[0] for r in g.TAKEN]
eis(len(set(_codes)) == len(_codes), 'dubbele taakcode')
for code, taaknaam, podium, startuur, vergoeding in g.TAKEN:
    eis(re.fullmatch(r'T\d{2}', code), f'taakcode {code!r} wijkt af van Tnn')
    eis(taaknaam and podium, f'onvolledige taak bij {code}')
    eis(isinstance(startuur, datetime.time), f'{code}: startuur is geen tijd')
    eis(vergoeding > 0, f'{code}: geen vergoeding')
    GETELD['taken nagerekend'] += 1
# zonder minuten die niet nul zijn, valt de les over uu:mm half weg
eis(any(r[3].minute for r in g.TAKEN),
    'elk startuur staat op een heel uur — dan maakt de vorm uu:mm weinig uit')
# en zonder een bedrag over duizend ziet niemand het duizendpunt
eis(any(r[4] >= 1000 for r in g.TAKEN) or
    any(r[9] >= 1000 for r in g.SPONSORS),
    'nergens een bedrag van duizend of meer — dan leert #.##0,00 niets')

for rij in g.VRIJWILLIGERS:
    (voornaam, achternaam, straat, nummer, postcode, gemeente, geboorte,
     taakcode) = rij
    eis(voornaam and achternaam, f'onvolledige naam: {rij}')
    eis(straat and nummer > 0, f'{voornaam} {achternaam}: onvolledig adres')
    eis(1000 <= postcode <= 9999,
        f'{voornaam} {achternaam}: postcode {postcode} is geen vier cijfers')
    eis(gemeente, f'{voornaam} {achternaam}: geen gemeente')
    eis(isinstance(geboorte, datetime.date),
        f'{voornaam} {achternaam}: geboortedatum is geen datum')
    g.taak(taakcode)        # faalt luid bij een onbekende code
    GETELD['vrijwilligers nagerekend'] += 1
eis(len({f'{r[0]} {r[1]}' for r in g.VRIJWILLIGERS}) == len(g.VRIJWILLIGERS),
    'twee vrijwilligers met dezelfde naam')
eis(len({r[0] for r in g.VRIJWILLIGERS}) == len(g.VRIJWILLIGERS),
    'twee vrijwilligers met dezelfde voornaam — de aanhef "Beste X" is dan '
    'niet eenduidig en de brieven zijn niet van elkaar te onderscheiden')
eis(0 < a.AANTAL_MINDERJARIG < a.AANTAL_VRIJ,
    f'{a.AANTAL_MINDERJARIG} van de {a.AANTAL_VRIJ} zijn minderjarig — dan '
    'zegt de regel van stap 4 niets')
eis(len(a.NIPT) >= 2,
    'niemand is vlak voor of vlak na de festivaldag jarig — dan verdwijnt de '
    'les over hele jaren')
eis(len(a.PER_PODIUM) >= 3, 'te weinig podia om op te filteren')
eis(0 < a.FILTER_AANTAL < a.AANTAL_VRIJ,
    f'het filter op {g.FILTER_PODIUM} laat {a.FILTER_AANTAL} van de '
    f'{a.AANTAL_VRIJ} over — dan is er niets aan te zien')

for rij in g.SPONSORS:
    (bedrijf, voornaam, naam, aanspreking, straat, nummer, postcode,
     gemeente, pakket, bedrag) = rij
    eis(bedrijf and voornaam and naam, f'onvolledige sponsor: {bedrijf}')
    eis(aanspreking in g.SPON_AANSPREKINGEN,
        f'{bedrijf}: onbekende aanspreking {aanspreking!r}')
    eis(pakket in g.SPON_PAKKETTEN, f'{bedrijf}: onbekend pakket {pakket!r}')
    eis(1000 <= postcode <= 9999, f'{bedrijf}: postcode {postcode}')
    eis(bedrag > 0, f'{bedrijf}: geen bedrag')
    GETELD['sponsors nagerekend'] += 1
eis(len({r[0] for r in g.SPONSORS}) == len(g.SPONSORS), 'dubbele sponsor')
eis(0 < a.AANTAL_SPON_EXTRA < a.AANTAL_SPON,
    f'{a.AANTAL_SPON_EXTRA} van de {a.AANTAL_SPON} sponsors halen de drempel '
    f'{g.SPON_DREMPEL} — dan zegt de regel van de eindopdracht niets')
eis(len(set(g.SPON_AANSPREKINGEN)) == 2
    and len({r[3] for r in g.SPONSORS}) == 2,
    'niet beide aansprekingen komen voor — dan is de zakelijke aanhef van de '
    'eindopdracht altijd hetzelfde')

# de twee hulpjes moeten doen wat Excel doet
eis(g.euro(1250.0) == '€ 1.250,00', f'euro() geeft {g.euro(1250.0)!r}')
eis(g.euro(45.0) == '€ 45,00', f'euro() geeft {g.euro(45.0)!r}')
eis(g.uur(datetime.time(9, 30)) == '09:30', 'uur() vult niet aan tot twee cijfers')
eis(g.leeftijd_op(datetime.date(2009, 7, 16), g.FESTIVALDAG) == 18,
    'wie op de festivaldag jarig is, hoort al 18 te zijn')
eis(g.leeftijd_op(datetime.date(2009, 7, 17), g.FESTIVALDAG) == 17,
    'wie de dag na de festivaldag jarig is, hoort nog 17 te zijn')

# ======================================================================
#  2. de antwoorden, langs een tweede weg
# ======================================================================
for v in a.VRIJ:
    _c, taaknaam, podium, startuur, vergoeding = g.taak(v.taakcode)
    eis(v.taak == taaknaam and v.podium == podium, f'{v.naam}: taak klopt niet')
    eis(v.startuur == startuur.strftime('%H:%M'),
        f'{v.naam}: startuur klopt niet')
    eis(v.vergoeding.startswith('€'), f'{v.naam}: vergoeding zonder euroteken')
    eis(v.adresregel == f'{v.straat} {v.nummer}', f'{v.naam}: adresregel')
    eis(v.woonplaats == f'{v.postcode} {v.gemeente}', f'{v.naam}: woonplaats')
    eis(v.aanhef.startswith('Beste '), f'{v.naam}: aanhef')
    eis((v.begeleiding == 'ja') == (v.leeftijd < g.MEERDERJARIG),
        f'{v.naam}: begeleiding klopt niet met de leeftijd')
    GETELD['kolomwaarden nagerekend'] += 8
eis(a.AANTAL_MINDERJARIG == sum(1 for v in a.VRIJ if v.leeftijd < g.MEERDERJARIG),
    'AANTAL_MINDERJARIG klopt niet')
eis(a.ETIKET_BLADEN * g.ETIKET_PER_BLAD >= a.AANTAL_VRIJ,
    'er passen minder etiketten op de bladen dan er adressen zijn')
eis(a.ETIKET_LAATSTE_BLAD + a.ETIKET_LEEG_OP_LAATSTE == g.ETIKET_PER_BLAD,
    'het laatste etiketblad telt niet op')
for s in a.SPON:
    eis(s.aanhef == f'Geachte {s.aanspreking} {s.naam}', f'{s.bedrijf}: aanhef')
    eis(s.bedrag_tekst.startswith('€'), f'{s.bedrijf}: bedrag zonder euroteken')
    eis(s.extra_zin == (s.bedrag >= g.SPON_DREMPEL),
        f'{s.bedrijf}: extra zin klopt niet met het bedrag')
    GETELD['kolomwaarden nagerekend'] += 4

# elke vraag op het antwoordblad hoort bij een stap die bestaat
_stapnummers = {stap['nr'] for stap in o.STAPPEN}
for stap, vraag, antwoord in a.ANTWOORDBLAD:
    eis(stap in _stapnummers, f'vraag bij stap {stap}, die niet bestaat')
    eis(vraag and vraag.endswith('?'), f'geen vraagteken: {vraag!r}')
    eis(antwoord is not None and antwoord != '',
        f'geen antwoord op {vraag!r}')
    GETELD['vragen gekeurd'] += 1
# geen twee keer hetzelfde tekstantwoord: dan kan je het ergens anders aflezen
_tekst = collections.defaultdict(list)
for i, (stap, vraag, antwoord) in enumerate(a.ANTWOORDBLAD, 1):
    if isinstance(antwoord, str):
        _tekst[antwoord].append(f'rij {a.ANTW_START + i - 1}')
for antwoord, plekken in _tekst.items():
    eis(len(plekken) == 1,
        f'het antwoord {antwoord!r} staat op {len(plekken)} plaatsen: '
        f'{", ".join(plekken)}')

# ======================================================================
#  3. de opdracht
# ======================================================================
eis(o.TOTAAL == 100, f'de bundel staat op {o.TOTAAL} punten in plaats van 100')
eis(o.LESUREN == g.LESUREN,
    f'de stappen tellen op tot {o.LESUREN} lesuren, gegevens.py zegt '
    f'{g.LESUREN}')
eis([stap['nr'] for stap in o.STAPPEN] == list(range(1, len(o.STAPPEN) + 1)),
    'de stappen zijn niet doorlopend genummerd')

FUNCTIE = re.compile(r'\b([A-Z][A-Z.]{2,})\(')
BEKEND_ELDERS = {'ALS', 'DATUMVERSCHIL'}     # uit de festivalbundels
geleerd = {naam for kaart in f.FICHES for naam in kaart['functies']}
gebruikt = set()
koppen_van = {g.VRIJ_BLAD: g.VRIJ_KOP, g.SPON_BLAD: g.SPON_KOP}
start_van = {g.VRIJ_BLAD: g.VRIJ_START, g.SPON_BLAD: g.SPON_START}

for stap in o.STAPPEN:
    eis(stap['fiches'], f"stap {stap['nr']}: geen verwijzing naar de theorie")
    for n in stap['fiches']:
        eis(1 <= n <= len(f.FICHES),
            f"stap {stap['nr']}: fiche {n} bestaat niet")
    eis(stap['lesuren'] >= 1, f"stap {stap['nr']}: geen lesuur")
    eis(stap.get('vullen') or stap.get('stappen'),
        f"stap {stap['nr']}: er valt niets te doen")
    for kolom, naam, _wat, formule, _p in stap.get('vullen', []):
        koppen = koppen_van[stap['blad']]
        eis(naam in koppen,
            f"stap {stap['nr']}: kolom {naam!r} staat niet in de koprij")
        eis(get_column_letter(koppen.index(naam) + 1) == kolom,
            f"stap {stap['nr']}: {naam!r} hoort in kolom "
            f"{get_column_letter(koppen.index(naam) + 1)}, niet in {kolom}")
        gebruikt |= set(FUNCTIE.findall(formule))
        # de formule hoort in de bovenste gegevensrij te staan
        rij = start_van[stap['blad']]
        losse = {int(x) for x in re.findall(r'(?<!\$)\b[A-Z]{1,2}(\d+)', formule)}
        eis(losse <= {rij},
            f"stap {stap['nr']} kolom {kolom}: de formule verwijst naar rij "
            f"{sorted(losse)} in plaats van naar rij {rij}")
        eis(f'{kolom}{rij}' not in formule,
            f"stap {stap['nr']} kolom {kolom}: de formule verwijst naar "
            'zichzelf')
        # een bedrag of een uur in de brief moet door TEKST
        if naam in ('Startuur', 'Vergoeding', 'Bedrag in tekst'):
            eis(formule.startswith('=TEKST('),
                f"stap {stap['nr']} kolom {naam}: zonder TEKST komt de opmaak "
                'niet mee naar Word — dat is de hele les van stap 1')
        GETELD['formules gekeurd'] += 1
    GETELD['stappen gekeurd'] += 1

eis(gebruikt <= geleerd | BEKEND_ELDERS,
    f'de opdracht gebruikt functies zonder fiche: '
    f'{sorted(gebruikt - geleerd - BEKEND_ELDERS)}')
for kaart in f.FICHES:
    if kaart['functies']:
        eis(set(kaart['functies']) & gebruikt,
            f"fiche {kaart['naam']} leert iets dat nergens gebruikt wordt")

verwezen = {n for stap in o.STAPPEN for n in stap['fiches']}
eis(verwezen == set(range(1, len(f.FICHES) + 1)),
    f'niet naar elke fiche wordt verwezen: '
    f'{sorted(set(range(1, len(f.FICHES) + 1)) - verwezen)}')
for kaart in f.FICHES:
    eis(kaart['deel'] in f.DELEN, f"onbekend deel bij {kaart['naam']}")
    eis(kaart.get('wat') and kaart.get('fout'),
        f"fiche {kaart['naam']} is niet volledig")
    eis(kaart.get('schrijf') or kaart.get('stappen') or kaart.get('uitleg'),
        f"fiche {kaart['naam']} zegt niet hoe het moet")
    GETELD['fiches gekeurd'] += 1
volgorde = [k['deel'] for k in f.FICHES]
eis(volgorde == sorted(volgorde, key=f.DELEN.index),
    'de fiches van de drie delen staan door elkaar')

# geen theorie in de opdracht
VERBODEN = ['tabblad verzendlijsten, afdruk samenvoegen starten, etiketten.'
            ' kies']
tekst_opdracht = ' '.join(r for stap in o.STAPPEN
                          for r in stap['inleiding']).lower()
for woord in VERBODEN:
    eis(woord not in tekst_opdracht,
        f'de opdracht legt theorie uit ("{woord}")')

# ======================================================================
#  4. het startbestand
# ======================================================================
WERKBOEK = os.path.join(HIER, o.STARTBESTAND)
LIJSTEN = [
    (g.VRIJ_BLAD, g.VRIJ_KOPRIJ, g.VRIJ_START, g.VRIJ_EIND, g.VRIJ_KOP,
     g.VRIJ_KLAAR),
    (g.TAKEN_BLAD, g.TAKEN_KOPRIJ, g.TAKEN_START, g.TAKEN_EIND, g.TAKEN_KOP,
     len(g.TAKEN_KOP)),
    (g.SPON_BLAD, g.SPON_KOPRIJ, g.SPON_START, g.SPON_EIND, g.SPON_KOP,
     g.SPON_KLAAR),
    (a.ANTW_BLAD, a.ANTW_KOPRIJ, a.ANTW_START, a.ANTW_EIND, a.ANTW_KOP,
     len(a.ANTW_KOP) - 1),
]
eis(os.path.exists(WERKBOEK), 'het startbestand bestaat niet — draai eerst '
                              'maak-startbestand.py')
if os.path.exists(WERKBOEK):
    wb = load_workbook(WERKBOEK)
    eis({x[0] for x in LIJSTEN} <= set(wb.sheetnames),
        f'ontbrekende bladen: '
        f'{sorted({x[0] for x in LIJSTEN} - set(wb.sheetnames))}')

    # SAMENVOEGKLAAR: nergens een samengevoegde cel, in geen enkel blad
    for ws in wb.worksheets:
        eis(not list(ws.merged_cells.ranges),
            f'{ws.title}: er staan samengevoegde cellen in '
            f'({[str(r) for r in ws.merged_cells.ranges][:3]}) — dan kan Word '
            'de lijst niet lezen')
        eis(not list(ws.tables),
            f'{ws.title}: er staat al een tabel in het startbestand')

    for blad, koprij, start, eind, koppen, klaar in LIJSTEN:
        if blad not in wb.sheetnames:
            continue
        ws = wb[blad]
        for i, titel in enumerate(koppen, start=1):
            eis(ws.cell(row=koprij, column=i).value == titel,
                f'{blad}: koprij verschilt in kolom {get_column_letter(i)} '
                f'({ws.cell(row=koprij, column=i).value!r} in plaats van '
                f'{titel!r})')
        eis(len(set(koppen)) == len(koppen),
            f'{blad}: twee kolommen heten hetzelfde — Word kan ze dan niet '
            'onderscheiden')
        for titel in koppen:
            eis(re.fullmatch(r'[A-Za-z][A-Za-z0-9 ]*', titel),
                f'{blad}: kolomnaam {titel!r} bevat tekens waar Word over '
                'struikelt')
        # de koprij IS de eerste rij: Word neemt de eerste gebruikte rij
        # van een blad als kolomnamen, dus er mag niets boven staan
        eis(koprij == 1,
            f'{blad}: de koprij staat op rij {koprij}. Word neemt de eerste '
            'gebruikte rij als kolomnamen, dus de koprij hoort op rij 1')
        # en er staat niets BUITEN de lijst: geen titel, geen voetnoot, geen
        # losse cel rechts van de laatste kolom
        buiten = [f'{c.coordinate}={c.value!r}' for rij in ws.iter_rows()
                  for c in rij
                  if c.value is not None
                  and not (koprij <= c.row <= eind
                           and 1 <= c.column <= len(koppen))]
        eis(not buiten,
            f'{blad}: er staat iets buiten de lijst ({buiten[:3]}) — dan leest '
            'Word een kolom of een rij mee die er niet bij hoort')
        # geen lege rij in de lijst, en niets eronder
        for rij in range(start, eind + 1):
            eis(any(ws.cell(row=rij, column=c).value is not None
                    for c in range(1, klaar + 1)),
                f'{blad}: rij {rij} is leeg in de kolommen die klaarstaan')
        for kolom in range(1, len(koppen) + 1):
            eis(ws.cell(row=eind + 1, column=kolom).value is None,
                f'{blad}: er staat iets op rij {eind + 1}, direct onder de '
                'lijst')
        # de klaarstaande kolommen zijn gevuld, de te maken kolommen leeg
        for kolom in range(1, len(koppen) + 1):
            heeft = any(ws.cell(row=r, column=kolom).value is not None
                        for r in range(start, eind + 1))
            eis(heeft == (kolom <= klaar),
                f'{blad}: kolom {get_column_letter(kolom)} '
                f'({koppen[kolom - 1]}) is '
                f'{"gevuld" if heeft else "leeg"} terwijl ze '
                f'{"leeg" if kolom > klaar else "gevuld"} hoort te zijn')
        GETELD['lijsten gekeurd'] += 1

    # de peildatum staat op het blad Start, waar Word niet komt
    eis(g.START_BLAD in wb.sheetnames,
        f'het blad {g.START_BLAD} ontbreekt — daar staat de peildatum')
    if g.START_BLAD in wb.sheetnames:
        ws = wb[g.START_BLAD]
        c = ws.cell(row=g.PEILRIJ, column=g.PEILKOLOM)
        eis(isinstance(c.value, datetime.datetime)
            and c.value.date() == g.FESTIVALDAG,
            f'{g.START_BLAD}: op '
            f'{get_column_letter(g.PEILKOLOM)}{g.PEILRIJ} staat {c.value!r} '
            f'in plaats van de peildatum {g.FESTIVALDAG}')
        eis(ws.cell(row=g.PEILRIJ, column=1).value == g.PEIL_LABEL,
            f'{g.START_BLAD}: er staat geen label bij de peildatum')
        eis(g.PEILCEL == f'{g.START_BLAD}!'
                         f'${get_column_letter(g.PEILKOLOM)}${g.PEILRIJ}',
            f'PEILCEL ({g.PEILCEL}) wijst niet naar de cel waar de peildatum '
            'echt staat')

    # de takentabel moet opgemaakt zijn, want dat is de valkuil van stap 1
    ws = wb[g.TAKEN_BLAD]
    for i in range(len(g.TAKEN)):
        rij = g.TAKEN_START + i
        eis(ws.cell(row=rij, column=4).number_format == g.UURNOTATIE,
            f'Taken rij {rij}: het startuur heeft geen uurnotatie — dan ziet '
            'de leerling het verschil tussen opmaak en inhoud niet')
        eis(ws.cell(row=rij, column=5).number_format == g.EURONOTATIE,
            f'Taken rij {rij}: de vergoeding heeft geen euronotatie')
        GETELD['opmaak nagekeken'] += 2

    # het antwoordblad: vragen gevuld, antwoordkolom leeg
    ws = wb[a.ANTW_BLAD]
    kolom_antwoord = len(a.ANTW_KOP)
    for i, (stap, vraag, _antwoord) in enumerate(a.ANTWOORDBLAD):
        rij = a.ANTW_START + i
        eis(ws.cell(row=rij, column=1).value == stap,
            f'{a.ANTW_BLAD} rij {rij}: verkeerd stapnummer')
        eis(ws.cell(row=rij, column=2).value == vraag,
            f'{a.ANTW_BLAD} rij {rij}: de vraag wijkt af van antwoorden.py')
        eis(ws.cell(row=rij, column=kolom_antwoord).value is None,
            f'{a.ANTW_BLAD} rij {rij}: de antwoordcel is niet leeg')
        GETELD['antwoordcellen leeg'] += 1

    # de lijst die Word straks leest, moet evenveel rijen hebben als de bron
    ws = wb[g.VRIJ_BLAD]
    gevonden = sum(1 for r in range(g.VRIJ_START, g.VRIJ_EIND + 1)
                   if ws.cell(row=r, column=1).value)
    eis(gevonden == len(g.VRIJWILLIGERS),
        f'{g.VRIJ_BLAD}: {gevonden} rijen in plaats van '
        f'{len(g.VRIJWILLIGERS)}')

# ======================================================================
#  5. de documenten
# ======================================================================
DOCUMENTEN = ['samenvoegen-opdracht.docx', o.THEORIEBUNDEL,
              'samenvoegen-lerarensleutel.docx', o.BRIEF_VRIJ, o.BRIEF_SPON]
for naam in DOCUMENTEN:
    eis(os.path.exists(os.path.join(HIER, naam)),
        f'{naam} bestaat niet — draai eerst maak-documenten.py')

MARKER = re.compile(r'\[\[([^\]]+)\]\]')
pad_vrij = os.path.join(HIER, o.BRIEF_VRIJ)
if os.path.exists(pad_vrij):
    tekst = doc_tekst(pad_vrij)
    in_brief = set(MARKER.findall(tekst))
    verwacht = set(o.BRIEF_VRIJ_MARKERS)
    eis(in_brief == verwacht,
        f'{o.BRIEF_VRIJ}: de markers in de brief zijn {sorted(in_brief)}, de '
        f'opdracht noemt {sorted(verwacht)}')
    for m in sorted(in_brief):
        eis(m in g.VRIJ_KOP,
            f'{o.BRIEF_VRIJ}: [[{m}]] is geen kolom van het werkblad '
            f'{g.VRIJ_BLAD} — dat veld bestaat straks niet in Word')
        GETELD['markers gekeurd'] += 1
    eis(g.datum_lang(g.BRIEFDATUM) in tekst,
        f'{o.BRIEF_VRIJ}: de briefdatum staat er niet in')
    eis('Als' in tekst and 'stap 4' in tekst,
        f'{o.BRIEF_VRIJ}: er staat niet waar de regel van stap 4 komt')

pad_spon = os.path.join(HIER, o.BRIEF_SPON)
if os.path.exists(pad_spon):
    tekst = doc_tekst(pad_spon)
    eis(not MARKER.findall(tekst),
        f'{o.BRIEF_SPON}: hier horen GEEN markers in te staan — de '
        'eindopdracht is juist dat zij de plaatsen kiezen '
        f'({sorted(set(MARKER.findall(tekst)))})')
    for veld in o.BRIEF_SPON_VELDEN:
        eis(veld in g.SPON_KOP,
            f'de eindopdracht vraagt veld {veld!r}, dat niet in de '
            f'sponsorlijst staat')
        eis(veld in tekst,
            f'{o.BRIEF_SPON}: het gevraagde veld {veld!r} staat nergens in de '
            'uitleg bij de brief')
        GETELD['sponsorvelden gekeurd'] += 1

# de opdracht moet naar alle vijf de bestanden verwijzen
pad_opdracht = os.path.join(HIER, 'samenvoegen-opdracht.docx')
if os.path.exists(pad_opdracht):
    tekst = doc_tekst(pad_opdracht)
    for naam in (o.STARTBESTAND, o.THEORIEBUNDEL, o.BRIEF_VRIJ, o.BRIEF_SPON):
        eis(naam in tekst, f'de opdracht noemt {naam} nergens')
    eis(str(o.TOTAAL) in tekst, 'de opdracht noemt het totaal niet')
    GETELD['verwijzingen gekeurd'] += 4

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
