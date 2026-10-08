# -*- coding: utf-8 -*-
"""Gegevens voor de vijf detectivezaken.

Elke zaak staat op zichzelf: één werkblad, ongeveer 25 minuten, zes
basisformules en precies één geneste functie die de zaak kraakt. Elke zaak
heeft een andere soort nesting, zodat ze vijf keer iets anders leren.

Alles wordt zelfstandig gemaakt, zonder leerkracht erbij. Daarom staat bij
elke zaak een controlegetal in de opdracht: daarmee weten ze zelf of ze goed
zitten, zonder dat iemand het antwoord hoeft te geven.

Personen, bedrijven en voorvallen zijn verzonnen.
"""

TITEL = "Excel — vijf detectivezaken"
ONDERTITEL = "vijf losse zaken van ongeveer 25 minuten"
WAARSCHUWING = ("Alle personen, bedrijven en voorvallen in dit bestand zijn verzonnen. "
                "Elke gelijkenis met echte mensen berust op toeval.")

# =====================================================================
#  ZAAK 1 — De verdwenen avonden
#  Nesting: EN binnen ALS
# =====================================================================
Z1_GRENS = 30            # minder dan zoveel minuten overwerk is geen overwerk
Z1_DADERCODE = 'H-05'
Z1_KOP = ["Datum", "Wat Rudi zei", "Minuten over", "Bedrag", "Code", "Handelaar",
          "Klopt het?"]
Z1_ZOEKKOP = ["Code", "Handelaar"]
Z1_HANDELAARS = [
    ("H-01", "Broodjeszaak De Korf"),
    ("H-02", "Tankstation Ring Oost"),
    ("H-03", "Supermarkt Delmo"),
    ("H-04", "Café De Zwaan"),
    ("H-05", "Dansschool Tango Nova"),
    ("H-06", "Apotheek Vermeulen"),
]
# datum, wat hij zei, minuten overwerk volgens de badge, bedrag, handelaarscode
Z1 = [
    ("02/09", "overwerk", 90, 12.40, "H-01"),
    ("03/09", "sport", 0, 6.50, "H-01"),
    ("04/09", "overwerk", 0, 45.00, "H-05"),
    ("05/09", "overwerk", 60, 8.75, "H-01"),
    ("09/09", "thuis", 0, 38.90, "H-03"),
    ("10/09", "sport", 0, 52.00, "H-02"),
    ("11/09", "overwerk", 0, 45.00, "H-05"),
    ("12/09", "thuis", 0, 7.80, "H-01"),
    ("16/09", "overwerk", 120, 21.30, "H-03"),
    ("17/09", "sport", 0, 11.25, "H-04"),
    ("18/09", "overwerk", 15, 45.00, "H-05"),
    ("19/09", "thuis", 0, 64.30, "H-03"),
    ("23/09", "overwerk", 45, 9.60, "H-01"),
    ("24/09", "sport", 0, 49.50, "H-02"),
    ("25/09", "overwerk", 0, 45.00, "H-05"),
    ("26/09", "thuis", 0, 15.60, "H-06"),
    ("01/10", "sport", 0, 9.40, "H-04"),
    ("02/10", "overwerk", 20, 45.00, "H-05"),
    ("07/10", "overwerk", 75, 14.20, "H-03"),
    ("09/10", "overwerk", 0, 45.00, "H-05"),
]
Z1_LEUGEN, Z1_KLOPT = "LEUGEN", "klopt"
Z1_KOPRIJ = 4
Z1_START = Z1_KOPRIJ + 1                   # 5
Z1_EIND = Z1_START + len(Z1) - 1           # 24
Z1_ANTWOORD = Z1_EIND + 2                  # 26 — vijf antwoordregels
Z1_TAB_START = 5
Z1_TAB_EIND = Z1_TAB_START + len(Z1_HANDELAARS) - 1   # 10

# =====================================================================
#  ZAAK 2 — De Mercedes van de Koning
#  Nesting: MAX binnen VERT.ZOEKEN
# =====================================================================
Z2_KOP = ["Rit", "Datum", "Chauffeur", "Vertrek", "Km vertrek", "Km aankomst",
          "Bestemming", "Afstand"]
