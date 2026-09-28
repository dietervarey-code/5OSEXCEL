# -*- coding: utf-8 -*-
"""De vijf oefeningen, stap voor stap.

Geen geneste functies: elke formule gebruikt hoogstens één functie. Optellen,
aftrekken, vermenigvuldigen en delen zijn geen functies, dus die mogen wel
binnen de haakjes staan.
"""

OEFENINGEN = [
    dict(
        nr=1,
        titel='Voorraadlijst afwerken',
        blad='1 Voorraad',
        duur='10 minuten',
        situatie='Het magazijn heeft twaalf artikelen geteld. Jij zet er de waarde bij en '
                 'maakt er een lijst van die de boekhouding meteen kan gebruiken.',
        functies=['SOM'],
        hulp=['Doorvoeren met de vulgreep', 'Getalnotatie: valuta, percentage en decimalen'],
        stappen=[
            ('Bereken de waarde van de eerste regel.',
             'Klik E4 aan en typ =C4*D4. Dat is het aantal maal de eenheidsprijs. '
             'Druk op Enter.'),
            ('Voer de formule door tot E15.',
             'Klik E4 opnieuw aan, pak het blokje rechtsonder — de vulgreep — en sleep tot E15. '
             'Klik daarna E15 aan en kijk in de formulebalk: er hoort =C15*D15 te staan. '
             'Staat er iets anders, dan is het doorvoeren misgelopen.'),
            ('Tel de totale voorraadwaarde op.',
             'Klik E17 aan en typ =SOM(E4:E15). Let op dat je bereik bij rij 4 begint en bij '
             'rij 15 stopt: neem rij 17 niet mee, want dat is de cel waar je in staat.'),
            ('Tel ook het totale aantal stuks.',
             'Klik C17 aan en typ =SOM(C4:C15). Zo zie je in één oogopslag hoeveel stuks er '
             'in het magazijn liggen, naast wat ze waard zijn.'),
            ('Geef de bedragen de notatie valuta.',
             'Selecteer D4 tot en met D15, hou Ctrl ingedrukt en selecteer er ook E4 tot en met '
             'E17 bij. Kies dan Start › Getal › Valuta. Zo doe je beide kolommen in één keer.'),
            ('Maak de koptekst duidelijk.',
             'Selecteer A3 tot en met E3. Zet ze in het vet, geef ze een achtergrondkleur en '
             'lijn ze gecentreerd uit.'),
            ('Zet de totaalrij apart.',
             'Selecteer B17 tot en met E17 en zet die in het vet. Geef de rij een bovenrand, '
             'zodat het totaal duidelijk losstaat van de lijst erboven.'),
        ],
        klaar='Twaalf regels met een waarde in euro, een totaal aantal stuks en een totale '
              'waarde, een koptekst die opvalt en een totaalrij met een lijn erboven.',
        controle='Klopt E17, dan kloppen de twaalf regels erboven ook. Dat is je snelste controle.',
    ),
    dict(
        nr=2,
        titel='Prijslijst aanpassen',
        blad='2 Prijslijst',
        duur='10 minuten',
        situatie='De leverancier verhoogt zijn prijzen. Jij past de hele lijst aan zonder één '
                 'prijs met de hand te berekenen, en laat zien wat de klant er per artikel '
                 'van merkt.',
        functies=['AFRONDEN'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep'],
        stappen=[
            ('Toon het percentage als percentage.',
             'In B3 staat 0,035. Klik de cel aan en kies Start › Getal › Percentage. '
             'Er staat nu 3,50 %. Het getal zelf verandert niet — kijk maar in de formulebalk.'),
            ('Bereken de eerste nieuwe prijs.',
             'Klik C6 aan en typ =AFRONDEN(B6*(1+$B$3);2). De dollartekens zorgen dat B3 '
             'blijft staan als je straks doorvoert. Zonder die tekens loopt het mis.'),
            ('Voer door tot C15 en controleer.',
             'Sleep de vulgreep van C6 naar beneden. Klik daarna C15 aan en kijk in de '
             'formulebalk: er hoort =AFRONDEN(B15*(1+$B$3);2) te staan. Zie je daar B12 of '
             'een lege verwijzing, dan zijn de dollartekens vergeten.'),
            ('Bereken het verschil in euro.',
             'Klik D6 aan en typ =C6-B6. Voer door tot D15. Zo zie je per artikel hoeveel '
             'duurder het wordt.'),
            ('Bereken het verschil in procent.',
             'Klik E6 aan en typ =D6/B6. Dat is het verschil gedeeld door de oude prijs. '
             'Voer door tot E15 en geef de kolom de notatie percentage.'),
            ('Controleer je werk.',
             'Alle waarden in kolom E moeten rond de 3,5 % liggen. Wijkt er één sterk af, '
             'dan zit er een fout in die rij. Dat is een handige controle: een percentage '
             'dat overal gelijk hoort te zijn, verraadt meteen waar het misloopt.'),
            ('Werk het blad af.',
             'Geef B, C en D de notatie valuta. Zet de koptekst in rij 5 in het vet met een '
             'achtergrondkleur, en zet een rand rond de hele tabel A5:E15.'),
        ],
        klaar='Tien nieuwe prijzen, per artikel het verschil in euro én in procent, '
              'en een tabel met randen en een duidelijke koptekst.',
        controle='Alle percentages in kolom E liggen rond 3,5 %. Eén die eruit springt, '
                 'wijst naar een fout in die rij.',
    ),
    dict(
        nr=3,
        titel='Verkoopcijfers samenvatten',
        blad='3 Verkoop',
        duur='10 minuten',
        situatie='Acht verkopers, drie maanden. De verkoopleider wil morgen geen tabel vol '
                 'cijfers, maar een blad waarop hij in vijf seconden ziet hoe het gegaan is.',
        functies=['SOM', 'MAX', 'MIN', 'GEMIDDELDE', 'AANTAL'],
        hulp=['Doorvoeren met de vulgreep',
              'Getalnotatie: valuta, percentage en decimalen'],
        stappen=[
            ('Bereken het kwartaaltotaal per verkoper.',
             'Klik E4 aan en typ =SOM(B4:D4). Dat telt januari, februari en maart op voor die '
             'ene verkoper. Voer door tot E11.'),
            ('Bereken het totaal per maand.',
             'Klik B13 aan en typ =SOM(B4:B11). Voer die formule nu naar rechts door, '
             'tot en met E13. Sleep daarvoor de vulgreep zijwaarts in plaats van naar beneden.'),
            ('Controleer of je twee totalen kloppen.',
             'In E13 staat nu het eindtotaal. Dat is zowel de som van de kwartaaltotalen als '
             'de som van de maandtotalen. Komen die twee niet overeen, dan mis je ergens een rij '
             'of een kolom in een bereik.'),
            ('Zoek het hoogste kwartaaltotaal.',
             'Klik B16 aan en typ =MAX(E4:E11). Let erop dat je naar kolom E kijkt — de '
             'kwartaaltotalen — en niet naar één maand.'),
            ('Zoek het laagste kwartaaltotaal.',
             'Klik B17 aan en typ =MIN(E4:E11).'),
            ('Bereken het gemiddelde.',
             'Klik B18 aan en typ =GEMIDDELDE(E4:E11). Typ hier niet =SOM(E4:E11)/8: dat werkt '
             'vandaag, maar niet meer zodra er een verkoper bijkomt.'),
            ('Tel hoeveel verkopers er zijn.',
             'Klik B19 aan en typ =AANTAL(E4:E11). Je krijgt 8. Dat getal hoort te kloppen met '
             'het aantal rijen in je tabel — nog een controle.'),
            ('Laat de samenvatting opvallen.',
             'Selecteer A15 tot en met B19 en geef dat blok een achtergrondkleur. Zet A15 in '
             'het vet. Geef de vier getallen in B16 tot B19 de notatie valuta, behalve B19: '
             'dat is een aantal, geen bedrag.'),
            ('Werk de tabel af.',
             'Zet de koptekst in rij 3 in het vet met een achtergrondkleur en centreer ze. '
             'Zet de totaalrij 13 in het vet met een bovenrand.'),
        ],
        klaar='Acht kwartaaltotalen, drie maandtotalen met een eindtotaal, en een gekleurd '
              'blokje met vier samenvattende cijfers.',
        controle='Het eindtotaal in E13 moet langs twee wegen hetzelfde zijn: via de rijen '
                 'en via de kolommen.',
    ),
    dict(
        nr=4,
        titel='Bestellingen beoordelen',
        blad='4 Bestellingen',
        duur='10 minuten',
        situatie='Vanaf een bepaald bedrag is de levering gratis. Jij laat het rekenblad per '
                 'bestelling beslissen, en rekent daarna uit wat die actie het bedrijf kost.',
        functies=['ALS', 'AANTAL.ALS', 'SOM.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Voorwaardelijke opmaak'],
        stappen=[
            ('Zoek eerst op welke grens geldt.',
             'In B3 staat het bedrag vanaf wanneer de levering gratis is. Lees dat af voor je '
             'begint — je gaat ernaar verwijzen in plaats van het getal over te typen.'),
            ('Laat het rekenblad beslissen.',
             'Klik D6 aan en typ =ALS(C6>=$B$3;"Gratis";"Betalend"). Let op de aanhalingstekens '
             'rond de twee woorden, en op >= in plaats van >. De opdracht zegt vanaf, '
             'niet meer dan.'),
            ('Voer door tot D19 en kijk naar twee rijen.',
             'Sleep de vulgreep naar beneden. Zoek dan bestelling B-2104: die staat op 489,90 '
             'en moet Betalend geven. En B-2108 staat op 501,00 en moet Gratis geven. '
             'Daar zie je in de praktijk wat >= betekent.'),
            ('Tel de gratis leveringen.',
             'Klik C21 aan en typ =AANTAL.ALS(D6:D19;"Gratis"). Je telt in kolom D, waar de '
             'woorden staan — niet in kolom C met de bedragen.'),
            ('Tel de betalende leveringen.',
             'Klik C22 aan en typ =AANTAL.ALS(D6:D19;"Betalend"). De twee aantallen samen '
             'moeten veertien zijn, want zoveel bestellingen staan er.'),
            ('Tel op hoeveel omzet gratis geleverd wordt.',
             'Klik C23 aan en typ =SOM.ALS(D6:D19;"Gratis";C6:C19). Lees de volgorde als een '
             'zin: kijk in kolom D, zoek Gratis, tel de bedragen uit kolom C op.'),
            ('Doe hetzelfde voor de betalende leveringen.',
             'Klik C24 aan en typ =SOM.ALS(D6:D19;"Betalend";C6:C19).'),
            ('Controleer je twee bedragen.',
             'Tel C23 en C24 samen op een lege cel: =C23+C24. Dat moet hetzelfde geven als '
             '=SOM(C6:C19), het totaal van alle bestellingen. Klopt dat niet, dan mist er een '
             'rij in een van je bereiken. Wis die hulpcel daarna weer.'),
            ('Kleur de grote bestellingen automatisch.',
             'Selecteer C6 tot en met C19. Kies Start › Voorwaardelijke opmaak › Regels voor '
             'markeren › Groter dan, vul 500 in en kies een groene opvulling.'),
            ('Werk af.',
             'Geef kolom C de notatie valuta, en ook C23 en C24. Zet de koptekst in rij 5 in '
             'het vet met een achtergrondkleur. Zet de vier labels in B21 tot B24 in het vet.'),
        ],
        klaar='Veertien bestellingen met Gratis of Betalend erachter, de grote bedragen groen '
              'gekleurd, en vier antwoorden onderaan die samen kloppen met het totaal.',
        controle='Aantal gratis plus aantal betalend is veertien. Bedrag gratis plus bedrag '
                 'betalend is het totaal van alle bestellingen.',
    ),
    dict(
        nr=5,
        titel='Klantenbestand aanvullen',
        blad='5 Klanten',
        duur='10 minuten',
        situatie='Je krijgt een lijst met alleen klantcodes. De namen en steden staan in de '
                 'zoektabel ernaast. Overtypen mag niet: dat is precies waar het in de praktijk '
                 'misgaat.',
        functies=['VERT.ZOEKEN'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Beeld vastzetten',
              'Doorvoeren met de vulgreep'],
        stappen=[
            ('Bekijk eerst de zoektabel.',
             'Rechts op het blad, in G3 tot en met I13, staat de zoektabel. De codes staan in '
             'kolom G, de namen in H, de steden in I. Binnen die tabel is G kolom 1, H kolom 2 '
             'en I kolom 3. Dat nummer heb je straks nodig.'),
            ('Haal de eerste naam op.',
             'Klik B4 aan en typ =VERT.ZOEKEN(A4;$G$4:$I$13;2;ONWAAR). Het cijfer 2 betekent: '
             'de tweede kolom van de zoektabel. ONWAAR betekent: zoek exact.'),
            ('Voer door tot B15.',
             'Sleep de vulgreep naar beneden. Klik daarna B15 aan en controleer in de '
             'formulebalk of de tabel nog altijd $G$4:$I$13 is. Is ze meegeschoven, dan zijn '
             'de dollartekens vergeten.'),
            ('Haal de steden op.',
             'Klik C4 aan en typ dezelfde formule, maar met 3 in plaats van 2: '
             '=VERT.ZOEKEN(A4;$G$4:$I$13;3;ONWAAR). Voer door tot C15.'),
            ('Zoek de rij die #N/B geeft.',
             'Eén klantcode in de lijst staat niet in de zoektabel. Die geeft #N/B, en dat is '
             'geen fout van jou: het betekent dat de code niet bestaat. Zoek op welke rij dat '
             'is en welke code het betreft.'),
            ('Meld die code apart.',
             'Typ in E4 het woord Onbekend, en zet daarnaast in F4 de code die niet gevonden '
             'werd. Zo weet de collega die dit bestand krijgt meteen wat er nagekeken moet worden.'),
            ('Zet de koppen vast.',
             'Klik A4 aan — de eerste cel ónder wat moet blijven staan — en kies '
             'Beeld › Blokkeren › Titels blokkeren. Scrol naar beneden: de koppen blijven staan.'),
            ('Werk de tabel af.',
             'Zet een rand rond A3 tot en met C15. Zet de koptekst in rij 3 in het vet met een '
             'achtergrondkleur. Controleer of alle kolommen breed genoeg zijn: geen enkele naam '
             'mag afgekapt worden.'),
        ],
        klaar='Twaalf regels met naam en stad ingevuld, één rij met #N/B die je apart gemeld '
              'hebt, vastgezette koppen en een tabel met randen.',
        controle='Precies één rij geeft #N/B. Zijn het er meer, dan zijn de dollartekens '
                 'vergeten of is de zoektabel meegeschoven.',
    ),
]
