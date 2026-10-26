# -*- coding: utf-8 -*-
"""Gegevens voor de tekstbundel: de line-up van Zomerklank opkuisen.

Vijf werkbladen. Telkens dezelfde situatie: er komt een lijst uit een systeem
en die deugt niet. De leerling maakt er een bruikbare lijst van, en op blad 5
wordt die lijst een tabel met een draaitabel, een draaigrafiek en een slicer.

WAT KLOPT EN WAT NIET
  Zomerklank bestaat niet. De artiesten, de podia, de boekingscodes en de
  crewleden zijn allemaal verzonnen. Dat is hier geen probleem: wat je
  oefent is het opkuisen, en de rommel is wél echt. Zo komt een line-up uit
  een boekingssysteem, met de spaties, de hoofdletters en de dubbele regels
  erbij.
"""

TITEL = "Excel — de line-up van Zomerklank opkuisen"
ONDERTITEL = "Vijf keer een lijst die niet deugt, en wat je eraan doet"
FESTIVAL = "Zomerklank"
DOMEIN = "zomerklank.be"
ZUSTERBUNDEL = "excel-festival-datums"
DUUR = 50

WAARSCHUWING = (
    "Zomerklank bestaat niet en de artiesten evenmin. Alles in dit bestand is "
    "verzonnen — behalve de rommel. Zo ziet een lijst er echt uit als ze uit "
    "een boekingssysteem komt: spaties waar ze niet horen, hoofdletters door "
    "elkaar, drie velden in één cel en een paar regels dubbel. Dat opkuisen is "
    "het werk."
)

# ================================================================= blad 1
# Vaste lengte: LINKS en RECHTS. En de les dat tekst geen getal is.
B1_KOP = ["Artiest", "Artiestcode", "Land", "Jaar (tekst)", "Jaar (getal)"]
B1_LANDEN = ["BE", "DE", "FR", "NL", "SE", "UK", "US"]
# (artiest, land, jaar van hun eerste optreden op Zomerklank)
B1 = [
    ("Nachtkever",          "BE", 2019),
    ("Lotte & de Wolken",   "BE", 2016),
    ("Blauwe Maandag",      "BE", 2021),
    ("Kaai 12",             "BE", 2022),
    ("Zoutelande Zeven",    "NL", 2018),
    ("Kompaan",             "NL", 2020),
    ("The Paper Tigers",    "UK", 2014),
    ("Velvet Grid",         "UK", 2022),
    ("Marée Haute",         "FR", 2017),
    ("Les Bruyères",        "FR", 2023),
    ("Nordlicht",           "DE", 2015),
    ("Kabelbrand",          "DE", 2019),
    ("Silverhorn",          "US", 2013),
    ("Dust & Denim",        "US", 2021),
    ("Fjärran",             "SE", 2018),
    ("Havsbris",            "SE", 2024),
]
B1_VOETNOOT = (
    "De artiestcode is altijd even lang: twee letters land, vier cijfers jaar. "
    "Daarom kan je hier met LINKS en RECHTS werken."
)
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1