Z2_CHAUFFEURS = ["Vermeiren", "Claeys", "Dubois", "onbekend"]
# Het logboek lag door elkaar toen het gevonden werd: de ritten staan niet op
# volgorde. De kilometerstanden verraden wel welke rit de laatste was.
# rit, datum, chauffeur, vertrekplaats, km vertrek, km aankomst, bestemming
Z2 = [
    (7, "14/03", "Vermeiren", "Brussel", 84643, 84729, "Namen"),
    (14, "22/03", "Vermeiren", "Mechelen", 85852, 85906, "Brussel"),
    (3, "11/03", "Claeys", "Brussel", 84265, 84412, "Oostende"),
    (11, "19/03", "Dubois", "Brussel", 85640, 85719, "Gent"),
    (1, "10/03", "Vermeiren", "Brussel", 84120, 84198, "Antwerpen"),
    (16, "24/03", "onbekend", "Hasselt", 85969, 86041, "Hoeve Ter Linden"),
    (5, "12/03", "Dubois", "Brussel", 84559, 84601, "Leuven"),
    (9, "17/03", "Claeys", "Brussel", 84815, 85235, "Luxemburg"),
    (12, "19/03", "Dubois", "Gent", 85719, 85798, "Brussel"),
    (2, "10/03", "Vermeiren", "Antwerpen", 84198, 84265, "Brussel"),
    (15, "23/03", "Claeys", "Brussel", 85906, 85969, "Hasselt"),
    (6, "12/03", "Dubois", "Leuven", 84601, 84643, "Brussel"),
    (10, "18/03", "Claeys", "Luxemburg", 85235, 85640, "Brussel"),
    (4, "11/03", "Claeys", "Oostende", 84412, 84559, "Brussel"),
    (13, "22/03", "Vermeiren", "Brussel", 85798, 85852, "Mechelen"),
    (8, "15/03", "Vermeiren", "Namen", 84729, 84815, "Brussel"),
]
Z2_KOPRIJ = 3
Z2_START = Z2_KOPRIJ + 1                   # 4
Z2_EIND = Z2_START + len(Z2) - 1           # 19
Z2_BLOK = Z2_EIND + 2                      # 21 — koprij van het chauffeursblokje
Z2_PER_CHAUFFEUR = Z2_BLOK + 1             # 22 — vier rijen
Z2_ANTWOORD = Z2_PER_CHAUFFEUR + len(Z2_CHAUFFEURS) + 1    # 27 — vijf regels

# =====================================================================
#  ZAAK 3 — De museumroof
#  Nesting: AANTAL.ALS binnen ALS
# =====================================================================
Z3_KOP = ["Catalogusnr", "Stuk", "Zaalcode", "Zaal", "Waarde", "Status"]
Z3_ZAALKOP = ["Code", "Zaal"]
Z3_ZALEN = [
    ("Z1", "Schilderijenzaal"),
    ("Z2", "Zaal van de Oudheid"),
    ("Z3", "Zilverkamer"),
    ("Z4", "Moderne vleugel"),
]
# catalogusnummer, stuk, zaalcode, geschatte waarde
Z3 = [
    ("K-101", "Portret van een onbekende vrouw", "Z1", 185000),
    ("K-102", "Winterlandschap met molen", "Z1", 142000),
    ("K-103", "Stilleven met citroenen", "Z1", 96000),
    ("K-104", "Zelfportret in blauw", "Z1", 210000),
    ("K-105", "Romeinse olielamp", "Z2", 4200),
    ("K-106", "Grieks drinkschaaltje", "Z2", 7800),
    ("K-107", "Bronzen speerpunt", "Z2", 3100),
    ("K-108", "Mozaïekfragment", "Z2", 15400),
    ("K-109", "Zilveren tabaksdoos", "Z3", 12800),
    ("K-110", "Zilveren kandelaar (paar)", "Z3", 24500),
    ("K-111", "Zilveren suikerstrooier", "Z3", 9600),
    ("K-112", "Zilveren zakhorloge", "Z3", 18700),
    ("K-113", "Zilveren soeplepel", "Z3", 5400),
    ("K-114", "Zilveren theepot", "Z3", 31200),
    ("K-115", "Zilveren vingerhoedje", "Z3", 2100),
    ("K-116", "Neonsculptuur 'Puls'", "Z4", 46000),
    ("K-117", "Videowerk 'Stille lijn'", "Z4", 28000),
    ("K-118", "Installatie 'Zeven stoelen'", "Z4", 39500),
    ("K-119", "Fotoreeks 'Haven'", "Z4", 17200),
    ("K-120", "Keramiek 'Scherf nr. 4'", "Z4", 11300),
]
# Wat de conservator 's ochtends terugvond. Vier nummers ontbreken.
Z3_TELLING = [
    "K-101", "K-102", "K-103", "K-104", "K-105", "K-106", "K-107", "K-108",
    "K-111", "K-113", "K-115", "K-116", "K-117", "K-118", "K-119", "K-120",
]
Z3_GESTOLEN, Z3_AANWEZIG = "GESTOLEN", "aanwezig"
Z3_KOPRIJ = 3
Z3_START = Z3_KOPRIJ + 1                   # 4
Z3_EIND = Z3_START + len(Z3) - 1           # 23
Z3_ANTWOORD = Z3_EIND + 2                  # 25 — vijf antwoordregels
Z3_TEL_START = 4
Z3_TEL_EIND = Z3_TEL_START + len(Z3_TELLING) - 1      # 19
Z3_ZAAL_START = 4
Z3_ZAAL_EIND = Z3_ZAAL_START + len(Z3_ZALEN) - 1      # 7

