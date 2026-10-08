# -*- coding: utf-8 -*-
"""Gegevens voor de zelfstudiebundel: De Slimste Mens Ter Wereld.

Vijf werkbladen, 40 minuten, zelfstandig te maken zonder leerkracht erbij.
De nadruk ligt op de drie functies waar het vaakst op vastgelopen wordt:
SOM, AANTAL (en AANTAL.ALS) en VERT.ZOEKEN. Plus opmaak op elk blad.

Het spelprogramma bestaat echt, dit seizoen niet. Deelnemers, kijkcijfers en
uitslagen zijn verzonnen oefengegevens. Dat staat ook op het startbestand en
in beide documenten.
"""

TITEL = "Excel — De Slimste Mens Ter Wereld"
ONDERTITEL = "zelfstudiebundel · 40 minuten · seizoen 22 (verzonnen)"
WAARSCHUWING = ("De quiz bestaat echt, dit seizoen niet: alle deelnemers, kijkcijfers en "
                "uitslagen zijn verzonnen oefengegevens.")
BASISBUNDEL = "excel-functiebladen.docx"

# ---------------------------------------------------------------- blad 1
# Kijkcijfers: SOM per rij en per kolom. Het eenvoudigste blad, om in te komen.
B1_KOP = ["Aflevering", "Live", "Uitgesteld", "Online", "Totaal"]
B1 = [
    (1, 812340, 198450, 87210),
    (2, 798120, 205630, 91480),
    (3, 835670, 212890, 95340),
    (4, 821450, 199780, 88960),
    (5, 856230, 221540, 102370),
    (6, 843910, 215670, 98820),
    (7, 879540, 234120, 109650),
    (8, 867230, 228940, 105480),
    (9, 901870, 246310, 118290),
    (10, 948560, 271480, 132740),
]
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1                  # 4
B1_EIND = B1_START + len(B1) - 1          # 13
B1_TOTAAL = B1_EIND + 2                   # 15

# ---------------------------------------------------------------- blad 2
# De deelnemers: SOM, GEMIDDELDE, MAX, MIN, AANTAL, ALS en AANTAL.ALS.
B2_FINALIST = 3          # vanaf zoveel overwinningen mag je naar de finaleweek
B2_KOP = ["Deelnemer", "Beroep", "Afleveringen", "Overwinningen", "Seconden",
          "Finaleweek?"]
B2 = [
    ("Lies Vanhaverbeke", "journaliste", 7, 4, 412),
    ("Maarten Coninx", "acteur", 5, 2, 268),
    ("Fatima Benali", "advocate", 9, 6, 534),
    ("Jonas Vermeersch", "muzikant", 3, 0, 142),
    ("Hanne Dewitte", "lerares", 6, 3, 351),
    ("Tuur Van Isacker", "cabaretier", 4, 1, 198),
    ("Sarah Peeters", "dokter", 8, 5, 487),
    ("Bram Maes", "kok", 2, 0, 96),
    ("Nele Claes", "schrijfster", 11, 8, 642),
    ("Karim El Haddad", "econoom", 5, 2, 289),
    ("Lotte Vandamme", "presentatrice", 4, 1, 214),
    ("Stijn Boeykens", "historicus", 7, 4, 398),
    ("Ine Verhoeven", "bioloog", 3, 1, 156),
    ("Tom Declercq", "sportjournalist", 6, 3, 327),
    ("Amelie Rogge", "zangeres", 2, 0, 108),
    ("Pieter Vanacker", "komiek", 8, 5, 461),
    ("Esther Lammertyn", "notaris", 5, 2, 273),
    ("Gert Vanderplas", "wielrenner", 3, 0, 134),
]
B2_KOPRIJ = 4
B2_START = B2_KOPRIJ + 1                  # 5
B2_EIND = B2_START + len(B2) - 1          # 22
B2_SAMENVATTING = B2_EIND + 2             # 24 — zeven antwoordregels

# ---------------------------------------------------------------- blad 3
# Vragen per thema: AANTAL.ALS en SOM.ALS met een criterium uit een cel.
B3_THEMAS = ["Muziek", "Sport", "Geschiedenis", "Film & TV", "Aardrijkskunde",
             "Wetenschap"]
