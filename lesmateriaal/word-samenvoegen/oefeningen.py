# -*- coding: utf-8 -*-
"""De vijf stappen. Eén lesuur per stap, twee voor de eindopdracht.

Er staat geen theorie in de opdracht: die staat in samenvoegen-theorie.docx,
en bij elke stap staat welke fiches je nodig hebt.
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

THEORIEBUNDEL = "samenvoegen-theorie.docx"
STARTBESTAND = "samenvoegen-startbestand.xlsx"
BRIEF_VRIJ = "samenvoegen-brief-vrijwilligers.docx"
BRIEF_SPON = "samenvoegen-brief-sponsors.docx"

# De markers die in de vrijwilligersbrief staan, in de volgorde waarin ze er
# staan. Zowel het briefmodel als de opdracht worden hieruit opgebouwd, zodat
# ze nooit uit elkaar kunnen lopen.
BRIEF_VRIJ_MARKERS = ['Voornaam', 'Achternaam', 'Aanhef', 'Adresregel',
                      'Woonplaats', 'Taak', 'Startuur', 'Vergoeding']
# En de velden die in de sponsorbrief MOETEN voorkomen; waar, bepalen ze zelf.
BRIEF_SPON_VELDEN = ['Bedrijf', 'Aanhef', 'Adresregel', 'Woonplaats',
                     'Pakket', 'Bedrag in tekst']


def marker(naam):
    return f'[[{naam}]]'


# Wat er op één etiket komt: drie regels, en per regel welke velden.
ETIKET_REGELS = [['Voornaam', 'Achternaam'], ['Adresregel'], ['Woonplaats']]


def _fiche(naam):
    for i, kaart in enumerate(f.FICHES, 1):
        if kaart['naam'] == naam:
            return i
    raise KeyError(f'fiche {naam!r} bestaat niet — de fiches heten: '
                   f'{[k["naam"] for k in f.FICHES]}')


def _kol(n):
    uit = ''
    while n:
        n, r = divmod(n - 1, 26)
        uit = chr(65 + r) + uit
    return uit


# de kolom waarin elke te maken kolom staat, afgeleid uit de koprij
def _kolomletter(blad_kop, naam):
    if naam not in blad_kop:
        raise KeyError(
            f'de opdracht verwijst naar een kolom {naam!r} die niet in de '
            f'koprij staat. De kolommen heten: {blad_kop}')
    return _kol(blad_kop.index(naam) + 1)


V = g.VRIJ_KOP
S = g.SPON_KOP
_vr = f'{g.VRIJ_START}'
_sp = f'{g.SPON_START}'
_taken = (f'{g.TAKEN_BLAD}!${_kol(1)}${g.TAKEN_START}:'
          f'${_kol(len(g.TAKEN_KOP))}${g.TAKEN_EIND}')
_code = f'{_kolomletter(V, "Taakcode")}{_vr}'

STAPPEN = [
    dict(
        nr=1, titel='De lijst samenvoegklaar maken', waar='Excel',
        blad=g.VRIJ_BLAD, lesuren=1,
        fiches=[_fiche('Wat Word van je lijst verwacht'), _fiche('Plakken met &'),
                _fiche('VERT.ZOEKEN'), _fiche('TEKST')],
        inleiding=[
            f'Op het werkblad {g.VRIJ_BLAD} staan {len(g.VRIJWILLIGERS)} '
            f'vrijwilligers voor {g.FESTIVAL} {g.EDITIE}. De eerste acht '
            'kolommen staan klaar. De acht daarna maak jij.',
            'Dit is de belangrijkste stap van de hele reeks, en ook de enige '
            'waar je formules typt. Wat je hier goed zet, hoef je in Word niet '
            'meer op te lossen. Wat je hier overslaat, kom je in elke brief '
            'tegen.',
            f'De peildatum waarmee je de leeftijd uitrekent, staat op het '
            f'blad {g.START_BLAD}, op {g.PEILCEL}. Niet bij de lijst — op een '
            'blad dat Word moet lezen, mag niets boven of naast de koprij '
            'staan. Fiche 1 legt uit waarom.',
            'Let vooral op de kolommen Startuur en Vergoeding. Op je scherm '
            'staat er in de takentabel netjes 14:00 en € 45,00 — maar dat is '
            'alleen de OPMAAK van die cellen, en opmaak gaat niet mee naar '
            'Word. Daarom zet je de vorm met TEKST in de cel zelf.',
        ],
        vullen=[
            (f'{_kolomletter(V, "Aanhef")}', 'Aanhef',
             'het woord Beste, een spatie, en de voornaam. Niets meer. Je '
             'typt hier NERGENS zelf mevrouw of mijnheer: dat staat niet in '
             'deze lijst, en vrijwilligers spreek je met hun voornaam aan',
             f'="Beste "&{_kolomletter(V, "Voornaam")}{_vr}', 2),
            (f'{_kolomletter(V, "Adresregel")}', 'Adresregel',
             'de straat, één spatie, en het huisnummer — in die volgorde, op '
             'één regel',
             f'={_kolomletter(V, "Straat")}{_vr}&" "'
             f'&{_kolomletter(V, "Nummer")}{_vr}', 2),
            (f'{_kolomletter(V, "Woonplaats")}', 'Woonplaats',
             'de postcode, één spatie, en de gemeente — in die volgorde, op '
             'één regel',
             f'={_kolomletter(V, "Postcode")}{_vr}&" "'
             f'&{_kolomletter(V, "Gemeente")}{_vr}', 2),
            (f'{_kolomletter(V, "Taak")}', 'Taak',
             f'de taak die bij de taakcode hoort, opgezocht op het werkblad '
             f'{g.TAKEN_BLAD} (kolom 2 van die tabel)',
             f'=VERT.ZOEKEN({_code};{_taken};2;ONWAAR)', 2),
            (f'{_kolomletter(V, "Startuur")}', 'Startuur',
             f'het startuur uit {g.TAKEN_BLAD} (kolom 4), omgezet naar TEKST '
             'in de vorm uu:mm — twee cijfers, een dubbele punt, twee cijfers',
             f'=TEKST(VERT.ZOEKEN({_code};{_taken};4;ONWAAR);"uu:mm")', 2),
            (f'{_kolomletter(V, "Vergoeding")}', 'Vergoeding',
             f'de vergoeding uit {g.TAKEN_BLAD} (kolom 5), omgezet naar TEKST '
             'met een euroteken, een spatie en twee cijfers achter de komma',
             f'=TEKST(VERT.ZOEKEN({_code};{_taken};5;ONWAAR);"€ #.##0,00")', 2),
            (f'{_kolomletter(V, "Leeftijd")}', 'Leeftijd',
             f'de leeftijd in HELE jaren op {g.datum(g.FESTIVALDAG)}, als '
             f'gewoon getal. Reken met de peildatum op {g.PEILCEL}',
             f'=DATUMVERSCHIL({_kolomletter(V, "Geboortedatum")}{_vr};'
             f'{g.PEILCEL};"J")', 2),
            (f'{_kolomletter(V, "Begeleiding")}', 'Begeleiding',
             f'het woord ja als de leeftijd onder {g.MEERDERJARIG} ligt, en '
             'anders het woord nee. Klein geschreven, zonder punt — Word gaat '
             'er in stap 4 letterlijk mee vergelijken',
             f'=ALS({_kolomletter(V, "Leeftijd")}{_vr}<{g.MEERDERJARIG};'
             '"ja";"nee")', 2),
        ],
        klaar=f'Acht volle kolommen, {len(g.VRIJWILLIGERS)} rijen diep. Geen '
              '#N/B, geen #WAARDE!, en in de kolom Vergoeding een euroteken.',
        controle=f'In de kolom Vergoeding moet overal een € staan. Staat er '
                 'een kaal getal, dan heb je de TEKST eromheen vergeten en '
                 'loopt het in stap 3 mis.',
        vast=[
            '#N/B onderaan de kolom Taak: de zoektabel is niet vastgezet met '
            'dollartekens.',
            'In de kolom Startuur staat 0,5833: je hebt de TEKST eromheen '
            'vergeten, of je hebt de cel alleen opgemaakt.',
            'In de kolom Leeftijd staat een datum: zet de getalnotatie van die '
            'kolom op Standaard.',
        ],
    ),
    dict(
        nr=2, titel='Etiketten', waar='Word', lesuren=1,
        fiches=[_fiche('Wat afdruk samenvoegen is'),
                _fiche('De lijst aan je document hangen'),
                _fiche('Samenvoegvelden invoegen'), _fiche('Etiketten'),
                _fiche('Voorbeeld, en voltooien')],
        inleiding=[
            'Je eerste samenvoeging, en met opzet de eenvoudigste: een vel '
            'adresetiketten voor de enveloppen.',
            'Je begint met een LEEG Worddocument. Alles wat je nodig hebt, '
            'zit op het tabblad Verzendlijsten.',
            f'De lijst die je gebruikt is het werkblad {g.VRIJ_BLAD} uit '
            f'{STARTBESTAND} — de lijst die je in stap 1 hebt afgemaakt. Zet '
            'allebei de bestanden in dezelfde map voor je begint.',
        ],
        etiket=ETIKET_REGELS,
        stappen=[
            ('Nieuw Worddocument, en kies Etiketten',
             f'Verzendlijsten, Afdruk samenvoegen starten, Etiketten. Kies '
             f'{g.ETIKET_SOORT}. Staat dat formaat er niet bij, neem er dan '
             f'een met {g.ETIKET_PER_BLAD} etiketten per blad en schrijf op '
             'welk formaat je genomen hebt.', 2),
            ('Hang je lijst eraan',
             f'Adressen selecteren, Een bestaande lijst gebruiken, '
             f'{STARTBESTAND}, werkblad {g.VRIJ_BLAD}. Laat "De eerste rij '
             'bevat kolomnamen" aangevinkt.', 3),
            ('Vul het EERSTE etiket in',
             f'{len(ETIKET_REGELS)} regels, in deze volgorde: '
             + ' / '.join(' '.join(f'«{v}»' for v in regel)
                          for regel in ETIKET_REGELS)
             + '. Druk na elke regel op Enter. Gebruik Samenvoegveld '
               'invoegen — typ de punthaken niet zelf, en typ er geen komma '
               'of punt bij.', 3),
            ('Labels bijwerken',
             'Verzendlijsten, Labels bijwerken. Nu staat hetzelfde op alle '
             'etiketten. Sla deze stap niet over.', 2),
            ('Voorbeeld en voltooien',
             'Voorbeeld van resultaten, loop even door de records, dan '
             'Voltooien en samenvoegen, Afzonderlijke documenten bewerken. '
             'Bewaar als etiketten-jouwnaam.docx.', 1),
        ],
        klaar=f'Een document met {a.ETIKET_BLADEN} bladen etiketten, '
              f'{a.AANTAL_VRIJ} gevuld en {a.ETIKET_LEEG_OP_LAATSTE} leeg op '
              'het laatste blad.',
        controle='Op elk etiket staat een ANDERE naam. Staat overal dezelfde, '
                 'dan heb je Labels bijwerken gedaan maar niet samengevoegd; '
                 'staat alleen het eerste etiket gevuld, dan omgekeerd.',
        vast=[
            'Alleen het eerste etiket is gevuld: Labels bijwerken vergeten.',
            'De punthaken blijven staan: zet Voorbeeld van resultaten aan, of '
            'je hebt ze zelf getypt.',
            'Word vindt je lijst niet: het Excelbestand staat in een andere '
            'map dan toen je het koppelde.',
        ],
    ),
    dict(
        nr=3, titel='De brief', waar='Word', lesuren=1,
        fiches=[_fiche('De lijst aan je document hangen'),
                _fiche('Samenvoegvelden invoegen'),
                _fiche('Voorbeeld, en voltooien'),
                _fiche('De opmaak komt niet mee')],
        inleiding=[
            f'Open {BRIEF_VRIJ}. De brief staat er al in; jij hoeft hem niet '
            'te typen.',
            'Overal waar iets persoonlijks komt, staat een oranje marker '
            'tussen dubbele haken, zoals [[Aanhef]]. Elke marker vervang je '
            'door het samenvoegveld met dezelfde naam. De marker verwijder '
            'je, het veld komt ervoor in de plaats.',
            'Hier merk je waarom stap 1 nodig was. Gebruik je kolommen '
            'Startuur en Vergoeding — die met TEKST — dan staat er netjes '
            f'{a.VOORBEELD_EERSTE.startuur} en '
            f'{a.VOORBEELD_EERSTE.vergoeding}. Gebruik je de kolommen uit de '
            'takentabel, dan niet.',
        ],
        stappen=[
            ('Bewaar de brief onder je eigen naam',
             'Bestand, Opslaan als, brief-jouwnaam.docx. Werk daarin, niet in '
             'het model.', 2),
            ('Maak er een hoofddocument van',
             f'Verzendlijsten, Afdruk samenvoegen starten, Brieven. Dan '
             f'Adressen selecteren, werkblad {g.VRIJ_BLAD}.', 4),
            (f'Vervang de {len(BRIEF_VRIJ_MARKERS)} markers door '
             'samenvoegvelden',
             ', '.join(marker(m) for m in BRIEF_VRIJ_MARKERS)
             + '. Zet je cursor op de marker, verwijder hem, en voeg het veld '
               'in. Dezelfde marker kan twee keer voorkomen.', 6),
            ('Kijk na en voeg samen',
             'Voorbeeld van resultaten: kijk naar brief 1, naar een brief uit '
             'het midden en naar de laatste. Dan Voltooien en samenvoegen, '
             'Afzonderlijke documenten bewerken. Bewaar als '
             'brieven-jouwnaam.docx.', 4),
        ],
        klaar=f'{a.AANTAL_BRIEVEN} brieven, elk op een eigen pagina, met een '
              'naam, een adres, een taak, een startuur en een vergoeding die '
              'per brief verschillen.',
        controle=f'In de brief van {a.VOORBEELD_EERSTE.naam} staat taak '
                 f'{a.VOORBEELD_EERSTE.taak}, startuur '
                 f'{a.VOORBEELD_EERSTE.startuur} en vergoeding '
                 f'{a.VOORBEELD_EERSTE.vergoeding}.',
        vast=[
            'Er staat 0,5833 in plaats van een uur: je hebt het veld uit de '
            'takentabel gebruikt in plaats van je eigen tekstkolom. Fiche '
            f'{_fiche("De opmaak komt niet mee")} legt uit wat je eraan doet.',
            'De marker staat er nog naast je veld: je hebt het veld ervoor '
            'gezet in plaats van de marker te verwijderen.',
            'Alle brieven zijn identiek: Voorbeeld van resultaten staat af, of '
            'je hebt gewone tekst getypt in plaats van velden.',
        ],
    ),
    dict(
        nr=4, titel='Regels en filters', waar='Word', lesuren=1,
        fiches=[_fiche('Als…Dan…Anders'),
                _fiche('Ontvangers filteren en sorteren'),
                _fiche('De vijf klachten')],
        inleiding=[
            'Je brief van stap 3 is voor iedereen hetzelfde, op de velden na. '
            'Nu ga je er een zin in zetten die alleen voor sommige mensen '
            'geldt.',
            f'{a.AANTAL_MINDERJARIG} van de {a.AANTAL_VRIJ} vrijwilligers zijn '
            f'op de festivaldag nog geen {g.MEERDERJARIG}. Zij moeten een '
            'toelating van thuis meebrengen. Die zin hoort alleen in hun '
            'brief.',
            'Daarna leer je ontvangers filteren en sorteren — handig als je '
            'maar één ploeg wil aanschrijven, of als je de brieven per '
            'gemeente wil bundelen.',
        ],
        stappen=[
            ('Zet de regel in je brief',
             'Werk verder in brief-jouwnaam.docx. Zet je cursor op de regel '
             'onder de alinea over je taak. Verzendlijsten, Regels, '
             'Als…Dan…Anders. Veld Begeleiding, is gelijk aan, ja. Typ bij '
             '"Deze tekst invoegen": Omdat je op het festival nog geen 18 '
             'bent, breng je een ondertekende toelating van je ouders mee. '
             'Laat het andere vak leeg.', 6),
            ('Filter op één podium',
             f'Lijst met ontvangers bewerken, Filteren. Podium is gelijk aan '
             f'{g.FILTER_PODIUM}. Kijk hoeveel brieven er overblijven en '
             'schrijf dat op. Zet het filter daarna weer AF.', 3),
            ('Sorteer op postcode',
             'Lijst met ontvangers bewerken, Sorteren, op Postcode. Voeg '
             'opnieuw samen en bewaar als brieven-gesorteerd-jouwnaam.docx.',
             3),
        ],
        klaar=f'Twee samengevoegde documenten: één met alle '
              f'{a.AANTAL_BRIEVEN} brieven op postcode gesorteerd, en in '
              f'{a.AANTAL_MINDERJARIG} daarvan de extra zin.',
        controle=f'De extra zin staat in {a.AANTAL_MINDERJARIG} brieven. Staat '
                 f'ze in alle {a.AANTAL_BRIEVEN}, dan vergelijkt je regel met '
                 'het verkeerde veld; staat ze nergens, dan staat er "Ja" met '
                 'een hoofdletter in je vergelijking.',
        vast=[
            f'De zin staat in alle {a.AANTAL_BRIEVEN} brieven: je regel '
            'vergelijkt met een kolom die altijd gevuld is. Vergelijk met '
            'Begeleiding, niet met Leeftijd.',
            'Er komen maar zes brieven uit terwijl het filter af staat: er '
            'staan nog vinkjes uit bij Lijst met ontvangers bewerken.',
            'Je ziet de regel niet terug in je document. Dat hoort: druk '
            'Alt+F9 om het veld zelf te zien.',
        ],
    ),
    dict(
        nr=5, titel='Eindopdracht: de sponsorbrief', waar='Excel en Word',
        blad=g.SPON_BLAD, lesuren=2,
        fiches=[_fiche('Plakken met &'), _fiche('TEKST'),
                _fiche('Samenvoegvelden invoegen'), _fiche('Etiketten'),
                _fiche('Als…Dan…Anders'),
                _fiche('Ontvangers filteren en sorteren')],
        inleiding=[
            f'Nu alles zelf, op een lijst die je nog niet gezien hebt: op het '
            f'werkblad {g.SPON_BLAD} staan {len(g.SPONSORS)} bedrijven die '
            f'{g.FESTIVAL} steunen.',
            f'Open {BRIEF_SPON}. De brief staat er al in, maar er staan GEEN '
            'markers. Jij beslist waar de samenvoegvelden horen — en welke '
            f'van de {len(BRIEF_SPON_VELDEN)} gevraagde velden waar hoort.',
            'Er is één verschil met de vrijwilligersbrief: de aanhef is '
            'zakelijk. Niet "Beste Karel" maar "Geachte de heer Van Hoof". '
            'Daar heb je twee kolommen voor nodig, niet één.',
            'Dit is de eindopdracht. Er staat niet meer stap voor stap bij hoe '
            'het moet — dat weet je nu. Wat er wél bij staat, is wat er in '
            'moet zitten.',
        ],
        vullen=[
            (f'{_kolomletter(S, "Aanhef")}', 'Aanhef',
             'het woord Geachte, een spatie, de aanspreking uit kolom '
             f'{_kolomletter(S, "Aanspreking")}, een spatie, en de naam uit '
             f'kolom {_kolomletter(S, "Naam")}. Hier is het dus WEL zakelijk — '
             'maar ook hier typ je de aanspreking niet zelf: ze staat in de '
             'lijst, en ze is niet voor iedereen hetzelfde',
             f'="Geachte "&{_kolomletter(S, "Aanspreking")}{_sp}&" "'
             f'&{_kolomletter(S, "Naam")}{_sp}', 3),
            (f'{_kolomletter(S, "Adresregel")}', 'Adresregel',
             'de straat, één spatie, en het huisnummer',
             f'={_kolomletter(S, "Straat")}{_sp}&" "'
             f'&{_kolomletter(S, "Nummer")}{_sp}', 3),
            (f'{_kolomletter(S, "Woonplaats")}', 'Woonplaats',
             'de postcode, één spatie, en de gemeente',
             f'={_kolomletter(S, "Postcode")}{_sp}&" "'
             f'&{_kolomletter(S, "Gemeente")}{_sp}', 3),
            (f'{_kolomletter(S, "Bedrag in tekst")}', 'Bedrag in tekst',
             'het bedrag omgezet naar TEKST met een euroteken en twee cijfers '
             'achter de komma, precies zoals de kolom Vergoeding in stap 1',
             f'=TEKST({_kolomletter(S, "Bedrag")}{_sp};"€ #.##0,00")', 3),
        ],
        stappen=[
            ('De brief, met minstens vijf velden',
             'Bedrijf, Aanhef, Adresregel, Woonplaats, Pakket en Bedrag in '
             'tekst. Bewaar als sponsorbrief-jouwnaam.docx en voeg samen.', 6),
            ('Eén regel met Als…Dan…Anders',
             f'Wie {g.euro(g.SPON_DREMPEL)} of meer geeft, krijgt een extra '
             'zin: een uitnodiging voor de sponsoravond. De anderen niet. '
             'Gebruik het veld Bedrag.', 5),
            ('Etiketten voor de enveloppen',
             f'Eén vel etiketten voor de {len(g.SPONSORS)} bedrijven, met het '
             'bedrijf op de eerste regel. Bewaar als '
             'sponsoretiketten-jouwnaam.docx.', 3),
            ('Gesorteerd op postcode',
             'Sorteer de ontvangers op postcode voor je de etiketten '
             'samenvoegt.', 2),
        ],
        klaar=f'Vier volle kolommen in Excel, {a.AANTAL_SPON} sponsorbrieven '
              f'waarvan {a.AANTAL_SPON_EXTRA} met de extra zin, en één vel '
              'etiketten op postcode gesorteerd.',
        controle=f'{a.AANTAL_SPON_EXTRA} van de {a.AANTAL_SPON} brieven '
                 f'krijgen de extra zin. In de brief van '
                 f'{a.SPON_VOORBEELD.bedrijf} staat "{a.SPON_VOORBEELD.aanhef}" '
                 f'en {a.SPON_VOORBEELD.bedrag_tekst}.',
        vast=[
            'Er staat "Geachte de heer" zonder naam: je hebt de kolom Naam '
            'niet meegeplakt.',
            'De extra zin staat bij niemand of bij iedereen: Word vergelijkt '
            'het bedrag soms als tekst. Maak in Excel een hulpkolom met ja of '
            'nee en vergelijk daarmee — net zoals bij Begeleiding in stap 4.',
            f'Er staat {int(g.SPON_DREMPEL)} in plaats van '
            f'{g.euro(g.SPON_DREMPEL)}: gebruik je kolom Bedrag in tekst.',
        ],
    ),
]


def punten_van(stap):
    return (sum(p for *_, p in stap.get('vullen', []))
            + sum(p for *_, p in stap.get('stappen', []))
            + sum(1 for st, _v, _a in a.ANTWOORDBLAD if st == stap['nr']))


TOTAAL = sum(punten_van(s) for s in STAPPEN)
LESUREN = sum(s['lesuren'] for s in STAPPEN)

if __name__ == '__main__':
    for stap in STAPPEN:
        vragen = sum(1 for st, _v, _a in a.ANTWOORDBLAD if st == stap['nr'])
        fiches = ', '.join(str(n) for n in stap['fiches'])
        print(f"stap {stap['nr']}  {stap['titel']:<34} {stap['waar']:<16} "
              f"{stap['lesuren']} lesu.   fiche {fiches:<16} "
              f"{vragen} vragen   {punten_van(stap)} punten")
    print(f'\n{TOTAAL} punten, {LESUREN} lesuren')
