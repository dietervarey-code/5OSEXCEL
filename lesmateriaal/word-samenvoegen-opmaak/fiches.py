# -*- coding: utf-8 -*-
"""Het tweede theorieboekje: de fiches gaan verder waar het eerste stopte.

Het eerste boekje (samenvoegen-theorie.docx) heeft dertien fiches en legt het
mechanisme uit: hoofddocument, gegevensbron, velden invoegen, etiketten,
voorbeeld en voltooien, Als…Dan…Anders, filteren en sorteren. Dat blijft
gelden en wordt hier niet herhaald.

Dit boekje begint bij fiche 14 en gaat over twee soorten samenvoegen die daar
niet in staan — enveloppen en lijsten — en over opmaak. De nummering loopt
door, zodat "fiche 17" in allebei de boekjes hetzelfde betekent.

De lintnamen zijn die van het Nederlandstalige Word (Microsoft 365 en 2021).
"""
import sys

sys.dont_write_bytecode = True

EERSTE_BOEKJE = "samenvoegen-theorie.docx"
FICHES_EERSTE_BOEKJE = 13
FICHE_START = FICHES_EERSTE_BOEKJE + 1

DELEN = ["Twee soorten die je nog niet deed", "Opmaak",
         "Als de opmaak niet klopt"]

