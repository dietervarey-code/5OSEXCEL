# -*- coding: utf-8 -*-
"""Controleert of opdracht, startbestand en lerarensleutel bij elkaar passen.

Voor een bundel die zonder leerkracht gemaakt wordt is één controle extra
belangrijk: elke formule uit de sleutel moet LETTERLIJK in de stappen staan.
Loopt dat uit elkaar, dan typt een leerling iets anders dan wat de sleutel
verwacht en kan niemand het rechtzetten.
"""
import importlib.util
import os
import re
import sys
from collections import Counter
from openpyxl import load_workbook

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

wb = load_workbook(os.path.join(HIER, 'slimste-mens-startbestand.xlsx'))
fouten = []

BASIS_FUNCTIES = {'SOM', 'AFRONDEN', 'MAX', 'MIN', 'GEMIDDELDE', 'AANTAL',
                  'ALS', 'AANTAL.ALS', 'SOM.ALS', 'VERT.ZOEKEN'}
BASIS_HULP = {'Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak',
              'Beeld vastzetten'}
NADRUK = {'SOM', 'AANTAL.ALS', 'VERT.ZOEKEN'}   # waar deze bundel over gaat


def cellen_van(verwijzing):
    """'E4:E15' -> alle cellen daartussen. 'C17' -> die ene cel."""
    if ':' not in verwijzing:
        return [verwijzing]
    links, rechts = verwijzing.split(':')
    k1, r1 = re.match(r'([A-Z]+)(\d+)', links).groups()
    k2, r2 = re.match(r'([A-Z]+)(\d+)', rechts).groups()
    return [f'{chr(k)}{r}'
            for k in range(ord(k1), ord(k2) + 1)
            for r in range(int(r1), int(r2) + 1)]


def eerste_cel(verwijzing):
    return verwijzing.split(':')[0]


# 1. Bestaat elk genoemd werkblad?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        fouten.append(f"werkblad {oef['blad']} bestaat niet in het startbestand")

# 2. Klopt de opdracht met het startbestand?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        continue
    ws = wb[oef['blad']]

    temaken = [c for waar, *_ in oef['maken'] for c in cellen_van(waar)]
    bezet = [c for c in temaken if ws[c].value is not None]
    if bezet:
        fouten.append(f"{oef['blad']}: deze cellen moet de leerling maken, maar ze zijn al "
                      f'gevuld: {bezet[:5]}')

    gegeven = [c for waar, _ in oef['gegeven'] for c in cellen_van(waar)]
    leeg = [c for c in gegeven if ws[c].value is None]
    if leeg:
        fouten.append(f"{oef['blad']}: deze cellen zouden gegeven moeten zijn, maar zijn "
                      f'leeg: {leeg[:5]}')

    tekst = ' '.join(t + ' ' + u for t, u in oef['stappen'])
    uit_stappen = set(re.findall(r'Klik ([A-Z]\d{1,3}) aan en typ', tekst))
    buiten = sorted(uit_stappen - set(temaken))
    if buiten:
        fouten.append(f"{oef['blad']}: de stappen laten typen in {buiten}, maar dat staat "
                      f'niet in de opdrachtomschrijving')
    print(f"blad {oef['nr']} ({oef['blad']}): {len(gegeven)} gegeven, {len(temaken)} te maken")

# 3. Gebruikt deze bundel alleen functies en opmaak waar een fiche voor bestaat?
for oef in o.OEFENINGEN:
    for fn in oef['functies']:
        if fn not in BASIS_FUNCTIES:
            fouten.append(f"blad {oef['nr']}: {fn} staat niet in de basisbundel")
    for h in oef['hulp']:
        if h not in BASIS_HULP:
            fouten.append(f"blad {oef['nr']}: hulpfiche '{h}' bestaat niet")

# 4. Komt elke functie aan bod, en liggen de drie waar het om gaat bovenaan?
langste_eerst = sorted(BASIS_FUNCTIES, key=len, reverse=True)
telling = Counter()
for oef in o.OEFENINGEN:
    for _, _, hoe in oef['maken']:
        for fn in langste_eerst:
            if fn in hoe:
                telling[fn] += 1
                break
ontbreekt = sorted(BASIS_FUNCTIES - set(telling))
if ontbreekt:
    fouten.append(f'deze functies komen nergens aan bod: {ontbreekt}')
