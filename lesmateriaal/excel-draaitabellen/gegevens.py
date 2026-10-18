# -*- coding: utf-8 -*-
"""Gegevens voor de draaitabelbundel: Türkiye in cijfers.

Vijf datasets, vijf keer dezelfde techniek op heel ander materiaal. Er staat
in deze bundel GEEN theorie: die staat in draaitabellen-en-grafieken.docx en
de opdracht verwijst er per blad naar.

WAT KLOPT EN WAT NIET — dit staat ook op het startblad en in de opdracht.
  Echt: de namen van de clubs, steden, provincies, gerechten en series, de
        regio waarin een stad of provincie ligt, en de oprichtings- en
        startjaren.
  Verzonnen: ALLE getallen waarmee gerekend wordt — punten, doelpunten,
        toeschouwers, bereidingstijden, porties, afleveringen, kijkcijfers,
        transferbedragen. Ze zijn gekozen om realistisch te lijken en netjes
        uit te komen, niet omdat ze ergens vandaan komen.
  Benaderend: de inwonersaantallen van de provincies zijn afgeronde cijfers
        van rond 2023, op honderdduizendtallen. Goed genoeg om mee te
        rekenen, niet om te citeren.
"""

TITEL = "Excel — Türkiye in draaitabellen"
ONDERTITEL = "Vijf datasets, vijf keer samenvatten zonder één formule"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
DUUR = 50

WAARSCHUWING = (
    "De namen in dit bestand zijn echt: de clubs, de steden, de provincies, de "
    "gerechten en de series bestaan, en de regio waarin ze liggen klopt. ALLE "
    "GETALLEN WAARMEE JE REKENT ZIJN VERZONNEN — punten, toeschouwers, "
    "bereidingstijden, afleveringen, kijkcijfers, bedragen. De inwonersaantallen "
    "zijn afgeronde schattingen van rond 2023. Je oefent dus op echte namen met "
    "verzonnen cijfers. Dat mag, zolang je weet welke van de twee je straks aan "
    "iemand doorvertelt."
)

REGIOS = ["Akdeniz", "Doğu Anadolu", "Ege", "Güneydoğu Anadolu",
          "İç Anadolu", "Karadeniz", "Marmara"]

# ================================================================= blad 1
# Süper Lig. Rijen + Waarden: de eenvoudigste draaitabel die er is.
B1_KOP = ["Club", "Stad", "Regio", "Opgericht", "Punten", "Doelpunten",
          "Toeschouwers"]
B1 = [
    ("Beşiktaş JK",          "İstanbul",  "Marmara",             1903, 62, 58, 32000),
    ("Galatasaray SK",       "İstanbul",  "Marmara",             1905, 78, 71, 41000),
    ("Fenerbahçe SK",        "İstanbul",  "Marmara",             1907, 74, 66, 38000),
    ("MKE Ankaragücü",       "Ankara",    "İç Anadolu",          1910, 31, 34, 14000),
    ("Kasımpaşa SK",         "İstanbul",  "Marmara",             1921, 39, 42, 6000),
    ("Konyaspor",            "Konya",     "İç Anadolu",          1922, 45, 40, 18000),
    ("Göztepe SK",           "İzmir",     "Ege",                 1925, 48, 44, 16000),
    ("Adana Demirspor",      "Adana",     "Akdeniz",             1940, 55, 52, 19000),
    ("Alanyaspor",           "Alanya",    "Akdeniz",             1948, 42, 38, 7000),
    ("Çaykur Rizespor",      "Rize",      "Karadeniz",           1953, 36, 33, 9000),
    ("Bursaspor",            "Bursa",     "Marmara",             1963, 34, 31, 15000),
    ("Samsunspor",           "Samsun",    "Karadeniz",           1965, 47, 45, 21000),
    ("Eskişehirspor",        "Eskişehir", "İç Anadolu",          1965, 29, 27, 11000),
    ("Denizlispor",          "Denizli",   "Ege",                 1966, 27, 25, 8000),
    ("Kayserispor",          "Kayseri",   "İç Anadolu",          1966, 40, 37, 13000),
    ("Antalyaspor",          "Antalya",   "Akdeniz",             1966, 51, 49, 17000),
    ("Trabzonspor",          "Trabzon",   "Karadeniz",           1967, 67, 61, 35000),
    ("Sivasspor",            "Sivas",     "İç Anadolu",          1967, 44, 41, 10000),
    ("Hatayspor",            "Hatay",     "Akdeniz",             1967, 33, 30, 12000),
    ("İstanbul Başakşehir",  "İstanbul",  "Marmara",             1990, 58, 54, 5000),
]
B1_KOPRIJ = 3
B1_START = B1_KOPRIJ + 1
B1_EIND = B1_START + len(B1) - 1
B1_ANKER = f"A{B1_EIND + 3}"          # waar de draaitabel komt, op blad 'Draaitabel 1'