FICHES = [
    # ======================= deel 1 — twee nieuwe soorten
    dict(
        deel="Twee soorten die je nog niet deed", naam="Enveloppen",
        wat="Eén envelop per adres, met je afzender er al op.",
        stappen=[
            'Nieuw, leeg Worddocument.',
            'Verzendlijsten, Afdruk samenvoegen starten, Enveloppen.',
            'Kies het formaat. DL is het gewone langwerpige formaat: '
            '110 × 220 mm. Onder Opties voor afdrukken staat hoe de envelop '
            'in de printer gaat — daar kijk je nu niet naar.',
            'Hang je lijst eraan: Adressen selecteren, Een bestaande lijst '
            'gebruiken.',
            'Klik LINKSBOVEN en typ je afzender. Dat is vaste tekst en komt '
            'op elke envelop hetzelfde.',
            'Klik in het kader RECHTSONDER (het geadresseerdevak) en voeg '
            'daar je samenvoegvelden in.',
            'Voorbeeld van resultaten, dan Voltooien en samenvoegen.',
        ],
        uitleg=[
            'Een envelop is één bladzijde per adres, net als een brief. Het '
            'enige verschil is dat die bladzijde de vorm van een envelop '
            'heeft.',
            'Word zet twee kaders op de envelop klaar: een klein voor de '
            'afzender linksboven en een groot voor de geadresseerde '
            'rechtsonder. In dat tweede kader komen je velden. Klik erin tot '
            'je de rand ziet.',
            'Zet de afzender klein, 8 of 9 punten. Hij hoort leesbaar te zijn '
            'maar niet op te vallen; de geadresseerde is waar de post naar '
            'kijkt.',
        ],
        voorbeeld=dict(
            koppen=['Waar', 'Wat erin komt'],
            rijen=[['linksboven, 8 pt',
                    'de clubnaam, de straat en de gemeente — vaste tekst'],
                   ['rechtsonder, 11 pt',
                    '«Voornaam» «Achternaam» / «Adresregel» / «Woonplaats»']]),
        weten=['Een envelop van 110 × 220 mm past niet op A4. Dat hoort: Word '
               'maakt er een eigen bladzijde van met dat formaat.',
               'Wil je ze toch op A4 afdrukken om te kijken of alles staat, '
               'kies dan Afdrukken en vink Aanpassen aan papierformaat aan.'],
        fout='In het verkeerde kader typen. Zet je je velden linksboven, dan '
             'staat het adres bij de afzender en blijft de rest van de '
             'envelop leeg.',
    ),
    dict(
        deel="Twee soorten die je nog niet deed",
        naam="Een lijst samenvoegen",
        wat="Niet één bladzijde per persoon, maar één REGEL per persoon.",
        stappen=[
            'Nieuw, leeg Worddocument.',
            'Verzendlijsten, Afdruk samenvoegen starten, Lijst.',
            'Hang je lijst eraan en filter op wat je wil (één ploeg, één '
            'categorie).',
            'Maak een tabel van ÉÉN rij, met evenveel cellen als je kolommen '
            'wil.',
            'Zet in elke cel één samenvoegveld. Geen koprij, geen titel, '
            'niets anders.',
            'Voltooien en samenvoegen, Afzonderlijke documenten bewerken.',
            'Nu pas zet je in het RESULTAAT de koprij en de titel erboven.',
        ],
        uitleg=[
            'Dit is de soort die niemand kent en die je het vaakst nodig '
            'hebt: een ploeglijst, een deelnemerslijst, een inventaris.',
            'En er is één ding dat je moet weten, anders loopt het altijd '
            'mis. Bij brieven, etiketten en enveloppen herhaalt Word een '
            'BLADZIJDE per record. Bij een lijst herhaalt Word HET HELE '
            'DOCUMENT per record.',
            'Zet je dus een koprij in je hoofddocument, dan komt die koprij '
            'bij elk lid opnieuw. Zet je er een titel boven, dan staat die er '
            'ook twintig keer. Daarom staat er in je hoofddocument alleen die '
            'ene tabelrij, en zet je de koprij pas achteraf in het resultaat.',
        ],
        voorbeeld=dict(
            koppen=['In je hoofddocument', 'Wat eruit komt'],
            rijen=[['één tabelrij met vier velden',
                    'één tabelrij per lid, netjes onder elkaar'],
                   ['een koprij erboven',
                    'die koprij tussen ELKE twee leden — fout']]),
        weten=['De tabelranden van je ene rij lopen door in het resultaat, dus '
               'je krijgt vanzelf een nette tabel.',
               'In een Engelse Word heet deze soort Directory.'],
        fout='De koprij in het hoofddocument zetten. Je ziet het pas in het '
             'resultaat, en dan moet je alles opnieuw doen.',
    ),
    # ======================= deel 2 — opmaak
    dict(
        deel="Opmaak", naam="Opmaak op een etiket",
        wat="Eerst het eerste etiket helemaal afwerken, DAN Labels bijwerken.",
        stappen=[
            'Vul het eerste etiket met je velden en je vaste tekst.',
            'Maak dat eerste etiket helemaal op: lettergrootte per regel, vet '
            'of cursief, uitlijning, en de afstand tussen de alinea\'s op 0.',
            'Kijk of het past. Een etiket van 38 mm hoog houdt ongeveer vier '
            'regels; meer wordt het niet.',
            'PAS DAN: Verzendlijsten, Labels bijwerken.',
        ],
        uitleg=[
            'Labels bijwerken kopieert het eerste etiket naar alle andere — '
            'inhoud ÉN opmaak. Doe je het in de juiste orde, dan staat je '
            'opmaak in één klik op alle veertien.',
            'Doe je het omgekeerd, dan is alleen de eerste kaart opgemaakt en '
            'moet je Labels bijwerken opnieuw doen. Dat kan, maar je verliest '
            'alles wat je daarna op de andere etiketten gewijzigd had.',
            'Zet de alinea-afstand op 0 (Start, Alinea, Afstand na: 0 pt). '
            'Anders duwt Word je vierde regel van het etiket af en zie je er '
            'maar drie.',
        ],
        voorbeeld=dict(
            koppen=['Regel', 'Opmaak'],
            rijen=[['de clubnaam', '8 pt, vet, hoofdletters, gecentreerd'],
                   ['de naam van het lid', '14 pt, vet, gecentreerd'],
                   ['de ploeg en de training', '9 pt, cursief, gecentreerd'],
                   ['het lidnummer', '8 pt, grijs, gecentreerd']]),
        weten=['Selecteer het hele etiket en zet de uitlijning in één keer op '
               'gecentreerd; de lettergrootte zet je per regel.',
               'Zie je de etiketranden niet? Tabelontwerp, Randen, '
               'Rasterlijnen weergeven. Die lijnen worden niet afgedrukt.'],
        fout='Opmaken na Labels bijwerken. Dan is alleen het eerste etiket '
             'mooi en de rest kaal.',
    ),
    dict(
        deel="Opmaak", naam="Tabstops in plaats van spaties",
        wat="Iets rechts op de bladzijde zetten doe je met een tabstop, nooit "
            "met spaties.",
        stappen=[
            'Zet je cursor in de alinea die je wil uitlijnen.',
            'Start, Alinea, het kleine pijltje rechtsonder, dan Tabs.',
            'Vul de positie in (bijvoorbeeld 16 cm), kies Rechts bij '
            'Uitlijning, en klik Instellen.',
            'Druk in je tekst op Tab om naar die positie te springen.',
        ],
        uitleg=[
            'Spaties lijken te werken tot je iets verandert. Een andere '
            'letter, een langere datum, een andere printer — en je datum '
            'staat weer scheef. Een tabstop staat vast.',
            'Een RECHTSE tabstop laat de tekst eindigen op die positie. '
            'Daarom staat de datum altijd netjes tegen de rechtermarge, hoe '
            'lang hij ook is.',
            'Op het lint zie je de tabstops als kleine tekentjes in de '
            'lintlijn boven je document. Je kan ze daar ook verslepen.',
        ],
        voorbeeld=dict(
            koppen=['Hoe je het doet', 'Wat er gebeurt als de tekst wijzigt'],
            rijen=[['vijfentwintig spaties', 'de datum schuift mee en staat '
                                             'scheef'],
                   ['één rechtse tabstop op 16 cm',
                    'de datum blijft tegen de rechtermarge staan']]),
        weten=['Een LINKSE tabstop laat de tekst beginnen op die positie. Die '
               'gebruik je voor kolommen in lopende tekst.',
               'Zet nooit twee tabs achter elkaar om verder te komen. Zet de '
               'tabstop op de juiste plaats.'],
        fout='De datum rechts zetten met de knop Rechts uitlijnen terwijl er '
             'ook tekst links op dezelfde regel staat. Dan schuift alles mee '
             'naar rechts.',
    ),
    dict(
        deel="Opmaak", naam="Een tabel in een brief",
        wat="Gegevens die bij elkaar horen, zet je in een tabel — ook in een "
            "brief.",
        stappen=[
            'Invoegen, Tabel, en kies het aantal kolommen en rijen.',
            'Links het opschrift, rechts de waarde of het samenvoegveld.',
            'Zet de randen weg waar je ze niet wil: Tabelontwerp, Randen, '
            'Geen rand. Of laat alleen een lijn onder de koprij staan.',
            'Maak de linkerkolom smaller dan de rechter, en zet de tabel niet '
            'over de hele breedte.',
        ],
        uitleg=[
            'Een tabel in een brief is bijna altijd beter dan een rijtje met '
            'tabs: hij blijft recht als de tekst verandert en je kan hem in '
            'één keer opmaken.',
            'Een samenvoegveld in een tabelcel werkt precies zoals in gewone '
            'tekst. Je kan er dus een betalingsoverzicht van maken dat per '
            'brief verschilt.',
            'Een tabel zonder randen ziet eruit als nette tekst en blijft '
            'toch een tabel. Dat is vaak precies wat je wil in een brief.',
        ],
        voorbeeld=dict(
            koppen=['Links', 'Rechts'],
            rijen=[['Ploeg', '«Ploeg»'],
                   ['Lidgeld', '«Lidgeld in tekst»'],
                   ['Te betalen vóór', '«Vervaldatum in tekst»'],
                   ['Rekeningnummer', 'vaste tekst']]),
        weten=['Een tabel verplaatsen: klik op het kruisje linksboven de tabel '
               'en sleep.',
               'Wordt je tabel te breed? Tabelindeling, Eigenschappen, '
               'Voorkeursbreedte.'],
        fout='De tabel over de volle breedte laten staan, zodat de waarden '
             'twaalf centimeter van hun opschrift staan. Zet de tabel op de '
             'breedte die je nodig hebt.',
    ),
    dict(
        deel="Opmaak", naam="Kop- en voettekst",
        wat="Tekst die op elke bladzijde terugkomt, zonder dat je ze herhaalt.",
        stappen=[
            'Invoegen, Voettekst (of Koptekst), en kies een lege.',
            'Typ wat er moet staan.',
            'Voor een paginanummer: Invoegen, Paginanummer, Huidige positie.',
            'Sluit de koptekst en voettekst met de knop rechts, of dubbelklik '
            'in je tekst.',
        ],
        uitleg=[
            'Een voettekst hoort NIET in je gewone tekst. Typ je de clubnaam '
            'onderaan je brief, dan staat ze op de tweede bladzijde niet meer '
            'waar ze hoort.',
            'Word berekent het paginanummer zelf. Daarom moet je het als VELD '
            'invoegen en niet als getal typen.',
            'In een samengevoegd document loopt de nummering door alle '
            'brieven. Wil je dat niet, dan is dat een teken dat je het nummer '
            'niet nodig had.',
        ],
        voorbeeld=dict(
            koppen=['Waar', 'Wat je erin zet'],
            rijen=[['koptekst', 'niets — je briefhoofd staat in de brief zelf'],
                   ['voettekst', 'de clubnaam, en het paginanummer als veld']]),
        weten=['De kop- en voettekst staan in de marge. Zijn ze te groot, dan '
               'duwen ze je tekst weg: Indeling, Marges, Aangepaste marges.'],
        fout='Het paginanummer als cijfer typen. Op bladzijde twee staat er '
             'dan nog altijd 1.',
    ),
    dict(
        deel="Opmaak", naam="Marges en wat op papier past",
        wat="Hoeveel ruimte je echt hebt, en wat je ermee doet.",
        uitleg=[
            'Een A4 is 210 bij 297 mm. Met de standaardmarges van Word houd '
            'je ongeveer 16 cm breedte over. Dat is waarom een rechtse '
            'tabstop vaak op 16 cm staat.',
            'Marges wijzig je bij Indeling, Marges. Maak ze niet kleiner dan '
            '1,5 cm: de meeste printers kunnen niet tot aan de rand.',
            'Een etiket of een envelop heeft zijn eigen formaat en zijn eigen '
            'marges. Daar verander je niets aan — je past je tekst aan, niet '
            'het papier.',
            'Wil je zien wat er echt op een bladzijde staat? Beeld, '
            'Afdrukweergave, en zet de zoom op één volledige pagina. Dat is '
            'de enige manier om opmaak te beoordelen.',
        ],
        voorbeeld=dict(
            koppen=['Wat', 'Hoe groot'],
            rijen=[['A4', '210 × 297 mm'],
                   ['bruikbare breedte met standaardmarges', 'ongeveer 16 cm'],
                   ['DL-envelop', '110 × 220 mm'],
                   ['het etiket van deze opdracht', '99,1 × 38,1 mm']]),
        weten=['Lettergrootte onder 8 punten is op papier niet meer te lezen. '
               'Op een etiket is 8 punten het minimum.',
               'Twee verschillende letterfamilies in één document is al veel. '
               'Drie is te veel.'],
        fout='De opmaak beoordelen op het scherm, in de gewone weergave. Pas '
             'in de afdrukweergave zie je waar de bladzijde stopt.',
    ),
    # ======================= deel 3 — als het misgaat
    dict(
        deel="Als de opmaak niet klopt", naam="De opmaakklachten",
        wat="Wat je ziet, waar het aan ligt, en wat je eraan doet.",
        voorbeeld=dict(
            koppen=['Wat je ziet', 'Wat eraan te doen'],
            rijen=[
                ['Alleen het eerste etiket is opgemaakt',
                 'Je hebt opgemaakt na Labels bijwerken. Doe Labels bijwerken '
                 'opnieuw.'],
                ['De vierde regel van mijn etiket is weg',
                 'De alinea-afstand staat niet op 0, of je lettergrootte is '
                 'te groot voor 38 mm.'],
                ['Mijn datum staat scheef',
                 'Je hebt spaties gebruikt in plaats van een rechtse tabstop.'],
                ['De koprij van mijn lijst staat er twintig keer',
                 'Hij stond in het hoofddocument. Hij hoort in het resultaat.'],
                ['Het adres staat bij de afzender op de envelop',
                 'Je velden staan in het verkeerde kader. Klik rechtsonder.'],
                ['Mijn voettekst staat op bladzijde 2 midden in de tekst',
                 'Je hebt ze getypt in plaats van ze als voettekst in te '
                 'voegen.'],
                ['Er staat 0,79 waar een uur hoort',
                 'De opmaak van een cel komt niet mee. Gebruik de tekstkolom '
                 'uit je lijst — fiche 12 uit het eerste boekje.'],
            ]),
        uitleg=[
            'Loop dit lijstje af voor je je hand opsteekt. En doe het in de '
            'afdrukweergave: de helft van deze klachten zie je niet in de '
            'gewone weergave.',
        ],
        weten=['Opmaak kwijt na het samenvoegen? Je hebt het resultaat '
               'opgemaakt in plaats van het hoofddocument. Maak altijd het '
               'hoofddocument op; het resultaat erft alles.'],
        fout='Opnieuw beginnen. Opmaak repareren is bijna altijd één klik; '
             'opnieuw beginnen is twintig minuten.',
    ),
]


