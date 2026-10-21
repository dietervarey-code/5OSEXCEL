# -*- coding: utf-8 -*-
"""Gegevens voor de Minecraft-draaitabelbundel.

Vijf datasets, vijf keer dezelfde techniek op ander materiaal. Er staat in
deze bundel GEEN theorie: die staat in draaitabellen-en-grafieken.docx en de
opdracht verwijst er per blad naar.

WAT KLOPT EN WAT NIET
  Echt (Java-editie): de namen van de mobs, blokken, gereedschappen,
        updates en dorpelingenberoepen, hun categorie en dimensie, de
        levenspunten van de mobs, de duurzaamheid van het gereedschap, de
        jaartallen van de updates en het werkblok van elk beroep.
  Een keuze van ons: de indeling van blokken in categorieën en van updates in
        een hoofdthema. Daar valt over te discussiëren — en dat is meteen een
        les: een draaitabel is maar zo goed als de kolom waarop je ze bouwt.
  Verzonnen: het aantal aanbiedingen van de dorpelingen en het aantal nieuwe
        blokken per update.

Alles mag nagekeken worden op de wiki. Doe dat gerust: een leerling die een
fout vindt, heeft beter opgelet dan wie dat niet doet.
"""

TITEL = "Excel — Minecraft in draaitabellen"
ONDERTITEL = "Vijf datasets, vijf keer samenvatten zonder één formule"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
DUUR = 50

WAARSCHUWING = (
    "De gegevens in dit bestand komen uit de Java-editie van Minecraft. De "
    "namen, de levenspunten, de duurzaamheid en de jaartallen kloppen — je mag ze nakijken op de wiki, en wie een fout vindt "
    "krijgt een pluim. De indeling van de blokken in categorieën en van de "
    "updates in een thema is onze keuze; daar valt over te praten. Het aantal "
    "aanbiedingen van de dorpelingen en het aantal nieuwe blokken per update "
    "zijn verzonnen."
)

DIMENSIES = ["De End", "Nether", "Overworld"]

# ================================================================= blad 1
# Mobs. Rijen + Waarden: de eenvoudigste draaitabel die er is.
B1_KOP = ["Mob", "Categorie", "Dimensie", "Levenspunten"]
B1_CATEGORIEEN = ["Baas", "Neutraal", "Passief", "Vijandig"]
B1 = [
    ("Kip",            "Passief",  "Overworld",   4),
    ("Schaap",         "Passief",  "Overworld",   8),
    ("Varken",         "Passief",  "Overworld",  10),
    ("Koe",            "Passief",  "Overworld",  10),
    ("Konijn",         "Passief",  "Overworld",   3),
    ("Dorpeling",      "Passief",  "Overworld",  20),
    ("Wolf",           "Neutraal", "Overworld",   8),
    ("Enderman",       "Neutraal", "Overworld",  40),
    ("IJzergolem",     "Neutraal", "Overworld", 100),
    ("Bij",            "Neutraal", "Overworld",  10),
    ("Zombie",         "Vijandig", "Overworld",  20),
    ("Skelet",         "Vijandig", "Overworld",  20),
    ("Creeper",        "Vijandig", "Overworld",  20),
    ("Spin",           "Vijandig", "Overworld",  16),
    ("Heks",           "Vijandig", "Overworld",  26),
    ("Verdronkene",    "Vijandig", "Overworld",  20),
    ("Phantom",        "Vijandig", "Overworld",  20),
    ("Plunderaar",     "Vijandig", "Overworld",  24),
    ("Verwoester",     "Vijandig", "Overworld", 100),
    ("Bewaker",        "Vijandig", "Overworld",  30),
    ("Slijm",          "Vijandig", "Overworld",  16),
    ("Piglin",         "Neutraal", "Nether",     16),
    ("Zombiepiglin",   "Neutraal", "Nether",     20),
    ("Blaze",          "Vijandig", "Nether",     20),
    ("Ghast",          "Vijandig", "Nether",     10),
    ("Witherskelet",   "Vijandig", "Nether",     20),
    ("Hoglin",         "Vijandig", "Nether",     40),
    ("Magmakubus",     "Vijandig", "Nether",     16),
    ("Wither",         "Baas",     "Nether",    300),
    ("Shulker",        "Vijandig", "De End",     30),
    ("Endermiet",      "Vijandig", "De End",      8),
    ("Enderdraak",     "Baas",     "De End",    200),
]
B1_VOETNOOT = (
    "Levenspunten van de Java-editie; twee punten is één hartje. De Enderman "
    "staat bij de Overworld, maar je komt hem in alle drie de dimensies tegen. "
    "De Wither moet je zelf oproepen — hij spawnt nergens vanzelf."
)
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1
B1_ANKER = f"A{B1_EIND + 3}"

