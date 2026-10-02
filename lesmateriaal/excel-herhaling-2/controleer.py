# -*- coding: utf-8 -*-
"""Controleert of opdrachtbestand en startbestand bij elkaar passen.

Alle posities worden afgeleid uit gegevens.py: er staan geen vaste rijnummers
in. Voeg je daar regels toe, dan schuift deze controle vanzelf mee.
"""
import importlib.util
import sys

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal
import os
import re
from collections import Counter
from openpyxl import load_workbook

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', 'gegevens.py')
o = laad('o', 'oefeningen.py')

wb = load_workbook(os.path.join(HIER, 'excel-herhaling-2-startbestand.xlsx'))
fouten = []

# De functies en hulpfiches die de basisbundel aanbiedt. Deze bundel mag er
# niets buiten gebruiken, want dan staat er geen fiche tegenover.
BASIS_FUNCTIES = {'SOM', 'AFRONDEN', 'MAX', 'MIN', 'GEMIDDELDE', 'AANTAL',
                  'ALS', 'AANTAL.ALS', 'SOM.ALS', 'VERT.ZOEKEN'}
BASIS_HULP = {'Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak',
              'Beeld vastzetten'}


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


# 1. Gebruikt deze bundel alleen functies waar een fiche voor bestaat?
for oef in o.OEFENINGEN:
    for fn in oef['functies']:
        if fn not in BASIS_FUNCTIES:
            fouten.append(f"blad {oef['nr']}: {fn} heeft geen fiche in de basisbundel")
    for h in oef['hulp']:
        if h not in BASIS_HULP:
            fouten.append(f"blad {oef['nr']}: hulpfiche '{h}' bestaat niet in de basisbundel")

# 2. Komt elke functie vaak genoeg terug? Dat is het punt van een herhalingsbundel.
langste_eerst = sorted(BASIS_FUNCTIES, key=len, reverse=True)
telling = Counter()
for oef in o.OEFENINGEN:
    for _, _, hoe in oef['maken']:
        for fn in langste_eerst:
            if fn in hoe:
                telling[fn] += 1
                break
mager = [fn for fn in BASIS_FUNCTIES if telling[fn] < 2]
if mager:
    fouten.append(f'deze functies komen maar één keer voor: {sorted(mager)}')
print(f'formules in totaal: {sum(telling.values())}')
for fn, n in telling.most_common():
    bladen = ', '.join(str(oef['nr']) for oef in o.OEFENINGEN if fn in oef['functies'])
    print(f'   {fn:12s} {n}x   (bladen {bladen})')

# 3. Bestaat elk genoemd werkblad?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        fouten.append(f"blad {oef['nr']}: werkblad {oef['blad']} bestaat niet")

# 4. Klopt de opdrachtomschrijving met het startbestand?
print()
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        continue
    ws = wb[oef['blad']]

    temaken = [c for waar, *_ in oef['maken'] for c in cellen_van(waar)]
    bezet = [c for c in temaken if ws[c].value is not None]
    if bezet:
        fouten.append(f"{oef['blad']}: deze cellen moet de leerling maken, maar ze zijn al "
                      f"gevuld: {bezet[:5]}")

    gegeven = [c for waar, _ in oef['gegeven'] for c in cellen_van(waar)]
    leeg = [c for c in gegeven if ws[c].value is None]
    if leeg:
        fouten.append(f"{oef['blad']}: deze cellen zouden gegeven moeten zijn, maar zijn "
                      f"leeg: {leeg[:5]}")

    tekst = ' '.join(t + ' ' + u for t, u in oef['stappen'])
    uit_stappen = set(re.findall(r'Klik ([A-Z]\d{1,3}) aan en typ', tekst))
    buiten = sorted(uit_stappen - set(temaken))
    if buiten:
        fouten.append(f"{oef['blad']}: de stappen laten typen in {buiten}, maar dat staat "
                      f"niet in de opdrachtomschrijving")

    print(f"blad {oef['nr']} ({oef['blad']}): {len(gegeven)} gegeven, {len(temaken)} te maken")