mager = sorted(fn for fn in NADRUK if telling[fn] < 3)
if mager:
    fouten.append(f'deze bundel gaat over {sorted(NADRUK)}, maar {mager} komt minder dan '
                  f'drie keer voor')
print(f'\nformules: {sum(telling.values())} | nadruk: '
      + ', '.join(f'{fn} {telling[fn]}x' for fn in sorted(NADRUK)))

# 5. Geen geneste functies: in geen enkele stap mag een functie binnen een
#    functie staan. Dat is de belofte van deze bundel.
BUITENSTE = re.compile(r'=([A-Z][A-Z.]*)\((.*?)\)(?=[ ,.]|$)')
for oef in o.OEFENINGEN:
    for titel, uitleg in oef['stappen']:
        for naam, binnenkant in BUITENSTE.findall(titel + ' ' + uitleg):
            genest = re.findall(r'[A-Z][A-Z.]{2,}\(', binnenkant)
            if genest:
                fouten.append(f"blad {oef['nr']}: ={naam}({binnenkant}) heeft een functie "
                              f'binnen een functie ({genest}) — die horen niet in deze '
                              f'bundel')

# 6. Staat elke formule uit de sleutel letterlijk in de stappen?
for oef in o.OEFENINGEN:
    tekst = ' '.join(t + ' ' + u for t, u in oef['stappen'])
    for cel, formule, _ in sl.SLEUTEL[oef['nr']]:
        if formule not in tekst:
            fouten.append(f"blad {oef['nr']} {cel}: de sleutel zegt {formule}, maar die "
                          f'formule staat nergens in de stappen')
    uit_sleutel = {cel for cel, _, _ in sl.SLEUTEL[oef['nr']]}
    uit_opdracht = {eerste_cel(waar) for waar, *_ in oef['maken']}
    if uit_sleutel != uit_opdracht:
        fouten.append(f"blad {oef['nr']}: sleutel en opdracht noemen andere cellen: "
                      f'{sorted(uit_sleutel ^ uit_opdracht)}')

# 7. Het controlegetal moet bij een cel horen die de leerling zelf maakt.
for oef in o.OEFENINGEN:
    cel, waarde = sl.CONTROLE[oef['nr']]
    temaken = [c for waar, *_ in oef['maken'] for c in cellen_van(waar)]
    if cel != oef['controlecel']:
        fouten.append(f"blad {oef['nr']}: controlecel {oef['controlecel']} in de opdracht, "
                      f'{cel} in de sleutel')
    if cel not in temaken:
        fouten.append(f"blad {oef['nr']}: controlegetal staat in {cel}, maar die cel maakt "
                      f'de leerling niet')
    if not waarde:
        fouten.append(f"blad {oef['nr']}: geen controlegetal")
print('controlegetallen: '
      + ' | '.join(f'{sl.CONTROLE[n][0]}={sl.CONTROLE[n][1]}' for n in sorted(sl.CONTROLE)))

# 8. Heeft elk blad een lijstje 'Loop je vast?' met minstens drie regels?
for oef in o.OEFENINGEN:
    if len(oef.get('vastgelopen', [])) < 3:
        fouten.append(f"blad {oef['nr']}: minder dan drie regels bij 'Loop je vast?' — "
                      f'te weinig voor een bundel die alleen gemaakt wordt')

