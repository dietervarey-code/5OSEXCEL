# -*- coding: utf-8 -*-
"""De fiches die in de opdrachtbundel zelf staan.

Nieuw onderwerp, dus de uitleg gaat mee in de opdracht. Voor de draaitabel,
het groeperen en de draaigrafiek van blad 5 verwijzen we naar het boekje dat
ze al hebben.
"""
import sys

sys.dont_write_bytecode = True

THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"

DELEN = ["Rekenen met datums", "Uit een datum halen", "Werkdagen",
         "Zonder formules"]

FICHES = [
    dict(
        deel="Rekenen met datums", naam="Een datum is een getal",
        functies=[],
        wat="Excel bewaart een datum als een getal. Daarom kan je ermee "
            "rekenen.",
        schrijf='=einde-start',
        argumenten=[('einde-start', 'het aantal dagen tussen twee datums')],
        uitleg=[
            '1 januari 1900 is dag 1. 17 juli 2026 is dag 46 220. Wat je ziet '
            'is alleen de opmaak; wat eronder zit is een gewoon getal.',
            'Twee datums van elkaar aftrekken geeft dus gewoon het aantal '
            'dagen. Een datum plus 7 is een week later.',
            'Komt er een datum uit waar je een getal verwacht? Dan heeft Excel '
            'de opmaak overgenomen van de cellen waarmee je rekende. Zet de '
            'cel op Standaard of Getal en het probleem is weg.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = 29/06/2026   B2 = 16/07/2026', '=B2-A2  geeft  17'],
                   ['A2 = 29/06/2026', '=A2+7  geeft  06/07/2026']]),
        weten=['Een datum die je als tekst typt ("17 juli") is geen datum. '
               'Excel zet een echte datum rechts in de cel, tekst links.'],
        fout='Het antwoord krijgen als een datum in 1900. Dat is geen fout in '
             'je formule maar in de opmaak van de cel.',
    ),
    dict(
        deel="Rekenen met datums", naam="VANDAAG", functies=['VANDAAG'],
        wat="De datum van vandaag, zoals de computer hem kent.",
        schrijf='=VANDAAG()',
        argumenten=[('()', 'niets tussen de haakjes — toch moeten ze er staan')],
        uitleg=[
            'Deze formule rekent zichzelf elke dag opnieuw uit. Morgen staat '
            'er iets anders dan vandaag.',
            'Dat is handig in een bestand dat je blijft gebruiken, en lastig '
            'in een oefening: niemand kan nakijken wat er gisteren stond.',
            'Daarom staat rechtsboven op elk blad een PEILDATUM. Reken daarop, '
            'behalve waar er uitdrukkelijk VANDAAG() gevraagd wordt.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['G1 = 17/07/2026',
                    '=$G$1-VANDAAG()  geeft  het aantal dagen dat je nog moet '
                    'wachten'],
                   ['', '=VANDAAG()+30  geeft  de datum over dertig dagen']]),
        weten=['NU() geeft de datum én het uur.',
               'Wil je de datum van vandaag vastzetten, zodat hij niet meer '
               'verandert? Typ Ctrl+; — dat zet de datum er als vaste waarde '
               'in.'],
        fout='De haakjes vergeten. =VANDAAG zonder haakjes geeft #NAAM?.',
    ),
    dict(
        deel="Rekenen met datums", naam="DATUMVERSCHIL",
        functies=['DATUMVERSCHIL'],
        wat="Het aantal hele jaren, maanden of dagen tussen twee datums.",
        schrijf='=DATUMVERSCHIL(eerste;laatste;"J")',
        argumenten=[('eerste', 'de vroegste datum — die hoort vooraan'),
                    ('laatste', 'de latere datum'),
                    ('"J"', 'wat je wil tellen: "J" jaren, "M" maanden, '
                            '"D" dagen')],
        uitleg=[
            'Voor een leeftijd heb je dit nodig. Gewoon aftrekken en delen '
            'door 365 geeft om de vier jaar een dag te weinig.',
            'DATUMVERSCHIL telt hele jaren. Wie op de peildatum jarig is, is '
            'die dag al een jaar ouder; wie de dag erna jarig is, nog niet.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['B2 = 17/07/2008   G1 = 17/07/2026',
                    '=DATUMVERSCHIL(B2;$G$1;"J")  geeft  18'],
                   ['B2 = 18/07/2008   G1 = 17/07/2026',
                    '=DATUMVERSCHIL(B2;$G$1;"J")  geeft  17']]),
        weten=['Deze functie staat in geen enkel menu en Excel helpt je niet '
               'met een tooltip. Je moet ze gewoon kennen. Typ ze volledig uit.',
               'De letter moet tussen aanhalingstekens staan.',
               'Zet je de datums omgekeerd, dan krijg je #GETAL!.'],
        fout='De peildatum niet vastzetten met dollartekens. Bij het doorvoeren '
             'schuift hij dan mee naar beneden en krijg je onzin.',
    ),
    dict(
        deel="Uit een datum halen", naam="JAAR, MAAND en DAG",
        functies=['JAAR', 'MAAND', 'DAG'],
        wat="Haalt één stuk uit een datum, als getal.",
        schrijf='=JAAR(cel)    =MAAND(cel)    =DAG(cel)',
        argumenten=[('cel', 'waar de datum staat')],
        uitleg=[
            'Je krijgt altijd een getal terug, nooit een naam: MAAND geeft 7, '
            'niet "juli".',
            'Dat is net handig: op een getal kan je sorteren en groeperen, op '
            'een naam niet. December komt alfabetisch vóór februari.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = 20/06/2026', '=MAAND(A2)  geeft  6'],
                   ['A2 = 20/06/2026', '=JAAR(A2)  geeft  2026']]),
        weten=['Wil je de naam van de maand zien in plaats van het nummer, '
               'geef de cel dan de aangepaste getalnotatie mmmm. De waarde '
               'blijft dan een datum; alleen de weergave verandert.'],
        fout='MAAND op een cel waar tekst in staat. Dan krijg je #WAARDE!, en '
             'de oorzaak is dat je datum geen datum is.',
    ),
    dict(
        deel="Uit een datum halen", naam="WEEKDAG", functies=['WEEKDAG'],
        wat="Zegt op welke dag van de week een datum valt, als nummer.",
        schrijf='=WEEKDAG(cel;2)',
        argumenten=[('cel', 'waar de datum staat'),
                    ('2', 'het soort telling: met 2 is maandag 1 en zondag 7')],
        uitleg=[
            'Die 2 is belangrijk. Laat je ze weg, dan is ZONDAG dag 1 en '
            'maandag dag 2 — de Amerikaanse telling, en dan klopt je weekend '
            'niet meer.',
            'Met ;2 is het weekend dag 6 en 7. Daarmee kan je met een ALS '
            'uitrekenen of een datum in het weekend valt.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = 17/07/2026 (een vrijdag)',
                    '=WEEKDAG(A2;2)  geeft  5'],
                   ['A2 = 18/07/2026 (een zaterdag)',
                    '=ALS(WEEKDAG(A2;2)>=6;"weekend";"weekdag")  geeft  '
                    'weekend']]),
        weten=['De naam van de dag krijg je met de aangepaste getalnotatie '
               'dddd op de datum zelf.'],
        fout='De ;2 vergeten. Je krijgt dan wel een getal, en het lijkt te '
             'kloppen — tot je weekend een dag verschoven blijkt.',
    ),
    dict(
        deel="Werkdagen", naam="NETTO.WERKDAGEN",
        functies=['NETTO.WERKDAGEN'],
        wat="Telt de werkdagen tussen twee datums. Zaterdag en zondag tellen "
            "niet mee.",
        schrijf='=NETTO.WERKDAGEN(begin;einde)',
        argumenten=[('begin', 'de eerste dag — die telt mee'),
                    ('einde', 'de laatste dag — die telt ook mee')],
        uitleg=[
            'Gewoon aftrekken geeft kalenderdagen. Een ploeg die niet in het '
            'weekend werkt, heeft daar niets aan.',
            'Allebei de datums tellen mee. Van maandag tot vrijdag is dus 5, '
            'niet 4.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = 29/06/2026   G1 = 17/07/2026',
                    '=NETTO.WERKDAGEN(A2;$G$1)  geeft  15'],
                   ['A2 = 29/06/2026   G1 = 17/07/2026',
                    '=$G$1-A2  geeft  18 — de drie weekenddagen zitten erbij']]),
        weten=['Er bestaat een derde argument voor feestdagen: een bereik met '
               'de datums die ook niet meetellen. Dat hebben we hier niet '
               'nodig.',
               'NETTO.WERKDAGEN.INTL kan ook andere vrije dagen aan dan '
               'zaterdag en zondag.'],
        fout='De einddatum niet vastzetten met dollartekens, waardoor hij bij '
             'het doorvoeren mee naar beneden zakt.',
    ),
    dict(
        deel="Werkdagen", naam="WERKDAG", functies=['WERKDAG'],
        wat="Geeft de datum een aantal werkdagen later.",
        schrijf='=WERKDAG(begin;aantal)',
        argumenten=[('begin', 'de startdatum — die telt NIET mee'),
                    ('aantal', 'hoeveel werkdagen erbij')],
        uitleg=[
            'Dit is het omgekeerde van NETTO.WERKDAGEN. Daar tel je de dagen '
            'tussen twee datums, hier zoek je de datum.',
            'De startdag telt niet mee. Start je op maandag en duurt de taak '
            '5 werkdagen, dan ben je de maandag erna klaar.',
            'Weekends worden overgeslagen. Een taak van 5 werkdagen die op '
            'woensdag start, is pas de woensdag erna af.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['B2 = 13/07/2026 (maandag)   C2 = 5',
                    '=WERKDAG(B2;C2)  geeft  20/07/2026'],
                   ['B2 = 13/07/2026   C2 = 5',
                    '=B2+C2  geeft  18/07/2026 — een zaterdag, dus fout']]),
        weten=['Komt er een getal uit in plaats van een datum, geef de cel dan '
               'de datumnotatie. De berekening klopt wel.'],
        fout='Denken dat de startdag meetelt. Een taak van één werkdag die '
             'maandag start, komt met WERKDAG op dinsdag uit.',
    ),
    dict(
        deel="Zonder formules", naam="Een tabel maken (Ctrl+T)", functies=[],
        wat="Maakt van je lijst een echte tabel, die meegroeit.",
        schrijf=None,
        stappen=[
            'Klik één cel in de lijst aan.',
            'Druk Ctrl+T.',
            'Controleer dat "De tabel bevat kopteksten" aangevinkt staat.',
            'Klik OK. Je lijst krijgt kleur en filterpijltjes.',
        ],
        uitleg=[
            'Een tabel is meer dan opmaak. Zet je er een rij bij onderaan, dan '
            'hoort die er meteen bij — ook in elke draaitabel en grafiek die '
            'erop staat.',
            'Een tijdlijn of een slicer kan alleen op een tabel of op een '
            'draaitabel.',
        ],
        weten=['Boven in het lint verschijnt Tabelontwerp. Daar geef je de '
               'tabel een naam die later prettiger leest dan Tabel1.'],
        fout='Ctrl+T drukken terwijl er een lege rij in je lijst zit. Dan pakt '
             'Excel maar de helft.',
    ),
    dict(
        deel="Zonder formules", naam="Een tijdlijn", functies=[],
        wat="Een slicer voor datums: een schuifbalk waarmee je op maand, "
            "kwartaal of jaar filtert.",
        schrijf=None,
        stappen=[
            'Klik je draaitabel aan.',
            'Ga naar Draaitabel analyseren, en klik op Tijdlijn invoegen.',
            'Vink het datumveld aan. Klik OK.',
            'Rechtsboven in de tijdlijn kies je MAANDEN, KWARTALEN of JAREN. '
            'Klik dan op een maand.',
        ],
        uitleg=[
            'Een tijdlijn kan alleen op een veld met echte datums. Staat je '
            'datum als tekst in de kolom, dan blijft de knop grijs.',
            'Alles wat aan de draaitabel hangt beweegt mee, ook de '
            'draaigrafiek. Je klikt op juni en je grafiek toont juni.',
            'Je kan slepen om meer dan één maand tegelijk te kiezen.',
        ],
        weten=['Met het gommetje rechtsboven in de tijdlijn zet je het filter '
               'weer af.',
               'Een tijdlijn en een gewone slicer kunnen samen op dezelfde '
               'draaitabel staan.'],
        fout='Een tijdlijn proberen invoegen op een draaitabel zonder '
             'datumveld. Excel zegt dan dat er geen datums zijn, en dat klopt.',
    ),
]

# waar de fiches van het andere boekje gebruikt worden
KAARTEN_ELDERS = {
    3: 'Een draaitabel invoegen',
    4: 'Rijen en Waarden — je eerste draaitabel',
    8: 'Groeperen',
    13: 'Een draaigrafiek',
}

if __name__ == '__main__':
    for i, f in enumerate(FICHES, 1):
        stuk = (f.get('schrijf') or '(geen formule — menu)').splitlines()[0]
        print(f"{i:>2}. {f['naam']:<26} {f['deel']:<20} {stuk}")
    print(f'\n{len(FICHES)} fiches in {len(DELEN)} delen')
