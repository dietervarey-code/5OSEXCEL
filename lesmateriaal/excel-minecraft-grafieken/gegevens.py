# -*- coding: utf-8 -*-
"""Gegevens voor de Minecraft-grafiekbundel.

Vijf datasets, vijf keer een ander grafiektype. Er staat in deze bundel GEEN
theorie: die staat in draaitabellen-en-grafieken.docx, kaart 10 tot 14, en de
opdracht verwijst er per blad naar.

WAT KLOPT EN WAT NIET
  Echt (Java-editie): de namen van de mobs, de dimensie waar ze thuishoren,
        hun levenspunten, de schade van zwaard, bijl en hak per materiaal, de
        namen van de dorpelingenberoepen en hun werkblok, en de items die ze
        verhandelen.
  Verzonnen: de diamantvondsten per Y-niveau, de verdeling van de
        ertsvondsten en de prijzen in smaragden. Ze lijken op wat je in het
        spel ziet, maar ze zijn gekozen om mee te kunnen rekenen.

Alles mag nagekeken worden op de wiki. Een leerling die een fout vindt, heeft
beter opgelet dan wie dat niet doet.
"""

TITEL = "Excel — Minecraft in grafieken"
ONDERTITEL = "Vijf datasets, vijf keer het juiste grafiektype kiezen"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
ZUSTERBUNDEL = "excel-minecraft-draaitabellen"
DUUR = 50

WAARSCHUWING = (
    "De namen in dit bestand zijn echt, en de levenspunten en de schade per "
    "wapen ook: die komen uit de Java-editie en je mag ze nakijken op de wiki. "
    "VERZONNEN ZIJN: de diamantvondsten per diepte, de verdeling van de "
    "ertsvondsten en de prijzen in smaragden. Een grafiek maakt een getal "
    "overtuigend; let erop dat je niet overtuigend wordt over iets dat niet "
    "klopt."
)

DIMENSIES = ["De End", "Nether", "Overworld"]

# ================================================================= blad 1
# Levenspunten van tien mobs. Staafdiagram: vergelijken.
B1_KOP = ["Mob", "Dimensie", "Levenspunten"]
B1 = [
    ("Hoglin",     "Nether",    40),
    ("Bewaker",    "Overworld", 30),
    ("Heks",       "Overworld", 26),
    ("Plunderaar", "Overworld", 24),
    ("Zombie",     "Overworld", 20),
    ("Spin",       "Overworld", 16),
    ("Ghast",      "Nether",    10),
    ("Wolf",       "Overworld",  8),
    ("Kip",        "Overworld",  4),
    ("Konijn",     "Overworld",  3),
]
B1_VOETNOOT = (
    "Tien bekende mobs, al gesorteerd van taai naar teer. Twee levenspunten is "
    "één hartje. De bazen staan er niet bij: de Wither heeft er 300 en dan zie "
    "je van de rest niets meer."
)
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1
B1_SOORT = "staafdiagram"
B1_TITEL = "Levenspunten per mob"

