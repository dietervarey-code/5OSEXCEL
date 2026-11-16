# -*- coding: utf-8 -*-
"""De vijf stappen. Eén lesuur per stap, en in elke stap wordt de opmaak apart
gequoteerd.

Er valt in Excel niets te doen: de lijsten staan klaar. Alles gebeurt in Word.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = _laad('g', 'gegevens.py')
a = _laad('a', 'antwoorden.py')
f = _laad('f', 'fiches.py')

THEORIEBUNDEL = "samenvoegen-opmaak-theorie.docx"
STARTBESTAND = "samenvoegen-opmaak-startbestand.xlsx"


def marker(naam):
    return f'[[{naam}]]'


def _velden(regel):
    """['Voornaam', 'Achternaam'] -> '«Voornaam» «Achternaam»'."""
    return ' '.join(f'«{v}»' for v in regel)


def _opmaak_tekst(regel):
    """De opmaak van één lidkaartregel als één leesbare opsomming."""
    stukken = [f"{regel['grootte']} punten"]
    if regel['vet']:
        stukken.append('vet')
    if regel['cursief']:
        stukken.append('cursief')
    if regel['kleur'] != 'zwart':
        stukken.append(regel['kleur'])
    stukken.append(g.LIDKAART_UITLIJNING)
    return ', '.join(stukken)


STAPPEN = [
    dict(
        nr=1, titel='Lidkaarten', soort='Etiketten', lesuren=1,
        lijst=g.LEDEN_BLAD,
        fiches=[f.op_naam('Opmaak op een etiket')],
        fiches_eerste=[8, 7, 9],
        inleiding=[
            f'{a.AANTAL_LEDEN} leden krijgen een lidkaart: een etiket dat ze '
            'in hun portefeuille steken. Je maakt er één vel van.',
            'Samenvoegen heb je al gedaan. Nieuw is de opmaak: op een kaart '
            f'van {g.ETIKET_SOORT.split("(")[1].rstrip(")")} moeten vier '
            'regels passen, en elke regel ziet er anders uit.',
            'De orde doet ertoe. Je maakt het EERSTE etiket helemaal af — '
            'inhoud én opmaak — en dan pas klik je op Labels bijwerken. Doe '
            'je het omgekeerd, dan mag je het tweemaal doen.',
        ],
        stappen=[
            ('Etiketten kiezen',
             'Nieuw, leeg Worddocument. Verzendlijsten, Afdruk samenvoegen '
             f'starten, Etiketten. Kies {g.ETIKET_SOORT}. Staat dat formaat '
             f'er niet bij, neem er dan een met {g.ETIKET_PER_BLAD} etiketten '
             'per blad en schrijf op welk je genomen hebt.', 2),
            ('De lijst eraan hangen',
             f'Adressen selecteren, Een bestaande lijst gebruiken, '
             f'{STARTBESTAND}, werkblad {g.LEDEN_BLAD}.', 2),
            ('Het eerste etiket vullen',
             'Vier regels, in deze volgorde: '
             + ' / '.join(regel['inhoud'] for regel in g.LIDKAART)
             + '. Enter na elke regel. De punthaken typ je niet zelf.', 2),
            ('Labels bijwerken en voltooien',
             'Pas NADAT de opmaak hieronder klaar is: Labels bijwerken, dan '
             'Voorbeeld van resultaten, dan Voltooien en samenvoegen, '
             'Afzonderlijke documenten bewerken. Bewaar als '
             'lidkaarten-jouwnaam.docx.', 2),
        ],
        opmaak=[(f'Regel {i}: {regel["inhoud"]}',
                 f'{regel["hoe"]}. Opmaak: {_opmaak_tekst(regel)}.', 2)
                for i, regel in enumerate(g.LIDKAART, 1)],
        klaar=f'Eén document met {a.ETIKET_BLADEN} bladen, {a.AANTAL_LEDEN} '
              f'kaarten gevuld en {a.ETIKET_LEEG} leeg op het laatste blad. '
              'Op elke kaart een andere naam, en op elke kaart dezelfde '
              'opmaak.',
        controle='Zet de zoom op één volledige pagina in de afdrukweergave. '
                 'Alle veertien kaarten op het eerste blad horen er identiek '
                 'uit te zien, met alleen andere namen. Is er één anders, dan '
                 'heb je daar met de hand in gewerkt.',
        vast=[
            'Alleen de eerste kaart is opgemaakt: je hebt opgemaakt na Labels '
            'bijwerken. Doe Labels bijwerken opnieuw.',
            'De vierde regel is weg: de alinea-afstand staat niet op 0. Start, '
            'Alinea, Afstand na: 0 pt.',
            'Je ziet de randen van de etiketten niet. Tabelontwerp, Randen, '
            'Rasterlijnen weergeven. Die lijnen worden niet afgedrukt.',
        ],
    ),
    dict(
        nr=2, titel='Enveloppen', soort='Enveloppen', lesuren=1,
        lijst=g.LEDEN_BLAD,
        fiches=[f.op_naam('Enveloppen')],
        fiches_eerste=[6, 11],
        inleiding=[
            'Een envelop is de derde soort samenvoegdocument, en de '
            'eenvoudigste van allemaal: twee kaders, en in één daarvan je '
            'velden.',
            f'Je stuurt ze niet naar iedereen. Alleen de leden die hun '
            f'lidgeld nog niet betaald hebben krijgen post, en dat zijn er '
            f'minder dan {a.AANTAL_LEDEN}. Daar heb je een filter voor.',
            'Let op in welk kader je typt. De afzender linksboven is vaste '
            'tekst; de geadresseerde rechtsonder zijn je velden. Klik tot je '
            'de rand van het kader ziet.',
        ],
        stappen=[
            ('Enveloppen kiezen',
             'Nieuw, leeg Worddocument. Verzendlijsten, Afdruk samenvoegen '
             f'starten, Enveloppen. Formaat: {g.ENVELOP_FORMAAT}.', 2),
            ('De lijst eraan hangen en filteren',
             f'Hang {g.LEDEN_BLAD} eraan. Dan Lijst met ontvangers bewerken, '
             f'Filteren: {g.ENVELOP_FILTER[0]} is gelijk aan '
             f'{g.ENVELOP_FILTER[1]}. Schrijf op hoeveel ontvangers er '
             'overblijven.', 3),
            ('Voltooien',
             'Voorbeeld van resultaten, loop door de enveloppen, dan '
             'Voltooien en samenvoegen, Afzonderlijke documenten bewerken. '
             'Bewaar als enveloppen-jouwnaam.docx.', 2),
        ],
        opmaak=[
            ('De afzender linksboven',
             'Drie regels vaste tekst: '
             + ' / '.join(g.ENVELOP_AFZENDER)
             + f'. Lettergrootte {g.ENVELOP_AFZENDER_GROOTTE} punten, links '
               'uitgelijnd. Hij hoort leesbaar te zijn, niet op te vallen.',
             3),
            ('De geadresseerde rechtsonder',
             'Drie regels met velden: '
             + ' / '.join(_velden(regel) for regel in g.ENVELOP_GEADRESSEERDE)
             + f'. Lettergrootte {g.ENVELOP_GEADRESSEERDE_GROOTTE} punten.',
             2),
        ],
        klaar=f'{a.AANTAL_ENVELOPPEN} enveloppen, elk met een ander adres '
              'rechtsonder en op elk dezelfde afzender linksboven.',
        controle=f'Er horen {a.AANTAL_ENVELOPPEN} enveloppen uit te komen, '
                 f'niet {a.AANTAL_LEDEN}. Komen er {a.AANTAL_LEDEN} uit, dan '
                 'staat je filter niet aan.',
        vast=[
            'Het adres staat bij de afzender: je velden staan in het '
            'verkeerde kader. Klik rechtsonder, in het grote kader.',
            'De envelop past niet op je scherm: dat hoort. Een envelop is '
            'geen A4. Zet de zoom op één volledige pagina.',
            f'Er komen {a.AANTAL_LEDEN} enveloppen uit: je filter staat niet '
            'aan, of je hebt hem op de verkeerde kolom gezet.',
        ],
    ),
    dict(
        nr=3, titel='De brief', soort='Brieven', lesuren=1,
        lijst=g.LEDEN_BLAD, brief=g.BRIEF_LEDEN,
        fiches=[f.op_naam('Tabstops in plaats van spaties'),
                f.op_naam('Een tabel in een brief'),
                f.op_naam('Kop- en voettekst'),
                f.op_naam('Marges en wat op papier past')],
        fiches_eerste=[7, 10, 12],
        inleiding=[
            f'Open {g.BRIEF_LEDEN}. De tekst staat er al in — en met opzet '
            'helemaal zonder opmaak. Alles staat links, in dezelfde letter, '
            'zonder tabel en zonder voettekst. Het ziet eruit als een '
            'kladje, en dat is het ook.',
            'Dit uur is dus voor de helft samenvoegen en voor de helft '
            'opmaken. De markers vervang je door velden; de opmaak maak je '
            'zelf, volgens de lijst hieronder.',
            f'Eén ding kan je niet met opmaak oplossen: in de lijst staan '
            f'twee kolommen met hetzelfde lidgeld, {g.LEDEN_KOP[10]} en '
            f'{g.LEDEN_KOP[11]}. Gebruik de tweede. Probeer de eerste één '
            'keer en kijk wat er in je brief staat — dan weet je waarom.',
        ],
        stappen=[
            ('De brief onder je eigen naam bewaren',
             'Bestand, Opslaan als, brief-jouwnaam.docx. Werk daarin, niet in '
             'het model.', 1),
            ('Hoofddocument en lijst',
             'Verzendlijsten, Afdruk samenvoegen starten, Brieven. Dan '
             f'Adressen selecteren, werkblad {g.LEDEN_BLAD}. Géén filter dit '
             'keer: iedereen krijgt deze brief.', 2),
            (f'De {len(g.BRIEF_MARKERS)} markers vervangen',
             ', '.join(marker(m) for m in g.BRIEF_MARKERS)
             + '. Verwijder de marker en voeg het veld in de plaats ervan in.',
             4),
            ('De aanmaningszin met een regel',
             'Verzendlijsten, Regels, Als…Dan…Anders. '
             f'Veld {g.BRIEF_REGEL[0]}, is gelijk aan, {g.BRIEF_REGEL[1]}. '
             'Deze tekst invoegen: Volgens onze gegevens is je lidgeld nog '
             'niet betaald. Wil je dat vóór de vervaldatum in orde brengen? '
             'Het andere vak laat je leeg.', 3),
        ],
        opmaak=[
            ('Het briefhoofd',
             f'De clubnaam {g.CLUB} op de eerste regel, 16 punten, vet. '
             'Daaronder het adres en het e-mailadres op één regel, 9 punten, '
             'grijs. Zet onder die tweede regel een lijn (Start, Randen, '
             'Onderrand).', 3),
            ('De datum rechts',
             f'De regel met {g.CLUB_GEMEENTE}, '
             f'{g.datum_lang(g.BRIEFDATUM)} hoort tegen de rechtermarge te '
             f'eindigen. Met een RECHTSE tabstop op {g.BRIEF_TABSTOP_CM:g} '
             'cm — niet met spaties, en niet met de knop Rechts uitlijnen.',
             4),
            ('De tabel met het overzicht',
             f'Een tabel van {len(g.BRIEF_TABEL)} rijen en 2 kolommen, met '
             'links het opschrift en rechts de waarde: '
             + ' / '.join(opschrift for opschrift, _v in g.BRIEF_TABEL)
             + '. Zet de randen weg en maak de tabel niet breder dan je '
               'nodig hebt. De linkerkolom smaller dan de rechter.', 3),
            ('De voettekst',
             f'Invoegen, Voettekst. Daarin de clubnaam en het paginanummer '
             'als VELD (Invoegen, Paginanummer, Huidige positie). Niet als '
             'cijfer typen.', 2),
        ],
        klaar=f'{a.AANTAL_BRIEVEN} brieven, elk op één bladzijde, met een '
              'briefhoofd, een datum die rechts staat, een tabel met de '
              f'gegevens van dat lid, en in {a.AANTAL_AANMANING} ervan de '
              'aanmaningszin.',
        controle=f'In de brief van {a.VOORBEELD.naam} staat ploeg '
                 f'{a.VOORBEELD.ploeg}, trainer {a.VOORBEELD.trainer} en '
                 f'{a.VOORBEELD.trainingsdag} om '
                 f'{a.VOORBEELD.trainingsuur}. En zij heeft betaald, dus bij '
                 'haar staat de aanmaningszin NIET.',
        vast=[
            'Je datum staat scheef: je hebt spaties gebruikt. Zet een rechtse '
            'tabstop.',
            'De aanmaningszin staat bij iedereen: je regel vergelijkt met de '
            f'verkeerde kolom. Vergelijk met {g.BRIEF_REGEL[0]}.',
            'Er staat een kommagetal in je tabel waar een bedrag of een datum '
            'hoort: je hebt de verkeerde van de twee kolommen genomen.',
            'Je voettekst staat midden in je tekst op de tweede bladzijde: je '
            'hebt ze getypt in plaats van ingevoegd.',
        ],
    ),
    dict(
        nr=4, titel='Een ploeglijst', soort='Lijst', lesuren=1,
        lijst=g.LEDEN_BLAD,
        fiches=[f.op_naam('Een lijst samenvoegen')],
        fiches_eerste=[11, 9],
        inleiding=[
            'De vierde soort, en de soort die niemand kent: een Lijst. Niet '
            'één bladzijde per lid, maar één REGEL per lid.',
            f'Je maakt de ploeglijst van {g.LIJST_BLAD_PLOEG} voor de '
            'trainer: een tabel met de leden onder elkaar, gesorteerd op '
            'achternaam.',
            'Er is één valkuil, en die kost je het hele uur als je hem niet '
            'kent. Bij een Lijst herhaalt Word niet een bladzijde per lid, '
            'maar HET HELE DOCUMENT. Zet je dus een koprij in je '
            'hoofddocument, dan komt die koprij bij elk lid opnieuw. In je '
            'hoofddocument staat ALLEEN die ene tabelrij.',
        ],
        stappen=[
            ('Lijst kiezen',
             'Nieuw, leeg Worddocument. Verzendlijsten, Afdruk samenvoegen '
             'starten, Lijst. (In een Engelse Word: Directory.)', 2),
            ('Filteren en sorteren',
             f'Hang {g.LEDEN_BLAD} eraan. Lijst met ontvangers bewerken, '
             f'Filteren: Ploeg is gelijk aan {g.LIJST_BLAD_PLOEG}. Dan '
             f'Sorteren op {g.LIJST_SORTEER}.', 3),
            ('Eén tabelrij met vier velden',
             f'Invoegen, Tabel, {len(g.LIJST_KOLOMMEN)} kolommen en 1 rij. '
             'In elke cel één veld: '
             + ' | '.join(f'«{k}»' for k in g.LIJST_KOLOMMEN)
             + '. Verder NIETS in het document. Dan Voltooien en samenvoegen, '
               'Afzonderlijke documenten bewerken.', 3),
        ],
        opmaak=[
            ('De koprij en de titel in het RESULTAAT',
             'Pas in het samengevoegde document zet je er een rij boven met '
             + ', '.join(g.LIJST_KOLOMMEN)
             + f', en daarboven een titel: Ploeglijst '
               f'{g.LIJST_BLAD_PLOEG} — {g.CLUB}. Maak de koprij vet en zet '
               'er een lijn onder. Bewaar als '
               f'ploeglijst-{g.LIJST_BLAD_PLOEG.lower()}-jouwnaam.docx.', 2),
            ('De tabel leesbaar maken',
             'Geef de kolommen een breedte die bij hun inhoud past — een '
             'geboortejaar heeft geen vier centimeter nodig. Zet de getallen '
             'rechts en de namen links.', 2),
        ],
        klaar=f'Een tabel met {a.AANTAL_LIJSTRIJEN} regels, één per lid van '
              f'{g.LIJST_BLAD_PLOEG}, op achternaam gesorteerd, met een '
              'koprij en een titel erboven.',
        controle=f'Er horen {a.AANTAL_LIJSTRIJEN} regels te staan, en de '
                 'koprij hoort er ÉÉN keer te staan. Staat ze er bij elk lid '
                 'opnieuw, dan stond ze in je hoofddocument.',
        vast=[
            'De koprij staat er zeven keer: hij stond in het hoofddocument. '
            'Haal hem daar weg, voeg opnieuw samen, en zet hem in het '
            'resultaat.',
            'Je krijgt één regel per bladzijde: je hebt Brieven gekozen in '
            'plaats van Lijst.',
            f'Er staan {a.AANTAL_LEDEN} regels: je filter staat niet aan.',
        ],
    ),
    dict(
        nr=5, titel='Eindopdracht: het tornooi', soort='Alles samen',
        lesuren=1, lijst=g.TORN_BLAD, brief=g.BRIEF_TORNOOI,
        fiches=[f.op_naam('Enveloppen'), f.op_naam('Een lijst samenvoegen'),
                f.op_naam('Tabstops in plaats van spaties'),
                f.op_naam('Kop- en voettekst'),
                f.op_naam('De opmaakklachten')],
        fiches_eerste=[10, 11],
        inleiding=[
            f'{g.CLUB} organiseert een tornooi. Op het werkblad '
            f'{g.TORN_BLAD} staan {a.AANTAL_CLUBS} clubs die willen '
            'deelnemen. Die lijst heb je nog niet gezien.',
            f'Open {g.BRIEF_TORNOOI}. Ook die brief staat er zonder opmaak '
            'in, en er staan GEEN markers. Jij beslist waar de velden horen '
            'en hoe het eruitziet.',
            'Drie documenten, in dit uur: de uitnodigingsbrief, de '
            'enveloppen, en één ploeglijst per categorie. Je hebt alle drie '
            'de soorten al gedaan — nu zonder dat erbij staat hoe.',
        ],
        stappen=[
            ('De uitnodigingsbrief',
             'Minstens deze velden: Club, de aanhef (Geachte, de '
             'aanspreking, de naam), Adresregel, Woonplaats, Categorie, '
             'Aantal ploegen en Inschrijvingsgeld in tekst. Eén regel met '
             f'Als…Dan…Anders: wie met {g.TORN_GROOT} ploegen of meer komt, '
             'krijgt een zin over een eigen kleedkamer. Bewaar als '
             'tornooibrief-jouwnaam.docx.', 6),
            ('Enveloppen voor de clubs',
             f'Alle {a.AANTAL_CLUBS}, met de clubnaam op de eerste regel van '
             'het adres. Bewaar als tornooienveloppen-jouwnaam.docx.', 4),
            (f'Een lijst van categorie {g.TORN_EIND_CATEGORIE}',
             f'Een Lijst-samenvoeging met een filter op Categorie = '
             f'{g.TORN_EIND_CATEGORIE}: club, contactpersoon, aantal ploegen '
             'en inschrijvingsgeld. Bewaar als '
             f'tornooilijst-{g.TORN_EIND_CATEGORIE.lower()}-jouwnaam.docx.',
             4),
        ],
        opmaak=[
            ('De brief ziet eruit als een brief',
             'Een briefhoofd, een datum rechts met een tabstop, een adresblok '
             'op de juiste plaats, en een voettekst met een paginanummer.', 4),
            ('De lijst is leesbaar',
             'Koprij vet met een lijn eronder, een titel erboven, en '
             'kolombreedtes die bij de inhoud passen.', 2),
            ('De enveloppen staan goed',
             'Afzender klein linksboven, geadresseerde in het grote kader '
             'rechtsonder.', 2),
        ],
        klaar=f'Drie documenten: {a.AANTAL_CLUBS} brieven waarvan '
              f'{a.AANTAL_EXTRA} met de extra zin, {a.AANTAL_CLUBS} '
              f'enveloppen, en één lijst met {a.AANTAL_EINDLIJST} regels.',
        controle=f'De brief van {a.CLUB_VOORBEELD.club} is gericht aan '
                 f'Geachte {a.CLUB_VOORBEELD.aanspreking} '
                 f'{a.CLUB_VOORBEELD.naam} en vermeldt '
                 f'{a.CLUB_VOORBEELD.geld_tekst}. Die club komt met '
                 f'{a.CLUB_VOORBEELD.aantal_ploegen} ploegen, dus bij hem '
                 'staat de extra zin NIET.',
        vast=[
            'Je weet niet meer hoe iets ging: dat staat in de twee '
            'theorieboekjes. Daar zijn ze voor.',
            'Je aanhef wordt "Geachte heer" zonder naam: je hebt het veld '
            'Naam niet meegenomen.',
            'Alles staat links en in dezelfde letter: dan heb je de opmaak '
            'overgeslagen, en daar staan acht van de vijfentwintig punten op.',
        ],
    ),
]


def vragen_van(stap):
    return [(i, v, antw) for i, (st, v, antw) in enumerate(a.ANTWOORDBLAD, 1)
            if st == stap['nr']]


def punten_van(stap):
    return (sum(p for *_, p in stap.get('stappen', []))
            + sum(p for *_, p in stap.get('opmaak', []))
            + len(vragen_van(stap)))


TOTAAL = sum(punten_van(s) for s in STAPPEN)
LESUREN = sum(s['lesuren'] for s in STAPPEN)
PUNTEN_OPMAAK = sum(p for s in STAPPEN for *_, p in s.get('opmaak', []))

if __name__ == '__main__':
    for stap in STAPPEN:
        werk = sum(p for *_, p in stap.get('stappen', []))
        opm = sum(p for *_, p in stap.get('opmaak', []))
        fiches = ', '.join(str(n) for n in stap['fiches'])
        print(f"stap {stap['nr']}  {stap['titel']:<28} {stap['soort']:<12} "
              f"{stap['lesuren']} u   fiche {fiches:<14} "
              f"werk {werk:>2} + opmaak {opm:>2} + vragen "
              f"{len(vragen_van(stap))} = {punten_van(stap):>3}")
    print(f'\n{TOTAAL} punten ({PUNTEN_OPMAAK} op opmaak), {LESUREN} lesuren')
