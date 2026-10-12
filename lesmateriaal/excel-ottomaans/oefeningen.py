# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad moet maken, en hoe.

Blad 1 tot 3 zijn herhaling: basisfuncties op historische gegevens. Blad 4 en 5
zijn nieuw: daar wordt niet getypt maar gesleept en getekend.

Elke regel noemt:
  waar     het celadres of het bereik dat de leerling vult
  wat      wat er moet komen, in gewone taal
  hoe      welke functie, of 'een formule, geen functie'
  formule  de formule zoals ze hoort te zijn (voor de sleutel)
  punten   het gewicht bij de beoordeling

De bereiken worden uit gegevens.py afgeleid. Nergens een vast rijnummer.
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

# handige afkortingen voor de bereiken
_b1 = f'{g.B1_START}:{g.B1_EIND}'
_b2 = f'{g.B2_START}:{g.B2_EIND}'
_b3 = f'{g.B3_START}:{g.B3_EIND}'
_b5 = f'{g.B5_START}:{g.B5_EIND}'
S1, E1 = g.B1_START, g.B1_EIND
S2, E2 = g.B2_START, g.B2_EIND
S3, E3 = g.B3_START, g.B3_EIND
S5, E5 = g.B5_START, g.B5_EIND
SAM = g.B1_SAMENVATTING
VK2 = g.B2_VRAAGRIJ          # koprij van het vragenblokje op blad 2
VK3 = g.B3_VRAAGRIJ
VK5 = g.B5_VRAAGRIJ
V4 = g.B4_VRAAGRIJ

def _kol(n):
    """1 -> A, 11 -> K. Zo staat er nergens een vaste kolomletter."""
    uit = ''
    while n:
        n, r = divmod(n - 1, 26)
        uit = chr(65 + r) + uit
    return uit


