# -*- coding: utf-8 -*-
"""Gegevens voor de datumbundel: de planning van Zomerklank.

De zusterbundel van excel-festival-tekst. Daar kuisten ze de lijst op, hier
rekenen ze met de datums die erin staan. Blad 5 eindigt op een draaitabel met
een draaigrafiek en een tijdlijn — een slicer voor datums.

WAT KLOPT EN WAT NIET
  Zomerklank bestaat niet, en de planning, de vrijwilligers en de
  ticketverkoop zijn verzonnen. De kalender is wél echt: 17 juli 2026 is
  een vrijdag, en elke weekdag in dit bestand klopt met de echte kalender.
  Dat moet ook, anders kan je er niet mee rekenen.

WAAROM ER EEN PEILDATUM IS
  Als je met VANDAAG() rekent, verandert je antwoord elke dag. Dan kan een
  leerkracht niets nakijken en kan een leerling zijn eigen werk niet
  controleren. Daarom staat op elk blad rechtsboven de eerste festivaldag,
  en rekenen we daarop. VANDAAG() komt wél aan bod, één keer, op blad 2 —
  en daar staat erbij dat het antwoord elke dag anders is.
"""
import datetime

TITEL = "Excel — de planning van Zomerklank"
ONDERTITEL = "Vijf werkbladen rond datums, en één tijdlijn"
FESTIVAL = "Zomerklank"
ZUSTERBUNDEL = "excel-festival-tekst"
DUUR = 50

PEILDATUM = datetime.date(2026, 7, 17)       # vrijdag, de eerste festivaldag
PEIL_LABEL = "Eerste festivaldag"
DATUMNOTATIE = 'dd/mm/yyyy'

WAARSCHUWING = (
    "Zomerklank bestaat niet en de planning is verzonnen. De kalender niet: "
    "17 juli 2026 is echt een vrijdag, en elke weekdag die je uitrekent klopt "
    "met de echte kalender. Reken overal met de peildatum rechtsboven, niet "
    "met VANDAAG() — anders staat er morgen iets anders dan vandaag, en dan "
    "kan niemand je werk nog nakijken."
)

# ================================================================= blad 1
# Een datum is een getal. Aftrekken geeft dagen.
B1_KOP = ["Taak", "Start", "Einde", "Dagen"]
# (taak, start, einde) — alles in de aanloop naar het festival
B1 = [
    ("Vergunning aanvragen",       datetime.date(2026, 1, 12),
                                   datetime.date(2026, 3, 6)),
    ("Line-up vastleggen",         datetime.date(2026, 1, 26),
                                   datetime.date(2026, 4, 24)),
    ("Terrein huren",              datetime.date(2026, 2, 2),
                                   datetime.date(2026, 2, 27)),
    ("Ticketverkoop voorbereiden", datetime.date(2026, 2, 16),
                                   datetime.date(2026, 3, 20)),
    ("Campagne online",            datetime.date(2026, 3, 9),
                                   datetime.date(2026, 6, 19)),
    ("Vrijwilligers werven",       datetime.date(2026, 3, 23),
                                   datetime.date(2026, 5, 29)),
    ("Catering aanbesteden",       datetime.date(2026, 4, 6),
                                   datetime.date(2026, 5, 1)),
    ("Podia bestellen",            datetime.date(2026, 4, 20),
                                   datetime.date(2026, 5, 15)),
    ("Beveiliging contracteren",   datetime.date(2026, 5, 4),
                                   datetime.date(2026, 6, 5)),
    ("Signalisatie laten drukken", datetime.date(2026, 5, 18),
                                   datetime.date(2026, 6, 12)),
    ("Opbouw terrein",             datetime.date(2026, 6, 29),
                                   datetime.date(2026, 7, 16)),
    ("Technische check",           datetime.date(2026, 7, 13),
                                   datetime.date(2026, 7, 16)),
]
B1_VOETNOOT = (
    "Twaalf taken uit de voorbereiding. Een datum is voor Excel gewoon een "
    "getal: het aantal dagen sinds 1 januari 1900. Daarom kan je twee datums "
    "van elkaar aftrekken."
)
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1

# ================================================================= blad 2
# DATUMVERSCHIL, en één keer VANDAAG.
B2_KOP = ["Vrijwilliger", "Geboortedatum", "Leeftijd op de eerste festivaldag",
          "Achter de bar?"]
