# -*- coding: utf-8 -*-
"""De kaarten van de theoriebundel over draaitabellen en grafieken.

Twee regels, dezelfde als bij de functiefiches van de basisbundel:

1. Een kaart geeft NOOIT de oplossing van een opdracht. De voorbeelden spelen
   in een eigen wereldje — de schoolbibliotheek, de kantine, het schoolarchief
   — met andere kolommen en andere cijfers dan welk startbestand ook.
   controleer.py faalt als er toch een woord uit een opdracht in opduikt.
2. Een kaart staat op zichzelf. Wie vastloopt, pakt die ene kaart en kan
   verder zonder iets anders te raadplegen.

Veertien kaarten: negen over de draaitabel, vijf over de grafiek.
"""

DEEL_TABEL = 'Deel 1 — De draaitabel'
DEEL_GRAFIEK = 'Deel 2 — De grafiek'

# --------------------------------------------------------------------------
#  De voorbeeldwereldjes
# --------------------------------------------------------------------------
BIB_KOP = ['Datum', 'Klas', 'Soort', 'Dagen']
BIB = [
    ['02/09', '5OS', 'roman', 14],
    ['02/09', '6EC', 'strip', 7],
    ['03/09', '5OS', 'strip', 10],
    ['03/09', '5OS', 'roman', 21],
    ['04/09', '6EC', 'naslag', 3],
    ['04/09', '5OS', 'strip', 7],
    ['05/09', '6EC', 'roman', 14],
]
KOL_BIB = [('A', 58), ('B', 48), ('C', 58), ('D', 48)]

# dezelfde lijst, maar met de fouten erin die een draaitabel tegenhouden
BIB_SLORDIG = [
    ['Uitleningen september', '', '', ''],
    ['', '', '', ''],
    ['Datum', 'Klas', 'Soort', 'Dagen'],
    ['02/09', '5OS', 'roman', 14],
    ['02/09', '6EC', 'strip', 7],
    ['', '', '', ''],
    ['03/09', '5OS', 'strip', 10],
    ['Totaal', '', '', 31],
]

KANTINE_KOP = ['Maand', 'Porties soep']
KANTINE = [
    ['september', 120], ['oktober', 180], ['november', 240],
    ['december', 260], ['januari', 300], ['februari', 280],
]
KOL_KANTINE = [('A', 78), ('B', 70)]

ARCHIEF_KOP = ['Jaar', 'Verbouwing']
ARCHIEF = [
    [1972, 'nieuwe turnzaal'], [1978, 'fietsenstalling'],
    [1985, 'eerste computerlokaal'], [1991, 'dakwerken'],
    [1996, 'refter vernieuwd'], [2004, 'smartboards'],
    [2009, 'zonnepanelen'], [2017, 'nieuwe vleugel'],
]
KOL_ARCHIEF = [('A', 48), ('B', 128)]

# de draaitabel die uit BIB komt: rijen = Soort, kolommen = Klas,
# waarden = Som van Dagen
DRAAI_KOP = ['Som van Dagen', '5OS', '6EC', 'Eindtotaal']
DRAAI = [
    ['naslag', '', 3, 3],
    ['roman', 35, 14, 49],
    ['strip', 17, 7, 24],
    ['Eindtotaal', 52, 24, 76],
]
KOL_DRAAI = [('A', 86), ('B', 48), ('C', 48), ('D', 66)]

# dezelfde draaitabel, maar met Aantal in plaats van Som
DRAAI_AANTAL_KOP = ['Aantal van Soort', '5OS', '6EC', 'Eindtotaal']
DRAAI_AANTAL = [
    ['naslag', '', 1, 1],
    ['roman', 2, 1, 3],
    ['strip', 2, 1, 3],
    ['Eindtotaal', 4, 3, 7],
]
KOL_DRAAI_AANTAL = [('A', 96), ('B', 48), ('C', 48), ('D', 66)]

# alleen rijen, geen kolommen — de eerste draaitabel die ze maken
DRAAI_KAAL_KOP = ['Rijlabels', 'Som van Dagen']
DRAAI_KAAL = [
    ['naslag', 3],
    ['roman', 49],
    ['strip', 24],
    ['Eindtotaal', 76],
]
KOL_DRAAI_KAAL = [('A', 74), ('B', 86)]

# het archief, gegroepeerd per tien jaar
DRAAI_GROEP_KOP = ['Rijlabels', 'Aantal verbouwingen']
DRAAI_GROEP = [
    ['1970 - 1979', 2],
    ['1980 - 1989', 1],
    ['1990 - 1999', 2],
    ['2000 - 2009', 2],
    ['2010 - 2019', 1],
    ['Eindtotaal', 8],
]
KOL_DRAAI_GROEP = [('A', 82), ('B', 112)]


