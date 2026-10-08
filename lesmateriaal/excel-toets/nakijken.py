# -*- coding: utf-8 -*-
"""Kijkt één ingeleverde toets na en schrijft het resultaat weg als JSON.

Gebruik:  python3 -I nakijken.py <bestand.xlsx> "<naam van de leerling>"

Twee dingen worden per cel nagegaan: staat er een FORMULE in (en geen
overgetypt getal), en klopt de UITKOMST. Allebei nodig voor de punten.

Wat het script met opzet NIET afstraft:
  * Engelse functienamen. Een xlsx bewaart elke formule in het Engels, ook
    als de leerling SOM typte. Uit het bestand is niet te zien welke taal
    hij gebruikte, dus daar kan niet op gequoteerd worden.
  * Een andere maar werkende formule. Er wordt op de uitkomst gekeken, niet
    op de letterlijke tekst.
  * Hoofdletters in ja/nee en dergelijke: Excel vergelijkt zelf ook zonder
    onderscheid.
  * B$2 in plaats van $B$2. Wie een kolom naar beneden doorvoert, heeft aan
    een vaste rij genoeg. De uitkomst bewijst of het werkt.
"""
import json
import os
import re
import sys
import importlib.util
from openpyxl import load_workbook

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v = _laad('v', 'verwachting.py')

TOLERANTIE = 0.005          # bedragen tot op een halve cent


# --------------------------------------------------------------- waarden
def gelijk(gekregen, verwacht):
    """Is dit hetzelfde antwoord? Getallen met marge, tekst zonder
       onderscheid tussen hoofd- en kleine letters."""
    if gekregen is None:
        return False
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


def kijk_regel(wb_f, wb_w, blad, regel):
    """Eén opdrachtcel of doorgevoerde kolom nakijken."""
    fs, ws = wb_f[blad], wb_w[blad]
    juist, zonder_formule, leeg, fout = [], [], [], []
    for cel, verwacht in zip(regel['cellen'], regel['waarden']):
        formule = fs[cel].value
        waarde = ws[cel].value
        heeft_formule = isinstance(formule, str) and formule.startswith('=')
        if formule is None and waarde is None:
            leeg.append(cel)
        elif not heeft_formule:
            (juist if gelijk(waarde if waarde is not None else formule, verwacht)
             else fout).append(cel)
            zonder_formule.append(cel)
        elif gelijk(waarde, verwacht):
            juist.append(cel)
        else:
            fout.append(cel)

    n = len(regel['cellen'])
    # Alleen cellen met een formule EN het juiste antwoord tellen mee.
    telt_mee = [c for c in juist if c not in zonder_formule]
    deel = len(telt_mee) / n
    if deel == 1:
        punten = regel['punten']
    elif deel >= 0.7:
        punten = round(regel['punten'] * deel * 2) / 2
    elif deel > 0:
        punten = round(regel['punten'] * deel * 2) / 2
    else:
        punten = 0

    if leeg and len(leeg) == n:
        opmerking = 'niet gemaakt'
    elif zonder_formule and not [c for c in zonder_formule if c in fout]:
        opmerking = (f'het antwoord klopt, maar in {len(zonder_formule)} cel(len) staat '
                     f'een ingetypt getal in plaats van een formule')
    elif not fout and not leeg:
        opmerking = 'juist'
    else:
        stuk = []
        if fout:
            eerste = fout[0]
            gekregen = wb_w[blad][eerste].value
            idx = regel['cellen'].index(eerste)
            stuk.append(f'fout vanaf {eerste} (daar staat {toon(gekregen)}, verwacht '
                        f"{toon(regel['waarden'][idx])})")
        if leeg:
            stuk.append(f'{len(leeg)} cel(len) leeg')
        opmerking = '; '.join(stuk)

    return dict(waar=regel['waar'], wat=regel['wat'], functie=regel['functie'],
                max=regel['punten'], punten=punten, aantal=n, juist=len(telt_mee),
                fout=fout[:4], leeg=len(leeg), zonder_formule=zonder_formule[:4],
                opmerking=opmerking,
                formule=fs[regel['cellen'][0]].value)


# ---------------------------------------------------------------- opmaak
def cellen(bereik):
    return v.cellen_van(bereik)


def vet(ws, bereik):
    return all(ws[c].font and ws[c].font.bold for c in cellen(bereik))


def vulling(ws, bereik):
    def gevuld(c):
        f = ws[c].fill
        return bool(f and f.fill_type and f.fill_type != 'none')
    return all(gevuld(c) for c in cellen(bereik))


def gecentreerd(ws, bereik):
    return all(ws[c].alignment and ws[c].alignment.horizontal == 'center'
               for c in cellen(bereik))