# ================================================================= blad 2
# Blokken. Kruistabel: Rijen én Kolommen.
B2_KOP = ["Blok", "Categorie", "Gereedschap", "Hardheid"]
B2_CATEGORIEEN = ["Bouwblok", "Erts", "Functioneel", "Natuurlijk"]
B2_GEREEDSCHAP = ["Bijl", "Geen", "Pikhouweel", "Schep"]
B2 = [
    ("Steen",          "Bouwblok",    "Pikhouweel", 1.5),
    ("Graniet",        "Bouwblok",    "Pikhouweel", 1.5),
    ("Andesiet",       "Bouwblok",    "Pikhouweel", 1.5),
    ("Zandsteen",      "Bouwblok",    "Pikhouweel", 0.8),
    ("Eikenplanken",   "Bouwblok",    "Bijl",       2.0),
    ("Eikenstam",      "Bouwblok",    "Bijl",       2.0),
    ("Obsidiaan",      "Bouwblok",    "Pikhouweel", 50.0),
    ("Wol",            "Bouwblok",    "Geen",       0.8),
    ("Glas",           "Bouwblok",    "Geen",       0.3),
    ("Kolenerts",      "Erts",        "Pikhouweel", 3.0),
    ("IJzererts",      "Erts",        "Pikhouweel", 3.0),
    ("Kopererts",      "Erts",        "Pikhouweel", 3.0),
    ("Gouderts",       "Erts",        "Pikhouweel", 3.0),
    ("Redstone-erts",  "Erts",        "Pikhouweel", 3.0),
    ("Lapiserts",      "Erts",        "Pikhouweel", 3.0),
    ("Diamanterts",    "Erts",        "Pikhouweel", 3.0),
    ("Smaragderts",    "Erts",        "Pikhouweel", 3.0),
    ("Oud puin",       "Erts",        "Pikhouweel", 30.0),
    ("Aarde",          "Natuurlijk",  "Schep",      0.5),
    ("Grasblok",       "Natuurlijk",  "Schep",      0.6),
    ("Zand",           "Natuurlijk",  "Schep",      0.5),
    ("Grind",          "Natuurlijk",  "Schep",      0.6),
    ("Klei",           "Natuurlijk",  "Schep",      0.6),
    ("Sneeuw",         "Natuurlijk",  "Schep",      0.1),
    ("Bladeren",       "Natuurlijk",  "Geen",       0.2),
    ("Netherrack",     "Natuurlijk",  "Pikhouweel", 0.4),
    ("Endsteen",       "Natuurlijk",  "Pikhouweel", 3.0),
    ("Werkbank",       "Functioneel", "Bijl",       2.5),
    ("Kist",           "Functioneel", "Bijl",       2.5),
    ("Oven",           "Functioneel", "Pikhouweel", 3.5),
    ("Aambeeld",       "Functioneel", "Pikhouweel", 5.0),
    ("Betoveringstafel", "Functioneel", "Pikhouweel", 5.0),
]
B2_VOETNOOT = (
    "Het gereedschap is wat je nodig hebt om er iets aan over te houden. De "
    "indeling in categorieën is onze keuze: netherrack kan je even goed een "
    "bouwblok noemen."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1
B2_ANKER = f"A{B2_EIND + 3}"

# ================================================================= blad 3
# Gereedschap. Som en sorteren — en het verschil tussen Aantal en Som.
B3_KOP = ["Gereedschap", "Materiaal", "Soort", "Duurzaamheid"]
B3_MATERIALEN = ["Diamant", "Goud", "Hout", "IJzer", "Netheriet", "Steen"]
B3_SOORTEN = ["Bijl", "Houweel", "Pikhouweel", "Schep", "Zwaard"]
B3_DUURZAAMHEID = {"Hout": 59, "Goud": 32, "Steen": 131,
                   "IJzer": 250, "Diamant": 1561, "Netheriet": 2031}
B3 = [(f"{soort} van {materiaal.lower()}", materiaal, soort,
       B3_DUURZAAMHEID[materiaal])
      for materiaal in ["Hout", "Steen", "IJzer", "Goud", "Diamant", "Netheriet"]
      for soort in B3_SOORTEN]
B3_VOETNOOT = (
    "Duurzaamheid is het aantal keren dat je het kan gebruiken voor het "
    "breekt. Binnen één materiaal is die voor elk soort gereedschap gelijk."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1
B3_ANKER = f"A{B3_EIND + 3}"

# ================================================================= blad 4
# Updates. Gemiddelde, groeperen per vijf jaar, filteren.
B4_KOP = ["Versie", "Naam", "Jaar", "Hoofdthema", "Nieuwe blokken"]
B4_THEMAS = ["Algemeen", "De End", "Nether", "Overworld"]
B4 = [
    ("1.0",  "Adventure Update",            2011, "Algemeen",  34),
    ("1.1",  "Beta-opvolger",               2012, "Algemeen",  12),
    ("1.2",  "Jungle Update",               2012, "Overworld", 21),
    ("1.3",  "Handel en bezienswaardigheden", 2012, "Overworld", 18),
    ("1.4",  "Pretty Scary Update",         2012, "Algemeen",  26),
    ("1.5",  "Redstone Update",             2013, "Algemeen",  23),
    ("1.6",  "Horse Update",                2013, "Overworld", 14),
    ("1.7",  "The Update that Changed the World", 2013, "Overworld", 38),
    ("1.8",  "Bountiful Update",            2014, "Overworld", 41),
    ("1.9",  "Combat Update",               2016, "De End",    27),
    ("1.10", "Frostburn Update",            2016, "Nether",    16),
    ("1.11", "Exploration Update",          2016, "Overworld", 19),
    ("1.12", "World of Color Update",       2017, "Algemeen",  31),
    ("1.13", "Update Aquatic",              2018, "Overworld", 44),
    ("1.14", "Village & Pillage",           2019, "Overworld", 52),
    ("1.15", "Buzzy Bees",                  2019, "Overworld",  9),
    ("1.16", "Nether Update",               2020, "Nether",    47),
    ("1.17", "Caves & Cliffs deel I",       2021, "Overworld", 43),
    ("1.18", "Caves & Cliffs deel II",      2021, "Overworld",  7),
    ("1.19", "The Wild Update",             2022, "Overworld", 36),
    ("1.20", "Trails & Tales",              2023, "Overworld", 29),
    ("1.21", "Tricky Trials",               2024, "Overworld", 33),
]
B4_VOETNOOT = (
    "Versienummers, namen en jaartallen van de Java-editie. Het hoofdthema is "
    "onze samenvatting in één woord; het aantal nieuwe blokken is verzonnen."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1
B4_ANKER = f"A{B4_EIND + 3}"
B4_GROEP_VAN = 2010
B4_GROEP_TOT = 2024
B4_GROEP_PER = 5
B4_FILTER = "Nether"

# ================================================================= blad 5
# Dorpelingen. EERST aanvullen met VERT.ZOEKEN, DAN de draaitabel.
B5_BEROEPEN = [
    # (beroep, werkblok, categorie)
    ("Boer",             "Composteerbak",   "Voedsel"),
    ("Visser",           "Ton",             "Voedsel"),
    ("Slager",           "Rookoven",        "Voedsel"),
    ("Herder",           "Weefgetouw",      "Bouw"),
    ("Pijlenmaker",      "Pijlmakerstafel", "Bouw"),
    ("Metselaar",        "Steenzaag",       "Bouw"),
    ("Bibliothecaris",   "Lessenaar",       "Kennis"),
    ("Cartograaf",       "Cartografietafel", "Kennis"),
    ("Geestelijke",      "Brouwstandaard",  "Kennis"),
    ("Wapensmid",        "Slijpsteen",      "Uitrusting"),
    ("Harnassmid",       "Hoogoven",        "Uitrusting"),
    ("Gereedschapssmid", "Smeedtafel",      "Uitrusting"),
    ("Leerbewerker",     "Ketel",           "Uitrusting"),
]
B5_KOP = ["Dorpeling", "Beroepcode", "Aanbiedingen",
          "Beroep", "Werkblok", "Categorie"]
# (naam, beroepnummer in B5_BEROEPEN (1-based), aanbiedingen)
B5 = [
    ("Dorpeling 01",  1,  6), ("Dorpeling 02",  7,  9),
    ("Dorpeling 03", 10,  5), ("Dorpeling 04",  4,  7),
    ("Dorpeling 05",  7, 11), ("Dorpeling 06",  2,  4),
    ("Dorpeling 07", 12,  8), ("Dorpeling 08",  1,  5),
    ("Dorpeling 09",  9,  6), ("Dorpeling 10",  5,  3),
    ("Dorpeling 11", 11,  7), ("Dorpeling 12",  8,  4),
    ("Dorpeling 13",  3,  6), ("Dorpeling 14",  7, 10),
    ("Dorpeling 15", 13,  5), ("Dorpeling 16",  6,  8),
    ("Dorpeling 17", 10,  6), ("Dorpeling 18",  2,  5),
    ("Dorpeling 19",  9,  7), ("Dorpeling 20",  4,  9),
]
B5_VOETNOOT = (
    "De beroepen en hun werkblok kloppen. Het aantal aanbiedingen is verzonnen."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_EIND = B5_START + len(B5) - 1
B5_ZOEKKOL = 8                       # kolom H: de beroepentabel staat ernaast
B5_ZOEKRIJ = B5_KOPRIJ
B5_ANKER = f"A{B5_EIND + 4}"
# de dorpeling die ze er achteraf bij typen (kaart 9)
B5_EXTRA = ("Dorpeling 21", 7, 12)


# ---------------------------------------------------------------- helpers
def beroepcode(nummer):
    return f"B-{nummer:02d}"


def beroep(nummer):
    if not 1 <= nummer <= len(B5_BEROEPEN):
        raise IndexError(
            f'beroepnummer {nummer} bestaat niet — er zijn er '
            f'{len(B5_BEROEPEN)}, dus de geldige nummers zijn 1 tot '
            f'{len(B5_BEROEPEN)}')
    return B5_BEROEPEN[nummer - 1]


def periode(jaar):
    """2016 -> '2015 - 2019', zoals Excel een groepering per vijf benoemt."""
    van = B4_GROEP_VAN + (jaar - B4_GROEP_VAN) // B4_GROEP_PER * B4_GROEP_PER
    return f"{van} - {van + B4_GROEP_PER - 1}"
