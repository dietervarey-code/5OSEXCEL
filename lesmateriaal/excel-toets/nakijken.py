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
from openpyxl.worksheet.formula import ArrayFormula

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v = _laad('v', 'verwachting.py')

# Alleen de ruis van drijvende komma wegfilteren, niets meer. Een halve cent
# marge zou op blad 4 net de fout wegmoffelen waar dat blad over gaat: wie
# niet afrondt krijgt 10,875 in plaats van 10,88, en dat verschil IS de fout.
TOLERANTIE = 1e-6


# Een xlsx bewaart elke formule in het Engels. Om na te gaan of de gevraagde
# functie gebruikt is, moet de Nederlandse naam dus eerst vertaald worden.
ENGELS = {'SOM': 'SUM', 'AFRONDEN': 'ROUND', 'MAX': 'MAX', 'MIN': 'MIN',
          'GEMIDDELDE': 'AVERAGE', 'AANTAL': 'COUNT', 'ALS': 'IF',
          'AANTAL.ALS': 'COUNTIF', 'SOM.ALS': 'SUMIF', 'VERT.ZOEKEN': 'VLOOKUP'}
VERWIJZING = re.compile(r'(\$?[A-Z]{1,3}\$?\d{1,4})(?::(\$?[A-Z]{1,3}\$?\d{1,4}))?')


def gebruikt_functie(formule, functie):
    """Staat de gevraagde functie in de formule? COUNT mag niet matchen op
       COUNTIF, dus er wordt op het haakje erachter gekeken."""
    if not functie or not isinstance(formule, str):
        return True
    engels = ENGELS.get(functie)
    if not engels:
        return True
    return re.search(rf'\b{re.escape(engels)}\s*\(', formule.upper()) is not None


def spilkaart(ws):
    """Welke cellen worden gevuld door een matrixformule elders?

    Een dynamische matrixformule (de 'spill' van Excel 365) staat maar in één
    cel; de rest van het bereik vult zichzelf. openpyxl geeft in die andere
    cellen alleen de uitkomst terug, en zonder deze kaart lijkt het alsof de
    leerling daar getallen heeft ingetypt. Dat is hij net niet.
    """
    kaart = {}
    for rij in ws.iter_rows():
        for cel in rij:
            if not isinstance(cel.value, ArrayFormula):
                continue
            tekst = cel.value.text or ''
            for c in cellen_van_veilig(str(cel.value.ref)):
                kaart[c] = (tekst, cel.coordinate)
    return kaart


def formule_van(ws, cel, spill):
    """De formule achter een cel, als tekst. None als er geen formule is."""
    waarde = ws[cel].value
    if isinstance(waarde, ArrayFormula):
        return waarde.text or ''
    if isinstance(waarde, str) and waarde.startswith('='):
        return waarde
    if cel in spill:
        return spill[cel][0]
    return None


def kaal(formule):
    """Een formule zonder celadressen, zodat twee formules te vergelijken zijn
       op hun vorm. =SOM(B5:B12) en =SOM(C5:C12) worden allebei =SOM(#:#)."""
    if not isinstance(formule, str):
        return ''
    return re.sub(r'\$?[A-Z]{1,3}\$?\d{1,4}', '#', formule.upper())


def losse_formules(formules, cellen):
    """Zijn dit losse, met de hand getypte formules in plaats van één
       doorgevoerde? Een doorgevoerde formule heeft overal dezelfde vorm;
       alleen de celadressen schuiven mee. Wie per rij iets anders intypt —
       bijvoorbeeld het criterium letterlijk — heeft een andere vorm per cel.
    """
    vormen = {kaal(formules.get(c)) for c in cellen if formules.get(c)}
    return len(vormen) > 1


