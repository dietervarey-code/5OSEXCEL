# -*- coding: utf-8 -*-
"""Controleert of toetsblad, startbestand en verbetersleutel bij elkaar passen.

Alle posities worden afgeleid uit gegevens.py: er staan geen vaste rijnummers
in. Voeg je daar een speler of een wedstrijd toe, dan schuift deze controle
vanzelf mee.
"""
import importlib.util
import os
import re
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
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

wb = load_workbook(os.path.join(HIER, 'rodeduivels-toets-startbestand.xlsx'))
fouten = []

# De tien functies en vijf hulpfiches van de basisbundel. Een toets mag er
# niets buiten gebruiken: daar hebben ze geen fiche voor gezien.
BASIS_FUNCTIES = {'SOM', 'AFRONDEN', 'MAX', 'MIN', 'GEMIDDELDE', 'AANTAL',
                  'ALS', 'AANTAL.ALS', 'SOM.ALS', 'VERT.ZOEKEN'}
BASIS_HULP = {'Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak',
              'Beeld vastzetten'}
FORMULE = re.compile(r"=\s*[A-Z$'(]|[A-Z][A-Z.]+\(")


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


def opdrachttekst(oef):
    """Alles wat de leerling te lezen krijgt bij één werkblad."""
    stukken = [oef['doel'], oef['klaar'], oef['controle']]
    stukken += [f'{waar} {wat}' for waar, wat in oef['gegeven']]
    stukken += [f"{m['waar']} {m['wat']} {m['hoe']}" for m in oef['maken']]
    stukken += [eis for eis, _ in oef['opmaak']]
    return stukken


# 1. Bestaat elk genoemd werkblad?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        fouten.append(f"werkblad {oef['blad']} bestaat niet in het startbestand")

# 2. Klopt het toetsblad met het startbestand?
for oef in o.OEFENINGEN:
    if oef['blad'] not in wb.sheetnames:
        continue
    ws = wb[oef['blad']]

    temaken = [c for m in oef['maken'] for c in cellen_van(m['waar'])]
    bezet = [c for c in temaken if ws[c].value is not None]
    if bezet:
        fouten.append(f"{oef['blad']}: deze cellen moet de leerling maken, maar ze zijn al "
                      f'gevuld: {bezet[:5]}')

    gegeven = [c for waar, _ in oef['gegeven'] for c in cellen_van(waar)]
    leeg = [c for c in gegeven if ws[c].value is None]
    if leeg:
        fouten.append(f"{oef['blad']}: deze cellen zouden gegeven moeten zijn, maar zijn "
                      f'leeg: {leeg[:5]}')
    print(f"blad {oef['nr']} ({oef['blad']}): {len(gegeven)} gegeven, {len(temaken)} te maken")

# 3. Het toetsblad mag de formule niet weggeven.
for oef in o.OEFENINGEN:
    for stuk in opdrachttekst(oef):
        if FORMULE.search(stuk):
            fouten.append(f"blad {oef['nr']}: er staat een formule op het toetsblad: "
                          f'{stuk[:70]!r}')

# 4. Gebruikt deze toets alleen functies en opmaak waar een fiche voor bestaat?
for oef in o.OEFENINGEN:
    for fn in oef['functies']:
        if fn not in BASIS_FUNCTIES:
            fouten.append(f"blad {oef['nr']}: {fn} staat niet in de basisbundel")
    for h in oef['hulp']:
        if h not in BASIS_HULP:
            fouten.append(f"blad {oef['nr']}: hulpfiche '{h}' bestaat niet")
    for m in oef['maken']:
        if m['functie'] and m['functie'] not in BASIS_FUNCTIES:
            fouten.append(f"blad {oef['nr']} {m['waar']}: {m['functie']} staat niet in de "
                          f'basisbundel')
        if m['functie'] and m['functie'] not in oef['functies']:
            fouten.append(f"blad {oef['nr']} {m['waar']}: {m['functie']} ontbreekt in de "
                          f'functielijst van dat blad')

# 5. Komen alle tien de functies aan bod? Dat is het punt van een synthesetoets.
telling = Counter(m['functie'] for oef in o.OEFENINGEN for m in oef['maken'] if m['functie'])
ontbreekt = sorted(BASIS_FUNCTIES - set(telling))
if ontbreekt:
    fouten.append(f'deze functies komen nergens aan bod: {ontbreekt}')
hulp_telling = Counter(h for oef in o.OEFENINGEN for h in oef['hulp'])
hulp_weg = sorted(BASIS_HULP - set(hulp_telling))
if hulp_weg:
    fouten.append(f'deze hulpfiches komen nergens aan bod: {hulp_weg}')