B3_KOP = ["Vraag", "Thema", "Ronde", "Seconden"]
B3 = [
    ("V-01", "Muziek", "3-6-9", 20),
    ("V-02", "Sport", "Open deur", 15),
    ("V-03", "Geschiedenis", "Puzzel", 10),
    ("V-04", "Film & TV", "3-6-9", 20),
    ("V-05", "Muziek", "Galerij", 15),
    ("V-06", "Aardrijkskunde", "Open deur", 15),
    ("V-07", "Film & TV", "Collectief geheugen", 10),
    ("V-08", "Wetenschap", "Puzzel", 10),
    ("V-09", "Sport", "3-6-9", 20),
    ("V-10", "Geschiedenis", "Galerij", 15),
    ("V-11", "Muziek", "Open deur", 15),
    ("V-12", "Film & TV", "Puzzel", 10),
    ("V-13", "Wetenschap", "3-6-9", 20),
    ("V-14", "Sport", "Collectief geheugen", 10),
    ("V-15", "Aardrijkskunde", "Galerij", 15),
    ("V-16", "Geschiedenis", "3-6-9", 20),
    ("V-17", "Muziek", "Collectief geheugen", 10),
    ("V-18", "Film & TV", "Open deur", 15),
    ("V-19", "Wetenschap", "Galerij", 15),
    ("V-20", "Sport", "Puzzel", 10),
    ("V-21", "Muziek", "3-6-9", 20),
    ("V-22", "Geschiedenis", "Open deur", 15),
    ("V-23", "Aardrijkskunde", "3-6-9", 20),
    ("V-24", "Film & TV", "Galerij", 15),
]
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1                  # 4
B3_EIND = B3_START + len(B3) - 1          # 27
B3_SAMENVATTING = B3_EIND + 2             # 29 — koprij van het blokje
B3_PER_THEMA = B3_SAMENVATTING + 1        # 30 — zes rijen, één per thema
B3_CONTROLE = B3_PER_THEMA + len(B3_THEMAS) + 1   # 37

# ---------------------------------------------------------------- blad 4
# Eén aflevering uitgewerkt: twee keer VERT.ZOEKEN, dan SOM en AFRONDEN.
B4_KOP = ["Code", "Ronde", "Sec. per antwoord", "Juiste antwoorden",
          "Gewonnen seconden"]
B4_ZOEKKOP = ["Code", "Ronde", "Sec. per antwoord"]
B4_TABEL = [
    ("R1", "3-6-9", 20),
    ("R2", "Open deur", 15),
    ("R3", "Puzzel", 10),
    ("R4", "Collectief geheugen", 10),
    ("R5", "Galerij", 15),
    ("R6", "Finale", 20),
]
B4_REGELS = [
    ("R1", 4), ("R2", 6), ("R3", 3), ("R4", 5), ("R5", 2), ("R6", 7),
    ("R1", 3), ("R2", 5), ("R3", 4), ("R4", 6), ("R5", 3), ("R6", 5),
]
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1                  # 4
B4_EIND = B4_START + len(B4_REGELS) - 1   # 15
B4_TOTAAL = B4_EIND + 2                   # 17
B4_GEMIDDELDE = B4_TOTAAL + 1             # 18
B4_TAB_START = 4
B4_TAB_EIND = B4_TAB_START + len(B4_TABEL) - 1    # 9

# ---------------------------------------------------------------- blad 5
# De finaleweek: nog eens VERT.ZOEKEN, plus ALS, SOM, AANTAL.ALS, GEMIDDELDE.
B5_DOOR = 150            # vanaf zoveel seconden ga je door naar de volgende ronde
B5_KOP = ["Startnr", "Deelnemer", "Ronde 1", "Ronde 2", "Ronde 3", "Totaal",
          "Door?"]
B5_ZOEKKOP = ["Startnr", "Deelnemer"]
B5_TABEL = [
    (1, "Nele Claes"),
    (2, "Fatima Benali"),
    (3, "Sarah Peeters"),
    (4, "Pieter Vanacker"),
    (5, "Lies Vanhaverbeke"),
    (6, "Stijn Boeykens"),
    (7, "Hanne Dewitte"),
    (8, "Tom Declercq"),
]
# Startnummer en de seconden per ronde. Bewust door elkaar, zodat opzoeken nodig is.
B5_UITSLAG = [
    (5, 62, 48, 55),
    (2, 71, 59, 64),
    (8, 44, 38, 41),
    (1, 83, 72, 69),
    (6, 57, 51, 42),
    (3, 68, 61, 58),
    (7, 49, 42, 52),
    (4, 66, 55, 60),
]
B5_KOPRIJ = 4
B5_START = B5_KOPRIJ + 1                  # 5
B5_EIND = B5_START + len(B5_UITSLAG) - 1  # 12
B5_ANTWOORD = B5_EIND + 2                 # 14 — drie antwoordregels
B5_TAB_START = 5
B5_TAB_EIND = B5_TAB_START + len(B5_TABEL) - 1    # 12


def zoek_ronde(code):
    """De juiste rij uit de rondetabel van blad 4."""
    for rij in B4_TABEL:
        if rij[0] == code:
            return rij
    raise KeyError(code)


def zoek_deelnemer(startnr):
    """De juiste rij uit de deelnemerstabel van blad 5."""
    for rij in B5_TABEL:
        if rij[0] == startnr:
            return rij
    raise KeyError(startnr)