def verwezen_cellen(formule):
    """Alle cellen waar een formule naar kijkt, bereiken uitgeschreven."""
    uit = set()
    if not isinstance(formule, str):
        return uit
    for m in VERWIJZING.finditer(formule):
        links = m.group(1).replace('$', '')
        rechts = (m.group(2) or m.group(1)).replace('$', '')
        uit |= set(cellen_van_veilig(f'{links}:{rechts}'))
    return uit


def cellen_van_veilig(bereik):
    try:
        return v.cellen_van(bereik)
    except (AttributeError, ValueError):
        return []


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


def toon(x, naast=None):
    """Een waarde leesbaar maken. Staat er een waarde naast waar ze op twee
       cijfers niet van te onderscheiden is, dan worden er meer cijfers
       getoond — anders leest een melding als 'daar staat 10,88, verwacht
       10,88' en begrijpt niemand er iets van."""
    if not isinstance(x, float):
        return str(x)
    cijfers = 2
    if isinstance(naast, (int, float)):
        while cijfers < 6 and f'{x:.{cijfers}f}' == f'{float(naast):.{cijfers}f}' \
                and abs(x - naast) > TOLERANTIE:
            cijfers += 1
    return f'{x:.{cijfers}f}'.rstrip('0').rstrip('.').replace('.', ',')


def kijk_regel(wb_f, wb_w, blad, regel, spill):
    """Eén opdrachtcel of doorgevoerde kolom nakijken."""
    fs, ws = wb_f[blad], wb_w[blad]
    juist, zonder_formule, leeg, fout = [], [], [], []
    for cel, verwacht in zip(regel['cellen'], regel['waarden']):
        formule = formule_van(fs, cel, spill)
        waarde = ws[cel].value
        heeft_formule = formule is not None
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

    # Een ALS-kolom met twee mogelijke uitkomsten kan helemaal omgekeerd
    # staan. Dan is 'fout vanaf de eerste rij' een nutteloze melding: wat hij
    # moet horen is dat hij de twee antwoorden verwisseld heeft.
    omgewisseld = False
    mogelijk = sorted({str(x) for x in regel['waarden']})
    if len(mogelijk) == 2 and len(fout) > len(juist):
        andersom = {mogelijk[0]: mogelijk[1], mogelijk[1]: mogelijk[0]}
        raak = sum(1 for cel, verwacht in zip(regel['cellen'], regel['waarden'])
                   if gelijk(ws[cel].value, andersom.get(str(verwacht))))
        omgewisseld = raak / len(regel['cellen']) >= 0.9

    n = len(regel['cellen'])
    # Alleen cellen met een formule EN het juiste antwoord tellen mee.
    telt_mee = [c for c in juist if c not in zonder_formule]
    deel = len(telt_mee) / n
    if deel == 1:
        punten = regel['punten']
    else:
        # Naar beneden afronden op een half punt, en nooit het maximum: wie
        # één cel fout heeft, hoort niet alles te krijgen. Bij een opdracht
        # van één punt betekent dat een half punt of niets.
        punten = min(int(regel['punten'] * deel * 2) / 2, regel['punten'] - 0.5)
        punten = max(punten, 0)

    if leeg and len(leeg) == n:
        opmerking = 'niet gemaakt'
    elif omgewisseld:
        opmerking = (f'de twee antwoorden staan omgewisseld: overal waar '
                     f'"{mogelijk[0]}" hoort staat "{mogelijk[1]}" en omgekeerd. '
                     'Je vergelijking staat de verkeerde kant op')
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
            verwacht = regel['waarden'][idx]
            stuk.append(f'fout vanaf {eerste} (daar staat '
                        f'{toon(gekregen, verwacht)}, verwacht '
                        f'{toon(verwacht, gekregen)})')
        if leeg:
            stuk.append(f'{len(leeg)} cel(len) leeg')
        opmerking = '; '.join(stuk)

    formules = {c: formule_van(fs, c, spill) for c in regel['cellen']}
    eerste_formule = formules[regel['cellen'][0]]
    # Een doorgevoerde formule hoort haar bereik vast te zetten. Wie dat niet
    # doet, kan toch het juiste antwoord krijgen als de gegevens toevallig
    # netjes gegroepeerd staan. Dat is het vermelden waard: bij een andere
    # volgorde loopt het mis.
    # Een matrixformule wordt niet doorgevoerd: ze staat één keer en vult zelf
    # het hele bereik. Praten over een bereik dat meeschuift slaat dan nergens
    # op.
    is_matrix = any(c in spill for c in regel['cellen'])
    schuift = (n > 1 and not is_matrix and '$' in (regel['formule'] or '')
               and isinstance(eerste_formule, str) and '$' not in eerste_formule)
    # Waar is de gevraagde functie blijven liggen? Niet overal: soms is een
    # andere functie even juist. Daarom een melding, geen aftrek.
    zonder_functie = [c for c in regel['cellen'] if formules[c]
                      and not gebruikt_functie(formules[c], regel['functie'])]

    handmatig = n > 1 and losse_formules(formules, regel['cellen'])

    return dict(waar=regel['waar'], wat=regel['wat'], functie=regel['functie'],
                max=regel['punten'], punten=punten, aantal=n, juist=len(telt_mee),
                fout=fout[:4], alle_fout=fout, leeg=len(leeg),
                zonder_formule=zonder_formule[:4],
                zonder_functie=zonder_functie[:4],
                aantal_zonder_functie=len(zonder_functie), schuift=schuift,
                omgewisseld=omgewisseld, handmatig=handmatig,
                opmerking=opmerking,
                formules=formules, formule=eerste_formule,
                matrix=is_matrix)


