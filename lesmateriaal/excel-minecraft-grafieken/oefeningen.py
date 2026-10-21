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

V1, V2, V3, V4, V5 = 5, 5, 5, 6, 11     # kolom van het vragenblok per blad

OEFENINGEN = [
    dict(
        nr=1, blad='1 Levenspunten', titel='Mobs vergelijken',
        duur='8 minuten', kaarten=[10, 12],
        inleiding=[
            f'{len(g.B1)} mobs met hun levenspunten, al gesorteerd van taai naar '
            'teer.',
            'De vraag is "wie houdt het langst vol?". Daar hoort één grafiektype '
            'bij.',
        ],
        grafiek=dict(
            soort=g.B1_SOORT, titel=g.B1_TITEL,
            selectie=f'A{g.B1_KOPRIJ}:A{g.B1_EIND} én '
                     f'C{g.B1_KOPRIJ}:C{g.B1_EIND} (Ctrl ingedrukt houden)',
            astitel_x='mob', astitel_y='levenspunten',
            legende='geen — er is maar één reeks', vanaf_nul=True),
        punten_grafiek=6,
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}', 'welke mob de langste balk heeft',
             a.B1_HOOGSTE, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'hoeveel levenspunten er tussen de langste en de kortste balk zitten',
             a.B1_VERSCHIL, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B1_REEKSEN, 1),
        ],
        klaar=f'{len(g.B1)} balken, van hoog naar laag, met een titel en twee '
              'astitels.',
        controle=f'De langste balk staat links en is ruim {int(a.B1_VERHOUDING)} '
                 'keer zo hoog als de kortste. Staat je grafiek door elkaar, dan '
                 'heb je de kolom Dimensie meegeselecteerd.',
        vast=[
            'Je krijgt Overworld en Nether onder je balken in plaats van '
            'mobnamen: je hebt kolom B meegeselecteerd. Selecteer A, hou Ctrl '
            'ingedrukt en selecteer C.',
            'Je balken hebben nummers in plaats van namen: je hebt alleen de '
            'getallen geselecteerd, zonder de kolom met de mobnamen.',
        ],
    ),
    dict(
        nr=2, blad='2 Diepte', titel='Een verloop met een piek',
        duur='10 minuten', kaarten=[11, 12, 14],
        inleiding=[
            f'Hoeveel diamanten je per 1000 afgegraven blokken vindt, gemeten op '
            f'{len(g.B2)} diepten tussen Y = {g.B2[0][0]} en Y = {g.B2[-1][0]}.',
            'Hier is de vraag niet "wie is de grootste?" maar "hoe verloopt het?". '
            'Dat is een ander type grafiek.',
            'Vul eerst de verschilkolom in, zodat je je grafiek kan controleren.',
        ],
        vullen=[(f'C{g.B2_START + 1}:C{g.B2_EIND}',
                 'het verschil met de vorige meting',
                 f'=B{g.B2_START + 1}-B{g.B2_START}', 2)],
        grafiek=dict(
            soort=g.B2_SOORT, titel=g.B2_TITEL,
            selectie=f'A{g.B2_KOPRIJ}:B{g.B2_EIND}',
            astitel_x='Y-niveau', astitel_y='diamanten per 1000 blokken',
            legende='geen — één reeks', vanaf_nul=True),
        punten_grafiek=6,
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'tussen welke twee Y-niveaus de vondst het sterkst steeg',
             f'{a.B2_GROOTSTE_VAN} en {a.B2_GROOTSTE_TOT}', 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}',
             'hoeveel diamanten dat scheelde', a.B2_GROOTSTE, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'hoeveel Y-niveaus er tussen de laatste twee metingen zitten',
             a.B2_LAATSTE_STAP, 1),
        ],
        klaar=f'Eén lijn met {len(g.B2)} punten die stijgt, piekt en dan terugvalt, '
              'met een titel en twee astitels.',
        controle=f'De som van je verschilkolom moet {a.B2_SOM_VERSCHIL} geven: het '
                 f'verschil tussen Y = {g.B2[0][0]} en Y = {g.B2[-1][0]}.',
        vast=[
            'Je grafiek heeft twee lijnen: je hebt de kolom met de Y-niveaus als '
            'reeks meegenomen. Haal die eruit bij Gegevens selecteren.',
            'Je lijn loopt onderaan plotseling steiler. Dat is geen fout van jou — '
            'kijk naar de afstand tussen de Y-niveaus op je as. Onderaan springt '
            f'ze per {a.B2_LAATSTE_STAP} niveaus, bovenaan per '
            f'{a.B2_GEWONE_STAP}.',
        ],
    ),
    dict(
        nr=3, blad='3 Ertsvondsten', titel='Een aandeel van een geheel',
        duur='8 minuten', kaarten=[11, 14],
        inleiding=[
            f'{a.B3_TOTAAL} gevonden ertsblokken, verdeeld over {len(g.B3)} '
            'soorten die samen het geheel vormen.',
            'Nu is de vraag "welk deel van het geheel?". Dat is het enige geval '
            'waarin een cirkeldiagram mag.',
        ],
        vullen=[(f'C{g.B3_START}:C{g.B3_EIND}', 'het aandeel in procent',
                 f'=B{g.B3_START}/SOM($B${g.B3_START}:$B${g.B3_EIND})', 2)],
        grafiek=dict(
            soort=g.B3_SOORT, titel=g.B3_TITEL,
            selectie=f'A{g.B3_KOPRIJ}:B{g.B3_EIND}',
            astitel_x=None, astitel_y=None,
            legende='ja, met de namen van de ertssoorten', vanaf_nul=None,
            labels='gegevenslabels met het percentage'),
        punten_grafiek=5,
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'welk aandeel de grootste soort heeft, in procent',
             round(a.B3_GROOTSTE_AANDEEL * 100), 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'welk grafiektype je zou nemen als er vijftien ertssoorten waren',
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
        nr=4, blad='4 Schade', titel='Drie reeksen in één grafiek',
        duur='10 minuten', kaarten=[12, 14],
        inleiding=[
            f'De schade per slag van {len(g.B4_WAPENS)} wapens in '
            f'{len(g.B4)} materialen.',
            'Drie reeksen in één grafiek. Nu heb je wél een legende nodig.',
            'En let op het type: de horizontale as is hier geen tijd maar een '
            'rijtje materialen. Een lijn tussen Steen en IJzer zou doen alsof er '
            'iets tussenin bestaat. Dat is er niet.',
        ],
        grafiek=dict(
            soort=g.B4_SOORT, titel=g.B4_TITEL,
            selectie=f'A{g.B4_KOPRIJ}:D{g.B4_EIND}',
            astitel_x='materiaal', astitel_y='schade per slag',
            legende=f'ja, met de {len(g.B4_WAPENS)} wapens', vanaf_nul=True),
        punten_grafiek=7,
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             f'welk wapen het meest wint als je van {g.B4[0][0].lower()} naar '
             f'{a.B4_BESTE_MATERIAAL.lower()} gaat', a.B4_MEESTE_WINST, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             f'welk wapen met {a.B4_BESTE_MATERIAAL.lower()} de meeste schade doet',
             a.B4_HOOGSTE_LAATST, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B4_REEKSEN, 1),
        ],
        klaar=f'Per materiaal {len(g.B4_WAPENS)} balken naast elkaar, met een '
              'legende, een titel en twee astitels, en een as die bij nul begint.',
        controle=f'Eén reeks blijft overal even hoog: de {a.B4_VLAK[0].lower()} '
                 'doet altijd 1 schade, wat je materiaal ook is. Loopt die bij jou '
                 'op, dan heb je een rij of een kolom verschoven.',
        vast=[
            f'De {a.B4_VLAK[0].lower()} lijkt helemaal te verdwijnen: dat komt '
            'omdat 1 naast 10 niets is. Dat is juist het punt — laat je as bij nul '
            'beginnen en zeg erbij dat kleine reeksen zo onzichtbaar worden.',
            'Je legende toont Reeks1, Reeks2, Reeks3: je hebt de koprij niet '
            'meegeselecteerd.',
        ],
    ),
    dict(
        nr=5, blad='5 Handel', titel='Eerst aanvullen, dan tekenen',
        duur='14 minuten', kaarten=[10, 13],
        inleiding=[
            f'{len(g.B5)} aanbiedingen van dorpelingen, maar er staat alleen een '
            'beroepcode bij. Vul eerst de twee laatste kolommen aan met '
            'VERT.ZOEKEN uit de beroepentabel ernaast.',
            'Daarna maak je een staafdiagram van de items en hun prijs. Let op: '
            'die twee kolommen staan niet naast elkaar.',
            'Klaar en nog tijd over? Maak er dan een draaigrafiek van: eerst een '
            'draaitabel van beroep en prijs, en daar een grafiek op. Kaart 13 '
            'legt uit hoe dat gaat, en je ziet meteen waarom dat handiger is zodra '
            'de lijst langer wordt.',
        ],
        vullen=[
            (f'D{g.B5_START}:D{g.B5_EIND}', 'het beroep',
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 2)}${g.B5_ZOEKRIJ + len(g.B5_BEROEPEN)};2;"
             "ONWAAR)", 2),
            (f'E{g.B5_START}:E{g.B5_EIND}', 'het werkblok',
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 2)}${g.B5_ZOEKRIJ + len(g.B5_BEROEPEN)};3;"
             "ONWAAR)", 2),
        ],
        grafiek=dict(
            soort=g.B5_SOORT, titel=g.B5_TITEL,
            selectie=f'A{g.B5_KOPRIJ}:A{g.B5_EIND} én '
                     f'C{g.B5_KOPRIJ}:C{g.B5_EIND} (Ctrl ingedrukt houden)',
            astitel_x='item', astitel_y='prijs in smaragden',
            legende='geen — één reeks', vanaf_nul=True),
        punten_grafiek=4,
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}', 'welk item het duurst is',
             a.B5_DUURSTE, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}',
             'bij welk beroep je dat item koopt', a.B5_DUURSTE_BEROEP, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}', 'hoeveel reeksen je grafiek heeft',
             a.B5_REEKSEN, 1),
        ],
        klaar=f'Twee volle kolommen zonder #N/B, en {len(g.B5)} balken met de '
              'namen van de items eronder.',
        controle=f'De hoogste balk is {a.B5_DUURSTE_PRIJS} smaragden. Staan er '
                 'beroepcodes onder je balken, dan heb je kolom B meegeselecteerd '
                 'in plaats van met Ctrl te werken.',
        vast=[
            'Onderaan kolom D staat #N/B: je beroepentabel is niet vastgezet. Zet '
            'er dollartekens om en voer opnieuw door.',
            'Onder je balken staan de beroepcodes: selecteer A, hou Ctrl ingedrukt '
            'en selecteer dan pas C.',
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
              f"{oef['grafiek']['soort']:<30} {punten} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
