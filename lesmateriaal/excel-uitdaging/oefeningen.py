# -*- coding: utf-8 -*-
"""De vijf werkbladen van de uitdagingsopdracht.

Belangrijk verschil met de basisbundel: hier staat NIET welke formule je moet
typen. Er staat wat er moet uitkomen en met welke functie. Hoe je het in
elkaar zet, zoek je zelf uit — met de kaarten uit uitleg.py erbij.

controleer.py weigert dan ook elke opdrachttekst waarin een formule staat.
"""

OEFENINGEN = [
    dict(
        nr=1,
        titel='De ticketverkoop afsluiten',
        blad='1 Boekingen',
        duur='12 minuten',
        doel='Twintig boekingen doorrekenen met een staffelprijs, en er daarna vijf cijfers '
             'uit trekken die de avond samenvatten.',
        functies=['VERT.ZOEKEN (benaderend)', 'AFRONDEN', 'SOM', 'SOMMEN.ALS',
                  'AANTALLEN.ALS', 'GEMIDDELDE.ALS', 'MAX', 'INDEX', 'VERGELIJKEN'],
        kaarten=['VERT.ZOEKEN met WAAR — benaderend zoeken',
                 'SOMMEN.ALS — optellen met meer dan één voorwaarde',
                 'AANTALLEN.ALS — tellen met meer dan één voorwaarde',
                 'GEMIDDELDE.ALS — het gemiddelde van een deel',
                 'INDEX en VERGELIJKEN — niet de waarde maar de naam',
                 'Geneste functies — een functie binnen een functie'],
        gegeven=[
            ('A4:A23', 'de boekingsnummers'),
            ('B4:B23', 'de naam van de groep'),
            ('C4:C23', 'het aantal personen'),
            ('D4:D23', 'het tijdslot waarop de groep binnen mocht'),
            ('E4:E23', 'het kanaal: online of aan de kassa'),
            ('I3:K7', 'de tarievenstaffel — niet aanpassen. De eerste kolom bevat de '
                      'ONDERgrenzen, van klein naar groot'),
        ],
        maken=[
            ('F4:F23', 'de prijs per persoon volgens de staffel',
             'VERT.ZOEKEN, benaderend (WAAR)'),
            ('G4:G23', 'het bedrag van de boeking, afgerond op cent', 'AFRONDEN'),
            ('C25', 'het totale aantal bezoekers van de avond', 'SOM'),
            ('C26', 'de totale ticketomzet', 'SOM'),
            ('C27', 'de omzet van de online boekingen van tien personen of meer',
             'SOMMEN.ALS'),
            ('C28', 'het aantal boekingen aan de kassa met minder dan vijf personen',
             'AANTALLEN.ALS'),
            ('C29', 'de gemiddelde groepsgrootte van de online boekingen', 'GEMIDDELDE.ALS'),
            ('C30', 'het aantal personen van de grootste groep', 'MAX'),
            ('C31', 'de naam van de grootste groep', 'INDEX met VERGELIJKEN'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'F4:G23 en C26:C27: notatie valuta.',
            'C29: twee cijfers na de komma.',
            'Tarievenstaffel I3:K7: rand eromheen en een lichte vulling, zodat meteen te '
            'zien is dat het brongegevens zijn.',
            'Zet een autofilter op rij 3.',
        ],
        hints=[
            'De staffel staat van klein naar groot. Dat is geen toeval: benaderend zoeken '
            'werkt alleen zo, en de kaart legt uit waarom.',
            'Zet de staffel vast met dollartekens vóór je de kolom doorvoert. Anders '
            'schuift de tabel mee naar beneden en kloppen de laatste rijen niet meer.',
            'Twee van de drie nieuwe .ALS-functies beginnen met het bereik waarin je kijkt. '
            'Eén begint met het bereik dat je optelt. Zoek op de kaart welke.',
            'C31 vraagt een naam, geen getal. Twee functies in elkaar dus. Bouw ze eerst '
            'los op in een lege cel en schuif ze daarna naar binnen.',
        ],
        klaar='Twintig bedragen in kolom G, en zeven antwoorden onder de lijst — waarvan er '
              'één een naam is en geen getal.',
        controle='In de staffel staan vier verschillende prijzen. Alle vier horen in kolom F '
                 'voor te komen. Zie je er maar drie, dan pakt je benaderend zoeken ergens '
                 'de verkeerde schijf.',
    ),
    dict(
        nr=2,
        titel='Welke attractie trok het meest',
        blad='2 Attracties',
        duur='7 minuten',
        doel='Een kruistabel van zes attracties en vijf uurblokken in twee richtingen '
             'optellen, en er daarna namen uit halen in plaats van getallen.',
        functies=['SOM', 'MAX', 'GROOTSTE', 'INDEX', 'VERGELIJKEN', 'AFRONDEN'],
        kaarten=['INDEX en VERGELIJKEN — niet de waarde maar de naam',
                 'GROOTSTE en KLEINSTE — de tweede, de derde',
                 'Geneste functies — een functie binnen een functie'],
        gegeven=[
            ('A4:A9', 'de zes attracties'),
            ('B3:F3', 'de vijf uurblokken'),
            ('B4:F9', 'het aantal bezoekers per attractie per uurblok'),
        ],
        maken=[
            ('G4:G9', 'het totaal per attractie', 'SOM over de rij'),
            ('B11:G11', 'het totaal per uurblok, en rechts het totaal van de hele avond',
             'SOM over de kolom, naar rechts doorvoeren'),
            ('B13', 'de naam van de drukste attractie',
             'INDEX met VERGELIJKEN en MAX'),
            ('B14', 'het uurblok waarin de meeste bezoekers rondliepen',
             'INDEX met VERGELIJKEN en MAX, maar zijwaarts'),
            ('B15', 'de naam van de op één na drukste attractie',
             'INDEX met VERGELIJKEN en GROOTSTE'),
            ('B16', 'het aandeel van de drukste attractie in het totaal van de avond',
             'AFRONDEN'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'B4:F9: voorwaardelijke opmaak met een kleurenschaal, zodat de piek meteen '
            'opvalt.',
            'Kolom G en rij 11: vet, met een rand die ze van de gegevens scheidt.',
            'B16: notatie percentage met één cijfer na de komma.',
        ],
        hints=[
            'B13 vraagt een naam. MAX geeft een getal. Je hebt dus iets nodig dat van een '
            'getal naar de juiste rij gaat, en van die rij naar de naam.',
            'B14 werkt net als B13, maar liggend: de koppen staan in rij 3, de totalen in '
            'rij 11. Beide functies kunnen ook horizontaal.',
            'B15 is dezelfde formule als B13 met één functie anders.',
            'B16 is een deling, een afronding en een getalnotatie. Drie dingen, en de '
            'notatie is er één van.',
        ],
        klaar='Zes rijtotalen, vijf uurtotalen, één totaal van de avond, drie namen en een '
              'percentage.',
        controle='G11 kun je op twee manieren maken: als som van de zes rijtotalen, of als '
                 'som van de vijf uurtotalen. Beide moeten hetzelfde getal geven. Zo niet, '
                 'dan loopt een bereik een rij of een kolom mis.',
    ),
    dict(
        nr=3,
        titel='Wie werkte wanneer',
        blad='3 Ploegen',
        duur='8 minuten',
        doel='Van zestien medewerkers de dienstlengte berekenen uit begin- en einduur, en '
             'met één formule aanduiden wie tot de nachtploeg hoorde.',
        functies=['tijden aftrekken', 'ALS met EN', 'AANTAL.ALS', 'AANTALLEN.ALS',
                  'SOM', 'GEMIDDELDE.ALS', 'MAX', 'INDEX', 'VERGELIJKEN'],
        kaarten=['Rekenen met tijden',
                 'EN en OF binnen ALS',
                 'AANTALLEN.ALS — tellen met meer dan één voorwaarde',
                 'GEMIDDELDE.ALS — het gemiddelde van een deel',
                 'INDEX en VERGELIJKEN — niet de waarde maar de naam'],
        gegeven=[
            ('A4:A19', 'de namen van de zestien medewerkers'),
            ('B4:B19', 'hun rol: gids, techniek, toezicht, onthaal of bar'),
            ('C4:C19', 'de post waar ze stonden'),
            ('D4:D19', 'het uur waarop hun dienst begon'),
            ('E4:E19', 'het uur waarop hun dienst eindigde'),
            ('J3', 'de grens voor de nachtploeg: later gestopt dan dit uur'),
            ('J4', 'en minstens zoveel uur gewerkt'),
        ],
        maken=[
            ('F4:F19', 'het aantal gewerkte uren, als gewoon getal',
             'de twee tijden van elkaar aftrekken'),
            ('G4:G19', 'ja of nee: hoort de medewerker tot de nachtploeg',
             'ALS met EN, met absolute verwijzingen naar J3 en J4'),
            ('B22', 'het aantal gidsen', 'AANTAL.ALS'),
            ('B23', 'het aantal mensen in de nachtploeg', 'AANTAL.ALS'),
            ('B24', 'het aantal technici dat op de schatkamer stond', 'AANTALLEN.ALS'),
            ('B25', 'het totaal aantal gewerkte uren van de hele ploeg', 'SOM'),
            ('B26', 'de gemiddelde dienstlengte van de gidsen', 'GEMIDDELDE.ALS'),
            ('B27', 'de langste dienst, in uren', 'MAX'),
            ('B28', 'de naam van wie het langst werkte', 'INDEX met VERGELIJKEN'),
        ],
        opmaak=[
            'Koptekst in rij 3: vet met achtergrondkleur, gecentreerd.',
            'D4:E19: notatie tijd uu:mm.',
            'F4:F19 en B25:B27: twee cijfers na de komma.',
            'G4:G19: voorwaardelijke opmaak — ja krijgt een kleur.',
            'Grensblok I2:J4: rand eromheen en een lichte vulling.',
        ],
        hints=[
            'Een tijd is voor Excel een deel van een dag. Trek je twee tijden af, dan krijg '
            'je ook een deel van een dag. Er moet dus nog iets gebeuren voor er uren staan.',
            'Geef kolom F de notatie Getal en niet Tijd. Anders probeert Excel 4,5 als een '
            'tijdstip te tonen.',
            'De nachtploeg vraagt twee dingen tegelijk. Één functie binnen een andere dus.',
            'Vergelijk met de cel waarin de grenstijd staat. Een tijd die je zelf tussen '
            'aanhalingstekens typt, is tekst — en tekst is nooit groter dan een tijd.',
            'Eén iemand stopte precies op de grens, en één iemand werkte precies lang '
            'genoeg. Dat staat er met opzet in.',
        ],
        klaar='Zestien dienstlengtes, zestien keer ja of nee, en zeven antwoorden onder de '
              'lijst — waarvan er één een naam is.',
        controle='Tel de ja\'s in kolom G met het oog na. Dat getal moet in B23 staan. Komt '
                 'het niet uit, kijk dan naar wie precies op de grens stopte: hoort die er '
                 'bij of niet, volgens de omschrijving?',
    ),
    dict(
        nr=4,
        titel='Wie nam de Zilveren Pompoen',
        blad='4 Verdachten',
        duur='9 minuten',
        doel='Vijf getuigenverklaringen omzetten in één formule, en zo van acht verdachten '
             'naar precies één naam gaan.',
        functies=['VERT.ZOEKEN (ander werkblad)', 'ALS met EN', 'AANTAL.ALS', 'INDEX',
                  'VERGELIJKEN'],
        kaarten=['Verwijzen naar een ander werkblad',
                 'EN en OF binnen ALS',
                 'INDEX en VERGELIJKEN — niet de waarde maar de naam',
                 'Geneste functies — een functie binnen een functie'],
        verklaringen=[
            ('De portier', 'Na tien uur was er nog personeel binnen. Wie zijn dienst om tien '
                           'uur of vroeger had beëindigd, stond toen al buiten.'),
            ('Het badgesysteem', 'De deur van de schatkamer ging tussen tien en elf enkele '
                                 'keren open. Wie in dat uur geen enkele keer badgde, kan er '
                                 'niet binnen geweest zijn.'),
            ('Een bezoeker', 'Ik zag een zwarte schim de trap afglippen. Zwart, dat weet ik '
                             'zeker — de rest was donker.'),
            ('De poetsvrouw', 'Die pompoen is te groot voor een jaszak. Wie geen tas bij had, '
                              'kreeg hem niet mee.'),
            ('De ploegbaas', 'Van sommigen heeft een collega uitdrukkelijk bevestigd waar ze '
                             'waren. Die vallen af.'),
        ],
        gegeven=[
            ('B2', 'het uur waarna de dief nog aan het werk was'),
            ('B3', 'de kleur van het kostuum dat de bezoeker zag'),
            ('A5:A12', 'de acht verdachten'),
            ('B5:B12', 'het aantal badgescans aan de schatkamer tussen tien en elf'),
            ('C5:C12', 'de kleur van hun kostuum'),
            ('D5:D12', 'of ze een tas bij hadden'),
            ('E5:E12', 'wie hun alibi bevestigde, of "geen"'),
        ],
        maken=[
            ('F5:F12', 'het uur waarop hun dienst eindigde, opgehaald van het ploegenblad',
             'VERT.ZOEKEN naar een ander werkblad'),
            ('G5:G12', 'MOGELIJK of uitgesloten, volgens de vijf verklaringen samen',
             'ALS met EN'),
            ('B14', 'hoeveel verdachten er overblijven', 'AANTAL.ALS'),
            ('B15', 'de naam van de dader', 'INDEX met VERGELIJKEN'),
        ],
        opmaak=[
            'Koptekst in rij 4: vet met achtergrondkleur, gecentreerd.',
            'F5:F12: notatie tijd uu:mm.',
            'G5:G12: voorwaardelijke opmaak — MOGELIJK wordt rood en vet.',
            'B14:B15: rand eromheen, vet.',
        ],
        hints=[
            'Het ploegenblad weet al wanneer ieders dienst eindigde. Typ dat niet over: '
            'haal het op.',
            'Kolom F toont eerst een lang kommagetal. Dat is geen fout in je formule, dat '
            'is een ontbrekende getalnotatie.',
            'Vijf verklaringen, vijf voorwaarden, één EN. Bouw het op: eerst twee '
            'voorwaarden, kijk of het klopt, dan de derde erbij.',
            'Verwijs naar B2 en B3 in plaats van het uur en de kleur in te typen. Dan kun je '
            'achteraf een verklaring aanpassen en meteen zien wat er verandert.',
            'De nachtploeg van blad 3 is NIET de lijst van verdachten. Lees de eerste '
            'verklaring nog eens: die gaat over het einde van de dienst, niet over hoe lang '
            'iemand werkte.',
        ],
        klaar='Acht keer een oordeel in kolom G, en daaronder één aantal en één naam.',
        controle='B14 moet precies 1 geven. Staat er 0, dan is een voorwaarde te streng. '
                 'Staat er meer dan 1, dan is er een verklaring die je nog niet gebruikt.',
    ),
    dict(
        nr=5,
        titel='De avond afrekenen',
        blad='5 Afrekening',
        duur='4 minuten',
        doel='De opbrengst en de kosten van de avond tegenover elkaar zetten, met cijfers die '
             'van blad 1 en blad 3 komen in plaats van overgetypt te zijn.',
        functies=['verwijzing naar een ander werkblad', 'SOM', 'AFRONDEN'],
        kaarten=['Verwijzen naar een ander werkblad',
                 'Geneste functies — een functie binnen een functie'],
        gegeven=[
            ('B5', 'de baromzet van de avond'),
            ('B10', 'het uurloon'),
            ('B12', 'de kosten voor decor en techniek'),
            ('B13', 'de cateringkosten'),
        ],
        maken=[
            ('B4', 'de ticketomzet, van het boekingsblad',
             'verwijzing naar een ander werkblad'),
            ('B6', 'de totale opbrengst', 'SOM'),
            ('B9', 'het totaal aantal gewerkte uren, van het ploegenblad',
             'verwijzing naar een ander werkblad'),
            ('B11', 'de loonkost', 'AFRONDEN'),
            ('B14', 'de totale kosten', 'SOM'),
            ('B17', 'de winst van de avond', 'formule'),
            ('B18', 'de winstmarge', 'AFRONDEN'),
            ('B19', 'de opbrengst per bezoeker',
             'AFRONDEN, met het bezoekersaantal van blad 1'),
        ],
        opmaak=[
            'De drie kopjes Opbrengsten, Kosten en Resultaat: vet in een kleur.',
            'Alle bedragen: notatie valuta.',
            'B18: notatie percentage met één cijfer na de komma.',
            'B9: twee cijfers na de komma. B17: vet, met een rand eromheen.',
        ],
        hints=[
            'Geen enkel getal overtypen. Elk cijfer dat elders al staat, haal je op met een '
            'verwijzing.',
            'De marge is de winst gedeeld door de opbrengst, niet door de kosten.',
            'Voor B19 heb je een cel van blad 1 nodig die je daar al hebt uitgerekend. Die '
            'hoeft hier dus niet opnieuw.',
        ],
        klaar='Een blad waarop geen enkel getal staat dat je zelf hebt ingetypt, behalve de '
              'vier die er al stonden.',
        controle='De echte test: ga naar blad 3 en zet bij één medewerker het einduur een half '
                 'uur later. De winst op dit blad moet meteen dalen. Verandert er niets, dan '
                 'heb je ergens een getal overgetypt in plaats van verwezen. Zet het einduur '
                 'daarna terug.',
    ),
]
