# -*- coding: utf-8 -*-
"""Gegevens voor de herhalingsbundel: zeven korte oefeningen, 40 minuten.

Dezelfde functies als in de basisbundel, maar vaker en in kleinere brokken.
De nadruk ligt op kilometers maken, niet op nieuwe leerstof.
"""

TITEL = "Excel — herhalingsbundel"
BEDRIJF = "Bouwcentrale Decock nv"
BASISBUNDEL = "excel-functiebladen.docx"   # waar de functiefiches in staan

# ---------------------------------------------------------------- blad 1
# Dagontvangsten: SOM per rij en per kolom.
B1_KOP = ["Dag", "Contant", "Bancontact", "Online", "Dagtotaal"]
B1 = [
    ("maandag", 412.50, 1284.30, 310.00),
    ("dinsdag", 386.20, 1105.75, 288.40),
    ("woensdag", 524.80, 1476.90, 412.60),
    ("donderdag", 398.15, 1198.40, 276.90),
    ("vrijdag", 641.30, 1832.60, 508.25),
    ("zaterdag", 878.45, 2104.20, 623.80),
    ("zondag", 214.60, 486.75, 145.30),
]
B1_START = 4
B1_EIND = B1_START + len(B1) - 1        # 10
B1_TOTAAL = B1_EIND + 2                 # 12

# ---------------------------------------------------------------- blad 2
# Werkuren: SOM, GEMIDDELDE, MAX, MIN, AANTAL.
B2_KOP = ["Medewerker", "Week 1", "Week 2", "Week 3", "Totaal", "Voltijds?"]
B2 = [
    ("An Peeters", 38.5, 36.0, 39.5),
    ("Bram De Smet", 40.0, 40.0, 38.0),
    ("Cindy Vermeulen", 32.5, 34.0, 33.5),
    ("Dirk Lambrecht", 41.5, 42.0, 40.5),
    ("Els Vandamme", 28.0, 30.5, 29.0),
    ("Frank Nauwelaerts", 37.0, 38.5, 36.5),
    ("Greet Ostyn", 39.5, 37.0, 40.0),
    ("Hans Vanacker", 35.5, 36.5, 34.0),
]
B2_VOLTIJDS = 110.0   # vanaf dit totaal noemen we het voltijds
B2_START = 4
B2_EIND = B2_START + len(B2) - 1        # 11
B2_SAMENVATTING = B2_EIND + 2           # 13

# ---------------------------------------------------------------- blad 3
# Kortingen: AFRONDEN met een absolute verwijzing, daarna SOM.
B3_PERCENTAGE = 0.12
B3_KOP = ["Artikel", "Prijs", "Korting", "Nieuwe prijs"]
B3 = [
    ("Handzaag 400 mm", 24.90),
    ("Waterpas 60 cm", 18.75),
    ("Boormachine 750 W", 89.50),
    ("Schroevendraaierset", 32.40),
    ("Ladder 3 m", 146.00),
    ("Verfrol met bak", 12.85),
    ("Kruiwagen 90 l", 67.30),
    ("Hamer 500 g", 15.60),
    ("Steeksleutelset", 41.20),
    ("Werkhandschoenen", 8.95),
]
B3_START = 5
B3_EIND = B3_START + len(B3) - 1        # 14
B3_TOTAAL = B3_EIND + 2                 # 16

# ---------------------------------------------------------------- blad 4
# Verbruik: SOM, GEMIDDELDE, MAX, MIN, AANTAL + voorwaardelijke opmaak.
B4_KOP = ["Maand", "Verbruik (kWh)"]
B4 = [
    ("januari", 1840), ("februari", 1675), ("maart", 1420), ("april", 1180),
    ("mei", 960), ("juni", 845), ("juli", 790), ("augustus", 815),
    ("september", 1025), ("oktober", 1360), ("november", 1590), ("december", 1925),
]
B4_START = 4
B4_EIND = B4_START + len(B4) - 1        # 15
B4_SAMENVATTING = B4_EIND + 2           # 17
B4_DREMPEL = 1500                       # voor de telling met AANTAL.ALS

