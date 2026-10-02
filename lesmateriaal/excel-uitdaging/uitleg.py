# -*- coding: utf-8 -*-
"""Nieuw gereedschap voor de uitdagingsopdracht.

Dezelfde twee regels als bij de functiefiches van de basisbundel:

1. Een kaart leert de functie gebruiken. Ze geeft NOOIT de oplossing van de
   opdracht. De voorbeelden spelen in een eigen wereldje — een rapport, een
   fruithandel, een uurrooster — met andere cellen en andere cijfers dan in
   het startbestand. controleer.py bewaakt dat.
2. Een kaart staat op zichzelf. Wie vastloopt, pakt de kaart en kan verder.

De tien functies van de basisbundel staan hier NIET in. Die kennen ze al; de
fiches daarvan blijven gelden.
"""

# --------------------------------------------------------------------------
#  De voorbeeldwereldjes. Bewust ver van de opdracht.
# --------------------------------------------------------------------------

RAPPORT = [
    ['Leerling', 'Punten', 'Vermelding', '', 'Vanaf', 'Vermelding'],
    ['Amir', 72, 'goed', '', 0, 'onvoldoende'],
    ['Bo', 48, 'onvoldoende', '', 50, 'voldoende'],
    ['Cis', 85, 'zeer goed', '', 65, 'goed'],
    ['Dina', 50, 'voldoende', '', 80, 'zeer goed'],
]
KOL_RAPPORT = [('A', 85), ('B', 65), ('C', 105), ('D', 24), ('E', 55), ('F', 100)]

FRUIT = [
    ['Datum', 'Soort', 'Winkel', 'Kilo'],
    ['02/09', 'appel', 'Gent', 120],
    ['02/09', 'peer', 'Gent', 45],
    ['03/09', 'appel', 'Brugge', 80],
    ['03/09', 'appel', 'Gent', 95],
    ['04/09', 'peer', 'Brugge', 60],
]
KOL_FRUIT = [('A', 115), ('B', 70), ('C', 70), ('D', 60)]

PUNTEN = [
    ['Leerling', 'Punten'],
    ['Amir', 72],
    ['Bo', 48],
    ['Cis', 85],
    ['Dina', 50],
]
KOL_PUNTEN = [('A', 120), ('B', 70)]


