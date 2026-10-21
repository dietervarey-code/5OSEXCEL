# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad maakt. Alleen draaitabellen.

In deze bundel staat GEEN theorie. Elk blad verwijst naar de kaarten in
draaitabellen-en-grafieken.docx; daar staat elke kaart op een eigen pagina.
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


# de kaarten uit de theoriebundel, zoals ze daar heten
KAARTEN = {
    2: 'Eerst je lijst in orde brengen',
    3: 'Een draaitabel invoegen',
    4: 'Rijen en Waarden — je eerste draaitabel',
    5: 'Aantal of Som?',
    6: 'Een tweede richting: Kolommen',
    7: 'Sorteren en filteren',
    8: 'Groeperen',
    9: 'Vernieuwen',
}

V1, V2, V3 = 6, 6, 6        # kolom van het vragenblok op blad 1, 2, 3
V4, V5 = 7, 13              # blad 4 en blad 5 (blad 5 heeft een zoektabel)

OEFENINGEN = [
    dict(
        nr=1, blad='1 Mobs', titel='Mobs per dimensie', duur='6 minuten',
        kaarten=[3, 4],
        inleiding=[
            f'{len(g.B1)} mobs uit de Java-editie, met hun categorie, de dimensie '
            'waar ze thuishoren en hun levenspunten. Je vat de lijst samen per '
            'dimensie.',
            'Dit is de eenvoudigste draaitabel die bestaat: één veld in Rijen, één '
            'in Waarden. Meer niet.',
        ],
        draai=dict(rijen='Dimensie', kolommen=None, waarden='Mob',
                   bewerking='Aantal', tweede=None, sorteren=None,
                   anker=g.B1_ANKER),
        punten_draai=5,
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}',
             'in welke dimensie de meeste mobs thuishoren', a.D1_TOP, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'hoeveel mobs dat er zijn', a.D1_TOP_AANTAL, 1),
        ],
        klaar=f'Een draaitabel met {len(a.D1_LABELS)} regels en een eindtotaal.',
        controle=f'Het eindtotaal moet {a.D1_TOTAAL} zijn — evenveel als er mobs '
                 'in de lijst staan.',
        vast=[
            'Excel wil geen draaitabel maken: je hebt een cel buiten de lijst '
            'aangeklikt. Klik één cel IN de lijst aan en probeer opnieuw.',
            'Je krijgt getallen in plaats van een telling: sleep Mob naar Waarden, '
            'niet Levenspunten.',
        ],
    ),
    dict(
        nr=2, blad='2 Blokken', titel='Categorie tegenover gereedschap',
        duur='8 minuten', kaarten=[6, 5],
        inleiding=[
            f'{len(g.B2)} blokken met hun categorie, het gereedschap dat je nodig '
            'hebt om er iets aan over te houden, en hun hardheid. Nu gebruik je '
            'twee richtingen tegelijk.',
            'Een kruistabel beantwoordt niet "hoeveel per categorie" en "hoeveel '
            'per gereedschap", maar "hoeveel per categorie én gereedschap". Die '
            'derde vraag zie je alleen zo.',
        ],
        draai=dict(rijen='Categorie', kolommen='Gereedschap', waarden='Blok',
                   bewerking='Aantal', tweede=None, sorteren=None,
                   anker=g.B2_ANKER),
        punten_draai=6,
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'welk gereedschap je voor de meeste blokken nodig hebt',
             a.D2_VEELST_GEREEDSCHAP, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}',
             'hoeveel natuurlijke blokken je met een schep breekt',
             a.D2_NATUURLIJK_SCHEP, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'in welke categorie élk blok hetzelfde gereedschap vraagt',
             a.D2_EEN_GEREEDSCHAP, 1),
        ],
        klaar=f'Een tabel van {len(a.D2_RIJEN)} rijen bij {len(a.D2_KOLLEN)} '
              'kolommen, met rij- en kolomtotalen.',
        controle=f'Het eindtotaal rechtsonder moet {a.D2_TOTAAL} zijn. De onderste '
                 f'rij moet {", ".join(str(a.D2_KOLTOT[k]) for k in a.D2_KOLLEN)} '
                 'geven.',
        vast=[
            f'Er staan {a.D2_LEGE_VAKJES} lege vakjes in je tabel. Dat is geen '
            'fout: die combinaties komen niet voor. Zet er een streepje in via '
            'Draaitabelopties als je dat rustiger vindt lezen.',
            f'Je krijgt {len(g.B2)} kolommen in plaats van {len(a.D2_KOLLEN)}: '
            'je hebt een veld met te veel verschillende waarden in Kolommen '
            'gezet. Daar hoort Gereedschap.',
        ],
    ),
    dict(
        nr=3, blad='3 Gereedschap', titel='Duurzaamheid per materiaal',
        duur='8 minuten', kaarten=[5, 7],
        inleiding=[
            f'{len(g.B3)} stuks gereedschap: {len(g.B3_SOORTEN)} soorten in '
            f'{len(g.B3_MATERIALEN)} materialen. Nu tel je niet, maar tel je OP.',
            'Let op het kopje van je draaitabel. Staat er Aantal waar Som hoort, '
            f'dan krijg je {len(g.B3_SOORTEN)} op elke rij — want van elk materiaal '
            f'zijn er evenveel soorten. Daar zie je dus niets aan.',
        ],
        draai=dict(rijen='Materiaal', kolommen=None, waarden='Duurzaamheid',
                   bewerking='Som', tweede=None, sorteren='aflopend',
                   anker=g.B3_ANKER),
        punten_draai=6,
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'welk materiaal samen de hoogste duurzaamheid haalt', a.D3_TOP, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'hoeveel dat is', a.D3_TOP_DUURZAAMHEID, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 3}',
             'welk materiaal het laagst uitkomt', a.D3_LAAGSTE, 1),
        ],
        klaar=f'Een gesorteerde lijst van {len(g.B3_MATERIALEN)} materialen, '
              'hoogste bovenaan.',
        controle=f'Het eindtotaal moet {a._getal(a.D3_TOTAAL)} zijn. Staat er '
                 f'{len(g.B3)}, dan telt je draaitabel de stuks gereedschap in '
                 'plaats van hun duurzaamheid.',
        vast=[
            'Je draaitabel telt in plaats van op te tellen. Klik het veld in '
            'Waarden aan, kies Waardeveldinstellingen en zet het op Som.',
            'Sorteren lukt niet: rechtsklik op een GETAL in de kolom waarop je wil '
            'sorteren, niet op een materiaalnaam.',
        ],
    ),
    dict(
        nr=4, blad='4 Updates', titel='Updates per periode', duur='12 minuten',
        kaarten=[8, 5, 7],
        inleiding=[
            f'{len(g.B4)} grote updates van de Java-editie, met hun jaartal, hun '
            'hoofdthema en het aantal nieuwe blokken. '
            f'{len({r[2] for r in g.B4})} verschillende jaartallen geven '
            f'{len({r[2] for r in g.B4})} regels — daar zie je niets aan.',
            f'Daarom groepeer je de jaartallen per {g.B4_GROEP_PER}. En je zet twee '
            'velden in Waarden: het aantal én het gemiddelde.',
        ],
        draai=dict(rijen='Jaar', kolommen=None, waarden='Nieuwe blokken',
                   bewerking='Gemiddelde', tweede='Versie', sorteren=None,
                   anker=g.B4_ANKER,
                   groeperen=f'per {g.B4_GROEP_PER}, van {g.B4_GROEP_VAN} tot '
                             f'{g.B4_GROEP_TOT}'),
        punten_draai=8,
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             'in welke periode de meeste updates verschenen', a.D4_DRUKSTE, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             'hoeveel updates dat er zijn', a.D4_DRUKSTE_AANTAL, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 3}',
             f'hoeveel updates overblijven als je filtert op het hoofdthema '
             f'{a.D4_FILTER_THEMA}', a.D4_FILTER_AANTAL, 1),
        ],
        klaar=f'{len(a.D4_LABELS)} regels met een periode, een aantal en een '
              'gemiddelde — en daarna, met het filter aan, een kleinere tabel.',
        controle=f'Zonder filter moet het eindtotaal {a.D4_TOTAAL_AANTAL} updates '
                 f'geven en een gemiddelde van {a._getal(a.D4_TOTAAL_GEMIDDELD)}.',
        vast=[
            'Groeperen staat niet in het menu: je hebt rechtsgeklikt op een gewone '
            'cel in plaats van op een rijlabel met een jaartal.',
            'Je krijgt groepen als 2011 - 2015: laat Excel niet zelf beginnen. Vul '
            f'bij Beginnen bij {g.B4_GROEP_VAN} in.',
            'Na het filteren veranderen je getallen. Dat hoort: wat je wegfiltert '
            'telt niet meer mee. Zet het filter daarna weer af.',
        ],
    ),
    dict(
        nr=5, blad='5 Dorpelingen', titel='Eerst aanvullen, dan samenvatten',
        duur='16 minuten', kaarten=[2, 9],
        inleiding=[
            f'{len(g.B5)} dorpelingen, maar de lijst is nog niet compleet: er staat '
            'alleen een beroepcode. Een draaitabel kan niet groeperen op een kolom '
            'die er niet is.',
            'Je vult dus EERST de drie laatste kolommen aan met VERT.ZOEKEN uit de '
            'beroepentabel ernaast, en pas DAN maak je de draaitabel.',
            'Daarna leer je het belangrijkste wat er over draaitabellen te zeggen '
            'valt: ze rekenen niet vanzelf mee.',
        ],
        vullen=[
            (f'D{g.B5_START}:D{g.B5_EIND}', 'het beroep', 2,
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B5_BEROEPEN)};2;"
             "ONWAAR)", 2),
            (f'E{g.B5_START}:E{g.B5_EIND}', 'het werkblok', 3,
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B5_BEROEPEN)};3;"
             "ONWAAR)", 2),
            (f'F{g.B5_START}:F{g.B5_EIND}', 'de categorie', 4,
             f"=VERT.ZOEKEN(B{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B5_BEROEPEN)};4;"
             "ONWAAR)", 2),
        ],
        draai=dict(rijen='Categorie', kolommen=None, waarden='Aanbiedingen',
                   bewerking='Som', tweede=None, sorteren='aflopend',
                   anker=g.B5_ANKER),
        punten_draai=5,
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}',
             'welke categorie samen de meeste aanbiedingen heeft', a.D5_TOP, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}',
             'hoeveel aanbiedingen dat zijn', a.D5_TOP_AANBIEDINGEN, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}',
             'wat het eindtotaal is NADAT je de extra dorpeling hebt toegevoegd en '
             'je draaitabel hebt vernieuwd', a.D5_NA_TOTAAL, 1),
        ],
        extra=dict(rij=g.B5_EIND + 1, waarden=g.B5_EXTRA,
                   beroep=a.D5_EXTRA_BEROEP, categorie=a.D5_EXTRA_CATEGORIE),
        klaar='Drie volle kolommen zonder #N/B, en een draaitabel van '
              f'{len(a.D5)} categorieën waarin de extra dorpeling meegeteld is.',
        controle=f'Vóór de extra dorpeling is het eindtotaal '
                 f'{a._getal(a.D5_TOTAAL)} aanbiedingen, erna '
                 f'{a._getal(a.D5_NA_TOTAAL)}.',
        vast=[
            'Onderaan kolom D staat #N/B: je beroepentabel is niet vastgezet. Zet '
            'er dollartekens om en voer opnieuw door.',
            'Je draaitabel toont "(leeg)": kolom F is nog niet overal gevuld.',
            'De extra dorpeling staat er wel, maar niet in je draaitabel. '
            'Vernieuwen volstaat hier niet: je bronbereik loopt nog tot de oude '
            'laatste rij. Ga naar Draaitabel analyseren, Gegevensbron wijzigen, en '
            'rek het bereik één rij op.',
        ],
    ),
]

TOTAAL = sum(oef['punten_draai']
             + sum(p for *_, p in oef['vragen'])
             + sum(p for *_, p in oef.get('vullen', []))
             for oef in OEFENINGEN)

if __name__ == '__main__':
    for oef in OEFENINGEN:
        punten = (oef['punten_draai'] + sum(p for *_, p in oef['vragen'])
                  + sum(p for *_, p in oef.get('vullen', [])))
        kaarten = ', '.join(str(k) for k in oef['kaarten'])
        print(f"blad {oef['nr']}  {oef['blad']:<16} {oef['duur']:<12} "
              f"kaart {kaarten:<8} {punten} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
