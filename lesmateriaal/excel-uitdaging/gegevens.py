# -*- coding: utf-8 -*-
"""Gegevens voor de uitdagingsopdracht: Halloween op Kasteel Ravenstein.

Eén avond, vijf werkbladen, 40 minuten. Bedoeld voor leerlingen die de
basisbundel en de herhaling vlot afwerken en meer willen.

Alles hangt aan elkaar: de omzet van blad 1 en de uren van blad 3 komen terug
op blad 5, en het einde van de dienst op blad 3 bepaalt mee wie op blad 4
overblijft. Verander je hier één cijfer, dan schuift de rest mee.
"""
from datetime import time

TITEL = "Halloween op Kasteel Ravenstein"
ONDERTITEL = "31 oktober · de nacht van de Zilveren Pompoen"

# ---------------------------------------------------------------- blad 1
# Boekingen. De prijs per persoon komt uit een staffel: VERT.ZOEKEN met
# WAAR, dus benaderend zoeken. De eerste kolom staat daarom oplopend.
B1_KOP = ["Boeking", "Groep", "Personen", "Tijdslot", "Kanaal",
          "Prijs p.p.", "Bedrag"]
B1_TARIEFKOP = ["Vanaf", "Groepsgrootte", "Prijs p.p."]
B1_TARIEVEN = [
    (1, "1 tot 4 personen", 14.00),
    (5, "5 tot 9 personen", 12.50),
    (10, "10 tot 19 personen", 11.00),
    (20, "20 personen of meer", 9.50),
]
B1 = [
    ("H-101", "Familie Vandeputte", 4, "18:00", "online"),
    ("H-102", "Chiro Ravenstein", 22, "18:00", "online"),
    ("H-103", "Klas 5OS", 18, "19:00", "online"),
    ("H-104", "Familie Soens", 3, "19:00", "kassa"),
    ("H-105", "Vriendengroep Kato", 7, "19:00", "online"),
    ("H-106", "Bedrijf Delvaux bv", 26, "20:00", "online"),
    ("H-107", "Familie Nolf", 5, "20:00", "kassa"),
    ("H-108", "Scouts Sint-Jan", 31, "20:00", "online"),
    ("H-109", "Familie Bauwens", 2, "20:00", "kassa"),
    ("H-110", "Jeugdhuis De Kelder", 14, "21:00", "online"),
    ("H-111", "Familie Deprez", 6, "21:00", "kassa"),
    ("H-112", "Fotoclub Lens", 9, "21:00", "online"),
    ("H-113", "Familie Oosterlinck", 4, "21:00", "kassa"),
    ("H-114", "Turnkring Flik-Flak", 24, "22:00", "online"),
    ("H-115", "Vriendengroep Joren", 8, "22:00", "kassa"),
    ("H-116", "Familie Tant", 5, "22:00", "kassa"),
    ("H-117", "Wandelclub Pas-Op", 17, "22:00", "online"),
    ("H-118", "Familie Ghijs", 3, "18:00", "kassa"),
    ("H-119", "KSA Ravenstein", 19, "18:00", "online"),
    ("H-120", "Familie Verlinde", 11, "19:00", "kassa"),
]
B1_GROOT = 10          # vanaf hoeveel personen we van een grote groep spreken
B1_KLEIN = 5           # onder hoeveel personen we van een kleine groep spreken
B1_START = 4
B1_EIND = B1_START + len(B1) - 1          # 23
B1_ANTWOORD = B1_EIND + 2                 # 25 — zeven antwoordregels
B1_TAR_START = 4
B1_TAR_EIND = B1_TAR_START + len(B1_TARIEVEN) - 1   # 7

# ---------------------------------------------------------------- blad 2
# Bezoekers per attractie per uurblok. Een kruistabel: totalen in twee
# richtingen, en daarna de naam van de drukste met INDEX en VERGELIJKEN.
B2_UREN = ["18u", "19u", "20u", "21u", "22u"]
B2 = [
    ("Kerkers", [62, 78, 95, 110, 84]),
    ("Spookzolder", [45, 58, 72, 88, 61]),
    ("Doolhof", [70, 92, 118, 134, 97]),
    ("Heksenkeuken", [38, 49, 63, 71, 52]),
    ("Grafkelder", [55, 67, 81, 96, 74]),
    ("Torenkamer", [29, 34, 41, 48, 36]),
]
B2_START = 4
B2_EIND = B2_START + len(B2) - 1          # 9
B2_TOTAALRIJ = B2_EIND + 2                # 11
B2_ANTWOORD = B2_TOTAALRIJ + 2            # 13 — vier antwoordregels

