# -*- coding: utf-8 -*-
"""Gegevens voor de tweede herhalingsbundel: zeven korte oefeningen, 40 minuten.

Zelfde opbouw als de eerste herhalingsbundel, zelfde tien functies, andere
wereld en andere cijfers. Wie de eerste bundel deed, herkent de volgorde —
dat is de bedoeling: wie het nog niet vast heeft, oefent het nog eens.
"""

TITEL = "Excel — herhalingsbundel 2"
BEDRIJF = "Tuincentrum Het Groenhof"
BASISBUNDEL = "excel-functiebladen.docx"   # waar de functiefiches in staan

# ---------------------------------------------------------------- blad 1
# Weekomzet: SOM per rij en per kolom.
B1_KOP = ["Dag", "Planten", "Tuinmeubels", "Gereedschap", "Dagtotaal"]
B1 = [
    ("maandag", 1842.60, 486.20, 312.75),
    ("dinsdag", 1654.30, 398.50, 287.40),
    ("woensdag", 2310.85, 712.90, 445.60),
    ("donderdag", 1976.40, 524.75, 368.20),
    ("vrijdag", 2845.70, 968.30, 591.85),
    ("zaterdag", 4126.95, 1584.60, 823.40),
    ("zondag", 1238.50, 342.15, 176.90),
]
B1_START = 4
B1_EIND = B1_START + len(B1) - 1        # 10
B1_TOTAAL = B1_EIND + 2                 # 12

# ---------------------------------------------------------------- blad 2
# Kwekers: SOM, GEMIDDELDE, MAX, MIN, AANTAL, ALS en AANTAL.ALS.
B2_KOP = ["Kweker", "April", "Mei", "Juni", "Totaal", "Grote kweker?"]
B2 = [
    ("Kwekerij Verhaeghe", 420, 515, 480),
    ("De Groene Hof", 395, 410, 395),
    ("Plantencentrum Bral", 610, 725, 690),
    ("Boomkwekerij Timmers", 295, 340, 310),
    ("Serres Delanghe", 505, 560, 535),
    ("Kwekerij Van Hoof", 348, 392, 371),
    ("Tuinplant Decoster", 470, 445, 498),
    ("Vaste Planten Mertens", 262, 288, 275),
]
B2_GROOT = 1200       # vanaf dit totaal noemen we het een grote kweker
B2_START = 4
B2_EIND = B2_START + len(B2) - 1        # 11
B2_SAMENVATTING = B2_EIND + 2           # 13

# ---------------------------------------------------------------- blad 3
# Prijsverhoging: AFRONDEN met een absolute verwijzing, daarna SOM.
# Vorige keer ging een percentage eraf, nu komt het erbij.
B3_PERCENTAGE = 0.07
B3_KOP = ["Artikel", "Oude prijs", "Verhoging", "Nieuwe prijs"]
B3 = [
    ("Potgrond 40 l", 7.95),
    ("Gieter 10 l", 12.40),
    ("Snoeischaar", 24.75),
    ("Tuinslang 25 m", 38.90),
    ("Bloempot terracotta 30 cm", 16.20),
    ("Graszaad 5 kg", 29.50),
    ("Tuinhandschoenen", 6.85),
    ("Plantenvoeding 1 l", 9.30),
    ("Harkbezem", 18.60),
    ("Kweekkas 120 cm", 74.95),
]
B3_START = 5
B3_EIND = B3_START + len(B3) - 1        # 14
B3_TOTAAL = B3_EIND + 2                 # 16

# ---------------------------------------------------------------- blad 4
# Bezoekers: SOM, GEMIDDELDE, MAX, MIN, AANTAL, AANTAL.ALS + voorwaardelijke opmaak.
B4_KOP = ["Maand", "Bezoekers"]
B4 = [
    ("januari", 1850), ("februari", 2140), ("maart", 3960), ("april", 6420),
    ("mei", 7180), ("juni", 5240), ("juli", 3870), ("augustus", 3510),
    ("september", 4680), ("oktober", 4120), ("november", 2890), ("december", 3340),
]
B4_START = 4
B4_EIND = B4_START + len(B4) - 1        # 15
B4_SAMENVATTING = B4_EIND + 2           # 17
B4_DREMPEL = 5000                       # voor de telling met AANTAL.ALS

