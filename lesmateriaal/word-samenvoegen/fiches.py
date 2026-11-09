# -*- coding: utf-8 -*-
"""De theoriebundel: twaalf fiches over samenvoegen.

Apart boekje, net als draaitabellen-en-grafieken.docx. De opdracht verwijst
er per stap naar en legt zelf niets uit.

Deel 1 is Excel: de lijst zo klaarmaken dat Word ermee kan werken.
Deel 2 is Word: etiketten, brieven, regels en filters.
Deel 3 is wat er misgaat — de fiche die je het vaakst zal moeten aanwijzen.

De lintnamen zijn die van het Nederlandstalige Word (Microsoft 365 en 2021).
In een Engelse Word heet het tabblad Mailings in plaats van Verzendlijsten.
"""
import sys

sys.dont_write_bytecode = True

DELEN = ["De lijst klaarmaken (Excel)", "Samenvoegen (Word)",
         "Als het misgaat"]

FICHES = [
    # ============================================ deel 1 — Excel
    dict(
        deel="De lijst klaarmaken (Excel)", naam="Wat Word van je lijst verwacht",
        functies=[],
        wat="Vijf regels. Houd je er één niet aan, dan werkt het samenvoegen "
            "niet of maar half.",
        stappen=[
            'ÉÉN koprij, en die staat bovenaan de kolom. Geen titel erboven, '
            'geen tweede koprij eronder.',
            'Elke kolom heeft een naam, en die naam is kort en zonder '
            'rariteiten. "Adresregel" werkt, "Adres (straat + nr.)" vraagt '
            'problemen.',
            'GEEN samengevoegde cellen. Nergens. Word maakt daar een '
            'onleesbare kolom van.',
            'Geen lege rij IN de lijst, en niets eronder dat er niet bij hoort.',
            'Geef het werkblad een duidelijke naam. Word vraagt straks welk '
            'blad het moet gebruiken, en dan zoek je niet graag tussen '
            'Blad1, Blad2 en Blad3.',
        ],
        uitleg=[
            'Dit is dezelfde regel als bij een draaitabel, en om dezelfde '
            'reden: een programma dat je lijst leest, moet weten waar ze '
            'begint en waar ze stopt.',
            'Regel 1 is strenger dan je denkt. Word neemt de EERSTE GEBRUIKTE '
            'RIJ van het werkblad als kolomnamen. Staat er een titel op rij 1 '
            'en je koprij op rij 3, dan denkt Word dat die titel de kolomnaam '
            'is en gaat alles mis. Daarom staat er op zo\'n blad niets anders '
            'dan de lijst — zelfs geen losse cel rechts ervan.',
            'Heb je toch een cel nodig waar je naar wil verwijzen, zoals een '
            'peildatum? Zet die op een ANDER werkblad. Word leest alleen het '
            'blad dat je kiest, dus daar komt het niet in de weg. Je verwijst '
            'er dan naar met de bladnaam ervoor: Start!$B$1.',
            'Bewaar het Excelbestand en het Worddocument in DEZELFDE map. '
            'Word onthoudt waar je lijst staat; verplaats je ze achteraf, dan '
            'vindt Word ze niet meer terug.',
        ],
        weten=['Een kolom die je niet gebruikt mag blijven staan. Word toont '
               'alle kolommen en jij kiest wat je invoegt.'],
        fout='Een titel boven de koprij laten staan. Word denkt dan dat die '
             'titel de kolomnaam is, en je krijgt één kolom met een rare naam '
             'en de echte koprij als eerste gegevensrij.',
    ),
    dict(
        deel="De lijst klaarmaken (Excel)", naam="Plakken met &",
        functies=[],
        wat="Zet stukken tekst aan elkaar tot één nieuwe tekst.",
        schrijf='=A2&" "&B2',
        argumenten=[('&', 'plakt wat ervoor en erna staat aan elkaar'),
                    ('" "', 'een stukje tekst dat je er zelf bij typt')],
        uitleg=[
            'In een brief wil je "Kerkstraat 12" op één regel, niet de straat '
            'en het nummer in twee kolommen. Daarom plak je ze in Excel aan '
            'elkaar, en voeg je in Word één veld in.',
            'Alles wat je zelf bijtypt, moet tussen aanhalingstekens. '
            'Celverwijzingen niet. Vergeet de spatie niet: =A2&B2 geeft '
            'Kerkstraat12.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = Kerkstraat     B2 = 12',
                    '=A2&" "&B2  geeft  Kerkstraat 12'],
                   ['A2 = Lotte',
                    '="Beste "&A2  geeft  Beste Lotte']]),
        weten=['Je kan ook in Word alles los invoegen met een spatie ertussen. '
               'Dat werkt, maar één kolom in Excel is minder werk en minder '
               'kans op een dubbele spatie.'],
        fout='De aanhalingstekens vergeten rond het stukje tekst dat je zelf '
             'typt. Zonder aanhalingstekens denkt Excel dat je een celnaam '
             'bedoelt en krijg je #NAAM?.',
    ),
    dict(
        deel="De lijst klaarmaken (Excel)", naam="VERT.ZOEKEN",
        functies=['VERT.ZOEKEN'],
        wat="Haalt bij een code de bijhorende gegevens uit een andere tabel.",
        schrijf='=VERT.ZOEKEN(code;$tabel$;kolom;ONWAAR)',
        argumenten=[('code', 'de cel met de code die je opzoekt'),
                    ('$tabel$', 'de zoektabel, vastgezet met dollartekens'),
                    ('kolom', 'de hoeveelste kolom van die tabel je wil'),
                    ('ONWAAR', 'alleen een exacte treffer telt')],
        uitleg=[
            'In je lijst staat alleen een taakcode. Een brief waarin "T01" '
            'staat, stuur je niet op.',
            'Zet de zoektabel vast met dollartekens voor je doorvoert, anders '
            'zakt ze mee naar beneden en krijg je onderaan #N/B.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['H4 = T01',
                    '=VERT.ZOEKEN(H4;Taken!$A$4:$E$11;2;ONWAAR)  geeft  Bar'],
                   ['H4 = T01',
                    '=VERT.ZOEKEN(H4;Taken!$A$4:$E$11;3;ONWAAR)  geeft  '
                    'Main Stage']]),
        weten=['Staat de zoektabel op een ander werkblad, dan zet je de '
               'bladnaam en een uitroepteken ervoor: Taken!$A$4:$E$11.'],
        fout='#N/B onderaan de kolom. De zoektabel is niet vastgezet.',
    ),
    dict(
        deel="De lijst klaarmaken (Excel)", naam="TEKST",
        functies=['TEKST'],
        wat="Maakt van een getal of een datum tekst, in precies de vorm die "
            "je wil.",
        schrijf='=TEKST(waarde;"vorm")',
        argumenten=[('waarde', 'het getal, de datum of het uur'),
                    ('"vorm"', 'hoe het eruit moet zien, tussen '
                               'aanhalingstekens')],
        uitleg=[
            'Dit is de belangrijkste fiche van deel 1, en de reden is Word.',
            'Een uur is in Excel een getal tussen 0 en 1, en een bedrag is '
            'een getal zonder euroteken. Wat je op je scherm ziet — 14:00 en '
            '€ 45,00 — is alleen de OPMAAK van de cel. Die opmaak gaat niet '
            'mee naar Word.',
            'Voeg je zo\'n cel samen, dan staat er in je brief 0,5833 of 45. '
            'Met TEKST zet je de vorm in de cel zelf, en dan komt ze wél mee.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['M4 = 14:00', '=TEKST(M4;"uu:mm")  geeft  14:00'],
                   ['N4 = 45', '=TEKST(N4;"€ #.##0,00")  geeft  € 45,00'],
                   ['B4 = 16/07/2027',
                    '=TEKST(B4;"d mmmm jjjj")  geeft  16 juli 2027']]),
        weten=['De vormcodes: uu:mm voor een uur, d/m/jjjj of d mmmm jjjj voor '
               'een datum, #.##0,00 voor een bedrag met twee cijfers achter '
               'de komma en een punt bij de duizenden.',
               'Let op: na TEKST is het TEKST. Je kan er niet meer mee '
               'rekenen. Wil je het nog optellen, hou dan de kolom met het '
               'echte getal ernaast staan.'],
        fout='Denken dat de celopmaak volstaat. Op je scherm klopt alles, en '
             'in de brief staat 0,5833333. De opmaak van een cel is niet '
             'hetzelfde als de inhoud.',
    ),
    # ============================================ deel 2 — Word
    dict(
        deel="Samenvoegen (Word)", naam="Wat afdruk samenvoegen is",
        functies=[],
        wat="Eén document plus één lijst wordt honderd documenten.",
        uitleg=[
            'Je hebt altijd drie dingen:',
            '1.  Het HOOFDDOCUMENT. Dat is je brief of je etiketvel. Daarin '
            'staat alles wat voor iedereen hetzelfde is, plus de plaatsen waar '
            'iets persoonlijks komt.',
            '2.  De GEGEVENSBRON. Dat is je Excellijst. Eén rij per persoon.',
            '3.  Het SAMENGEVOEGDE RESULTAAT. Dat maakt Word: één brief per '
            'rij.',
            'Het hoofddocument blijft bestaan en blijft aan de lijst hangen. '
            'Verandert er een adres, dan pas je de lijst aan en voeg je '
            'opnieuw samen. Je hoeft geen enkele brief te hertypen.',
        ],
        voorbeeld=dict(
            koppen=['Wat je maakt', 'Hoeveel'],
            rijen=[['hoofddocument (de brief)', '1'],
                   ['gegevensbron (de lijst)', '1 bestand, 24 rijen'],
                   ['resultaat', '24 brieven']]),
        weten=['Alles zit op het tabblad Verzendlijsten. In een Engelse Word '
               'heet dat Mailings.'],
        fout='De brief vierentwintig keer kopiëren en de namen met de hand '
             'aanpassen. Dat werkt, tot er een adres verandert.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="De lijst aan je document hangen",
        functies=[],
        wat="Word vertellen welke Excellijst het moet gebruiken.",
        stappen=[
            'Tabblad Verzendlijsten.',
            'Afdruk samenvoegen starten, en kies wat je maakt: Brieven of '
            'Etiketten.',
            'Adressen selecteren, dan Een bestaande lijst gebruiken.',
            'Zoek je Excelbestand en open het.',
            'Word vraagt welk WERKBLAD het moet gebruiken. Kies het juiste, en '
            'laat "De eerste rij bevat kolomnamen" aangevinkt staan.',
        ],
        uitleg=[
            'Vanaf nu kent Word al je kolomnamen. Je ziet er nog niets van: '
            'eerst moet je velden invoegen.',
            'Sluit je Excelbestand voor je het selecteert. Dat hoeft niet, '
            'maar het scheelt een hoop vreemde foutmeldingen.',
        ],
        weten=['Via Lijst met ontvangers bewerken zie je wat Word uit je '
               'lijst gelezen heeft. Loop dat één keer na: je ziet er meteen '
               'of er een kolom verkeerd ingelezen is.'],
        fout='Het verkeerde werkblad kiezen. Je krijgt dan de takentabel in '
             'plaats van de vrijwilligers, of een leeg blad.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="Samenvoegvelden invoegen",
        functies=[],
        wat="De plaatsen in je brief waar Word iets uit de lijst zet.",
        stappen=[
            'Zet je cursor waar het veld moet komen.',
            'Verzendlijsten, Samenvoegveld invoegen, en kies de kolom.',
            'Herhaal voor elk veld. Typ de spaties, komma\'s en punten er '
            'zelf tussen.',
        ],
        uitleg=[
            'In je document staat dan «Aanhef» met die punthaken erom. Die '
            'punthaken typ je NIET zelf — dan is het gewone tekst en gebeurt '
            'er niets.',
            'Een veld is niet hetzelfde als een woord. Je kan het selecteren, '
            'verwijderen en vet of cursief maken, maar je kan er geen letter '
            'uit halen.',
        ],
        voorbeeld=dict(
            koppen=['Wat je typt', 'Wat er na het samenvoegen staat'],
            rijen=[['«Aanhef»,', 'Beste Lotte,'],
                   ['«Adresregel» — «Woonplaats»',
                    'Kerkstraat 12 — 2000 Antwerpen']]),
        weten=['Er bestaat ook een kant-en-klaar Adresblok. Handig, maar het '
               'gokt welke kolom het adres is. Met losse velden weet je wat '
               'je krijgt.'],
        fout='De punthaken zelf typen. Het ziet er hetzelfde uit en het doet '
             'niets. Echte velden worden grijs als je erop klikt.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="Etiketten",
        functies=[],
        wat="Eén vel met evenveel etiketten als er op het blad passen.",
        stappen=[
            'Verzendlijsten, Afdruk samenvoegen starten, Etiketten.',
            'Kies de leverancier en het nummer van je etiketvellen. Staat '
            'jouw soort er niet bij, neem dan een formaat met hetzelfde '
            'aantal per blad.',
            'Hang je lijst eraan (zie de vorige fiche).',
            'Vul HET EERSTE etiket in met je samenvoegvelden.',
            'Klik dan op LABELS BIJWERKEN. Nu staat hetzelfde op alle '
            'etiketten.',
            'Voorbeeld van resultaten om te kijken, en Voltooien en '
            'samenvoegen om het vel te maken.',
        ],
        uitleg=[
            'Labels bijwerken is de stap die iedereen één keer overslaat. Doe '
            'je het niet, dan is alleen het eerste etiket gevuld en blijft de '
            'rest leeg.',
            'Op de andere etiketten zie je dan «Volgende record» staan. Dat '
            'hoort zo: dat veld zegt tegen Word dat het naar de volgende rij '
            'moet.',
        ],
        weten=['Komt er een rij te veel of te weinig? Het aantal etiketten op '
               'een blad staat vast. Wie meer adressen heeft dan er op één '
               'blad passen, krijgt gewoon een tweede blad.'],
        fout='Labels bijwerken vergeten, en dan denken dat de lijst niet '
             'gelezen is.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="Voorbeeld, en voltooien",
        functies=[],
        wat="Kijken wat eruit komt, en het dan echt maken.",
        stappen=[
            'Verzendlijsten, Voorbeeld van resultaten. In plaats van «Aanhef» '
            'zie je nu Beste Lotte.',
            'Met de pijltjes ernaast loop je door de records. Doe dat: kijk '
            'naar nummer 1, naar een nummer uit het midden en naar het '
            'laatste.',
            'Voltooien en samenvoegen, en kies: Afzonderlijke documenten '
            'bewerken (alles in één nieuw document), Documenten afdrukken, of '
            'E-mailberichten verzenden.',
        ],
        uitleg=[
            'Kies in de les altijd Afzonderlijke documenten bewerken. Dan '
            'krijg je één nieuw document met alle brieven achter elkaar, en '
            'kan je nakijken wat je gemaakt hebt zonder papier te verspillen.',
            'Dat nieuwe document heeft geen lijst meer achter zich. Het is '
            'gewone tekst — handig om in te dienen, maar pas je de lijst nog '
            'aan, dan moet je opnieuw samenvoegen.',
        ],
        weten=['Het samengevoegde document bewaar je onder een andere naam dan '
               'je hoofddocument, anders ben je je brief met de velden kwijt.'],
        fout='Het samengevoegde document bewaren en het hoofddocument '
             'weggooien. Dan moet je bij de volgende editie alles opnieuw '
             'opbouwen.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="Als…Dan…Anders",
        functies=[],
        wat="Een zin die er alleen staat als er iets waar is.",
        stappen=[
            'Zet je cursor waar de zin moet komen.',
            'Verzendlijsten, Regels, Als…Dan…Anders.',
            'Kies het veld, de vergelijking en de waarde.',
            'Typ bij "Deze tekst invoegen" de zin die er dan moet staan, en '
            'bij "Anders deze tekst invoegen" wat er in de andere gevallen '
            'komt — of laat dat leeg.',
        ],
        uitleg=[
            'Dit is de ALS van Excel, maar in Word. Je gebruikt het voor een '
            'zin die niet voor iedereen geldt.',
            'Je kan de vergelijking op elke kolom van je lijst doen. Heb je in '
            'Excel al een kolom gemaakt met ja of nee, dan is de regel hier '
            'eenvoudig: is Begeleiding gelijk aan ja.',
            'Je ziet de regel niet in je document staan; je ziet alleen het '
            'resultaat. Met Alt+F9 zie je het veld zelf.',
        ],
        voorbeeld=dict(
            koppen=['De regel', 'Wat er in de brief komt'],
            rijen=[['Begeleiding is gelijk aan ja',
                    'de extra zin, alleen bij wie nog geen 18 is'],
                   ['Bedrag is groter dan 1000',
                    'de zin over het grote pakket, alleen bij de grote '
                    'sponsors']]),
        weten=['Vergelijk je met een getal, let dan op: Word vergelijkt soms '
               'als tekst. Een ja-of-nee-kolom in Excel is daarom veiliger dan '
               'een vergelijking op een bedrag.'],
        fout='De zin eerst typen en dan de regel eromheen proberen te zetten. '
             'Het omgekeerde werkt: eerst de regel, de zin typ je in het '
             'venster.',
    ),
    dict(
        deel="Samenvoegen (Word)", naam="Ontvangers filteren en sorteren",
        functies=[],
        wat="Niet iedereen een brief, of niet in deze volgorde.",
        stappen=[
            'Verzendlijsten, Lijst met ontvangers bewerken.',
            'Vinkjes uitzetten doet het ook, maar voor meer dan tien rijen '
            'klik je op Filteren.',
            'Kies de kolom, de vergelijking en de waarde. Bijvoorbeeld: '
            'Podium is gelijk aan Main Stage.',
            'Op Sorteren kies je op welke kolom de brieven op elkaar volgen.',
        ],
        uitleg=[
            'Filteren verandert je Excellijst niet. Het zegt alleen welke '
            'rijen deze keer meegaan.',
            'Sorteren op postcode is geen schoonheidsfoutje: zo kan de post '
            'goedkoper, en bij etiketten houd je de bundels per gemeente bij '
            'elkaar.',
            'Zet het filter achteraf weer af, anders mist de volgende '
            'samenvoeging de helft van je ontvangers.',
        ],
        weten=['Je kan twee voorwaarden combineren met EN en OF. Met EN moeten '
               'ze allebei waar zijn, met OF volstaat er één.'],
        fout='Het filter laten staan en dan niet begrijpen waarom er maar zes '
             'brieven uit komen.',
    ),
    # ============================================ deel 3 — als het misgaat
    dict(
        deel="Als het misgaat", naam="De opmaak komt niet mee",
        functies=[],
        wat="In Word staat 0,5833 of 45 waar 14:00 of € 45,00 hoort.",
        uitleg=[
            'Dit overkomt iedereen, en het is geen fout van jou. Word neemt '
            'de WAARDE uit je cel over, niet de opmaak.',
            'Er zijn twee oplossingen, en de eerste is bijna altijd de beste.',
            'OPLOSSING 1 — in Excel. Maak een kolom met TEKST, zoals in fiche '
            '4. Dan staat de vorm in de cel zelf en komt ze mee. Je ziet in '
            'Excel meteen wat er in de brief zal staan.',
            'OPLOSSING 2 — in Word. Zet een opmaakschakelaar in het veld. '
            'Druk Alt+F9 om de velden te zien, typ de schakelaar erbij, en '
            'druk opnieuw Alt+F9.',
        ],
        voorbeeld=dict(
            koppen=['Wat je in het veld zet', 'Wat er dan staat'],
            rijen=[['{ MERGEFIELD Vergoeding \\# "€ #.##0,00" }', '€ 45,00'],
                   ['{ MERGEFIELD Startuur \\@ "uu:mm" }', '14:00']]),
        weten=['\\# is voor getallen, \\@ is voor datums en uren.',
               'Die accolades typ je niet met je toetsenbord; ze horen bij het '
               'veld en verschijnen met Alt+F9.',
               'Oplossing 2 is korter als je lijst van iemand anders komt en '
               'je er geen kolom bij mag zetten.'],
        fout='De celopmaak in Excel nog eens veranderen en verwachten dat het '
             'nu wel meekomt. Dat is precies wat niet werkt.',
    ),
    dict(
        deel="Als het misgaat", naam="De vijf klachten",
        functies=[],
        wat="Wat je ziet, waar het aan ligt, en wat je eraan doet.",
        voorbeeld=dict(
            koppen=['Wat je ziet', 'Wat eraan te doen'],
            rijen=[
                ['Alleen het eerste etiket is gevuld',
                 'Labels bijwerken vergeten. Verzendlijsten, Labels '
                 'bijwerken.'],
                ['«Aanhef» blijft gewoon staan',
                 'Je hebt de punthaken zelf getypt, of Voorbeeld van '
                 'resultaten staat af.'],
                ['Er staat 0,5833 of 45 in plaats van een uur of een bedrag',
                 'De opmaak komt niet mee. Zie de vorige fiche.'],
                ['Er komen te weinig brieven uit',
                 'Er staat nog een filter aan, of er staan vinkjes uit bij '
                 'Lijst met ontvangers bewerken.'],
                ['Word vindt je lijst niet meer',
                 'Je hebt het Excelbestand verplaatst of hernoemd. Hang de '
                 'lijst opnieuw aan je document.'],
            ]),
        uitleg=[
            'Loop dit lijstje af voor je je hand opsteekt. In negen van de '
            'tien gevallen staat je klacht erbij.',
        ],
        weten=['Een lege regel midden in je adres komt van een leeg veld. In '
               'de brieven waar dat veld leeg is, blijft die regel wit.'],
        fout='Opnieuw beginnen in plaats van zoeken waar het aan ligt. Je '
             'hoofddocument is bijna nooit kapot.',
    ),
]

if __name__ == '__main__':
    deel = None
    for i, f in enumerate(FICHES, 1):
        if f['deel'] != deel:
            deel = f['deel']
            print(f'\n{deel}')
        soort = 'formule' if f.get('schrijf') else (
            'stappen' if f.get('stappen') else 'uitleg')
        print(f'  {i:>2}. {f["naam"]:<36} {soort}')
    print(f'\n{len(FICHES)} fiches in {len(DELEN)} delen')
