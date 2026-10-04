# -*- coding: utf-8 -*-
"""Gegevens voor de synthesetoets: de Rode Duivels in cijfers.

Vijf werkbladen, 50 minuten, 50 punten. Alleen de tien functies en de vijf
opmaakonderwerpen uit de basisbundel. Geen geneste functies, geen
verwijzingen over de bladen heen.

De spelersnamen zijn echt, ALLE CIJFERS ZIJN VERZONNEN. Het is oefenmateriaal
en geen statistiek: leeftijden, caps, doelpunten, uitslagen en prijzen zijn
verzonnen zodat de oefening uitkomt. Dat staat ook op het startbestand en in
beide documenten.
"""

TITEL = "Excel-toets — de Rode Duivels in cijfers"
ONDERTITEL = "synthese van de basisfuncties · 50 minuten · 50 punten"
WAARSCHUWING = ("Alle cijfers in dit bestand zijn verzonnen oefengegevens. "
                "Het zijn geen echte statistieken.")
BASISBUNDEL = "excel-functiebladen.docx"

POSITIES = ["Doelman", "Verdediger", "Middenvelder", "Aanvaller"]

# ---------------------------------------------------------------- blad 1
# De selectie: SOM, GEMIDDELDE, MAX, MIN, AANTAL, ALS en AANTAL.ALS.
B1_ERVAREN = 50          # vanaf zoveel caps noemen we een speler ervaren
B1_KOP = ["Speler", "Positie", "Leeftijd", "Caps", "Doelpunten", "Ervaren?"]
B1 = [
    ("Thibaut Courtois", "Doelman", 33, 102, 0),
    ("Koen Casteels", "Doelman", 33, 12, 0),
    ("Matz Sels", "Doelman", 33, 9, 0),
    ("Jan Vertonghen", "Verdediger", 38, 157, 10),
    ("Wout Faes", "Verdediger", 27, 31, 1),
    ("Zeno Debast", "Verdediger", 22, 24, 1),
    ("Timothy Castagne", "Verdediger", 29, 50, 2),
    ("Arthur Theate", "Verdediger", 25, 29, 1),
    ("Maxim De Cuyper", "Verdediger", 25, 11, 0),
    ("Brandon Mechele", "Verdediger", 32, 5, 0),
    ("Kevin De Bruyne", "Middenvelder", 34, 109, 30),
    ("Youri Tielemans", "Middenvelder", 28, 73, 9),
    ("Amadou Onana", "Middenvelder", 24, 27, 2),
    ("Orel Mangala", "Middenvelder", 27, 22, 0),
    ("Arthur Vermeeren", "Middenvelder", 20, 8, 0),
    ("Hans Vanaken", "Middenvelder", 33, 38, 4),
    ("Romelu Lukaku", "Aanvaller", 32, 120, 85),
    ("Jérémy Doku", "Aanvaller", 23, 39, 5),
    ("Leandro Trossard", "Aanvaller", 31, 46, 11),
    ("Charles De Ketelaere", "Aanvaller", 24, 26, 2),
    ("Loïs Openda", "Aanvaller", 25, 34, 7),
    ("Johan Bakayoko", "Aanvaller", 22, 21, 3),
]
B1_KOPRIJ = 4
B1_START = B1_KOPRIJ + 1                  # 5
B1_EIND = B1_START + len(B1) - 1          # 26
B1_SAMENVATTING = B1_EIND + 2             # 28 — zeven antwoordregels

# ---------------------------------------------------------------- blad 2
# De wedstrijden: optellen in twee richtingen, ALS, AANTAL.ALS, GEMIDDELDE, MAX.
B2_KOP = ["Datum", "Tegenstander", "Thuis of uit", "Voor", "Tegen", "Saldo",
          "Gewonnen?"]
B2 = [
    ("05/09", "Frankrijk", "thuis", 2, 1),
    ("09/09", "Oekraïne", "uit", 1, 1),
    ("10/10", "Noorwegen", "thuis", 3, 0),
    ("14/10", "Italië", "uit", 0, 2),
    ("15/11", "Denemarken", "thuis", 2, 2),
    ("18/11", "Wales", "uit", 4, 1),
    ("23/03", "Nederland", "thuis", 1, 3),
    ("26/03", "Portugal", "uit", 2, 0),
]
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1                  # 4
B2_EIND = B2_START + len(B2) - 1          # 11
B2_TOTAAL = B2_EIND + 2                   # 13
B2_ANTWOORD = B2_TOTAAL + 2               # 15 — drie antwoordregels

