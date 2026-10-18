# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad maakt. Alleen grafieken.

Geen theorie in deze bundel: elk blad verwijst naar de kaarten van
draaitabellen-en-grafieken.docx, waar elke kaart op een eigen pagina staat.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = _laad('g', 'gegevens.py')
a = _laad('a', 'antwoorden.py')


def _kol(n):
    uit = ''
    while n:
        n, r = divmod(n - 1, 26)
        uit = chr(65 + r) + uit
    return uit


KAARTEN = {
    10: 'Een grafiek invoegen',
    11: 'Welk type bij welke vraag?',
    12: 'Een grafiek leesbaar maken',
    13: 'Een draaigrafiek',
    14: 'Wat een grafiek kan verbergen',
}

V1, V2, V3, V4, V5 = 5, 5, 5, 6, 12     # kolom van het vragenblok per blad

OEFENINGEN = [
    dict(
        nr=1, blad='1 Toeschouwers', titel='Clubs vergelijken',
        duur='8 minuten', kaarten=[10, 12],
        inleiding=[
            f'{len(g.B1)} clubs met hun gemiddeld aantal toeschouwers, al '
            'gesorteerd van groot naar klein.',
            'De vraag is "wie is de grootste?". Daar hoort één grafiektype bij.',
        ],
        grafiek=dict(
            soort=g.B1_SOORT, titel=g.B1_TITEL,
            selectie=f'A{g.B1_KOPRIJ}:A{g.B1_EIND} én '
                     f'C{g.B1_KOPRIJ}:C{g.B1_EIND} (Ctrl ingedrukt houden)',
            astitel_x='club', astitel_y='toeschouwers',
            legende='geen — er is maar één reeks', vanaf_nul=True),
        punten_grafiek=6,
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}', 'welke club de langste balk heeft',
             a.B1_HOOGSTE, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'hoeveel toeschouwers er tussen de langste en de kortste balk zitten',
             a.B1_VERSCHIL, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B1_REEKSEN, 1),
        ],
        klaar='Tien balken, van hoog naar laag, met een titel en twee astitels.',
        controle='De langste balk staat links en is bijna drie keer zo hoog als de '
                 'kortste. Staat je grafiek door elkaar, dan heb je de kolom Stad '
                 'meegeselecteerd.',
        vast=[
            'Je krijgt steden in plaats van clubs onder je balken: je hebt kolom B '
            'meegeselecteerd. Selecteer A, hou Ctrl ingedrukt en selecteer C.',
            'Je balken hebben nummers in plaats van namen: je hebt alleen de '
            'getallen geselecteerd, zonder de kolom met de clubnamen.',
        ],
    ),
    dict(
        nr=2, blad='2 Bevolking', titel='Een verloop in de tijd',
        duur='10 minuten', kaarten=[11, 12, 14],
        inleiding=[
            f'De bevolking van Türkiye op {len(g.B2)} momenten tussen '
            f'{g.B2[0][0]} en {g.B2[-1][0]}.',
            'Hier is de vraag niet "wie is de grootste?" maar "hoe verloopt het?". '
            'Dat is een ander type grafiek.',
            'Vul eerst de groeikolom in, zodat je je grafiek kan controleren.',
        ],
        vullen=[(f'C{g.B2_START + 1}:C{g.B2_EIND}', 'de groei sinds de vorige meting',
                 f'=B{g.B2_START + 1}-B{g.B2_START}', 2)],
        grafiek=dict(
            soort=g.B2_SOORT, titel=g.B2_TITEL,
            selectie=f'A{g.B2_KOPRIJ}:B{g.B2_EIND}',
            astitel_x='jaar', astitel_y='miljoen inwoners',
            legende='geen — één reeks', vanaf_nul=True),
        punten_grafiek=6,
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'tussen welke twee jaren de bevolking het sterkst groeide',
             f'{a.B2_GROOTSTE_VAN} en {a.B2_GROOTSTE_TOT}', 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}', 'hoeveel miljoen dat was',
             a.B2_GROOTSTE, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'hoeveel jaar er tussen de laatste twee metingen zit',
             a.B2_LAATSTE_STAP, 1),
        ],
        klaar='Eén stijgende lijn met negen punten, een titel en twee astitels.',
        controle=f'De som van je groeikolom moet '
                 f'{a._getal(round(a.B2_INWONERS[-1] - a.B2_INWONERS[0], 1))} geven: '
                 f'het verschil tussen {g.B2[0][0]} en {g.B2[-1][0]}.',
        vast=[
            'Je grafiek heeft twee lijnen: je hebt de kolom met de jaartallen als '
            'reeks meegenomen. Haal die eruit bij Gegevens selecteren.',
            'Je lijn ziet er aan het einde vlakker uit. Dat is geen fout van jou — '
            'kijk naar de afstand tussen de laatste twee jaartallen.',
        ],
    ),
    dict(
        nr=3, blad='3 Export', titel='Een aandeel van een geheel',
        duur='8 minuten', kaarten=[11, 14],
        inleiding=[
            f'De export van Türkiye in {len(g.B3)} productgroepen die samen het '
            'geheel vormen.',
            'Nu is de vraag "welk deel van het geheel?". Dat is het enige geval '
            'waarin een cirkeldiagram mag.',
        ],
        vullen=[(f'C{g.B3_START}:C{g.B3_EIND}', 'het aandeel in procent',
                 f'=B{g.B3_START}/SOM($B${g.B3_START}:$B${g.B3_EIND})', 2)],
        grafiek=dict(
            soort=g.B3_SOORT, titel=g.B3_TITEL,
            selectie=f'A{g.B3_KOPRIJ}:B{g.B3_EIND}',
            astitel_x=None, astitel_y=None,
            legende='ja, met de namen van de productgroepen', vanaf_nul=None,
            labels='gegevenslabels met het percentage'),
        punten_grafiek=5,
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'welk aandeel de grootste groep heeft, in procent',
             round(a.B3_GROOTSTE_AANDEEL * 100), 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'welk grafiektype je zou nemen als er vijftien productgroepen waren',
             a.B3_BIJ_VEEL_DELEN, 1),
        ],
        klaar=f'Een cirkel van {len(g.B3)} taartpunten met een legende en de '
              'percentages erin.',
        controle='Je aandelen moeten samen 100 % geven. Doen ze dat niet, dan deel '
                 'je niet door het totaal of staat je deling niet vast.',
        vast=[
            'Je percentages veranderen als je doorvoert: zet het totaal vast met '
            'dollartekens.',
            'Je cirkel heeft maar één punt: je hebt de kolom met de namen niet '
            'meegeselecteerd.',
        ],
    ),
    dict(
        nr=4, blad='4 Toerisme', titel='Drie reeksen in één grafiek',
        duur='10 minuten', kaarten=[12, 14],
        inleiding=[
            f'Bezoekers uit {len(g.B4_LANDEN)} landen over {len(g.B4)} jaar.',
            'Drie reeksen in één grafiek. Nu heb je wél een legende nodig — en je '
            'moet opletten waar je verticale as begint.',
        ],
        grafiek=dict(
            soort=g.B4_SOORT, titel=g.B4_TITEL,
            selectie=f'A{g.B4_KOPRIJ}:D{g.B4_EIND}',
            astitel_x='jaar', astitel_y='bezoekers (miljoen)',
            legende='ja, met de drie landen', vanaf_nul=True),
        punten_grafiek=7,
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             f'welk land in {a.B4_VALJAAR} het sterkst terugviel',
             a.B4_GROOTSTE_VAL, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             f'welk land in {g.B4[-1][0]} het hoogst staat',
             a.B4_HOOGSTE_LAATST, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B4_REEKSEN, 1),
        ],
        klaar='Drie lijnen met een legende, een titel en twee astitels, en een as '
              'die bij nul begint.',
        controle='Alle drie de lijnen zakken in hetzelfde jaar diep weg en klimmen '
                 'daarna weer. Ziet één lijn er plat uit, dan staat je as niet bij '
                 'nul of heb je een reeks vergeten.',
        vast=[
            'Nederland lijkt een rechte lijn: dat komt omdat die getallen veel '
            'kleiner zijn. Dat is juist het punt — laat je as bij nul beginnen en '
            'zeg erbij dat kleine reeksen zo verdwijnen.',
            'Je legende toont Reeks1, Reeks2, Reeks3: je hebt de koprij niet '
            'meegeselecteerd.',
        ],
    ),
    dict(
        nr=5, blad='5 Topscorers', titel='Eerst aanvullen, dan tekenen',
        duur='14 minuten', kaarten=[10, 13],
        inleiding=[
            f'{len(g.B5)} topscorers, maar er staat alleen een clubcode bij. Vul '
            'eerst de twee laatste kolommen aan met VERT.ZOEKEN uit de clubtabel '
            'ernaast.',
            'Daarna maak je een staafdiagram van de spelers en hun doelpunten. Let '
            'op: die twee kolommen staan niet naast elkaar.',
        ],
        vullen=[
            (f'D{g.B5_START}:D{g.B5_EIND}', 'de naam van de club',
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 2)}${g.B5_ZOEKRIJ + len(g.B1)};2;ONWAAR)", 2),
            (f'E{g.B5_START}:E{g.B5_EIND}', 'de stad',
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 2)}${g.B5_ZOEKRIJ + len(g.B1)};3;ONWAAR)", 2),
        ],
        grafiek=dict(
            soort=g.B5_SOORT, titel=g.B5_TITEL,
            selectie=f'A{g.B5_KOPRIJ}:A{g.B5_EIND} én '
                     f'C{g.B5_KOPRIJ}:C{g.B5_EIND} (Ctrl ingedrukt houden)',
            astitel_x='speler', astitel_y='doelpunten',
            legende='geen — één reeks', vanaf_nul=True),
        punten_grafiek=4,
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}', 'wie de meeste doelpunten maakte',
             a.B5_TOPSCORER, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}', 'bij welke club die speler zit',
             a.B5_TOPSCORER_CLUB, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B5_REEKSEN, 1),
        ],
        klaar='Twee volle kolommen zonder #N/B, en twaalf balken met de namen van '
              'de spelers eronder.',
        controle=f'De hoogste balk is {a.B5_TOPSCORER_DOELPUNTEN} doelpunten. Staan '
                 'er clubcodes onder je balken, dan heb je kolom B meegeselecteerd '
                 'in plaats van met Ctrl te werken.',
        vast=[
            'Onderaan kolom D staat #N/B: je clubtabel is niet vastgezet. Zet er '
            'dollartekens om en voer opnieuw door.',
            'Onder je balken staan de clubcodes: selecteer A, hou Ctrl ingedrukt en '
            'selecteer dan pas C.',
        ],
    ),
]

TOTAAL = sum(oef['punten_grafiek']
             + sum(p for *_, p in oef['vragen'])
             + sum(p for *_, p in oef.get('vullen', []))
             for oef in OEFENINGEN)

if __name__ == '__main__':
    for oef in OEFENINGEN:
        punten = (oef['punten_grafiek'] + sum(p for *_, p in oef['vragen'])
                  + sum(p for *_, p in oef.get('vullen', [])))
        print(f"blad {oef['nr']}  {oef['blad']:<16} {oef['duur']:<12} "
              f"kaart {', '.join(str(k) for k in oef['kaarten']):<10} "
              f"{oef['grafiek']['soort']:<28} {punten} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
