# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad maakt.

De fiches staan in deze bundel zelf (fiches.py). Alleen de draaitabel en de
draaigrafiek van blad 5 verwijzen naar het boekje dat ze al hebben.
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


def _kol(n):
    uit = ''
    while n:
        n, r = divmod(n - 1, 26)
        uit = chr(65 + r) + uit
    return uit


def _fiche(naam):
    """Het nummer van een fiche opzoeken, zodat geen enkel nummer vastligt."""
    for i, kaart in enumerate(f.FICHES, 1):
        if kaart['naam'] == naam:
            return i
    raise KeyError(f'fiche {naam!r} bestaat niet — de fiches heten: '
                   f'{[k["naam"] for k in f.FICHES]}')


V1, V2, V3, V4, V5 = 7, 6, 6, 7, 6     # kolom van het vragenblok per blad

_LAND = len(g.B1_LANDEN[0])
_JAAR = len(str(g.B1[0][2]))

OEFENINGEN = [
    dict(
        nr=1, blad='1 Artiestcodes', titel='Het begin en het einde',
        duur='8 minuten',
        fiches=[_fiche('LINKS en RECHTS'), _fiche('WAARDE')],
        inleiding=[
            f'{len(g.B1)} acts met hun artiestcode. In die code zit het land '
            'en het jaar waarin ze hier voor het eerst speelden, maar je kan '
            'er niets mee zolang ze aan elkaar plakken.',
            f'Elke code is even lang: {_LAND} letters land, {_JAAR} cijfers '
            'jaar. Daarom kan je hier gewoon tellen vanaf het begin en vanaf '
            'het einde.',
            'De derde kolom lijkt overbodig en is dat niet. Kijk goed naar de '
            'tweede vraag voor je ze overslaat.',
        ],
        vullen=[
            (f'C{g.B1_START}:C{g.B1_EIND}', 'de landcode',
             f'=LINKS(B{g.B1_START};{_LAND})', 2),
            (f'D{g.B1_START}:D{g.B1_EIND}', 'het jaar, zoals het eruit komt',
             f'=RECHTS(B{g.B1_START};{_JAAR})', 2),
            (f'E{g.B1_START}:E{g.B1_EIND}', 'hetzelfde jaar, maar als getal',
             f'=WAARDE(D{g.B1_START})', 2),
        ],
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}',
             'van welk land er de meeste acts komen (de landcode volstaat)',
             a.B1_MEESTE_LAND, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'wat het vroegste jaar in de lijst is', a.B1_VROEGSTE, 1),
        ],
        klaar='Drie volle kolommen. Kolom D staat links in de cel, kolom E '
              'rechts.',
        controle=f'Zet onder kolom D eens =MIN(D{g.B1_START}:D{g.B1_EIND}) en '
                 f'onder kolom E =MIN(E{g.B1_START}:E{g.B1_EIND}). De eerste '
                 f'geeft 0, de tweede {a.B1_VROEGSTE}. Dat verschil is het '
                 'hele punt van kolom E.',
        vast=[
            'Je krijgt het hele codeveld terug in plaats van twee letters: je '
            'hebt het aantal tekens vergeten of te hoog gezet.',
            'MIN geeft 0 terwijl er jaartallen staan. Dan reken je op tekst. '
            'Dat is precies waarom kolom E bestaat.',
        ],
    ),
    dict(
        nr=2, blad='2 Podia', titel='Zoeken waar je moet knippen',
        duur='12 minuten',
        fiches=[_fiche('VIND.ALLES'), _fiche('LENGTE'),
                _fiche('LINKS en RECHTS')],
        inleiding=[
            f'{len(g.B2)} regels zoals ze uit het systeem komen: podium en '
            f'artiest in één cel, met {g.B2_SCHEIDING.strip()} ertussen.',
            'Hier werkt de aanpak van blad 1 niet. "Klub C" is zes tekens, '
            '"Main Stage" is er tien. Je moet Excel eerst laten zoeken waar '
            'het streepje staat.',
            'Dit is het moeilijkste blad van de bundel. Neem er de tijd voor '
            'en tel één regel op papier uit voor je begint.',
        ],
        vullen=[
            (f'B{g.B2_START}:B{g.B2_EIND}', 'het podium',
             f'=LINKS(A{g.B2_START};VIND.ALLES("|";A{g.B2_START})-2)', 3),
            (f'C{g.B2_START}:C{g.B2_EIND}', 'de artiest',
             f'=RECHTS(A{g.B2_START};LENGTE(A{g.B2_START})'
             f'-VIND.ALLES("|";A{g.B2_START})-1)', 3),
            (f'D{g.B2_START}:D{g.B2_EIND}', 'hoeveel tekens die naam telt',
             f'=LENGTE(C{g.B2_START})', 2),
        ],
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'welk podium de meeste acts heeft', a.B2_MEESTE_PODIUM, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}',
             f'hoeveel acts er op {a.B2_TELPODIUM} staan',
             a.B2_TELPODIUM_AANTAL, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'hoeveel tekens de langste artiestennaam telt',
             a.B2_LANGSTE_LENGTE, 1),
        ],
        klaar='Kolom B en C zonder streepjes en zonder spaties aan de randen.',
        controle=f'De langste naam telt {a.B2_LANGSTE_LENGTE} tekens. Staat er '
                 f'{a.B2_LANGSTE_LENGTE + 1}, dan zit er nog een spatie voor: '
                 'je -1 achteraan ontbreekt.',
        vast=[
            'Je podium eindigt op een spatie. De -2 achter VIND.ALLES '
            'ontbreekt: één voor het streepje zelf, één voor de spatie ervoor.',
            'Je artiest begint met een spatie. Dan mist de -1 achteraan.',
            'Je krijgt #WAARDE!. Controleer of het streepje tussen '
            'aanhalingstekens staat en of je eerst WAT en dan WAAR hebt gezet.',
        ],
    ),
    dict(
        nr=3, blad='3 Boekingscodes', titel='Een stuk uit het midden',
        duur='10 minuten',
        fiches=[_fiche('DEEL'), _fiche('WAARDE')],
        inleiding=[
            f'{len(g.B3)} boekingscodes. Ze zijn allemaal op dezelfde manier '
            f'gebouwd en allemaal {a.B3_CODELENGTE} tekens lang.',
            'Dat maakt het makkelijker dan blad 2, niet moeilijker: je hoeft '
            'niets te zoeken. Tel één keer uit waar elk stuk begint en de rest '
            'volgt vanzelf.',
        ],
        vullen=[
            (f'B{g.B3_START}:B{g.B3_EIND}', 'de dag',
             f'=DEEL(A{g.B3_START};{a.B3_POS_DAG};{a.B3_LEN_DAG})', 2),
            (f'C{g.B3_START}:C{g.B3_EIND}', 'de podiumcode',
             f'=DEEL(A{g.B3_START};{a.B3_POS_PODIUM};{a.B3_LEN_PODIUM})', 2),
            (f'D{g.B3_START}:D{g.B3_EIND}', 'het volgnummer, als getal',
             f'=WAARDE(RECHTS(A{g.B3_START};{a.B3_LEN_VOLGNUMMER}))', 2),
        ],
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'op welke dag de meeste acts staan', a.B3_DRUKSTE_DAG, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'welk podium de minste acts heeft', a.B3_MINSTE_PODIUM, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 3}',
             'wat het hoogste volgnummer is', a.B3_HOOGSTE_VOLGNUMMER, 1),
        ],
        klaar='Drie kolommen zonder streepjes erin, en kolom D rechts in de '
              'cel.',
        controle=f'In kolom B mag alleen {", ".join(g.B3_DAGEN)} staan en in '
                 f'kolom C alleen {", ".join(g.B3_PODIUMCODES)}. Zie je ergens '
                 'een streepje, dan zit je er één teken naast.',
        vast=[
            'Er staat een streepje in je antwoord. Je "vanaf" moet eentje '
            'hoger, of je "aantal" eentje lager.',
            f'MAX op kolom D geeft 0. Dan is het nog tekst en mist de WAARDE '
            'eromheen.',
        ],
    ),
    dict(
        nr=4, blad='4 Vrijwilligers', titel='Opkuisen en samenplakken',
        duur='10 minuten',
        fiches=[_fiche('SPATIES.WISSEN'), _fiche('BEGINLETTERS'),
                _fiche('SUBSTITUEREN'), _fiche('Plakken met &')],
        inleiding=[
            f'{len(g.B4)} vrijwilligers, aangemeld via drie verschillende '
            'formulieren. De namen staan er door elkaar in: hoofdletters, '
            'kleine letters, en spaties waar ze niet horen.',
            'Je maakt er één nette naam van en daarna een e-mailadres. Bouw '
            'dat op in twee stappen — eerst de naam in kolom C, dan het adres '
            'uit kolom C. Eén lange formule in één keer is vragen om fouten.',
            'Let op de dubbele achternamen. De spatie MIDDEN in "De Smet" moet '
            'in de naam blijven staan en in het adres een punt worden.',
        ],
        vullen=[
            (f'C{g.B4_START}:C{g.B4_EIND}', 'de nette naam: voornaam, spatie, '
             'achternaam',
             f'=BEGINLETTERS(SPATIES.WISSEN(B{g.B4_START}))&" "'
             f'&BEGINLETTERS(SPATIES.WISSEN(A{g.B4_START}))', 2),
            (f'D{g.B4_START}:D{g.B4_EIND}', 'het e-mailadres',
             f'=KLEINE.LETTERS(SUBSTITUEREN(C{g.B4_START};" ";"."))'
             f'&"@{g.DOMEIN}"', 3),
            (f'E{g.B4_START}:E{g.B4_EIND}', 'hoeveel tekens dat adres telt',
             f'=LENGTE(D{g.B4_START})', 1),
        ],
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             'hoeveel tekens het langste e-mailadres telt',
             a.B4_LANGSTE_LENGTE, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             'van wie dat adres is (de nette naam)', a.B4_LANGSTE_NAAM, 1),
        ],
        klaar='Zestien nette namen en zestien adressen, allemaal in kleine '
              f'letters en allemaal eindigend op @{g.DOMEIN}.',
        controle=f'Het langste adres telt {a.B4_LANGSTE_LENGTE} tekens. Tel er '
                 'nergens een spatie in: zoek met Ctrl+F naar een spatie in '
                 'kolom D en je hoort niets te vinden.',
        vast=[
            'In je adres staat nog een spatie. SPATIES.WISSEN haalt alleen de '
            'spaties aan de randen weg; voor die ene midden in heb je '
            'SUBSTITUEREN nodig.',
            'Je naam staat aan elkaar geplakt zonder spatie. De &" "& ertussen '
            'ontbreekt.',
            'Je adres begint met een hoofdletter. Zet KLEINE.LETTERS om het '
            'hele stuk, niet alleen om een deeltje.',
        ],
    ),
    dict(
        nr=5, blad='5 Line-up', titel='Opkuisen, tabel, draaitabel, slicer',
        duur='10 minuten',
        fiches=[_fiche('Duplicaten verwijderen'),
                _fiche('Een tabel maken (Ctrl+T)'), _fiche('Een slicer')],
        kaarten_elders=[3, 4, 13],
        inleiding=[
            f'De volledige line-up, {len(g.B5_EXPORT)} regels, uit twee '
            'systemen samengevoegd. Een paar acts staan er daardoor twee keer '
            'in.',
            'Geen formules op dit blad. Je kuist op, maakt er een tabel van en '
            'zet er een draaitabel, een draaigrafiek en een slicer op.',
            'De volgorde doet ertoe: eerst de dubbels eruit, dan pas tellen. '
            'Doe je het omgekeerd, dan tel je iets wat er niet is.',
        ],
        stappen=[
            ('Duplicaten verwijderen', 'Gegevens, Duplicaten verwijderen. '
             'Laat alle vier de kolommen aangevinkt. Lees hoeveel regels '
             'Excel weggooit.', 2),
            ('De lijst een tabel maken', 'Klik erin en druk Ctrl+T. '
             'Kopteksten aangevinkt laten.', 2),
            ('Een draaitabel erop', f'Rijen: {g.B5_DRAAI_RIJEN}. Waarden: '
             f'Aantal van {g.B5_DRAAI_WAARDEN}. Laat Excel ze op een nieuw '
             'werkblad zetten; dat is de standaard en dan zit je niets in de '
             'weg.', 3),
            ('Een draaigrafiek erbij', 'Klik je draaitabel aan, Draaitabel '
             'analyseren, Draaigrafiek. Een staafdiagram volstaat. Geef hem '
             'een titel.', 3),
            ('Een slicer erop', f'Draaitabel analyseren, Slicer invoegen, veld '
             f'{g.B5_SLICER_VELD}. Klik daarna op {g.B5_SLICER_KEUZE} en kijk '
             'wat je grafiek doet.', 1),
        ],
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}',
             'hoeveel regels Excel weggooit bij Duplicaten verwijderen',
             a.B5_DUBBELE_REGELS, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}',
             'wat het eindtotaal van je draaitabel is', a.B5_DRAAI_TOTAAL, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}',
             f'hoeveel acts er overblijven met de slicer op '
             f'{g.B5_SLICER_KEUZE}', a.B5_SLICER_AANTAL, 1),
        ],
        klaar='Een tabel met kleur en filterpijltjes, een draaitabel van '
              f'{len(a.B5_DRAAI_LABELS)} podia, een staafdiagram ernaast en '
              f'een slicer met {len(g.B5_GENRES)} knoppen.',
        controle=f'Het eindtotaal van je draaitabel moet {a.B5_DRAAI_TOTAAL} '
                 f'zijn. Staat er {len(g.B5_EXPORT)}, dan heb je de dubbels '
                 'nog niet verwijderd.',
        vast=[
            'Duplicaten verwijderen vindt niets. Je hebt maar één kolom '
            'aangevinkt gelaten, of je stond buiten de lijst.',
            'De knop Slicer invoegen staat grijs. Klik eerst in je draaitabel.',
            'Je grafiek beweegt niet mee met de slicer. Dan is het een gewone '
            'grafiek en geen draaigrafiek. Maak hem opnieuw vanuit de '
            'draaitabel.',
        ],
    ),
]


def punten_van(oef):
    return (sum(p for *_, p in oef.get('vullen', []))
            + sum(p for *_, p in oef.get('stappen', []))
            + sum(p for *_, p in oef['vragen']))


TOTAAL = sum(punten_van(oef) for oef in OEFENINGEN)

if __name__ == '__main__':
    for oef in OEFENINGEN:
        fiches = ', '.join(str(n) for n in oef['fiches'])
        print(f"blad {oef['nr']}  {oef['blad']:<18} {oef['duur']:<12} "
              f"fiche {fiches:<10} {punten_van(oef)} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