# --------------------------------------------------------------------------
#  De kaarten
# --------------------------------------------------------------------------
KAARTEN = [
    dict(
        naam='VERT.ZOEKEN met WAAR — benaderend zoeken',
        wat='Zoekt niet de exacte waarde, maar de hoogste drempel die er nog onder zit. '
            'Daarmee lees je een staffel of een tarieventabel uit.',
        schrijf='=VERT.ZOEKEN(wat;tabel;kolom;WAAR)',
        argumenten=[
            ('wat', 'het getal waarvoor je de schijf zoekt, bijvoorbeeld een aantal'),
            ('tabel', 'de drempeltabel. De eerste kolom bevat de ONDERgrenzen'),
            ('kolom', 'de hoeveelste kolom van die tabel je wil terugkrijgen'),
            ('WAAR', 'zoek benaderend. ONWAAR zou exact zoeken en hier #N/B geven'),
        ],
        uitleg=[
            'Je kent VERT.ZOEKEN al met ONWAAR: dan moet de waarde exact in de tabel staan. '
            'Een code als M-03 staat er letterlijk in, dus dat werkt.',
            'Een aantal staat er niet letterlijk in. In een staffel staat alleen 0, 50, 65 '
            'en 80, maar je zoekt 72. Met WAAR pakt Excel de laatste drempel die nog onder '
            '72 ligt — dat is 65 — en geeft de rij daarvan terug.',
            'Eén harde voorwaarde: de eerste kolom van de tabel moet van klein naar groot '
            'gesorteerd staan. Anders klopt het antwoord niet, zonder enige foutmelding.',
        ],
        beelden=[
            dict(bestand='benaderend-1',
                 onderschrift='72 punten staat niet in de tabel. Met WAAR pakt Excel de '
                              'drempel 65 en geeft "goed". Dina heeft precies 50, de drempel '
                              'zelf, en krijgt "voldoende".',
                 kolommen=KOL_RAPPORT, rijen=RAPPORT,
                 formule='=VERT.ZOEKEN(B2;$E$2:$F$5;2;WAAR)', geselecteerd='C2',
                 gemarkeerd=('E4', 'F4'), rechts=('B', 'E'), vet_rij=1),
        ],
        varianten=[
            ('=VERT.ZOEKEN(B2;$E$2:$F$5;2;WAAR)', 'benaderend: pakt de drempel eronder'),
            ('=VERT.ZOEKEN(B2;$E$2:$F$5;2;ONWAAR)', 'exact: geeft #N/B zodra 72 er niet '
                                                    'letterlijk staat'),
            ('=VERT.ZOEKEN(B2;$E$2:$F$5;2)', 'laat je het laatste argument weg, dan neemt '
                                             'Excel WAAR. Schrijf het toch, dan weet je wat '
                                             'je doet'),
        ],
        weten=[
            'De eerste kolom bevat ondergrenzen, geen bovengrenzen. Staat er 50, dan geldt '
            'die rij vanaf 50 tot net onder de volgende drempel.',
            'Begin je staffel bij het laagst mogelijke getal. Zoek je 3 en begint de tabel '
            'bij 5, dan krijg je #N/B.',
            'Zet de tabel vast met dollartekens voordat je doorvoert. Precies zoals bij '
            'het exacte zoeken.',
        ],
        fout='De tabel niet gesorteerd zetten. Excel gaat ervan uit dat de eerste kolom '
             'oploopt en stopt bij de eerste drempel die te groot lijkt. Je krijgt dan een '
             'antwoord dat er plausibel uitziet maar fout is — en géén foutmelding.',
    ),
    dict(
        naam='SOMMEN.ALS — optellen met meer dan één voorwaarde',
        wat='Telt bedragen op die aan twee (of meer) voorwaarden tegelijk voldoen.',
        schrijf='=SOMMEN.ALS(optelbereik;bereik1;criterium1;bereik2;criterium2)',
        argumenten=[
            ('optelbereik', 'de getallen die je wil optellen'),
            ('bereik1 / criterium1', 'waar je kijkt, en wat er moet staan'),
            ('bereik2 / criterium2', 'de tweede voorwaarde. Je mag er meer toevoegen'),
        ],
        uitleg=[
            'SOM.ALS kende je al: één voorwaarde. SOMMEN.ALS doet hetzelfde met meerdere '
            'voorwaarden, en alleen de rijen die aan ALLE voorwaarden voldoen tellen mee.',
            'Let op de volgorde, want die is anders dan bij SOM.ALS: bij SOMMEN.ALS komt '
            'het optelbereik EERST. Dat is de fout die iedereen één keer maakt.',
        ],
        beelden=[
            dict(bestand='sommenals-1',
                 onderschrift='Alleen de rijen met appel én Gent tellen mee: 120 en 95. '
                              'De rij met peer in Gent en die met appel in Brugge vallen af.',
                 kolommen=KOL_FRUIT,
                 rijen=FRUIT + [['', '', '', ''], ['appel in Gent', '', '', 215]],
                 formule='=SOMMEN.ALS(D2:D6;B2:B6;"appel";C2:C6;"Gent")',
                 geselecteerd='D8', gemarkeerd=('D2', 'D5'), rechts=('D',), vet_rij=1),
        ],
        varianten=[
            ('=SOM.ALS(B2:B6;"appel";D2:D6)', 'één voorwaarde: bereik eerst, optelbereik achteraan'),
            ('=SOMMEN.ALS(D2:D6;B2:B6;"appel")', 'dezelfde som, maar met het optelbereik vooraan'),
            ('=SOMMEN.ALS(D2:D6;B2:B6;"appel";D2:D6;">=100")',
             'een voorwaarde mag ook over het optelbereik zelf gaan'),
            ('=SOMMEN.ALS(D2:D6;C2:C6;"Gent";D2:D6;">50")', 'Gent én meer dan 50 kilo'),
        ],
        weten=[
            'Alle bereiken moeten even hoog zijn. D2:D6 en B2:B6 wel, D2:D6 en B2:B7 niet.',
            'Een vergelijking als criterium staat tussen aanhalingstekens: ">=100".',
            'Een criterium mag ook uit een cel komen: dan typ je gewoon A20 in plaats van '
            '"Gent", en kun je de formule doorvoeren.',
            'Nul als antwoord betekent bijna altijd dat geen enkele rij aan alle '
            'voorwaarden voldoet. Haal er dan één voorwaarde af om te zien welke knelt.',
        ],
        fout='De volgorde van SOM.ALS gebruiken. =SOMMEN.ALS(B2:B6;"appel";D2:D6) telt de '
             'woorden in kolom B op in plaats van de kilo in kolom D. Je krijgt 0 of een '
             'onzinnig getal.',
    ),
    dict(
        naam='AANTALLEN.ALS — tellen met meer dan één voorwaarde',
        wat='Telt hoeveel rijen aan twee (of meer) voorwaarden tegelijk voldoen.',
        schrijf='=AANTALLEN.ALS(bereik1;criterium1;bereik2;criterium2)',
        argumenten=[
            ('bereik1 / criterium1', 'waar je kijkt, en wat er moet staan'),
            ('bereik2 / criterium2', 'de tweede voorwaarde'),
        ],
        uitleg=[
            'Dit is AANTAL.ALS met meer voorwaarden. Er is geen optelbereik, want je telt '
            'rijen en geen bedragen — dus begint de formule hier gewoon met het eerste '
            'bereik.',
            'Een rij telt mee als ze aan ALLE voorwaarden voldoet. Eén voorwaarde die niet '
            'klopt, en de rij valt af.',
        ],
        beelden=[
            dict(bestand='aantallenals-1',
                 onderschrift='Twee leveringen zijn appel én Gent. Het antwoord is dus 2 — '
                              'het aantal rijen, niet het aantal kilo.',
                 kolommen=KOL_FRUIT,
                 rijen=FRUIT + [['', '', '', ''], ['appel in Gent', '', '', 2]],
                 formule='=AANTALLEN.ALS(B2:B6;"appel";C2:C6;"Gent")',
                 geselecteerd='D8', gemarkeerd=('B2', 'B5'), rechts=('D',), vet_rij=1),
        ],
        varianten=[
            ('=AANTAL.ALS(B2:B6;"appel")', 'één voorwaarde'),
            ('=AANTALLEN.ALS(B2:B6;"appel";C2:C6;"Gent")', 'twee voorwaarden'),
            ('=AANTALLEN.ALS(C2:C6;"Gent";D2:D6;">=100")', 'Gent én minstens 100 kilo'),
            ('=AANTALLEN.ALS(B2:B6;"appel";D2:D6;"<100")', 'appel én minder dan 100 kilo'),
        ],
        weten=[
            'Geen optelbereik. Wie er toch een vooraan zet, krijgt een foutmelding over het '
            'aantal argumenten.',
            'Het antwoord is altijd een aantal rijen: een rond getal, nooit een bedrag.',
            'Tekst vergelijken gaat zonder onderscheid tussen hoofd- en kleine letters: '
            '"gent" vindt ook "Gent".',
        ],
        fout='SOMMEN.ALS en AANTALLEN.ALS verwisselen. Krijg je een groot getal waar een '
             'klein aantal hoort te staan, dan tel je bedragen op in plaats van rijen.',
    ),
    dict(
        naam='GEMIDDELDE.ALS — het gemiddelde van een deel',
        wat='Berekent het gemiddelde van alleen die rijen die aan een voorwaarde voldoen.',
        schrijf='=GEMIDDELDE.ALS(bereik;criterium;gemiddeldebereik)',
        argumenten=[
            ('bereik', 'waar je de voorwaarde toetst'),
            ('criterium', 'wat er in dat bereik moet staan'),
            ('gemiddeldebereik', 'de getallen waarvan je het gemiddelde wil'),
        ],
        uitleg=[
            'De volgorde is die van SOM.ALS: eerst waar je kijkt, dan wat er moet staan, '
            'dan waarvan je het gemiddelde neemt.',
            'Staat het laatste bereik er niet, dan neemt Excel het gemiddelde van het '
            'eerste bereik zelf. Dat is handig als voorwaarde en getallen in dezelfde '
            'kolom staan.',
        ],
        beelden=[
            dict(bestand='gemiddeldeals-1',
                 onderschrift='Alleen de drie appelleveringen tellen mee: 120, 80 en 95. '
                              'Samen 295, gedeeld door 3 is 98,33.',
                 kolommen=KOL_FRUIT,
                 rijen=FRUIT + [['', '', '', ''], ['gemiddelde appel', '', '', '98,33']],
                 formule='=GEMIDDELDE.ALS(B2:B6;"appel";D2:D6)',
                 geselecteerd='D8', gemarkeerd=('D2', 'D4', 'D5'), rechts=('D',), vet_rij=1),
        ],
        varianten=[
            ('=GEMIDDELDE.ALS(B2:B6;"appel";D2:D6)', 'gemiddeld aantal kilo per appellevering'),
            ('=GEMIDDELDE.ALS(D2:D6;">=80")', 'gemiddelde van alle leveringen vanaf 80 kilo'),
            ('=GEMIDDELDEN.ALS(D2:D6;B2:B6;"appel";C2:C6;"Gent")',
             'meer dan één voorwaarde: dan heet hij GEMIDDELDEN.ALS en komt het '
             'gemiddeldebereik vooraan'),
        ],
        weten=[
            'Een gemiddelde van niets geeft #DEEL/0!. Dat betekent dat geen enkele rij aan '
            'de voorwaarde voldoet — meestal een typfout in het criterium.',
            'Lege cellen tellen niet mee in het gemiddelde. Een cel met 0 wél. Dat maakt '
            'verschil.',
            'Rond het antwoord zelf af met AFRONDEN als je ermee verder rekent. Een '
            'getalnotatie toont wel twee cijfers, maar rekent met alles erachter.',
        ],
        fout='De volgorde van SOMMEN.ALS gebruiken en het gemiddeldebereik vooraan zetten. '
             'GEMIDDELDE.ALS begint met het bereik waarin je zoekt, net als SOM.ALS.',
    ),
    dict(
        naam='EN en OF binnen ALS',
        wat='Laat een ALS pas beslissen als meerdere voorwaarden tegelijk kloppen (EN), of '
            'als er minstens één klopt (OF).',
        schrijf='=ALS(EN(voorwaarde1;voorwaarde2);danwel;anders)',
        argumenten=[
            ('EN(...)', 'WAAR als álle voorwaarden kloppen'),
            ('OF(...)', 'WAAR als minstens één voorwaarde klopt'),
            ('danwel / anders', 'wat er moet komen in beide gevallen'),
        ],
        uitleg=[
            'Een gewone ALS toetst één voorwaarde. Wil je er twee, dan zet je EN of OF op '
            'de plaats van die voorwaarde.',
            'EN en OF geven zelf alleen WAAR of ONWAAR. Ze zijn op zichzelf zelden nuttig: '
            'je gebruikt ze bijna altijd binnen een ALS.',
            'Je mag er zoveel voorwaarden in zetten als je wil, gescheiden door puntkomma\'s.',
        ],
        beelden=[
            dict(bestand='alsen-1',
                 onderschrift='Geslaagd vraagt twee dingen tegelijk: minstens 50 punten én '
                              'minstens 80 % aanwezigheid. Bo haalt de punten niet, Cis de '
                              'aanwezigheid niet.',
                 kolommen=[('A', 85), ('B', 65), ('C', 85), ('D', 90)],
                 rijen=[['Leerling', 'Punten', 'Aanwezig', 'Geslaagd?'],
                        ['Amir', 72, '92 %', 'ja'],
                        ['Bo', 48, '95 %', 'nee'],
                        ['Cis', 85, '64 %', 'nee'],
                        ['Dina', 50, '88 %', 'ja']],
                 formule='=ALS(EN(B2>=50;C2>=0,8);"ja";"nee")',
                 geselecteerd='D2', rechts=('B', 'C'), vet_rij=1),
        ],
        varianten=[
            ('=ALS(EN(B2>=50;C2>=0,8);"ja";"nee")', 'beide voorwaarden moeten kloppen'),
            ('=ALS(OF(B2>=50;C2>=0,9);"ja";"nee")', 'één van de twee volstaat'),
            ('=ALS(EN(B2>=50;C2>=0,8;D2="aanwezig");"ja";"nee")', 'drie voorwaarden'),
            ('=EN(B2>=50;C2>=0,8)', 'zonder ALS: geeft WAAR of ONWAAR'),
        ],
        weten=[
            'Lees de formule van binnen naar buiten: eerst wat EN oplevert, dan wat ALS '
            'ermee doet.',
            'Tekst vergelijk je met een isgelijkteken en aanhalingstekens: C2="zwart".',
            'Vergelijk een tijd met een cel waarin die tijd staat, niet met een stukje '
            'getypte tekst. "22:30" tussen aanhalingstekens is tekst en geen tijd.',
            'Hoe meer voorwaarden, hoe belangrijker het is om één voorwaarde tegelijk toe '
            'te voegen. Werkt de formule met twee, zet er dan een derde bij.',
        ],
        fout='Haakjes kwijtraken. EN heeft zijn eigen paar haakjes BINNEN die van ALS. '
             'Excel kleurt de haakjes per paar — gebruik die kleuren.',
    ),
    dict(
        naam='Geneste functies — een functie binnen een functie',
        wat='Het antwoord van de ene functie meteen gebruiken als argument van de andere.',
        schrijf='=BUITEN(BINNEN(...);...)',
        argumenten=[
            ('BINNEN(...)', 'wordt eerst uitgerekend'),
            ('BUITEN(...)', 'werkt verder met dat resultaat'),
        ],
        uitleg=[
            'In de basisbundel was nesten verboden, zodat je per formule één ding kon '
            'controleren. Hier mag het wel — en soms moet het.',
            'Excel rekent van binnen naar buiten. In =AFRONDEN(GEMIDDELDE(B2:B6);2) wordt '
            'eerst het gemiddelde gemaakt, en dat gemiddelde wordt afgerond.',
            'Bouw een geneste formule in twee stappen: typ eerst de binnenste functie in een '
            'lege cel en kijk of het antwoord klopt. Pas dan schuif je ze naar binnen.',
        ],
        varianten=[
            ('=AFRONDEN(GEMIDDELDE(B2:B6);2)', 'eerst het gemiddelde, dan afronden'),
            ('=ALS(EN(B2>=50;C2>0);"ja";"nee")', 'EN zit genest in ALS'),
            ('=INDEX(A2:A5;VERGELIJKEN(MAX(B2:B5);B2:B5;0))', 'drie diep: MAX in VERGELIJKEN '
                                                              'in INDEX'),
            ('=AFRONDEN(MAX(B2:B6)/SOM(B2:B6);4)', 'twee functies naast elkaar binnen een derde'),
        ],
        weten=[
            'Elke functie heeft zijn eigen paar haakjes. Tel ze na: evenveel open als dicht.',
            'Zet een lange formule in de formulebalk uiteen met Alt+Enter. Excel rekent '
            'nog altijd hetzelfde, maar jij ziet de lagen.',
            'Klik in de formulebalk op een stuk van je formule en druk F9: Excel toont wat '
            'dat stuk oplevert. Zo vind je welke laag knelt.',
            'Nest niet omdat het kan. Twee korte formules in twee cellen zijn vaak beter '
            'te controleren dan één lange.',
        ],
        fout='Puntkomma en haakje verwisselen, zodat een argument van de buitenste functie '
             'binnen de binnenste belandt. De formule werkt dan wel, maar rekent iets '
             'anders uit dan je bedoelde.',
    ),
    dict(
        naam='INDEX en VERGELIJKEN — niet de waarde maar de naam',
        wat='MAX geeft het hoogste getal. Deze twee samen geven erbij wie dat getal heeft.',
        schrijf='=INDEX(waaruit;VERGELIJKEN(wat;waarin;0))',
        argumenten=[
            ('waaruit', 'de kolom of rij waar het antwoord in staat, bijvoorbeeld de namen'),
            ('wat', 'de waarde die je zoekt'),
            ('waarin', 'de kolom of rij waarin die waarde staat'),
            ('0', 'exact zoeken. Met 1 zou hij benaderend zoeken'),
        ],
        uitleg=[
            'VERGELIJKEN geeft geen waarde terug, maar een plaats: de hoeveelste rij van '
            'het bereik. Zoek je 85 in B2:B5 en staat die in de derde rij, dan geeft '
            'VERGELIJKEN 3.',
            'INDEX doet het omgekeerde: geef hem een bereik en een plaats, en hij haalt '
            'wat daar staat. INDEX(A2:A5;3) geeft de derde naam.',
            'Samen: VERGELIJKEN zoekt de plaats op in de ene kolom, INDEX haalt op diezelfde '
            'plaats het antwoord uit de andere kolom.',
            'Dit werkt ook naar links, waar VERT.ZOEKEN niet kan: de namen mogen vóór de '
            'getallen staan.',
        ],
        beelden=[
            dict(bestand='indexvergelijken-1',
                 onderschrift='In B7 staat het hoogste punt. VERGELIJKEN vindt dat getal op '
                              'plaats 3 in de puntenkolom, en INDEX haalt de derde naam op.',
                 kolommen=KOL_PUNTEN,
                 rijen=PUNTEN + [['', ''], ['hoogste punt', 85], ['wie dat is', 'Cis']],
                 formule='=INDEX(A2:A5;VERGELIJKEN(B7;B2:B5;0))',
                 geselecteerd='B8', gemarkeerd=('A4', 'B4'), rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=VERGELIJKEN(85;B2:B5;0)', 'geeft 3: de plaats, niet de waarde'),
            ('=INDEX(A2:A5;3)', 'geeft de derde naam'),
            ('=INDEX(A2:A5;VERGELIJKEN(MAX(B2:B5);B2:B5;0))', 'alles in één formule'),
            ('=INDEX(B1:E1;VERGELIJKEN(MAX(B9:E9);B9:E9;0))',
             'werkt ook zijwaarts: haalt een kolomkop op'),
        ],
        weten=[
            'De twee bereiken moeten even lang zijn en op dezelfde rij beginnen. A2:A5 en '
            'B2:B5 wel, A2:A5 en B3:B6 niet — dan krijg je de verkeerde naam.',
            'Staat de gezochte waarde twee keer in de kolom, dan geeft VERGELIJKEN de '
            'eerste. Bij een gelijkspel krijg je dus één naam, en dat is niet fout: er is '
            'maar plaats voor één.',
            '#N/B betekent dat VERGELIJKEN de waarde niet vindt. Negentien keer op twintig '
            'is dat een bereik dat één rij te kort is.',
        ],
        fout='De twee bereiken verschillend lang maken. VERGELIJKEN telt dan vanaf een '
             'andere rij dan INDEX, en je krijgt de buur van de naam die je zocht. Zonder '
             'foutmelding.',
    ),
    dict(
        naam='GROOTSTE en KLEINSTE — de tweede, de derde',
        wat='MAX geeft de hoogste. GROOTSTE geeft de hoeveelste hoogste je wil.',
        schrijf='=GROOTSTE(bereik;n)',
        argumenten=[
            ('bereik', 'de getallen'),
            ('n', 'de hoeveelste van boven af. 1 is hetzelfde als MAX'),
        ],
        uitleg=[
            'Soms wil je niet de topper maar de nummer twee. MAX kan dat niet; GROOTSTE wel.',
            'KLEINSTE werkt identiek, maar van onder af.',
            'Wil je ook weten WIE dat is, zet GROOTSTE dan in VERGELIJKEN, precies zoals je '
            'dat met MAX zou doen.',
        ],
        beelden=[
            dict(bestand='grootste-1',
                 onderschrift='85 is de hoogste, 72 de tweede hoogste. GROOTSTE met 2 geeft '
                              'dus 72.',
                 kolommen=KOL_PUNTEN,
                 rijen=PUNTEN + [['', ''], ['tweede hoogste', 72]],
                 formule='=GROOTSTE(B2:B5;2)', geselecteerd='B7',
                 gemarkeerd=('B2',), rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ('=GROOTSTE(B2:B5;1)', 'hetzelfde als =MAX(B2:B5)'),
            ('=GROOTSTE(B2:B5;2)', 'de tweede hoogste'),
            ('=KLEINSTE(B2:B5;2)', 'de tweede laagste'),
            ('=INDEX(A2:A5;VERGELIJKEN(GROOTSTE(B2:B5;2);B2:B5;0))',
             'de naam van de tweede hoogste'),
        ],
        weten=[
            'Vraag je de vijfde van vier getallen, dan krijg je #GETAL!.',
            'Twee keer hetzelfde getal telt twee keer. Staan er twee van 85, dan geeft '
            'GROOTSTE met 2 ook 85.',
            'n mag ook uit een cel komen. Dan kun je de formule doorvoeren en krijg je de '
            'eerste, tweede en derde op een rij.',
        ],
        fout='Denken dat GROOTSTE met 2 de tweede cel van het bereik geeft. Hij geeft de '
             'tweede in GROOTTE, en die kan overal in de lijst staan.',
    ),
    dict(
        naam='Rekenen met tijden',
        wat='Een tijd is voor Excel een getal: een deel van een dag. Daarmee kun je rekenen.',
        schrijf='=(einde-start)*24',
        argumenten=[
            ('einde-start', 'het verschil tussen twee tijden, als deel van een dag'),
            ('*24', 'omzetten naar uren, want een dag heeft 24 uur'),
        ],
        uitleg=[
            '12:00 is voor Excel 0,5 — de helft van een dag. 18:00 is 0,75.',
            'Twee tijden van elkaar aftrekken geeft dus ook een deel van een dag. 3,5 uur '
            'verschil geeft 0,1458. Maal 24 maakt er 3,5 van.',
            'Zonder die *24 lijkt het antwoord fout, maar dat is het niet: het staat alleen '
            'in een andere eenheid.',
        ],
        beelden=[
            dict(bestand='tijden-1',
                 onderschrift='Van 09:00 tot 12:30 is 3,5 uur. Vergeet je de *24, dan staat '
                              'er 0,15 — hetzelfde antwoord, maar in dagen.',
                 kolommen=[('A', 90), ('B', 70), ('C', 70), ('D', 70)],
                 rijen=[['Dag', 'Start', 'Einde', 'Uren'],
                        ['maandag', '09:00', '12:30', '3,50'],
                        ['dinsdag', '13:15', '17:45', '4,50'],
                        ['woensdag', '08:30', '16:00', '7,50']],
                 formule='=(C2-B2)*24', geselecteerd='D2',
                 rechts=('B', 'C', 'D'), vet_rij=1),
        ],
        varianten=[
            ('=(C2-B2)*24', 'het verschil in uren, als gewoon getal'),
            ('=C2-B2', 'het verschil als tijd. Geef de cel dan de notatie uu:mm'),
            ('=SOM(D2:D4)', 'uren als gewone getallen tel je gewoon op'),
            ('=C2>$F$1', 'een tijd vergelijken met een tijd die in een cel staat'),
        ],
        weten=[
            'Geef de uitkomst de notatie Getal, niet Tijd. Anders probeert Excel 3,5 als een '
            'tijdstip te tonen.',
            'Vergelijk een tijd altijd met een cel waarin een echte tijd staat. Typ je '
            '"22:30" met aanhalingstekens, dan vergelijk je met tekst en klopt niets meer.',
            'Komt een shift over middernacht, dan wordt het verschil negatief. Dat hoeft '
            'hier niet: alle diensten eindigen dezelfde avond.',
            'Haalt een cel met een opgezochte tijd een lang kommagetal? Dan is het de '
            'notatie die ontbreekt, niet de formule.',
        ],
        fout='De *24 vergeten en dan concluderen dat de formule fout is. Kijk eerst of het '
             'antwoord maal 24 wél klopt.',
    ),
    dict(
        naam='Verwijzen naar een ander werkblad',
        wat='Een cel van een ander blad gebruiken in je formule, zonder iets over te typen.',
        schrijf="='Bladnaam'!A1",
        argumenten=[
            ("'Bladnaam'", 'de naam van het blad, tussen enkele aanhalingstekens als er een '
                           'spatie of een cijfer in staat'),
            ('!', 'scheidt de bladnaam van het celadres'),
            ('A1', 'de cel of het bereik op dat blad'),
        ],
        uitleg=[
            'Je hoeft een getal nooit over te typen van het ene blad naar het andere. '
            'Verwijs ernaar, en het blijft kloppen als het origineel verandert.',
            'De eenvoudigste manier: typ een isgelijkteken, klik het andere blad aan, klik '
            'de cel aan en druk op Enter. Excel schrijft de verwijzing zelf.',
            'Het werkt ook binnen een functie: =SOM(\'Blad 2\'!B4:B20) telt een bereik van '
            'een ander blad op.',
        ],
        beelden=[
            dict(bestand='anderblad-1',
                 onderschrift='In B2 staat geen getal maar een verwijzing. Verandert D12 op '
                              'het blad Verkoop, dan verandert dit mee.',
                 kolommen=[('A', 130), ('B', 85)],
                 rijen=[['Samenvatting', ''],
                        ['Totaal verkoop', '1.284,50'],
                        ['Aantal klanten', 37]],
                 formule="='Verkoop'!D12", geselecteerd='B2',
                 rechts=('B',), vet_rij=1),
        ],
        varianten=[
            ("='Verkoop'!D12", 'één cel van een ander blad'),
            ("=SOM('Verkoop'!D4:D20)", 'een bereik van een ander blad optellen'),
            ("=AFRONDEN('Verkoop'!D12/'Verkoop'!B2;2)", 'twee cellen van een ander blad'),
            ("=VERT.ZOEKEN(A2;'Prijzen'!$A$2:$C$40;3;ONWAAR)",
             'opzoeken in een tabel die op een ander blad staat'),
        ],
        weten=[
            'Hernoem je het blad, dan past Excel alle verwijzingen zelf aan. Typ je de naam '
            'handmatig fout, dan krijg je #VERW!.',
            'Dollartekens werken precies zoals binnen één blad. Bij een zoektabel op een '
            'ander blad heb je ze even hard nodig.',
            'Verwijs liever naar het blad dan een getal over te typen. Een overgetypt getal '
            'is op het moment van typen juist en daarna nooit meer.',
        ],
        fout='De aanhalingstekens vergeten bij een bladnaam met een spatie of een cijfer '
             'erin. =Verkoop maart!D12 werkt niet; =\'Verkoop maart\'!D12 wel. Excel zet '
             'ze er zelf bij als je het blad aanklikt in plaats van de naam te typen.',
    ),
]