def nummer(index):
    """De index in FICHES -> het fichenummer zoals het in de boekjes staat."""
    return FICHE_START + index


def op_naam(naam):
    for i, kaart in enumerate(FICHES):
        if kaart['naam'] == naam:
            return nummer(i)
    raise KeyError(f'fiche {naam!r} bestaat niet — de fiches heten: '
                   f'{[k["naam"] for k in FICHES]}')


# de fiches uit het EERSTE boekje waar deze bundel naar verwijst
EERSTE = {
    6: 'De lijst aan je document hangen',
    7: 'Samenvoegvelden invoegen',
    8: 'Etiketten',
    9: 'Voorbeeld, en voltooien',
    10: 'Als…Dan…Anders',
    11: 'Ontvangers filteren en sorteren',
    12: 'De opmaak komt niet mee',
}

if __name__ == '__main__':
    deel = None
    for i, k in enumerate(FICHES):
        if k['deel'] != deel:
            deel = k['deel']
            print(f'\n{deel}')
        print(f'  fiche {nummer(i):>2}. {k["naam"]}')
    print(f'\n{len(FICHES)} fiches, {FICHE_START} tot {nummer(len(FICHES) - 1)}')
    print(f'verwijst naar {len(EERSTE)} fiches uit {EERSTE_BOEKJE}')