# --------------------------------------------------------------------------
#  De kaarten
# --------------------------------------------------------------------------
KAARTEN = [
    # ------------------------------------------------------------ 1
    dict(
        deel=DEEL_TABEL,
        naam='Wat is een draaitabel?',
        wat='Een draaitabel vat een lange lijst samen tot een klein overzicht. '
            'Je typt er geen enkele formule voor: je sleept kolomtitels in vakjes '
            'en Excel rekent.',
        uitleg=[
            'Je kan hetzelfde met AANTAL.ALS en SOM.ALS. Voor drie categorieën is '
            'dat prima. Maar bij zeven soorten en acht eeuwen heb je 56 formules '
            'nodig, en voeg je één rij toe aan je lijst, dan mag je ze allemaal '
            'nakijken. Een draaitabel doet dat met vier keer slepen.',
            'Een draaitabel verandert niets aan je lijst. Ze maakt er een samenvatting '
            'van, ergens anders. Gooi je de draaitabel weg, dan staat je lijst er nog '
            'precies zoals ze was.',
            'Het woord "draai" komt van wat je ermee doet: je draait de lijst een '
            'kwartslag. Wat in de lijst onder elkaar staat (zeven uitleningen), staat '
            'in de draaitabel naast elkaar (drie soorten).',
        ],
        beelden=[
            dict(soort='rooster', bestand='wat-lijst',
                 onderschrift='Dit is de LIJST: zeven uitleningen, elk op een eigen rij. '
                              'Zeven regels is te overzien — zevenhonderd niet.',
                 kolommen=KOL_BIB, rijen=[BIB_KOP] + BIB, vet_rij=1,
                 rechts=('D',)),
            dict(soort='rooster', bestand='wat-draai',
                 onderschrift='Dit is de DRAAITABEL die eruit komt: dezelfde gegevens, '
                              'samengevat per soort en per klas. 76 is de som van alle '
                              'uitleendagen samen.',
                 kolommen=KOL_DRAAI, rijen=[DRAAI_KOP] + DRAAI, vet_rij=1,
                 rechts=('B', 'C', 'D')),
        ],
        weten=[
            'Een draaitabel is er om te LEZEN, niet om in te typen. Typ je in een '
            'draaitabel, dan geeft Excel een foutmelding of gooit het weg bij de '
            'eerste vernieuwing.',
            'Je kan er zoveel maken als je wil, ook meerdere van dezelfde lijst. Ze '
            'kosten niets en je kan ze gerust weggooien.',
        ],
        fout='Denken dat een draaitabel je lijst vervangt. Ze vat ze samen. De lijst '
             'blijft de waarheid; de draaitabel is een blik erop.',
    ),
    # ------------------------------------------------------------ 2
    dict(
        deel=DEEL_TABEL,
        naam='Eerst je lijst in orde brengen',
        wat='Een draaitabel stelt zes eisen aan de lijst waar ze van vertrekt. Is er '
            'één niet in orde, dan weigert Excel of komt er onzin uit.',
        stappen=[
            'Eén koprij, en maar één. Elke kolom heeft een titel, en geen twee kolommen '
            'dezelfde.',
            'Geen lege rij in de lijst. Excel denkt dan dat de lijst daar stopt.',
            'Geen lege kolom in de lijst. Zelfde verhaal.',
            'Geen totaalrij onder de lijst. Die zou als gewone rij meegeteld worden, en '
            'dan staat alles dubbel.',
            'Eén soort gegeven per kolom. Niet "14 dagen" in een kolom waar verder '
            'getallen staan: dan is het tekst en kan Excel er niet mee optellen.',
            'Geen samengevoegde cellen. Nergens.',
        ],
        uitleg=[
            'De regel achter alle zes: elke rij is één feit, elke kolom is één soort '
            'gegeven. Een titel boven de lijst mag, als er een lege rij tussen zit — '
            'dan hoort ze gewoon niet bij de lijst.',
            'Moet je toch een totaal zien? Zet het NAAST de lijst, met één lege kolom '
            'ertussen, of laat de draaitabel het maken. Die geeft je het eindtotaal '
            'gratis.',
        ],
        beelden=[
            dict(soort='rooster', bestand='lijst-slordig',
                 onderschrift='Drie fouten tegelijk: een titel zonder lege rij eronder '
                              '(rij 1 en 2 lijken deel van de lijst), een lege rij '
                              'midden in de lijst (rij 6) en een totaalrij eronder '
                              '(rij 8). Excel maakt hier een draaitabel van die 31 '
                              'dubbel telt.',
                 kolommen=KOL_BIB, rijen=BIB_SLORDIG, vet_rij=3, rechts=('D',),
                 kaders=[('A6:D6', 'ROOD'), ('A8:D8', 'ROOD')]),
            dict(soort='rooster', bestand='lijst-net',
                 onderschrift='Zo hoort het: koprij, dan alleen gegevens, en niets '
                              'eronder. Wil je er toch iets bij berekenen, zet het dan '
                              'rechts met een lege kolom ertussen.',
                 kolommen=KOL_BIB, rijen=[BIB_KOP] + BIB, vet_rij=1, rechts=('D',),
                 kaders=[('A1:D8', 'GROEN')]),
        ],
        weten=[
            'Klik één cel in je lijst aan en druk Ctrl+Shift+*. Excel selecteert dan '
            'precies wat het als "de lijst" beschouwt. Is dat niet wat jij bedoelt, '
            'dan zit er een lege rij of kolom in de weg.',
            'Je kan je lijst ook omzetten naar een echte tabel (Invoegen, Tabel). Dan '
            'groeit je draaitabel automatisch mee als je er rijen bij zet. Dat is '
            'handig, maar niet verplicht.',
        ],
        fout='Een totaalrij onder de lijst laten staan. De draaitabel telt die als een '
             'gewone uitlening mee en je eindtotaal is dan precies dubbel zo groot als '
             'het hoort. Ligt je eindtotaal opvallend dicht bij het dubbele, dan is dit het.',
    ),
    # ------------------------------------------------------------ 3
    dict(
        deel=DEEL_TABEL,
        naam='Een draaitabel invoegen',
        wat='Je maakt een lege draaitabel en krijgt het paneel Draaitabelvelden te '
            'zien. Daar gebeurt alles.',
        waar='Invoegen → Draaitabel',
        stappen=[
            'Klik één cel aan ergens in je lijst. Niet de hele lijst selecteren — één '
            'cel volstaat, Excel zoekt de rest zelf.',
            'Invoegen, dan Draaitabel.',
            'Controleer het bereik dat Excel voorstelt. Staat daar niet je hele lijst, '
            'dan klopt er iets met je lijst (zie de vorige kaart).',
            'Kies waar de draaitabel komt: Nieuw werkblad, of Bestaand werkblad met een '
            'cel die je zelf aanwijst.',
            'OK. Je krijgt een leeg vak en rechts het paneel Draaitabelvelden.',
        ],
        uitleg=[
            'Het paneel heeft twee delen. Bovenaan staan de kolomtitels van je lijst, '
            'elk met een vinkvakje. Onderaan staan vier vakken: Filters, Kolommen, '
            'Rijen en Waarden.',
            'Een veld naar Rijen slepen betekent: geef me één regel per verschillende '
            'waarde die daarin voorkomt. Naar Kolommen: één kolom per waarde. Naar '
            'Waarden: reken ermee. Naar Filters: zet er een schuifje boven waarmee ik '
            'kan kiezen wat ik zie.',
            'Vinkjes aanzetten werkt ook, maar dan raadt Excel waar het veld hoort. '
            'Tekst gaat naar Rijen, getallen naar Waarden. Slepen is duidelijker.',
            'Is het paneel weg? Klik in de draaitabel. Het paneel komt alleen als je '
            'erin staat. Blijft het weg: rechtsklik in de draaitabel en kies '
            'Veldenlijst weergeven.',
        ],
        beelden=[
            dict(soort='paneel', bestand='paneel-leeg',
                 onderschrift='Het paneel zoals je het krijgt: de vier kolomtitels '
                              'bovenaan, de vier vakken leeg. Niets aangevinkt, dus de '
                              'draaitabel is nog leeg.',
                 velden=BIB_KOP, aangevinkt=()),
        ],
        weten=[
            'Waar je de draaitabel neerzet, moet plaats zijn. Excel weigert als ze over '
            'bestaande cellen zou vallen, en een draaitabel groeit mee als er rijen bij '
            'komen. Zet ze dus niet pal boven iets anders.',
            'Twee draaitabellen van dezelfde lijst op hetzelfde blad: laat er minstens '
            'tien rijen tussen, anders botsen ze zodra er één groeit.',
        ],
        fout='De hele lijst selecteren inclusief lege rijen eronder. Dan krijg je een '
             'veld dat "(leeg)" heet, en dat telt mee in je totalen.',
    ),
    # ------------------------------------------------------------ 4
    dict(
        deel=DEEL_TABEL,
        naam='Rijen en Waarden — je eerste draaitabel',
        wat='Met twee keer slepen heb je al een samenvatting: één regel per categorie, '
            'met een getal ernaast.',
        stappen=[
            'Sleep het veld waar je PER wil samenvatten naar Rijen. Hier: Soort.',
            'Sleep het veld waar je MEE wil rekenen naar Waarden. Hier: Dagen.',
            'Lees af. Excel heeft de drie soorten gevonden en per soort de dagen '
            'opgeteld, en zet er een Eindtotaal onder.',
        ],
        uitleg=[
            'Je hebt nergens moeten typen welke soorten er bestaan. Excel heeft ze uit '
            'de lijst gehaald. Komt er morgen een vierde soort bij, dan verschijnt die '
            'vanzelf (na vernieuwen — zie kaart 9).',
            'Het veld in Rijen bepaalt de regels. Zou je Klas in Rijen zetten in plaats '
            'van Soort, dan kreeg je twee regels: 5OS en 6EC.',
            'Je mag meer dan één veld in Rijen zetten. Dan krijg je een tabel met twee '
            'niveaus: per soort, en binnen elke soort per klas. Handig, maar begin met '
            'één.',
        ],
        beelden=[
            dict(soort='paneel', bestand='rijen-paneel',
                 onderschrift='Soort in Rijen, Dagen in Waarden. Meer niet.',
                 velden=BIB_KOP, rijen=['Soort'], waarden=['Som van Dagen'],
                 aangevinkt=('Soort', 'Dagen')),
            dict(soort='rooster', bestand='rijen-tabel',
                 onderschrift='Het resultaat: drie regels en een eindtotaal. 49 is '
                              '14 + 21 + 14, de drie romans uit de lijst.',
                 kolommen=KOL_DRAAI_KAAL, rijen=[DRAAI_KAAL_KOP] + DRAAI_KAAL,
                 vet_rij=1, rechts=('B',)),
        ],
        weten=[
            'Een veld weer weghalen: sleep het uit het vak, of klik het vinkje uit. Je '
            'lijst merkt daar niets van.',
            'De volgorde van de regels is alfabetisch. Dat is zelden de volgorde die je '
            'wil — zie kaart 7 om te sorteren.',
        ],
        fout='Hetzelfde veld in Rijen én in Waarden zetten en je afvragen waarom er '
             'rare getallen komen. Dat mag wel degelijk (je telt dan hoe vaak elke '
             'waarde voorkomt), maar doe het bewust.',
    ),
    # ------------------------------------------------------------ 5
    dict(
        deel=DEEL_TABEL,
        naam='Aantal of Som?',
        wat='Excel kiest zelf wat het met je waardeveld doet. Die keuze is vaak fout, '
            'en je ziet het alleen als je op het kopje let.',
        waar='Klik het veld in Waarden aan → Waardeveldinstellingen',
        stappen=[
            'Kijk naar het kopje linksboven in je draaitabel. Staat daar "Som van '
            'Dagen" of "Aantal van Dagen"?',
            'Klopt het niet: klik het veld aan in het vak Waarden.',
            'Kies Waardeveldinstellingen.',
            'Kies Som, Aantal, Gemiddelde, Max of Min. OK.',
        ],
        uitleg=[
            'De regel die Excel volgt: staan er in die kolom alleen getallen, dan Som. '
            'Staat er ook maar één stukje tekst in, of één lege cel, dan Aantal.',
            'Daarom is het zo belangrijk dat elke kolom één soort gegeven bevat. Eén '
            'cel waar iemand "onbekend" typte in plaats van ze leeg te laten, en je '
            'hele draaitabel telt in plaats van op te tellen.',
            'Aantal is niet fout — het is gewoon een ander antwoord. "Hoeveel '
            'uitleningen?" is Aantal. "Hoeveel dagen samen?" is Som. Vraag jezelf '
            'telkens af welke van de twee je nodig hebt.',
        ],
        beelden=[
            dict(soort='dialoog', bestand='waardeveld',
                 onderschrift='Waardeveldinstellingen. Hier kies je wat er met het veld '
                              'gebeurt. Som is wat je meestal wil.',
                 titel='Waardeveldinstellingen', regels=['Samenvatten met:'],
                 keuzes=['Som', 'Aantal', 'Gemiddelde', 'Max', 'Min'], gekozen='Som'),
            dict(soort='rooster', bestand='aantal-tabel',
                 onderschrift='Dezelfde velden, maar met Aantal. Nu staat er hoeveel '
                              'KEER er iets uitgeleend is, niet voor hoeveel dagen. '
                              'Zeven uitleningen in plaats van 76 dagen.',
                 kolommen=KOL_DRAAI_AANTAL,
                 rijen=[DRAAI_AANTAL_KOP] + DRAAI_AANTAL, vet_rij=1,
                 rechts=('B', 'C', 'D')),
        ],
        weten=[
            'Het kopje van je draaitabel zegt altijd wat er gebeurt: "Som van Dagen", '
            '"Aantal van Soort". Lees dat kopje. Het is je enige waarschuwing.',
            'Je mag hetzelfde veld twee keer in Waarden zetten: één keer als Som en één '
            'keer als Aantal. Dan staan ze naast elkaar.',
            'Gemiddelde van een gemiddelde is geen gemiddelde. Wil je het gemiddelde '
            'over alles, lees dan de rij Eindtotaal — niet het gemiddelde van de '
            'regels erboven.',
        ],
        fout='Niet merken dat er Aantal staat. Je draaitabel geeft dan keurige kleine '
             'getallen die er plausibel uitzien, en je eindtotaal is het aantal rijen '
             'van je lijst in plaats van de som. Komt je eindtotaal precies overeen met '
             'het aantal regels in je lijst, dan staat het op Aantal.',
    ),
    # ------------------------------------------------------------ 6
    dict(
        deel=DEEL_TABEL,
        naam='Een tweede richting: Kolommen',
        wat='Zet je er ook een veld in Kolommen bij, dan krijg je een kruistabel: twee '
            'vragen tegelijk beantwoord.',
        stappen=[
            'Je hebt al Soort in Rijen en Dagen in Waarden.',
            'Sleep Klas naar Kolommen.',
            'Nu heeft elke soort een kolom per klas, en Excel zet er rij- en '
            'kolomtotalen bij.',
        ],
        uitleg=[
            'Een kruistabel beantwoordt niet "hoeveel per soort" en "hoeveel per klas", '
            'maar "hoeveel per soort PER klas". Dat is een derde vraag, en je ziet ze '
            'alleen zo.',
            'Lege vakjes betekenen: die combinatie komt niet voor. In het voorbeeld '
            'heeft 5OS geen enkel naslagwerk geleend, dus daar staat niets. Dat is geen '
            'fout.',
            'Wil je een streepje in plaats van een leeg vak: rechtsklik in de '
            'draaitabel, Draaitabelopties, en vul bij "Voor lege cellen weergeven" een '
            'streepje in. Dat leest rustiger.',
            'Hou het bij één veld in Kolommen. Twee velden in Kolommen geeft een tabel '
            'die niemand nog kan lezen.',
        ],
        beelden=[
            dict(soort='paneel', bestand='kruis-paneel',
                 onderschrift='Drie vakken gevuld: Soort in Rijen, Klas in Kolommen, '
                              'Dagen in Waarden.',
                 velden=BIB_KOP, rijen=['Soort'], kolommen=['Klas'],
                 waarden=['Som van Dagen'],
                 aangevinkt=('Klas', 'Soort', 'Dagen')),
            dict(soort='rooster', bestand='kruis-tabel',
                 onderschrift='De kruistabel. Je leest er nu drie dingen uit: per soort '
                              '(rechterkolom), per klas (onderste rij) en per combinatie '
                              '(binnenin). 5OS leende geen naslagwerk, vandaar het lege '
                              'vak.',
                 kolommen=KOL_DRAAI, rijen=[DRAAI_KOP] + DRAAI, vet_rij=1,
                 rechts=('B', 'C', 'D'),
                 kaders=[('D2:D5', 'GROEN'), ('B5:C5', 'GROEN')]),
        ],
        weten=[
            'Rijen en Kolommen mag je verwisselen door de velden van vak te wisselen. '
            'De cijfers blijven dezelfde, de tabel draait een kwartslag. Kies de vorm '
            'die op je blad past: veel categorieën horen in Rijen, weinig in Kolommen.',
            'De kolommen staan in de volgorde van het veld: getallen van klein naar '
            'groot, tekst alfabetisch.',
        ],
        fout='Een veld met veertig verschillende waarden in Kolommen zetten. Je krijgt '
             'veertig kolommen die niemand kan overzien. Zulke velden horen in Rijen.',
    ),
    # ------------------------------------------------------------ 7
    dict(
        deel=DEEL_TABEL,
        naam='Sorteren en filteren',
        wat='Een draaitabel staat alfabetisch. Meestal wil je ze op de getallen '
            'gesorteerd, met de grootste bovenaan.',
        stappen=[
            'Sorteren: rechtsklik op een getal in de kolom waarop je wil sorteren, kies '
            'Sorteren, dan Van groot naar klein.',
            'Filteren: klik op het pijltje naast Rijlabels en vink uit wat je niet wil '
            'zien.',
            'Een filterschuif erboven: sleep een veld naar het vak Filters. Je krijgt '
            'dan bovenaan je draaitabel een keuzevakje.',
        ],
        uitleg=[
            'Sorteren op waarde is bijna altijd wat je bedoelt. "Welke soort wordt het '
            'meest geleend" lees je in één blik als de grootste bovenaan staat, en niet '
            'als alles alfabetisch door elkaar staat.',
            'Het eindtotaal blijft altijd onderaan, ook na sorteren. Dat is de bedoeling.',
            'Een filter verandert de getallen: wat je wegfiltert, telt niet meer mee in '
            'de totalen. Vergeet dus niet dat je gefilterd hebt — zet er een tekstje '
            'bij als je het blad doorgeeft.',
            'Maak je straks een grafiek van je draaitabel, dan volgt die grafiek de '
            'volgorde van de tabel. Sorteer dus EERST de tabel en maak DAN de grafiek.',
        ],
        beelden=[
            dict(soort='rooster', bestand='sorteren',
                 onderschrift='Dezelfde drie soorten, nu gesorteerd van groot naar '
                              'klein. Je ziet meteen dat romans veruit het langst '
                              'uitstaan.',
                 kolommen=KOL_DRAAI_KAAL,
                 rijen=[DRAAI_KAAL_KOP, ['roman', 49], ['strip', 24], ['naslag', 3],
                        ['Eindtotaal', 76]],
                 vet_rij=1, rechts=('B',), gemarkeerd=('A2', 'B2')),
        ],
        weten=[
            'Sorteren op de rijlabels zelf (A naar Z) kan ook, via hetzelfde menu. Soms '
            'is alfabetisch juist wel wat je wil, bijvoorbeeld bij maanden of eeuwen die '
            'toevallig in volgorde staan.',
            'Een filter zet je weer af door bij het pijltje "Alles selecteren" aan te '
            'vinken.',
        ],
        fout='Een grafiek maken en dan pas de tabel sorteren, en je afvragen waarom de '
             'balken in de verkeerde orde staan. Eerst de tabel.',
    ),
    # ------------------------------------------------------------ 8
    dict(
        deel=DEEL_TABEL,
        naam='Groeperen',
        wat='Je kan jaartallen, getallen of datums in een draaitabel laten bundelen: '
            'per tien, per maand, per eeuw. Dan krijg je een handvol regels in plaats '
            'van tientallen.',
        waar='Rechtsklik op een rijlabel → Groeperen',
        stappen=[
            'Zet het veld met de jaartallen in Rijen. Je krijgt één regel per jaar — te '
            'veel om iets te zien.',
            'Rechtsklik op een van die jaartallen en kies Groeperen.',
            'Vul in: Beginnen bij, Eindigen bij, en Per. Voor decennia: beginnen bij '
            '1970, per 10.',
            'OK. De regels zijn nu groepen.',
        ],
        uitleg=[
            'Dit werkt alleen als het veld echt getallen of echte datums bevat. Staan '
            'je jaartallen als tekst in de lijst, dan biedt Excel Groeperen niet aan.',
            'Bij datums krijg je een ander venster: daar vink je Jaren, Kwartalen of '
            'Maanden aan. Je mag er meer dan één aanvinken; dan krijg je niveaus.',
            'Een groepering ongedaan maken: rechtsklik en Groepering opheffen.',
            'Je kan ook zonder groeperen werken: zet gewoon een kolom in je lijst waar '
            'de groep al in staat (een kolom "decennium" naast de kolom "jaar"). Dat is '
            'meer werk vooraf, maar het werkt overal en je ziet wat er gebeurt.',
        ],
        beelden=[
            dict(soort='rooster', bestand='groeperen-bron',
                 onderschrift='De lijst: acht verbouwingen, acht verschillende '
                              'jaartallen. Een draaitabel hierop geeft acht regels van '
                              'elk één.',
                 kolommen=KOL_ARCHIEF, rijen=[ARCHIEF_KOP] + ARCHIEF, vet_rij=1),
            dict(soort='rooster', bestand='groeperen-na',
                 onderschrift='Na Groeperen per 10: vijf regels in plaats van acht, en '
                              'nu zie je wel iets — de jaren negentig en de jaren nul '
                              'waren de drukste.',
                 kolommen=KOL_DRAAI_GROEP,
                 rijen=[DRAAI_GROEP_KOP] + DRAAI_GROEP, vet_rij=1, rechts=('B',)),
        ],
        weten=[
            'Groepeer altijd met ronde grenzen. Laat je Excel zelf beginnen, dan start '
            'het bij het kleinste getal uit je lijst en krijg je groepen als '
            '1972 - 1981. Dat leest niemand.',
            'Twee draaitabellen van dezelfde lijst delen soms hun groepering. Verandert '
            'de ene mee met de andere, dan is dat de reden.',
        ],
        fout='Groeperen proberen op een kolom die tekst bevat. Excel zegt dan "Kan die '
             'selectie niet groeperen". Controleer of je jaartallen rechts in de cel '
             'staan (getal) of links (tekst).',
    ),
    # ------------------------------------------------------------ 9
    dict(
        deel=DEEL_TABEL,
        naam='Vernieuwen',
        wat='Een draaitabel rekent NIET automatisch mee. Verander je iets in je lijst, '
            'dan blijft de draaitabel het oude getal tonen tot je ze vernieuwt.',
        waar='Rechtsklik in de draaitabel → Vernieuwen',
        uitleg=[
            'Dit is het grote verschil met een gewone formule. Zet je in een cel '
            '=SOM(D2:D8) en verander je D5, dan springt het totaal meteen mee. Een '
            'draaitabel niet: die werkt op een kopie van je lijst die Excel apart '
            'bijhoudt.',
            'Dat is geen fout van Excel. Bij een lijst van honderdduizend regels zou '
            'alles vastlopen als elke draaitabel bij elke toetsaanslag opnieuw rekende.',
            'Voeg je rijen TOE onderaan je lijst, dan volstaat vernieuwen vaak niet: het '
            'bronbereik loopt nog tot de oude laatste rij. Dan moet je het bereik '
            'aanpassen (Draaitabel analyseren, Gegevensbron wijzigen) — of je lijst van '
            'bij het begin als echte tabel opzetten, want die groeit vanzelf mee.',
        ],
        beelden=[],
        weten=[
            'Vernieuwen kost niets. Doe het uit gewoonte, elke keer voor je iets van je '
            'draaitabel aflezen of noteren.',
            'Alles tegelijk vernieuwen: Gegevens, dan Alles vernieuwen.',
            'Controlegetal: als je lijst een totaal heeft dat je ook met SOM kan '
            'berekenen, leg dat naast het eindtotaal van je draaitabel. Lopen ze uit '
            'elkaar, dan heb je nog niet vernieuwd of staat je bronbereik verkeerd.',
        ],
        fout='Een rij toevoegen, de draaitabel niet vernieuwen, en het oude getal '
             'overschrijven in je verslag. Niets in Excel waarschuwt je hiervoor. '
             'Vernieuwen is een gewoonte, geen knop die je zoekt als er iets misgaat.',
    ),
    # ------------------------------------------------------------ 10
    dict(
        deel=DEEL_GRAFIEK,
        naam='Een grafiek invoegen',
        wat='Een grafiek maken is drie handelingen. De tijd gaat zitten in wat erna '
            'komt: leesbaar maken.',
        waar='Invoegen → het soort grafiek',
        stappen=[
            'Selecteer wat in de grafiek moet: de kolom met de namen EN de kolom met de '
            'getallen, koprij inbegrepen. Niet de totaalrij.',
            'Invoegen, dan het soort grafiek dat je wil.',
            'Sleep de grafiek naar waar ze moet staan, en trek ze groot genoeg.',
        ],
        uitleg=[
            'Wat je selecteert, bepaalt alles. Selecteer je alleen de getallen, dan '
            'krijg je 1, 2, 3 onder je balken in plaats van namen. Selecteer je de '
            'totaalrij mee, dan krijg je één reusachtige balk waar de rest bij in het '
            'niet valt.',
            'Twee kolommen die niet naast elkaar staan: selecteer de eerste, hou Ctrl '
            'ingedrukt en selecteer de tweede.',
            'Een grafiek hoort bij een blad, niet bij een cel. Ze zweeft erboven. Je mag '
            'ze overal neerzetten, ook op een ander blad (Grafiek verplaatsen).',
        ],
        beelden=[
            dict(soort='rooster', bestand='selectie',
                 onderschrift='Wat je selecteert voor een staafdiagram: de koprij en de '
                              'zes maanden. Het kader stopt vóór een eventuele '
                              'totaalrij.',
                 kolommen=KOL_KANTINE, rijen=[KANTINE_KOP] + KANTINE, vet_rij=1,
                 rechts=('B',), kaders=[('A1:B7', 'GROEN')]),
            dict(soort='staaf', bestand='eerste-grafiek',
                 onderschrift='Wat eruit komt. Nog kaal, maar de vorm klopt al.',
                 titel='Porties soep per maand',
                 labels=[r[0][:3] for r in KANTINE],
                 waarden=[r[1] for r in KANTINE]),
        ],
        weten=[
            'Een grafiek is levend: verander je een getal in de cellen, dan beweegt de '
            'balk mee. Anders dan een draaitabel heeft een gewone grafiek géén '
            'vernieuwen nodig.',
            'Grafiek weg? Klik ze aan en druk Delete. Je gegevens blijven staan.',
            'Een grafiek op een eigen blad: rechtsklik, Grafiek verplaatsen, Nieuw blad. '
            'Handig als ze groot moet geprojecteerd worden.',
        ],
        fout='De totaalrij meeselecteren. Je krijgt dan een balk die even groot is als '
             'alle andere samen, en de rest wordt onleesbaar klein.',
    ),
    # ------------------------------------------------------------ 11
    dict(
        deel=DEEL_GRAFIEK,
        naam='Welk type bij welke vraag?',
        wat='Het type grafiek is geen smaakkwestie. Elk type beantwoordt één soort '
            'vraag; het verkeerde type maakt je gegevens onleesbaar of zelfs '
            'misleidend.',
        uitleg=[
            'STAAFDIAGRAM — "wie is de grootste?" Categorieën naast elkaar vergelijken. '
            'Werkt voor alles wat je kan opsommen: landen, soorten, klassen. Sorteer op '
            'grootte, dan is het antwoord één blik.',
            'LIJNDIAGRAM — "hoe evolueert het?" Alleen voor iets dat in de tijd '
            'verloopt. De lijn tussen twee punten suggereert dat het daartussen '
            'geleidelijk ging; gebruik hem dus niet voor categorieën, want tussen '
            '"roman" en "strip" ligt niets.',
            'CIRKELDIAGRAM — "welk aandeel van het geheel?" Alleen als de delen samen '
            'een zinvol geheel vormen, en bij hoogstens vier of vijf delen. Mensen '
            'kunnen hoeken slecht vergelijken; bij zes punten raad je maar wat.',
            'Twijfel je? Neem een staafdiagram. Dat is voor bijna elke vraag het '
            'veiligste antwoord.',
        ],
        beelden=[
            dict(soort='lijn', bestand='type-lijn',
                 onderschrift='GOED gebruik van een lijn: de maanden volgen elkaar op, '
                              'dus de lijn ertussen betekent iets. Je ziet de stijging '
                              'tot januari en de knik daarna.',
                 titel='Porties soep per maand',
                 labels=[r[0][:3] for r in KANTINE],
                 waarden=[r[1] for r in KANTINE], astitel_x='maand'),
            dict(soort='lijn', bestand='type-lijn-fout',
                 onderschrift='FOUT gebruik van een lijn: tussen naslag en '
                              'roman ligt niets. De lijn doet alsof er een verloop is '
                              'dat er niet is. Dit hoort een staafdiagram te zijn.',
                 titel='Uitleendagen per soort',
                 labels=['naslag', 'roman', 'strip'], waarden=[3, 49, 24]),
            dict(soort='cirkel', bestand='type-cirkel',
                 onderschrift='Een cirkeldiagram kan hier wél: drie delen, en samen zijn '
                              'ze het geheel van alle uitleendagen. Bij zeven soorten '
                              'was dit onleesbaar geweest.',
                 titel='Aandeel in de uitleendagen',
                 labels=['naslag', 'roman', 'strip'], waarden=[3, 49, 24]),
        ],
        weten=[
            'Een staafdiagram met de balken liggend heet een staafdiagram, rechtopstaand '
            'heet het eigenlijk een kolomdiagram. In het menu van Excel staat het onder '
            'Kolom. In de spreektaal zegt iedereen staafdiagram.',
            'Metingen die niet even ver uit elkaar liggen (1850, 1875, 1900, 1914) zet '
            'een gewoon lijndiagram toch op gelijke afstand. De vorm van je lijn klopt '
            'dan niet helemaal. Zeg dat erbij, of gebruik een spreidingsdiagram.',
        ],
        fout='Een cirkeldiagram van zeven of meer stukken. Niemand ziet het verschil '
             'tussen 13 % en 15 %, en de taartpunten die klein zijn verdwijnen in de '
             'legende.',
    ),
    # ------------------------------------------------------------ 12
    dict(
        deel=DEEL_GRAFIEK,
        naam='Een grafiek leesbaar maken',
        wat='Een grafiek zonder titel en astitels is een plaatje. Met titel en astitels '
            'is het een antwoord.',
        waar='Klik de grafiek aan → het plusteken rechtsboven (Grafiekelementen)',
        stappen=[
            'Klik de grafiek aan. Rechtsboven verschijnt een plusteken.',
            'Vink aan wat je nodig hebt: Grafiektitel, Astitels, Gegevenslabels, '
            'Legenda.',
            'Klik de titel aan en typ er iets zinnigs in. "Grafiektitel" laten staan is '
            'geen titel.',
        ],
        uitleg=[
            'Een goede titel zegt wat er te zien is, niet wat er getekend is. "Porties '
            'soep per maand" is beter dan "Grafiek 1". Nog beter is een titel die het '
            'antwoord geeft: "Soep piekt in januari".',
            'Astitels zijn nodig zodra de eenheid niet vanzelf spreekt. Staat er 300 op '
            'de as — driehonderd wat? Zet "porties" links en "maand" onderaan.',
            'Gegevenslabels (het getal boven elke balk) zijn handig bij weinig balken en '
            'storend bij veel. Vuistregel: tot een stuk of acht balken wel, daarboven '
            'niet.',
            'Een legenda heeft alleen zin bij meer dan één reeks. Eén reeks betekent: '
            'legenda weg, de titel zegt al wat het is.',
        ],
        beelden=[
            dict(soort='staaf', bestand='leesbaar-slecht',
                 onderschrift='Zonder titel en zonder astitels. Je ziet dat iets stijgt, '
                              'maar niet wat, en niet in welke eenheid.',
                 titel='', labels=[r[0][:3] for r in KANTINE],
                 waarden=[r[1] for r in KANTINE], waardelabels=False),
            dict(soort='staaf', bestand='leesbaar-goed',
                 onderschrift='Dezelfde cijfers, nu met een titel die iets zegt, '
                              'astitels en getallen boven de balken.',
                 titel='Soep piekt in januari',
                 labels=[r[0][:3] for r in KANTINE],
                 waarden=[r[1] for r in KANTINE],
                 astitel_x='maand', astitel_y='porties'),
        ],
        weten=[
            'Maak de grafiek groot genoeg. Jaartallen die schuin staan of over elkaar '
            'vallen, zijn bijna altijd een te smalle grafiek.',
            'Kleur hoeft niet. Eén kleur voor alle balken is rustiger dan zeven. '
            'Gebruik een tweede kleur alleen om één balk te laten opvallen.',
        ],
        fout='De tekst "Grafiektitel" laten staan. Dat is het eerste wat een lezer ziet '
             'en meteen de indruk dat je niet klaar bent.',
    ),
    # ------------------------------------------------------------ 13
    dict(
        deel=DEEL_GRAFIEK,
        naam='Een draaigrafiek',
        wat='Een grafiek die rechtstreeks op een draaitabel staat. Verander je de '
            'draaitabel, dan verandert de grafiek mee.',
        waar='Klik in de draaitabel → Invoegen → Draaigrafiek',
        stappen=[
            'Klik één cel aan in je draaitabel.',
            'Invoegen, dan Draaigrafiek. Kies het type.',
            'De grafiek verschijnt met dezelfde categorieën en waarden als de tabel.',
        ],
        uitleg=[
            'Het voordeel: je hoeft niets te selecteren en de grafiek blijft gelijk aan '
            'de tabel. Sorteer je de tabel, dan sorteert de grafiek mee. Filter je iets '
            'weg, dan verdwijnt de balk.',
            'Het eindtotaal komt NIET als balk in de grafiek. Excel weet dat het een '
            'totaal is. Dat is precies waarom een draaigrafiek handiger is dan zelf '
            'selecteren — daar moet je het totaal met de hand buiten je selectie '
            'houden.',
            'Op de draaigrafiek staan knopjes met de veldnamen. Daarmee filter je '
            'rechtstreeks in de grafiek. Storen ze bij het afdrukken: rechtsklik en kies '
            'Alle veldknoppen verbergen.',
        ],
        beelden=[
            dict(soort='rooster', bestand='draaigrafiek-tabel',
                 onderschrift='De draaitabel, gesorteerd van groot naar klein.',
                 kolommen=KOL_DRAAI_KAAL,
                 rijen=[DRAAI_KAAL_KOP, ['roman', 49], ['strip', 24], ['naslag', 3],
                        ['Eindtotaal', 76]],
                 vet_rij=1, rechts=('B',)),
            dict(soort='staaf', bestand='draaigrafiek-beeld',
                 onderschrift='De draaigrafiek erbij. Let op: geen balk voor het '
                              'eindtotaal van 76, en de volgorde volgt de tabel.',
                 titel='Uitleendagen per soort',
                 labels=['roman', 'strip', 'naslag'], waarden=[49, 24, 3],
                 astitel_y='dagen'),
        ],
        weten=[
            'Een draaigrafiek en zijn draaitabel horen bij elkaar. Verwijder je de tabel, '
            'dan verdwijnt de grafiek.',
            'Wil je een grafiek die NIET meebeweegt, kopieer ze dan en plak ze als '
            'afbeelding. Handig als je ze in een verslag zet.',
        ],
        fout='Een draaigrafiek maken van een draaitabel die nog niet gesorteerd of nog '
             'niet vernieuwd is. De grafiek erft alles, ook wat er niet klopt.',
    ),
    # ------------------------------------------------------------ 14
    dict(
        deel=DEEL_GRAFIEK,
        naam='Wat een grafiek kan verbergen',
        wat='Dezelfde cijfers kunnen er heel anders uitzien. Dat is niet altijd '
            'kwaadwillig, maar je moet het kunnen zien — in de grafieken van anderen én '
            'in die van jezelf.',
        uitleg=[
            'DE AS DIE NIET BIJ NUL BEGINT. Begint je verticale as bij 250 in plaats van '
            '0, dan lijkt een verschil van 10 % een verdubbeling. Bij een staafdiagram '
            'is dat altijd misleidend: de hoogte van de balk IS de boodschap. Bij een '
            'lijndiagram mag het soms, als het om kleine schommelingen gaat, maar zeg '
            'het er dan bij.',
            'TE WEINIG PUNTEN. Twee metingen met een lijn ertussen zien er uit als een '
            'trend. Twee punten zijn geen trend.',
            'ONGELIJKE AFSTANDEN. Metingen om de 80, 100, 50 en 14 jaar op gelijke '
            'afstand zetten vervormt de vorm van je lijn. De laatste jaren lijken dan '
            'veel trager te gaan dan ze gingen.',
            'DRIE DIMENSIES. Een 3D-taart of 3D-balk ziet er professioneel uit en liegt: '
            'wat vooraan staat lijkt groter. Laat het weg.',
        ],
        beelden=[
            dict(soort='staaf', bestand='verbergen-goed',
                 onderschrift='As vanaf nul. Je ziet wat er is: november, december en '
                              'januari liggen dicht bij elkaar.',
                 titel='Porties soep — as vanaf 0',
                 labels=['nov', 'dec', 'jan'], waarden=[240, 260, 300],
                 waardelabels=True),
            dict(soort='staaf', bestand='verbergen-fout',
                 onderschrift='Exact dezelfde drie getallen, maar de as begint bij 230. '
                              'Januari lijkt nu zeven keer zo hoog als november, terwijl '
                              'het er maar een kwart meer zijn. Er is niets gelogen en '
                              'toch klopt het beeld niet.',
                 titel='Porties soep — as vanaf 230',
                 labels=['nov', 'dec', 'jan'], waarden=[240, 260, 300],
                 laag=230, waardelabels=True),
        ],
        weten=[
            'Kijk bij elke grafiek die je krijgt eerst naar de verticale as. Waar begint '
            'ze? Dat is de snelste controle die er is.',
            'Maak je zelf een grafiek voor anderen: as vanaf nul, geen 3D, één kleur, '
            'een titel die zegt wat er staat. Dan kan niemand je iets verwijten.',
        ],
        fout='Je eigen grafiek niet nalezen. De meeste misleidende grafieken zijn niet '
             'gemaakt om te misleiden — iemand heeft gewoon op OK geklikt bij wat Excel '
             'voorstelde.',
    ),
]

DELEN = [DEEL_TABEL, DEEL_GRAFIEK]