# ---------------------------------------------------------------- opmaak
def cellen(bereik):
    return v.cellen_van(bereik)


def gevulde_cellen(ws, bereik):
    """Alleen de cellen waar iets in staat.

    Een opmaakeis als 'B5:D14 in valuta' slaat op de getallen, niet op de
    lege tussenrij die daar toevallig in valt. Wie het blok netjes opmaakt
    maar die lege rij overslaat, doet precies wat gevraagd is.
    """
    return [c for c in cellen(bereik) if ws[c].value is not None]


def _over_gevulde(ws, bereik, test):
    doel = gevulde_cellen(ws, bereik)
    return bool(doel) and all(test(ws[c]) for c in doel)


def vet(ws, bereik):
    return _over_gevulde(ws, bereik, lambda cel: cel.font and cel.font.bold)


def vulling(ws, bereik):
    return _over_gevulde(ws, bereik, lambda cel: bool(
        cel.fill and cel.fill.fill_type and cel.fill.fill_type != 'none'))


def gecentreerd(ws, bereik):
    return _over_gevulde(ws, bereik, lambda cel: bool(
        cel.alignment and cel.alignment.horizontal == 'center'))


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
    doel = gevulde_cellen(ws, bereik)
    return bool(doel) and all(past(c) for c in doel)


