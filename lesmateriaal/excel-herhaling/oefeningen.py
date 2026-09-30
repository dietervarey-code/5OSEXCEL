# -*- coding: utf-8 -*-
"""De zeven oefeningen van de herhalingsbundel.

Geen nieuwe leerstof: alle functies komen uit de basisbundel. Wat hier telt is
het aantal keer dat ze langskomen. Geen geneste functies.
"""

OEFENINGEN = [
    dict(
        nr=1,
        titel='Ontvangsten per dag',
        blad='1 Dagontvangsten',
        duur='5 minuten',
        doel='Een week ontvangsten optellen in twee richtingen: per dag en per betaalwijze.',
        functies=['SOM'],
        hulp=['Doorvoeren met de vulgreep', 'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A10', 'de zeven dagen van de week'),
            ('B4:D10', 'de ontvangsten per betaalwijze: contant, bancontact en online'),
        ],
        maken=[
            ('E4:E10', 'het dagtotaal', 'SOM over de rij'),
            ('B12:E12', 'het totaal per betaalwijze, en rechts het weektotaal',
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
            ('Tel de eerste kolom op.',
             'Klik B12 aan en typ =SOM(B4:B10). Voer die formule nu naar RECHTS door, '
             'tot en met E12. Sleep de vulgreep dus zijwaarts.'),
            ('Werk het blad af.',
             'Geef B4:E12 de notatie valuta. Zet de koptekst in rij 3 in het vet met een '
             'achtergrondkleur, en rij 12 in het vet met een bovenrand.'),
        ],
        klaar='Zeven dagtotalen, vier kolomtotalen, alles in euro, met een duidelijke koptekst '
              'en totaalrij.',
        controle='E12 is zowel de som van de zeven dagtotalen als de som van de drie '
                 'betaalwijzen. Komen die niet overeen, dan mis je een rij of een kolom.',
    ),
    dict(
        nr=2,
        titel='Gewerkte uren samenvatten',
        blad='2 Werkuren',
        duur='6 minuten',
        doel='Van acht medewerkers over drie weken vier kerncijfers halen.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'ALS', 'AANTAL.ALS'],
        hulp=['Doorvoeren met de vulgreep', 'Getalnotatie: valuta, percentage en decimalen',
              'Absolute celverwijzing: de dollartekens'],
        gegeven=[
            ('A4:A11', 'de namen van de acht medewerkers'),
            ('B4:D11', 'de gewerkte uren per week'),
        ],
        maken=[
            ('E4:E11', 'het totaal per medewerker', 'SOM over de rij'),
            ('B13', 'het totaal aantal gewerkte uren', 'SOM'),
            ('B14', 'het gemiddelde per medewerker', 'GEMIDDELDE'),
            ('B15', 'het hoogste totaal', 'MAX'),
            ('B16', 'het laagste totaal', 'MIN'),
            ('B17', 'het aantal medewerkers', 'AANTAL'),
            ('F4:F11', 'ja of nee: haalt de medewerker 110 uur of meer', 'ALS'),
            ('B18', 'het aantal medewerkers dat voltijds werkte', 'AANTAL.ALS'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'Kolom B tot E: één cijfer na de komma.',
            'Samenvattingsblok A13:B18: achtergrondkleur.',
        ],
        stappen=[
            ('Tel de uren per medewerker op.',
             'Klik E4 aan en typ =SOM(B4:D4). Voer door tot E11.'),
            ('Vul de samenvatting in.',
             'Klik B13 aan en typ =SOM(E4:E11). Daarna B14: =GEMIDDELDE(E4:E11), '
             'B15: =MAX(E4:E11), B16: =MIN(E4:E11) en B17: =AANTAL(E4:E11). '
             'Vijf keer hetzelfde bereik, vijf verschillende functies.'),
            ('Zet erbij wie voltijds werkte.',
             'Klik F4 aan en typ =ALS(E4>=110;"ja";"nee"). Voer door tot F11.'),
            ('Tel hoeveel dat er zijn.',
             'Klik B18 aan en typ =AANTAL.ALS(F4:F11;"ja").'),
            ('Werk het blad af.',
             'Zet de kolommen B tot E op één cijfer na de komma. Geef A13:B18 een '
             'achtergrondkleur en zet de koptekst in rij 3 in het vet.'),
        ],
        klaar='Acht totalen, een kolom met ja of nee, en daaronder zes samenvattende cijfers '
              'in een gekleurd blokje.',
        controle='B17 moet 8 geven — evenveel als er medewerkers in de lijst staan. '
                 'Geeft het een ander getal, dan klopt je bereik niet.',
    ),
    dict(
        nr=3,
        titel='Kortingsactie doorrekenen',
        blad='3 Kortingen',
        duur='6 minuten',
        doel='Op tien artikelen dezelfde korting toepassen, met één percentage dat op één '
             'plaats staat.',
        functies=['AFRONDEN', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep'],
        gegeven=[
            ('B2', 'het kortingspercentage — één keer, voor de hele lijst'),
            ('A5:A14', 'de artikelnamen'),
            ('B5:B14', 'de prijzen'),
        ],
        maken=[
            ('C5:C14', 'de korting in euro, afgerond op cent',
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
             'Klik B2 aan en kies Start › Getal › Percentage. Er staat nu 12,00 %.'),
            ('Bereken de eerste korting.',
             'Klik C5 aan en typ =AFRONDEN(B5*$B$2;2). De dollartekens zorgen dat B2 blijft '
             'staan bij het doorvoeren. Voer door tot C14.'),
            ('Bereken de nieuwe prijs.',
             'Klik D5 aan en typ =B5-C5. Voer door tot D14.'),
            ('Tel de drie kolommen op.',
             'Klik B16 aan en typ =SOM(B5:B14). Voer naar rechts door tot D16.'),
            ('Werk het blad af.',
             'Geef B5:D16 de notatie valuta, zet de koptekst in rij 4 in het vet met een '
             'achtergrondkleur en zet een rand rond A4:D16.'),
        ],
        klaar='Tien kortingen en tien nieuwe prijzen, met drie kolomtotalen eronder.',
        controle='B16 min C16 moet precies D16 geven. Klopt dat niet, dan zit er een fout in '
                 'een van de rijen.',
    ),
    dict(
        nr=4,
        titel='Verbruik over een jaar',
        blad='4 Verbruik',
        duur='5 minuten',
        doel='Twaalf maandcijfers samenvatten, en de dure maanden er automatisch uit laten '
             'springen.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'AANTAL.ALS'],
        hulp=['Voorwaardelijke opmaak'],
        gegeven=[
            ('A4:A15', 'de twaalf maanden'),
            ('B4:B15', 'het verbruik in kilowattuur'),
        ],
        maken=[
            ('B17', 'het totale jaarverbruik', 'SOM'),
            ('B18', 'het gemiddelde per maand', 'GEMIDDELDE'),
            ('B19', 'de hoogste maand', 'MAX'),
            ('B20', 'de laagste maand', 'MIN'),
            ('B21', 'het aantal maanden', 'AANTAL'),
            ('B22', 'het aantal maanden boven 1500 kWh', 'AANTAL.ALS'),
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
            ('Tel de dure maanden.',
             'Klik B22 aan en typ =AANTAL.ALS(B4:B15;">1500"). Let op: een vergelijking als '
             'criterium staat helemaal tussen aanhalingstekens.'),
            ('Laat de dure maanden oplichten.',
             'Selecteer B4 tot en met B15. Kies Start › Voorwaardelijke opmaak › Boven/onder › '
             'Boven gemiddelde, en kies een kleur. Excel rekent het gemiddelde zelf uit.'),
            ('Werk het blad af.',
             'Zet de koptekst in rij 3 in het vet met een achtergrondkleur en geef A17:B22 '
             'ook een kleur.'),
        ],
        klaar='Zes samenvattende cijfers, en in de kolom verbruik springen de maanden boven '
              'het gemiddelde eruit.',
        controle='Tel de gekleurde maanden. Dat aantal hoort te kloppen met wat je ziet als je '
                 'de cijfers vergelijkt met B18.',
    ),
    dict(
        nr=5,
        titel='Inschrijvingen indelen',
        blad='5 Inschrijvingen',
        duur='6 minuten',
        doel='Twaalf deelnemers automatisch indelen in jeugd of volwassene, en daarna tellen.',
        functies=['ALS', 'AANTAL.ALS', 'GEMIDDELDE'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Voorwaardelijke opmaak'],
        gegeven=[
            ('B2', 'de leeftijdsgrens vanaf wanneer iemand volwassene is'),
            ('A5:A16', 'de namen van de deelnemers'),
            ('B5:B16', 'hun leeftijd'),
        ],
        maken=[
            ('C5:C16', 'de categorie: Jeugd of Volwassene',
             'ALS, met een absolute verwijzing naar B2'),
            ('B18', 'het aantal volwassenen', 'AANTAL.ALS'),
            ('B19', 'het aantal jeugd', 'AANTAL.ALS'),
            ('B20', 'de gemiddelde leeftijd', 'GEMIDDELDE'),
        ],
        opmaak=[
            'Koptekst in rij 4: vet met achtergrondkleur.',
            'C5:C16: voorwaardelijke opmaak — Jeugd krijgt een andere kleur dan Volwassene.',
            'B20: één cijfer na de komma.',
        ],
        stappen=[
            ('Laat het rekenblad indelen.',
             'Klik C5 aan en typ =ALS(B5>=$B$2;"Volwassene";"Jeugd"). Let op de '
             'aanhalingstekens rond de woorden, en op >= in plaats van >. Voer door tot C16.'),
            ('Kijk naar Gilles Hermans.',
             'Hij is precies 18. Met >= hoort er Volwassene te staan. Staat er Jeugd, dan heb '
             'je > gebruikt in plaats van >=.'),
            ('Tel de twee groepen.',
             'Klik B18 aan en typ =AANTAL.ALS(C5:C16;"Volwassene"). Daarna B19: '
             '=AANTAL.ALS(C5:C16;"Jeugd"). Je telt in kolom C, waar de woorden staan.'),
            ('Bereken de gemiddelde leeftijd.',
             'Klik B20 aan en typ =GEMIDDELDE(B5:B16). Let op: hier kijk je naar kolom B, '
             'de leeftijden, niet naar kolom C.'),
            ('Werk het blad af.',
             'Selecteer C5:C16 en geef met voorwaardelijke opmaak (Tekst die bevat) een kleur '
             'aan Jeugd. Zet de koptekst in rij 4 in het vet en B20 op één decimaal.'),
        ],
        klaar='Twaalf deelnemers ingedeeld, twee aantallen en een gemiddelde leeftijd.',
        controle='B18 plus B19 moet twaalf geven. Is het minder, dan loopt je bereik niet tot '
                 'rij 16.',
    ),
    dict(
        nr=6,
        titel='Verkoop per afdeling',
        blad='6 Afdelingen',
        duur='6 minuten',
        doel='Vijftien bonnen opsplitsen per afdeling, met één formule die je doorvoert.',
        functies=['AANTAL.ALS', 'SOM.ALS', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A18', 'de bonnummers'),
            ('B4:B18', 'de afdeling per bon'),
            ('C4:C18', 'het bedrag per bon'),
            ('A20:A22', 'de drie afdelingen — die gebruik je als criterium'),
        ],
        maken=[
            ('B20:B22', 'het aantal bonnen per afdeling',
             'AANTAL.ALS met een absoluut bereik, daarna doorvoeren'),
            ('C20:C22', 'het totale bedrag per afdeling',
             'SOM.ALS met absolute bereiken, daarna doorvoeren'),
            ('C24', 'het totaal van alle bonnen samen', 'SOM'),
        ],
        opmaak=[
            'Koptekst in rij 3 en rij 19: vet met achtergrondkleur.',
            'C4:C24: notatie valuta.',
            'Rand rond het samenvattingsblok A19:C22.',
        ],
        stappen=[
            ('Tel de bonnen van de eerste afdeling.',
             'Klik B20 aan en typ =AANTAL.ALS($B$4:$B$18;A20). Het bereik staat vast met '
             'dollartekens; A20 is het criterium en mag wél meeschuiven.'),
            ('Voer door tot B22.',
             'Nu telt B21 de bonnen van Sanitair en B22 die van Elektro — zonder dat je de '
             'formule opnieuw typt. Dat is waarom het criterium uit een cel komt.'),
            ('Tel de bedragen per afdeling op.',
             'Klik C20 aan en typ =SOM.ALS($B$4:$B$18;A20;$C$4:$C$18). Voer door tot C22. '
             'Lees de volgorde als een zin: kijk in kolom B, zoek wat in A20 staat, tel de '
             'bedragen uit kolom C op.'),
            ('Tel alle bonnen samen.',
             'Klik C24 aan en typ =SOM(C4:C18).'),
            ('Werk het blad af.',
             'Geef kolom C de notatie valuta, zet de koptekst in rij 3 en rij 19 in het vet '
             'met een achtergrondkleur, en zet een rand rond A19:C22.'),
        ],
        klaar='Drie afdelingen met elk een aantal en een bedrag, en daaronder het totaal van '
              'alle bonnen.',
        controle='C20 plus C21 plus C22 moet precies C24 geven. Klopt dat niet, dan staat er '
                 'een afdelingsnaam verkeerd gespeld in de lijst of in je criterium.',
    ),
    dict(
        nr=7,
        titel='Materiaalbestelling',
        blad='7 Materiaal',
        duur='6 minuten',
        doel='Van tien codes de omschrijving en de prijs ophalen, en de bestelling doorrekenen.',
        functies=['VERT.ZOEKEN', 'AFRONDEN', 'SOM', 'SOM.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Beeld vastzetten',
              'Doorvoeren met de vulgreep'],
        gegeven=[
            ('A4:A13', 'de tien materiaalcodes'),
            ('D4:D13', 'het bestelde aantal'),
            ('G3:I11', 'de zoektabel: code, omschrijving en prijs — niet aanpassen'),
        ],
        maken=[
            ('B4:B13', 'de omschrijving', 'VERT.ZOEKEN, kolom 2'),
            ('C4:C13', 'de prijs per stuk', 'VERT.ZOEKEN, kolom 3'),
            ('E4:E13', 'het bedrag: prijs maal aantal, afgerond op cent', 'AFRONDEN'),
            ('E15', 'het eindtotaal van de bestelling', 'SOM'),
            ('E17', 'wat er in totaal aan cement besteld is (code M-01)', 'SOM.ALS'),
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
            ('Tel op wat er aan cement besteld is.',
             'Code M-01 staat twee keer in de lijst. Klik E17 aan en typ '
             '=SOM.ALS(A4:A13;"M-01";E4:E13). Zo tel je alleen de regels met die code op.'),
            ('Werk het blad af.',
             'Zet de koppen vast: klik A4 aan en kies Beeld › Blokkeren › Titels blokkeren. '
             'Geef C en E de notatie valuta, zet rij 3 in het vet met een achtergrondkleur '
             'en zet een rand rond A3:E15.'),
        ],
        klaar='Tien regels met omschrijving, prijs en bedrag, een eindtotaal, en het '
              'deeltotaal voor cement.',
        controle='Geen enkele cel mag #N/B tonen. Zie je die melding, dan zijn de dollartekens '
                 'rond de zoektabel vergeten.',
    ),
]