# =====================================================================
#  ZAAK 4 — Het gelekte examen
#  Nesting: SOM.ALS binnen ALS
# =====================================================================
Z4_GRENS = 20            # vanaf zoveel bestanden samen wordt het verdacht
Z4_KOP = ["Logregel", "Gebruiker", "Dag", "Tijdstip", "Bestanden"]
Z4_GEBRUIKERKOP = ["Code", "Naam", "Functie"]
Z4_GEBRUIKERS = [
    ("G-01", "mevr. Dekeyser", "leerkracht wiskunde"),
    ("G-02", "dhr. Boone", "leerkracht wiskunde"),
    ("G-03", "mevr. Tytgat", "directie"),
    ("G-04", "dhr. Serneels", "ICT-coördinator"),
    ("G-05", "Lars Vermote", "leerling 6TW"),
    ("G-06", "Yasmine Ait Allal", "leerling 6TW"),
    ("G-07", "mevr. Cornelis", "secretariaat"),
    ("G-08", "Jonas Debbaut", "leerling 6TW"),
]
# logregel, gebruikerscode, dag, tijdstip, aantal bestanden geopend
Z4 = [
    ("L-01", "G-01", "maandag", "08:15", 5),
    ("L-02", "G-05", "maandag", "12:40", 7),
    ("L-03", "G-02", "maandag", "14:22", 6),
    ("L-04", "G-04", "maandag", "16:05", 9),
    ("L-05", "G-01", "maandag", "17:30", 4),
    ("L-06", "G-03", "dinsdag", "08:50", 6),
    ("L-07", "G-06", "dinsdag", "10:15", 8),
    ("L-08", "G-07", "dinsdag", "11:40", 4),
    ("L-09", "G-02", "dinsdag", "13:05", 3),
    ("L-10", "G-01", "dinsdag", "15:20", 5),
    ("L-11", "G-08", "dinsdag", "16:45", 2),
    ("L-12", "G-04", "dinsdag", "18:10", 9),
    ("L-13", "G-06", "dinsdag", "19:25", 4),
    ("L-14", "G-08", "dinsdag", "23:40", 9),
    ("L-15", "G-08", "dinsdag", "23:52", 12),
    ("L-16", "G-03", "woensdag", "07:55", 3),
    ("L-17", "G-07", "woensdag", "09:30", 2),
    ("L-18", "G-02", "woensdag", "10:45", 4),
    ("L-19", "G-05", "woensdag", "12:15", 5),
    ("L-20", "G-01", "woensdag", "13:50", 3),
    ("L-21", "G-06", "woensdag", "15:05", 3),
    ("L-22", "G-04", "woensdag", "16:20", 1),
]
Z4_VERDACHT, Z4_VRIJ = "VERDACHT", "vrij"
Z4_KOPRIJ = 4
Z4_START = Z4_KOPRIJ + 1                   # 5
Z4_EIND = Z4_START + len(Z4) - 1           # 26
Z4_BLOK = Z4_EIND + 2                      # 28 — koprij van het gebruikersblokje
Z4_PER_GEBRUIKER = Z4_BLOK + 1             # 29 — acht rijen
Z4_ANTWOORD = Z4_PER_GEBRUIKER + len(Z4_GEBRUIKERS) + 1   # 38 — vier regels
Z4_TAB_START = 5
Z4_TAB_EIND = Z4_TAB_START + len(Z4_GEBRUIKERS) - 1       # 12