# ---------------------------------------------------------------- blad 5
# Inschrijvingen: ALS, twee keer AANTAL.ALS, GEMIDDELDE.
B5_GRENS = 18
B5_KOP = ["Naam", "Leeftijd", "Categorie"]
B5 = [
    ("Amira Bakkali", 17), ("Bo Cornelis", 22), ("Cis Demeyer", 15),
    ("Dina El Founti", 19), ("Emir Kaya", 16), ("Fien Goossens", 25),
    ("Gilles Hermans", 18), ("Hanne Iserbyt", 14), ("Ibrahim Jacobs", 31),
    ("Jana Kestens", 17), ("Karel Loos", 20), ("Lotte Maes", 16),
]
B5_START = 5
B5_EIND = B5_START + len(B5) - 1        # 16
B5_ANTWOORD = B5_EIND + 2               # 18

# ---------------------------------------------------------------- blad 6
# Verkoop per afdeling: AANTAL.ALS en SOM.ALS met een criterium uit een cel,
# zodat één formule volstaat en ze kan doorgevoerd worden.
B6_AFDELINGEN = ["Hout", "Sanitair", "Elektro"]
B6_KOP = ["Bonnummer", "Afdeling", "Bedrag"]
B6 = [
    ("K-3001", "Hout", 184.50), ("K-3002", "Elektro", 76.20),
    ("K-3003", "Sanitair", 342.80), ("K-3004", "Hout", 95.40),
    ("K-3005", "Elektro", 218.60), ("K-3006", "Hout", 421.30),
    ("K-3007", "Sanitair", 158.75), ("K-3008", "Elektro", 63.90),
    ("K-3009", "Hout", 276.10), ("K-3010", "Sanitair", 489.25),
    ("K-3011", "Elektro", 134.70), ("K-3012", "Hout", 312.45),
    ("K-3013", "Sanitair", 207.60), ("K-3014", "Elektro", 91.80),
    ("K-3015", "Hout", 168.95),
]
B6_START = 4
B6_EIND = B6_START + len(B6) - 1        # 18
B6_SAMENVATTING = B6_EIND + 2           # 20 — drie rijen, één per afdeling
B6_CONTROLE = B6_SAMENVATTING + len(B6_AFDELINGEN) + 1   # 24

# ---------------------------------------------------------------- blad 7
# Materiaalcodes: twee keer VERT.ZOEKEN, dan AFRONDEN en SOM.
B7_KOP = ["Code", "Omschrijving", "Prijs", "Aantal", "Bedrag"]
B7_ZOEKKOP = ["Code", "Omschrijving", "Prijs"]
B7_TABEL = [
    ("M-01", "Cement 25 kg", 7.95),
    ("M-02", "Zand per zak", 4.60),
    ("M-03", "Isolatieplaat", 14.30),
    ("M-04", "Gipsplaat", 9.45),
    ("M-05", "Tegellijm 20 kg", 13.20),
    ("M-06", "Voegmortel 4 kg", 5.20),
    ("M-07", "Silicone koker", 4.85),
    ("M-08", "Wapeningsnet", 22.60),
]
# Codes en aantallen die de leerling moet opzoeken en doorrekenen.
B7_REGELS = [
    ("M-03", 18), ("M-01", 40), ("M-07", 125), ("M-05", 22),
    ("M-02", 60), ("M-08", 14), ("M-04", 35), ("M-06", 48),
    ("M-01", 25), ("M-03", 12),
]
B7_START = 4
B7_EIND = B7_START + len(B7_REGELS) - 1     # 13
B7_TOTAAL = B7_EIND + 2                     # 15
B7_TAB_START = 4
B7_TAB_EIND = B7_TAB_START + len(B7_TABEL) - 1   # 11


def zoek(code):
    """De juiste rij uit de zoektabel van blad 7."""
    for rij in B7_TABEL:
        if rij[0] == code:
            return rij
    raise KeyError(code)
