# -*- coding: utf-8 -*-
"""Kijkt één ingeleverde basisbundel na.

    python3 -I nakijken.py <bestand.xlsx> "<naam>"

Twee cijfers, zoals afgesproken:

  8 punten voor het werk    — de 21 opdrachten en de 18 opmaakeisen samen,
                              naar verhouding van wat er juist is
  2 punten voor de inzet    — is het werk gemaakt, en is er met formules
                              gewerkt in plaats van met ingetypte getallen

Twee regels die overal gelden:

  Een cel is pas juist als er een FORMULE staat EN de uitkomst klopt. Een
  ingetypt getal dat toevallig klopt, is geen Excel.

  Wie verder rekent op een fout die hierboven al is aangerekend, verliest
  daar geen punten meer. Een fout telt één keer.
"""
import importlib.util
import json
import math
import os
import re
import sys
from openpyxl import load_workbook
from openpyxl.worksheet.formula import ArrayFormula

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v = _laad('v', 'verwachting.py')

PUNTEN_WERK = 8
PUNTEN_INZET = 2
TOLERANTIE = 1e-6        # alleen ruis van drijvende komma wegfilteren

# Een xlsx bewaart elke formule in het Engels, wat de leerling ook typte.
ENGELS = {'SOM': 'SUM', 'AFRONDEN': 'ROUND', 'MAX': 'MAX', 'MIN': 'MIN',
          'GEMIDDELDE': 'AVERAGE', 'AANTAL': 'COUNT', 'ALS': 'IF',
          'AANTAL.ALS': 'COUNTIF', 'SOM.ALS': 'SUMIF', 'VERT.ZOEKEN': 'VLOOKUP'}
VERWIJZING = re.compile(r'(\$?[A-Z]{1,3}\$?\d{1,4})(?::(\$?[A-Z]{1,3}\$?\d{1,4}))?')


# ------------------------------------------------------------- formules
def gebruikt_functie(formule, functie):
    """Staat de gevraagde functie erin? COUNT mag niet matchen op COUNTIF,
       dus er wordt op het haakje erachter gekeken."""
    if not functie or not isinstance(formule, str):
        return True
    engels = ENGELS.get(functie)
    return not engels or bool(
        re.search(rf'\b{re.escape(engels)}\s*\(', formule.upper()))


def spilkaart(ws):
    """Cellen die gevuld worden door een matrixformule elders. Zonder deze
       kaart lijkt de spill van Excel 365 op ingetypte getallen."""
    kaart = {}
    for rij in ws.iter_rows():
        for cel in rij:
            if isinstance(cel.value, ArrayFormula):
                tekst = cel.value.text or ''
                for c in cellen_veilig(str(cel.value.ref)):
                    kaart[c] = tekst
    return kaart


def formule_van(ws, cel, spill):
    waarde = ws[cel].value
    if isinstance(waarde, ArrayFormula):
        return waarde.text or ''
    if isinstance(waarde, str) and waarde.startswith('='):
        return waarde
    return spill.get(cel)


def kaal(formule):
    """Een formule zonder celadressen, om twee formules op hun VORM te
       vergelijken. =SOM(B5:B12) en =SOM(C5:C12) worden allebei =SOM(#:#)."""
    if not isinstance(formule, str):
        return ''
    return re.sub(r'\$?[A-Z]{1,3}\$?\d{1,4}', '#', formule.upper())


def cellen_veilig(bereik):
    try:
        return v.cellen_van(bereik)
    except (AttributeError, ValueError):
        return []


def verwezen_cellen(formule):
    uit = set()
    if not isinstance(formule, str):
        return uit
    for m in VERWIJZING.finditer(formule):
        links = m.group(1).replace('$', '')
        rechts = (m.group(2) or m.group(1)).replace('$', '')
        uit |= set(cellen_veilig(f'{links}:{rechts}'))
    return uit


def is_fout(waarde):
    return isinstance(waarde, str) and waarde.startswith('#')