# 5. Staan de brongegevens waar de opdracht beweert?
controles = [
    ('1 Weekomzet', f'B{g.B1_START}', g.B1[0][1]),
    ('1 Weekomzet', f'D{g.B1_EIND}', g.B1[-1][3]),
    ('2 Kwekers', f'B{g.B2_START}', g.B2[0][1]),
    ('2 Kwekers', f'D{g.B2_EIND}', g.B2[-1][3]),
    ('3 Prijsverhoging', 'B2', g.B3_PERCENTAGE),
    ('3 Prijsverhoging', f'B{g.B3_EIND}', g.B3[-1][1]),
    ('4 Bezoekers', f'B{g.B4_START}', g.B4[0][1]),
    ('4 Bezoekers', f'B{g.B4_EIND}', g.B4[-1][1]),
    ('5 Snoeicursus', 'B2', g.B5_GRENS),
    ('5 Snoeicursus', f'B{g.B5_EIND}', g.B5[-1][1]),
    ('6 Leveranciers', f'C{g.B6_START}', g.B6[0][2]),
    ('6 Leveranciers', f'B{g.B6_EIND}', g.B6[-1][1]),
    ('6 Leveranciers', f'A{g.B6_SAMENVATTING}', g.B6_LEVERANCIERS[0]),
    ('7 Zaden', f'A{g.B7_START}', g.B7_REGELS[0][0]),
    ('7 Zaden', f'D{g.B7_EIND}', g.B7_REGELS[-1][1]),
    ('7 Zaden', f'G{g.B7_TAB_START}', g.B7_TABEL[0][0]),
    ('7 Zaden', f'I{g.B7_TAB_EIND}', g.B7_TABEL[-1][2]),
]
for blad, cel, verwacht in controles:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: verwacht {verwacht!r}, gevonden {echt!r}')

# 6. Op blad 2 moet precies één kweker op de grens zitten, en op blad 5 precies
#    één cursist. Zonder die ene rij merkt niemand het verschil tussen > en >=.
op_de_grens = [naam for naam, ap, me, jn in g.B2 if ap + me + jn == g.B2_GROOT]
if len(op_de_grens) != 1:
    fouten.append(f'blad 2: precies één kweker op {g.B2_GROOT} planten verwacht, '
                  f'gevonden: {op_de_grens}')
else:
    print(f'\nblad 2: {op_de_grens[0]} zit precies op de grens ({g.B2_GROOT})')

op_de_grens = [naam for naam, punten in g.B5 if punten == g.B5_GRENS]
if len(op_de_grens) != 1:
    fouten.append(f'blad 5: precies één cursist met {g.B5_GRENS} punten verwacht, '
                  f'gevonden: {op_de_grens}')
else:
    print(f'blad 5: {op_de_grens[0]} zit precies op de grens ({g.B5_GRENS}) — '
          f'daar wordt > tegenover >= zichtbaar')

# 7. Op blad 4 moet de drempel van AANTAL.ALS een ander antwoord geven dan
#    "boven het gemiddelde", anders lijken het twee keer dezelfde vraag.
waarden = [v for _, v in g.B4]
gem = sum(waarden) / len(waarden)
boven_gem = sum(1 for v in waarden if v > gem)
boven_drempel = sum(1 for v in waarden if v > g.B4_DREMPEL)
if boven_gem == boven_drempel:
    fouten.append(f'blad 4: boven het gemiddelde ({boven_gem}) en boven de drempel '
                  f'({boven_drempel}) geven hetzelfde aantal — kies een andere drempel')
else:
    print(f'blad 4: {boven_gem} maanden boven het gemiddelde, {boven_drempel} boven '
          f'{g.B4_DREMPEL} — twee verschillende antwoorden')

# 8. Op blad 7 moet de code van het deeltotaal meer dan één keer besteld zijn,
#    anders heeft de SOM.ALS aan het eind geen betekenis.
dubbel = [c for c, n in Counter(c for c, _ in g.B7_REGELS).items() if n > 1]
if g.B7_DEELTOTAAL not in dubbel:
    fouten.append(f'blad 7: code {g.B7_DEELTOTAAL} moet meer dan één keer besteld zijn '
                  f'voor de SOM.ALS')
else:
    print(f'blad 7: codes die meer dan één keer voorkomen: {", ".join(sorted(dubbel))}')

# 9. Elke code in de bestelling moet in de zoektabel staan, anders geeft
#    VERT.ZOEKEN #N/B en is de oefening niet te maken.
bekend = {c for c, _, _ in g.B7_TABEL}
onbekend = sorted({c for c, _ in g.B7_REGELS} - bekend)
if onbekend:
    fouten.append(f'blad 7: deze codes staan niet in de zoektabel: {onbekend}')

print()
if fouten:
    print('PROBLEMEN:')
    for p in fouten:
        print('  -', p)
    raise SystemExit(1)
print('Alles sluit: opdrachten, startbestand en de fiches van de basisbundel')
print('passen bij elkaar, en elke functie komt minstens twee keer terug.')
