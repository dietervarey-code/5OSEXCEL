# -*- coding: utf-8 -*-
"""De vijf oefeningen, stap voor stap. Geen geneste functies: elke formule
   gebruikt hoogstens één functie."""

OEFENINGEN = [
    dict(
        nr=1,
        titel='Voorraadlijst afwerken',
        blad='1 Voorraad',
        duur='10 minuten',
        situatie='Het magazijn heeft geteld. Jij zet er de waarde bij, zodat de boekhouding '
                 'weet wat er in het rek staat.',
        functies=['SOM'],
        hulp=['Doorvoeren met de vulgreep', 'Getalnotatie: valuta en percentage'],
        stappen=[
            ('Bereken de waarde van de eerste regel.',
             'Klik E4 aan en typ =C4*D4. Dat is het aantal maal de eenheidsprijs. '
             'Druk op Enter. Er verschijnt 1131.'),
            ('Voer de formule door tot E11.',
             'Klik E4 opnieuw aan, pak het blokje rechtsonder (de vulgreep) en sleep tot E11. '
             'Controleer daarna E11: daar hoort =C11*D11 te staan.'),
            ('Tel alle waarden op.',
             'Klik E13 aan en typ =SOM(E4:E11). Resultaat: 10204,5.'),
            ('Geef de bedragen de notatie valuta.',
             'Selecteer D4 tot en met D11 en ook E4 tot en met E13. Kies Start › Getal › Valuta. '
             'Je ziet nu € en twee decimalen.'),
            ('Maak de koptekst duidelijk.',
             'Selecteer A3 tot en met E3. Zet ze in het vet en geef ze een achtergrondkleur. '
             'Zet het totaal in E13 ook in het vet.'),
        ],
        klaar='Je blad toont acht bedragen in euro en een totaal van € 10.204,50, '
              'met een koptekst die opvalt.',
    ),
    dict(
        nr=2,
        titel='Prijslijst aanpassen',
        blad='2 Prijslijst',
        duur='10 minuten',
        situatie='De leverancier verhoogt zijn prijzen met 3,5 %. Jij past de hele lijst aan — '
                 'zonder één prijs met de hand te berekenen.',
        functies=['AFRONDEN'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Getalnotatie: valuta en percentage'],
        stappen=[
            ('Toon het percentage als percentage.',
             'In B3 staat 0,035. Klik de cel aan en kies Start › Getal › Percentage. '
             'Er staat nu 3,50 %. Het getal zelf verandert niet.'),
            ('Bereken de eerste nieuwe prijs.',
             'Klik C6 aan en typ =AFRONDEN(B6*(1+$B$3);2). Resultaat: 0,81. '
             'De dollartekens zorgen dat B3 blijft staan als je straks doorvoert.'),
            ('Voer door tot C12.',
             'Sleep de vulgreep van C6 naar beneden. Klik daarna C12 aan en kijk in de '
             'formulebalk: er hoort =AFRONDEN(B12*(1+$B$3);2) te staan. Staat er $B$9 of B9, '
             'dan zijn de dollartekens vergeten.'),
            ('Bereken het verschil.',
             'Klik D6 aan en typ =C6-B6. Voer door tot D12. Zo zie je per artikel hoeveel '
             'duurder het wordt.'),
            ('Werk het blad af.',
             'Geef B, C en D de notatie valuta. Zet de koptekst in rij 5 in het vet met een '
             'achtergrondkleur, en zet een rand rond de tabel.'),
        ],
        klaar='Zeven nieuwe prijzen, van € 0,81 tot € 40,26, met per artikel het verschil ernaast.',
    ),
    dict(
        nr=3,
        titel='Verkoopcijfers samenvatten',
        blad='3 Verkoop',
        duur='10 minuten',
        situatie='De verkoopleider wil morgen op de vergadering geen zes rijen cijfers, '
                 'maar vier getallen die het verhaal vertellen.',
        functies=['SOM', 'MAX', 'MIN', 'GEMIDDELDE', 'AANTAL'],
        hulp=['Doorvoeren met de vulgreep'],
        stappen=[
            ('Bereken het kwartaaltotaal per verkoper.',
             'Klik E4 aan en typ =SOM(B4:D4). Dat telt januari, februari en maart op. '
             'Voer door tot E9.'),
            ('Zoek het hoogste kwartaaltotaal.',
             'Klik B12 aan en typ =MAX(E4:E9). Resultaat: 89050.'),
            ('Zoek het laagste kwartaaltotaal.',
             'Klik B13 aan en typ =MIN(E4:E9). Resultaat: 40750.'),
            ('Bereken het gemiddelde.',
             'Klik B14 aan en typ =GEMIDDELDE(E4:E9). Resultaat: 62325.'),
            ('Tel hoeveel verkopers er zijn.',
             'Klik B15 aan en typ =AANTAL(E4:E9). Resultaat: 6.'),
            ('Laat de samenvatting opvallen.',
             'Selecteer A11 tot en met B15 en geef dat blok een achtergrondkleur. '
             'Zet A11 in het vet. Geef de vier getallen in B12 tot B15 de notatie valuta.'),
        ],
        klaar='Zes kwartaaltotalen, en daaronder een gekleurd blokje met vier samenvattende cijfers.',
    ),
    dict(
        nr=4,
        titel='Bestellingen beoordelen',
        blad='4 Bestellingen',
        duur='10 minuten',
        situatie='Vanaf 500 euro is de levering gratis. Jij laat het rekenblad per bestelling '
                 'beslissen, en telt daarna op wat dat kost.',
        functies=['ALS', 'AANTAL.ALS', 'SOM.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Voorwaardelijke opmaak'],
        stappen=[
            ('Laat het rekenblad beslissen.',
             'Klik D6 aan en typ =ALS(C6>=$B$3;"Gratis";"Betalend"). '
             'Let op de aanhalingstekens rond de woorden, en op >= in plaats van >.'),
            ('Voer door tot D15.',
             'Sleep de vulgreep naar beneden. Kijk naar B-2104: 489,90 euro geeft Betalend. '
             'En naar B-2108: 501,00 euro geeft Gratis. Daar zie je het verschil tussen '
             '>= en > in de praktijk.'),
            ('Tel de gratis leveringen.',
             'Klik C17 aan en typ =AANTAL.ALS(D6:D15;"Gratis"). Resultaat: 6.'),
            ('Tel op hoeveel omzet dat is.',
             'Klik C18 aan en typ =SOM.ALS(D6:D15;"Gratis";C6:C15). Resultaat: 5618,85. '
             'Eerst waar je zoekt, dan wat je zoekt, dan wat je optelt.'),
            ('Kleur de grote bestellingen automatisch.',
             'Selecteer C6 tot en met C15. Kies Start › Voorwaardelijke opmaak › '
             'Regels voor markeren › Groter dan, vul 500 in en kies een groene opvulling.'),
            ('Werk af.',
             'Geef kolom C de notatie valuta. Zet de koptekst in rij 5 in het vet.'),
        ],
        klaar='Tien bestellingen met Gratis of Betalend erachter, zes groen gekleurd, '
              'en twee antwoorden onderaan: 6 en € 5.618,85.',
    ),
    dict(
        nr=5,
        titel='Klantenbestand aanvullen',
        blad='5 Klanten',
        duur='10 minuten',
        situatie='Je krijgt een lijst met alleen klantcodes. De namen en steden staan in de '
                 'zoektabel ernaast. Overtypen mag niet: dat is precies wat fout gaat.',
        functies=['VERT.ZOEKEN'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Beeld vastzetten'],
        stappen=[
            ('Haal de eerste naam op.',
             'Klik B4 aan en typ =VERT.ZOEKEN(A4;$G$4:$I$11;2;ONWAAR). '
             'Resultaat: Dakwerken Lievens. Het cijfer 2 betekent: de tweede kolom van de '
             'zoektabel, dus kolom H.'),
            ('Voer door tot B11.',
             'Sleep de vulgreep naar beneden. Krijg je #N/B, kijk dan of de dollartekens rond '
             '$G$4:$I$11 er nog staan.'),
            ('Haal de steden op.',
             'Klik C4 aan en typ dezelfde formule, maar met 3 in plaats van 2: '
             '=VERT.ZOEKEN(A4;$G$4:$I$11;3;ONWAAR). Voer door tot C11.'),
            ('Zet de koppen vast.',
             'Klik A4 aan en kies Beeld › Blokkeren › Titels blokkeren. '
             'Scrol naar beneden: de koppen blijven staan.'),
            ('Werk de tabel af.',
             'Zet een rand rond A3 tot en met C11. Zet de koptekst in rij 3 in het vet met een '
             'achtergrondkleur. Maak de kolommen breed genoeg zodat geen enkele naam afgekapt wordt.'),
        ],
        klaar='Acht klanten met naam en stad ingevuld, geen enkele #N/B, en een tabel met '
              'randen waarvan de koppen blijven staan.',
    ),
]
