# -*- coding: utf-8 -*-
"""De vijf werkbladen van de synthesetoets.

Dit is een toets, geen oefening. Daarom staat er NERGENS een formule: er staat
wat er moet uitkomen en met welke functie. Bij een handvol cellen staat zelfs
dat niet — daar moeten ze zelf de juiste functie kiezen.

Elke cel en elke opmaakeis heeft punten. Samen 50, voor 50 minuten.
Alleen de tien functies en de vijf hulpfiches uit de basisbundel.
"""

KIES_ZELF = 'kies zelf de juiste functie'
GEEN_FUNCTIE = 'een formule, geen functie'

OEFENINGEN = [
    dict(
        nr=1,
        titel='De selectie in cijfers',
        blad='1 Selectie',
        duur='13 minuten',
        doel='Bij de volledige selectie een kolom zetten die aanduidt wie ervaren is, en '
             'er daarna zeven kerncijfers uit halen.',
        functies=['SOM', 'GEMIDDELDE', 'MAX', 'MIN', 'AANTAL', 'ALS', 'AANTAL.ALS'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep', 'Voorwaardelijke opmaak', 'Beeld vastzetten'],
        gegeven=[
            ('B2', 'vanaf hoeveel caps een speler ervaren heet'),
            ('A5:A26', 'de 22 spelers van de selectie'),
            ('B5:B26', 'hun positie'),
            ('C5:C26', 'hun leeftijd'),
            ('D5:D26', 'het aantal caps'),
            ('E5:E26', 'het aantal doelpunten voor de nationale ploeg'),
        ],
        maken=[
            dict(waar='F5:F26', wat='ja of nee: is de speler ervaren',
                 hoe='ALS, met een absolute verwijzing naar B2', functie='ALS', punten=2),
            dict(waar='B28', wat='het totale aantal caps van de selectie',
                 hoe='SOM', functie='SOM', punten=1),
            dict(waar='B29', wat='het totale aantal doelpunten',
                 hoe='SOM', functie='SOM', punten=1),
            dict(waar='B30', wat='de gemiddelde leeftijd',
                 hoe='GEMIDDELDE', functie='GEMIDDELDE', punten=1),
            dict(waar='B31', wat='de leeftijd van de oudste speler',
                 hoe=KIES_ZELF, functie='MAX', punten=1),
            dict(waar='B32', wat='de leeftijd van de jongste speler',
                 hoe=KIES_ZELF, functie='MIN', punten=1),
            dict(waar='B33', wat='het aantal spelers in de selectie',
                 hoe='AANTAL', functie='AANTAL', punten=1),
            dict(waar='B34', wat='het aantal ervaren spelers',
                 hoe='AANTAL.ALS', functie='AANTAL.ALS', punten=1),
        ],
        opmaak=[
            ('Koprij 4 vet met een achtergrondkleur en gecentreerd, en het '
             'samenvattingsblok A28:B34 met een achtergrondkleur.', 1),
            ('B30 op één cijfer na de komma, en de koprij geblokkeerd zodat ze blijft '
             'staan als je naar beneden scrolt.', 1),
            ('Voorwaardelijke opmaak op D5:D26: wie meer caps heeft dan het gemiddelde, '
             'krijgt een kleur.', 1),
        ],
        klaar='Een kolom met 22 keer ja of nee, en daaronder zeven cijfers in een gekleurd '
              'blokje.',
        controle='B33 moet 22 geven — evenveel als er spelers in de lijst staan. Geeft het '
                 'een ander getal, dan loopt je bereik niet van rij 5 tot rij 26.',
    ),
    dict(
        nr=2,
        titel='De acht wedstrijden',
        blad='2 Wedstrijden',
        duur='11 minuten',
        doel='Acht wedstrijden doorrekenen: het saldo per wedstrijd, de totalen eronder, en '
             'drie cijfers over het seizoen.',
        functies=['SOM', 'ALS', 'AANTAL.ALS', 'GEMIDDELDE', 'MAX'],
        hulp=['Doorvoeren met de vulgreep', 'Voorwaardelijke opmaak',
              'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A11', 'de datum van elke wedstrijd'),
            ('B4:B11', 'de tegenstander'),
            ('C4:C11', 'thuis of uit'),
            ('D4:D11', 'het aantal doelpunten dat België maakte'),
            ('E4:E11', 'het aantal doelpunten dat België incasseerde'),
        ],
        maken=[
            dict(waar='F4:F11', wat='het doelpuntensaldo van de wedstrijd',
                 hoe=GEEN_FUNCTIE, functie=None, punten=1),
            dict(waar='G4:G11', wat='ja of nee: is de wedstrijd gewonnen',
                 hoe='ALS', functie='ALS', punten=2),
            dict(waar='D13:F13', wat='de totalen van de drie kolommen',
                 hoe='SOM, naar rechts doorvoeren', functie='SOM', punten=2),
            dict(waar='B15', wat='het aantal gewonnen wedstrijden',
                 hoe='AANTAL.ALS', functie='AANTAL.ALS', punten=1),
            dict(waar='B16', wat='het gemiddelde aantal doelpunten dat België maakte '
                                 'per wedstrijd',
                 hoe='GEMIDDELDE', functie='GEMIDDELDE', punten=1),
            dict(waar='B17', wat='het grootste doelpuntensaldo van het seizoen',
                 hoe=KIES_ZELF, functie='MAX', punten=1),
        ],
        opmaak=[
            ('Koprij 3 vet met een achtergrondkleur, totaalrij 13 vet met een bovenrand, '
             'en een rand rond A3:G13.', 1),
            ('Voorwaardelijke opmaak op G4:G11 — de gewonnen wedstrijden krijgen een '
             'kleur — en B16 op één cijfer na de komma.', 1),
        ],
        klaar='Acht saldo\'s, acht keer ja of nee, drie kolomtotalen en drie cijfers '
              'eronder.',
        controle='D13 min E13 moet precies F13 geven. Klopt dat niet, dan zit er een fout '
                 'in een van de acht saldo\'s.',
    ),
    dict(
        nr=3,
        titel='Doelpunten per positie',
        blad='3 Clubdoelpunten',
        duur='10 minuten',
        doel='Zestien spelers opsplitsen per positie, met één formule die je doorvoert — '
             'dus met het criterium uit een cel.',
        functies=['AANTAL.ALS', 'SOM.ALS', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Voorwaardelijke opmaak'],
        gegeven=[
            ('A4:A19', 'zestien spelers'),
            ('B4:B19', 'hun positie'),
            ('C4:C19', 'het aantal doelpunten dat ze dit seizoen bij hun club maakten'),
            ('D4:D19', 'het aantal assists'),
            ('A22:A25', 'de vier posities — die gebruik je als criterium'),
        ],
        maken=[
            dict(waar='B22:B25', wat='het aantal spelers per positie',
                 hoe='AANTAL.ALS met een absoluut bereik, daarna doorvoeren',
                 functie='AANTAL.ALS', punten=2),
            dict(waar='C22:C25', wat='het totale aantal doelpunten per positie',
                 hoe='SOM.ALS met absolute bereiken, daarna doorvoeren',
                 functie='SOM.ALS', punten=3),
            dict(waar='C27', wat='het totaal van alle doelpunten samen',
                 hoe=KIES_ZELF, functie='SOM', punten=1),
        ],
        opmaak=[
            ('Koprij 3 en koprij 21 vet met een achtergrondkleur.', 1),
            ('Een rand rond het blokje A21:C25, en C27 vet.', 1),
            ('Voorwaardelijke opmaak op C4:C19: wie tien doelpunten of meer maakte, '
             'krijgt een kleur.', 1),
        ],
        klaar='Vier posities met elk een aantal spelers en een aantal doelpunten, en '
              'daaronder het totaal.',
        controle='De vier aantallen in kolom C moeten samen precies C27 geven. Klopt dat '
                 'niet, dan staat er een positie verkeerd gespeld in de lijst of in je '
                 'criterium.',
    ),
    dict(
        nr=4,
        titel='Ticketprijzen voor abonnees',
        blad='4 Tickets',
        duur='8 minuten',
        doel='Op acht ticketprijzen dezelfde korting toepassen, met één percentage dat op '
             'één plaats staat.',
        functies=['AFRONDEN', 'SOM'],
        hulp=['Absolute celverwijzing: de dollartekens',
              'Getalnotatie: valuta, percentage en decimalen',
              'Doorvoeren met de vulgreep'],
        gegeven=[
            ('B2', 'het kortingspercentage voor abonnees — één keer, voor de hele lijst'),
            ('A5:A12', 'de acht vakken van het stadion'),
            ('B5:B12', 'de normale prijs per vak'),
        ],
        maken=[
            dict(waar='C5:C12', wat='de korting in euro, afgerond op cent',
                 hoe='AFRONDEN, met een absolute verwijzing naar B2',
                 functie='AFRONDEN', punten=3),
            dict(waar='D5:D12', wat='de prijs die een abonnee betaalt',
                 hoe=GEEN_FUNCTIE, functie=None, punten=1),
            dict(waar='B14:D14', wat='de totalen van de drie kolommen',
                 hoe='SOM, naar rechts doorvoeren', functie='SOM', punten=2),
        ],
        opmaak=[
            ('B2 met de notatie percentage.', 1),
            ('B5:D14 met de notatie valuta.', 1),
            ('Koprij 4 vet met een achtergrondkleur, totaalrij 14 vet, en een rand rond '
             'A4:D14.', 1),
        ],
        klaar='Acht kortingen en acht abonneeprijzen, met drie kolomtotalen eronder.',
        controle='B14 min C14 moet precies D14 geven. Klopt dat niet, dan zit er een fout '
                 'in een van de acht rijen.',
    ),
    dict(
        nr=5,
        titel='Het wedstrijdblad',
        blad='5 Wedstrijdblad',
        duur='8 minuten',
        doel='Van elf rugnummers de speler en de positie ophalen uit de spelerslijst, en '
             'de basiself samenvatten.',
        functies=['VERT.ZOEKEN', 'SOM', 'AANTAL.ALS', 'GEMIDDELDE'],
        hulp=['Absolute celverwijzing: de dollartekens', 'Doorvoeren met de vulgreep',
              'Getalnotatie: valuta, percentage en decimalen'],
        gegeven=[
            ('A4:A14', 'de elf rugnummers van de basiself'),
            ('D4:D14', 'het aantal minuten dat elke speler op het veld stond'),
            ('F3:H25', 'de spelerslijst: rugnummer, speler en positie — niet aanpassen'),
        ],
        maken=[
            dict(waar='B4:B14', wat='de naam van de speler',
                 hoe='VERT.ZOEKEN, kolom 2 — zet de spelerslijst vast voor je doorvoert',
                 functie='VERT.ZOEKEN', punten=3),
            dict(waar='C4:C14', wat='de positie van de speler',
                 hoe='VERT.ZOEKEN, kolom 3', functie='VERT.ZOEKEN', punten=2),
            dict(waar='B16', wat='het totale aantal gespeelde minuten',
                 hoe='SOM', functie='SOM', punten=1),
            dict(waar='B17', wat='het aantal verdedigers in de basiself',
                 hoe='AANTAL.ALS', functie='AANTAL.ALS', punten=1),
            dict(waar='B18', wat='het gemiddelde aantal minuten per speler',
                 hoe=KIES_ZELF, functie='GEMIDDELDE', punten=1),
        ],
        opmaak=[
            ('Koprij 3 vet met een achtergrondkleur, en de spelerslijst F3:H25 met een '
             'lichte vulling en een rand eromheen.', 1),
            ('B18 op één cijfer na de komma, en kolom A en kolom D gecentreerd.', 1),
        ],
        klaar='Elf namen en elf posities die je nergens hebt ingetypt, en drie cijfers '
              'eronder.',
        controle='Geen enkele cel mag #N/B tonen. Zie je die melding, dan zijn de '
                 'dollartekens rond de spelerslijst vergeten en is de lijst meegeschoven '
                 'bij het doorvoeren.',
    ),
]