# ================================================================= blad 2
# De keuken. Kruistabel: Rijen én Kolommen.
B2_KOP = ["Gerecht", "Soort", "Regio", "Pittig", "Bereidingstijd", "Porties"]
B2_SOORTEN = ["Drank", "Hoofdgerecht", "Nagerecht", "Voorgerecht"]
B2 = [
    ("Lahmacun",       "Hoofdgerecht", "Güneydoğu Anadolu", "ja",  45, 6),
    ("Adana kebap",    "Hoofdgerecht", "Akdeniz",           "ja",  60, 4),
    ("İskender kebap", "Hoofdgerecht", "Marmara",           "nee", 50, 4),
    ("Mantı",          "Hoofdgerecht", "İç Anadolu",        "nee", 90, 6),
    ("Karadeniz pide", "Hoofdgerecht", "Karadeniz",         "nee", 40, 4),
    ("Hamsi tava",     "Hoofdgerecht", "Karadeniz",         "nee", 25, 4),
    ("İmam bayıldı",   "Hoofdgerecht", "Ege",               "nee", 70, 4),
    ("Testi kebabı",   "Hoofdgerecht", "İç Anadolu",        "ja",  120, 4),
    ("Çiğ köfte",      "Voorgerecht",  "Güneydoğu Anadolu", "ja",  35, 8),
    ("Mercimek çorbası", "Voorgerecht", "İç Anadolu",       "nee", 30, 6),
    ("Cacık",          "Voorgerecht",  "Ege",               "nee", 15, 4),
    ("Su böreği",      "Voorgerecht",  "Marmara",           "nee", 80, 8),
    ("Midye dolma",    "Voorgerecht",  "Marmara",           "ja",  55, 6),
    ("Gözleme",        "Voorgerecht",  "İç Anadolu",        "nee", 45, 4),
    ("Baklava",        "Nagerecht",    "Güneydoğu Anadolu", "nee", 75, 12),
    ("Künefe",         "Nagerecht",    "Akdeniz",           "nee", 35, 4),
    ("Sütlaç",         "Nagerecht",    "Marmara",           "nee", 50, 6),
    ("Lokum",          "Nagerecht",    "Marmara",           "nee", 90, 20),
    ("Kazandibi",      "Nagerecht",    "Marmara",           "nee", 60, 6),
    ("Revani",         "Nagerecht",    "Ege",               "nee", 45, 10),
    ("Çay",            "Drank",        "Karadeniz",         "nee", 10, 6),
    ("Ayran",          "Drank",        "İç Anadolu",        "nee", 5,  4),
    ("Salep",          "Drank",        "Marmara",           "nee", 20, 4),
    ("Şalgam",         "Drank",        "Akdeniz",           "ja",  15, 6),
]
B2_VOETNOOT = (
    "De regio is de streek waar het gerecht het sterkst mee verbonden wordt. "
    "Over sommige gerechten valt daarover te discussiëren — en dat is meteen een "
    "les: een draaitabel is maar zo goed als de kolom waarop je ze bouwt."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1
B2_EIND = B2_START + len(B2) - 1
B2_ANKER = f"A{B2_EIND + 3}"

# ================================================================= blad 3
# De provincies. Som en sorteren.
B3_KOP = ["Provincie", "Regio", "Inwoners", "Oppervlakte (km²)", "Aan zee"]
B3 = [
    ("İstanbul",       "Marmara",            15900000, 5461,  "ja"),
    ("Ankara",         "İç Anadolu",          5800000, 25632, "nee"),
    ("İzmir",          "Ege",                 4500000, 11891, "ja"),
    ("Bursa",          "Marmara",             3200000, 10813, "ja"),
    ("Antalya",        "Akdeniz",             2700000, 20177, "ja"),
    ("Konya",          "İç Anadolu",          2300000, 40814, "nee"),
    ("Adana",          "Akdeniz",             2300000, 13844, "ja"),
    ("Şanlıurfa",      "Güneydoğu Anadolu",   2200000, 19336, "nee"),
    ("Gaziantep",      "Güneydoğu Anadolu",   2200000, 6803,  "nee"),
    ("Kocaeli",        "Marmara",             2100000, 3626,  "ja"),
    ("Mersin",         "Akdeniz",             1900000, 15853, "ja"),
    ("Diyarbakır",     "Güneydoğu Anadolu",   1800000, 15168, "nee"),
    ("Hatay",          "Akdeniz",             1700000, 5524,  "ja"),
    ("Manisa",         "Ege",                 1500000, 13339, "nee"),
    ("Kayseri",        "İç Anadolu",          1400000, 17170, "nee"),
    ("Samsun",         "Karadeniz",           1400000, 9352,  "ja"),
    ("Balıkesir",      "Marmara",             1300000, 14583, "ja"),
    ("Kahramanmaraş",  "Akdeniz",             1200000, 14520, "nee"),
    ("Van",            "Doğu Anadolu",        1100000, 20921, "nee"),
    ("Aydın",          "Ege",                 1100000, 8116,  "ja"),
    ("Denizli",        "Ege",                 1100000, 11868, "nee"),
    ("Trabzon",        "Karadeniz",            800000, 4664,  "ja"),
    ("Malatya",        "Doğu Anadolu",         800000, 12259, "nee"),
    ("Erzurum",        "Doğu Anadolu",         750000, 25006, "nee"),
    ("Sivas",          "İç Anadolu",           640000, 28488, "nee"),
    ("Rize",           "Karadeniz",            340000, 3920,  "ja"),
]
B3_VOETNOOT = (
    "Inwonersaantallen afgerond op honderdduizendtallen, cijfers van rond 2023. "
    "De zesentwintig grootste provincies van de eenentachtig."
)
B3_KOPRIJ = 3
B3_START = B3_KOPRIJ + 1
B3_EIND = B3_START + len(B3) - 1
B3_ANKER = f"A{B3_EIND + 3}"

# ================================================================= blad 4
# De series. Gemiddelde, groeperen per decennium, filter.
B4_KOP = ["Serie", "Genre", "Startjaar", "Seizoenen", "Afleveringen",
          "Kijkers (x1000)"]
B4_GENRES = ["Actie", "Drama", "Historisch", "Misdaad", "Romantiek"]
B4 = [
    ("Kurtlar Vadisi",                 "Actie",      2003, 2,  97,  2800),
    ("Behzat Ç.",                      "Misdaad",    2010, 4,  95,  1600),
    ("Aşk-ı Memnu",                    "Drama",      2008, 2,  79,  3100),
    ("Muhteşem Yüzyıl",                "Historisch", 2011, 4, 139,  3900),
    ("Fatmagül'ün Suçu Ne?",           "Drama",      2010, 2,  80,  3400),
    ("Kara Sevda",                     "Romantiek",  2015, 2,  74,  2900),
    ("Diriliş: Ertuğrul",              "Historisch", 2014, 5, 150,  3800),
    ("Eşkıya Dünyaya Hükümdar Olmaz",  "Actie",      2015, 5, 166,  2400),
    ("Çukur",                          "Misdaad",    2017, 4, 131,  3600),
    ("Söz",                            "Actie",      2017, 3,  93,  1900),
    ("Kadın",                          "Drama",      2017, 2,  81,  2600),
    ("Erkenci Kuş",                    "Romantiek",  2018, 1,  51,  2200),
    ("Bir Zamanlar Çukurova",          "Drama",      2018, 4, 148,  3300),
    ("Hercai",                         "Romantiek",  2019, 3,  67,  2100),
    ("Kuruluş: Osman",                 "Historisch", 2019, 5, 169,  4000),
    ("Sen Çal Kapımı",                 "Romantiek",  2020, 2,  52,  2700),
    ("Masumlar Apartmanı",             "Drama",      2020, 3,  62,  2500),
    ("Sadakatsiz",                     "Drama",      2020, 2,  60,  2300),
    ("Yargı",                          "Misdaad",    2021, 3,  86,  3000),
    ("Teşkilat",                       "Actie",      2021, 4, 115,  2000),
]
B4_VOETNOOT = (
    "Startjaar en genre horen bij de serie; het aantal seizoenen, afleveringen "
    "en kijkers is verzonnen."
)
B4_KOPRIJ = 3
B4_START = B4_KOPRIJ + 1
B4_EIND = B4_START + len(B4) - 1
B4_ANKER = f"A{B4_EIND + 3}"
B4_GROEP_VAN = 2000
B4_GROEP_TOT = 2029
B4_GROEP_PER = 10

# ================================================================= blad 5
# De transfers. EERST aanvullen met VERT.ZOEKEN, DAN de draaitabel.
# De clubcode verwijst naar de clublijst van blad 1.
B5_KOP = ["Speler", "Positie", "Clubcode", "Bedrag (milj. €)",
          "Club", "Stad", "Regio"]
B5_POSITIES = ["Aanvaller", "Doelman", "Middenvelder", "Verdediger"]
# (speler, positie, clubnummer in B1 (1-based), bedrag)
B5 = [
    ("Emre Yıldız",      "Aanvaller",    2, 12.5),
    ("Kaan Demir",       "Middenvelder", 3,  8.0),
    ("Arda Şahin",       "Verdediger",   1,  6.5),
    ("Berk Aydın",       "Doelman",     17,  4.0),
    ("Mert Kaya",        "Aanvaller",   20,  9.5),
    ("Onur Çelik",       "Middenvelder", 2, 11.0),
    ("Yusuf Arslan",     "Verdediger",   8,  5.5),
    ("Deniz Koç",        "Aanvaller",    3, 14.0),
    ("Burak Polat",      "Middenvelder",16,  3.5),
    ("Efe Doğan",        "Doelman",      1,  7.0),
    ("Serkan Aslan",     "Verdediger",  12,  2.5),
    ("Tolga Erdem",      "Aanvaller",   17, 10.0),
    ("Cem Özkan",        "Middenvelder", 6,  4.5),
    ("Hakan Güneş",      "Verdediger",   7,  3.0),
    ("Umut Kılıç",       "Aanvaller",    2, 13.5),
    ("Barış Yalçın",     "Middenvelder",20,  6.0),
    ("Eren Taş",         "Doelman",     18,  2.0),
    ("Can Bulut",        "Verdediger",   3,  7.5),
    ("Selim Acar",       "Aanvaller",    1,  8.5),
    ("Kerem Sönmez",     "Middenvelder",13,  1.5),
    ("Alp Turan",        "Verdediger",  15,  2.5),
    ("Murat Şimşek",     "Aanvaller",   16,  5.0),
]
B5_VOETNOOT = (
    "Verzonnen spelers en verzonnen bedragen. De clubcodes verwijzen naar de "
    "clublijst, die je op dit blad opnieuw ziet staan."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1
B5_EIND = B5_START + len(B5) - 1
B5_ZOEKKOL = 9                       # kolom I: de zoektabel staat ernaast
B5_ZOEKRIJ = B5_KOPRIJ
B5_ANKER = f"A{B5_EIND + 4}"
# De rij die ze er achteraf bij typen, om te leren dat een draaitabel niet
# automatisch meerekent (kaart 9) en dat een bronbereik niet meegroeit.
B5_EXTRA = ("Volkan Arı", "Aanvaller", 17, 9.0)


# ---------------------------------------------------------------- helpers
def clubcode(nummer):
    """1 -> 'C-01'. De code die in de transferlijst staat."""
    return f"C-{nummer:02d}"


def club(nummer):
    """De rij uit de clublijst die bij een clubnummer hoort."""
    if not 1 <= nummer <= len(B1):
        raise IndexError(
            f'clubnummer {nummer} bestaat niet — de clublijst telt {len(B1)} '
            f'clubs, dus de geldige nummers zijn 1 tot {len(B1)}')
    return B1[nummer - 1]


def decennium(jaar):
    """2014 -> '2010 - 2019', zoals Excel een groepering per tien benoemt."""
    van = jaar // 10 * 10
    return f"{van} - {van + 9}"
