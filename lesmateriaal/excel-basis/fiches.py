# -*- coding: utf-8 -*-
"""De functiefiches.

Twee regels waar niet van afgeweken wordt:

1. Een fiche leert de functie gebruiken. Ze geeft NOOIT de oplossing van een
   oefening. De voorbeelden spelen daarom in een eigen wereldje — punten van
   een toets, temperaturen, uitgaven van een klasuitstap — met andere cellen
   en andere cijfers dan in het startbestand.
2. Een fiche staat op zichzelf. Wie vastloopt, pakt de fiche en kan verder
   zonder iets anders te raadplegen.

Elke fiche heeft een of twee schermbeelden. Die worden getekend door
schermbeeld.py; de opbouw staat hieronder bij 'beelden'.
"""

# --------------------------------------------------------------------------
#  De voorbeeldwereldjes. Bewust ver van de oefeningen.
# --------------------------------------------------------------------------

PUNTEN = [
    ['Leerling', 'Punten'],
    ['Amir', 14],
    ['Bo', 17],
    ['Cis', 11],
    ['Dina', 19],
    ['Emir', 15],
]

TEMPERATUUR = [
    ['Dag', 'Graden'],
    ['maandag', 12],
    ['dinsdag', 15],
    ['woensdag', 9],
    ['donderdag', 17],
    ['vrijdag', 14],
]

UITGAVEN = [
    ['Datum', 'Soort', 'Bedrag'],
    ['02/09', 'Drank', 12.5],
    ['03/09', 'Eten', 28],
    ['05/09', 'Drank', 9.75],
    ['06/09', 'Vervoer', 45],
    ['09/09', 'Eten', 31.2],
]

CODES = [
    ['Code', 'Artikel', 'Prijs'],
    ['A01', 'Balpen', 1.2],
    ['A02', 'Schrift', 2.5],
    ['A03', 'Gum', 0.8],
    ['A04', 'Lat', 1.75],
]

KOL_AB = [('A', 110), ('B', 80)]
KOL_ABC = [('A', 80), ('B', 90), ('C', 85)]