print(f'\nfunctiedekking: {len(telling)}/{len(BASIS_FUNCTIES)} functies, '
      f'{len(hulp_telling)}/{len(BASIS_HULP)} hulpfiches')

# 6. Heeft elke cel uit de opdracht een oplossing, en kloppen de punten?
formulepunten = 0
for oef in o.OEFENINGEN:
    uit_sleutel = {cel: pt for cel, _, _, pt, _ in sl.SLEUTEL[oef['nr']]}
    for m in oef['maken']:
        cel = eerste_cel(m['waar'])
        if cel not in uit_sleutel:
            fouten.append(f"blad {oef['nr']}: {m['waar']} staat niet in de verbetersleutel")
        elif uit_sleutel[cel] != m['punten']:
            fouten.append(f"blad {oef['nr']} {cel}: {m['punten']} punten op het toetsblad, "
                          f'{uit_sleutel[cel]} in de sleutel')
    uit_opdracht = {eerste_cel(m['waar']) for m in oef['maken']}
    extra = sorted(set(uit_sleutel) - uit_opdracht)
    if extra:
        fouten.append(f"blad {oef['nr']}: de sleutel lost cellen op die niet gevraagd "
                      f'worden: {extra}')
    formulepunten += sum(m['punten'] for m in oef['maken'])

opmaakpunten = sum(n for oef in o.OEFENINGEN for _, n in oef['opmaak'])
minuten = sum(int(oef['duur'].split()[0]) for oef in o.OEFENINGEN)
if formulepunten + opmaakpunten != 50:
    fouten.append(f'de toets staat op {formulepunten + opmaakpunten} punten in plaats van 50')
if minuten != 50:
    fouten.append(f'de toets duurt {minuten} minuten in plaats van 50')
print(f'punten: {formulepunten} formules + {opmaakpunten} opmaak = '
      f'{formulepunten + opmaakpunten}, voor {minuten} minuten')

# 7. Staan de brongegevens waar het toetsblad beweert?
controles = [
    ('1 Selectie', 'B2', g.B1_ERVAREN),
    ('1 Selectie', f'A{g.B1_START}', g.B1[0][0]),
    ('1 Selectie', f'E{g.B1_EIND}', g.B1[-1][4]),
    ('2 Wedstrijden', f'B{g.B2_START}', g.B2[0][1]),
    ('2 Wedstrijden', f'E{g.B2_EIND}', g.B2[-1][4]),
    ('3 Clubdoelpunten', f'C{g.B3_START}', g.B3[0][2]),
    ('3 Clubdoelpunten', f'D{g.B3_EIND}', g.B3[-1][3]),
    ('3 Clubdoelpunten', f'A{g.B3_PER_POSITIE}', g.POSITIES[0]),
    ('4 Tickets', 'B2', g.B4_KORTING),
    ('4 Tickets', f'B{g.B4_EIND}', g.B4[-1][1]),
    ('5 Wedstrijdblad', f'A{g.B5_START}', g.B5_BASIS[0][0]),
    ('5 Wedstrijdblad', f'D{g.B5_EIND}', g.B5_BASIS[-1][1]),
    ('5 Wedstrijdblad', f'F{g.B5_TAB_START}', g.B5_TABEL[0][0]),
    ('5 Wedstrijdblad', f'H{g.B5_TAB_EIND}', g.B5_TABEL[-1][2]),
]
for blad, cel, verwacht in controles:
    echt = wb[blad][cel].value
    if echt != verwacht:
        fouten.append(f'{blad}!{cel}: verwacht {verwacht!r}, gevonden {echt!r}')

# 8. Blad 1: precies één speler op de capsgrens, anders wordt > tegenover >=
#    nooit zichtbaar. En de voorwaardelijke opmaak moet een ANDER antwoord
#    geven dan de ALS, anders lijken het twee keer dezelfde vraag.
if len(a.B1_OP_DE_GRENS) != 1:
    fouten.append(f'blad 1: precies één speler met {g.B1_ERVAREN} caps verwacht, '
                  f'gevonden: {a.B1_OP_DE_GRENS}')
else:
    print(f'\nblad 1: {a.B1_OP_DE_GRENS[0]} zit precies op de grens ({g.B1_ERVAREN} caps)')
if len(a.B1_BOVEN_GEM) == a.B1_AANTAL_ERVAREN:
    fouten.append(f'blad 1: "boven het gemiddelde" ({len(a.B1_BOVEN_GEM)}) en "ervaren" '
                  f'({a.B1_AANTAL_ERVAREN}) geven hetzelfde aantal — kies een andere grens')
