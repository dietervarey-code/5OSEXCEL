# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad moet maken, en hoe.

Zelfde opbouw als excel-ottomaans: blad 1 tot 3 zijn herhaling, blad 4 en 5
zijn de draaitabel en de grafiek. Wie die bundel gemaakt heeft, herkent elk
blad en kan sneller.

Elke regel noemt:
  waar     het celadres of het bereik dat de leerling vult
  wat      wat er moet komen, in gewone taal
  hoe      welke functie, of een van de nieuwe werkwijzen
  formule  de formule zoals ze hoort te zijn (voor de sleutel)
  punten   het gewicht bij de beoordeling
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

GEEN_FUNCTIE = 'een formule, geen functie'
SLEPEN = 'slepen, niet typen'
LEZEN = 'aflezen van je draaitabel'
TEKENEN = 'een grafiek, geen formule'

S1, E1 = g.B1_START, g.B1_EIND
S2, E2 = g.B2_START, g.B2_EIND
S3, E3 = g.B3_START, g.B3_EIND
S5, E5 = g.B5_START, g.B5_EIND
SAM = g.B1_SAMENVATTING
VK2, VK3, VK5 = g.B2_VRAAGRIJ, g.B3_VRAAGRIJ, g.B5_VRAAGRIJ
V4 = g.B4_VRAAGRIJ


def _kol(n):
    """1 -> A, 11 -> K. Zo staat er nergens een vaste kolomletter."""
    uit = ''
    while n:
        n, r = divmod(n - 1, 26)
        uit = chr(65 + r) + uit
    return uit


A2 = _kol(g.B2_VRAAGKOL + 1)     # waar de antwoorden van blad 2 komen
A3 = _kol(g.B3_VRAAGKOL + 1)
A4 = _kol(g.B4_VRAAGKOL + 1)
A5 = _kol(g.B5_VRAAGKOL + 1)