# ---------------------------------------------------------------- blad 5
# Snoeicursus: ALS, twee keer AANTAL.ALS, GEMIDDELDE.
B5_GRENS = 50
B5_KOP = ["Cursist", "Punten", "Resultaat"]
B5 = [
    ("Arno Buelens", 62), ("Britt Coene", 47), ("Cédric Dhaene", 50),
    ("Delphine Engels", 71), ("Elias Feys", 38), ("Fatima Gharbi", 55),
    ("Gust Hollevoet", 44), ("Hilde Ivens", 68), ("Imke Jonckheere", 49),
    ("Jens Kinoo", 58), ("Kato Lievens", 33), ("Lander Maes", 76),
]
B5_START = 5
B5_EIND = B5_START + len(B5) - 1        # 16
B5_ANTWOORD = B5_EIND + 2               # 18

# ---------------------------------------------------------------- blad 6
# Bestellingen per leverancier: AANTAL.ALS en SOM.ALS met een criterium uit
# een cel, zodat één formule volstaat en ze doorgevoerd kan worden.
B6_LEVERANCIERS = ["Floralux", "Terra Nova", "Groenwerk"]
B6_KOP = ["Bonnummer", "Leverancier", "Bedrag"]
B6 = [
    ("B-5001", "Floralux", 284.60), ("B-5002", "Groenwerk", 128.40),
    ("B-5003", "Terra Nova", 512.75), ("B-5004", "Floralux", 196.30),
    ("B-5005", "Groenwerk", 347.80), ("B-5006", "Floralux", 623.50),
    ("B-5007", "Terra Nova", 254.90), ("B-5008", "Groenwerk", 87.60),
    ("B-5009", "Floralux", 418.25), ("B-5010", "Terra Nova", 735.40),
    ("B-5011", "Groenwerk", 162.95), ("B-5012", "Floralux", 389.70),
    ("B-5013", "Terra Nova", 298.15), ("B-5014", "Groenwerk", 143.20),
    ("B-5015", "Floralux", 507.85),
]
B6_START = 4
B6_EIND = B6_START + len(B6) - 1        # 18
B6_SAMENVATTING = B6_EIND + 2           # 20 — drie rijen, één per leverancier
B6_CONTROLE = B6_SAMENVATTING + len(B6_LEVERANCIERS) + 1   # 24

# ---------------------------------------------------------------- blad 7
# Zaadcodes: twee keer VERT.ZOEKEN, dan AFRONDEN, SOM en SOM.ALS.
B7_KOP = ["Code", "Omschrijving", "Prijs", "Aantal", "Bedrag"]
B7_ZOEKKOP = ["Code", "Omschrijving", "Prijs"]
B7_TABEL = [
    ("Z-01", "Graszaad 5 kg", 29.50),
    ("Z-02", "Bloemenmengsel 1 kg", 11.80),
    ("Z-03", "Wortelzaad zakje", 2.35),
    ("Z-04", "Slazaad zakje", 1.95),
    ("Z-05", "Tomatenzaad zakje", 3.40),
    ("Z-06", "Groenbemester 2 kg", 14.60),
    ("Z-07", "Kruidenmix zakje", 4.25),
    ("Z-08", "Bonenzaad 500 g", 8.70),
]
B7_DEELTOTAAL = "Z-02"       # komt meer dan één keer voor
B7_REGELS = [
    ("Z-03", 85), ("Z-02", 30), ("Z-06", 18), ("Z-01", 24),
    ("Z-04", 120), ("Z-08", 42), ("Z-02", 45), ("Z-05", 96),
    ("Z-07", 64), ("Z-03", 50),
]
B7_START = 4
B7_EIND = B7_START + len(B7_REGELS) - 1          # 13
B7_TOTAAL = B7_EIND + 2                          # 15
B7_DEEL = B7_TOTAAL + 2                          # 17
B7_TAB_START = 4
B7_TAB_EIND = B7_TAB_START + len(B7_TABEL) - 1   # 11


def zoek(code):
    """De juiste rij uit de zoektabel van blad 7."""
    for rij in B7_TABEL:
        if rij[0] == code:
            return rij
    raise KeyError(code)
