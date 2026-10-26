# -*- coding: utf-8 -*-
"""De fiches die in de opdrachtbundel zelf staan.

Dit is een nieuw onderwerp, dus de uitleg gaat mee in de opdracht — zoals in
excel-basis en excel-uitdaging, en anders dan in de draaitabelbundels, waar
de theorie in een apart boekje zit.

Twee dingen verwijzen wél naar dat boekje: de draaitabel (kaart 3 en 4) en de
draaigrafiek (kaart 13). Die hebben ze al gehad.
"""
import sys

sys.dont_write_bytecode = True

THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"

DELEN = ["Knippen", "Opkuisen en plakken", "Zonder formules"]

FICHES = [
    dict(
        deel="Knippen", naam="LINKS en RECHTS", functies=['LINKS', 'RECHTS'],
        wat="De eerste of de laatste tekens van een stuk tekst.",
        schrijf='=LINKS(cel;aantal)    =RECHTS(cel;aantal)',
        argumenten=[('cel', 'waar de tekst staat'),
                    ('aantal', 'hoeveel tekens je wil hebben')],
        uitleg=[
            'LINKS telt vanaf het begin, RECHTS vanaf het einde.',
            'Dit werkt alleen als het stuk dat je wil altijd even lang is. '
            'Staat er de ene keer twee letters en de andere keer drie, dan heb '
            'je VIND.ALLES nodig.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['BE2019', '=LINKS(A2;2)  geeft  BE'],
                   ['BE2019', '=RECHTS(A2;4)  geeft  2019']]),
        weten=['Een spatie is ook een teken en telt gewoon mee.'],
        fout='Tellen vanaf nul. Het eerste teken is teken 1, niet teken 0.',
    ),
    dict(
        deel="Knippen", naam="WAARDE", functies=['WAARDE'],
        wat="Maakt van tekst die eruitziet als een getal, een echt getal.",
        schrijf='=WAARDE(cel)',
        argumenten=[('cel', 'de cel met tekst die een getal voorstelt')],
        uitleg=[
            'Wat je met LINKS, RECHTS of DEEL uit een cel knipt, is ALTIJD '
            'tekst — ook als er cijfers staan.',
            'Je ziet het verschil aan de uitlijning: tekst gaat vanzelf naar '
            'links in de cel, een getal naar rechts.',
            'Zolang het tekst is, kan je er niet mee rekenen. MIN, MAX en SOM '
            'slaan die cellen gewoon over.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt', 'Wat je krijgt'],
            rijen=[['BE2019', '=RECHTS(A2;4)', '2019  links in de cel: tekst'],
                   ['BE2019', '=WAARDE(RECHTS(A2;4))',
                    '2019  rechts in de cel: getal']]),
        weten=['=RECHTS(A2;4)*1 doet hetzelfde als WAARDE. Allebei goed.'],
        fout='Een MIN of MAX die 0 geeft terwijl er duidelijk getallen staan. '
             'Dan is het tekst en heb je WAARDE vergeten.',
    ),
    dict(
        deel="Knippen", naam="VIND.ALLES", functies=['VIND.ALLES'],
        wat="Zegt op welke plaats een teken in een cel staat.",
        schrijf='=VIND.ALLES("teken";cel)',
        argumenten=[('"teken"', 'waar je naar zoekt, tussen aanhalingstekens'),
                    ('cel', 'waarin je zoekt')],
        uitleg=[
            'Het antwoord is een getal: het hoeveelste teken het is.',
            'Daarmee kan je LINKS en RECHTS gebruiken op tekst die NIET altijd '
            'even lang is. Je laat Excel eerst zoeken waar de scheiding staat.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['Klub C | Kompaan', '=VIND.ALLES("|";A2)  geeft  8'],
                   ['Main Stage | Nachtkever',
                    '=VIND.ALLES("|";A2)  geeft  12']]),
        weten=['VIND.ALLES let op hoofdletters, VIND.SPEC niet. Voor een '
               'streepje of een komma maakt dat niets uit.',
               'Staat het teken er niet in, dan krijg je #WAARDE!.'],
        fout='De twee argumenten omwisselen. Eerst WAT je zoekt, dan WAAR.',
    ),
    dict(
        deel="Knippen", naam="LENGTE", functies=['LENGTE'],
        wat="Telt hoeveel tekens er in een cel staan.",
        schrijf='=LENGTE(cel)',
        argumenten=[('cel', 'waarvan je de tekens telt')],
        uitleg=[
            'Simpel op zich, maar onmisbaar in combinatie met RECHTS: om het '
            'stuk ACHTER een scheidingsteken te pakken, moet je weten hoeveel '
            'tekens dat er zijn.',
            'Dat is de hele lengte, min alles tot en met het scheidingsteken.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['Klub C | Kompaan', '=LENGTE(A2)  geeft  16'],
                   ['Klub C | Kompaan',
                    '=RECHTS(A2;LENGTE(A2)-VIND.ALLES("|";A2)-1)  geeft  '
                    'Kompaan']]),
        weten=['Spaties tellen mee. Daarom staat er -1 achteraan: de spatie na '
               'het streepje wil je niet mee hebben.'],
        fout='Vergeten dat de spatie rond het streepje ook tekens zijn, en '
             'dan een antwoord krijgen dat met een spatie begint.',
    ),
    dict(
        deel="Knippen", naam="DEEL", functies=['DEEL'],
        wat="Een stuk uit het MIDDEN van een cel.",
        schrijf='=DEEL(cel;vanaf;aantal)',
        argumenten=[('cel', 'waar de tekst staat'),
                    ('vanaf', 'het hoeveelste teken je begint'),
                    ('aantal', 'hoeveel tekens je meeneemt')],
        uitleg=[
            'LINKS pakt vooraan, RECHTS pakt achteraan, DEEL pakt ertussenin.',
            'Dit is de makkelijkste van de drie zodra elke code op dezelfde '
            'manier is opgebouwd: dan staat elk stuk altijd op dezelfde plaats.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['ZK26-VR-MAIN-007', '=DEEL(A2;6;2)  geeft  VR'],
                   ['ZK26-VR-MAIN-007', '=DEEL(A2;9;4)  geeft  MAIN']]),
        weten=['Tel op papier eens mee voor je typt. Z=1, K=2, 2=3, 6=4, '
               'streepje=5, dus de dag begint op 6.'],
        fout='Eén teken naast de plaats beginnen, waardoor overal een streepje '
             'in je antwoord staat. Dan moet "vanaf" eentje hoger of lager.',
    ),
    dict(
        deel="Opkuisen en plakken", naam="SPATIES.WISSEN", functies=['SPATIES.WISSEN'],
        wat="Haalt de spaties weg die je niet ziet.",
        schrijf='=SPATIES.WISSEN(cel)',
        argumenten=[('cel', 'die je wil opkuisen')],
        uitleg=[
            'Spaties vooraan en achteraan gaan weg. Dubbele spaties midden in '
            'de tekst worden er één.',
            'Eén spatie tussen twee woorden blijft dus gewoon staan — en dat '
            'is maar goed ook.',
            'Zulke spaties zijn de reden dat een VERT.ZOEKEN #N/B geeft terwijl '
            'je met je eigen ogen ziet dat de naam er staat.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['"  DE SMET  "', '=SPATIES.WISSEN(A2)  geeft  "DE SMET"'],
                   ['"peeters"', '=SPATIES.WISSEN(A2)  geeft  "peeters"']]),
        weten=['Wil je ALLE spaties weg, ook die tussen twee woorden, dan heb '
               'je SUBSTITUEREN nodig.'],
        fout='Denken dat er niets gebeurd is omdat je het verschil niet ziet. '
             'Zet er even =LENGTE() naast, dan zie je het wel.',
    ),
    dict(
        deel="Opkuisen en plakken", naam="BEGINLETTERS", functies=['BEGINLETTERS', 'HOOFDLETTERS', 'KLEINE.LETTERS'],
        wat="Zet elk woord met een hoofdletter en de rest klein.",
        schrijf='=BEGINLETTERS(cel)    =HOOFDLETTERS(cel)    '
                '=KLEINE.LETTERS(cel)',
        argumenten=[('cel', 'waarvan je de hoofdletters rechtzet')],
        uitleg=[
            'BEGINLETTERS maakt van VANDENBERGHE en van vandenberghe allebei '
            'Vandenberghe.',
            'HOOFDLETTERS maakt alles groot, KLEINE.LETTERS maakt alles klein. '
            'Die laatste gebruik je voor e-mailadressen.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['VANDENBERGHE', '=BEGINLETTERS(A2)  geeft  Vandenberghe'],
                   ['Lotte', '=KLEINE.LETTERS(A2)  geeft  lotte']]),
        weten=['BEGINLETTERS weet niets van namen. "de smet" wordt "De Smet" '
               'en "mcdonald" wordt "Mcdonald". Soms moet je dus nog met de '
               'hand bijsturen; dat hoeft hier niet.'],
        fout='BEGINLETTERS op een e-mailadres loslaten. Dan krijg je '
             'Lotte.Vandenberghe@Zomerklank.Be.',
    ),
    dict(
        deel="Opkuisen en plakken", naam="SUBSTITUEREN", functies=['SUBSTITUEREN'],
        wat="Vervangt overal een stukje tekst door een ander stukje.",
        schrijf='=SUBSTITUEREN(cel;"oud";"nieuw")',
        argumenten=[('cel', 'waarin je vervangt'),
                    ('"oud"', 'wat eruit moet'),
                    ('"nieuw"', 'wat ervoor in de plaats komt')],
        uitleg=[
            'Wil je iets wegdoen in plaats van vervangen, zet dan twee '
            'aanhalingstekens zonder iets ertussen: "".',
            'Dit is de enige manier om een spatie MIDDEN in een woord weg te '
            'krijgen; SPATIES.WISSEN laat die staan.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['Lotte Vandenberghe',
                    '=SUBSTITUEREN(A2;" ";".")  geeft  Lotte.Vandenberghe'],
                   ['Van Damme', '=SUBSTITUEREN(A2;" ";"")  geeft  VanDamme']]),
        weten=['SUBSTITUEREN vervangt ÉLK voorkomen. "Amina De Smet" heeft twee '
               'spaties en krijgt dus twee punten.'],
        fout='De aanhalingstekens vergeten rond het stukje tekst. Zonder '
             'aanhalingstekens denkt Excel dat je een celnaam bedoelt.',
    ),
    dict(
        deel="Opkuisen en plakken", naam="Plakken met &", functies=[],
        wat="Zet stukken tekst aan elkaar tot één nieuwe tekst.",
        schrijf='=A2&" "&B2',
        argumenten=[('&', 'plakt wat ervoor en erna staat aan elkaar'),
                    ('" "', 'een stukje tekst dat je er zelf bij typt')],
        uitleg=[
            'Alles wat je zelf bijtypt, moet tussen aanhalingstekens. '
            'Celverwijzingen niet.',
            'Vergeet de spatie niet: =A2&B2 geeft LotteVandenberghe.',
            'Bouw een lange plakformule in stappen op. Maak eerst een kolom met '
            'de nette naam, en plak daar pas in de volgende kolom het '
            'e-mailadres uit. Dan zie je ook meteen waar het misloopt.',
        ],
        voorbeeld=dict(
            koppen=['In de cel staat', 'Wat je typt, en wat je krijgt'],
            rijen=[['A2 = Lotte     B2 = Vandenberghe',
                    '=A2&" "&B2  geeft  Lotte Vandenberghe'],
                   ['A2 = lotte.vandenberghe',
                    '=A2&"@zomerklank.be"  geeft  '
                    'lotte.vandenberghe@zomerklank.be']]),
        weten=['TEKST.SAMENVOEGEN doet hetzelfde en kan meer, maar bestaat '
               'alleen vanaf Excel 2019. Met & zit je altijd goed.'],
        fout='De aanhalingstekens rond het apenstaartje vergeten.',
    ),
    dict(
        deel="Zonder formules", naam="Duplicaten verwijderen", functies=[],
        wat="Gooit regels weg die helemaal dubbel staan.",
        schrijf=None,
        stappen=[
            'Klik één cel in de lijst aan.',
            'Ga naar Gegevens, en klik op Duplicaten verwijderen.',
            'Vink aan op welke kolommen Excel moet vergelijken. Laat ze gewoon '
            'allemaal aangevinkt: pas als ÉLKE kolom gelijk is, is het echt '
            'dubbel.',
            'Excel zegt hoeveel regels hij weggegooid heeft. Lees dat getal, '
            'je hebt het nodig.',
        ],
        uitleg=[
            'Dit verandert je lijst voorgoed. Er gaan rijen weg, en Ctrl+Z is '
            'je enige weg terug.',
        ],
        weten=['Vink je maar één kolom aan, dan gooit Excel ook regels weg die '
               'alleen in die ene kolom gelijk zijn. Dat is bijna nooit wat je '
               'wil.'],
        fout='Eerst de draaitabel maken en pas daarna opkuisen. Dan staan de '
             'dubbels al in je telling.',
    ),
    dict(
        deel="Zonder formules", naam="Een tabel maken (Ctrl+T)", functies=[],
        wat="Maakt van je lijst een echte tabel, die meegroeit.",
        schrijf=None,
        stappen=[
            'Klik één cel in de lijst aan.',
            'Druk Ctrl+T.',
            'Controleer dat "De tabel bevat kopteksten" aangevinkt staat.',
            'Klik OK. Je lijst krijgt kleur en filterpijltjes.',
        ],
        uitleg=[
            'Een tabel is meer dan opmaak. Zet je er een rij bij onderaan, dan '
            'hoort die er meteen bij — ook in elke draaitabel en grafiek die '
            'erop staat.',
            'Weet je nog dat je bij de draaitabellen het bronbereik met de hand '
            'moest oprekken toen er een rij bijkwam? Dit is de oplossing '
            'daarvoor. Maak van je lijst eerst een tabel, dan hoeft dat nooit '
            'meer.',
            'En een slicer kan alleen op een tabel of op een draaitabel.',
        ],
        weten=['Boven in het lint verschijnt Tabelontwerp. Daar kan je de tabel '
               'een naam geven; dat leest later een stuk prettiger dan '
               'Tabel1.'],
        fout='Ctrl+T drukken terwijl er een lege rij in je lijst zit. Dan pakt '
             'Excel maar de helft.',
    ),
    dict(
        deel="Zonder formules", naam="Een slicer", functies=[],
        wat="Knoppen waarmee je een tabel of draaitabel filtert.",
        schrijf=None,
        stappen=[
            'Klik je draaitabel aan.',
            'Ga naar Draaitabel analyseren, en klik op Slicer invoegen.',
            'Vink het veld aan waarop je wil kunnen filteren. Klik OK.',
            'Klik een knop aan om te filteren. Met het gommetje rechtsboven in '
            'de slicer zet je het filter weer af.',
        ],
        uitleg=[
            'Een slicer doet hetzelfde als een filter, maar je ziet in één '
            'oogopslag wat er aanstaat. Daarom staan ze op elk dashboard.',
            'Alles wat aan je draaitabel hangt, beweegt mee — ook de '
            'draaigrafiek. Dat is het mooie: je klikt op Hiphop en je grafiek '
            'verandert.',
            'Een gewone grafiek op een gewone lijst doet dat niet. Daarom eerst '
            'een draaitabel, dan een draaigrafiek, dan pas de slicer.',
        ],
        weten=['Hou Ctrl ingedrukt om meer dan één knop tegelijk te kiezen.',
               'Een slicer voor datums heet een tijdlijn en werkt net zo.'],
        fout='Een slicer proberen invoegen terwijl je buiten de draaitabel '
             'geklikt hebt. De knop staat dan grijs.',
    ),
]

# waar de fiches van het andere boekje gebruikt worden
KAARTEN_ELDERS = {
    3: 'Een draaitabel invoegen',
    4: 'Rijen en Waarden — je eerste draaitabel',
    13: 'Een draaigrafiek',
}

if __name__ == '__main__':
    for i, f in enumerate(FICHES, 1):
        stuk = f.get('schrijf') or '(geen formule — menu)'
        print(f"{i:>2}. {f['naam']:<28} {f['deel']:<20} {stuk.splitlines()[0]}")
    print(f'\n{len(FICHES)} fiches in {len(DELEN)} delen')
