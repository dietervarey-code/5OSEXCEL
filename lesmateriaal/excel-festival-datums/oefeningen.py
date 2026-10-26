# -*- coding: utf-8 -*-
"""Wat de leerling op elk blad maakt.

De fiches staan in deze bundel zelf. Voor de draaitabel, het groeperen en de
draaigrafiek van blad 5 verwijzen we naar het boekje dat ze al hebben.
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
    for i, kaart in enumerate(f.FICHES, 1):
        if kaart['naam'] == naam:
            return i
    raise KeyError(f'fiche {naam!r} bestaat niet — de fiches heten: '
                   f'{[k["naam"] for k in f.FICHES]}')


V1, V2, V3, V4, V5 = 6, 6, 7, 8, 5     # kolom van het vragenblok per blad
PEILRIJ = 1                            # de peildatum staat rechtsboven
LOSRIJ = 2                             # en daaronder de ene VANDAAG-cel


def peil(vraagkol):
    """De vaste verwijzing naar de peildatum op dat blad."""
    return f'${_kol(vraagkol + 1)}${PEILRIJ}'


OEFENINGEN = [
    dict(
        nr=1, blad='1 Voorbereiding', titel='Een datum is een getal',
        duur='8 minuten', vraagkol=V1,
        fiches=[_fiche('Een datum is een getal')],
        inleiding=[
            f'{len(g.B1)} taken uit de voorbereiding, elk met een start- en '
            'een einddatum.',
            'Excel bewaart een datum als een getal: het aantal dagen sinds '
            '1 januari 1900. Daarom hoef je niets bijzonders te doen om uit '
            'te rekenen hoe lang iets duurt — je trekt gewoon af.',
            'Komt er een datum uit waar je een getal verwacht? Dan is het de '
            'opmaak van de cel, niet je formule. Zet ze op Standaard.',
        ],
        vullen=[
            (f'D{g.B1_START}:D{g.B1_EIND}', 'hoeveel dagen de taak duurt',
             f'=C{g.B1_START}-B{g.B1_START}', 4),
        ],
        vragen=[
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 1}',
             'welke taak het langst duurt', a.B1_LANGSTE, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 2}',
             'hoeveel dagen dat zijn', a.B1_LANGSTE_DAGEN, 1),
            (f'{_kol(V1 + 1)}{g.B1_KOPRIJ + 3}',
             'hoeveel dagen er zitten tussen de vroegste start en het laatste '
             'einde', a.B1_SPANNE, 1),
        ],
        klaar=f'Eén kolom met {len(g.B1)} gewone getallen, geen datums.',
        controle=f'De langste taak duurt {a.B1_LANGSTE_DAGEN} dagen. Staat er '
                 'ergens iets als 12/04/1900, dan klopt je formule wel maar je '
                 'celopmaak niet.',
        vast=[
            'Je krijgt overal een datum in 1900. Selecteer kolom D en zet de '
            'getalnotatie op Standaard.',
            'Je krijgt een negatief getal. Dan heb je start min einde gedaan '
            'in plaats van einde min start.',
        ],
    ),
    dict(
        nr=2, blad='2 Vrijwilligers', titel='Hoe oud is iedereen?',
        duur='10 minuten', vraagkol=V2,
        fiches=[_fiche('DATUMVERSCHIL'), _fiche('VANDAAG')],
        inleiding=[
            f'{len(g.B2)} vrijwilligers met hun geboortedatum. Wie op de '
            f'eerste festivaldag {g.B2_MEERDERJARIG} is, mag achter de bar.',
            'Reken met de peildatum rechtsboven, niet met VANDAAG(). Zet er '
            'dollartekens om, anders zakt hij mee als je doorvoert.',
            'Twee vrijwilligers zijn in de festivalweek jarig. Kijk wat één '
            'dag verschil met hun leeftijd doet.',
        ],
        vullen=[
            (f'C{g.B2_START}:C{g.B2_EIND}',
             'de leeftijd op de eerste festivaldag',
             f'=DATUMVERSCHIL(B{g.B2_START};{peil(V2)};"J")', 4),
            (f'D{g.B2_START}:D{g.B2_EIND}', 'of die persoon achter de bar mag',
             f'=ALS(C{g.B2_START}>={g.B2_MEERDERJARIG};"ja";"nee")', 2),
        ],
        los=(f'{_kol(V2 + 1)}{LOSRIJ}',
             'hoeveel dagen het nog is tot het festival, vanaf vandaag',
             f'={peil(V2)}-VANDAAG()', 1),
        vragen=[
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 1}',
             'hoeveel vrijwilligers er achter de bar mogen', a.B2_AANTAL_MAG, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 2}',
             'wie de jongste is', a.B2_JONGSTE, 1),
            (f'{_kol(V2 + 1)}{g.B2_KOPRIJ + 3}',
             'hoe oud de oudste is', a.B2_OUDSTE_LEEFTIJD, 1),
        ],
        klaar=f'Twee volle kolommen, en in {_kol(V2 + 1)}{LOSRIJ} een getal '
              'dat morgen één lager staat.',
        controle=f'{a.B2_AANTAL_MAG} van de {len(g.B2)} mogen achter de bar. '
                 'Krijg je er één meer of minder, kijk dan naar de twee die in '
                 'juli jarig zijn.',
        vast=[
            'Je krijgt #GETAL!. Dan staan de twee datums omgekeerd: eerst de '
            'geboortedatum, dan de peildatum.',
            'Onderaan klopt je leeftijd niet meer. De peildatum is niet '
            'vastgezet met dollartekens.',
            'Excel stelt DATUMVERSCHIL niet voor terwijl je typt. Dat hoort '
            'zo; typ ze gewoon helemaal uit.',
        ],
    ),
    dict(
        nr=3, blad='3 Ticketverkoop', titel='Uit een datum halen',
        duur='10 minuten', vraagkol=V3,
        fiches=[_fiche('JAAR, MAAND en DAG'), _fiche('WEEKDAG')],
        inleiding=[
            f'{len(g.B3)} verkoopdagen met het aantal tickets van die dag.',
            'Aan een datum zie je niet of het een zaterdag was. Excel wel — '
            'maar alleen als je het vraagt.',
            'Let op het tweede argument van WEEKDAG. Zonder de ;2 is zondag '
            'dag 1 en klopt je weekend niet.',
        ],
        vullen=[
            (f'C{g.B3_START}:C{g.B3_EIND}', 'het maandnummer',
             f'=MAAND(A{g.B3_START})', 2),
            (f'D{g.B3_START}:D{g.B3_EIND}', 'het weekdagnummer',
             f'=WEEKDAG(A{g.B3_START};2)', 2),
            (f'E{g.B3_START}:E{g.B3_EIND}', 'of het een weekenddag was',
             f'=ALS(D{g.B3_START}>={g.B3_WEEKEND_VANAF};"weekend";"weekdag")',
             3),
        ],
        vragen=[
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 1}',
             'hoeveel verkoopdagen in het weekend vielen', a.B3_WEEKENDDAGEN,
             1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 2}',
             'hoeveel tickets er op de drukste dag verkocht zijn',
             a.B3_DRUKSTE_TICKETS, 1),
            (f'{_kol(V3 + 1)}{g.B3_KOPRIJ + 3}',
             'welk weekdagnummer die drukste dag heeft', a.B3_DRUKSTE_WEEKDAG,
             1),
        ],
        klaar='Drie volle kolommen. In kolom C staan getallen van 1 tot 12, in '
              'kolom D van 1 tot 7.',
        controle=f'{a.B3_WEEKENDDAGEN} van de {len(g.B3)} dagen vielen in het '
                 'weekend. Krijg je er meer, dan mist de ;2 in je WEEKDAG.',
        vast=[
            'In kolom C staat een datum in plaats van een maandnummer. Zet de '
            'getalnotatie op Standaard.',
            'Je weekend komt op acht of negen dagen uit. Dan telt je WEEKDAG '
            'nog op de Amerikaanse manier: voeg de ;2 toe.',
        ],
    ),
    dict(
        nr=4, blad='4 Opbouw', titel='Rekenen zonder weekends',
        duur='12 minuten', vraagkol=V4,
        fiches=[_fiche('WERKDAG'), _fiche('NETTO.WERKDAGEN')],
        inleiding=[
            f'{len(g.B4)} opbouwtaken. De ploeg werkt niet in het weekend, '
            'dus kalenderdagen zeggen hier niets.',
            'WERKDAG geeft je de datum waarop een taak klaar is. '
            'NETTO.WERKDAGEN telt hoeveel werkdagen er tussen twee datums '
            'zitten. Dat zijn twee verschillende vragen.',
            'Eén taak komt te laat. Welke, dat is precies waarom je dit blad '
            'maakt.',
        ],
        vullen=[
            (f'D{g.B4_START}:D{g.B4_EIND}', 'de datum waarop de taak klaar is',
             f'=WERKDAG(B{g.B4_START};C{g.B4_START})', 4),
            (f'E{g.B4_START}:E{g.B4_EIND}',
             'hoeveel werkdagen er tussen de start en het festival zitten',
             f'=NETTO.WERKDAGEN(B{g.B4_START};{peil(V4)})', 2),
            (f'F{g.B4_START}:F{g.B4_EIND}', 'of de taak op tijd klaar is',
             f'=ALS(D{g.B4_START}<={peil(V4)};"ja";"nee")', 2),
        ],
        vragen=[
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 1}',
             'welke taak te laat komt', a.B4_TE_LAAT_TAAK, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 2}',
             'welke taak de meeste werkdagen nodig heeft', a.B4_ZWAARSTE, 1),
            (f'{_kol(V4 + 1)}{g.B4_KOPRIJ + 3}',
             'wat het hoogste getal in kolom E is', a.B4_MEESTE_WERKDAGEN, 1),
        ],
        klaar='Kolom D met datums, kolom E met getallen, en in kolom F één '
              'keer "nee".',
        controle=f'Precies één taak komt te laat: {a.B4_TE_LAAT_TAAK}, klaar '
                 f'op {a._dat(a.B4_TE_LAAT_KLAAR)}. Staan er meer op "nee", '
                 'dan is de peildatum niet vastgezet.',
        vast=[
            'In kolom D staan getallen van rond de 46 000. Dat zijn je datums '
            'zonder opmaak; geef de cellen de datumnotatie.',
            'Je einddatum valt in het weekend. Dan heb je gewoon opgeteld in '
            'plaats van WERKDAG te gebruiken.',
            'Alles staat op "nee" of alles op "ja". Kijk of je peildatum '
            'vastgezet is met dollartekens.',
        ],
    ),
    dict(
        nr=5, blad='5 Verkoop per maand',
        titel='Tabel, draaitabel, grafiek, tijdlijn', duur='10 minuten',
        vraagkol=V5,
        fiches=[_fiche('Een tabel maken (Ctrl+T)'), _fiche('Een tijdlijn')],
        kaarten_elders=[3, 4, 8, 13],
        inleiding=[
            f'{len(g.B5)} verkoopregels: per dag één regel per kanaal. Dit is '
            'dezelfde verkoop als op blad 3, maar dan uitgesplitst.',
            'Geen formules. Je maakt er een tabel van, zet er een draaitabel '
            'op die per maand groepeert, en hangt daar een draaigrafiek en '
            'een tijdlijn aan.',
            'Een tijdlijn is een slicer voor datums. Hij werkt alleen als je '
            'datumkolom echte datums bevat — en dat is hier zo.',
        ],
        stappen=[
            ('De lijst een tabel maken', 'Klik erin en druk Ctrl+T. '
             'Kopteksten aangevinkt laten.', 2),
            ('Een draaitabel erop, per maand',
             f'Rijen: {g.B5_DRAAI_RIJEN}. Waarden: Som van '
             f'{g.B5_DRAAI_WAARDEN}. Rechtsklik daarna op een datum in de '
             'draaitabel en kies Groeperen, Maanden. Kaart 8 van je boekje '
             'legt dat uit.', 4),
            ('Een draaigrafiek erbij', 'Draaitabel analyseren, Draaigrafiek. '
             'Een staafdiagram volstaat. Geef hem een titel.', 2),
            ('Een tijdlijn erop', f'Draaitabel analyseren, Tijdlijn invoegen, '
             f'veld {g.B5_DRAAI_RIJEN}. Klik daarna op {g.B5_TIJDLIJN_MAAND} '
             'en kijk wat je grafiek doet.', 1),
        ],
        vragen=[
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 1}',
             'in welke maand er de meeste tickets verkocht zijn', a.B5_TOPMAAND,
             1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 2}',
             'wat het eindtotaal van je draaitabel is', a.B5_TOTAAL, 1),
            (f'{_kol(V5 + 1)}{g.B5_KOPRIJ + 3}',
             f'hoeveel tickets er in {g.B5_TIJDLIJN_MAAND} verkocht zijn, '
             'afgelezen met de tijdlijn', a.B5_TIJDLIJN_TICKETS, 1),
        ],
        klaar=f'Een tabel met filterpijltjes, een draaitabel van '
              f'{len(a.B5_MAANDEN)} maanden, een staafdiagram ernaast en een '
              'tijdlijn erboven.',
        controle=f'Het eindtotaal moet {a._getal(a.B5_TOTAAL)} zijn — evenveel '
                 'als alle tickets van blad 3 samen. Staan er '
                 f'{len(g.B5)} regels in je draaitabel in plaats van '
                 f'{len(a.B5_MAANDEN)}, dan heb je nog niet gegroepeerd.',
        vast=[
            'Je draaitabel toont elke datum apart. Rechtsklik op een datum, '
            'niet op een getal, en kies Groeperen.',
            'De knop Tijdlijn invoegen staat grijs. Dan staan je datums als '
            'tekst in de kolom, of je hebt buiten de draaitabel geklikt.',
            'Je grafiek beweegt niet mee met de tijdlijn. Dan is het een '
            'gewone grafiek en geen draaigrafiek.',
        ],
    ),
]


def punten_van(oef):
    los = oef.get('los')
    return (sum(p for *_, p in oef.get('vullen', []))
            + sum(p for *_, p in oef.get('stappen', []))
            + (los[-1] if los else 0)
            + sum(p for *_, p in oef['vragen']))


TOTAAL = sum(punten_van(oef) for oef in OEFENINGEN)

if __name__ == '__main__':
    for oef in OEFENINGEN:
        fiches = ', '.join(str(n) for n in oef['fiches'])
        print(f"blad {oef['nr']}  {oef['blad']:<20} {oef['duur']:<12} "
              f"fiche {fiches:<8} {punten_van(oef)} punten")
    print(f'\n{TOTAAL} punten, '
          f"{sum(int(o['duur'].split()[0]) for o in OEFENINGEN)} minuten")