def gelijk(gekregen, verwacht):
    """Getallen met marge, tekst zonder onderscheid tussen hoofd- en kleine
       letters. Een verwachte foutmelding mag elke foutmelding zijn: Excel
       schrijft #N/B of #N/A naargelang de taal."""
    if gekregen is None:
        return False
    if isinstance(verwacht, str) and verwacht.startswith('#'):
        return is_fout(gekregen)
    if isinstance(verwacht, (int, float)) and not isinstance(verwacht, bool):
        try:
            return abs(float(gekregen) - float(verwacht)) <= TOLERANTIE
        except (TypeError, ValueError):
            return False
    return str(gekregen).strip().lower() == str(verwacht).strip().lower()


def toon(x):
    if isinstance(x, float):
        return f'{x:.2f}'.rstrip('0').rstrip('.').replace('.', ',')
    return str(x)


def naar_half(x):
    """Naar beneden op een half punt. Nooit afronden naar boven: wie iets
       fout heeft, hoort niet het maximum te krijgen."""
    return math.floor(x * 2) / 2


# -------------------------------------------------------------- opmaak
def gevulde(ws, bereik):
    """Alleen de cellen waar iets in staat. Een eis als 'rij 17 vet' slaat op
       de gevulde cellen, niet op de lege plek ernaast."""
    return [c for c in cellen_veilig(bereik) if ws[c].value is not None]


def _over(ws, bereik, test):
    doel = gevulde(ws, bereik)
    return bool(doel) and all(test(ws[c]) for c in doel)


def notatie_is(ws, bereik, soort):
    def past(c):
        n = ws[c].number_format or 'General'
        if soort == 'valuta':
            return '€' in n or '[$' in n or 'EUR' in n.upper()
        return '%' in n
    doel = gevulde(ws, bereik)
    return bool(doel) and all(past(c) for c in doel)


def rand_rond(ws, bereik):
    lijst = cellen_veilig(bereik)
    kol = sorted({re.match(r'([A-Z]+)', c).group(1) for c in lijst})
    rij = sorted({int(re.match(r'[A-Z]+(\d+)', c).group(1)) for c in lijst})
    return (all(ws[f'{k}{rij[0]}'].border.top.style for k in kol)
            and all(ws[f'{k}{rij[-1]}'].border.bottom.style for k in kol)
            and all(ws[f'{kol[0]}{r}'].border.left.style for r in rij)
            and all(ws[f'{kol[-1]}{r}'].border.right.style for r in rij))


def vw_opmaak(ws, bereik):
    doel = set(cellen_veilig(bereik))
    for regel in ws.conditional_formatting:
        for stuk in str(regel.sqref).split():
            gedekt = set(cellen_veilig(stuk)) if ':' in stuk else {stuk}
            if doel & gedekt:
                return True
    return False


def breed_genoeg(ws, wsv, bereik):
    """Past de langste tekst in de kolom? Excel meet kolombreedte in tekens
       van het standaardlettertype, dus een ruwe vergelijking volstaat.

    Een kolom waar nog niets in staat, is niet 'breed genoeg': daar valt niets
    te beoordelen. Anders zou een leeg blad hier punten voor krijgen.
    """
    lijst = cellen_veilig(bereik)
    kolom = re.match(r'([A-Z]+)', lijst[0]).group(1)
    inhoud = [len(str(wsv[c].value)) for c in lijst if wsv[c].value is not None]
    if len(inhoud) < 2:                      # alleen de koptekst of niets
        return False
    breedte = ws.column_dimensions[kolom].width
    if breedte is None:
        breedte = 8.43                       # de standaardbreedte van Excel
    return breedte + 0.5 >= max(inhoud)


