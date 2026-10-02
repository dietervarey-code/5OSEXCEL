# -*- coding: utf-8 -*-
"""Rekent alle antwoorden uit, precies zoals Excel het zou doen."""
import importlib.util
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HIER, 'gegevens.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)


def afronden(x, n=2):
    """Zoals AFRONDEN in Excel: halve eenheden naar boven."""
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * n), rounding=ROUND_HALF_UP))


# --- blad 1: boekingen -------------------------------------------------
B1_PRIJS = [g.tarief(personen) for _, _, personen, _, _ in g.B1]
B1_BEDRAG = [afronden(personen * prijs)
             for (_, _, personen, _, _), prijs in zip(g.B1, B1_PRIJS)]

B1_BEZOEKERS = sum(personen for _, _, personen, _, _ in g.B1)
B1_OMZET = afronden(sum(B1_BEDRAG))
# SOMMEN.ALS: online EN minstens tien personen
B1_OMZET_ONLINE_GROOT = afronden(sum(
    bedrag for (_, _, personen, _, kanaal), bedrag in zip(g.B1, B1_BEDRAG)
    if kanaal == 'online' and personen >= g.B1_GROOT))
# AANTALLEN.ALS: aan de kassa EN minder dan vijf personen
B1_KASSA_KLEIN = sum(1 for _, _, personen, _, kanaal in g.B1
                     if kanaal == 'kassa' and personen < g.B1_KLEIN)
# GEMIDDELDE.ALS: gemiddelde groepsgrootte van de online boekingen
_online = [personen for _, _, personen, _, kanaal in g.B1 if kanaal == 'online']
B1_GEM_ONLINE = afronden(sum(_online) / len(_online), 2)
B1_GROOTSTE = max(personen for _, _, personen, _, _ in g.B1)
B1_GROOTSTE_NAAM = next(groep for _, groep, personen, _, _ in g.B1
                        if personen == B1_GROOTSTE)

# --- blad 2: attracties ------------------------------------------------
B2_RIJTOTAAL = [sum(waarden) for _, waarden in g.B2]
B2_UURTOTAAL = [sum(waarden[i] for _, waarden in g.B2) for i in range(len(g.B2_UREN))]
B2_ALLES = sum(B2_RIJTOTAAL)
B2_DRUKSTE = max(B2_RIJTOTAAL)
B2_DRUKSTE_NAAM = g.B2[B2_RIJTOTAAL.index(B2_DRUKSTE)][0]
B2_DRUKSTE_UUR = g.B2_UREN[B2_UURTOTAAL.index(max(B2_UURTOTAAL))]
_tweede = sorted(B2_RIJTOTAAL, reverse=True)[1]
B2_TWEEDE_NAAM = g.B2[B2_RIJTOTAAL.index(_tweede)][0]
B2_AANDEEL = afronden(B2_DRUKSTE / B2_ALLES, 4)

# --- blad 3: ploegen ---------------------------------------------------
B3_UREN = [afronden(g.duur_in_uren(start, einde), 2)
           for _, _, _, start, einde in g.B3]
B3_NACHT = ['ja' if (einde > g.B3_GRENS_TIJD and uren >= g.B3_GRENS_UREN) else 'nee'
            for (_, _, _, _, einde), uren in zip(g.B3, B3_UREN)]
B3_AANTAL_ROL = sum(1 for _, rol, _, _, _ in g.B3 if rol == g.B3_ROL_TELLEN)
B3_AANTAL_NACHT = B3_NACHT.count('ja')
B3_KRUIS = sum(1 for _, rol, post, _, _ in g.B3
               if (rol, post) == g.B3_ROL_KRUIS)
B3_TOTAAL_UREN = afronden(sum(B3_UREN), 2)
_gids = [u for (_, rol, _, _, _), u in zip(g.B3, B3_UREN) if rol == g.B3_ROL_TELLEN]
B3_GEM_ROL = afronden(sum(_gids) / len(_gids), 2)
B3_LANGSTE = max(B3_UREN)
B3_LANGSTE_NAAM = g.B3[B3_UREN.index(B3_LANGSTE)][0]

# --- blad 4: verdachten ------------------------------------------------
_einde = {naam: einde for naam, _, _, _, einde in g.B3}
B4_EINDE = [_einde[naam] for naam, *_ in g.B4]
B4_OORDEEL = []
for (naam, badge, kostuum, tas, alibi), einde in zip(g.B4, B4_EINDE):
    mogelijk = (einde > g.B4_TIJDSTIP and badge >= 1 and kostuum == g.B4_KLEUR
                and tas == 'ja' and alibi == 'geen')
    B4_OORDEEL.append(g.B4_MOGELIJK if mogelijk else g.B4_UITGESLOTEN)
B4_AANTAL_OVER = B4_OORDEEL.count(g.B4_MOGELIJK)
B4_DADER = (g.B4[B4_OORDEEL.index(g.B4_MOGELIJK)][0]
            if B4_AANTAL_OVER == 1 else None)