# --------------------------------------------------------------------------
#  De functiefiches
# --------------------------------------------------------------------------
FUNCTIES = [
    dict(
        naam='SOM',
        wat='Telt getallen bij elkaar op.',
        schrijf='=SOM(bereik)',
        argumenten=[
            ('bereik', 'de cellen die je wil optellen, bijvoorbeeld B2:B6'),
        ],
        uitleg=[
            'Stel dat in B2 tot en met B6 vijf punten staan. Je wil het totaal in B7.',
            'Je klikt B7 aan en typt de formule. Excel telt op zodra je op Enter drukt.',
        ],
        beelden=[
            dict(bestand='som-1',
                 onderschrift='In B7 staat de formule. In de cel zie je het resultaat, '
                              'in de formulebalk bovenaan zie je hoe hij gemaakt is.',
                 kolommen=KOL_AB,
                 rijen=PUNTEN + [['Totaal', 76]],
                 formule='=SOM(B2:B6)', geselecteerd='B7', rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=SOM(B2:B6)', 'telt vijf cellen op: alles van B2 tot en met B6'),
            ('=SOM(B2;B6)', 'telt maar twee cellen op: alleen B2 en B6'),
            ('=SOM(B2:B6;D2:D6)', 'telt twee blokken samen op'),
        ],
        weten=[
            'De dubbele punt betekent tot en met. B2:B6 zijn vijf cellen.',
            'De puntkomma betekent en ook. Zo tel je losse cellen of losse blokken samen.',
            'SOM slaat lege cellen en tekst over. Staat er ergens een woord, dan stoort dat niet.',
            'Laat je bereik doorlopen tot de laatste rij met gegevens. Vergeet je de laatste '
            'rij, dan klopt je totaal niet en zegt Excel daar niets over.',
        ],
        fout='Het totaal in je eigen bereik meetellen. Staat het totaal in B7 en typ je '
             '=SOM(B2:B7), dan verwijst de cel naar zichzelf. Excel meldt een kringverwijzing.',
        zelf='Zet vijf getallen onder elkaar in een leeg blad en tel ze op met SOM. '
             'Verander daarna één getal: het totaal past zich vanzelf aan.',
    ),
    dict(
        naam='AFRONDEN',
        wat='Rondt een getal af op een aantal cijfers na de komma.',
        schrijf='=AFRONDEN(getal;aantal_decimalen)',
        argumenten=[
            ('getal', 'het getal of de berekening die je wil afronden'),
            ('aantal_decimalen', 'hoeveel cijfers na de komma je overhoudt'),
        ],
        uitleg=[
            'Een berekening geeft zelden een rond getal. 12,3456 euro bestaat niet: '
            'je wil 12,35.',
            'AFRONDEN maakt het getal zelf korter. Dat is iets anders dan een getalnotatie, '
            'die alleen verandert hoe het eruitziet.',
        ],
        beelden=[
            dict(bestand='afronden-1',
                 onderschrift='In B2 staat een lang getal. In B3 staat datzelfde getal, '
                              'afgerond op twee cijfers na de komma.',
                 kolommen=KOL_AB,
                 rijen=[['Berekening', 'Waarde'],
                        ['ruw', '12,3456'],
                        ['afgerond', '12,35']],
                 formule='=AFRONDEN(B2;2)', geselecteerd='B3', rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=AFRONDEN(12,3456;2)', 'geeft 12,35 — twee cijfers na de komma'),
            ('=AFRONDEN(12,3456;1)', 'geeft 12,3 — één cijfer na de komma'),
            ('=AFRONDEN(12,3456;0)', 'geeft 12 — een heel getal'),
            ('=AFRONDEN(B2*1,21;2)', 'rondt eerst de berekening af, dan pas het resultaat'),
        ],
        weten=[
            'Halve eenheden gaan naar boven: 0,125 wordt met twee decimalen 0,13.',
            'Bij bedragen rond je altijd af op 2. Anders reken je verder met cijfers die '
            'op geen enkele factuur passen.',
            'Het verschil met een getalnotatie: de notatie toont 12,35 maar rekent verder '
            'met 12,3456. AFRONDEN maakt er echt 12,35 van.',
            'De berekening mag binnen de haakjes staan. Dat is geen geneste functie: '
            'vermenigvuldigen en optellen zijn geen functies.',
        ],
        fout='Het tweede argument vergeten. =AFRONDEN(B2) werkt niet — AFRONDEN heeft er '
             'altijd twee nodig. Excel geeft dan een melding dat er te weinig argumenten zijn.',
        zelf='Typ in een lege cel =AFRONDEN(3,14159;2) en daarna =AFRONDEN(3,14159;0). '
             'Kijk wat er verandert.',
    ),
    dict(
        naam='MAX',
        wat='Geeft het grootste getal uit een reeks.',
        schrijf='=MAX(bereik)',
        argumenten=[
            ('bereik', 'de cellen waaruit je het grootste getal wil'),
        ],
        uitleg=[
            'Je hebt een kolom met cijfers en je wil weten wat de hoogste is. '
            'MAX zoekt dat voor je, ook als de lijst honderd rijen lang is.',
        ],
        beelden=[
            dict(bestand='max-1',
                 onderschrift='MAX kijkt naar B2 tot B6 en geeft het grootste getal: 17.',
                 kolommen=KOL_AB,
                 rijen=TEMPERATUUR + [['Warmste', 17]],
                 formule='=MAX(B2:B6)', geselecteerd='B7', rechts=('B',), vet_rij=1,
                 gemarkeerd=('B5',)),
        ],
        varianten=[
            ('=MAX(B2:B6)', 'het grootste getal uit die vijf cellen'),
            ('=MAX(B2:B6;D2:D6)', 'het grootste getal uit twee blokken samen'),
        ],
        weten=[
            'MAX geeft het getal, niet de naam of de dag die erbij hoort.',
            'Tekst en lege cellen worden overgeslagen.',
            'Staan er alleen negatieve getallen, dan geeft MAX het getal dat het dichtst '
            'bij nul ligt. Dat is ook het grootste.',
            'MIN werkt precies hetzelfde, maar dan de andere kant op.',
        ],
        fout='Het bereik van de verkeerde kolom nemen. Controleer altijd of je MAX naar de '
             'kolom kijkt waar de getallen staan die je bedoelt.',
        zelf='Zet vijf getallen onder elkaar en zoek het grootste met MAX. Verander daarna '
             'het grootste getal in iets kleiners: het antwoord springt mee.',
    ),
    dict(
        naam='MIN',
        wat='Geeft het kleinste getal uit een reeks.',
        schrijf='=MIN(bereik)',
        argumenten=[
            ('bereik', 'de cellen waaruit je het kleinste getal wil'),
        ],
        uitleg=[
            'MIN is de tegenhanger van MAX. Alles wat je over MAX weet, geldt hier ook.',
        ],
        beelden=[
            dict(bestand='min-1',
                 onderschrift='MIN kijkt naar dezelfde cellen en geeft het kleinste getal: 9.',
                 kolommen=KOL_AB,
                 rijen=TEMPERATUUR + [['Koudste', 9]],
                 formule='=MIN(B2:B6)', geselecteerd='B7', rechts=('B',), vet_rij=1,
                 gemarkeerd=('B4',)),
        ],
        varianten=[
            ('=MIN(B2:B6)', 'het kleinste getal uit die vijf cellen'),
        ],
        weten=[
            'Een lege cel telt niet mee. MIN wordt dus geen 0 omdat er ergens niets staat.',
            'Een cel waar echt 0 in staat, telt wél mee — en wordt dan je minimum.',
            'Dat is het verschil tussen niets ingevuld en nul verkocht.',
        ],
        fout='Denken dat lege cellen je antwoord naar 0 trekken. Dat gebeurt niet. '
             'Zie je toch onverwacht 0, kijk dan of er ergens een echte 0 staat.',
        zelf='Zet vijf getallen neer, zoek het kleinste met MIN, en maak daarna één cel leeg. '
             'Het antwoord verandert niet naar 0.',
    ),
    dict(
        naam='GEMIDDELDE',
        wat='Berekent het gemiddelde: de som gedeeld door het aantal.',
        schrijf='=GEMIDDELDE(bereik)',
        argumenten=[
            ('bereik', 'de cellen waarvan je het gemiddelde wil'),
        ],
        uitleg=[
            'Het gemiddelde is het totaal gedeeld door hoeveel getallen er zijn. '
            'GEMIDDELDE doet die twee bewerkingen in één keer.',
            'Je zou ook =SOM(B2:B6)/5 kunnen typen. Dat werkt, tot er een rij bijkomt en '
            'je die 5 vergeet aan te passen.',
        ],
        beelden=[
            dict(bestand='gemiddelde-1',
                 onderschrift='Vijf punten samen 76, gedeeld door 5: het gemiddelde is 15,2.',
                 kolommen=KOL_AB,
                 rijen=PUNTEN + [['Gemiddelde', '15,2']],
                 formule='=GEMIDDELDE(B2:B6)', geselecteerd='B7', rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=GEMIDDELDE(B2:B6)', 'het gemiddelde van vijf cellen'),
        ],
        weten=[
            'Lege cellen tellen niet mee in de deling. Vijf cellen waarvan één leeg is, '
            'deelt Excel door vier.',
            'Een cel met 0 telt wél mee en trekt het gemiddelde naar beneden.',
            'Denk daarover na voor je begint: is een lege cel hier hetzelfde als een nul, '
            'of niet? Het antwoord verschilt.',
        ],
        fout='Zelf delen door een vast getal. =SOM(B2:B6)/5 klopt vandaag en morgen niet meer.',
        zelf='Bereken het gemiddelde van vijf getallen. Maak daarna één cel leeg en kijk wat '
             'er met het antwoord gebeurt. Zet er dan 0 in en kijk opnieuw.',
    ),
    dict(
        naam='AANTAL',
        wat='Telt hoeveel cellen een getal bevatten.',
        schrijf='=AANTAL(bereik)',
        argumenten=[
            ('bereik', 'de cellen die je wil tellen'),
        ],
        uitleg=[
            'AANTAL telt niet op, maar telt hoeveel. En het telt alleen getallen.',
            'Wil je ook tekst meetellen, gebruik dan AANTALARG. Dat is het verschil tussen '
            'de twee, en het is het enige verschil.',
        ],
        beelden=[
            dict(bestand='aantal-1',
                 onderschrift='In B4 staat het woord ziek, geen getal. AANTAL telt er daarom '
                              'vier; AANTALARG zou er vijf tellen.',
                 kolommen=KOL_AB,
                 rijen=[['Leerling', 'Punten'],
                        ['Amir', 14],
                        ['Bo', 17],
                        ['Cis', 'ziek'],
                        ['Dina', 19],
                        ['Emir', 15],
                        ['Aantal cijfers', 4]],
                 formule='=AANTAL(B2:B6)', geselecteerd='B7', rechts=('B',), vet_rij=1,
                 gemarkeerd=('B4',)),
        ],
        varianten=[
            ('=AANTAL(B2:B6)', 'telt de cellen met een getal: 4'),
            ('=AANTALARG(B2:B6)', 'telt alle gevulde cellen, ook tekst: 5'),
        ],
        weten=[
            'AANTAL telt alleen getallen. Namen, woorden en lege cellen tellen niet mee.',
            'AANTALARG telt alles wat niet leeg is.',
            'Gebruik AANTAL als je wil weten hoeveel er een cijfer hebben, en AANTALARG '
            'als je wil weten hoeveel er iets ingevuld hebben.',
        ],
        fout='AANTAL gebruiken om namen te tellen. Namen zijn tekst, dus je krijgt 0. '
             'Daarvoor heb je AANTALARG nodig.',
        zelf='Zet vier getallen en één woord onder elkaar. Tel ze met AANTAL en daarna met '
             'AANTALARG. Het verschil is precies dat ene woord.',
    ),
    dict(
        naam='ALS',
        wat='Laat het rekenblad kiezen tussen twee uitkomsten.',
        schrijf='=ALS(voorwaarde;dan;anders)',
        argumenten=[
            ('voorwaarde', 'een vergelijking die waar of onwaar is, bijvoorbeeld B2>=10'),
            ('dan', 'wat er in de cel komt als de voorwaarde klopt'),
            ('anders', 'wat er in de cel komt als ze niet klopt'),
        ],
        uitleg=[
            'ALS stelt een vraag en kiest daarna zelf. Je schrijft de vraag één keer, '
            'en voert ze door over de hele lijst.',
            'Lees de formule als een zin: ALS dit waar is, zet er dan dit; anders dat.',
        ],
        beelden=[
            dict(bestand='als-1',
                 onderschrift='Van 10 op 20 ben je geslaagd. In C2 staat de vraag, en die is '
                              'doorgevoerd tot C6. Cis haalt 11 en is dus geslaagd.',
                 kolommen=KOL_ABC,
                 rijen=[['Leerling', 'Punten', 'Resultaat'],
                        ['Amir', 14, 'geslaagd'],
                        ['Bo', 17, 'geslaagd'],
                        ['Cis', 8, 'niet geslaagd'],
                        ['Dina', 19, 'geslaagd'],
                        ['Emir', 9, 'niet geslaagd']],
                 formule='=ALS(B2>=10;"geslaagd";"niet geslaagd")',
                 geselecteerd='C2', rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=ALS(B2>=10;"geslaagd";"niet geslaagd")', 'twee woorden als uitkomst'),
            ('=ALS(B2>=10;1;0)', 'twee getallen als uitkomst, zonder aanhalingstekens'),
            ('=ALS(B2>=10;"geslaagd";"")', 'niets tonen als het niet klopt'),
        ],
        weten=[
            'Tekst zet je tussen aanhalingstekens: "geslaagd". Getallen niet.',
            'De vergelijkingstekens: > groter dan, < kleiner dan, >= groter dan of gelijk aan, '
            '<= kleiner dan of gelijk aan, = gelijk aan, <> niet gelijk aan.',
            'Let op het verschil tussen > en >=. Bij precies 10 geeft >= geslaagd, '
            'en > geeft niet geslaagd. Lees de opdracht goed: staat er vanaf, of meer dan?',
            'Twee lege aanhalingstekens ("") betekenen: laat de cel leeg.',
        ],
        fout='De aanhalingstekens vergeten. =ALS(B2>=10;geslaagd;niet geslaagd) geeft #NAAM?, '
             'want Excel zoekt dan naar een functie die geslaagd heet.',
        zelf='Zet vijf getallen neer en laat ernaast verschijnen of ze boven of onder de tien '
             'liggen. Verander daarna >= in > en kijk welke rij omslaat.',
    ),
    dict(
        naam='AANTAL.ALS',
        wat='Telt hoeveel cellen aan één voorwaarde voldoen.',
        schrijf='=AANTAL.ALS(bereik;voorwaarde)',
        argumenten=[
            ('bereik', 'waar je in zoekt, bijvoorbeeld B2:B6'),
            ('voorwaarde', 'waarop je telt, bijvoorbeeld "Eten" of ">20"'),
        ],
        uitleg=[
            'AANTAL telt alles. AANTAL.ALS telt alleen wat aan je voorwaarde voldoet.',
            'Je gebruikt het om te tellen hoe vaak iets voorkomt in een lijst, zonder zelf '
            'te turven.',
        ],
        beelden=[
            dict(bestand='aantalals-1',
                 onderschrift='In kolom B staat het soort uitgave. De formule telt hoe vaak '
                              'daar Eten staat: twee keer.',
                 kolommen=KOL_ABC,
                 rijen=UITGAVEN + [['', 'Aantal Eten', 2]],
                 formule='=AANTAL.ALS(B2:B6;"Eten")',
                 geselecteerd='C7', rechts=('C',), vet_rij=1,
                 gemarkeerd=('B3', 'B6')),
        ],
        varianten=[
            ('=AANTAL.ALS(B2:B6;"Eten")', 'telt hoe vaak het woord Eten voorkomt'),
            ('=AANTAL.ALS(C2:C6;">20")', 'telt hoeveel bedragen boven 20 liggen'),
            ('=AANTAL.ALS(C2:C6;"<>0")', 'telt hoeveel cellen niet 0 zijn'),
        ],
        weten=[
            'De punt in de naam hoort erbij: AANTAL.ALS, niet AANTALALS.',
            'Tekst als voorwaarde zet je tussen aanhalingstekens.',
            'Ook een vergelijking gaat helemaal tussen aanhalingstekens: ">20", niet >20.',
            'Hoofdletters maken niet uit: "eten" en "Eten" tellen allebei mee.',
        ],
        fout='Tellen in de verkeerde kolom. Je telt in de kolom waar het woord staat, '
             'niet in de kolom met de bedragen.',
        zelf='Maak een lijstje met drie keer ja en twee keer nee, en tel de ja\'s. '
             'Verander daarna een nee in een ja: je teller springt mee.',
    ),
    dict(
        naam='SOM.ALS',
        wat='Telt bedragen op, maar alleen die aan een voorwaarde voldoen.',
        schrijf='=SOM.ALS(zoekbereik;voorwaarde;optelbereik)',
        argumenten=[
            ('zoekbereik', 'waar je de voorwaarde toetst, bijvoorbeeld B2:B6'),
            ('voorwaarde', 'waarop je selecteert, bijvoorbeeld "Eten"'),
            ('optelbereik', 'welke cellen je optelt als het klopt, bijvoorbeeld C2:C6'),
        ],
        uitleg=[
            'AANTAL.ALS telt hoevéél. SOM.ALS telt op hoevéél euro.',
            'Denk aan de volgorde als een zin: kijk hier, zoek dit, tel dat op.',
        ],
        beelden=[
            dict(bestand='somals-1',
                 onderschrift='De formule kijkt in kolom B naar het woord Eten, en telt de '
                              'bijbehorende bedragen uit kolom C op: 28 + 31,20 = 59,20.',
                 kolommen=KOL_ABC,
                 rijen=UITGAVEN + [['', 'Totaal Eten', '59,20']],
                 formule='=SOM.ALS(B2:B6;"Eten";C2:C6)',
                 geselecteerd='C7', rechts=('C',), vet_rij=1,
                 gemarkeerd=('B3', 'B6', 'C3', 'C6')),
        ],
        varianten=[
            ('=SOM.ALS(B2:B6;"Eten";C2:C6)', 'telt de bedragen op van alle rijen met Eten'),
            ('=SOM.ALS(C2:C6;">20")', 'telt alle bedragen boven 20 op — hier mag het derde '
                                      'argument weg, want je telt op waar je ook zoekt'),
        ],
        weten=[
            'De volgorde: eerst waar je zoekt, dan wat je zoekt, dan wat je optelt.',
            'Het zoekbereik en het optelbereik moeten even groot zijn en op dezelfde rijen liggen.',
            'Laat je het derde argument weg, dan telt Excel het zoekbereik zelf op.',
            'De voorwaarde werkt net zoals bij AANTAL.ALS: tekst of een vergelijking, '
            'allebei tussen aanhalingstekens.',
        ],
        fout='Het zoekbereik en het optelbereik omwisselen. Je krijgt dan 0, want in de '
             'kolom met bedragen staat nergens het woord dat je zoekt. Geen foutmelding — '
             'gewoon een nul die klopt noch opvalt.',
        zelf='Maak een lijstje met twee soorten en wat bedragen. Tel eerst alles op met SOM, '
             'daarna één soort met SOM.ALS. De twee deeltotalen samen moeten je SOM geven.',
    ),
    dict(
        naam='VERT.ZOEKEN',
        wat='Zoekt een waarde op in een tabel en haalt er een gegeven uit dezelfde rij bij.',
        schrijf='=VERT.ZOEKEN(zoekwaarde;tabel;kolomnummer;ONWAAR)',
        argumenten=[
            ('zoekwaarde', 'wat je zoekt, meestal een code uit je eigen lijst'),
            ('tabel', 'het hele zoekblok, met de code in de eerste kolom'),
            ('kolomnummer', 'de hoeveelste kolom van dat blok je wil, geteld vanaf links'),
            ('ONWAAR', 'zoek exact; met WAAR neemt Excel de dichtstbijzijnde waarde'),
        ],
        uitleg=[
            'Je hebt een code en je wil weten wat erbij hoort. VERT.ZOEKEN gaat dat halen '
            'in een andere tabel, zodat je niets hoeft over te typen.',
            'De V staat voor verticaal: Excel zoekt van boven naar beneden in de eerste '
            'kolom van je tabel, en gaat dan naar rechts.',
        ],
        beelden=[
            dict(bestand='vertzoeken-1',
                 onderschrift='De zoektabel staat in A1 tot C5. Er wordt gezocht naar A03 '
                              'in de eerste kolom, en kolom 2 van die tabel wordt opgehaald.',
                 kolommen=[('A', 75), ('B', 90), ('C', 70)],
                 rijen=CODES,
                 formule='', geselecteerd=None, rechts=('C',), vet_rij=1,
                 gemarkeerd=('A4', 'B4')),
            dict(bestand='vertzoeken-2',
                 onderschrift='In E2 staat de code die je zoekt. De formule haalt de naam erbij. '
                              'Het cijfer 2 betekent: de tweede kolom van de zoektabel.',
                 kolommen=[('E', 75), ('F', 100)],
                 rijen=[['Code', 'Artikel'], ['A03', 'Gum']],
                 formule='=VERT.ZOEKEN(E2;$A$2:$C$5;2;ONWAAR)',
                 geselecteerd='F2', rechts=(), vet_rij=1),
        ],
        varianten=[
            ('=VERT.ZOEKEN(E2;$A$2:$C$5;2;ONWAAR)', 'haalt kolom 2 op: het artikel'),
            ('=VERT.ZOEKEN(E2;$A$2:$C$5;3;ONWAAR)', 'haalt kolom 3 op: de prijs'),
        ],
        weten=[
            'De kolom waarin je zoekt moet de EERSTE kolom van je tabel zijn.',
            'Het kolomnummer telt binnen je tabel, niet in het werkblad. Begint je tabel in '
            'kolom A, dan is A nummer 1, B nummer 2, C nummer 3.',
            'Zet dollartekens rond de tabel. Zonder die tekens schuift ze mee als je doorvoert, '
            'en dan vindt Excel vanaf een bepaalde rij niets meer.',
            'Neem altijd ONWAAR als laatste argument. Met WAAR geeft Excel stilzwijgend de '
            'dichtstbijzijnde waarde, ook als jouw code helemaal niet bestaat.',
            'Vind je #N/B, dan bestaat de zoekwaarde niet in de eerste kolom. Controleer op '
            'een spatie te veel of een verschil tussen tekst en getal.',
        ],
        fout='De dollartekens vergeten. De eerste rij klopt dan nog, maar bij het doorvoeren '
             'schuift de tabel mee naar beneden en krijg je #N/B. Zie de fiche over '
             'absolute celverwijzing.',
        zelf='Maak een tabelletje met vier codes en vier namen. Zet ernaast één code en haal '
             'de naam op. Wijzig daarna de code: de naam springt mee.',
    ),
]

# --------------------------------------------------------------------------
#  Geen functies, maar wel nodig
# --------------------------------------------------------------------------
HULP = [
    dict(
        naam='Absolute celverwijzing: de dollartekens',
        wat='Zorgt dat een verwijzing blijft staan als je een formule doorvoert.',
        schrijf='$B$1',
        argumenten=[],
        uitleg=[
            'Normaal schuift een verwijzing mee als je een formule naar beneden sleept. '
            'B2 wordt B3, dan B4. Dat is meestal precies wat je wil.',
            'Maar soms staat een gegeven maar één keer — een btw-tarief, een drempel, een '
            'percentage. Dat mag níét meeschuiven. Daarvoor zijn de dollartekens.',
        ],
        beelden=[
            dict(bestand='absoluut-1',
                 onderschrift='FOUT. In B4 stond =A4*B1 en dat klopte. Maar bij het doorvoeren '
                              'schuift B1 mee: in B5 staat =A5*B2, en B2 is leeg. Nog een rij '
                              'lager wijst hij naar de koptekst en geeft Excel #WAARDE!.',
                 kolommen=[('A', 80), ('B', 95), ('C', 85)],
                 rijen=[['Btw', '21%', ''],
                        ['', '', ''],
                        ['Bedrag', 'Btw', ''],
                        [100, 21, ''],
                        [200, 0, '<- fout'],
                        [300, '#WAARDE!', '<- fout']],
                 formule='=A5*B2', geselecteerd='B5', rechts=('A', 'B'), vet_rij=3),
            dict(bestand='absoluut-2',
                 onderschrift='JUIST. Met $B$1 blijft de verwijzing naar het btw-tarief staan, '
                              'hoe ver je ook doorvoert. Elke rij rekent met 21 procent.',
                 kolommen=[('A', 80), ('B', 95), ('C', 85)],
                 rijen=[['Btw', '21%', ''],
                        ['', '', ''],
                        ['Bedrag', 'Btw', ''],
                        [100, 21, ''],
                        [200, 42, ''],
                        [300, 63, '']],
                 formule='=A5*$B$1', geselecteerd='B5', rechts=('A', 'B'), vet_rij=3,
                 gemarkeerd=('B1',)),
        ],
        varianten=[
            ('B1', 'relatief — kolom en rij schuiven allebei mee'),
            ('$B$1', 'absoluut — er schuift niets mee; dit heb je meestal nodig'),
            ('B$1', 'alleen de rij staat vast'),
            ('$B1', 'alleen de kolom staat vast'),
        ],
        weten=[
            'Een lege cel gedraagt zich in een vermenigvuldiging als 0. Een cel met tekst '
            'geeft #WAARDE!. Zo herken je meteen hoe ver je verwijzing is doorgeschoven.',
            'Sneltoets: zet je cursor in de formule op de verwijzing en druk op F4.',
            'F4 blijft wisselen: B1 wordt $B$1, dan B$1, dan $B1, dan weer B1.',
            'Voor een gegeven dat op één plaats staat, gebruik je de volledige vorm: $B$1.',
            'Het teken $ heeft niets met geld te maken. Het betekent alleen: dit blijft staan.',
        ],
        fout='Alleen de eerste rij controleren en dan doorvoeren. De eerste rij klopt bijna '
             'altijd, ook zonder dollartekens. Het gaat pas mis vanaf de tweede. '
             'Controleer dus altijd de laatste rij van je kolom.',
        zelf='Zet een percentage in één cel en drie bedragen eronder. Bereken de btw eerst '
             'zonder dollartekens en voer door: je ziet de fout verschijnen. Zet dan de '
             'dollartekens erbij.',
    ),
    dict(
        naam='Getalnotatie: valuta, percentage en decimalen',
        wat='Verandert hoe een getal eruitziet, zonder het getal zelf aan te passen.',
        schrijf='Start › Getal',
        argumenten=[],
        uitleg=[
            'Een cel heeft een inhoud en een weergave. De getalnotatie verandert alleen '
            'de weergave.',
            'In de cel zie je € 1.131,00 en in de formulebalk staat gewoon 1131. Je rekent '
            'altijd verder met de volledige inhoud, ook met cijfers die je niet ziet.',
        ],
        beelden=[
            dict(bestand='notatie-1',
                 onderschrift='Vier keer hetzelfde getal, vier keer een andere notatie. '
                              'De inhoud van de cel verandert niet.',
                 kolommen=[('A', 110), ('B', 95)],
                 rijen=[['Notatie', 'Wat je ziet'],
                        ['Standaard', '1131'],
                        ['Valuta', '€ 1.131,00'],
                        ['Twee decimalen', '1131,00'],
                        ['Percentage', '113100%']],
                 formule='1131', geselecteerd='B2', rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('Valuta', 'zet er € bij en twee cijfers na de komma'),
            ('Percentage', 'vermenigvuldigt met 100 en zet er % bij: 0,035 wordt 3,50 %'),
            ('Meer/minder decimalen', 'de twee knoppen met de pijltjes, naast de notatielijst'),
        ],
        weten=[
            'Wil je het getal echt korter maken, gebruik dan AFRONDEN. De notatie doet dat niet.',
            'Typ je zelf 3,5 % in een cel, dan zet Excel daar achter de schermen 0,035 van.',
            'Zet je per ongeluk percentage op een gewoon getal, dan zie je opeens 113100 %. '
            'Dat is geen fout in je berekening; alleen de notatie klopt niet.',
            'Selecteer altijd de hele kolom met bedragen in één keer. Anders krijg je '
            'halfweg een andere notatie.',
        ],
        fout='Denken dat ###### een foutmelding is. De kolom is gewoon te smal voor het getal. '
             'Sleep de rand tussen de kolomletters breder, of dubbelklik erop.',
        zelf='Typ 0,25 in een cel en zet er de notatie percentage op. Kijk daarna in de '
             'formulebalk: daar staat nog altijd 0,25.',
    ),
    dict(
        naam='Doorvoeren met de vulgreep',
        wat='Kopieert een formule naar de cellen eronder, met aangepaste verwijzingen.',
        schrijf='het blokje rechtsonder in de cel',
        argumenten=[],
        uitleg=[
            'Je typt een formule één keer en laat Excel de rest doen.',
            'Klik de cel met je formule aan. Rechtsonder in de rand zie je een klein '
            'vierkantje: de vulgreep. Sleep dat naar beneden.',
        ],
        beelden=[
            dict(bestand='vulgreep-1',
                 onderschrift='C2 is één keer getypt en doorgevoerd tot C6. In elke rij '
                              'past Excel de rijnummers aan: C3 rekent met A3 en B3.',
                 kolommen=KOL_ABC,
                 rijen=[['Aantal', 'Prijs', 'Bedrag'],
                        [3, 2.5, '7,50'],
                        [5, 1.2, '6,00'],
                        [2, 4, '8,00'],
                        [8, 0.75, '6,00'],
                        [4, 3.1, '12,40']],
                 formule='=A2*B2', geselecteerd='C2', rechts=('A', 'B', 'C'), vet_rij=1),
        ],
        varianten=[
            ('slepen', 'pak de vulgreep en trek naar beneden tot waar je wil'),
            ('dubbelklikken', 'vult ineens door tot het einde van de tabel ernaast'),
        ],
        weten=[
            'De rijnummers schuiven vanzelf mee. Dat heet een relatieve celverwijzing.',
            'Wil je dat iets niet meeschuift, gebruik dan dollartekens.',
            'Controleer na het doorvoeren de laatste cel van je kolom. Klik ze aan en kijk '
            'in de formulebalk of ze naar de juiste rij verwijst.',
            'Je kunt ook naar rechts doorvoeren. Dan schuiven de kolomletters mee.',
        ],
        fout='Het resultaat overtypen in plaats van de formule door te voeren. Verandert er '
             'later iets aan de brongegevens, dan klopt jouw cel niet meer — en niemand ziet het.',
        zelf='Zet twee kolommen getallen neer, bereken in de derde het product, en voer door. '
             'Verander daarna een getal bovenaan: het bedrag past zich aan.',
    ),
    dict(
        naam='Voorwaardelijke opmaak',
        wat='Geeft cellen automatisch een kleur op basis van wat erin staat.',
        schrijf='Start › Voorwaardelijke opmaak',
        argumenten=[],
        uitleg=[
            'Je zou cellen met de hand kunnen inkleuren. Maar verandert het getal morgen, '
            'dan klopt je kleur niet meer.',
            'Met voorwaardelijke opmaak hangt de kleur aan een regel. Verandert het getal, '
            'dan verandert de kleur mee.',
        ],
        beelden=[
            dict(bestand='voorwaardelijk-1',
                 onderschrift='Regel: groter dan 20 krijgt een groene vulling. De drie '
                              'gekleurde cellen zijn niet met de hand ingekleurd.',
                 kolommen=KOL_AB,
                 rijen=[['Artikel', 'Voorraad'],
                        ['Balpen', 34],
                        ['Schrift', 12],
                        ['Gum', 45],
                        ['Lat', 8],
                        ['Map', 27]],
                 formule='', geselecteerd=None, rechts=('B',), vet_rij=1,
                 gemarkeerd=('B2', 'B4', 'B6')),
        ],
        varianten=[
            ('Regels voor markeren', 'Groter dan, Kleiner dan, Tussen, Gelijk aan, Tekst die bevat'),
            ('Boven/onder', 'de tien hoogste, of alles boven het gemiddelde'),
            ('Gegevensbalken', 'een balkje in de cel, zo lang als het getal groot is'),
        ],
        weten=[
            'Selecteer eerst de cellen, dan pas de regel kiezen.',
            'Via Voorwaardelijke opmaak › Regels beheren vind je later terug welke regels '
            'er op een blad staan, en kun je ze aanpassen of wissen.',
            'Hou het beperkt. Twee of drie regels helpen; tien maken er een kermis van '
            'en dan valt niets meer op.',
        ],
        fout='Cellen met de hand inkleuren omdat dat sneller lijkt. Bij de volgende wijziging '
             'staat je kleur op de verkeerde rij, en dat valt niemand op.',
        zelf='Zet zes getallen neer en laat alles boven een grens groen kleuren. Verander '
             'daarna een getal: de kleur volgt.',
    ),
    dict(
        naam='Beeld vastzetten',
        wat='Houdt de koprij in beeld terwijl je door een lange lijst scrolt.',
        schrijf='Beeld › Blokkeren',
        argumenten=[],
        uitleg=[
            'Bij een lijst van honderd rijen scrol je de koppen weg, en weet je halverwege '
            'niet meer welke kolom wat was.',
            'Excel bevriest alles bóven en links van de cel die je aanklikt. Klik dus de '
            'cel aan die er nét onder valt.',
        ],
        beelden=[
            dict(bestand='vastzetten-1',
                 onderschrift='Wil je rij 1 vastzetten, klik dan A2 aan — de eerste cel '
                              'ONDER wat moet blijven staan. Daarna Beeld › Blokkeren.',
                 kolommen=KOL_ABC,
                 rijen=[['Datum', 'Klant', 'Bedrag'],
                        ['02/09', 'Maes', 120],
                        ['03/09', 'Verbeke', 85],
                        ['05/09', 'Six', 240]],
                 formule='', geselecteerd='A2', rechts=('C',), vet_rij=1),
        ],
        varianten=[
            ('Titels blokkeren', 'bevriest alles boven en links van je cel'),
            ('Bovenste rij blokkeren', 'altijd rij 1, ongeacht waar je staat'),
            ('Eerste kolom blokkeren', 'altijd kolom A'),
        ],
        weten=[
            'Er verschijnt een dun lijntje waar de grens ligt. Zo zie je of het gelukt is.',
            'Klik je B2 aan, dan blijft ook kolom A staan terwijl je naar rechts scrolt.',
            'Ongedaan maken: Beeld › Blokkeren › Blokkering titels opheffen.',
            'Dit geldt alleen voor het scherm. Op papier is het iets anders: daar heet het '
            'afdruktitels.',
        ],
        fout='De koprij zelf aanklikken. Klik je rij 1 aan, dan wordt er niets bevroren en '
             'scrolt je koprij toch weg. Klik de rij eronder aan.',
        zelf='Maak een lijst van dertig rijen, zet de koppen vast en scrol naar beneden. '
             'De koppen blijven staan.',
    ),
]