def blokkade(ws, juiste_rij):
    waar = ws.freeze_panes
    if not waar:
        return False, 'niets geblokkeerd'
    rij = int(re.match(r'[A-Z]+(\d+)', str(waar)).group(1))
    if rij == juiste_rij:
        return True, ''
    if rij < juiste_rij:
        return False, (f'geblokkeerd op {waar}, maar de koprij staat in rij '
                       f'{juiste_rij - 1} en schuift bij het scrollen toch weg')
    return True, (f'geblokkeerd op {waar} in plaats van op A{juiste_rij} — de '
                  'koprij blijft staan, maar de eerste rijen scrollen niet mee')


def doe_controle(ws, wsv, soort, bereik):
    if soort == 'vet':
        return _over(ws, bereik, lambda c: bool(c.font and c.font.bold)), ''
    if soort == 'vulling':
        return _over(ws, bereik, lambda c: bool(
            c.fill and c.fill.fill_type and c.fill.fill_type != 'none')), ''
    if soort == 'gecentreerd':
        return _over(ws, bereik, lambda c: bool(
            c.alignment and c.alignment.horizontal == 'center')), ''
    if soort in ('valuta', 'percentage'):
        return notatie_is(ws, bereik, soort), ''
    if soort == 'geen_valuta':
        # Een lege cel staat niet in valuta, maar dat is geen verdienste.
        if not gevulde(ws, bereik):
            return False, ''
        return not notatie_is(ws, bereik, 'valuta'), ''
    if soort == 'bovenrand':
        doel = gevulde(ws, bereik)
        return bool(doel) and all(ws[c].border.top.style for c in doel), ''
    if soort == 'rand_rond':
        return rand_rond(ws, bereik), ''
    if soort == 'vw_opmaak':
        gelukt = vw_opmaak(ws, bereik)
        elders = [str(r.sqref) for r in ws.conditional_formatting]
        bij = '' if gelukt or not elders else (
            f'er staat wel voorwaardelijke opmaak, maar op {", ".join(elders)}')
        return gelukt, bij
    if soort == 'blokkade':
        return blokkade(ws, int(bereik))
    if soort == 'breed':
        return breed_genoeg(ws, wsv, bereik), ''
    raise ValueError(soort)


# ------------------------------------------------------------- nakijken
def kijk_regel(ws, wsv, regel, spill):
    """Eén opdracht nakijken. Geeft het deel dat juist is plus opmerkingen."""
    formules, waarden, juist, leeg = {}, {}, [], []
    for cel, verwacht in zip(regel['cellen'], regel['waarden']):
        f = formule_van(ws, cel, spill)
        w = wsv[cel].value
        formules[cel], waarden[cel] = f, w
        if ws[cel].value is None and w is None:
            leeg.append(cel)
        klopt = gelijk(w, verwacht)
        heeft_formule = regel['getypt'] or f is not None
        juist.append(klopt and heeft_formule)

    deel = sum(juist) / len(juist)
    opmerkingen = []
    gemaakt = [c for c in regel['cellen'] if c not in leeg]

    if not gemaakt:
        return 0.0, ['niet gemaakt'], formules, waarden, leeg
    if leeg:
        opmerkingen.append(f'{len(leeg)} van de {len(regel["cellen"])} cellen '
                           'nog leeg')

    zonder = [c for c in gemaakt if not regel['getypt'] and formules[c] is None]
    if zonder:
        opmerkingen.append(f'in {len(zonder)} cel(len) staat een ingetypt '
                           f'antwoord in plaats van een formule: '
                           f'{", ".join(zonder[:4])}'
                           + ('…' if len(zonder) > 4 else ''))

    if regel['functie']:
        mist = [c for c in gemaakt if formules[c]
                and not gebruikt_functie(formules[c], regel['functie'])]
        if mist:
            opmerkingen.append(f'{regel["functie"]} ontbreekt in '
                               f'{len(mist)} cel(len)')

    vormen = {kaal(formules[c]) for c in gemaakt if formules[c]}
    if len(vormen) > 1 and len(regel['cellen']) > 1:
        opmerkingen.append('de formules zijn per cel apart getypt in plaats '
                           'van één keer doorgevoerd')

    # Alleen melden waar de UITKOMST fout is. Een cel waar het antwoord klopt
    # maar de formule ontbreekt, staat hierboven al — "geeft 8, verwacht 8"
    # zou daar alleen verwarring stichten.
    fout = [c for c, w in zip(regel['cellen'], regel['waarden'])
            if c not in leeg and not gelijk(waarden[c], w)]
    for c in fout[:2]:
        verwacht = regel['waarden'][regel['cellen'].index(c)]
        opmerkingen.append(f'{c} geeft {toon(waarden[c])}, verwacht '
                           f'{toon(verwacht)}')
    if len(fout) > 2:
        opmerkingen.append(f'… en nog {len(fout) - 2} cel(len) met een fout '
                           'antwoord')

    spaties = [c for c in gemaakt if isinstance(waarden[c], str)
               and waarden[c] != waarden[c].strip()]
    if spaties:
        opmerkingen.append(f'in {len(spaties)} cel(len) staat een spatie achter '
                           'de tekst — onzichtbaar, maar AANTAL.ALS vindt ze dan niet')

    return deel, opmerkingen, formules, waarden, leeg


