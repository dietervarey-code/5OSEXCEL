# -*- coding: utf-8 -*-
"""De vijf detectivezaken.

Elke zaak staat los van de andere en duurt ongeveer 25 minuten. Opbouw:

* zes of zeven BASISFORMULES — die staan letterlijk in de stappen, want er is
  geen leerkracht om iets aan te vragen;
* precies één SLEUTELFORMULE met een functie binnen een functie — daarvan
  staat alleen de vorm, niet de inhoud. Dat is de uitdaging van de zaak;
* twee CONTROLEGETALLEN, zodat ze zelf weten of ze goed zitten;
* een lijstje 'Loop je vast?'.

Elke zaak heeft een ANDERE soort nesting. Dat is met opzet: vijf keer
hetzelfde trucje leert niets.
"""

ZAKEN = [
    dict(
        nr=1,
        titel='De verdwenen avonden',
        blad='1 Verdwenen avonden',
        duur='25 minuten',
        nesting='EN binnen ALS',
        dossier=[
            'Mevrouw Deleu zit tegenover je in het kantoor van het detectivebureau. Haar '
            'man Rudi werkt al zes weken bijna elke avond over, zegt hij. Ze gelooft hem '
            'niet meer.',
            'Je hebt twee dingen kunnen bemachtigen: het badgeoverzicht van zijn kantoor — '
            'daarop staat hoeveel minuten hij na vijf uur nog binnen was — en zijn '
            'bankafschrift met elke betaling van die avonden.',
            'Minder dan een half uur na vijf uur binnen blijven is geen overwerk. Dat is '
            'nog net je jas aantrekken. Wie zegt dat hij overwerkt en toch binnen het '
            'halfuur buiten staat, liegt.',
            'Zoek uit op welke avonden hij loog, en waar zijn geld die avonden naartoe '
            'ging.',
        ],
        gegeven=[
            ('B2', 'de grens: minder dan zoveel minuten is geen overwerk'),
            ('A5:A24', 'de datum van twintig avonden'),
            ('B5:B24', 'wat Rudi die avond gezegd heeft'),
            ('C5:C24', 'hoeveel minuten hij volgens de badge nog gebleven is'),
            ('D5:D24', 'wat hij die avond betaald heeft'),
            ('E5:E24', 'de code van de handelaar waar hij betaalde'),
            ('J4:K10', 'de handelaarslijst: code en naam — niet aanpassen'),
        ],
        maken=[
            dict(waar='F5:F24', wat='de naam van de handelaar',
                 formule='=VERT.ZOEKEN(E5;$J$5:$K$10;2;ONWAAR)',
                 stap='Klik F5 aan en typ de formule. Voer door tot F24.'),
            dict(waar='G5:G24', wat='LEUGEN of klopt', genest=True,
                 vorm='=ALS(EN(...;...);"LEUGEN";"klopt")',
                 hulp=[
                     'Er moeten twee dingen tegelijk waar zijn voor het een leugen is: hij '
                     'zei dat hij overwerkte, EN hij was binnen het halfuur buiten.',
                     'Het eerste stuk vergelijk je met tekst. Tekst zet je tussen '
                     'aanhalingstekens, en je gebruikt een isgelijkteken.',
                     'Het tweede stuk vergelijk je met de grens in B2. Die grens moet '
                     'blijven staan als je doorvoert, dus zet er dollartekens rond.',
                     'Bouw het in twee stappen op. Typ eerst in een lege cel, bijvoorbeeld '
                     'I2, alleen het EN-stuk: =EN(...;...). Staat er WAAR bij de avonden '
                     'waar je het verwacht? Dan schuif je dat stuk binnen de ALS en wis je '
                     'I2 weer.',
                 ],
                 stap='Voer door tot G24.'),
            dict(waar='C26', wat='het aantal avonden dat hij loog',
                 formule='=AANTAL.ALS(G5:G24;"LEUGEN")'),
            dict(waar='C27', wat='wat hij op die avonden samen uitgaf',
                 formule='=SOM.ALS(G5:G24;"LEUGEN";D5:D24)'),
            dict(waar='C28', wat='de code van de handelaar die op al die avonden terugkomt',
                 formule=None,
                 stap='Geen formule. Kijk in kolom F naar de avonden waar LEUGEN staat. '
                      'Staat daar telkens dezelfde handelaar? Typ dan zijn CODE (uit kolom '
                      'E) in C28.'),
            dict(waar='C29', wat='wat hij bij die ene handelaar samen uitgaf',
                 formule='=SOM.ALS(E5:E24;C28;D5:D24)'),
            dict(waar='C30', wat='wat hij in totaal uitgaf', formule='=SOM(D5:D24)'),
            dict(waar='C31', wat='het grootste bedrag van één avond',
                 formule='=MAX(D5:D24)'),
        ],
        opmaak=[
            'Koprij 4: vet met een achtergrondkleur.',
            'D5:D24 en C27:C31: notatie valuta.',
            'Voorwaardelijke opmaak op G5:G24: LEUGEN wordt rood.',
            'De handelaarslijst J4:K10: een lichte vulling en een rand eromheen.',
        ],
        proef='C27 en C29 moeten precies hetzelfde getal geven. Dat is je bewijs: elke euro '
              'van de leugenavonden ging naar diezelfde ene handelaar. Geven ze iets anders, '
              'dan heb je de verkeerde code in C28 gezet.',
        vraag='Op welke avonden loog Rudi, en waar was hij dan?',
        vastgelopen=[
            ('In kolom F staat #N/B.',
             'De dollartekens rond de handelaarslijst ontbreken, of je tabel begint niet bij '
             'J5. Klik F24 aan en lees de formulebalk: staat er nog $J$5:$K$10?'),
            ('In kolom G staat overal klopt.',
             'Je EN-stuk klopt niet. Zet het even apart in een lege cel en kijk wanneer er '
             'WAAR verschijnt. Let op: "overwerk" moet tussen aanhalingstekens, en C5 moet '
             'KLEINER zijn dan de grens, niet groter.'),
            ('C27 en C29 geven iets anders.',
             'Of je hebt de verkeerde code in C28, of je C29-formule kijkt in de verkeerde '
             'kolom. SOM.ALS zoekt in kolom E (de codes) en telt op uit kolom D (de '
             'bedragen).'),
        ],
        afloop='Rudi loog zes keer, telkens op een donderdag, en betaalde telkens 45 euro bij '
               'Dansschool Tango Nova. Hij nam in het geheim danslessen voor hun '
               'vijfentwintigste huwelijksverjaardag. De detective heeft mevrouw Deleu dus '
               'vooral een verrassing verklapt.',
    ),
    dict(
        nr=2,
        titel='De Mercedes van de Koning',
        blad='2 Mercedes',
        duur='25 minuten',
        nesting='MAX binnen VERT.ZOEKEN',
        dossier=[
            'De koninklijke Mercedes staat niet meer in de garage van het paleis. Niemand '
            'weet waar hij is. Het logboek van de wagen ligt er nog wel: elke rit staat '
            'erin, met de kilometerstand bij vertrek en bij aankomst.',
            'Eén probleem: de bladen van het logboek lagen door elkaar toen de politie ze '
            'vond. De ritten staan dus NIET op volgorde.',
            'Dat geeft niet. Een kilometerteller loopt maar één kant op. De rit met de '
            'hoogste kilometerstand bij aankomst is dus altijd de laatste rit geweest — '
            'waar die rit eindigde, staat de wagen nu.',
        ],
        gegeven=[
            ('A4:A19', 'de ritnummers'),
            ('B4:B19', 'de datum'),
            ('C4:C19', 'de chauffeur'),
            ('D4:D19', 'waar de rit begon'),
            ('E4:E19', 'de kilometerstand bij vertrek'),
            ('F4:F19', 'de kilometerstand bij aankomst'),
            ('G4:G19', 'waar de rit eindigde'),
            ('A22:A25', 'de vier chauffeurs — die gebruik je zo als criterium'),
        ],
        grafiek=dict(
            titel='Kilometerstand bij aankomst',
            vraag='Kijk eerst naar de grafiek op het werkblad. Welke staaf is de hoogste? '
                  'Bij welke rit hoort die? Schrijf je vermoeden op voor je begint te '
                  'rekenen — op het einde kijk je of je gelijk had.',
        ),
        maken=[
            dict(waar='H4:H19', wat='hoeveel kilometer die rit was',
                 formule='=F4-E4',
                 stap='Klik H4 aan en typ de formule. Voer door tot H19.'),
            dict(waar='B22:B25', wat='het aantal ritten per chauffeur',
                 formule='=AANTAL.ALS($C$4:$C$19;A22)',
                 stap='Klik B22 aan en typ de formule. Het bereik staat vast, A22 niet — '
                      'die moet meeschuiven. Voer door tot B25.'),
            dict(waar='C22:C25', wat='het aantal kilometer per chauffeur',
                 formule='=SOM.ALS($C$4:$C$19;A22;$H$4:$H$19)',
                 stap='Klik C22 aan en typ de formule. Voer door tot C25.'),
            dict(waar='C27', wat='het totaal gereden aantal kilometer',
                 formule='=SOM(H4:H19)'),
            dict(waar='C28', wat='de hoogste kilometerstand min de laagste',
                 formule='=MAX(F4:F19)-MIN(E4:E19)'),
            dict(waar='C29', wat='de langste rit', formule='=MAX(H4:H19)'),
            dict(waar='C30', wat='de gemiddelde rit', formule='=GEMIDDELDE(H4:H19)'),
            dict(waar='C31', wat='waar de wagen nu staat', genest=True,
                 vorm='=VERT.ZOEKEN(MAX(...);$F$4:$G$19;2;ONWAAR)',
                 hulp=[
                     'Je weet welke kilometerstand de hoogste is: dat geeft MAX je. Maar je '
                     'wil niet dat getal, je wil de BESTEMMING die erbij hoort.',
                     'VERT.ZOEKEN zoekt iets op in de eerste kolom van een tabel. Hier is '
                     'die tabel F4:G19: links de kilometerstanden, rechts de bestemmingen.',
                     'In plaats van zelf een getal in te typen, zet je de MAX op de plaats '
                     'waar normaal het zoekgetal staat. Dat is de hele truc.',
                     'Bouw het in twee stappen op. Typ eerst in een lege cel, bijvoorbeeld '
                     'I2, alleen =MAX(F4:F19). Schrijf dat getal op. Zet daarna de MAX '
                     'binnen de VERT.ZOEKEN en wis I2 weer.',
                 ]),
        ],
        opmaak=[
            'Koprij 3: vet met een achtergrondkleur.',
            'E4:F19 en H4:H19: duizendtalscheiding zonder cijfers na de komma.',
            'C30: één cijfer na de komma.',
            'Rand rond het chauffeursblokje A21:C25, en C31 vet met een opvallende kleur.',
        ],
        proef='C27 en C28 moeten precies hetzelfde getal geven. Een kilometerteller loopt '
              'maar één kant op: alle ritten samen moeten dus even veel zijn als de hoogste '
              'stand min de laagste. Geven ze iets anders, dan zit er een fout in kolom H.',
        vraag='Waar is de Mercedes het laatst gezien, en welke rit was dat?',
        vastgelopen=[
            ('C27 en C28 geven iets anders.',
             'Er zit een fout in kolom H. Klik H19 aan: staat er =F19-E19? Een rit waarbij '
             'je per ongeluk vertrek en aankomst omdraait, geeft een negatief getal.'),
            ('C31 geeft #N/B.',
             'Je tabel begint niet bij kolom F. VERT.ZOEKEN zoekt altijd in de EERSTE kolom '
             'van de tabel die je opgeeft, en de kilometerstanden staan in F. De tabel moet '
             'dus F4:G19 zijn, niet A4:G19.'),
            ('C31 geeft een getal in plaats van een plaatsnaam.',
             'Het derde stuk van VERT.ZOEKEN zegt welke kolom je terugkrijgt. Met 1 krijg '
             'je de kilometerstand zelf, met 2 de bestemming.'),
        ],
        afloop='De hoogste stand is 86041, en die hoort bij rit 16: van Hasselt naar Hoeve '
               'Ter Linden in Zoutleeuw, gereden door een chauffeur die in het logboek '
               '"onbekend" heet. De langste rit van de maand was die naar Luxemburg (420 '
               'km), maar die is een afleider: de wagen kwam gewoon terug. Op de hoeve bleek '
               'de Mercedes in een loods te staan, waar hij in het geheim gerestaureerd '
               'werd voor een jubileum.',
    ),
    dict(
        nr=3,
        titel='De museumroof',
        blad='3 Museumroof',
        duur='25 minuten',
        nesting='AANTAL.ALS binnen ALS',
        dossier=[
            'Vannacht is er ingebroken in het Stedelijk Museum. Een ruit achteraan, geen '
            'alarm, geen beelden: de camera stond al weken stuk.',
            'De conservator heeft vanmorgen alles geteld wat hij nog terugvond en die '
            'nummers op een lijstje gezet. Naast dat lijstje ligt de volledige catalogus '
            'van twintig stukken.',
            'Wat er weg is, is dus precies wat in de catalogus staat maar NIET op het '
            'lijstje van vanmorgen. Zoek uit welke stukken dat zijn, hoeveel ze waard zijn, '
            'en uit welke zaal ze komen.',
        ],
        gegeven=[
            ('A4:A23', 'de twintig catalogusnummers'),
            ('B4:B23', 'wat het stuk is'),
            ('C4:C23', 'de code van de zaal waar het hing of stond'),
            ('E4:E23', 'de geschatte waarde'),
            ('H4:H19', 'wat de conservator vanmorgen teruggevonden heeft — zestien nummers'),
            ('J4:K7', 'de zalenlijst: code en naam — niet aanpassen'),
        ],
        maken=[
            dict(waar='D4:D23', wat='de naam van de zaal',
                 formule='=VERT.ZOEKEN(C4;$J$4:$K$7;2;ONWAAR)',
                 stap='Klik D4 aan en typ de formule. Voer door tot D23.'),
            dict(waar='F4:F23', wat='GESTOLEN of aanwezig', genest=True,
                 vorm='=ALS(AANTAL.ALS(...;...)=0;"GESTOLEN";"aanwezig")',
                 hulp=[
                     'AANTAL.ALS telt hoe vaak iets voorkomt. Tel je hoe vaak het '
                     'catalogusnummer van deze rij voorkomt in het lijstje van vanmorgen, '
                     'dan krijg je 1 als het er nog is en 0 als het weg is.',
                     'Dat getal zet je binnen een ALS: is het 0, dan is het stuk GESTOLEN.',
                     'Het lijstje van vanmorgen staat in H4:H19. Dat bereik moet blijven '
                     'staan als je doorvoert, dus zet er dollartekens rond. Het nummer waar '
                     'je naar zoekt staat in A4 en moet juist WEL meeschuiven.',
                     'Bouw het in twee stappen op. Typ eerst in een lege cel, bijvoorbeeld '
                     'M2, alleen =AANTAL.ALS($H$4:$H$19;A4). Krijg je 1? Dan klopt het '
                     'binnenste stuk en mag het binnen de ALS.',
                 ],
                 stap='Voer door tot F23.'),
            dict(waar='C25', wat='het aantal gestolen stukken',
                 formule='=AANTAL.ALS(F4:F23;"GESTOLEN")'),
            dict(waar='C26', wat='de waarde van de buit',
                 formule='=SOM.ALS(F4:F23;"GESTOLEN";E4:E23)'),
            dict(waar='C27', wat='de waarde van de hele collectie',
                 formule='=SOM(E4:E23)'),
            dict(waar='C28', wat='het duurste stuk van het museum',
                 formule='=MAX(E4:E23)'),
            dict(waar='C29', wat='de gemiddelde waarde van een stuk',
                 formule='=GEMIDDELDE(E4:E23)'),
        ],
        opmaak=[
            'Koprij 3: vet met een achtergrondkleur.',
            'E4:E23 en C26:C29: duizendtalscheiding zonder cijfers na de komma.',
            'Voorwaardelijke opmaak op F4:F23: GESTOLEN wordt rood.',
            'De twee lijstjes rechts (H en J:K): een lichte vulling en een rand eromheen.',
        ],
        proef='C25 moet 4 geven. De catalogus telt twintig stukken en de conservator vond er '
              'zestien terug: er kunnen er dus niet meer en niet minder dan vier weg zijn. '
              'Staat er iets anders, dan loopt een van je twee bereiken niet ver genoeg door.',
        vraag='Welke vier stukken zijn gestolen, voor hoeveel samen, en wat valt er op aan '
              'de zaal waar ze vandaan komen?',
        vastgelopen=[
            ('In kolom F staat overal GESTOLEN.',
             'Je AANTAL.ALS kijkt in het verkeerde bereik. Het lijstje van vanmorgen staat '
             'in kolom H, niet in kolom A. Zet het apart in een lege cel en kijk wat je '
             'krijgt.'),
            ('In kolom F staat overal aanwezig.',
             'Waarschijnlijk vergelijk je met 1 in plaats van met 0, of je hebt > gebruikt '
             'waar = hoort. Weg is weg: dan telt AANTAL.ALS nul keer.'),
            ('Vanaf rij 10 klopt er niets meer.',
             'De dollartekens rond $H$4:$H$19 ontbreken, waardoor het lijstje mee naar '
             'beneden schoof. Klik F23 aan en lees de formulebalk.'),
        ],
        afloop='Weg zijn K-109, K-110, K-112 en K-114, samen 87 200 euro. Alle vier komen ze '
               'uit de Zilverkamer, en alle vier zijn het kleine stukken die in een rugzak '
               'passen. Het duurste werk van het museum — een schilderij van 210 000 euro — '
               'hing twee zalen verder en is blijven hangen. De dief wist precies wat hij '
               'kwam halen en wat hij kwijt kon raken.',
    ),
    dict(
        nr=4,
        titel='Het gelekte examen',
        blad='4 Gelekt examen',
        duur='25 minuten',
        nesting='SOM.ALS binnen ALS',
        dossier=[
            'Het examen wiskunde van 6TW stond gisterennacht om kwart over twaalf op '
            'internet. Vanmorgen om acht uur wist de halve school het.',
            'De ICT-coördinator heeft het logbestand van de server uitgedraaid: elke keer '
            'dat iemand de map Examens opende in de drie dagen ervoor, met hoeveel '
            'bestanden erbij.',
            'Acht mensen hebben die map geopend. Zeven van hen hebben daar een reden voor. '
            'De school rekent erop dat wie samen meer dan twintig bestanden opent, iets '
            'anders aan het doen is dan een les voorbereiden.',
            'Let op: iemand die vaak inlogt, is niet verdacht. Het gaat om het AANTAL '
            'BESTANDEN dat hij samen opende.',
        ],
        gegeven=[
            ('B2', 'de grens: vanaf zoveel bestanden samen wordt het verdacht'),
            ('A5:A26', 'de tweeëntwintig logregels'),
            ('B5:B26', 'de code van wie inlogde'),
            ('C5:C26', 'de dag'),
            ('D5:D26', 'het tijdstip'),
            ('E5:E26', 'hoeveel bestanden er die keer geopend werden'),
            ('A29:A36', 'de acht gebruikerscodes — die gebruik je zo als criterium'),
            ('H4:J12', 'de gebruikerslijst: code, naam en functie — niet aanpassen'),
        ],
        maken=[
            dict(waar='B29:B36', wat='de naam van de gebruiker',
                 formule='=VERT.ZOEKEN(A29;$H$5:$J$12;2;ONWAAR)',
                 stap='Klik B29 aan en typ de formule. Voer door tot B36.'),
            dict(waar='C29:C36', wat='zijn functie op school',
                 formule='=VERT.ZOEKEN(A29;$H$5:$J$12;3;ONWAAR)',
                 stap='Klik C29 aan en typ dezelfde formule met een 3 in plaats van een 2. '
                      'Voer door tot C36.'),
            dict(waar='D29:D36', wat='hoe vaak die persoon inlogde',
                 formule='=AANTAL.ALS($B$5:$B$26;A29)',
                 stap='Klik D29 aan en typ de formule. Voer door tot D36.'),
            dict(waar='E29:E36', wat='VERDACHT of vrij', genest=True,
                 vorm='=ALS(SOM.ALS(...;...;...)>$B$2;"VERDACHT";"vrij")',
                 hulp=[
                     'Je zou eerst in een aparte kolom kunnen uitrekenen hoeveel bestanden '
                     'elke persoon samen opende, en die kolom daarna met de grens '
                     'vergelijken. Dat mag, maar het hoeft niet: je mag de SOM.ALS meteen '
                     'BINNEN de ALS zetten. Dat is precies wat een geneste functie is.',
                     'De SOM.ALS kijkt in de kolom met de codes (B), zoekt de code van deze '
                     'rij (A29), en telt de bestanden op uit kolom E.',
                     'Allebei de bereiken moeten blijven staan als je doorvoert, dus '
                     'dollartekens. A29 juist niet.',
                     'Bouw het in twee stappen op. Typ eerst in een lege cel, bijvoorbeeld '
                     'G2, alleen de SOM.ALS. Krijg je een getal tussen 5 en 25? Dan klopt '
                     'het binnenste stuk en mag het binnen de ALS.',
                 ],
                 stap='Voer door tot E36.'),
            dict(waar='C38', wat='hoeveel bestanden er in totaal geopend werden',
                 formule='=SOM(E5:E26)'),
            dict(waar='C39', wat='het grootste aantal bestanden in één keer',
                 formule='=MAX(E5:E26)'),
            dict(waar='C40', wat='hoeveel mensen er verdacht zijn',
                 formule='=AANTAL.ALS(E29:E36;"VERDACHT")'),
        ],
        opmaak=[
            'Koprij 4 en koprij 28: vet met een achtergrondkleur.',
            'Voorwaardelijke opmaak op E29:E36: VERDACHT wordt rood en vet.',
            'Voorwaardelijke opmaak op D5:D26: elk tijdstip na 22:00 krijgt een kleur '
            '(gebruik Markeringsregels › Tekst die bevat › 23:).',
            'Rand rond het gebruikersblokje A28:E36, en de gebruikerslijst H4:J12 een '
            'lichte vulling.',
        ],
        proef='C40 moet precies 1 geven. Staat er 0, dan is je grens of je SOM.ALS fout. '
              'Staat er meer dan 1, dan tel je iets anders op dan bestanden — kijk of het '
              'laatste bereik van je SOM.ALS wel naar kolom E wijst.',
        vraag='Wie heeft het examen gelekt, en wat zie je aan zijn tijdstippen?',
        vastgelopen=[
            ('E29 geeft #WAARDE! of een vreemde melding.',
             'Je haakjes kloppen niet. De SOM.ALS heeft zijn eigen paar haakjes BINNEN die '
             'van de ALS. Excel kleurt de haakjes per paar — gebruik die kleuren.'),
            ('Iedereen is verdacht, of niemand.',
             'Zet de SOM.ALS even apart in een lege cel en voer hem door. Krijg je acht '
             'verschillende getallen? Zo niet, dan ontbreken de dollartekens rond de twee '
             'bereiken.'),
            ('De namen in kolom B kloppen niet bij de codes.',
             'Je tabel begint op de verkeerde rij. De gebruikerslijst loopt van H5 tot J12; '
             'rij 4 is de koprij en hoort er niet bij.'),
        ],
        afloop='Jonas Debbaut (G-08, leerling 6TW) opende 23 bestanden, net boven de grens '
               'van twintig. Negen daarvan om 23:40 en twaalf om 23:52 — en om 00:15 stond '
               'het examen online. De ICT-coördinator zit met 19 bestanden vlak onder de '
               'grens; die is er dus niet uit te halen met deze telling alleen. Een goede '
               'gelegenheid om te vragen of een grens van twintig wel de juiste grens is.',
    ),
    dict(
        nr=5,
        titel='De sabotage in de chocoladefabriek',
        blad='5 Chocolade',
        duur='25 minuten',
        nesting='VERT.ZOEKEN binnen ALS',
        dossier=[
            'Chocoladefabriek Praliné Dumont moest deze week vierentwintig batches pralines '
            'leveren. Bij een deel ervan is zoveel afgekeurd dat de hele levering in het '
            'gedrang komt.',
            'De directie gelooft niet in toeval. Zes machines, drie ploegen, en toch loopt '
            'het maar bij een paar batches mis. Iemand heeft aan een machine gezeten.',
            'Je hebt de productiecijfers van alle batches en het onderhoudsregister, waarin '
            'staat welke technicus elke machine het laatst heeft nagekeken.',
            'Normaal wordt er ergens tussen de vier en de tien procent afgekeurd. Alles '
            'boven de vijftien procent is niet normaal meer.',
        ],
        gegeven=[
            ('B2', 'de grens: vanaf zoveel afkeur is een batch niet normaal meer'),
            ('A5:A28', 'de vierentwintig batchnummers'),
            ('B5:B28', 'de machine waarop de batch gemaakt werd'),
            ('C5:C28', 'de ploeg die aan het werk was'),
            ('D5:D28', 'hoeveel pralines er gemaakt werden'),
            ('E5:E28', 'hoeveel er afgekeurd werden'),
            ('J4:L10', 'het onderhoudsregister: machine, naam en wie ze het laatst '
                       'nakeek — niet aanpassen'),
        ],
        grafiek=dict(
            titel='Afgekeurde pralines per batch',
            vraag='Kijk eerst naar de grafiek op het werkblad. Hoeveel staven springen er '
                  'duidelijk boven de rest uit? Schrijf de batchnummers op voor je begint '
                  'te rekenen.',
        ),
        maken=[
            dict(waar='F5:F28', wat='hoeveel procent er afgekeurd werd',
                 formule='=AFRONDEN(E5/D5;3)',
                 stap='Klik F5 aan en typ de formule. Voer door tot F28. Geef kolom F '
                      'daarna de notatie percentage met één cijfer na de komma: er staat nu '
                      '23,6 % in plaats van 0,236.'),
            dict(waar='G5:G28', wat='bij een slechte batch: wie die machine het laatst '
                                    'nakeek', genest=True,
                 vorm='=ALS(F5>$B$2;VERT.ZOEKEN(...;$J$5:$L$10;3;ONWAAR);"-")',
                 hulp=[
                     'Deze keer zit de geneste functie niet in de VOORWAARDE van de ALS, '
                     'maar in het antwoord. Lees de formule als: is deze batch slecht? Zoek '
                     'dan op wie die machine nakeek. Zo niet, zet dan een streepje.',
                     'De VERT.ZOEKEN zoekt de machinecode van deze rij op in het '
                     'onderhoudsregister, en geeft de derde kolom terug: de naam van de '
                     'technicus.',
                     'Het register moet blijven staan als je doorvoert, dus dollartekens. '
                     'De machinecode die je opzoekt staat in kolom B en moet juist wel '
                     'meeschuiven.',
                     'Bouw het in twee stappen op. Typ eerst in een lege cel, bijvoorbeeld '
                     'I2, alleen de VERT.ZOEKEN. Krijg je een naam? Dan klopt het binnenste '
                     'stuk en mag het binnen de ALS.',
                 ],
                 stap='Voer door tot G28.'),
            dict(waar='D30', wat='hoeveel pralines er in totaal gemaakt werden',
                 formule='=SOM(D5:D28)'),
            dict(waar='D31', wat='hoeveel er in totaal afgekeurd werden',
                 formule='=SOM(E5:E28)'),
            dict(waar='D32', wat='het hoogste afkeurpercentage',
                 formule='=MAX(F5:F28)'),
            dict(waar='D33', wat='het gemiddelde afkeurpercentage',
                 formule='=GEMIDDELDE(F5:F28)'),
            dict(waar='D34', wat='de naam die in kolom G blijft terugkomen', formule=None,
                 stap='Geen formule. Kijk in kolom G: op de slechte batches staat telkens '
                      'een naam. Komt daar altijd dezelfde naam? Typ die dan in D34, exact '
                      'zoals hij in kolom G staat.'),
            dict(waar='D35', wat='hoeveel slechte batches op zijn naam staan',
                 formule='=AANTAL.ALS(G5:G28;D34)'),
        ],
        opmaak=[
            'Koprij 4: vet met een achtergrondkleur.',
            'F5:F28, B2 en D32:D33: notatie percentage met één cijfer na de komma.',
            'D5:E28: duizendtalscheiding zonder cijfers na de komma.',
            'Voorwaardelijke opmaak op F5:F28: alles boven het gemiddelde krijgt een kleur.',
            'Het onderhoudsregister J4:L10: een lichte vulling en een rand eromheen.',
        ],
        proef='D35 moet hetzelfde aantal geven als het aantal staven dat in de grafiek '
              'boven de rest uitsprong. Klopt dat, dan heb je alle slechte batches te '
              'pakken en komen ze allemaal bij dezelfde technicus uit.',
        vraag='Wie heeft aan de machines gezeten, en om welke machines gaat het?',
        vastgelopen=[
            ('In kolom G staat overal een streepje.',
             'Je vergelijkt met de verkeerde kant op, of met de verkeerde cel. Het moet F5 '
             'GROTER dan $B$2 zijn. Kijk ook of B2 echt 15 % bevat en niet 15.'),
            ('In kolom G staan machinenamen in plaats van namen van technici.',
             'Het derde stuk van VERT.ZOEKEN zegt welke kolom je terugkrijgt. Met 2 krijg '
             'je de machine, met 3 de technicus.'),
            ('D35 geeft 0.',
             'De naam in D34 is niet exact dezelfde als in kolom G. Kopieer hem liever: '
             'klik een cel in kolom G aan waar een naam staat, kopieer de INHOUD en plak '
             'die in D34 als waarde. Of typ hem over, met dezelfde hoofdletter.'),
        ],
        afloop='Vijf batches zitten boven de vijftien procent: B-02, B-08, B-11, B-17 en '
               'B-20. Ze komen van twee machines — Tempereermachine 2 en de Koeltunnel — en '
               'die zijn allebei het laatst nagekeken door technicus Vercammen. De drie '
               'ploegen zijn niet schuldig: de slechte batches zijn netjes over ploeg A, B '
               'en C verdeeld. Dat is de controle die de zaak sluit — het ligt aan de '
               'machine, niet aan de mensen die eraan stonden.',
    ),
]