# =====================================================================
#  ZAAK 5 — De sabotage in de chocoladefabriek
#  Nesting: VERT.ZOEKEN binnen ALS
# =====================================================================
Z5_GRENS = 0.15          # vanaf zoveel afkeur is een batch niet normaal meer
Z5_KOP = ["Batch", "Machine", "Ploeg", "Geproduceerd", "Afgekeurd", "Afkeur",
          "Laatst nagekeken door"]
Z5_MACHINEKOP = ["Code", "Machine", "Laatst nagekeken door"]
Z5_MACHINES = [
    ("M1", "Tempereermachine 1", "Dhondt"),
    ("M2", "Tempereermachine 2", "Vercammen"),
    ("M3", "Vormlijn A", "Dhondt"),
    ("M4", "Vormlijn B", "Peeters"),
    ("M5", "Koeltunnel", "Vercammen"),
    ("M6", "Verpakkingslijn", "Peeters"),
]
Z5_TECHNICI = ["Dhondt", "Vercammen", "Peeters"]
# batch, machine, ploeg, geproduceerd, afgekeurd
Z5 = [
    ("B-01", "M1", "A", 500, 32),
    ("B-02", "M2", "A", 500, 118),
    ("B-03", "M3", "A", 520, 41),
    ("B-04", "M4", "A", 480, 27),
    ("B-05", "M5", "A", 510, 36),
    ("B-06", "M6", "A", 495, 22),
    ("B-07", "M1", "B", 505, 38),
    ("B-08", "M2", "B", 490, 104),
    ("B-09", "M3", "B", 515, 45),
    ("B-10", "M4", "B", 500, 31),
    ("B-11", "M5", "B", 485, 97),
    ("B-12", "M6", "B", 510, 25),
    ("B-13", "M1", "C", 495, 29),
    ("B-14", "M2", "C", 520, 53),
    ("B-15", "M3", "C", 500, 43),
    ("B-16", "M4", "C", 490, 34),
    ("B-17", "M5", "C", 505, 132),
    ("B-18", "M6", "C", 515, 20),
    ("B-19", "M1", "A", 500, 35),
    ("B-20", "M2", "A", 480, 126),
    ("B-21", "M3", "A", 510, 48),
    ("B-22", "M4", "A", 495, 30),
    ("B-23", "M5", "A", 500, 44),
    ("B-24", "M6", "A", 505, 26),
]
Z5_GEEN = "-"
Z5_KOPRIJ = 4
Z5_START = Z5_KOPRIJ + 1                   # 5
Z5_EIND = Z5_START + len(Z5) - 1           # 28
Z5_ANTWOORD = Z5_EIND + 2                  # 30 — vijf antwoordregels
Z5_TAB_START = 5
Z5_TAB_EIND = Z5_TAB_START + len(Z5_MACHINES) - 1         # 10


def handelaar(code):
    for rij in Z1_HANDELAARS:
        if rij[0] == code:
            return rij
    raise KeyError(code)


def zaal(code):
    for rij in Z3_ZALEN:
        if rij[0] == code:
            return rij
    raise KeyError(code)


def gebruiker(code):
    for rij in Z4_GEBRUIKERS:
        if rij[0] == code:
            return rij
    raise KeyError(code)


def machine(code):
    for rij in Z5_MACHINES:
        if rij[0] == code:
            return rij
    raise KeyError(code)