# Waarom valt elke andere verdachte af? Dat staat in de lerarensleutel.
B4_REDEN = []
for (naam, badge, kostuum, tas, alibi), einde, oordeel in zip(g.B4, B4_EINDE, B4_OORDEEL):
    redenen = []
    if not einde > g.B4_TIJDSTIP:
        redenen.append(f'dienst eindigde om {einde.strftime("%H:%M")}, niet later dan '
                       f'{g.B4_TIJDSTIP.strftime("%H:%M")}')
    if badge < 1:
        redenen.append('geen enkele badgescan in dat uur')
    if kostuum != g.B4_KLEUR:
        redenen.append(f'kostuum was {kostuum}, geen {g.B4_KLEUR}')
    if tas != 'ja':
        redenen.append('had geen tas bij')
    if alibi != 'geen':
        redenen.append(f'alibi bevestigd door {alibi}')
    B4_REDEN.append((naam, oordeel, redenen))

# --- blad 5: afrekening ------------------------------------------------
B5_TICKETS = B1_OMZET
B5_OPBRENGST = afronden(B5_TICKETS + g.B5_BAROMZET)
B5_UREN = B3_TOTAAL_UREN
B5_LOONKOST = afronden(B5_UREN * g.B5_UURLOON)
B5_KOSTEN = afronden(B5_LOONKOST + g.B5_DECOR + g.B5_CATERING)
B5_WINST = afronden(B5_OPBRENGST - B5_KOSTEN)
B5_MARGE = afronden(B5_WINST / B5_OPBRENGST, 4)
B5_PER_BEZOEKER = afronden(B5_OPBRENGST / B1_BEZOEKERS)


if __name__ == '__main__':
    print('=== BLAD 1 — Boekingen ===')
    for (nr, groep, personen, slot, kanaal), prijs, bedrag in zip(g.B1, B1_PRIJS, B1_BEDRAG):
        print(f'   {nr}  {groep:22s} {personen:3d} x {prijs:6.2f} = {bedrag:8.2f}  '
              f'{slot} {kanaal}')
    print(f'   bezoekers                        {B1_BEZOEKERS}')
    print(f'   ticketomzet                      {B1_OMZET:.2f}')
    print(f'   omzet online vanaf {g.B1_GROOT} pers.      {B1_OMZET_ONLINE_GROOT:.2f}')
    print(f'   kassaboekingen onder {g.B1_KLEIN} pers.     {B1_KASSA_KLEIN}')
    print(f'   gemiddelde groepsgrootte online  {B1_GEM_ONLINE}')
    print(f'   grootste groep                   {B1_GROOTSTE} ({B1_GROOTSTE_NAAM})')

    print('\n=== BLAD 2 — Attracties ===')
    for (naam, waarden), totaal in zip(g.B2, B2_RIJTOTAAL):
        print(f'   {naam:14s} {waarden}  = {totaal}')
    print(f'   per uur: {dict(zip(g.B2_UREN, B2_UURTOTAAL))}')
    print(f'   alles samen {B2_ALLES}')
    print(f'   drukste attractie  {B2_DRUKSTE_NAAM} ({B2_DRUKSTE})')
    print(f'   drukste uur        {B2_DRUKSTE_UUR} ({max(B2_UURTOTAAL)})')
    print(f'   op één na drukste  {B2_TWEEDE_NAAM} ({_tweede})')
    print(f'   aandeel drukste    {B2_AANDEEL:.2%}')

    print('\n=== BLAD 3 — Ploegen ===')
    for (naam, rol, post, start, einde), uren, nacht in zip(g.B3, B3_UREN, B3_NACHT):
        print(f'   {naam:18s} {rol:9s} {post:13s} '
              f'{start.strftime("%H:%M")}-{einde.strftime("%H:%M")} {uren:5.2f} u  {nacht}')
    print(f'   aantal {g.B3_ROL_TELLEN.lower()}en          {B3_AANTAL_ROL}')
    print(f'   nachtploeg               {B3_AANTAL_NACHT}')
    print(f'   {g.B3_ROL_KRUIS[0]} op {g.B3_ROL_KRUIS[1]}  {B3_KRUIS}')
    print(f'   totaal gewerkte uren     {B3_TOTAAL_UREN}')
    print(f'   gemiddelde van de gidsen {B3_GEM_ROL}')
    print(f'   langste shift            {B3_LANGSTE} ({B3_LANGSTE_NAAM})')

    print('\n=== BLAD 4 — Verdachten ===')
    for naam, oordeel, redenen in B4_REDEN:
        uitleg = '; '.join(redenen) if redenen else 'alle vijf de getuigenissen passen'
        print(f'   {naam:18s} {oordeel:12s} {uitleg}')
    print(f'   blijft over: {B4_AANTAL_OVER}  →  {B4_DADER}')

    print('\n=== BLAD 5 — Afrekening ===')
    print(f'   ticketomzet      {B5_TICKETS:9.2f}')
    print(f'   baromzet         {g.B5_BAROMZET:9.2f}')
    print(f'   opbrengst        {B5_OPBRENGST:9.2f}')
    print(f'   uren x uurloon   {B5_UREN} x {g.B5_UURLOON} = {B5_LOONKOST:.2f}')
    print(f'   decor            {g.B5_DECOR:9.2f}')
    print(f'   catering         {g.B5_CATERING:9.2f}')
    print(f'   kosten           {B5_KOSTEN:9.2f}')
    print(f'   winst            {B5_WINST:9.2f}')
    print(f'   marge            {B5_MARGE:.2%}')
    print(f'   per bezoeker     {B5_PER_BEZOEKER:9.2f}')