OEFENINGEN = [
    dict(
        nr=1, blad='1 Sultans', titel='Dertien sultans', duur='8 minuten',
        inleiding=[
            'Dertien sultans met hun eerste en hun laatste regeringsjaar. Je rekent uit '
            'hoe lang elk van hen aan de macht was en je vat de lijst samen.',
            'Deze tabel is straks ook je ZOEKTABEL: op blad 2 ga je er met VERT.ZOEKEN '
            'namen uit halen. Verander er dus niets aan.',
        ],
        regels=[
            dict(waar=f'E{S1}:E{E1}', wat='het aantal regeringsjaren van elke sultan',
                 hoe=GEEN_FUNCTIE, formule=f'=D{S1}-C{S1}', punten=2,
                 toelichting='Laatste jaar min eerste jaar. Typ ze één keer in '
                             f'E{S1} en voer ze door tot E{E1}.'),
            dict(waar=f'F{S1}:F{E1}', wat='of die sultan lang geregeerd heeft',
                 hoe='ALS', formule=f'=ALS(E{S1}>=$B$2;"ja";"nee")', punten=2,
                 toelichting=f'De grens staat in B2 ({g.B1_DREMPEL} jaar). Zet er '
                             'dollartekens om, anders schuift de grens mee naar beneden. '
                             'Let op het grensgeval: precies '
                             f'{g.B1_DREMPEL} jaar is ook lang.'),
            dict(waar=f'B{SAM}', wat='het totaal aantal regeringsjaren',
                 hoe='SOM', formule=f'=SOM(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 1}', wat='de gemiddelde regeerperiode',
                 hoe='GEMIDDELDE', formule=f'=GEMIDDELDE(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 2}', wat='de langste regeerperiode',
                 hoe='MAX', formule=f'=MAX(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 3}', wat='de kortste regeerperiode',
                 hoe='MIN', formule=f'=MIN(E{S1}:E{E1})', punten=1),
            dict(waar=f'B{SAM + 4}', wat='het aantal sultans in de lijst',
                 hoe='AANTAL', formule=f'=AANTAL(C{S1}:C{E1})', punten=1,
                 toelichting='Tel een kolom met getallen, niet met namen: AANTAL telt '
                             'alleen getallen.'),
            dict(waar=f'B{SAM + 5}', wat='het aantal sultans met een lange regering',
                 hoe='AANTAL.ALS', formule=f'=AANTAL.ALS(F{S1}:F{E1};"ja")', punten=1),
        ],
        opmaak=[
            (f'Koprij {g.B1_KOPRIJ} vet, met een achtergrondkleur en gecentreerd.', 1),
            (f'Het samenvattingsblok A{SAM}:B{SAM + 5} met een rand eromheen, en '
             f'B{SAM + 1} op één cijfer na de komma.', 1),
            (f'Voorwaardelijke opmaak op E{S1}:E{E1}: wie langer dan het gemiddelde '
             'geregeerd heeft, krijgt een kleur.', 1),
        ],
        klaar='Een kolom met dertien getallen, een kolom met ja en nee, en zes cijfers '
              'in een omrand blokje.',
        controle=f'B{SAM} moet {a.B1_SOM} geven. Komt er iets anders uit, dan loopt je '
                 f'bereik niet van rij {S1} tot rij {E1}. '
                 f'B{SAM + 5} moet {a.B1_LANGE} geven.',
        vast=[
            f'E{S1} geeft een datum in plaats van een getal: je cel staat op '
            'datumnotatie. Zet ze op Standaard (Start, het vakje met de getalnotatie).',
            'Alle cellen in kolom F zeggen "nee": je bent de dollartekens om B2 '
            'vergeten, dus de grens schoof mee naar beneden.',
            f'B{SAM + 4} geeft 0: AANTAL telt alleen getallen. Richt ze op een kolom '
            'met jaartallen, niet op de namen.',
        ],
    ),
    dict(
        nr=2, blad='2 Gebeurtenissen', titel='Vijfendertig gebeurtenissen',
        duur='12 minuten',
        inleiding=[
            f'Een lijst van {len(g.B2)} gebeurtenissen met jaar, soort, regio, eeuw en '
            'de code van de sultan die toen regeerde. Je vult de drie laatste kolommen '
            'aan met VERT.ZOEKEN en ALS.',
            'Deze lijst wordt straks de BRON van je eerste draaitabel. Een draaitabel '
            'wil een kaarsrechte lijst: één koprij, geen lege rij ertussen en geen '
            'totaalrij eronder. Daarom staan de vier tellingen hiernaast, in kolom '
            f'{_kol(g.B2_VRAAGKOL)}, met een lege kolom ertussen. Hou dat zo.',
        ],
        regels=[
            dict(waar=f'G{S2}:G{E2}', wat='de naam van de sultan die bij de code hoort',
                 hoe='VERT.ZOEKEN', punten=3,
                 formule=f"=VERT.ZOEKEN(F{S2};'1 Sultans'!$A${S1}:$F${E1};2;ONWAAR)",
                 toelichting='De zoektabel staat op blad 1. Zet ze vast met '
                             'dollartekens voordat je doorvoert, anders zakt de tabel '
                             'mee naar beneden en krijg je onderaan #N/B.'),
            dict(waar=f'H{S2}:H{E2}',
                 wat='het aantal regeringsjaren van die sultan',
                 hoe='VERT.ZOEKEN', punten=3,
                 formule=f"=VERT.ZOEKEN(F{S2};'1 Sultans'!$A${S1}:$F${E1};5;ONWAAR)",
                 toelichting='Dezelfde zoektabel, maar nu de vijfde kolom. Die kolom '
                             'heb je op blad 1 zelf berekend — is blad 1 nog niet af, '
                             'dan staat hier niets zinnigs.'),
            dict(waar=f'I{S2}:I{E2}',
                 wat='of de gebeurtenis in een lange regering viel',
                 hoe='ALS', punten=2,
                 formule=f"=ALS(H{S2}>={g.B1_DREMPEL};\"ja\";\"nee\")",
                 toelichting=f'Lang is {g.B1_DREMPEL} jaar of meer, dezelfde grens als '
                             'op blad 1.'),
            dict(waar=f'{_kol(g.B2_VRAAGKOL + 1)}{VK2 + 1}',
                 wat='het aantal gebeurtenissen in de lijst',
                 hoe='AANTAL', formule=f'=AANTAL(A{S2}:A{E2})', punten=1),
            dict(waar=f'{_kol(g.B2_VRAAGKOL + 1)}{VK2 + 2}',
                 wat=f'het aantal gebeurtenissen van de soort {g.B2_TELSOORT}',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(C{S2}:C{E2};"{g.B2_TELSOORT}")'),
            dict(waar=f'{_kol(g.B2_VRAAGKOL + 1)}{VK2 + 3}',
                 wat=f'het aantal gebeurtenissen in de regio {g.B2_TELREGIO}',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(D{S2}:D{E2};"{g.B2_TELREGIO}")'),
            dict(waar=f'{_kol(g.B2_VRAAGKOL + 1)}{VK2 + 4}',
                 wat=f'het aantal gebeurtenissen in de {g.B2_TELEEUW}',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(E{S2}:E{E2};"{g.B2_TELEEUW}")'),
        ],
        opmaak=[
            (f'Koprij {g.B2_KOPRIJ} vet met een achtergrondkleur, en die koprij '
             'geblokkeerd zodat ze blijft staan als je naar beneden scrolt.', 1),
            (f'Kolom A gecentreerd, en kolom B breed genoeg om elke gebeurtenis '
             'helemaal te lezen.', 1),
        ],
        klaar='Drie volle kolommen tot de laatste rij, en vier getallen in het blokje '
              'ernaast. Nergens #N/B.',
        controle=f'De telling van de {g.B2_TELEEUW} moet {a.B2_TEL_EEUW} geven en de '
                 f'telling van {g.B2_TELREGIO} moet {a.B2_TEL_REGIO} geven. '
                 f'De laatste rij ({E2}) hoort {a.B2_SULTAN[-1]} te tonen.',
        vast=[
            'Onderaan kolom G staat #N/B: je zoektabel is niet vastgezet. Zet '
            'dollartekens rond het bereik en voer opnieuw door.',
            'Kolom G geeft overal dezelfde naam: je hebt de code van de eerste rij '
            'vastgezet in plaats van de tabel. Alleen de TABEL krijgt dollartekens, '
            'de code niet.',
            'Kolom H geeft 0: op blad 1 is kolom E nog leeg. Maak blad 1 eerst af.',
            f'De telling van {g.B2_TELSOORT} geeft 0: let op de schrijfwijze. Excel is '
            'niet gevoelig voor hoofdletters, maar wel voor een spatie te veel.',
        ],
    ),
    dict(
        nr=3, blad='3 Oorlogen', titel='Achttien oorlogen', duur='10 minuten',
        inleiding=[
            f'{len(g.B3)} oorlogen met hun begin- en eindjaar, de tegenstander en de '
            'uitkomst. Je rekent de duur uit en vat samen.',
            'Ook deze lijst wordt een bron: draaitabel 2 en je staafdiagram komen '
            'hiervandaan. Zelfde regel — het vragenblokje staat ERNAAST.',
        ],
        regels=[
            dict(waar=f'E{S3}:E{E3}', wat='de duur van elke oorlog in jaren',
                 hoe=GEEN_FUNCTIE, formule=f'=D{S3}-C{S3}', punten=2,
                 toelichting='Een oorlog die begint en eindigt in hetzelfde jaar krijgt '
                             '0. Dat is geen fout.'),
            dict(waar=f'G{S3}:G{E3}', wat='of het een lange oorlog was',
                 hoe='ALS', formule=f'=ALS(E{S3}>=$B$2;"ja";"nee")', punten=2,
                 toelichting=f'De grens staat in B2 ({g.B3_DREMPEL} jaar). Dollartekens, '
                             'zoals op blad 1.'),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 1}',
                 wat='het totaal aantal oorlogsjaren',
                 hoe='SOM', formule=f'=SOM(E{S3}:E{E3})', punten=1),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 2}',
                 wat='de gemiddelde duur van een oorlog',
                 hoe='GEMIDDELDE', formule=f'=GEMIDDELDE(E{S3}:E{E3})', punten=1),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 3}',
                 wat='de duur van de langste oorlog',
                 hoe='MAX', formule=f'=MAX(E{S3}:E{E3})', punten=1),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 4}',
                 wat='de duur van de kortste oorlog',
                 hoe='MIN', formule=f'=MIN(E{S3}:E{E3})', punten=1),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 5}',
                 wat=f'het aantal oorlogen met uitkomst {g.B3_TELUITKOMST}',
                 hoe='AANTAL.ALS', punten=1,
                 formule=f'=AANTAL.ALS(F{S3}:F{E3};"{g.B3_TELUITKOMST}")'),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 6}',
                 wat=f'het aantal oorlogsjaren tegen {g.B3_SOMLAND}',
                 hoe='SOM.ALS', punten=2,
                 formule=f'=SOM.ALS(B{S3}:B{E3};"{g.B3_SOMLAND}";E{S3}:E{E3})',
                 toelichting='Let op de volgorde: eerst waar je kijkt, dan wat er moet '
                             'staan, dan wat je optelt.'),
            dict(waar=f'{_kol(g.B3_VRAAGKOL + 1)}{VK3 + 7}',
                 wat=f'het aantal oorlogsjaren van de oorlogen met uitkomst '
                     f'{g.B3_SOMUITKOMST}',
                 hoe='SOM.ALS', punten=2,
                 formule=f'=SOM.ALS(F{S3}:F{E3};"{g.B3_SOMUITKOMST}";E{S3}:E{E3})'),
        ],
        opmaak=[
            (f'Koprij {g.B3_KOPRIJ} vet met een achtergrondkleur, en kolom C, D en E '
             'gecentreerd.', 1),
            (f'Voorwaardelijke opmaak op F{S3}:F{E3}: de oorlogen met uitkomst '
             f'{g.B3_SOMUITKOMST} krijgen een kleur.', 1),
        ],
        klaar='Een kolom met achttien duurtijden, een kolom met ja en nee, en acht '
              'getallen in het blokje ernaast.',
        controle=f'De som moet {a.B3_SOM} geven en het gemiddelde precies '
                 f'{a.B3_GEMIDDELDE:g}. De twee SOM.ALS-cellen geven {a.B3_SOMLAND} en '
                 f'{a.B3_SOMUITKOMST}.',
        vast=[
            'Je SOM.ALS geeft 0: je hebt het optelbereik en het zoekbereik omgewisseld. '
            'Bij SOM.ALS komt het bereik waarin je ZOEKT eerst.',
            'De kortste oorlog geeft een leeg vakje in plaats van 0: er staat ergens '
            'tekst in je duurkolom. Kijk de laatste rij na.',
        ],
    ),
    dict(
        nr=4, blad='4 Draaitabel', titel='Twee draaitabellen', duur='12 minuten',
        inleiding=[
            'Nu komt het nieuwe. Je hebt twee lange lijsten gemaakt. Niemand kan daar '
            'in één blik iets uit halen. Een DRAAITABEL vat zo\'n lijst samen zonder dat '
            'je één formule typt: je sleept de kolomtitels in vakjes en Excel rekent.',
            'Alles wat je hier moet weten, staat in de theoriebundel '
            f'{g.THEORIEBUNDEL} — kaart 1 tot 9. Hou ze ernaast.',
            'Lees de antwoorden op de vijf vragen AF van je eigen draaitabellen. Typ ze '
            'in; ze mogen gewoon getallen en woorden zijn.',
        ],
        regels=[
            dict(waar=g.B4_DRAAI1['anker'], wat=g.B4_DRAAI1['titel'], hoe=SLEPEN,
                 punten=5, formule=None,
                 toelichting=f"Bron: de lijst op blad '{g.B4_DRAAI1['bron']}'. "
                             f"Rijen = {g.B4_DRAAI1['rijen']}, "
                             f"Kolommen = {g.B4_DRAAI1['kolommen']}, "
                             f"Waarden = {g.B4_DRAAI1['waarden']} als "
                             f"{g.B4_DRAAI1['bewerking']}. "
                             f"Zet de tabel op dit blad, met de linkerbovenhoek in "
                             f"{g.B4_DRAAI1['anker']}."),
            dict(waar=g.B4_DRAAI2['anker'], wat=g.B4_DRAAI2['titel'], hoe=SLEPEN,
                 punten=5, formule=None,
                 toelichting=f"Bron: de lijst op blad '{g.B4_DRAAI2['bron']}'. "
                             f"Rijen = {g.B4_DRAAI2['rijen']}, geen kolommen, "
                             f"Waarden = {g.B4_DRAAI2['waarden']} als "
                             f"{g.B4_DRAAI2['bewerking']}. Sorteer aflopend op de "
                             f"waarden, zodat de langste bovenaan staat. "
                             f"Linkerbovenhoek in {g.B4_DRAAI2['anker']}."),
            dict(waar=f'{_kol(g.B4_VRAAGKOL + 1)}{V4 + 1}', wat='in welke eeuw er het meest gebeurde',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D1_TOPEEUW),
            dict(waar=f'{_kol(g.B4_VRAAGKOL + 1)}{V4 + 2}', wat='hoeveel gebeurtenissen dat waren',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D1_TOPEEUW_AANTAL),
            dict(waar=f'{_kol(g.B4_VRAAGKOL + 1)}{V4 + 3}', wat='welke soort gebeurtenis het vaakst voorkomt',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D1_TOPSOORT),
            dict(waar=f'{_kol(g.B4_VRAAGKOL + 1)}{V4 + 4}',
                 wat='tegen welke tegenstander het rijk het langst in oorlog was',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D2_TOP),
            dict(waar=f'{_kol(g.B4_VRAAGKOL + 1)}{V4 + 5}', wat='hoeveel oorlogsjaren dat samen waren',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D2_TOP_JAREN),
        ],
        opmaak=[
            ('Geef elke draaitabel een duidelijke naam boven de tabel, en zet de '
             'getallen erin gecentreerd.', 1),
            ('Vervang de lege vakjes in draaitabel 1 door een streepje, via '
             'Draaitabelopties (bij "Voor lege cellen weergeven").', 1),
        ],
        klaar='Twee draaitabellen op dit blad en vijf ingevulde antwoorden.',
        controle=f'Het eindtotaal van draaitabel 1 moet {a.D1_EINDTOTAAL} zijn — '
                 f'evenveel als er regels op blad 2 staan. Het eindtotaal van '
                 f'draaitabel 2 moet {a.D2_EINDTOTAAL} zijn, hetzelfde getal als de SOM '
                 f'die je op blad 3 al berekende. Klopt dat niet, dan heb je een rij te '
                 'veel of te weinig in je bron.',
        vast=[
            'Je draaitabel telt in plaats van op te tellen: klik op het veld in '
            'Waarden, kies Waardeveldinstellingen en zet het op Som. Excel kiest '
            'Aantal zodra er ook maar één lege cel of één stukje tekst in de kolom zit.',
            'Excel wil geen draaitabel maken: je hebt een lege rij of een lege kolom '
            'midden in je lijst, of je koprij mist een titel.',
            'Je hebt een rij aan blad 2 of 3 toegevoegd en de draaitabel ziet ze niet: '
            'een draaitabel rekent niet automatisch mee. Rechtsklik erin en kies '
            'Vernieuwen.',
            'De kolommen staan in de verkeerde orde: de eeuwen staan als tekst in de '
            'lijst, dus Excel sorteert ze alfabetisch. Dat is hier toevallig ook '
            'chronologisch.',
        ],
    ),
    dict(
        nr=5, blad='5 Grafiek', titel='Twee grafieken', duur='8 minuten',
        inleiding=[
            'Een draaitabel laat je iets zien; een grafiek laat het iemand anders in '
            'één blik zien. Je maakt er twee, van een verschillend type, en je kiest '
            'bewust welk type bij welke vraag past.',
            f'Theoriebundel {g.THEORIEBUNDEL}, kaart 10 tot 14.',
            g.B5_BRONTEKST,
        ],
        regels=[
            dict(waar=f'C{S5 + 1}:C{E5}',
                 wat='het verschil met de vorige meting',
                 hoe=GEEN_FUNCTIE, formule=f'=B{S5 + 1}-B{S5}', punten=2,
                 toelichting=f'C{S5} blijft leeg: voor de eerste meting is er geen '
                             'vorige. Een daling komt er als een negatief getal uit.'),
            dict(waar='grafiek 1', wat=f'een {a.B5_SOORT_VERGELIJK} van draaitabel 2: '
                                       'oorlogsjaren per tegenstander',
                 hoe=TEKENEN, formule=None, punten=4,
                 toelichting='Klik in draaitabel 2 op blad 4 en kies Invoegen, '
                             'Draaigrafiek, kolom. Zet de grafiek op dit blad. Titel: '
                             '"Oorlogsjaren per tegenstander". Geen legende nodig — er '
                             'is maar één reeks.'),
            dict(waar='grafiek 2', wat='een ' + a.B5_SOORT_TIJD +
                                       ' van de bevolkingsschatting per jaar',
                 hoe=TEKENEN, formule=None, punten=4,
                 toelichting=f'Selecteer A{g.B5_KOPRIJ}:B{E5} en kies Invoegen, Lijn. '
                             'Titel: "Geschat aantal inwoners". Zet er een astitel bij: '
                             'onder "jaar", links "miljoen inwoners".'),
            dict(waar=f'{_kol(g.B5_VRAAGKOL + 1)}{VK5 + 1}',
                 wat='tussen welke twee metingen de daling het grootst is',
                 hoe=LEZEN, formule=None, punten=1,
                 antwoord=f'{a.B5_DALING_VAN} en {a.B5_DALING_TOT}'),
            dict(waar=f'{_kol(g.B5_VRAAGKOL + 1)}{VK5 + 2}',
                 wat='hoeveel miljoen de schatting toen daalde',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.B5_DALING),
            dict(waar=f'{_kol(g.B5_VRAAGKOL + 1)}{VK5 + 3}',
                 wat='welk grafiektype bij een verloop in de tijd past',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.B5_SOORT_TIJD),
            dict(waar=f'{_kol(g.B5_VRAAGKOL + 1)}{VK5 + 4}',
                 wat='welke tegenstander de langste balk heeft',
                 hoe=LEZEN, formule=None, punten=1, antwoord=a.D2_TOP),
        ],
        opmaak=[
            ('Beide grafieken hebben een titel die zegt wat je ziet, en de assen zijn '
             'leesbaar: geen jaartallen die over elkaar vallen.', 1),
            (f'De kolom met verschillen op nul cijfers na de komma, en voorwaardelijke '
             f'opmaak op C{S5 + 1}:C{E5} zodat de dalingen rood worden.', 1),
        ],
        klaar='Twee grafieken naast elkaar, vier ingevulde antwoorden en een kolom met '
              'verschillen waarin de dalingen opvallen.',
        controle=f'De som van je verschilkolom moet {a.B5_INWONERS[-1] - a.B5_INWONERS[0]} '
                 f'geven: dat is precies het verschil tussen de eerste '
                 f'({a.B5_INWONERS[0]}) en de laatste meting ({a.B5_INWONERS[-1]}). '
                 'Reken dat even na met SOM in een lege cel en wis het daarna weer.',
        vast=[
            'Je lijndiagram heeft twee lijnen: je hebt de jaartallen als reeks '
            'meegenomen. Kies Gegevens selecteren en haal de reeks "Jaar" eruit, of '
            f'selecteer alleen A{g.B5_KOPRIJ}:B{E5}.',
            'De jaartallen onderaan staan niet gelijk verdeeld en dat hoort ook: de '
            'metingen liggen niet even ver van elkaar. Een lijndiagram met een '
            'categorie-as doet alsof dat wel zo is. Zeg dat erbij als je het blad '
            'uitlegt.',
            'Je staafdiagram staat in de verkeerde orde: sorteer eerst je draaitabel '
            'aflopend, dan volgt de grafiek automatisch.',
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
        print(f"blad {oef['nr']}  {oef['blad']:<18} {oef['duur']:<12} "
              f"{len(oef['regels'])} regels   {punten} + {opm} punten")
    print(f"\n{TOTAAL} punten voor het werk + {TOTAAL_OPMAAK} voor de opmaak "
          f"= {TOTAAL_ALLES}")
    duur = sum(int(o['duur'].split()[0]) for o in OEFENINGEN)
    print(f"samen {duur} minuten")