def doorwerkend(blad_regels):
    """Een fout die hierboven al is aangerekend, telt niet opnieuw mee.

    Alleen als de formule zelf de juiste vorm heeft: wie de verkeerde cellen
    optelt, heeft een eigen fout en geen gevolgfout.
    """
    fout_cellen = set()
    for r in blad_regels:
        if r['deel'] < 1:
            for c, ok in zip(r['regel']['cellen'], r['juist_per_cel']):
                if not ok:
                    fout_cellen.add(c)
    for r in blad_regels:
        if r['deel'] >= 1 or not r['formules']:
            continue
        bronnen = set()
        for f in r['formules'].values():
            bronnen |= verwezen_cellen(f)
        geraakt = bronnen & fout_cellen
        if geraakt and r['deel'] < 1:
            r['gevolgfout'] = sorted(geraakt)[:3]
    return blad_regels


def nakijken(pad, naam):
    wbf = load_workbook(pad)
    wbw = load_workbook(pad, data_only=True)
    uit = dict(naam=naam, bestand=os.path.basename(pad), bladen=[],
               laatst_bewerkt_door=wbf.properties.lastModifiedBy,
               gewijzigd=str(wbf.properties.modified))

    behaald = aangeraakt = getypte_antwoorden = 0
    for blad, info in v.PER_BLAD.items():
        if blad not in wbf.sheetnames:
            uit['bladen'].append(dict(blad=blad, nr=info['nr'],
                                      ontbreekt=True, regels=[], opmaak=[]))
            continue
        ws, wsv = wbf[blad], wbw[blad]
        spill = spilkaart(ws)

        rapport = []
        for regel in info['regels']:
            deel, opm, formules, waarden, leeg = kijk_regel(ws, wsv, regel, spill)
            juist_per_cel = [gelijk(waarden[c], w) and
                             (regel['getypt'] or formules[c] is not None)
                             for c, w in zip(regel['cellen'], regel['waarden'])]
            rapport.append(dict(regel=regel, deel=deel, opmerkingen=opm,
                                formules=formules, juist_per_cel=juist_per_cel,
                                leeg=leeg, gevolgfout=None))
            if len(leeg) < len(regel['cellen']):
                aangeraakt += 1
            if not regel['getypt']:
                getypte_antwoorden += sum(
                    1 for c in regel['cellen']
                    if c not in leeg and formules[c] is None)

        rapport = doorwerkend(rapport)
        for r in rapport:
            if r['gevolgfout']:
                r['deel'] = 1.0
                r['opmerkingen'] = [
                    'de formule klopt, maar rekent verder op een fout die '
                    f'hierboven al is aangerekend ({", ".join(r["gevolgfout"])})'
                    ' — daarom hier geen aftrek']
            behaald += r['deel']

        opmaak = []
        for omschrijving, controles in info['opmaak']:
            gelukt, gemist, bij = [], [], []
            for label, soort, bereik in controles:
                ok, melding = doe_controle(ws, wsv, soort, bereik)
                (gelukt if ok else gemist).append(label)
                if melding:
                    bij.append(melding)
            deel = len(gelukt) / len(controles)
            behaald += deel
            opmaak.append(dict(wat=omschrijving, deel=deel, gemist=gemist,
                               opmerkingen=bij))

        uit['bladen'].append(dict(
            blad=blad, nr=info['nr'], ontbreekt=False,
            regels=[dict(waar=r['regel']['waar'], wat=r['regel']['wat'],
                         deel=r['deel'], opmerkingen=r['opmerkingen'],
                         formule=r['formules'].get(r['regel']['cellen'][0]))
                    for r in rapport],
            opmaak=opmaak))

    werk = naar_half(PUNTEN_WERK * behaald / v.AANTAL_EENHEDEN)
    inzet_ruw = PUNTEN_INZET * aangeraakt / v.AANTAL_FORMULES
    if getypte_antwoorden:
        inzet_ruw -= 0.5
    inzet = max(0.0, naar_half(inzet_ruw))

    uit.update(eenheden=round(behaald, 3), van=v.AANTAL_EENHEDEN,
               aangeraakt=aangeraakt, van_opdrachten=v.AANTAL_FORMULES,
               getypte_antwoorden=getypte_antwoorden,
               werk=werk, inzet=inzet, totaal=werk + inzet)
    return uit