def rand_rond(ws, bereik):
    """Staat er langs alle vier de kanten van het blok een rand?"""
    lijst = cellen(bereik)
    kolommen = sorted({re.match(r'([A-Z]+)', c).group(1) for c in lijst})
    rijen = sorted({int(re.match(r'[A-Z]+(\d+)', c).group(1)) for c in lijst})
    boven = all(ws[f'{k}{rijen[0]}'].border.top.style for k in kolommen)
    onder = all(ws[f'{k}{rijen[-1]}'].border.bottom.style for k in kolommen)
    links = all(ws[f'{kolommen[0]}{r}'].border.left.style for r in rijen)
    rechts = all(ws[f'{kolommen[-1]}{r}'].border.right.style for r in rijen)
    return boven and onder and links and rechts


def bovenrand(ws, bereik):
    return all(ws[c].border.top.style for c in cellen(bereik))


def notatie(ws, bereik, soort):
    def past(c):
        n = (ws[c].number_format or 'General')
        if soort == 'valuta':
            return '€' in n or '[$' in n or 'EUR' in n.upper()
        if soort == 'percentage':
            return '%' in n
        if soort == 'decimaal1':
            m = re.search(r'\.(0+)', n)
            return bool(m) and len(m.group(1)) == 1
        if soort == 'duizend':
            return '#,##' in n or '# ##' in n
        raise ValueError(soort)
    return all(past(c) for c in cellen(bereik))


def vw_opmaak(ws, bereik):
    """Ligt er ergens voorwaardelijke opmaak over dit bereik?"""
    doel = set(cellen(bereik))
    for regel in ws.conditional_formatting:
        for stuk in str(regel.sqref).split():
            gedekt = set(cellen(stuk)) if ':' in stuk else {stuk}
            if doel & gedekt:
                return True
    return False


def blokkade(ws, juiste_rij):
    """Is de koprij geblokkeerd, en zo ja: op de juiste plaats?

    Het doel is dat de koprij blijft staan bij het scrollen. Dat lukt ook met
    een blokkade die te laag staat, maar dan scrollt de helft van de lijst
    niet mee. Het script geeft daar het punt wel voor en zet er een opmerking
    bij: of dat volstaat, beslist de leerkracht.
    """
    waar = ws.freeze_panes
    if not waar:
        return False, 'niets geblokkeerd'
    rij = int(re.match(r'[A-Z]+(\d+)', str(waar)).group(1))
    if rij == juiste_rij:
        return True, ''
    return True, (f'geblokkeerd op {waar} in plaats van op A{juiste_rij} — de koprij '
                  f'blijft wel staan, maar zo scrollen de eerste {rij - 1} rijen niet mee')


def score(onderdelen):
    """Deelpunten: hoeveel van de deelcontroles lukten, op een half punt na."""
    gelukt = [naam for naam, ok in onderdelen if ok]
    gemist = [naam for naam, ok in onderdelen if not ok]
    return len(gelukt) / len(onderdelen), gelukt, gemist


def kijk_opmaak(wb_f, blad, nr):
    """De opmaakeisen van één blad. Geeft per eis een score en wat er ontbreekt."""
    ws = wb_f[blad]
    eisen = v.PER_BLAD[blad]['opmaak']
    if nr == 1:
        controles = [
            [('koprij 4 vet', vet(ws, 'A4:F4')),
             ('koprij 4 achtergrondkleur', vulling(ws, 'A4:F4')),
             ('koprij 4 gecentreerd', gecentreerd(ws, 'A4:F4')),
             ('blok A28:B34 achtergrondkleur', vulling(ws, 'A28:B34'))],
            [('B30 op één decimaal', notatie(ws, 'B30', 'decimaal1')),
             ('koprij geblokkeerd', blokkade(ws, 5)[0])],
            [('voorwaardelijke opmaak op D5:D26', vw_opmaak(ws, 'D5:D26'))],
        ]
    elif nr == 2:
        controles = [
            [('koprij 3 vet', vet(ws, 'A3:G3')),
             ('koprij 3 achtergrondkleur', vulling(ws, 'A3:G3')),
             ('totaalrij 13 vet', vet(ws, 'A13:F13')),
             ('bovenrand op rij 13', bovenrand(ws, 'D13:F13')),
             ('rand rond A3:G13', rand_rond(ws, 'A3:G13'))],
            [('voorwaardelijke opmaak op G4:G11', vw_opmaak(ws, 'G4:G11')),
             ('B16 op één decimaal', notatie(ws, 'B16', 'decimaal1'))],
        ]
    elif nr == 3:
        controles = [
            [('koprij 3 vet', vet(ws, 'A3:D3')),
             ('koprij 3 achtergrondkleur', vulling(ws, 'A3:D3')),
             ('koprij 21 vet', vet(ws, 'A21:C21')),
             ('koprij 21 achtergrondkleur', vulling(ws, 'A21:C21'))],
            [('rand rond A21:C25', rand_rond(ws, 'A21:C25')),
             ('C27 vet', vet(ws, 'C27'))],
            [('voorwaardelijke opmaak op C4:C19', vw_opmaak(ws, 'C4:C19'))],
        ]
    elif nr == 4:
        controles = [
            [('B2 als percentage', notatie(ws, 'B2', 'percentage'))],
            [('B5:D14 als valuta', notatie(ws, 'B5:D14', 'valuta'))],
            [('koprij 4 vet', vet(ws, 'A4:D4')),
             ('koprij 4 achtergrondkleur', vulling(ws, 'A4:D4')),
             ('totaalrij 14 vet', vet(ws, 'A14:D14')),
             ('rand rond A4:D14', rand_rond(ws, 'A4:D14'))],
        ]
    else:
        controles = [
            [('koprij 3 vet', vet(ws, 'A3:D3')),
             ('koprij 3 achtergrondkleur', vulling(ws, 'A3:D3')),
             ('spelerslijst F3:H25 gevuld', vulling(ws, 'F3:H25')),
             ('rand rond F3:H25', rand_rond(ws, 'F3:H25'))],
            [('B18 op één decimaal', notatie(ws, 'B18', 'decimaal1')),
             ('kolom A gecentreerd', gecentreerd(ws, 'A4:A14')),
             ('kolom D gecentreerd', gecentreerd(ws, 'D4:D14'))],
        ]

    opmerkingen = []
    if nr == 1:
        _, melding = blokkade(ws, 5)
        if melding:
            opmerkingen.append(melding)

    uit = []
    for i, ((eis, punten), deelcontroles) in enumerate(zip(eisen, controles)):
        deel, gelukt, gemist = score(deelcontroles)
        uit.append(dict(eis=eis, max=punten, punten=round(punten * deel * 2) / 2,
                        gelukt=gelukt, gemist=gemist,
                        opmerking=opmerkingen[0] if (opmerkingen and i == 1
                                                     and nr == 1) else ''))
    return uit


