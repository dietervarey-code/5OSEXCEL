# -*- coding: utf-8 -*-
"""De inhoud van de functiefiches.

Elke fiche moet op zichzelf staan: een leerling die vastloopt, pakt de fiche
en kan verder zonder iets anders te raadplegen. Daarom staat bij elke functie
niet alleen de schrijfwijze, maar ook een voorbeeld met de cijfers uit de
oefening zelf, plus de fout die het vaakst gemaakt wordt.
"""

# (titel, ondertitel, [(kop, [regels])], voorbeeldblok, fout)
FUNCTIES = [
    dict(
        naam='SOM',
        wat='Telt getallen bij elkaar op.',
        gebruik='oefening 1 en 3',
        schrijf='=SOM(bereik)',
        argumenten=[
            ('bereik', 'de cellen die je wil optellen, bijvoorbeeld D4:D11'),
        ],
        voorbeeld=[
            'In D4 tot en met D11 staan acht bedragen.',
            'In D13 typ je:',
            '=SOM(D4:D11)',
            'Resultaat: 10204,50 — het totaal van die acht bedragen.',
        ],
        weten=[
            'De dubbele punt betekent tot en met. D4:D11 zijn acht cellen.',
            'Een puntkomma betekent en ook. =SOM(D4;D11) telt maar twee cellen op.',
            'Je mag ze combineren: =SOM(D4:D11;F4:F11) telt twee blokken samen.',
            'SOM slaat lege cellen en tekst over. Staat er ergens "ziek", dan stoort dat niet.',
        ],
        fout='Het totaal meetellen in je eigen bereik: =SOM(D4:D13) terwijl D13 het totaal zelf is. '
             'Excel meldt dan een kringverwijzing.',
    ),
    dict(
        naam='AFRONDEN',
        wat='Rondt een getal af op een aantal cijfers na de komma.',
        gebruik='oefening 2',
        schrijf='=AFRONDEN(getal;aantal_decimalen)',
        argumenten=[
            ('getal', 'het getal of de berekening die je wil afronden'),
            ('aantal_decimalen', 'hoeveel cijfers na de komma je overhoudt; 2 voor euro'),
        ],
        voorbeeld=[
            'In B6 staat 0,78. Je wil die prijs met 3,5 % verhogen en afronden op cent.',
            'In C6 typ je:',
            '=AFRONDEN(B6*(1+$B$3);2)',
            'Resultaat: 0,81.',
        ],
        weten=[
            'Afronden verandert het getal zelf. Een getalnotatie verandert alleen hoe het eruitziet.',
            'Bij een prijs wil je echt afronden: anders reken je verder met 0,8073.',
            'Halve eenheden gaan naar boven: 0,805 wordt 0,81.',
            'Met 0 als tweede argument rond je af op hele getallen.',
        ],
        fout='Het tweede argument vergeten: =AFRONDEN(B6*1,035) geeft een foutmelding. '
             'AFRONDEN heeft altijd twee argumenten.',
    ),
    dict(
        naam='MAX',
        wat='Geeft het grootste getal uit een reeks.',
        gebruik='oefening 3',
        schrijf='=MAX(bereik)',
        argumenten=[
            ('bereik', 'de cellen waaruit je het grootste getal wil'),
        ],
        voorbeeld=[
            'In E4 tot en met E9 staan zes kwartaaltotalen.',
            'In B12 typ je:',
            '=MAX(E4:E9)',
            'Resultaat: 89050 — het hoogste kwartaaltotaal.',
        ],
        weten=[
            'MAX geeft het getal zelf, niet de naam van wie het haalde.',
            'Tekst en lege cellen worden overgeslagen.',
            'Staan er alleen negatieve getallen, dan geeft MAX het getal dat het dichtst bij nul ligt.',
        ],
        fout='Het bereik van de verkeerde kolom nemen. Je wil het hoogste kwartaaltotaal (kolom E), '
             'niet de hoogste maandomzet (kolom B, C of D).',
    ),
    dict(
        naam='MIN',
        wat='Geeft het kleinste getal uit een reeks.',
        gebruik='oefening 3',
        schrijf='=MIN(bereik)',
        argumenten=[
            ('bereik', 'de cellen waaruit je het kleinste getal wil'),
        ],
        voorbeeld=[
            'In E4 tot en met E9 staan zes kwartaaltotalen.',
            'In B13 typ je:',
            '=MIN(E4:E9)',
            'Resultaat: 40750 — het laagste kwartaaltotaal.',
        ],
        weten=[
            'MIN werkt precies zoals MAX, maar dan de andere kant op.',
            'Lege cellen tellen niet mee als nul: ze worden gewoon overgeslagen.',
            'Een cel met het getal 0 telt wél mee, en wordt dan je minimum.',
        ],
        fout='Denken dat een lege cel het minimum wordt. Dat gebeurt niet — maar een cel '
             'waarin echt 0 staat, wel.',
    ),
    dict(
        naam='GEMIDDELDE',
        wat='Berekent het gemiddelde: de som gedeeld door het aantal.',
        gebruik='oefening 3',
        schrijf='=GEMIDDELDE(bereik)',
        argumenten=[
            ('bereik', 'de cellen waarvan je het gemiddelde wil'),
        ],
        voorbeeld=[
            'In E4 tot en met E9 staan zes kwartaaltotalen.',
            'In B14 typ je:',
            '=GEMIDDELDE(E4:E9)',
            'Resultaat: 62325 — het gemiddelde kwartaaltotaal.',
        ],
        weten=[
            'Lege cellen tellen niet mee in de deling. Zes cellen waarvan één leeg is, '
            'deelt Excel door vijf.',
            'Een cel met 0 telt wél mee en trekt je gemiddelde naar beneden.',
            'Dat is precies het verschil tussen "niets ingevuld" en "nul verkocht".',
        ],
        fout='=SOM(E4:E9)/6 typen in plaats van GEMIDDELDE. Dat werkt, tot er een verkoper '
             'bijkomt en je die 6 vergeet aan te passen.',
    ),
    dict(
        naam='AANTAL',
        wat='Telt hoeveel cellen een getal bevatten.',
        gebruik='oefening 3',
        schrijf='=AANTAL(bereik)',
        argumenten=[
            ('bereik', 'de cellen die je wil tellen'),
        ],
        voorbeeld=[
            'In E4 tot en met E9 staan zes kwartaaltotalen.',
            'In B15 typ je:',
            '=AANTAL(E4:E9)',
            'Resultaat: 6 — er staan zes getallen.',
        ],
        weten=[
            'AANTAL telt alleen getallen. Tekst en lege cellen worden niet meegeteld.',
            'Wil je ook tekst meetellen, gebruik dan AANTALARG.',
            'Voorbeeld: staat er in een cel "ziek", dan telt AANTAL die niet mee, AANTALARG wel.',
        ],
        fout='AANTAL gebruiken om namen te tellen. Namen zijn tekst, dus je krijgt 0. '
             'Gebruik daarvoor AANTALARG.',
    ),
    dict(
        naam='ALS',
        wat='Laat het rekenblad kiezen tussen twee uitkomsten.',
        gebruik='oefening 4',
        schrijf='=ALS(voorwaarde;dan;anders)',
        argumenten=[
            ('voorwaarde', 'een vergelijking die waar of onwaar is, bijvoorbeeld C6>=500'),
            ('dan', 'wat er in de cel komt als de voorwaarde klopt'),
            ('anders', 'wat er in de cel komt als ze niet klopt'),
        ],
        voorbeeld=[
            'In C6 staat 842,50. In B3 staat de grens 500.',
            'In D6 typ je:',
            '=ALS(C6>=$B$3;"Gratis";"Betalend")',
            'Resultaat: Gratis, want 842,50 is groter dan 500.',
        ],
        weten=[
            'Tekst zet je altijd tussen aanhalingstekens: "Gratis", niet Gratis.',
            'Getallen niet: 500 schrijf je zonder aanhalingstekens.',
            'De vergelijkingstekens: > groter dan, < kleiner dan, >= groter dan of gelijk aan, '
            '<= kleiner dan of gelijk aan, = gelijk aan, <> niet gelijk aan.',
            'Let op het verschil tussen > en >=. Bij een bedrag van precies 500 geeft >= '
            'Gratis, en > geeft Betalend.',
        ],
        fout='De aanhalingstekens vergeten: =ALS(C6>=500;Gratis;Betalend) geeft #NAAM?. '
             'Excel zoekt dan naar een functie die Gratis heet.',
    ),
    dict(
        naam='AANTAL.ALS',
        wat='Telt hoeveel cellen aan één voorwaarde voldoen.',
        gebruik='oefening 4',
        schrijf='=AANTAL.ALS(bereik;voorwaarde)',
        argumenten=[
            ('bereik', 'waar je in zoekt, bijvoorbeeld D6:D15'),
            ('voorwaarde', 'waarop je telt, bijvoorbeeld "Gratis"'),
        ],
        voorbeeld=[
            'In D6 tot en met D15 staat per bestelling Gratis of Betalend.',
            'In C17 typ je:',
            '=AANTAL.ALS(D6:D15;"Gratis")',
            'Resultaat: 6 — er zijn zes gratis leveringen.',
        ],
        weten=[
            'De punt in de naam hoort erbij: AANTAL.ALS, niet AANTALALS.',
            'Tekst als voorwaarde zet je tussen aanhalingstekens.',
            'Je mag ook op een getal tellen: =AANTAL.ALS(C6:C15;">500") telt alle bedragen '
            'boven 500. Zo\'n vergelijking staat helemaal tussen aanhalingstekens.',
            'Hoofdletters maken niet uit: "gratis" en "Gratis" tellen allebei mee.',
        ],
        fout='Het verkeerde bereik nemen. Je telt in de kolom waar Gratis staat (D), '
             'niet in de kolom met de bedragen (C).',
    ),
    dict(
        naam='SOM.ALS',
        wat='Telt bedragen op, maar alleen die aan een voorwaarde voldoen.',
        gebruik='oefening 4',
        schrijf='=SOM.ALS(zoekbereik;voorwaarde;optelbereik)',
        argumenten=[
            ('zoekbereik', 'waar je de voorwaarde toetst, bijvoorbeeld D6:D15'),
            ('voorwaarde', 'waarop je selecteert, bijvoorbeeld "Gratis"'),
            ('optelbereik', 'welke cellen je optelt als het klopt, bijvoorbeeld C6:C15'),
        ],
        voorbeeld=[
            'In D6 tot en met D15 staat Gratis of Betalend. In C6 tot en met C15 staan de bedragen.',
            'In C18 typ je:',
            '=SOM.ALS(D6:D15;"Gratis";C6:C15)',
            'Resultaat: 5618,85 — de som van de zes gratis leveringen.',
        ],
        weten=[
            'Let op de volgorde: eerst waar je zoekt, dan wat je zoekt, dan wat je optelt.',
            'De twee bereiken moeten even groot zijn en op dezelfde rijen liggen.',
            'Laat je het derde argument weg, dan telt Excel het zoekbereik zelf op.',
        ],
        fout='Het zoekbereik en het optelbereik omwisselen: =SOM.ALS(C6:C15;"Gratis";D6:D15). '
             'Je krijgt dan 0, want in kolom C staat nergens het woord Gratis.',
    ),
    dict(
        naam='VERT.ZOEKEN',
        wat='Zoekt een waarde op in een tabel en haalt er een gegeven uit dezelfde rij bij.',
        gebruik='oefening 5',
        schrijf='=VERT.ZOEKEN(zoekwaarde;tabel;kolomnummer;ONWAAR)',
        argumenten=[
            ('zoekwaarde', 'wat je zoekt, bijvoorbeeld de klantcode in A4'),
            ('tabel', 'het hele zoekblok, met de code in de eerste kolom: $G$4:$I$11'),
            ('kolomnummer', 'de hoeveelste kolom van dat blok je wil, geteld vanaf links'),
            ('ONWAAR', 'zoek exact; met WAAR neemt Excel de dichtstbijzijnde waarde'),
        ],
        voorbeeld=[
            'In A4 staat K-104. De zoektabel staat in G4 tot en met I11.',
            'In B4 typ je:',
            '=VERT.ZOEKEN(A4;$G$4:$I$11;2;ONWAAR)',
            'Resultaat: Dakwerken Lievens — kolom 2 van het zoekblok.',
            'Voor de stad gebruik je dezelfde formule met kolomnummer 3.',
        ],
        weten=[
            'De zoekkolom moet de EERSTE kolom van je tabel zijn. Hier is dat G, met de codes.',
            'Het kolomnummer telt binnen je tabel, niet in het werkblad. G is 1, H is 2, I is 3.',
            'Zet dollartekens rond de tabel: $G$4:$I$11. Anders schuift ze mee als je doorvoert.',
            'Neem altijd ONWAAR als laatste argument. Met WAAR krijg je stilzwijgend de '
            'verkeerde klant als de code niet bestaat.',
        ],
        fout='De dollartekens vergeten. De eerste rij klopt dan, maar bij het doorvoeren schuift '
             'de tabel mee en krijg je #N/B. Zie ook de fiche over absolute celverwijzing.',
    ),
]

