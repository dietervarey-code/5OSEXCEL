# -*- coding: utf-8 -*-
"""De zeven oefeningen van de tweede herhalingsbundel.

Geen nieuwe leerstof: alle functies komen uit de basisbundel. Wat hier telt is
het aantal keer dat ze langskomen. Geen geneste functies.
"""

OEFENINGEN = [
    dict(
        nr=1,
        titel='Omzet van een week',
        blad='1 Weekomzet',
        duur='5 minuten',
        doel='Een week omzet optellen in twee richtingen: per dag en per afdeling.',
        functies=['SOM'],
        hulp=['Doorvoeren met de vulgreep', 'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A10', 'de zeven dagen van de week'),
            ('B4:D10', 'de omzet per afdeling: planten, tuinmeubels en gereedschap'),
        ],
        maken=[
            ('E4:E10', 'het dagtotaal', 'SOM over de rij'),
            ('B12:E12', 'het totaal per afdeling, en rechts het weektotaal',
             'SOM over de kolom, naar rechts doorvoeren'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'B4:E12: notatie valuta.',
            'Totaalrij 12: vet met een bovenrand.',
        ],
        stappen=[
            ('Tel de eerste dag op.',
             'Klik E4 aan en typ =SOM(B4:D4). Voer door tot E10.'),
            ('Tel de eerste afdeling op.',
             'Klik B12 aan en typ =SOM(B4:B10). Voer die formule nu naar RECHTS door, '
             'tot en met E12. Sleep de vulgreep dus zijwaarts, niet naar beneden.'),
            ('Werk het blad af.',
             'Geef B4:E12 de notatie valuta. Zet de koptekst in rij 3 in het vet met een '
             'achtergrondkleur, en rij 12 in het vet met een bovenrand.'),
        ],
        klaar='Zeven dagtotalen, vier kolomtotalen, alles in euro, met een duidelijke koptekst '
              'en totaalrij.',
        controle='E12 is zowel de som van de zeven dagtotalen als de som van de drie '
                 'afdelingen. Komen die niet overeen, dan mis je een rij of een kolom.',
    ),
    dict(
        nr=2,
        titel='Leveringen van de kwekers',
        blad='2 Kwekers',
        duur='6 minuten',
        doel='Van acht kwekers over drie maanden vijf kerncijfers halen, en er daarna een '
             'ja-of-nee-kolom bij zetten.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'ALS', 'AANTAL.ALS'],
        hulp=['Doorvoeren met de vulgreep', 'Absolute celverwijzing: de dollartekens'],
        gegeven=[
            ('A4:A11', 'de namen van de acht kwekers'),
            ('B4:D11', 'het aantal geleverde planten per maand'),
        ],
        maken=[
            ('E4:E11', 'het totaal per kweker', 'SOM over de rij'),
            ('B13', 'het totaal aantal geleverde planten', 'SOM'),
            ('B14', 'het gemiddelde per kweker', 'GEMIDDELDE'),
            ('B15', 'het hoogste totaal', 'MAX'),
            ('B16', 'het laagste totaal', 'MIN'),
            ('B17', 'het aantal kwekers', 'AANTAL'),
            ('F4:F11', 'ja of nee: levert de kweker 1200 planten of meer', 'ALS'),
            ('B18', 'het aantal grote kwekers', 'AANTAL.ALS'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'B4:E18: notatie getal met een duizendscheiding en geen decimalen.',
            'Samenvattingsblok A13:B18: achtergrondkleur.',
        ],
        stappen=[
            ('Tel de planten per kweker op.',
             'Klik E4 aan en typ =SOM(B4:D4). Voer door tot E11.'),
            ('Vul de samenvatting in.',
             'Klik B13 aan en typ =SOM(E4:E11). Daarna B14: =GEMIDDELDE(E4:E11), '
             'B15: =MAX(E4:E11), B16: =MIN(E4:E11) en B17: =AANTAL(E4:E11). '
             'Vijf keer hetzelfde bereik, vijf verschillende functies.'),
            ('Zet erbij wie een grote kweker is.',
             'Klik F4 aan en typ =ALS(E4>=1200;"ja";"nee"). Voer door tot F11. '
             'Let op >= en niet >: een kweker van precies 1200 hoort erbij.'),
            ('Tel hoeveel grote kwekers er zijn.',
             'Klik B18 aan en typ =AANTAL.ALS(F4:F11;"ja").'),
            ('Werk het blad af.',
             'Geef B4:E18 een duizendscheiding zonder decimalen. Geef A13:B18 een '
             'achtergrondkleur en zet de koptekst in rij 3 in het vet.'),
        ],
        klaar='Acht totalen, een kolom met ja of nee, en daaronder zes samenvattende cijfers '
              'in een gekleurd blokje.',
        controle='B17 moet 8 geven — evenveel als er kwekers in de lijst staan. Geeft het een '
                 'ander getal, dan klopt je bereik niet.',
    ),
    dict(
        nr=3,
        titel='Prijzen verhogen',
        blad='3 Prijsverhoging',
        duur='6 minuten',
        doel='Op tien artikelen dezelfde verhoging toepassen, met één percentage dat op één '
             'plaats staat.',
        functies=['AFRONDEN', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep'],
        gegeven=[
            ('B2', 'het verhogingspercentage — één keer, voor de hele lijst'),
            ('A5:A14', 'de artikelnamen'),
            ('B5:B14', 'de oude prijzen'),
        ],
        maken=[
            ('C5:C14', 'de verhoging in euro, afgerond op cent',
             'AFRONDEN, met een absolute verwijzing naar B2'),
            ('D5:D14', 'de nieuwe prijs', 'formule'),
            ('B16:D16', 'de totalen van de drie kolommen', 'SOM, naar rechts doorvoeren'),
        ],
        opmaak=[
            'B2: notatie percentage.',
            'B5:D16: notatie valuta.',
            'Koptekst in rij 4: vet met achtergrondkleur. Rand rond A4:D16.',
        ],
        stappen=[
            ('Toon het percentage als percentage.',
             'Klik B2 aan en kies Start › Getal › Percentage. Er staat nu 7,00 %.'),
            ('Bereken de eerste verhoging.',
             'Klik C5 aan en typ =AFRONDEN(B5*$B$2;2). De dollartekens zorgen dat B2 blijft '
             'staan bij het doorvoeren. Voer door tot C14.'),
            ('Bereken de nieuwe prijs.',
             'Klik D5 aan en typ =B5+C5. Hier komt de verhoging erbij, dus plus. '
             'Voer door tot D14.'),
            ('Tel de drie kolommen op.',
             'Klik B16 aan en typ =SOM(B5:B14). Voer naar rechts door tot D16.'),
            ('Werk het blad af.',
             'Geef B5:D16 de notatie valuta, zet de koptekst in rij 4 in het vet met een '
             'achtergrondkleur en zet een rand rond A4:D16.'),
        ],
        klaar='Tien verhogingen en tien nieuwe prijzen, met drie kolomtotalen eronder.',
        controle='B16 plus C16 moet precies D16 geven. Klopt dat niet, dan zit er een fout in '
                 'een van de rijen.',
    ),
    dict(
        nr=4,
        titel='Bezoekers over een jaar',
        blad='4 Bezoekers',
        duur='5 minuten',
        doel='Twaalf maandcijfers samenvatten, en de drukke maanden er automatisch uit laten '
             'springen.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'AANTAL.ALS'],
        hulp=['Voorwaardelijke opmaak'],
        gegeven=[
            ('A4:A15', 'de twaalf maanden'),
            ('B4:B15', 'het aantal bezoekers per maand'),
        ],
        maken=[
            ('B17', 'het totale aantal bezoekers', 'SOM'),
            ('B18', 'het gemiddelde per maand', 'GEMIDDELDE'),
            ('B19', 'de drukste maand', 'MAX'),
            ('B20', 'de rustigste maand', 'MIN'),
            ('B21', 'het aantal maanden', 'AANTAL'),
            ('B22', 'het aantal maanden met meer dan 5000 bezoekers', 'AANTAL.ALS'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur.',
            'B4:B15: voorwaardelijke opmaak — alles boven het gemiddelde krijgt een kleur.',
            'Samenvattingsblok A17:B22: achtergrondkleur.',
        ],
        stappen=[
            ('Vul de samenvatting in.',
             'Klik B17 aan en typ =SOM(B4:B15). Daarna B18: =GEMIDDELDE(B4:B15), '
             'B19: =MAX(B4:B15), B20: =MIN(B4:B15) en B21: =AANTAL(B4:B15).'),
            ('Tel de drukke maanden.',
             'Klik B22 aan en typ =AANTAL.ALS(B4:B15;">5000"). Let op: een vergelijking als '
             'criterium staat helemaal tussen aanhalingstekens.'),
            ('Laat de drukke maanden oplichten.',
             'Selecteer B4 tot en met B15. Kies Start › Voorwaardelijke opmaak › Boven/onder › '
             'Boven gemiddelde, en kies een kleur. Excel rekent het gemiddelde zelf uit.'),
            ('Werk het blad af.',
             'Zet de koptekst in rij 3 in het vet met een achtergrondkleur en geef A17:B22 '
             'ook een kleur.'),
        ],
        klaar='Zes samenvattende cijfers, en in de kolom bezoekers springen de maanden boven '
              'het gemiddelde eruit.',
        controle='Tel de gekleurde maanden. Dat aantal hoort te kloppen met wat je ziet als je '
                 'de cijfers met B18 vergelijkt.',
    ),
    dict(
        nr=5,
        titel='Resultaten van de snoeicursus',
        blad='5 Snoeicursus',
        duur='6 minuten',
        doel='Twaalf cursisten automatisch geslaagd of niet geslaagd verklaren, en daarna '
             'tellen.',
        functies=['ALS', 'AANTAL.ALS', 'GEMIDDELDE'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Voorwaardelijke opmaak'],
        gegeven=[
            ('B2', 'de puntengrens vanaf wanneer iemand geslaagd is'),
            ('A5:A16', 'de namen van de cursisten'),
            ('B5:B16', 'hun punten op 100'),
        ],
        maken=[
            ('C5:C16', 'het resultaat: Geslaagd of Niet geslaagd',
             'ALS, met een absolute verwijzing naar B2'),
            ('B18', 'het aantal geslaagden', 'AANTAL.ALS'),
            ('B19', 'het aantal niet-geslaagden', 'AANTAL.ALS'),
            ('B20', 'het gemiddelde aantal punten', 'GEMIDDELDE'),
        ],
        opmaak=[
            'Koptekst in rij 4: vet met achtergrondkleur.',
            'C5:C16: voorwaardelijke opmaak — Niet geslaagd krijgt een andere kleur.',
            'B20: één cijfer na de komma.',
        ],
        stappen=[
            ('Laat het rekenblad beslissen.',
             'Klik C5 aan en typ =ALS(B5>=$B$2;"Geslaagd";"Niet geslaagd"). Let op de '
             'aanhalingstekens rond de woorden, en op >= in plaats van >. Voer door tot C16.'),
            ('Kijk naar Cédric Dhaene.',
             'Hij heeft precies 50, de grens zelf. Met >= hoort er Geslaagd te staan. '
             'Staat er Niet geslaagd, dan heb je > gebruikt in plaats van >=.'),
            ('Tel de twee groepen.',
             'Klik B18 aan en typ =AANTAL.ALS(C5:C16;"Geslaagd"). Daarna B19: '
             '=AANTAL.ALS(C5:C16;"Niet geslaagd"). Je telt in kolom C, waar de woorden staan.'),
            ('Bereken het gemiddelde.',
             'Klik B20 aan en typ =GEMIDDELDE(B5:B16). Let op: hier kijk je naar kolom B, '
             'de punten, niet naar kolom C.'),
            ('Werk het blad af.',
             'Selecteer C5:C16 en geef met voorwaardelijke opmaak (Tekst die bevat) een kleur '
             'aan Niet geslaagd. Zet de koptekst in rij 4 in het vet en B20 op één decimaal.'),
        ],
        klaar='Twaalf cursisten met een resultaat, twee aantallen en een gemiddelde.',
        controle='B18 plus B19 moet twaalf geven. Is het minder, dan loopt je bereik niet tot '
                 'rij 16.',
    ),
    dict(
        nr=6,
        titel='Bestellingen per leverancier',
        blad='6 Leveranciers',
        duur='6 minuten',
        doel='Vijftien bestelbonnen opsplitsen per leverancier, met één formule die je '
             'doorvoert.',
        functies=['AANTAL.ALS', 'SOM.ALS', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A18', 'de bonnummers'),
            ('B4:B18', 'de leverancier per bon'),
            ('C4:C18', 'het bedrag per bon'),
            ('A20:A22', 'de drie leveranciers — die gebruik je als criterium'),
        ],
        maken=[
            ('B20:B22', 'het aantal bonnen per leverancier',
             'AANTAL.ALS met een absoluut bereik, daarna doorvoeren'),
            ('C20:C22', 'het totale bedrag per leverancier',
             'SOM.ALS met absolute bereiken, daarna doorvoeren'),
            ('C24', 'het totaal van alle bonnen samen', 'SOM'),
        ],
        opmaak=[
            'Koptekst in rij 3 en rij 19: vet met achtergrondkleur.',
            'C4:C24: notatie valuta.',
            'Rand rond het samenvattingsblok A19:C22.',
        ],
        stappen=[
            ('Tel de bonnen van de eerste leverancier.',
             'Klik B20 aan en typ =AANTAL.ALS($B$4:$B$18;A20). Het bereik staat vast met '
             'dollartekens; A20 is het criterium en mag wél meeschuiven.'),
            ('Voer door tot B22.',
             'Nu telt B21 de bonnen van Terra Nova en B22 die van Groenwerk — zonder dat je '
             'de formule opnieuw typt. Dat is precies waarom het criterium uit een cel komt.'),
            ('Tel de bedragen per leverancier op.',
             'Klik C20 aan en typ =SOM.ALS($B$4:$B$18;A20;$C$4:$C$18). Voer door tot C22. '
             'Lees de volgorde als een zin: kijk in kolom B, zoek wat in A20 staat, tel de '
             'bedragen uit kolom C op.'),
            ('Tel alle bonnen samen.',
             'Klik C24 aan en typ =SOM(C4:C18).'),
            ('Werk het blad af.',
             'Geef kolom C de notatie valuta, zet de koptekst in rij 3 en rij 19 in het vet '
             'met een achtergrondkleur, en zet een rand rond A19:C22.'),
        ],
        klaar='Drie leveranciers met elk een aantal en een bedrag, en daaronder het totaal van '
              'alle bonnen.',
        controle='C20 plus C21 plus C22 moet precies C24 geven. Klopt dat niet, dan staat er '
                 'een leveranciersnaam verkeerd gespeld in de lijst of in je criterium.',
    ),
    dict(
        nr=7,
        titel='Zaadbestelling',
        blad='7 Zaden',
        duur='6 minuten',
        doel='Van tien codes de omschrijving en de prijs ophalen, en de bestelling '
             'doorrekenen.',
        functies=['VERT.ZOEKEN', 'AFRONDEN', 'SOM', 'SOM.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Beeld vastzetten',
              'Doorvoeren met de vulgreep'],
        gegeven=[
            ('A4:A13', 'de tien zaadcodes'),
            ('D4:D13', 'het bestelde aantal'),
            ('G3:I11', 'de zoektabel: code, omschrijving en prijs — niet aanpassen'),
        ],
        maken=[
            ('B4:B13', 'de omschrijving', 'VERT.ZOEKEN, kolom 2'),
            ('C4:C13', 'de prijs per stuk', 'VERT.ZOEKEN, kolom 3'),
            ('E4:E13', 'het bedrag: prijs maal aantal, afgerond op cent', 'AFRONDEN'),
            ('E15', 'het eindtotaal van de bestelling', 'SOM'),
            ('E17', 'wat er in totaal aan bloemenmengsel besteld is (code Z-02)', 'SOM.ALS'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur.',
            'C4:C13 en E4:E15: notatie valuta.',
            'Koppen vastzetten, zodat ze bij het scrollen blijven staan.',
            'Rand rond A3:E15.',
        ],
        stappen=[
            ('Haal de eerste omschrijving op.',
             'Klik B4 aan en typ =VERT.ZOEKEN(A4;$G$4:$I$11;2;ONWAAR). Voer door tot B13.'),
            ('Haal de prijzen op.',
             'Klik C4 aan en typ dezelfde formule met 3 in plaats van 2: '
             '=VERT.ZOEKEN(A4;$G$4:$I$11;3;ONWAAR). Voer door tot C13.'),
            ('Reken de bedragen uit.',
             'Klik E4 aan en typ =AFRONDEN(C4*D4;2). Voer door tot E13.'),
            ('Tel het eindtotaal op.',
             'Klik E15 aan en typ =SOM(E4:E13).'),
            ('Tel op wat er aan bloemenmengsel besteld is.',
             'Code Z-02 staat twee keer in de lijst. Klik E17 aan en typ '
             '=SOM.ALS(A4:A13;"Z-02";E4:E13). Zo tel je alleen de regels met die code op.'),
            ('Werk het blad af.',
             'Zet de koppen vast: klik A4 aan en kies Beeld › Blokkeren › Titels blokkeren. '
             'Geef C en E de notatie valuta, zet rij 3 in het vet met een achtergrondkleur '
             'en zet een rand rond A3:E15.'),
        ],
        klaar='Tien regels met omschrijving, prijs en bedrag, een eindtotaal, en het '
              'deeltotaal voor bloemenmengsel.',
        controle='Geen enkele cel mag #N/B tonen. Zie je die melding, dan zijn de dollartekens '
                 'rond de zoektabel vergeten.',
    ),
]