# ---------------------------------------------------------------- blad 3
# De ploegen van die avond. Rekenen met tijden, en een ALS met EN erin.
B3_KOP = ["Medewerker", "Rol", "Post", "Start", "Einde", "Uren", "Nachtploeg?"]
B3_GRENS_TIJD = time(22, 30)
B3_GRENS_UREN = 4
B3 = [
    ("Noor Baeyens", "Gids", "Kerkers", time(17, 30), time(22, 0)),
    ("Milan Coppens", "Gids", "Doolhof", time(18, 0), time(23, 0)),
    ("Fien Dewulf", "Techniek", "Spookzolder", time(17, 0), time(21, 30)),
    ("Senne Eeckhout", "Gids", "Grafkelder", time(18, 30), time(23, 0)),
    ("Lotte Fruytier", "Onthaal", "Onthaal", time(17, 0), time(22, 30)),
    ("Wout Gheysens", "Gids", "Heksenkeuken", time(18, 0), time(22, 0)),
    ("Amber Haegeman", "Bar", "Bar", time(18, 30), time(23, 30)),
    ("Jonas Impens", "Techniek", "Torenkamer", time(17, 30), time(21, 0)),
    ("Nina Jacobs", "Gids", "Kerkers", time(19, 0), time(23, 30)),
    ("Tuur Keirsebilck", "Toezicht", "Schatkamer", time(17, 0), time(20, 0)),
    ("Ella Lammens", "Gids", "Doolhof", time(19, 30), time(23, 0)),
    ("Victor Maes", "Toezicht", "Schatkamer", time(20, 0), time(23, 30)),
    ("Juul Nollet", "Onthaal", "Onthaal", time(18, 0), time(21, 0)),
    ("Lise Ostyn", "Gids", "Grafkelder", time(17, 30), time(22, 30)),
    ("Ruben Pieters", "Techniek", "Schatkamer", time(19, 0), time(22, 0)),
    ("Marie Quintens", "Bar", "Bar", time(17, 0), time(22, 0)),
]
B3_ROL_TELLEN = "Gids"
B3_ROL_KRUIS = ("Techniek", "Schatkamer")
B3_START = 4
B3_EIND = B3_START + len(B3) - 1          # 19
B3_SAMENVATTING = B3_EIND + 3             # 22 — zeven antwoordregels

# ---------------------------------------------------------------- blad 4
# De acht verdachten. Vijf getuigenissen worden samen één ALS met EN erin.
# Precies één naam blijft over; controleer.py bewaakt dat.
B4_KOP = ["Verdachte", "Badgescans 22-23u", "Kostuum", "Tas bij?",
          "Alibi bevestigd door", "Einde dienst", "Mogelijk?"]
B4_TIJDSTIP = time(22, 0)        # de dief was na dit uur nog aan het werk
B4_KLEUR = "zwart"
B4 = [
    # naam, badgescans, kostuum, tas bij, alibi
    ("Milan Coppens", 0, "zwart", "ja", "geen"),
    ("Senne Eeckhout", 2, "zwart", "ja", "Lotte Fruytier"),
    ("Amber Haegeman", 1, "rood", "ja", "geen"),
    ("Nina Jacobs", 3, "zwart", "nee", "geen"),
    ("Ella Lammens", 1, "zwart", "ja", "geen"),
    ("Victor Maes", 4, "wit", "ja", "geen"),
    ("Lise Ostyn", 0, "zwart", "ja", "geen"),
    ("Ruben Pieters", 5, "zwart", "nee", "geen"),
]
B4_MOGELIJK = "MOGELIJK"
B4_UITGESLOTEN = "uitgesloten"
B4_KOPRIJ = 4
B4_START = B4_KOPRIJ + 1                  # 5
B4_EIND = B4_START + len(B4) - 1          # 12
B4_ANTWOORD = B4_EIND + 2                 # 14 — twee antwoordregels

# ---------------------------------------------------------------- blad 5
# De afrekening van de avond. Haalt cijfers van blad 1 en blad 3 op.
B5_BAROMZET = 1842.50
B5_UURLOON = 18.50
B5_DECOR = 1250.00
B5_CATERING = 680.00


def tarief(personen):
    """De prijs per persoon volgens de staffel — zoals VERT.ZOEKEN met WAAR."""
    gekozen = None
    for vanaf, _, prijs in B1_TARIEVEN:
        if personen >= vanaf:
            gekozen = prijs
    if gekozen is None:
        raise ValueError(f'geen tarief voor {personen} personen')
    return gekozen


def duur_in_uren(start, einde):
    """Het verschil tussen twee tijden, in uren — zoals (einde-start)*24."""
    return ((einde.hour * 60 + einde.minute) - (start.hour * 60 + start.minute)) / 60


# De vaste plaatsen op blad 5. Eén woordenboek, zodat opdracht, startbestand
# en sleutel nooit uit elkaar lopen.
B5_RIJ = dict(ticket=4, bar=5, opbrengst=6,
              uren=9, uurloon=10, loonkost=11, decor=12, catering=13, kosten=14,
              winst=17, marge=18, per_bezoeker=19)