def vw_elders(ws, bereik):
    """Staat er wel voorwaardelijke opmaak op het blad, maar op een ander
       bereik? Dan is 'ontbreekt' een misleidende melding."""
    if vw_opmaak(ws, bereik):
        return ''
    elders = [str(r.sqref) for r in ws.conditional_formatting]
    if not elders:
        return ''
    return (f'er staat wel voorwaardelijke opmaak op dit blad, maar op '
            f'{", ".join(elders)} in plaats van op {bereik}')


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
    if rij < juiste_rij:
        # Alles boven deze rij blijft staan. Ligt de blokkade bóven de koprij,
        # dan verdwijnt die koprij alsnog zodra je scrolt: het doel is niet
        # gehaald, ook al staat er een blokkade.
        return False, (f'geblokkeerd op {waar}, maar de koprij staat in rij '
                       f'{juiste_rij - 1}. Alleen de {rij - 1} rij(en) erboven blijven '
                       f'staan, dus de koprij schuift bij het scrollen toch weg')
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

    VW_BEREIK = {1: 'D5:D26', 2: 'G4:G11', 3: 'C4:C19'}
    bij_eis = {}
    if nr == 1:
        _, melding = blokkade(ws, 5)
        if melding:
            bij_eis[1] = melding
    if nr in VW_BEREIK:
        melding = vw_elders(ws, VW_BEREIK[nr])
        if melding:
            bij_eis[{1: 2, 2: 1, 3: 2}[nr]] = melding

    uit = []
    for i, ((eis, punten), deelcontroles) in enumerate(zip(eisen, controles)):
        deel, gelukt, gemist = score(deelcontroles)
        if deel == 1:
            behaald = punten
        else:
            behaald = max(min(int(punten * deel * 2 + 1e-9) / 2, punten - 0.5), 0)
        uit.append(dict(eis=eis, max=punten, punten=behaald,
                        gelukt=gelukt, gemist=gemist,
                        opmerking=bij_eis.get(i, '')))
    return uit


def doorwerkend(regels):
    """Een fout die doorwerkt één keer aanrekenen, niet twee keer.

    Wie op blad 4 vergeet af te ronden, krijgt een verkeerde kolom C én een
    verkeerd totaal in C14. Dat totaal is dan niet nog eens fout: de formule
    klopt, de invoer niet. Staat dat ook zo in de verbetersleutel.

    Een cel heet doorwerkend als ze verwijst naar een cel die bij een ANDERE
    opdracht van hetzelfde blad al fout gerekend is. Zijn alle foute cellen
    van een opdracht doorwerkend, dan komen de punten terug.
    """
    for regel in regels:
        regel['doorwerkend'] = False
    for regel in regels:
        if not regel['alle_fout'] or regel['punten'] == regel['max']:
            continue
        elders_fout = {c for ander in regels if ander is not regel
                       for c in ander['alle_fout']}
        if not elders_fout:
            continue
        oorzaken = set()
        for cel in regel['alle_fout']:
            geraakt = verwezen_cellen(regel['formules'].get(cel)) & elders_fout
            if not geraakt:
                break
            oorzaken |= geraakt
        else:
            regel['doorwerkend'] = True
            regel['punten'] = regel['max']
            regel['opmerking'] = (
                'de formule klopt, maar rekent verder op een fout die hierboven al '
                f'is aangerekend ({", ".join(sorted(oorzaken)[:3])}) — daarom hier '
                'geen aftrek')
    return regels


# ------------------------------------------------------------------ main
def nakijken(pad, naam):
    wb_f = load_workbook(pad)
    wb_w = load_workbook(pad, data_only=True)
    ontbreekt = [b for b in v.PER_BLAD if b not in wb_f.sheetnames]
    if ontbreekt:
        raise SystemExit(f'deze werkbladen ontbreken in het bestand: {ontbreekt}')

    bladen = []
    for blad, info in v.PER_BLAD.items():
        spill = spilkaart(wb_f[blad])
        regels = [kijk_regel(wb_f, wb_w, blad, r, spill) for r in info['regels']]
        doorwerkend(regels)
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
            if x['zonder_functie']:
                meer = ('…' if x['aantal_zonder_functie'] > len(x['zonder_functie'])
                        else '')
                print(f"              let op: {x['functie']} ontbreekt in "
                      f"{x['aantal_zonder_functie']} cel(len): "
                      f"{', '.join(x['zonder_functie'])}{meer}")
            if x['matrix']:
                print('              let op: matrixformule — één formule die het hele '
                      'bereik vult')
            if x['handmatig'] and x['punten'] == x['max']:
                print('              let op: losse formules per rij in plaats van er '
                      'één doorvoeren')
            if x['schuift'] and x['punten'] == x['max']:
                print('              let op: het bereik staat niet vast en schuift mee '
                      'bij het doorvoeren — hier kwam het toevallig goed uit')
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