# --------------------------------------------------------------------------
# Geen functies, maar wel nodig om de oefeningen af te werken.
HULP = [
    dict(
        naam='Absolute celverwijzing: de dollartekens',
        wat='Zorgt dat een verwijzing blijft staan als je een formule doorvoert.',
        gebruik='oefening 2, 4 en 5',
        schrijf='$B$3',
        argumenten=[],
        voorbeeld=[
            'Het percentage staat één keer, in B3. Elke rij moet ernaar verwijzen.',
            'In C6 typ je:',
            '=AFRONDEN(B6*(1+$B$3);2)',
            'Voer je die door naar C7, dan wordt B6 vanzelf B7 — dat wil je.',
            'Maar $B$3 blijft $B$3 — en dat wil je ook.',
        ],
        weten=[
            'Zonder dollartekens schuift een verwijzing mee naar beneden: B3 wordt B4, dan B5.',
            'Die cellen zijn leeg, dus je berekening klopt niet meer.',
            'Sneltoets: zet je cursor op de verwijzing in de formule en druk op F4.',
            'F4 blijft wisselen: B3 wordt $B$3, dan B$3, dan $B3, dan weer B3.',
            'Voor deze oefeningen heb je altijd de volledige vorm nodig: $B$3.',
        ],
        fout='Eén rij controleren en dan doorvoeren. De eerste rij klopt bijna altijd; '
             'het gaat mis vanaf de tweede. Controleer dus altijd rij twee.',
    ),
    dict(
        naam='Getalnotatie: valuta en percentage',
        wat='Verandert hoe een getal eruitziet, zonder het getal zelf aan te passen.',
        gebruik='oefening 1, 2 en 4',
        schrijf='Start › Getal',
        argumenten=[],
        voorbeeld=[
            'In de cel staat 1131.',
            'Je selecteert de cel en kiest de notatie Valuta.',
            'Op het scherm staat nu € 1.131,00.',
            'In de formulebalk staat nog altijd gewoon 1131.',
        ],
        weten=[
            'Een cel heeft een inhoud en een weergave. De notatie verandert alleen de weergave.',
            'Je rekent altijd verder met de volledige inhoud, ook met de cijfers die je niet ziet.',
            'Wil je het getal echt veranderen, gebruik dan AFRONDEN.',
            'Percentage: 0,035 met de notatie percentage toont 3,50 %. Het getal blijft 0,035.',
            'Typ je zelf 3,5 % in een cel, dan zet Excel daar 0,035 achter de schermen van.',
            'Met de knoppen voor meer of minder decimalen kies je hoeveel cijfers je toont.',
        ],
        fout='Denken dat ### een fout is. De kolom is gewoon te smal. Sleep de rand tussen '
             'de kolomletters breder, of dubbelklik erop.',
    ),
    dict(
        naam='Doorvoeren met de vulgreep',
        wat='Kopieert een formule naar de cellen eronder, met aangepaste verwijzingen.',
        gebruik='alle oefeningen',
        schrijf='het blokje rechtsonder in de cel',
        argumenten=[],
        voorbeeld=[
            'In E4 staat =C4*D4.',
            'Klik E4 aan. Rechtsonder in de cel zie je een klein vierkantje: de vulgreep.',
            'Sleep dat naar beneden tot E11.',
            'In E5 staat nu =C5*D5, in E6 staat =C6*D6, enzovoort.',
        ],
        weten=[
            'De rijnummers schuiven vanzelf mee. Dat heet een relatieve celverwijzing.',
            'Wil je dat iets níét meeschuift, gebruik dan dollartekens.',
            'Dubbelklikken op de vulgreep vult ineens door tot het einde van de tabel ernaast.',
            'Na het doorvoeren: klik een cel onderaan aan en kijk in de formulebalk of ze klopt.',
        ],
        fout='Het resultaat kopiëren in plaats van de formule, door de cel over te typen. '
             'Verandert er dan iets aan de brongegevens, dan klopt jouw cel niet meer.',
    ),
    dict(
        naam='Voorwaardelijke opmaak',
        wat='Geeft cellen automatisch een kleur op basis van wat erin staat.',
        gebruik='oefening 4',
        schrijf='Start › Voorwaardelijke opmaak',
        argumenten=[],
        voorbeeld=[
            'Je wil elke bestelling boven 500 euro groen zien.',
            'Selecteer C6 tot en met C15.',
            'Kies Start › Voorwaardelijke opmaak › Regels voor markeren › Groter dan.',
            'Vul 500 in en kies een groene opvulling.',
        ],
        weten=[
            'De kleur hangt aan de regel, niet aan de cel. Verandert het bedrag, dan verandert '
            'de kleur mee.',
            'Dat is het verschil met een cel met de hand inkleuren: die blijft gekleurd.',
            'Via Regels beheren vind je later terug welke regels er op een blad staan.',
            'Hou het beperkt. Twee of drie regels helpen; tien maken er een kermis van.',
        ],
        fout='De cellen met de hand inkleuren omdat dat sneller lijkt. Bij de volgende '
             'bestelling klopt je kleur niet meer.',
    ),
    dict(
        naam='Beeld vastzetten',
        wat='Houdt de koprij in beeld terwijl je door een lange lijst scrolt.',
        gebruik='oefening 5',
        schrijf='Beeld › Blokkeren',
        argumenten=[],
        voorbeeld=[
            'De koppen staan in rij 3. Je wil dat rij 1 tot 3 blijven staan.',
            'Klik cel A4 aan — de eerste cel ONDER wat moet blijven staan.',
            'Kies Beeld › Blokkeren › Titels blokkeren.',
            'Scrol je nu naar beneden, dan blijven de koppen in beeld.',
        ],
        weten=[
            'Excel bevriest altijd alles bóven en links van de cel die je aanklikt.',
            'Klik je B4 aan, dan blijft ook kolom A staan.',
            'Er verschijnt een dun lijntje waar de grens ligt.',
            'Ongedaan maken: Beeld › Blokkeren › Blokkering titels opheffen.',
        ],
        fout='De koprij zelf aanklikken. Klik je rij 3 aan, dan blijft alleen rij 1 en 2 staan '
             'en scrolt je koprij toch weg. Klik de rij eronder aan.',
    ),
]
