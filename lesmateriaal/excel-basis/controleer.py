# -*- coding: utf-8 -*-
"""Controleert of stappenplan, fiches en startbestand bij elkaar passen."""
import importlib.util
import os

HIER = os.path.dirname(os.path.abspath(__file__))

import re
from openpyxl import load_workbook


def laad(naam, pad):
    spec = importlib.util.spec_from_file_location(naam, pad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', os.path.join(HIER, 'gegevens.py'))
f = laad('f', os.path.join(HIER, 'fiches.py'))
o = laad('o', os.path.join(HIER, 'oefeningen.py'))

wb = load_workbook(os.path.join(HIER, 'excel-startbestand.xlsx'))
fouten = []

# 1. Heeft elke genoemde functie een fiche?
fiches = {d['naam'] for d in f.FUNCTIES}
hulpfiches = {d['naam'] for d in f.HULP}
for oef in o.OEFENINGEN:
    for fn in oef['functies']:
        if fn not in fiches:
            fouten.append(f"oefening {oef['nr']}: geen functiefiche voor {fn}")
    for h in oef['hulp']:
        if h not in hulpfiches:
            fouten.append(f"oefening {oef['nr']}: geen hulpfiche voor {h}")
print(f'functiefiches: {len(fiches)} | hulpfiches: {len(hulpfiches)}')

# 2. Wordt elke fiche ook echt gebruikt?
gebruikt = {fn for oef in o.OEFENINGEN for fn in oef['functies']}
gebruikt_h = {h for oef in o.OEFENINGEN for h in oef['hulp']}
ongebruikt = (fiches - gebruikt) | (hulpfiches - gebruikt_h)
if ongebruikt:
    print('fiches die nergens genoemd worden:', ongebruikt)

# 3. Verwijst elke stap naar een blad dat bestaat?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        fouten.append(f"oefening {oef['nr']}: blad {oef['blad']} bestaat niet")

# 4. Kloppen de celverwijzingen uit de stappen met het startbestand?
CEL = re.compile(r'\b([A-Z])(\d{1,3})\b')
for oef in o.OEFENINGEN:
    ws = wb[oef['blad']]
    tekst = ' '.join(t + ' ' + u for t, u in oef['stappen'])
    # Cellen waar de leerling iets moet INVULLEN, horen leeg te zijn.
    invul = set()
    for m in re.finditer(r'Klik ([A-Z]\d{1,3}) aan en typ', tekst):
        invul.add(m.group(1))
    for cel in sorted(invul):
        if ws[cel].value is not None:
            fouten.append(f"{oef['blad']}: {cel} zou leeg moeten zijn, maar bevat {ws[cel].value!r}")
    print(f"oefening {oef['nr']} ({oef['blad']}): {len(invul)} invulcellen gecontroleerd -> {', '.join(sorted(invul))}")

# 5. Staan de bronnen waar de stappen beweren?
controles = [
    ('1 Voorraad', 'C4', g.O1[0][2]),
    ('1 Voorraad', 'D4', g.O1[0][3]),
    ('1 Voorraad', 'C11', g.O1[-1][2]),
    ('2 Prijslijst', 'B3', g.O2_PERCENTAGE),
    ('2 Prijslijst', 'B6', g.O2[0][1]),
    ('2 Prijslijst', 'B12', g.O2[-1][1]),
    ('3 Verkoop', 'B4', g.O3[0][1]),
    ('3 Verkoop', 'D9', g.O3[-1][3]),
    ('4 Bestellingen', 'B3', g.O4_DREMPEL),
    ('4 Bestellingen', 'C6', g.O4[0][2]),
    ('4 Bestellingen', 'C15', g.O4[-1][2]),
    ('5 Klanten', 'A4', g.O5_VRAAG[0]),
    ('5 Klanten', 'G4', g.O5_TABEL[0][0]),
    ('5 Klanten', 'I11', g.O5_TABEL[-1][2]),
]
for blad, cel, verwacht in controles:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: verwacht {verwacht!r}, gevonden {echt!r}')

# 6. Labels op de juiste rij?
labels = [
    ('1 Voorraad', f'C{g.O1_TOTAAL}', 'Totale voorraadwaarde'),
    ('3 Verkoop', f'A{g.O3_SAMENVATTING}', 'Hoogste kwartaaltotaal'),
    ('3 Verkoop', f'A{g.O3_SAMENVATTING + 3}', 'Aantal verkopers'),
    ('4 Bestellingen', f'B{g.O4_ANTWOORD}', 'Aantal gratis leveringen'),
    ('4 Bestellingen', f'B{g.O4_ANTWOORD + 1}', 'Bedrag van de gratis leveringen'),
]
for blad, cel, verwacht in labels:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: label verwacht {verwacht!r}, gevonden {echt!r}')

print()
if fouten:
    print('PROBLEMEN:')
    for p in fouten:
        print('  -', p)
    raise SystemExit(1)
print('Alles sluit: fiches, stappen en startbestand passen bij elkaar.')