def verslag(uit):
    print(f"=== {uit['naam']} — {uit['totaal']:g} / 10".replace('.', ','))
    print(f"    werk {uit['werk']:g}/{PUNTEN_WERK}  ·  "
          f"inzet {uit['inzet']:g}/{PUNTEN_INZET}".replace('.', ','))
    print(f"    {uit['eenheden']:g} van de {uit['van']} eenheden juist  ·  "
          f"{uit['aangeraakt']}/{uit['van_opdrachten']} opdrachten aangeraakt"
          .replace('.', ','))
    for blad in uit['bladen']:
        if blad['ontbreekt']:
            print(f"\n--- blad {blad['nr']} {blad['blad']}   ONTBREEKT")
            continue
        punt = sum(r['deel'] for r in blad['regels']) + \
            sum(o['deel'] for o in blad['opmaak'])
        van = len(blad['regels']) + len(blad['opmaak'])
        print(f"\n--- blad {blad['nr']} {blad['blad']}   "
              f"{punt:.2f}/{van}".replace('.', ','))
        for r in blad['regels']:
            vlag = ' ' if r['deel'] >= 1 else '!'
            print(f"  {vlag} {r['waar']:<9} {r['deel']*100:5.0f}%  "
                  f"{r['wat'][:44]}")
            if r['formule']:
                print(f"      {r['formule'][:70]}")
            for o in r['opmerkingen']:
                print(f"      · {o}")
        for o in blad['opmaak']:
            vlag = ' ' if o['deel'] >= 1 else '!'
            print(f"  {vlag} opmaak    {o['deel']*100:5.0f}%  {o['wat'][:44]}")
            if o['gemist']:
                print(f"      · mist: {', '.join(o['gemist'])}")
            for m in o['opmerkingen']:
                print(f"      · {m}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('gebruik: python3 -I nakijken.py <bestand.xlsx> "<naam>"')
    resultaat = nakijken(sys.argv[1], sys.argv[2])
    verslag(resultaat)
    doel = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),
                        re.sub(r'[^a-z0-9]+', '-', sys.argv[2].lower()).strip('-')
                        + '.json')
    with open(doel, 'w', encoding='utf-8') as fh:
        json.dump(resultaat, fh, ensure_ascii=False, indent=1, default=str)
    print('\nweggeschreven:', doel)