# ================================================================= blad 2
# Geen vaste lengte: VIND.ALLES, LENGTE.
B2_KOP = ["Regel uit het systeem", "Podium", "Artiest", "Lengte van de naam"]
B2_SCHEIDING = " | "
B2_PODIA = ["Bostent", "Klub C", "Main Stage", "Strandbar"]
# (podium, artiest)
B2 = [
    ("Main Stage", "Nachtkever"),
    ("Main Stage", "The Paper Tigers"),
    ("Main Stage", "Silverhorn"),
    ("Main Stage", "Lotte & de Wolken"),
    ("Main Stage", "Havsbris"),
    ("Main Stage", "Dust & Denim"),
    ("Klub C",     "Blauwe Maandag"),
    ("Klub C",     "Kompaan"),
    ("Klub C",     "Velvet Grid"),
    ("Klub C",     "Kabelbrand"),
    ("Klub C",     "Fjärran"),
    ("Bostent",    "Marée Haute"),
    ("Bostent",    "Les Bruyères"),
    ("Bostent",    "Nordlicht"),
    ("Bostent",    "Kaai 12"),
    ("Strandbar",  "Zoutelande Zeven"),
    ("Strandbar",  "Hofnar"),
    ("Strandbar",  "Pier 7"),
]
B2_VOETNOOT = (
    "Podium en artiest staan in één cel, gescheiden door een streepje met een "
    "spatie ervoor en erna. De namen zijn níét even lang — daarom werkt de "
    "aanpak van blad 1 hier niet."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1

# ================================================================= blad 3
# Vaste posities midden in de tekst: DEEL.
B3_KOP = ["Boekingscode", "Dag", "Podiumcode", "Volgnummer"]
B3_VOORVOEGSEL = "ZK26"
B3_DAGEN = ["VR", "ZA", "ZO"]
B3_PODIUMCODES = ["BOST", "KLUB", "MAIN", "STRA"]
# (dag, podiumcode, volgnummer)
B3 = [
    ("VR", "MAIN",   7), ("VR", "MAIN",  12), ("VR", "KLUB",  23),
    ("VR", "KLUB",  31), ("VR", "BOST",  44), ("VR", "STRA",  52),
    ("ZA", "MAIN",  61), ("ZA", "MAIN",  68), ("ZA", "MAIN",  74),
    ("ZA", "KLUB",  83), ("ZA", "KLUB",  91), ("ZA", "KLUB", 105),
    ("ZA", "BOST", 112), ("ZA", "STRA", 126), ("ZO", "MAIN", 134),
    ("ZO", "MAIN", 141), ("ZO", "KLUB", 158), ("ZO", "BOST", 163),
    ("ZO", "STRA", 177), ("ZO", "STRA", 189),
]
B3_VOETNOOT = (
    "Een boekingscode is altijd op dezelfde manier opgebouwd: ZK26, een "
    "streepje, de dag, een streepje, het podium, een streepje, het "
    "volgnummer. Elk stuk staat dus altijd op dezelfde plaats."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1

# ================================================================= blad 4
# Spaties en hoofdletters: SPATIES.WISSEN, BEGINLETTERS, en & om te plakken.
B4_KOP = ["Achternaam (ruw)", "Voornaam (ruw)", "Naam", "E-mailadres",
          "Lengte"]
# (achternaam zoals ze binnenkwam, voornaam zoals ze binnenkwam)
B4 = [
    ("  VANDENBERGHE ", " lotte  "),
    ("peeters", "  JONAS"),
    (" DE SMET  ", "amina "),
    ("Willems ", "  youssef"),
    ("  MERTENS", "ELISE  "),
    ("claes  ", " Bilal "),
    (" JANSSENS ", "  noor"),
    ("maes", "SAM  "),
    ("  WOUTERS ", " ayla  "),
    ("goossens ", "  LIAM"),
    (" DE COCK  ", "fatima "),
    ("hermans  ", " THIBAULT "),
    ("  LAMBRECHTS", "  zeynep "),
    ("van damme ", "ROBBE  "),
    (" SEGERS  ", " ilyas"),
    ("boeckx", "  MARGOT  "),
]
B4_VOETNOOT = (
    "Zestien vrijwilligers, aangemeld via drie verschillende formulieren. De "
    "een typte alles in hoofdletters, de ander plakte er spaties bij. Je ziet "
    "die spaties niet — maar Excel wel. Let op de dubbele achternamen: daar "
    "staat een spatie MIDDEN in, en die moet net blijven staan in de naam en "
    "verdwijnen in het e-mailadres."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1

# ================================================================= blad 5
# Opkuisen zonder formules, en dan de payoff: tabel, draaitabel,
# draaigrafiek en slicer.
B5_KOP = ["Artiest", "Dag", "Podium", "Genre"]
B5_GENRES = ["Elektro", "Hiphop", "Indie", "Rock"]
B5_SCHOON = [
    ("Nachtkever",        "vrijdag",  "Main Stage", "Indie"),
    ("The Paper Tigers",  "vrijdag",  "Main Stage", "Rock"),
    ("Blauwe Maandag",    "vrijdag",  "Klub C",     "Elektro"),
    ("Kompaan",           "vrijdag",  "Klub C",     "Hiphop"),
    ("Marée Haute",       "vrijdag",  "Bostent",    "Indie"),
    ("Zoutelande Zeven",  "vrijdag",  "Strandbar",  "Hiphop"),
    ("Hofnar",            "vrijdag",  "Strandbar",  "Hiphop"),
    ("Silverhorn",        "zaterdag", "Main Stage", "Rock"),
    ("Lotte & de Wolken", "zaterdag", "Main Stage", "Indie"),
    ("Havsbris",          "zaterdag", "Main Stage", "Elektro"),
    ("Velvet Grid",       "zaterdag", "Klub C",     "Rock"),
    ("Kabelbrand",        "zaterdag", "Klub C",     "Elektro"),
    ("Les Bruyères",      "zaterdag", "Bostent",    "Indie"),
    ("Nordlicht",         "zaterdag", "Bostent",    "Elektro"),
    ("Pier 7",            "zaterdag", "Strandbar",  "Hiphop"),
    ("Dust & Denim",      "zondag",   "Main Stage", "Rock"),
    ("Fjärran",           "zondag",   "Main Stage", "Indie"),
    ("Kaai 12",           "zondag",   "Klub C",     "Hiphop"),
    ("Grauwe Gans",       "zondag",   "Klub C",     "Indie"),
    ("Steenweg",          "zondag",   "Bostent",    "Rock"),
    ("Mistlamp",          "zondag",   "Bostent",    "Elektro"),
    ("Zandloper",         "zondag",   "Strandbar",  "Hiphop"),
    ("Kade Noord",        "zondag",   "Strandbar",  "Indie"),
]
# Welke regels er dubbel in de export staan, en achter welke regel ze komen.
# (index in B5_SCHOON, 0-based) — de export is dus langer dan de echte lijst.
B5_DUBBEL = [2, 9, 18]
B5_VOETNOOT = (
    "Deze export komt uit twee systemen die naast elkaar draaien. Drie acts "
    "staan er daardoor twee keer in. Welke, dat mag je zelf ontdekken."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_SLICER_VELD = "Genre"
B5_SLICER_KEUZE = "Hiphop"
B5_DRAAI_RIJEN = "Podium"
B5_DRAAI_WAARDEN = "Artiest"


# ---------------------------------------------------------------- helpers
def artiestcode(land, jaar):
    """('BE', 2019) -> 'BE2019'. Altijd zes tekens, dat is het punt."""
    return f"{land}{jaar}"


def systeemregel(podium, artiest):
    """('Klub C', 'Kompaan') -> 'Klub C | Kompaan'."""
    return f"{podium}{B2_SCHEIDING}{artiest}"


def boekingscode(dag, podiumcode, volgnummer):
    """('VR', 'MAIN', 7) -> 'ZK26-VR-MAIN-007'. Altijd zestien tekens."""
    return f"{B3_VOORVOEGSEL}-{dag}-{podiumcode}-{volgnummer:03d}"


def nette_naam(achternaam, voornaam):
    """'  VANDENBERGHE ' + ' lotte  ' -> 'Lotte Vandenberghe'."""
    return f"{voornaam.strip().title()} {achternaam.strip().title()}"


def mailadres(achternaam, voornaam):
    """-> 'lotte.vandenberghe@zomerklank.be'.

    Gebouwd op de nette naam, niet op de ruwe velden: elke spatie wordt een
    punt. Een dubbele achternaam geeft dus 'amina.de.smet' — dat is lelijk
    noch fout, het is gewoon wat de regel oplevert.
    """
    return nette_naam(achternaam, voornaam).lower().replace(' ', '.') + '@' + DOMEIN


def export():
    """De line-up zoals ze uit de twee systemen komt: met de dubbels erin."""
    uit = []
    for i, rij in enumerate(B5_SCHOON):
        uit.append(rij)
        if i in B5_DUBBEL:
            uit.append(rij)
    return uit


B5_EXPORT = export()
B5_EIND = B5_START + len(B5_EXPORT) - 1