# ================================================================= blad 2
# Diamanten per Y-niveau. Lijndiagram: een verloop met een piek.
B2_KOP = ["Y-niveau", "Diamanten per 1000 blokken", "Verschil met de vorige meting"]
B2 = [
    (60, 0), (40, 1), (20, 2), (0, 4), (-20, 7),
    (-40, 12), (-50, 18), (-55, 21), (-59, 24), (-63, 15),
]
B2_VOETNOOT = (
    "Verzonnen cijfers, maar de vorm klopt: boven Y = 16 vind je zo goed als "
    "niets, de piek ligt rond Y = -59, en daaronder zit het grondgesteente in "
    "de weg. Let op: de metingen liggen niet even ver uit elkaar. Bovenaan "
    "springt het per 20 niveaus, onderaan per 4."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1
B2_SOORT = "lijndiagram"
B2_TITEL = "Diamanten per diepte"

# ================================================================= blad 3
# Welke erts vond je? Cirkeldiagram: aandeel van een geheel.
B3_KOP = ["Erts", "Gevonden", "Aandeel"]
B3 = [
    ("Redstone", 80),
    ("IJzer",    60),
    ("Lapis",    30),
    ("Goud",     20),
    ("Diamant",  10),
]
B3_VOETNOOT = (
    "Tweehonderd ertsblokken, gevonden tijdens één lange graafsessie rond "
    "Y = -55. Verzonnen cijfers. Juist omdat de vijf soorten samen álle "
    "vondsten zijn, mag hier een cirkeldiagram."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1
B3_SOORT = "cirkeldiagram"
B3_TITEL = "Aandeel in de ertsvondsten"

# ================================================================= blad 4
# Schade per wapen en materiaal. Drie reeksen in één grafiek.
B4_KOP = ["Materiaal", "Zwaard", "Bijl", "Hak"]
B4_WAPENS = ["Zwaard", "Bijl", "Hak"]
B4 = [
    ("Hout",      4,  7, 1),
    ("Steen",     5,  9, 1),
    ("IJzer",     6,  9, 1),
    ("Diamant",   7,  9, 1),
    ("Netheriet", 8, 10, 1),
]
B4_VOETNOOT = (
    "Schade per slag in de Java-editie; deze cijfers kloppen. Wat er NIET in "
    "staat: de bijl slaat veel trager dan het zwaard. Per slag wint de bijl, "
    "per seconde niet. Je grafiek kan daar niets over zeggen, en toch zal ze "
    "er overtuigd uitzien."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1
B4_SOORT = "staafdiagram met drie reeksen"
B4_TITEL = "Schade per slag"

# ================================================================= blad 5
# Dorpelingenhandel. EERST aanvullen met VERT.ZOEKEN, DAN een grafiek.
B5_BEROEPEN = [
    # (beroep, werkblok)
    ("Boer",             "Composteerbak"),
    ("Visser",           "Ton"),
    ("Slager",           "Rookoven"),
    ("Herder",           "Weefgetouw"),
    ("Pijlenmaker",      "Pijlmakerstafel"),
    ("Metselaar",        "Steenzaag"),
    ("Bibliothecaris",   "Lessenaar"),
    ("Cartograaf",       "Cartografietafel"),
    ("Geestelijke",      "Brouwstandaard"),
    ("Wapensmid",        "Slijpsteen"),
    ("Harnassmid",       "Hoogoven"),
    ("Gereedschapssmid", "Smeedtafel"),
    ("Leerbewerker",     "Ketel"),
]
B5_KOP = ["Item", "Beroepcode", "Prijs (smaragden)", "Beroep", "Werkblok"]
# (item, beroepnummer in B5_BEROEPEN (1-based), prijs)
B5 = [
    ("Betoverd boek",                7, 30),
    ("Diamanten borstplaat",        11, 27),
    ("Diamanten bijl",              12, 24),
    ("Diamanten zwaard",            10, 22),
    ("Bosontdekkerskaart",           8, 19),
    ("Oceaanontdekkerskaart",        8, 17),
    ("Betoverd ijzeren pikhouweel", 12, 15),
    ("Ervaringsfles",                9, 13),
    ("Zadel",                       13, 11),
    ("Klok",                         7,  9),
    ("Kompas",                       8,  6),
    ("Gouden wortel",                1,  3),
]
B5_VOETNOOT = (
    "De items en de beroepen die ze verkopen kloppen; de prijzen zijn "
    "verzonnen. In het spel hangt de prijs af van het niveau van de dorpeling, "
    "van je reputatie in het dorp en van de vraag of hij net gered is uit een "
    "zombie-aanval. Eén vast getal bestaat dus niet."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_EIND = B5_START + len(B5) - 1
B5_ZOEKKOL = 7                       # kolom G: de beroepentabel staat ernaast
B5_ZOEKRIJ = B5_KOPRIJ
B5_SOORT = "staafdiagram"
B5_TITEL = "Prijs per item"


# ---------------------------------------------------------------- helpers
def beroepcode(nummer):
    return f"B-{nummer:02d}"


def beroep(nummer):
    if not 1 <= nummer <= len(B5_BEROEPEN):
        raise IndexError(
            f'beroepnummer {nummer} bestaat niet — de beroepentabel telt '
            f'{len(B5_BEROEPEN)} beroepen, dus de geldige nummers zijn 1 tot '
            f'{len(B5_BEROEPEN)}')
    return B5_BEROEPEN[nummer - 1]