# 9. Staan de brongegevens waar de opdracht beweert?
controles = [
    ('1 Kijkcijfers', f'B{g.B1_START}', g.B1[0][1]),
    ('1 Kijkcijfers', f'D{g.B1_EIND}', g.B1[-1][3]),
    ('2 Deelnemers', 'B2', g.B2_FINALIST),
    ('2 Deelnemers', f'A{g.B2_START}', g.B2[0][0]),
    ('2 Deelnemers', f'E{g.B2_EIND}', g.B2[-1][4]),
    ('3 Themas', f'B{g.B3_START}', g.B3[0][1]),
    ('3 Themas', f'D{g.B3_EIND}', g.B3[-1][3]),
    ('3 Themas', f'A{g.B3_PER_THEMA}', g.B3_THEMAS[0]),
    ('4 Rondes', f'A{g.B4_START}', g.B4_REGELS[0][0]),
    ('4 Rondes', f'D{g.B4_EIND}', g.B4_REGELS[-1][1]),
    ('4 Rondes', f'G{g.B4_TAB_START}', g.B4_TABEL[0][0]),
    ('4 Rondes', f'I{g.B4_TAB_EIND}', g.B4_TABEL[-1][2]),
    ('5 Finaleweek', 'B2', g.B5_DOOR),
    ('5 Finaleweek', f'A{g.B5_START}', g.B5_UITSLAG[0][0]),
    ('5 Finaleweek', f'E{g.B5_EIND}', g.B5_UITSLAG[-1][3]),
    ('5 Finaleweek', f'I{g.B5_TAB_START}', g.B5_TABEL[0][0]),
    ('5 Finaleweek', f'J{g.B5_TAB_EIND}', g.B5_TABEL[-1][1]),
]
for blad, cel, verwacht in controles:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: verwacht {verwacht!r}, gevonden {echt!r}')

# 10. Op blad 2 en blad 5 moet iemand precies op de grens zitten. Daar wordt
#     het verschil tussen > en >= zichtbaar, en de stappen wijzen die namen aan.
if not a.B2_OP_DE_GRENS:
    fouten.append(f'blad 2: niemand heeft precies {g.B2_FINALIST} overwinningen — dan '
                  f'wordt > tegenover >= nooit zichtbaar')
else:
    print(f'\nblad 2: op de grens staat {", ".join(a.B2_OP_DE_GRENS)}')
    for naam in a.B2_OP_DE_GRENS:
        if naam not in ' '.join(t + ' ' + u for t, u in o.OEFENINGEN[1]['stappen']):
            fouten.append(f'blad 2: {naam} zit op de grens maar wordt niet in de stappen '
                          f'genoemd — wie alleen werkt merkt het dan niet')
if len(a.B5_OP_DE_GRENS) != 1:
    fouten.append(f'blad 5: precies één deelnemer op {g.B5_DOOR} seconden verwacht, '
                  f'gevonden: {a.B5_OP_DE_GRENS}')
else:
    print(f'blad 5: op de grens staat {a.B5_OP_DE_GRENS[0]}')

# 11. Blad 3: elk thema moet voorkomen en de deeltotalen moeten het geheel geven.
leeg = [t for t, n in zip(g.B3_THEMAS, a.B3_AANTAL_PER) if n == 0]
if leeg:
    fouten.append(f'blad 3: deze themas komen niet voor in de lijst: {leeg}')
if a.B3_TOTAAL_PER != a.B3_TOTAAL:
    fouten.append(f'blad 3: de deeltotalen geven {a.B3_TOTAAL_PER}, het geheel {a.B3_TOTAAL}')
onbekend = sorted({t for _, t, _, _ in g.B3} - set(g.B3_THEMAS))
if onbekend:
    fouten.append(f'blad 3: deze themas staan niet in het blokje eronder: {onbekend}')

# 12. Blad 4 en 5: elke code en elk startnummer moet in de zoektabel staan,
#     en geen enkele twee keer. Anders geeft VERT.ZOEKEN #N/B of het verkeerde.
for naam, sleutels, gebruikt in [
    ('blad 4', [c for c, _, _ in g.B4_TABEL], [c for c, _ in g.B4_REGELS]),
    ('blad 5', [n for n, _ in g.B5_TABEL], [n for n, _, _, _ in g.B5_UITSLAG]),
]:
    dubbel = [k for k, n in Counter(sleutels).items() if n > 1]
    if dubbel:
        fouten.append(f'{naam}: deze sleutels staan twee keer in de zoektabel: {dubbel}')
    onbekend = sorted(set(gebruikt) - set(sleutels))
    if onbekend:
        fouten.append(f'{naam}: deze sleutels staan niet in de zoektabel: {onbekend}')

print()
if fouten:
    print('PROBLEMEN:')
    for p in fouten:
        print('  -', p)
    raise SystemExit(1)
print('Alles sluit: opdracht, startbestand en lerarensleutel passen bij elkaar.')
print('Elke formule uit de sleutel staat letterlijk in de stappen, elk blad heeft een')
print('controlegetal bij een cel die de leerling zelf maakt, en er zit geen enkele')
print('geneste functie in.')