# ---------------------------------------------------------------- blad 3
# Clubdoelpunten: AANTAL.ALS en SOM.ALS met een criterium uit een cel, zodat
# één formule volstaat en ze doorgevoerd kan worden.
B3_KOP = ["Speler", "Positie", "Doelpunten", "Assists"]
B3 = [
    ("Thibaut Courtois", "Doelman", 0, 0),
    ("Matz Sels", "Doelman", 0, 0),
    ("Jan Vertonghen", "Verdediger", 2, 1),
    ("Wout Faes", "Verdediger", 3, 0),
    ("Zeno Debast", "Verdediger", 1, 2),
    ("Timothy Castagne", "Verdediger", 2, 4),
    ("Arthur Theate", "Verdediger", 4, 1),
    ("Kevin De Bruyne", "Middenvelder", 9, 14),
    ("Youri Tielemans", "Middenvelder", 7, 5),
    ("Amadou Onana", "Middenvelder", 2, 1),
    ("Hans Vanaken", "Middenvelder", 11, 8),
    ("Romelu Lukaku", "Aanvaller", 18, 6),
    ("Jérémy Doku", "Aanvaller", 6, 11),
    ("Leandro Trossard", "Aanvaller", 12, 7),
    ("Loïs Openda", "Aanvaller", 15, 4),
    ("Johan Bakayoko", "Aanvaller", 8, 9),
]
B3_DREMPEL = 10          # vanaf zoveel doelpunten kleurt de voorwaardelijke opmaak
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1                  # 4
B3_EIND = B3_START + len(B3) - 1          # 19
B3_SAMENVATTING = B3_EIND + 2             # 21 — koprij van het blokje
B3_PER_POSITIE = B3_SAMENVATTING + 1      # 22 — vier rijen, één per positie
B3_CONTROLE = B3_PER_POSITIE + len(POSITIES) + 1   # 27

# ---------------------------------------------------------------- blad 4
# Ticketprijzen: AFRONDEN met een absolute verwijzing, daarna SOM.
B4_KORTING = 0.15
B4_KOP = ["Vak", "Normale prijs", "Korting", "Abonneeprijs"]
B4 = [
    ("Tribune 1 — middenvak", 95.00),
    ("Tribune 2 — zijvak", 72.50),
    ("Hoektribune", 58.00),
    ("Staantribune", 35.00),
    ("Businessseats", 185.00),
    ("Familievak", 42.50),
    ("Bezoekersvak", 48.00),
    ("Rolstoelplaats", 25.00),
]
B4_KOPRIJ = 4
B4_START = B4_KOPRIJ + 1                  # 5
B4_EIND = B4_START + len(B4) - 1          # 12
B4_TOTAAL = B4_EIND + 2                   # 14

# ---------------------------------------------------------------- blad 5
# Het wedstrijdblad: twee keer VERT.ZOEKEN, daarna SOM, AANTAL.ALS en GEMIDDELDE.
B5_KOP = ["Rugnummer", "Speler", "Positie", "Minuten"]
B5_ZOEKKOP = ["Rugnummer", "Speler", "Positie"]
B5_TABEL = [
    (1, "Thibaut Courtois", "Doelman"),
    (2, "Timothy Castagne", "Verdediger"),
    (3, "Arthur Theate", "Verdediger"),
    (4, "Wout Faes", "Verdediger"),
    (5, "Jan Vertonghen", "Verdediger"),
    (6, "Amadou Onana", "Middenvelder"),
    (7, "Kevin De Bruyne", "Middenvelder"),
    (8, "Youri Tielemans", "Middenvelder"),
    (9, "Romelu Lukaku", "Aanvaller"),
    (10, "Leandro Trossard", "Aanvaller"),
    (11, "Jérémy Doku", "Aanvaller"),
    (12, "Koen Casteels", "Doelman"),
    (13, "Matz Sels", "Doelman"),
    (14, "Loïs Openda", "Aanvaller"),
    (15, "Zeno Debast", "Verdediger"),
    (16, "Hans Vanaken", "Middenvelder"),
    (17, "Charles De Ketelaere", "Aanvaller"),
    (18, "Orel Mangala", "Middenvelder"),
    (19, "Johan Bakayoko", "Aanvaller"),
    (20, "Maxim De Cuyper", "Verdediger"),
    (21, "Arthur Vermeeren", "Middenvelder"),
    (22, "Brandon Mechele", "Verdediger"),
]
# De basiself tegen Portugal: rugnummer en gespeelde minuten.
B5_TELLEN = "Verdediger"
B5_BASIS = [
    (1, 90), (5, 90), (4, 90), (2, 78), (3, 90), (6, 90),
    (8, 65), (7, 90), (11, 72), (9, 85), (10, 90),
]
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1                  # 4
B5_EIND = B5_START + len(B5_BASIS) - 1    # 14
B5_ANTWOORD = B5_EIND + 2                 # 16 — drie antwoordregels
B5_TAB_START = 4
B5_TAB_EIND = B5_TAB_START + len(B5_TABEL) - 1   # 25


def zoek(rugnummer):
    """De juiste rij uit de spelerslijst van blad 5."""
    for rij in B5_TABEL:
        if rij[0] == rugnummer:
            return rij
    raise KeyError(rugnummer)