# ------------------------------------------------------------------ main
def nakijken(pad, naam):
    wb_f = load_workbook(pad)
    wb_w = load_workbook(pad, data_only=True)
    ontbreekt = [b for b in v.PER_BLAD if b not in wb_f.sheetnames]
    if ontbreekt:
        raise SystemExit(f'deze werkbladen ontbreken in het bestand: {ontbreekt}')

    bladen = []
    for blad, info in v.PER_BLAD.items():
        regels = [kijk_regel(wb_f, wb_w, blad, r) for r in info['regels']]
        opmaak = kijk_opmaak(wb_f, blad, info['nr'])
        bladen.append(dict(
            nr=info['nr'], blad=blad, regels=regels, opmaak=opmaak,
            formulepunten=sum(r['punten'] for r in regels),
            formulemax=sum(r['max'] for r in regels),
            opmaakpunten=sum(e['punten'] for e in opmaak),
            opmaakmax=sum(e['max'] for e in opmaak),
        ))

    resultaat = dict(
        naam=naam, bestand=os.path.basename(pad), bladen=bladen,
        formulepunten=sum(b['formulepunten'] for b in bladen),
        formulemax=sum(b['formulemax'] for b in bladen),
        opmaakpunten=sum(b['opmaakpunten'] for b in bladen),
        opmaakmax=sum(b['opmaakmax'] for b in bladen),
    )
    resultaat['totaal'] = resultaat['formulepunten'] + resultaat['opmaakpunten']
    resultaat['maximum'] = resultaat['formulemax'] + resultaat['opmaakmax']
    return resultaat


def getal(x):
    return f'{x:g}'.replace('.', ',')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit('gebruik: python3 -I nakijken.py <bestand.xlsx> "<naam>"')
    r = nakijken(sys.argv[1], sys.argv[2])
    print(f"=== {r['naam']} — {getal(r['totaal'])} / {r['maximum']}")
    print(f"    formules {getal(r['formulepunten'])}/{r['formulemax']}  ·  "
          f"opmaak {getal(r['opmaakpunten'])}/{r['opmaakmax']}\n")
    for b in r['bladen']:
        print(f"--- blad {b['nr']} {b['blad']}   "
              f"{getal(b['formulepunten'] + b['opmaakpunten'])}/"
              f"{b['formulemax'] + b['opmaakmax']}")
        for x in b['regels']:
            vlag = ' ' if x['punten'] == x['max'] else '!'
            print(f"  {vlag} {x['waar']:9s} {getal(x['punten'])}/{x['max']}  "
                  f"{x['opmerking']}")
            if x['formule']:
                print(f"              {x['formule']}")
        for e in b['opmaak']:
            vlag = ' ' if e['punten'] == e['max'] else '!'
            tekort = ('; mist: ' + ', '.join(e['gemist'])) if e['gemist'] else ''
            print(f"  {vlag} opmaak    {getal(e['punten'])}/{e['max']}  "
                  f"{e['eis'][:60]}{tekort}")
            if e.get('opmerking'):
                print(f"              let op: {e['opmerking']}")
        print()
    uit = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),
                       re.sub(r'\W+', '-', r['naam'].lower()).strip('-') + '.json')
    with open(uit, 'w', encoding='utf-8') as fh:
        json.dump(r, fh, ensure_ascii=False, indent=1)
    print('weggeschreven:', uit)