else:
    print(f'blad 1: {len(a.B1_BOVEN_GEM)} spelers boven het gemiddelde, '
          f'{a.B1_AANTAL_ERVAREN} ervaren — twee verschillende antwoorden')

# 9. Blad 2: er moet minstens één gelijkspel zijn, anders maakt > tegenover >=
#    geen verschil. En de kolomtotalen moeten op elkaar aansluiten.
gelijk = [tegenstander for _, tegenstander, _, voor, tegen in g.B2 if voor == tegen]
if not gelijk:
    fouten.append('blad 2: geen enkel gelijkspel — dan is > tegenover >= niet te zien')
else:
    print(f'blad 2: gelijkspelen tegen {", ".join(gelijk)}')
if a.B2_VOOR - a.B2_TEGEN != a.B2_SALDO_TOTAAL:
    fouten.append('blad 2: de drie kolomtotalen sluiten niet op elkaar aan')

# 10. Blad 3: elke positie moet voorkomen, de deeltotalen moeten het geheel
#     geven, en minstens één positie staat op nul (de doelmannen).
leeg = [p for p, n in zip(g.POSITIES, a.B3_AANTAL_PER) if n == 0]
if leeg:
    fouten.append(f'blad 3: deze posities komen niet voor in de lijst: {leeg}')
if a.B3_TOTAAL_PER != a.B3_TOTAAL:
    fouten.append(f'blad 3: de deeltotalen geven {a.B3_TOTAAL_PER}, het geheel '
                  f'{a.B3_TOTAAL}')
if 0 not in a.B3_DOELPUNTEN_PER:
    fouten.append('blad 3: geen enkele positie staat op nul doelpunten — dan toont niets '
                  'dat SOM.ALS over nullen gewoon 0 geeft')
onbekend = sorted({pos for _, pos, _, _ in g.B3} - set(g.POSITIES))
if onbekend:
    fouten.append(f'blad 3: deze posities staan niet in de lijst eronder: {onbekend}')

# 11. Blad 4: geen enkele prijs mag op een afrondingsgeval vallen waar een
#     berekening met floats een ander antwoord geeft dan het exacte. Anders
#     kan de sleutel afwijken van wat Excel toont — op een toets kan dat niet.
for vak, prijs in g.B4:
    exact = (Decimal(str(prijs)) * Decimal(str(g.B4_KORTING))
             ).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
    drijvend = Decimal(str(prijs * g.B4_KORTING)
                       ).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
    if exact != drijvend:
        fouten.append(f'blad 4: {vak} ({prijs}) rondt exact naar {exact} maar met floats '
                      f'naar {drijvend} — kies een andere prijs')
halve_cent = [vak for vak, prijs in g.B4
              if str(Decimal(str(prijs)) * Decimal(str(g.B4_KORTING))).endswith('5')]
if not halve_cent:
    fouten.append('blad 4: geen enkele korting valt op een halve cent — dan toont niets '
                  'waarom AFRONDEN nodig is')
else:
    print(f'blad 4: halve centen bij {", ".join(halve_cent)} — daar doet AFRONDEN zijn werk')

# 12. Blad 5: elk rugnummer uit de basiself moet in de spelerslijst staan, en
#     geen enkel rugnummer mag er twee keer in staan.
lijst = [nr for nr, _, _ in g.B5_TABEL]
dubbel = [nr for nr, n in Counter(lijst).items() if n > 1]
if dubbel:
    fouten.append(f'blad 5: deze rugnummers staan twee keer in de spelerslijst: {dubbel}')
onbekend = sorted({nr for nr, _ in g.B5_BASIS} - set(lijst))
if onbekend:
    fouten.append(f'blad 5: deze rugnummers staan niet in de spelerslijst: {onbekend}')
if len(g.B5_BASIS) != 11:
    fouten.append(f'blad 5: een basiself telt elf spelers, hier staan er {len(g.B5_BASIS)}')
if a.B5_AANTAL_TELLEN == 0:
    fouten.append(f'blad 5: geen enkele {g.B5_TELLEN.lower()} in de basiself — dan geeft de '
                  f'telling 0')

print()
if fouten:
    print('PROBLEMEN:')
    for p in fouten:
        print('  -', p)
    raise SystemExit(1)
print('Alles sluit: toetsblad, startbestand en verbetersleutel passen bij elkaar.')
print(f'Alle tien de functies en alle vijf de hulpfiches komen aan bod, de toets staat')
print(f'op {formulepunten + opmaakpunten} punten voor {minuten} minuten, en het toetsblad')
print('geeft nergens een formule weg.')