B2_MEERDERJARIG = 18
# (naam, geboortedatum)
B2 = [
    ("Lotte Vandenberghe", datetime.date(2006, 3, 14)),
    ("Jonas Peeters",      datetime.date(2009, 11, 2)),
    ("Amina De Smet",      datetime.date(2008, 7, 17)),
    ("Youssef Willems",    datetime.date(2007, 1, 30)),
    ("Elise Mertens",      datetime.date(2009, 4, 8)),
    ("Bilal Claes",        datetime.date(2005, 9, 21)),
    ("Noor Janssens",      datetime.date(2008, 7, 18)),
    ("Sam Maes",           datetime.date(2010, 2, 5)),
    ("Ayla Wouters",       datetime.date(2004, 12, 11)),
    ("Liam Goossens",      datetime.date(2009, 8, 27)),
    ("Fatima De Cock",     datetime.date(2003, 5, 3)),
    ("Thibault Hermans",   datetime.date(2008, 10, 19)),
    ("Zeynep Lambrechts",  datetime.date(2007, 6, 24)),
    ("Robbe Van Damme",    datetime.date(2010, 9, 9)),
    ("Ilyas Segers",       datetime.date(2002, 1, 16)),
    ("Margot Boeckx",      datetime.date(2009, 12, 30)),
]
B2_VOETNOOT = (
    "Zestien vrijwilligers. Wie op de eerste festivaldag al achttien is, mag "
    "achter de bar. Let op de twee die in juli jarig zijn: één dag scheelt "
    "daar een heel jaar."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1

# ================================================================= blad 3
# JAAR, MAAND, DAG, WEEKDAG.
B3_KOP = ["Datum", "Tickets", "Maand", "Weekdagnummer", "Soort dag"]
B3_WEEKEND_VANAF = 6          # met WEEKDAG(datum;2) is 6 zaterdag
# (datum, verkochte tickets op die dag)
B3 = [
    (datetime.date(2026, 3, 20),  840),
    (datetime.date(2026, 3, 21), 1260),
    (datetime.date(2026, 3, 27),  510),
    (datetime.date(2026, 4, 4),   930),
    (datetime.date(2026, 4, 10),  470),
    (datetime.date(2026, 4, 18), 1080),
    (datetime.date(2026, 4, 25),  760),
    (datetime.date(2026, 4, 30),  350),
    (datetime.date(2026, 5, 2),  1340),
    (datetime.date(2026, 5, 8),   620),
    (datetime.date(2026, 5, 16),  990),
    (datetime.date(2026, 5, 23), 1150),
    (datetime.date(2026, 5, 29),  580),
    (datetime.date(2026, 6, 6),  1420),
    (datetime.date(2026, 6, 12),  660),
    (datetime.date(2026, 6, 20), 1510),
    (datetime.date(2026, 6, 26),  720),
    (datetime.date(2026, 7, 4),  1680),
]
B3_VOETNOOT = (
    "Achttien verkoopdagen. Of een dag in het weekend viel, zie je niet aan "
    "de datum — daar heb je WEEKDAG voor nodig."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1

# ================================================================= blad 4
# NETTO.WERKDAGEN en WERKDAG: rekenen zonder weekends.
B4_KOP = ["Opbouwtaak", "Start", "Werkdagen nodig", "Klaar op",
          "Werkdagen tot het festival", "Op tijd?"]
# (taak, startdatum, aantal werkdagen dat de taak kost)
B4 = [
    ("Hekwerk plaatsen",        datetime.date(2026, 6, 29),  4),
    ("Main Stage opbouwen",     datetime.date(2026, 6, 29), 12),
    ("Klub C opbouwen",         datetime.date(2026, 7, 1),   7),
    ("Bostent zetten",          datetime.date(2026, 7, 2),   5),
    ("Strandbar bouwen",        datetime.date(2026, 7, 6),   3),
    ("Stroom aanleggen",        datetime.date(2026, 7, 1),   9),
    ("Water en sanitair",       datetime.date(2026, 7, 3),   6),
    ("Licht en geluid Main",    datetime.date(2026, 7, 13),  5),
    ("Signalisatie plaatsen",   datetime.date(2026, 7, 10),  2),
    ("Camping uitzetten",       datetime.date(2026, 7, 6),   8),
    ("Catering installeren",    datetime.date(2026, 7, 13),  3),
    ("Eindcontrole veiligheid", datetime.date(2026, 7, 15),  2),
]
B4_VOETNOOT = (
    "Twaalf opbouwtaken. De ploeg werkt niet in het weekend. Een taak van "
    "vijf werkdagen duurt dus zeven kalenderdagen als er een weekend in valt "
    "— en dat is precies waarom je NETTO.WERKDAGEN nodig hebt."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1

# ================================================================= blad 5
# Draaitabel per maand, draaigrafiek, tijdlijn.
B5_KOP = ["Datum", "Kanaal", "Tickets"]
B5_KANALEN = ["Kassa", "Online", "Partner", "Wedstrijd"]
B5_TIJDLIJN_MAAND = "juni"
B5_TIJDLIJN_MAANDNUMMER = 6
B5_DRAAI_RIJEN = "Datum"
B5_DRAAI_WAARDEN = "Tickets"
# (datum, kanaal, tickets)
B5 = [
    (datetime.date(2026, 3, 20), "Online",    620),
    (datetime.date(2026, 3, 20), "Kassa",     220),
    (datetime.date(2026, 3, 21), "Online",    910),
    (datetime.date(2026, 3, 21), "Partner",   350),
    (datetime.date(2026, 3, 27), "Online",    450),
    (datetime.date(2026, 3, 27), "Wedstrijd",  60),
    (datetime.date(2026, 4, 4),  "Online",    640),
    (datetime.date(2026, 4, 4),  "Kassa",     290),
    (datetime.date(2026, 4, 10), "Online",    320),
    (datetime.date(2026, 4, 10), "Partner",   150),
    (datetime.date(2026, 4, 18), "Online",    780),
    (datetime.date(2026, 4, 18), "Kassa",     300),
    (datetime.date(2026, 4, 25), "Online",    680),
    (datetime.date(2026, 4, 25), "Wedstrijd",  80),
    (datetime.date(2026, 4, 30), "Partner",   350),
    (datetime.date(2026, 5, 2),  "Online",    940),
    (datetime.date(2026, 5, 2),  "Kassa",     400),
    (datetime.date(2026, 5, 8),  "Online",    450),
    (datetime.date(2026, 5, 8),  "Partner",   170),
    (datetime.date(2026, 5, 16), "Online",    700),
    (datetime.date(2026, 5, 16), "Kassa",     290),
    (datetime.date(2026, 5, 23), "Online",    820),
    (datetime.date(2026, 5, 23), "Wedstrijd", 110),
    (datetime.date(2026, 5, 23), "Partner",   220),
    (datetime.date(2026, 5, 29), "Online",    430),
    (datetime.date(2026, 5, 29), "Kassa",     150),
    (datetime.date(2026, 6, 6),  "Online",   1010),
    (datetime.date(2026, 6, 6),  "Kassa",     410),
    (datetime.date(2026, 6, 12), "Online",    480),
    (datetime.date(2026, 6, 12), "Partner",   180),
    (datetime.date(2026, 6, 20), "Online",   1120),
    (datetime.date(2026, 6, 20), "Kassa",     270),
    (datetime.date(2026, 6, 20), "Wedstrijd", 120),
    (datetime.date(2026, 6, 26), "Online",    520),
    (datetime.date(2026, 6, 26), "Partner",   200),
    (datetime.date(2026, 7, 4),  "Online",   1250),
    (datetime.date(2026, 7, 4),  "Kassa",     430),
]
B5_VOETNOOT = (
    "Zevenendertig verkoopregels over vier maanden. Elke datum staat er een "
    "paar keer in, één keer per kanaal — precies de situatie waarin een "
    "draaitabel per maand iets laat zien wat je in de lijst niet ziet."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_EIND = B5_START + len(B5) - 1

MAANDNAMEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli",
              "augustus", "september", "oktober", "november", "december"]
DAGNAMEN = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag",
            "zaterdag", "zondag"]


# ---------------------------------------------------------------- helpers
def maandnaam(nummer):
    if not 1 <= nummer <= 12:
        raise IndexError(f'maand {nummer} bestaat niet — geldig is 1 tot 12')
    return MAANDNAMEN[nummer - 1]


def weekdagnummer(datum):
    """Zoals WEEKDAG(datum;2): maandag is 1, zondag is 7."""
    return datum.weekday() + 1


def dagnaam(datum):
    return DAGNAMEN[datum.weekday()]


def is_weekend(datum):
    return weekdagnummer(datum) >= B3_WEEKEND_VANAF


def netto_werkdagen(van, tot):
    """Zoals NETTO.WERKDAGEN: beide datums meegeteld, weekends niet."""
    if tot < van:
        return -netto_werkdagen(tot, van)
    dagen = 0
    d = van
    stap = __import__('datetime').timedelta(days=1)
    while d <= tot:
        if d.weekday() < 5:
            dagen += 1
        d += stap
    return dagen


def werkdag(start, aantal):
    """Zoals WERKDAG: het aantal werkdagen NA de startdatum."""
    d = start
    stap = __import__('datetime').timedelta(days=1)
    over = aantal
    while over > 0:
        d += stap
        if d.weekday() < 5:
            over -= 1
    return d


def leeftijd_op(geboortedatum, peil):
    """Zoals DATUMVERSCHIL(geboorte;peil;"J"): hele jaren."""
    jaren = peil.year - geboortedatum.year
    if (peil.month, peil.day) < (geboortedatum.month, geboortedatum.day):
        jaren -= 1
    return jaren
