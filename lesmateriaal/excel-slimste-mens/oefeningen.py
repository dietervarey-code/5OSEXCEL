# -*- coding: utf-8 -*-
"""De vijf werkbladen van de zelfstudiebundel.

Deze bundel wordt alleen gemaakt, zonder leerkracht in de buurt. Daarom:

* de stappen geven de formule letterlijk — hier mag niemand vastlopen op
  iets routineus;
* elk blad eindigt met een CONTROLEGETAL, zodat ze zelf kunnen nagaan of ze
  goed zitten zonder dat iemand het hoeft te zeggen;
* elk blad heeft een lijstje 'Loop je vast?' met de drie fouten die het
  vaakst gemaakt worden en wat je er dan aan doet.

Geen geneste functies. Alleen de tien functies van de basisbundel, met de
nadruk op SOM, AANTAL.ALS en VERT.ZOEKEN.
"""

OEFENINGEN = [
    dict(
        nr=1,
        titel='De kijkcijfers',
        blad='1 Kijkcijfers',
        duur='5 minuten',
        doel='Tien afleveringen optellen in twee richtingen: per aflevering en per manier '
             'van kijken.',
        functies=['SOM'],
        hulp=['Doorvoeren met de vulgreep',
              'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A13', 'de tien afleveringen'),
            ('B4:D13', 'het aantal kijkers: live, uitgesteld en online'),
        ],
        maken=[
            ('E4:E13', 'het totale aantal kijkers per aflevering', 'SOM over de rij'),
            ('B15:E15', 'het totaal per manier van kijken, en rechts het eindtotaal',
             'SOM over de kolom, naar rechts doorvoeren'),
        ],
        opmaak=[
            'Koprij 3: vet met een achtergrondkleur, gecentreerd.',
            'B4:E15: getalnotatie met een puntje tussen de duizendtallen en geen '
            'cijfers na de komma.',
            'Totaalrij 15: vet met een bovenrand.',
        ],
        stappen=[
            ('Tel de eerste aflevering op.',
             'Klik E4 aan en typ =SOM(B4:D4). Druk op Enter. Pak het blokje rechtsonder in '
             'E4 vast en sleep tot E13.'),
            ('Tel de eerste kolom op.',
             'Klik B15 aan en typ =SOM(B4:B13). Voer die formule nu naar RECHTS door, tot '
             'en met E15. Je sleept de vulgreep dus zijwaarts, niet naar beneden.'),
            ('Maak de getallen leesbaar.',
             'Selecteer B4:E15. Kies Start › Getal › Getalnotatie en zet de '
             'duizendtalscheiding aan. Zet de decimalen op 0. Er staat nu 812.340 in '
             'plaats van 812340.'),
            ('Werk het blad af.',
             'Zet rij 3 in het vet met een achtergrondkleur en centreer de koppen. Zet rij '
             '15 in het vet met een bovenrand.'),
        ],
        controlecel='E15',
        klaar='Tien rijtotalen, vier kolomtotalen, alles met een duizendtalscheiding, en '
              'een koprij en totaalrij die eruit springen.',
        controle='E15 kun je op twee manieren krijgen: als som van de tien afleveringen, of '
                 'als som van de drie kolommen. Allebei horen ze hetzelfde te geven.',
        vastgelopen=[
            ('In E15 staat niet hetzelfde als de som van E4 tot E13.',
             'Je hebt B15 naar beneden doorgevoerd in plaats van naar rechts. Wis B15:E15 '
             'en begin opnieuw: typ de formule in B15 en sleep zijwaarts.'),
            ('Er staat ###### in een cel.',
             'Dat is geen fout. De kolom is te smal. Dubbelklik op de rand tussen twee '
             'kolomletters; de kolom past zich dan vanzelf aan.'),
            ('Het totaal klopt niet helemaal.',
             'Kijk of je bereik tot rij 13 loopt. Klik E13 aan en lees in de formulebalk '
             'welke cellen er in je formule staan.'),
        ],
    ),
    dict(
        nr=2,
        titel='De achttien deelnemers',
        blad='2 Deelnemers',
        duur='10 minuten',
        doel='Van achttien deelnemers een kolom maken die aanduidt wie naar de finaleweek '
             'mag, en er daarna zeven cijfers uit halen.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'ALS', 'AANTAL.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Getalnotatie: valuta, percentage en decimalen', 'Beeld vastzetten'],
        gegeven=[
            ('B2', 'vanaf hoeveel overwinningen je naar de finaleweek mag'),
            ('A5:A22', 'de achttien deelnemers'),
            ('B5:B22', 'hun beroep'),
            ('C5:C22', 'het aantal afleveringen dat ze meespeelden'),
            ('D5:D22', 'het aantal afleveringen dat ze wonnen'),
            ('E5:E22', 'het aantal seconden dat ze bij elkaar speelden'),
        ],
        maken=[
            ('F5:F22', 'ja of nee: mag de deelnemer naar de finaleweek',
             'ALS, met een absolute verwijzing naar B2'),
            ('B24', 'het totale aantal gespeelde afleveringen', 'SOM'),
            ('B25', 'het totale aantal overwinningen', 'SOM'),
            ('B26', 'het gemiddelde aantal afleveringen per deelnemer', 'GEMIDDELDE'),
            ('B27', 'het hoogste aantal overwinningen', 'MAX'),
            ('B28', 'het laagste aantal overwinningen', 'MIN'),
            ('B29', 'het aantal deelnemers', 'AANTAL'),
            ('B30', 'het aantal deelnemers dat naar de finaleweek mag', 'AANTAL.ALS'),
        ],
        opmaak=[
            'Koprij 4: vet met een achtergrondkleur, gecentreerd.',
            'B26: één cijfer na de komma.',
            'Samenvattingsblok A24:B30: een achtergrondkleur en een rand eromheen.',
            'Koprij blokkeren, zodat ze blijft staan als je naar beneden scrolt.',
        ],
        stappen=[
            ('Zet erbij wie naar de finaleweek mag.',
             'Klik F5 aan en typ =ALS(D5>=$B$2;"ja";"nee"). Let op drie dingen: >= en niet '
             'alleen >, de aanhalingstekens rond ja en nee, en de dollartekens rond B2. '
             'Voer door tot F22.'),
            ('Kijk even naar Hanne Dewitte en Tom Declercq.',
             'Zij hebben allebei precies 3 overwinningen, net de grens. Met >= staat er bij '
             'allebei ja. Staat er nee, dan heb je > getypt in plaats van >=.'),
            ('Vul de eerste twee totalen in.',
             'Klik B24 aan en typ =SOM(C5:C22). Klik B25 aan en typ =SOM(D5:D22). '
             'Let op: B24 kijkt naar kolom C, B25 naar kolom D.'),
            ('Vul de vier cijfers daaronder in.',
             'B26: =GEMIDDELDE(C5:C22). B27: =MAX(D5:D22). B28: =MIN(D5:D22). '
             'B29: =AANTAL(C5:C22). Vier keer bijna dezelfde formule, vier verschillende '
             'functies.'),
            ('Tel de finalisten.',
             'Klik B30 aan en typ =AANTAL.ALS(F5:F22;"ja"). Je telt in kolom F, waar de '
             'woorden staan — niet in kolom D.'),
            ('Werk het blad af.',
             'Zet B26 op één decimaal. Geef A24:B30 een achtergrondkleur en een rand. Zet '
             'rij 4 in het vet. Klik dan A5 aan en kies Beeld › Blokkeren › Titels '
             'blokkeren.'),
        ],
        controlecel='B29',
        klaar='Een kolom met achttien keer ja of nee, en daaronder zeven cijfers in een '
              'gekleurd kader.',
        controle='B29 telt hoeveel deelnemers er in de lijst staan. Je kunt ze ook gewoon '
                 'natellen: het moeten er evenveel zijn.',
        vastgelopen=[
            ('In kolom F staat overal nee, of overal ja.',
             'De dollartekens rond B2 ontbreken. Klik F22 aan en lees de formulebalk: wijst '
             'hij nog naar B2, of naar een lege cel eronder? Zet $B$2 en voer opnieuw door.'),
            ('In kolom F staat #NAAM?.',
             'De aanhalingstekens rond ja en nee ontbreken. Zonder aanhalingstekens denkt '
             'Excel dat ja een functie is.'),
            ('B30 geeft 0.',
             'Je telt waarschijnlijk in kolom D in plaats van in kolom F. AANTAL.ALS zoekt '
             'het woord "ja", en dat staat in kolom F.'),
        ],
    ),
    dict(
        nr=3,
        titel='De vragen per thema',
        blad='3 Themas',
        duur='9 minuten',
        doel='Vierentwintig vragen opsplitsen per thema, met één formule die je doorvoert — '
             'dus met het thema uit een cel in plaats van ingetypt.',
        functies=['AANTAL.ALS', 'SOM.ALS', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak'],
        gegeven=[
            ('A4:A27', 'de vierentwintig vraagnummers'),
            ('B4:B27', 'het thema van elke vraag'),
            ('C4:C27', 'in welke ronde de vraag gesteld werd'),
            ('D4:D27', 'hoeveel seconden er met die vraag gewonnen werden'),
            ('A30:A35', 'de zes themas — die gebruik je zo als criterium'),
        ],
        maken=[
            ('B30:B35', 'het aantal vragen per thema',
             'AANTAL.ALS met een absoluut bereik, daarna doorvoeren'),
            ('C30:C35', 'het totale aantal seconden per thema',
             'SOM.ALS met absolute bereiken, daarna doorvoeren'),
            ('C37', 'het totaal van alle seconden samen', 'SOM'),
        ],
        opmaak=[
            'Koprij 3 en koprij 29: vet met een achtergrondkleur.',
            'Een rand rond het blokje A29:C35, en C37 in het vet.',
            'Voorwaardelijke opmaak op C30:C35: het thema met de meeste seconden krijgt '
            'een kleur (gebruik Bovenste/onderste regels › Bovenste 1 items).',
        ],
        stappen=[
            ('Tel de vragen van het eerste thema.',
             'Klik B30 aan en typ =AANTAL.ALS($B$4:$B$27;A30). Het bereik staat vast met '
             'dollartekens, A30 niet — die moet juist meeschuiven. Voer door tot B35.'),
            ('Kijk of het klopt.',
             'Klik B31 aan en lees de formulebalk. Het bereik hoort nog altijd $B$4:$B$27 '
             'te zijn, en het criterium A31. Is het bereik meegeschoven, dan zijn de '
             'dollartekens vergeten.'),
            ('Tel de seconden per thema op.',
             'Klik C30 aan en typ =SOM.ALS($B$4:$B$27;A30;$C$4:$C$27). Fout! De seconden '
             'staan in kolom D, niet in kolom C. Typ dus '
             '=SOM.ALS($B$4:$B$27;A30;$D$4:$D$27) en voer door tot C35.'),
            ('Lees de formule als een zin.',
             'Kijk in kolom B, zoek wat er in A30 staat, en tel dan de seconden uit kolom D '
             'op. Dat is precies wat SOM.ALS doet, in die volgorde.'),
            ('Tel alles samen.',
             'Klik C37 aan en typ =SOM(D4:D27). Let op: hier tel je de hele kolom D op, '
             'niet de zes deeltotalen.'),
            ('Werk het blad af.',
             'Zet een rand rond A29:C35, maak rij 3 en rij 29 vet met een achtergrondkleur, '
             'en geef C37 vet. Selecteer dan C30:C35 en kies Start › Voorwaardelijke '
             'opmaak › Bovenste/onderste regels › Bovenste 10 items, en zet het getal op 1.'),
        ],
        controlecel='C37',
        klaar='Zes themas met elk een aantal vragen en een aantal seconden, met daaronder '
              'het totaal, en het drukste thema dat eruit springt.',
        controle='De zes getallen in kolom C moeten samen precies C37 geven. Tel ze even na '
                 'met je ogen. Komt het niet uit, dan staat er een thema verkeerd gespeld.',
        vastgelopen=[
            ('Alle zes de getallen in kolom B zijn hetzelfde.',
             'Je hebt ook het criterium vastgezet ($A$30). Het bereik staat vast, het '
             'criterium niet. Typ A30 zonder dollartekens en voer opnieuw door.'),
            ('Vanaf de tweede rij staat er onzin.',
             'Je hebt niets vastgezet. Het bereik $B$4:$B$27 moet wél dollartekens hebben, '
             'anders schuift het mee naar beneden.'),
            ('C30 geeft 0.',
             'Je telt het verkeerde bereik op. Het derde stuk van SOM.ALS moet $D$4:$D$27 '
             'zijn: daar staan de seconden.'),
        ],
    ),
    dict(
        nr=4,
        titel='Eén aflevering uitgewerkt',
        blad='4 Rondes',
        duur='9 minuten',
        doel='Van twaalf rondecodes de naam en de waarde ophalen uit een tabel, en de '
             'aflevering doorrekenen.',
        functies=['VERT.ZOEKEN', 'SOM', 'AFRONDEN'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Beeld vastzetten'],
        gegeven=[
            ('A4:A15', 'de twaalf rondecodes'),
            ('D4:D15', 'het aantal juiste antwoorden in die ronde'),
            ('G3:I9', 'de rondetabel: code, naam en seconden per juist antwoord — '
                      'niet aanpassen'),
        ],
        maken=[
            ('B4:B15', 'de naam van de ronde', 'VERT.ZOEKEN, kolom 2'),
            ('C4:C15', 'het aantal seconden per juist antwoord', 'VERT.ZOEKEN, kolom 3'),
            ('E4:E15', 'de gewonnen seconden: seconden per antwoord maal het aantal juiste '
                       'antwoorden', 'een formule, geen functie'),
            ('D17:E17', 'het totaal van beide kolommen', 'SOM, naar rechts doorvoeren'),
            ('E18', 'gemiddeld aantal seconden per juist antwoord, op één cijfer na de '
                    'komma', 'AFRONDEN'),
        ],
        opmaak=[
            'Koprij 3: vet met een achtergrondkleur, gecentreerd.',
            'De rondetabel G3:I9: een lichte vulling en een rand eromheen, zodat meteen '
            'te zien is dat je er niet aan mag komen.',
            'Totaalrij 17: vet met een bovenrand. Rand rond A3:E17.',
        ],
        stappen=[
            ('Haal de eerste rondenaam op.',
             'Klik B4 aan en typ =VERT.ZOEKEN(A4;$G$4:$I$9;2;ONWAAR). Lees het als: zoek '
             'wat in A4 staat, in de tabel G4 tot I9, en geef me de 2de kolom. Voer door '
             'tot B15.'),
            ('Haal de seconden per antwoord op.',
             'Klik C4 aan en typ dezelfde formule met een 3 in plaats van een 2: '
             '=VERT.ZOEKEN(A4;$G$4:$I$9;3;ONWAAR). Voer door tot C15.'),
            ('Waarom die dollartekens?',
             'Klik C15 aan en lees de formulebalk. Staat er nog $G$4:$I$9? Goed. Zonder '
             'dollartekens zou de tabel mee naar beneden geschoven zijn en zou je onderaan '
             '#N/B krijgen.'),
            ('Reken de gewonnen seconden uit.',
             'Klik E4 aan en typ =C4*D4. Voer door tot E15.'),
            ('Tel de twee kolommen op.',
             'Klik D17 aan en typ =SOM(D4:D15). Voer naar rechts door tot E17.'),
            ('Bereken het gemiddelde.',
             'Klik E18 aan en typ =AFRONDEN(E17/D17;1). Je deelt de gewonnen seconden door '
             'het aantal juiste antwoorden, en houdt één cijfer na de komma over.'),
            ('Werk het blad af.',
             'Geef de rondetabel een lichte vulling en een rand. Zet rij 3 in het vet met '
             'een achtergrondkleur, rij 17 in het vet met een bovenrand, en zet een rand '
             'rond A3:E17.'),
        ],
        controlecel='E17',
        klaar='Twaalf rondenamen en twaalf waarden die je nergens hebt ingetypt, met twee '
              'totalen en een gemiddelde eronder.',
        controle='Geen enkele cel mag #N/B tonen. En E17 gedeeld door D17 hoort ongeveer '
                 'E18 te geven — dat is dezelfde berekening, dus dat klopt altijd als je '
                 'het goed doet.',
        vastgelopen=[
            ('Onderaan staat #N/B, bovenaan niet.',
             'De dollartekens rond de tabel ontbreken, waardoor de tabel mee naar beneden '
             'schoof. Zet $G$4:$I$9 en voer opnieuw door.'),
            ('Overal staat #N/B.',
             'De code die je zoekt staat niet in de tabel, of je zoekt in de verkeerde '
             'kolom. Het eerste stuk van VERT.ZOEKEN moet A4 zijn, en de tabel moet met '
             'kolom G beginnen — daar staan de codes.'),
            ('In kolom B staan getallen in plaats van namen.',
             'Je hebt een 3 getypt waar een 2 hoort. Het derde stuk van de formule zegt '
             'welke kolom je terugkrijgt: 2 is de naam, 3 is het aantal seconden.'),
        ],
    ),
    dict(
        nr=5,
        titel='De finaleweek',
        blad='5 Finaleweek',
        duur='7 minuten',
        doel='Van acht startnummers de naam opzoeken, de drie rondes optellen en zien wie '
             'door is.',
        functies=['VERT.ZOEKEN', 'SOM', 'ALS', 'AANTAL.ALS', 'GEMIDDELDE', 'MAX'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak'],
        gegeven=[
            ('B2', 'vanaf hoeveel seconden je doorgaat'),
            ('A5:A12', 'de acht startnummers'),
            ('C5:E12', 'de seconden per ronde'),
            ('I4:J12', 'de deelnemerslijst: startnummer en naam — niet aanpassen'),
        ],
        maken=[
            ('B5:B12', 'de naam van de deelnemer', 'VERT.ZOEKEN, kolom 2'),
            ('F5:F12', 'het totaal van de drie rondes', 'SOM over de rij'),
            ('G5:G12', 'ja of nee: gaat de deelnemer door',
             'ALS, met een absolute verwijzing naar B2'),
            ('B14', 'het aantal deelnemers dat doorgaat', 'AANTAL.ALS'),
            ('B15', 'het gemiddelde totaal', 'GEMIDDELDE'),
            ('B16', 'het hoogste totaal', 'MAX'),
        ],
        opmaak=[
            'Koprij 4: vet met een achtergrondkleur, gecentreerd.',
            'B15: één cijfer na de komma.',
            'Voorwaardelijke opmaak op G5:G12: wie doorgaat krijgt een groene kleur '
            '(Markeringsregels › Tekst die bevat › ja).',
        ],
        stappen=[
            ('Haal de namen op.',
             'Klik B5 aan en typ =VERT.ZOEKEN(A5;$I$5:$J$12;2;ONWAAR). Voer door tot B12. '
             'Dit is dezelfde formule als op blad 4, met een andere tabel.'),
            ('Tel de drie rondes op.',
             'Klik F5 aan en typ =SOM(C5:E5). Voer door tot F12.'),
            ('Zet erbij wie doorgaat.',
             'Klik G5 aan en typ =ALS(F5>=$B$2;"ja";"nee"). Voer door tot G12.'),
            ('Kijk even naar startnummer 6.',
             'Stijn Boeykens komt op precies 150 seconden, net de grens. Met >= gaat hij '
             'door. Staat er nee bij hem, dan heb je > getypt in plaats van >=.'),
            ('Vul de drie cijfers onderaan in.',
             'B14: =AANTAL.ALS(G5:G12;"ja"). B15: =GEMIDDELDE(F5:F12). B16: =MAX(F5:F12).'),
            ('Werk het blad af.',
             'Zet B15 op één decimaal, maak rij 4 vet met een achtergrondkleur, en geef '
             'G5:G12 voorwaardelijke opmaak: tekst die "ja" bevat krijgt een groene vulling.'),
        ],
        controlecel='B14',
        klaar='Acht namen die je niet hebt ingetypt, acht totalen, acht keer ja of nee, en '
              'drie cijfers eronder.',
        controle='Tel de ja\'s in kolom G met je ogen. Dat aantal hoort in B14 te staan. '
                 'Klopt het niet, kijk dan naar startnummer 6: die zit precies op de grens.',
        vastgelopen=[
            ('In kolom B staat #N/B.',
             'De dollartekens rond de deelnemerslijst ontbreken, of je tabel begint niet '
             'bij I5. De startnummers staan in kolom I, dus daar moet de tabel beginnen.'),
            ('In kolom F staan de startnummers mee opgeteld.',
             'Je bereik begint bij A5 in plaats van bij C5. SOM(C5:E5) telt alleen de drie '
             'rondes op.'),
            ('B14 geeft 8 of 0.',
             'Je telt in de verkeerde kolom, of het criterium klopt niet. Het moet '
             'AANTAL.ALS over G5:G12 zijn, met "ja" tussen aanhalingstekens.'),
        ],
    ),
]
