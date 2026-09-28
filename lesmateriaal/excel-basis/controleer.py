# -*- coding: utf-8 -*-
"""Controleert of stappenplan, fiches en startbestand bij elkaar passen.

Alle posities worden afgeleid uit gegevens.py. Voeg je daar rijen toe, dan
schuift deze controle vanzelf mee — er staan geen vaste rijnummers in.
"""
import importlib.util
import os
import re
from openpyxl import load_workbook

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = laad('g', 'gegevens.py')
f = laad('f', 'fiches.py')
o = laad('o', 'oefeningen.py')

wb = load_workbook(os.path.join(HIER, 'excel-startbestand.xlsx'))
fouten = []

# 1. Heeft elke genoemde functie een fiche, en omgekeerd?
fiches = {d['naam'] for d in f.FUNCTIES}
hulpfiches = {d['naam'] for d in f.HULP}
for oef in o.OEFENINGEN:
    for fn in oef['functies']:
        if fn not in fiches:
            fouten.append(f"oefening {oef['nr']}: geen functiefiche voor {fn}")
    for h in oef['hulp']:
        if h not in hulpfiches:
            fouten.append(f"oefening {oef['nr']}: geen hulpfiche voor {h}")
gebruikt = {fn for oef in o.OEFENINGEN for fn in oef['functies']}
gebruikt_h = {h for oef in o.OEFENINGEN for h in oef['hulp']}
ongebruikt = (fiches - gebruikt) | (hulpfiches - gebruikt_h)
print(f'functiefiches: {len(fiches)} | hulpfiches: {len(hulpfiches)}')
if ongebruikt:
    print('  fiches die in geen enkele oefening genoemd worden:', ', '.join(sorted(ongebruikt)))

# 2. Geven de fiches de oplossing van een oefening weg?
#    Een fiche mag nooit een celadres of een bedrag uit het startbestand bevatten.
verboden = set()
for artikel in g.O1:
    verboden.add(artikel[0])
for code in g.O5_VRAAG + [r[0] for r in g.O5_TABEL]:
    verboden.add(code)
for nr, *_ in g.O4:
    verboden.add(nr)
for d in f.FUNCTIES + f.HULP:
    tekst = ' '.join([d['wat'], d['schrijf'], d['fout'], d.get('zelf', '')]
                     + d['uitleg'] + d['weten']
                     + [x[0] + x[1] for x in d.get('varianten', [])]
                     + [b['onderschrift'] for b in d['beelden']]
                     + [str(b.get('formule', '')) for b in d['beelden']])
    lek = sorted(v for v in verboden if v in tekst)
    if lek:
        fouten.append(f"fiche {d['naam']}: verwijst naar gegevens uit de oefening: {lek}")

# 3. Bestaat elk genoemd werkblad?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        fouten.append(f"oefening {oef['nr']}: blad {oef['blad']} bestaat niet")

def cellen_van(verwijzing):
    """'E4:E15' -> alle cellen daartussen. 'C17' -> die ene cel."""
    if ':' not in verwijzing:
        return [verwijzing]
    links, rechts = verwijzing.split(':')
    k1, r1 = re.match(r'([A-Z]+)(\d+)', links).groups()
    k2, r2 = re.match(r'([A-Z]+)(\d+)', rechts).groups()
    uit = []
    for k in range(ord(k1), ord(k2) + 1):
        for r in range(int(r1), int(r2) + 1):
            uit.append(f'{chr(k)}{r}')
    return uit


# 4. Klopt de opdrachtomschrijving met het startbestand?
#    Wat de leerling moet maken, hoort leeg te zijn. Wat gegeven is, hoort gevuld.
for oef in o.OEFENINGEN:
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

    # De stappen mogen niet naar een cel wijzen die buiten de omschrijving valt.
    tekst = ' '.join(t + ' ' + u for t, u in oef['stappen'])
    uit_stappen = set(re.findall(r'Klik ([A-Z]\d{1,3}) aan en typ', tekst))
    buiten = sorted(uit_stappen - set(temaken))
    if buiten:
        fouten.append(f"{oef['blad']}: het stappenplan laat typen in {buiten}, maar dat staat "
                      f"niet in de opdrachtomschrijving")

    print(f"oefening {oef['nr']} ({oef['blad']}): {len(gegeven)} cellen gegeven, "
          f"{len(temaken)} te maken, {len(uit_stappen)} genoemd in de stappen")

# 5. Staan de brongegevens waar de stappen beweren? Alles afgeleid, niets vast.
controles = [
    ('1 Voorraad', f'C{g.O1_START}', g.O1[0][2]),
    ('1 Voorraad', f'D{g.O1_START}', g.O1[0][3]),
    ('1 Voorraad', f'C{g.O1_EIND}', g.O1[-1][2]),
    ('2 Prijslijst', 'B3', g.O2_PERCENTAGE),
    ('2 Prijslijst', f'B{g.O2_START}', g.O2[0][1]),
    ('2 Prijslijst', f'B{g.O2_EIND}', g.O2[-1][1]),
    ('3 Verkoop', f'B{g.O3_START}', g.O3[0][1]),
    ('3 Verkoop', f'D{g.O3_EIND}', g.O3[-1][3]),
    ('4 Bestellingen', 'B3', g.O4_DREMPEL),
    ('4 Bestellingen', f'C{g.O4_START}', g.O4[0][2]),
    ('4 Bestellingen', f'C{g.O4_EIND}', g.O4[-1][2]),
    ('5 Klanten', f'A{g.O5_START}', g.O5_VRAAG[0]),
    ('5 Klanten', f'G{g.O5_TAB_START}', g.O5_TABEL[0][0]),
    ('5 Klanten', f'I{g.O5_TAB_EIND}', g.O5_TABEL[-1][2]),
]
for blad, cel, verwacht in controles:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: verwacht {verwacht!r}, gevonden {echt!r}')

# 6. Staan de labels op de juiste rij?
labels = [
    ('1 Voorraad', f'B{g.O1_TOTAAL}', 'Totaal'),
    ('3 Verkoop', f'A{g.O3_MAANDTOTAAL}', 'Totaal per maand'),
    ('3 Verkoop', f'A{g.O3_SAMENVATTING}', 'Hoogste kwartaaltotaal'),
    ('3 Verkoop', f'A{g.O3_SAMENVATTING + 3}', 'Aantal verkopers'),
    ('4 Bestellingen', f'B{g.O4_ANTWOORD}', 'Aantal gratis leveringen'),
    ('4 Bestellingen', f'B{g.O4_ANTWOORD + 3}', 'Bedrag van de betalende leveringen'),
]
for blad, cel, verwacht in labels:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: label verwacht {verwacht!r}, gevonden {echt!r}')

# 7. De code die bewust niet bestaat, mag echt niet in de zoektabel staan.
if g.zoek(g.O5_ONBEKEND) is not None:
    fouten.append(f'{g.O5_ONBEKEND} zou NIET in de zoektabel mogen staan')
ontbrekend = [c for c in g.O5_VRAAG if g.zoek(c) is None]
if len(ontbrekend) != 1:
    fouten.append(f'precies één onbekende code verwacht, gevonden: {ontbrekend}')
else:
    print(f'oefening 5: één code geeft bewust #N/B -> {ontbrekend[0]} '
          f'op rij {g.O5_START + g.O5_VRAAG.index(ontbrekend[0])}')

print()
if fouten:
    print('PROBLEMEN:')
    for p in fouten:
        print('  -', p)
    raise SystemExit(1)
print('Alles sluit: fiches, stappen en startbestand passen bij elkaar,')
print('en geen enkele fiche verklapt een antwoord uit de oefening.')
