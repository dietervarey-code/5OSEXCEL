# -*- coding: utf-8 -*-
"""Gegevens voor de grafiekbundel: Türkiye in grafieken.

Vijf datasets, vijf keer een ander grafiektype. Er staat in deze bundel GEEN
theorie: die staat in draaitabellen-en-grafieken.docx, kaart 10 tot 14, en de
opdracht verwijst er per blad naar.

WAT KLOPT EN WAT NIET
  Echt: de namen van de clubs, de steden en de landen, en de volgorde van de
        jaartallen.
  Benaderend: de bevolkingscijfers van Türkiye zijn afgeronde schattingen,
        op honderdduizendtallen.
  Verzonnen: alle andere getallen — toeschouwers, exportaandelen, bezoekers,
        doelpunten. Ze lijken realistisch, maar ze komen nergens vandaan.
"""

TITEL = "Excel — Türkiye in grafieken"
ONDERTITEL = "Vijf datasets, vijf keer het juiste grafiektype kiezen"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
ZUSTERBUNDEL = "excel-draaitabellen"
DUUR = 50

WAARSCHUWING = (
    "De namen in dit bestand zijn echt: de clubs, de steden en de landen "
    "bestaan. De bevolkingscijfers van Türkiye zijn afgeronde schattingen. "
    "ALLE ANDERE GETALLEN ZIJN VERZONNEN — toeschouwers, exportaandelen, "
    "bezoekersaantallen, doelpunten. Je oefent dus op echte namen met "
    "verzonnen cijfers. Een grafiek maakt een getal overtuigend; let erop dat "
    "je niet overtuigend wordt over iets dat niet klopt."
)

REGIOS = ["Akdeniz", "Ege", "İç Anadolu", "Karadeniz", "Marmara"]

# ================================================================= blad 1
# Toeschouwers per club. Staafdiagram: vergelijken.
B1_KOP = ["Club", "Stad", "Toeschouwers"]
B1 = [
    ("Galatasaray SK",      "İstanbul", 41000),
    ("Fenerbahçe SK",       "İstanbul", 38000),
    ("Trabzonspor",         "Trabzon",  35000),
    ("Beşiktaş JK",         "İstanbul", 32000),
    ("Samsunspor",          "Samsun",   21000),
    ("Adana Demirspor",     "Adana",    19000),
    ("Konyaspor",           "Konya",    18000),
    ("Antalyaspor",         "Antalya",  17000),
    ("Göztepe SK",          "İzmir",    16000),
    ("Bursaspor",           "Bursa",    15000),
]
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1
B1_SOORT = "staafdiagram"
B1_TITEL = "Gemiddeld aantal toeschouwers per club"

# ================================================================= blad 2
# De bevolking van Türkiye. Lijndiagram: verloop in de tijd.
B2_KOP = ["Jaar", "Inwoners (miljoen)", "Groei sinds de vorige meting"]
B2 = [
    (1950, 21.0), (1960, 28.0), (1970, 35.6), (1980, 44.7), (1990, 56.5),
    (2000, 67.8), (2010, 73.7), (2020, 83.6), (2025, 85.7),
]
B2_VOETNOOT = (
    "Afgeronde schattingen. De metingen liggen niet even ver uit elkaar: tussen "
    "de laatste twee zit maar vijf jaar, tussen de andere tien."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1
B2_SOORT = "lijndiagram"
B2_TITEL = "De bevolking van Türkiye"

# ================================================================= blad 3
# Export per productgroep. Cirkeldiagram: aandeel van een geheel.
B3_KOP = ["Productgroep", "Waarde (miljard €)", "Aandeel"]
B3 = [
    ("Auto's en onderdelen", 36),
    ("Textiel en kleding",   30),
    ("Machines",             24),
    ("Chemie",               18),
    ("Landbouw en voeding",  12),
]
B3_VOETNOOT = (
    "Verzonnen cijfers, vijf groepen die samen de hele export vormen. Juist "
    "omdat de delen samen een geheel zijn, mag hier een cirkeldiagram."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1
B3_SOORT = "cirkeldiagram"
B3_TITEL = "Aandeel in de export"

# ================================================================= blad 4
# Toeristen uit drie landen. Twee of meer reeksen in één grafiek.
B4_KOP = ["Jaar", "Duitsland", "Rusland", "Nederland"]
B4 = [
    (2019, 5.0, 7.0, 1.2),
    (2020, 1.1, 2.1, 0.3),
    (2021, 3.1, 4.7, 0.6),
    (2022, 5.6, 5.2, 1.1),
    (2023, 6.2, 6.3, 1.4),
    (2024, 6.6, 6.7, 1.5),
]
B4_VOETNOOT = (
    "Verzonnen bezoekersaantallen in miljoenen. De inzinking van 2020 zit er "
    "wel in, want die is er in het echt ook geweest."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1
B4_SOORT = "lijndiagram met drie reeksen"
B4_TITEL = "Bezoekers per herkomstland"
B4_LANDEN = ["Duitsland", "Rusland", "Nederland"]

# ================================================================= blad 5
# Topscorers. EERST aanvullen met VERT.ZOEKEN, DAN een grafiek.
B5_KOP = ["Speler", "Clubcode", "Doelpunten", "Club", "Stad"]
# (speler, clubnummer in B1 (1-based), doelpunten)
B5 = [
    ("Emre Yıldız",   1, 24),
    ("Kaan Demir",    2, 21),
    ("Arda Şahin",    4, 18),
    ("Berk Aydın",    3, 17),
    ("Mert Kaya",     1, 15),
    ("Onur Çelik",    7, 14),
    ("Yusuf Arslan",  2, 13),
    ("Deniz Koç",     6, 12),
    ("Burak Polat",   5, 11),
    ("Efe Doğan",     8, 10),
    ("Serkan Aslan",  9,  9),
    ("Tolga Erdem",  10,  8),
]
B5_VOETNOOT = (
    "Verzonnen spelers en verzonnen doelpunten. De clubcodes verwijzen naar de "
    "clubtabel die ernaast staat."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_EIND = B5_START + len(B5) - 1
B5_ZOEKKOL = 7                       # kolom G: de clubtabel staat ernaast
B5_ZOEKRIJ = B5_KOPRIJ
B5_SOORT = "staafdiagram"
B5_TITEL = "Doelpunten per speler"


# ---------------------------------------------------------------- helpers
def clubcode(nummer):
    return f"C-{nummer:02d}"


def club(nummer):
    if not 1 <= nummer <= len(B1):
        raise IndexError(
            f'clubnummer {nummer} bestaat niet — de clubtabel telt {len(B1)} '
            f'clubs, dus de geldige nummers zijn 1 tot {len(B1)}')
    return B1[nummer - 1]