OEFENINGEN = [
    dict(
        nr=1, blad='1 Genres', titel='Negen genres', duur='8 minuten',
        inleiding=[
            'Een verzonnen peiling in de school: wat is je lievelingsgenre? Je '
            'vergelijkt 2024 met 2025 en vat de negen genres samen.',
            'Deze tabel is straks ook je ZOEKTABEL: op blad 2 haal je er met '
            'VERT.ZOEKEN gegevens uit. Verander er dus niets aan.',
        ],
        regels=[
            dict(waar=f'E{S1}:E{E1}', wat='de groei van elk genre',
                 hoe=GEEN_FUNCTIE, formule=f'=D{S1}-C{S1}', punten=2,
                 toelichting='Stemmen in 2025 min stemmen in 2024. Eén genre ging '
                             'erop achteruit, dus daar komt een negatief getal uit. '
                             'Dat is geen fout.'),
            dict(waar=f'F{S1}:F{E1}', wat='of dat genre sterk groeit',
                 hoe='ALS', formule=f'=ALS(E{S1}>=$B$3;"ja";"nee")', punten=2,
                 toelichting=f'De grens staat in B3 ({g.B1_DREMPEL} stemmen erbij). '
                             'Zet er dollartekens om, anders schuift de grens mee naar '
                             f'beneden. Let op: precies {g.B1_DREMPEL} telt ook mee.'),
            dict(waar=f'B{SAM}', wat='de totale groei over alle genres',
                 hoe='SOM', formule=f'=SOM(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 1}', wat='de gemiddelde groei',
                 hoe='GEMIDDELDE', formule=f'=GEMIDDELDE(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 2}', wat='de sterkste groei',
                 hoe='MAX', formule=f'=MAX(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 3}', wat='de zwakste groei',
                 hoe='MIN', formule=f'=MIN(E{S1}:E{E1})', punten=1,
                 toelichting='Hier komt een negatief getal uit. Klopt dat niet, dan '
                             'heb je ergens een typfout in kolom E.'),
            dict(waar=f'B{SAM + 4}', wat='het aantal genres in de tabel',
                 hoe='AANTAL', formule=f'=AANTAL(C{S1}:C{E1})', punten=1,
                 toelichting='Tel een kolom met getallen, niet met namen: AANTAL telt '
                             'alleen getallen.'),
            dict(waar=f'B{SAM + 5}', wat='het aantal sterk groeiende genres',
                 hoe='AANTAL.ALS', formule=f'=AANTAL.ALS(F{S1}:F{E1};"ja")', punten=1),
        ],
        opmaak=[
            (f'Koprij {g.B1_KOPRIJ} vet, met een achtergrondkleur en gecentreerd.', 1),
            (f'Het samenvattingsblok A{SAM}:B{SAM + 5} met een rand eromheen.', 1),
            (f'Voorwaardelijke opmaak op E{S1}:E{E1}: elke negatieve groei wordt '
             'rood.', 1),
        ],
        klaar='Een kolom met negen groeicijfers waarvan één negatief, een kolom met '
              'ja en nee, en zes getallen in een omrand blokje.',
        controle=f'B{SAM} moet {a.B1_SOM} geven en B{SAM + 1} precies '
                 f'{a.B1_GEMIDDELDE:g}. B{SAM + 5} moet {a.B1_STERKE} geven.',
        vast=[
            'Alle cellen in kolom F zeggen "nee": je bent de dollartekens om B3 '
            'vergeten, dus de grens schoof mee naar beneden.',
            f'B{SAM + 4} geeft 0: AANTAL telt alleen getallen. Richt ze op een kolom '
            'met stemmen, niet op de namen.',
            'Je MIN geeft 0 of een foutmelding: kijk na of kolom E echt tot de '
            f'laatste rij ({E1}) loopt.',
        ],
    ),
    dict(
        nr=2, blad='2 Aanbod', titel='Vijfendertig titels', duur='12 minuten',
        inleiding=[
            f'{len(g.B2)} series en films met hun soort, genrecode, taal, jaar en '
            'het aantal kijkers uit de verzonnen enquête. Je vult de drie laatste '
            'kolommen aan.',
            'Deze lijst wordt straks de bron van ALLEBEI je draaitabellen. Eén lijst, '
            'twee heel verschillende vragen — dat is precies waarvoor een draaitabel '
            'dient.',
            'Een draaitabel wil een kaarsrechte lijst: één koprij, geen lege rij '
            'ertussen en geen totaalrij eronder. Daarom staan de vier berekeningen '
            f'hiernaast, in kolom {_kol(g.B2_VRAAGKOL)}, met een lege kolom ertussen. '
            'Hou dat zo.',
        ],
        regels=[
            dict(waar=f'G{S2}:G{E2}', wat='de naam van het genre bij die code',
                 hoe='VERT.ZOEKEN', punten=3,
                 formule=f"=VERT.ZOEKEN(C{S2};'1 Genres'!$A${S1}:$F${E1};2;ONWAAR)",
                 toelichting='De zoektabel staat op blad 1. Zet ze vast met '
                             'dollartekens voordat je doorvoert, anders zakt de tabel '
                             'mee naar beneden en krijg je onderaan #N/B.'),
            dict(waar=f'H{S2}:H{E2}', wat='de groei van dat genre',
                 hoe='VERT.ZOEKEN', punten=3,
                 formule=f"=VERT.ZOEKEN(C{S2};'1 Genres'!$A${S1}:$F${E1};5;ONWAAR)",
                 toelichting='Dezelfde zoektabel, maar nu de vijfde kolom. Die heb je '
                             'op blad 1 zelf berekend — is blad 1 nog niet af, dan '
                             'staat hier niets zinnigs.'),
            dict(waar=f'I{S2}:I{E2}', wat='of de titel in een groeigenre zit',
                 hoe='ALS', punten=2,
                 formule=f'=ALS(H{S2}>={g.B1_DREMPEL};"ja";"nee")',
                 toelichting=f'Dezelfde grens als op blad 1: {g.B1_DREMPEL} of meer.'),
            dict(waar=f'{A2}{VK2 + 1}',
                 wat='het gemiddelde aantal kijkers per titel',
                 hoe='GEMIDDELDE', formule=f'=GEMIDDELDE(F{S2}:F{E2})', punten=1,
                 toelichting='Onthou dit getal. Je hebt het op blad 4 nodig als '
                             'controle van je tweede draaitabel.'),
            dict(waar=f'{A2}{VK2 + 2}', wat='het aantal titels in de lijst',
                 hoe='AANTAL', formule=f'=AANTAL(E{S2}:E{E2})', punten=1),
            dict(waar=f'{A2}{VK2 + 3}',
                 wat=f'het aantal titels van de soort {g.B2_TELSOORT}',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(B{S2}:B{E2};"{g.B2_TELSOORT}")'),
            dict(waar=f'{A2}{VK2 + 4}',
                 wat=f'het aantal {g.B2_TELTAAL}talige titels',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(D{S2}:D{E2};"{g.B2_TELTAAL}")'),
        ],
        opmaak=[
            (f'Koprij {g.B2_KOPRIJ} vet met een achtergrondkleur, en die koprij '
             'geblokkeerd zodat ze blijft staan als je naar beneden scrolt.', 1),
            ('Kolom A breed genoeg om elke titel helemaal te lezen, en kolom E en F '
             'gecentreerd.', 1),
        ],
        klaar='Drie volle kolommen tot de laatste rij, en vier getallen in het blokje '
              'ernaast. Nergens #N/B.',
        controle=f'Het gemiddelde moet {a.B2_GEMIDDELD:g} geven en de telling '
                 f'{a.B2_AANTAL}. De laatste rij ({E2}) hoort '
                 f'{a.B2_GENRE[-1]} te tonen.',
        vast=[
            'Onderaan kolom G staat #N/B: je zoektabel is niet vastgezet. Zet '
            'dollartekens rond het bereik en voer opnieuw door.',
            'Kolom G geeft overal hetzelfde genre: je hebt de code van de eerste rij '
            'vastgezet in plaats van de tabel. Alleen de TABEL krijgt dollartekens.',
            'Kolom H geeft 0: op blad 1 is kolom E nog leeg. Maak blad 1 eerst af.',
            'Je telling van de films geeft 0: let op de schrijfwijze. Excel is niet '
            'gevoelig voor hoofdletters, maar wel voor een spatie te veel.',
        ],
    ),
    dict(
        nr=3, blad='3 Schermtijd', titel='Twintig keer schermtijd',
        duur='10 minuten',
        inleiding=[
            f'Een verzonnen enquête bij {len(g.B3)} leerlingen: hoeveel minuten per '
            'dag zitten ze op een scherm, op een schooldag en op een weekenddag? Je '
            'rekent het om naar een week en vat samen.',
            'Een schoolweek telt vijf schooldagen en twee weekenddagen.',
        ],
        regels=[
            dict(waar=f'E{S3}:E{E3}', wat='de schermtijd per week',
                 hoe=GEEN_FUNCTIE, formule=f'=C{S3}*5+D{S3}*2', punten=2,
                 toelichting='Vijf schooldagen en twee weekenddagen. Let op de '
                             'volgorde: Excel vermenigvuldigt vanzelf vóór het '
                             'optelt, dus je hebt hier geen haakjes nodig.'),
            dict(waar=f'F{S3}:F{E3}', wat='of dat veel is',
                 hoe='ALS', formule=f'=ALS(E{S3}>=$B$3;"ja";"nee")', punten=2,
                 toelichting=f'De grens staat in B3 ({g.B3_DREMPEL} minuten per week, '
                             'dat is 25 uur). Dollartekens, zoals op blad 1. Twee '
                             'leerlingen zitten er precies op.'),
            dict(waar=f'{A3}{VK3 + 1}', wat='de totale schermtijd van de groep',
                 hoe='SOM', formule=f'=SOM(E{S3}:E{E3})', punten=1),
            dict(waar=f'{A3}{VK3 + 2}', wat='de gemiddelde schermtijd per week',
                 hoe='GEMIDDELDE', formule=f'=GEMIDDELDE(E{S3}:E{E3})', punten=1),
            dict(waar=f'{A3}{VK3 + 3}', wat='de hoogste schermtijd',
                 hoe='MAX', formule=f'=MAX(E{S3}:E{E3})', punten=1),
            dict(waar=f'{A3}{VK3 + 4}', wat='de laagste schermtijd',
                 hoe='MIN', formule=f'=MIN(E{S3}:E{E3})', punten=1),
            dict(waar=f'{A3}{VK3 + 5}', wat='het aantal leerlingen met veel schermtijd',
                 hoe='AANTAL.ALS', formule=f'=AANTAL.ALS(F{S3}:F{E3};"ja")', punten=1),
            dict(waar=f'{A3}{VK3 + 6}',
                 wat=f'de schermtijd van alle {g.B3_LEEFTIJD}-jarigen samen',
                 hoe='SOM.ALS', punten=2,
                 formule=f'=SOM.ALS(B{S3}:B{E3};{g.B3_LEEFTIJD};E{S3}:E{E3})',
                 toelichting='Let op de volgorde: eerst waar je kijkt, dan wat er moet '
                             'staan, dan wat je optelt.'),
            dict(waar=f'{A3}{VK3 + 7}',
                 wat='de schermtijd van iedereen die veel kijkt samen',
                 hoe='SOM.ALS', punten=2,
                 formule=f'=SOM.ALS(F{S3}:F{E3};"ja";E{S3}:E{E3})'),
        ],
        opmaak=[
            (f'Koprij {g.B3_KOPRIJ} vet met een achtergrondkleur, en kolom B tot E '
             'gecentreerd.', 1),
            (f'Voorwaardelijke opmaak op E{S3}:E{E3}: wie boven het gemiddelde zit, '
             'krijgt een kleur.', 1),
        ],
        klaar='Een kolom met twintig weektotalen, een kolom met ja en nee, en acht '
              'getallen in het blokje ernaast.',
        controle=f'De som moet {a.B3_SOM} geven en het gemiddelde precies '
                 f'{a.B3_GEMIDDELDE:g}. De twee SOM.ALS-cellen geven '
                 f'{a.B3_SOMLEEFTIJD} en {a.B3_SOMVEEL}.',
        vast=[
            'Je SOM.ALS geeft 0: je hebt het optelbereik en het zoekbereik '
            'omgewisseld. Bij SOM.ALS komt het bereik waarin je ZOEKT eerst.',
            'Je weektotalen zijn veel te klein: je hebt waarschijnlijk '
            f'=C{S3}+D{S3} getypt in plaats van met × 5 en × 2 te werken.',
            'De telling van wie veel kijkt geeft 6 in plaats van 8: je gebruikte > '
            'in plaats van >=, en dan vallen de twee leerlingen die er precies op '
            'zitten eruit.',
        ],
    ),
    dict(
        nr=4, blad='4 Draaitabel', titel='Twee draaitabellen', duur='12 minuten',
        inleiding=[
            'Nu het nieuwe werk. Je lijst op blad 2 is 35 regels lang en niemand haalt '
            'daar in één blik iets uit. Een DRAAITABEL vat ze samen zonder dat je één '
            'formule typt: je sleept kolomtitels in vakjes en Excel rekent.',
            'Allebei de draaitabellen komen van dezelfde lijst. Ze beantwoorden toch '
            'heel andere vragen — de eerste gaat over het AANBOD, de tweede over wat '
            'er GEKEKEN wordt.',
            f'Alles wat je hier nodig hebt, staat in {g.THEORIEBUNDEL}, kaart 1 tot 9.',
            'Lees de antwoorden op de vijf vragen af van je eigen draaitabellen en typ '
            'ze in.',
        ],
        regels=[
            dict(waar=g.B4_DRAAI1['anker'], wat=g.B4_DRAAI1['titel'], hoe=SLEPEN,
                 punten=5, formule=None,
                 toelichting=f"Bron: de lijst op blad '{g.B4_DRAAI1['bron']}'. "
                             f"Rijen = {g.B4_DRAAI1['rijen']}, "
                             f"Kolommen = {g.B4_DRAAI1['kolommen']}, "
                             f"Waarden = {g.B4_DRAAI1['waarden']} als "
                             f"{g.B4_DRAAI1['bewerking']}. Linkerbovenhoek in "
                             f"{g.B4_DRAAI1['anker']}."),
            dict(waar=g.B4_DRAAI2['anker'], wat=g.B4_DRAAI2['titel'], hoe=SLEPEN,
                 punten=5, formule=None,
                 toelichting=f"Bron: dezelfde lijst. Rijen = {g.B4_DRAAI2['rijen']}, "
                             f"geen kolommen. Sleep TWEE velden naar Waarden: eerst "
                             f"{g.B4_DRAAI2['tweede_waarde']} als "
                             f"{g.B4_DRAAI2['tweede_bewerking']}, dan "
                             f"{g.B4_DRAAI2['waarden']} als "
                             f"{g.B4_DRAAI2['bewerking']}. Excel zet er Som van; zet "
                             f"dat om via Waardeveldinstellingen. Sorteer aflopend op "
                             f"de gemiddelden. Linkerbovenhoek in "
                             f"{g.B4_DRAAI2['anker']}."),
            dict(waar=f'{A4}{V4 + 1}', wat='welk genre de meeste titels heeft',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D1_TOPGENRE),
            dict(waar=f'{A4}{V4 + 2}',
                 wat='welk genre alleen uit series bestaat, zonder één film',
                 hoe=LEZEN, formule=None, punten=1,
                 antwoord=a.D1_ALLEEN_SERIES[0]),
            dict(waar=f'{A4}{V4 + 3}',
                 wat='welke taal gemiddeld de meeste kijkers per titel haalt',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D2_TOPTAAL),
            dict(waar=f'{A4}{V4 + 4}',
                 wat='welke taal veruit de meeste titels heeft maar toch niet bovenaan '
                     'staat bij het gemiddelde',
                 hoe=LEZEN, formule=None, punten=2, antwoord=a.D2_MEESTE_TITELS),
        ],
        opmaak=[
            ('Geef elke draaitabel een duidelijke naam boven de tabel, en zet de '
             'getallen erin gecentreerd.', 1),
            ('Vervang de lege vakjes in draaitabel 1 door een streepje, via '
             'Draaitabelopties (bij "Voor lege cellen weergeven"), en zet de '
             'gemiddelden in draaitabel 2 op één cijfer na de komma.', 1),
        ],
        klaar='Twee draaitabellen op dit blad en vijf ingevulde antwoorden.',
        controle=f'Het eindtotaal van draaitabel 1 moet {a.D1_EINDTOTAAL} zijn — '
                 'evenveel als er titels op blad 2 staan. Bij draaitabel 2 moet de rij '
                 f'Eindtotaal {a.D2_EINDTOTAAL_GEMIDDELD:g} geven: precies het '
                 'gemiddelde dat je op blad 2 al berekende. Staat daar iets anders, '
                 'dan staat je waardeveld nog op Som of op Aantal.',
        vast=[
            'Je draaitabel telt in plaats van het gemiddelde te nemen: klik op het '
            'veld in Waarden, kies Waardeveldinstellingen en zet het op Gemiddelde. '
            'Excel kiest zelf Som of Aantal en kiest bijna nooit Gemiddelde.',
            'Excel wil geen draaitabel maken: je hebt een lege rij of een lege kolom '
            'midden in je lijst, of je koprij mist een titel.',
            'Je draaitabel toont nog de oude cijfers nadat je op blad 2 iets '
            'aanpaste: een draaitabel rekent niet automatisch mee. Rechtsklik erin '
            'en kies Vernieuwen.',
            'Kolom Genre is leeg in je draaitabel of heet "(leeg)": blad 2 kolom G is '
            'nog niet af. De draaitabel kan niet groeperen op een kolom die er niet is.',
        ],
    ),
    dict(
        nr=5, blad='5 Grafiek', titel='Twee grafieken', duur='8 minuten',
        inleiding=[
            'Een draaitabel laat jou iets zien; een grafiek laat het iemand anders in '
            'één blik zien. Je maakt er twee van een verschillend type, en je kiest '
            'bewust welk type bij welke vraag past.',
            f'Theoriebundel {g.THEORIEBUNDEL}, kaart 10 tot 14.',
            g.B5_BRONTEKST,
        ],
        regels=[
            dict(waar=f'C{S5 + 1}:C{E5}', wat='het verschil met het jaar ervoor',
                 hoe=GEEN_FUNCTIE, formule=f'=B{S5 + 1}-B{S5}', punten=2,
                 toelichting=f'C{S5} blijft leeg: voor 2016 is er geen vorig jaar. Een '
                             'daling komt er als een negatief getal uit.'),
            dict(waar='grafiek 1',
                 wat=f'een {a.B5_SOORT_VERGELIJK} van het gemiddelde aantal kijkers '
                     'per taal',
                 hoe=TEKENEN, formule=None, punten=4,
                 toelichting='Ga naar draaitabel 2 op blad 4. Selecteer de kolom met '
                             'de talen, hou Ctrl ingedrukt en selecteer ook de kolom '
                             'met de gemiddelden — NIET de kolom met het aantal '
                             'titels, en niet de rij Eindtotaal. Invoegen, Kolom. Zet '
                             'de grafiek op dit blad. Titel: "Gemiddeld aantal kijkers '
                             'per taal".'),
            dict(waar='grafiek 2',
                 wat=f'een {a.B5_SOORT_TIJD} van de schermtijd per jaar',
                 hoe=TEKENEN, formule=None, punten=4,
                 toelichting=f'Selecteer A{g.B5_KOPRIJ}:B{E5} en kies Invoegen, Lijn. '
                             'Titel: "Schermtijd per dag". Astitels: onder "jaar", '
                             'links "minuten per dag".'),
            dict(waar=f'{A5}{VK5 + 1}',
                 wat='tussen welke twee jaren de schermtijd het sterkst stijgt',
                 hoe=LEZEN, formule=None, punten=1,
                 antwoord=f'{a.B5_STIJGING_VAN} en {a.B5_STIJGING_TOT}'),
            dict(waar=f'{A5}{VK5 + 2}',
                 wat='hoeveel minuten per dag die stijging bedraagt',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.B5_STIJGING),
            dict(waar=f'{A5}{VK5 + 3}',
                 wat='welk grafiektype bij een verloop in de tijd past',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.B5_SOORT_TIJD),
            dict(waar=f'{A5}{VK5 + 4}',
                 wat='welke taal de kortste balk heeft in je staafdiagram',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D2_LAAGSTE),
        ],
        opmaak=[
            ('Beide grafieken hebben een titel die zegt wat je ziet, en de assen zijn '
             'leesbaar: geen jaartallen die over elkaar vallen.', 1),
            (f'Voorwaardelijke opmaak op C{S5 + 1}:C{E5} zodat de dalingen rood '
             'worden, en de verticale as van je lijndiagram begint bij 0.', 1),
        ],
        klaar='Twee grafieken naast elkaar, vier ingevulde antwoorden en een kolom met '
              'verschillen waarin de dalingen opvallen.',
        controle=f'De som van je verschilkolom moet '
                 f'{a.B5_MINUTEN[-1] - a.B5_MINUTEN[0]} geven: precies het verschil '
                 f'tussen {a.B5_JAREN[0]} ({a.B5_MINUTEN[0]}) en {a.B5_JAREN[-1]} '
                 f'({a.B5_MINUTEN[-1]}). Reken dat even na met SOM in een lege cel en '
                 'wis het daarna weer.',
        vast=[
            'Je lijndiagram heeft twee lijnen: je hebt de jaartallen als reeks '
            'meegenomen. Kies Gegevens selecteren en haal de reeks "Jaar" eruit, of '
            f'selecteer alleen A{g.B5_KOPRIJ}:B{E5}.',
            'Je staafdiagram heeft twee reeksen: je hebt ook de kolom met het aantal '
            'titels geselecteerd. Hou Ctrl ingedrukt en selecteer alleen de talen en '
            'de gemiddelden.',
            'Er staat een reusachtige balk bij: je hebt de rij Eindtotaal '
            'meegeselecteerd. Laat die buiten je selectie.',
            'Je balken staan in de verkeerde orde: sorteer eerst je draaitabel '
            'aflopend, dan volgt de grafiek vanzelf.',
        ],
    ),
]

TOTAAL = sum(r['punten'] for oef in OEFENINGEN for r in oef['regels'])
TOTAAL_OPMAAK = sum(p for oef in OEFENINGEN for _, p in oef['opmaak'])
TOTAAL_ALLES = TOTAAL + TOTAAL_OPMAAK

if __name__ == '__main__':
    for oef in OEFENINGEN:
        punten = sum(r['punten'] for r in oef['regels'])
        opm = sum(p for _, p in oef['opmaak'])
        print(f"blad {oef['nr']}  {oef['blad']:<16} {oef['duur']:<12} "
              f"{len(oef['regels'])} regels   {punten} + {opm} punten")
    print(f"\n{TOTAAL} punten voor het werk + {TOTAAL_OPMAAK} voor de opmaak "
          f"= {TOTAAL_ALLES}")
    print(f"samen {sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
