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

V1, V2, V3 = 9, 8, 7        # kolom van het vragenblok op blad 1, 2, 3
V4, V5 = 8, 14              # blad 4 en blad 5 (blad 5 heeft een zoektabel)

OEFENINGEN = [
    dict(
        nr=1, blad='1 Süper Lig', titel='Clubs per regio', duur='6 minuten',
        kaarten=[3, 4],
        inleiding=[
            f'{len(g.B1)} clubs uit de Süper Lig, met hun stad en de regio waarin '
            'die stad ligt. Je vat de lijst samen per regio.',
            'Dit is de eenvoudigste draaitabel die bestaat: één veld in Rijen, één '
            'in Waarden. Meer niet.',
        ],
        draai=dict(rijen='Regio', kolommen=None, waarden='Club',
                   bewerking='Aantal', tweede=None, sorteren=None,
                   anker=g.B1_ANKER),
        punten_draai=5,
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}',
             'welke regio de meeste clubs heeft', a.D1_TOP, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'hoeveel clubs dat er zijn', a.D1_TOP_AANTAL, 1),
        ],
        klaar=f'Een draaitabel met {len(a.D1_LABELS)} regels en een eindtotaal.',
        controle=f'Het eindtotaal moet {a.D1_TOTAAL} zijn — evenveel als er clubs '
                 'in de lijst staan.',
        vast=[
            'Excel wil geen draaitabel maken: je hebt een cel buiten de lijst '
            'aangeklikt. Klik één cel IN de lijst aan en probeer opnieuw.',
            'Je krijgt getallen in plaats van een telling: sleep Club naar Waarden, '
            'niet Opgericht of Punten.',
        ],
    ),
    dict(
        nr=2, blad='2 Keuken', titel='Soort tegenover pittig', duur='8 minuten',
        kaarten=[6, 5],
        inleiding=[
            f'{len(g.B2)} gerechten met hun soort, hun streek en of ze pittig zijn. '
            'Nu gebruik je twee richtingen tegelijk.',
            'Een kruistabel beantwoordt niet "hoeveel per soort" en "hoeveel pittig", '
            'maar "hoeveel per soort én pittig". Die derde vraag zie je alleen zo.',
        ],
        draai=dict(rijen='Soort', kolommen='Pittig', waarden='Gerecht',
                   bewerking='Aantal', tweede=None, sorteren=None,
                   anker=g.B2_ANKER),
        punten_draai=6,
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'welke soort de meeste pittige gerechten heeft', a.D2_TOP_PITTIG, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}',
             'hoeveel niet-pittige nagerechten er zijn', a.D2_NAGERECHT_NIET, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'welke soort geen enkel pittig gerecht bevat',
             a.D2_ZONDER_PITTIG[0], 1),
        ],
        klaar=f'Een tabel van {len(a.D2_RIJEN)} rijen bij {len(a.D2_KOLLEN)} '
              'kolommen, met rij- en kolomtotalen.',
        controle=f'Het eindtotaal rechtsonder moet {a.D2_TOTAAL} zijn. De onderste '
                 f'rij moet {a.D2_KOLTOT["ja"]} en {a.D2_KOLTOT["nee"]} geven.',
        vast=[
            'Eén vakje in je tabel is leeg. Dat is geen fout: die combinatie komt '
            'niet voor. Zet er een streepje in via Draaitabelopties als je dat '
            'rustiger vindt lezen.',
            'Je krijgt vier kolommen in plaats van twee: je hebt een veld met te '
            'veel verschillende waarden in Kolommen gezet. Daar hoort Pittig.',
        ],
    ),
    dict(
        nr=3, blad='3 Provincies', titel='Inwoners per regio', duur='8 minuten',
        kaarten=[5, 7],
        inleiding=[
            f'De {len(g.B3)} grootste provincies van Türkiye. Nu tel je niet, maar '
            'tel je OP.',
            'Let op het kopje van je draaitabel. Staat er Aantal waar Som hoort, dan '
            'krijg je het aantal provincies in plaats van het aantal inwoners.',
        ],
        draai=dict(rijen='Regio', kolommen=None, waarden='Inwoners',
                   bewerking='Som', tweede=None, sorteren='aflopend',
                   anker=g.B3_ANKER),
        punten_draai=6,
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'welke regio de meeste inwoners telt', a.D3_TOP, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'hoeveel inwoners dat zijn', a.D3_TOP_INWONERS, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 3}',
             'welke regio de minste inwoners telt', a.D3_LAAGSTE, 1),
        ],
        klaar='Een gesorteerde lijst van zeven regio\'s, grootste bovenaan.',
        controle=f'Het eindtotaal moet {a._getal(a.D3_TOTAAL)} zijn. Staat er '
                 f'{len(g.B3)}, dan telt je draaitabel de provincies in plaats van '
                 'de inwoners op.',
        vast=[
            'Je draaitabel telt in plaats van op te tellen. Klik het veld in '
            'Waarden aan, kies Waardeveldinstellingen en zet het op Som.',
            'Sorteren lukt niet: rechtsklik op een GETAL in de kolom waarop je wil '
            'sorteren, niet op een regionaam.',
        ],
    ),
    dict(
        nr=4, blad='4 Series', titel='Series per decennium', duur='12 minuten',
        kaarten=[8, 5, 7],
        inleiding=[
            f'{len(g.B4)} Turkse series met hun genre, startjaar en kijkcijfer. '
            'Twintig startjaren geven twintig regels — daar zie je niets aan.',
            'Daarom groepeer je de jaartallen per tien. En je zet twee velden in '
            'Waarden: het aantal én het gemiddelde.',
        ],
        draai=dict(rijen='Startjaar', kolommen=None, waarden='Kijkers (x1000)',
                   bewerking='Gemiddelde', tweede='Serie', sorteren=None,
                   anker=g.B4_ANKER,
                   groeperen=f'per {g.B4_GROEP_PER}, van {g.B4_GROEP_VAN} tot '
                             f'{g.B4_GROEP_TOT}'),
        punten_draai=8,
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             'in welk decennium de meeste series startten', a.D4_DRUKSTE, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             'hoeveel series dat er zijn', a.D4_DRUKSTE_AANTAL, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 3}',
             f'hoeveel series overblijven als je filtert op het genre '
             f'{a.D4_FILTER_GENRE}', a.D4_FILTER_AANTAL, 1),
        ],
        klaar='Drie regels met een decennium, een aantal en een gemiddelde — en '
              'daarna, met het filter aan, een kleinere tabel.',
        controle=f'Zonder filter moet het eindtotaal {a.D4_TOTAAL_AANTAL} series '
                 f'geven en een gemiddelde van {a._getal(a.D4_TOTAAL_GEMIDDELD)}.',
        vast=[
            'Groeperen staat niet in het menu: je hebt rechtsgeklikt op een gewone '
            'cel in plaats van op een rijlabel met een jaartal.',
            'Je krijgt groepen als 2003 - 2012: laat Excel niet zelf beginnen. Vul '
            f'bij Beginnen bij {g.B4_GROEP_VAN} in.',
            'Na het filteren veranderen je getallen. Dat hoort: wat je wegfiltert '
            'telt niet meer mee. Zet het filter daarna weer af.',
        ],
    ),
    dict(
        nr=5, blad='5 Transfers', titel='Eerst aanvullen, dan samenvatten',
        duur='16 minuten', kaarten=[2, 9],
        inleiding=[
            f'{len(g.B5)} transfers, maar de lijst is nog niet compleet: er staat '
            'alleen een clubcode. Een draaitabel kan niet groeperen op een kolom '
            'die er niet is.',
            'Je vult dus EERST de drie laatste kolommen aan met VERT.ZOEKEN uit de '
            'clubtabel ernaast, en pas DAN maak je de draaitabel.',
            'Daarna leer je het belangrijkste wat er over draaitabellen te zeggen '
            'valt: ze rekenen niet vanzelf mee.',
        ],
        vullen=[
            (f'E{g.B5_START}:E{g.B5_EIND}', 'de naam van de club', 2,
             f"=VERT.ZOEKEN(C{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B1)};2;ONWAAR)", 2),
            (f'F{g.B5_START}:F{g.B5_EIND}', 'de stad', 3,
             f"=VERT.ZOEKEN(C{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B1)};3;ONWAAR)", 2),
            (f'G{g.B5_START}:G{g.B5_EIND}', 'de regio', 4,
             f"=VERT.ZOEKEN(C{g.B5_START};${_kol(g.B5_ZOEKKOL)}${g.B5_ZOEKRIJ + 1}:"
             f"${_kol(g.B5_ZOEKKOL + 3)}${g.B5_ZOEKRIJ + len(g.B1)};4;ONWAAR)", 2),
        ],
        draai=dict(rijen='Regio', kolommen=None, waarden='Bedrag (milj. €)',
                   bewerking='Som', tweede=None, sorteren='aflopend',
                   anker=g.B5_ANKER),
        punten_draai=5,
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}',
             'naar welke regio het meeste geld ging', a.D5_TOP, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}',
             'hoeveel miljoen dat was', a.D5_TOP_BEDRAG, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}',
             'wat het eindtotaal is NADAT je de extra transfer hebt toegevoegd en '
             'je draaitabel hebt vernieuwd', a.D5_NA_TOTAAL, 1),
        ],
        extra=dict(rij=g.B5_EIND + 1, waarden=g.B5_EXTRA,
                   club=a.D5_EXTRA_CLUB, regio=g.club(g.B5_EXTRA[2])[2]),
        klaar='Drie volle kolommen zonder #N/B, en een draaitabel van vijf regio\'s '
              'waarin de extra transfer meegeteld is.',
        controle=f'Vóór de extra transfer is het eindtotaal '
                 f'{a._getal(a.D5_TOTAAL)} miljoen, erna '
                 f'{a._getal(a.D5_NA_TOTAAL)} miljoen.',
        vast=[
            'Onderaan kolom E staat #N/B: je zoektabel is niet vastgezet. Zet er '
            'dollartekens om en voer opnieuw door.',
            'Je draaitabel toont "(leeg)": kolom G is nog niet overal gevuld.',
            'De extra transfer staat er wel, maar niet in je draaitabel. Vernieuwen '
            'volstaat hier niet: je bronbereik loopt nog tot de oude laatste rij. '
            'Ga naar Draaitabel analyseren, Gegevensbron wijzigen, en rek het '
            'bereik één rij op.',
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
        print(f"blad {oef['nr']}  {oef['blad']:<14} {oef['duur']:<12} "
              f"kaart {kaarten:<8} {punten} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
