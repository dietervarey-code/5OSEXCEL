# -*- coding: utf-8 -*-
"""Gegevens voor de vijf Excel-oefeningen. Eén bron voor het startbestand,
   het stappenplan en de lerarenuitleg, zodat die drie nooit uit elkaar lopen."""

TITEL = "Excel — vijf basisoefeningen"
BEDRIJF = "Bouwcentrale Decock nv"

# ---------------------------------------------------------------- oefening 1
# Voorraadlijst: vermenigvuldigen + SOM. Opmaak: koptekst en valuta.
O1_KOP = ["Artikelcode", "Omschrijving", "Aantal", "Eenheidsprijs", "Waarde"]
O1 = [
    ("SB-190", "Snelbouwsteen 19 cm", 1450, 0.78),
    ("CM-225", "Cement 25 kg", 96, 7.95),
    ("IS-060", "Isolatieplaat 6 cm", 210, 14.30),
    ("WN-500", "Wapeningsnet 5 m", 48, 22.60),
    ("GP-125", "Gipsplaat 12,5 mm", 132, 9.45),
    ("DZ-300", "Dakgoot zink 3 m", 24, 38.90),
    ("VB-040", "Voegmortel 4 kg", 175, 5.20),
    ("SC-100", "Schroeven doos 100", 310, 3.65),
]
O1_START = 4                      # eerste gegevensrij
O1_EIND = O1_START + len(O1) - 1  # laatste gegevensrij
O1_TOTAAL = O1_EIND + 2           # rij met het totaal

# ---------------------------------------------------------------- oefening 2
# Prijslijst: AFRONDEN + absolute celverwijzing. Opmaak: percentage en valuta.
O2_PERCENTAGE = 0.035
O2_KOP = ["Artikel", "Huidige prijs", "Nieuwe prijs", "Verschil"]
O2 = [
    ("Snelbouwsteen 19 cm", 0.78),
    ("Cement 25 kg", 7.95),
    ("Isolatieplaat 6 cm", 14.30),
    ("Wapeningsnet 5 m", 22.60),
    ("Gipsplaat 12,5 mm", 9.45),
    ("Dakgoot zink 3 m", 38.90),
    ("Voegmortel 4 kg", 5.20),
]
O2_START = 6
O2_EIND = O2_START + len(O2) - 1

# ---------------------------------------------------------------- oefening 3
# Verkoopcijfers: SOM per rij, dan MAX, MIN, GEMIDDELDE, AANTAL.
O3_KOP = ["Verkoper", "Januari", "Februari", "Maart", "Kwartaaltotaal"]
O3 = [
    ("An Peeters", 18400, 21150, 19800),
    ("Bram De Smet", 24300, 22700, 26100),
    ("Cindy Vermeulen", 15900, 17250, 16400),
    ("Dirk Lambrecht", 29750, 28100, 31200),
    ("Els Vandamme", 12600, 14300, 13850),
    ("Frank Nauwelaerts", 20100, 19450, 22600),
]
O3_START = 4
O3_EIND = O3_START + len(O3) - 1
O3_SAMENVATTING = O3_EIND + 3     # eerste rij van het samenvattingsblok

# ---------------------------------------------------------------- oefening 4
# Bestellingen: ALS, AANTAL.ALS, SOM.ALS. Opmaak: voorwaardelijke opmaak.
O4_DREMPEL = 500
O4_KOP = ["Bestelnummer", "Klant", "Bedrag", "Levering"]
O4 = [
    ("B-2101", "Bouwbedrijf Maes", 842.50),
    ("B-2102", "Aannemingen Verbeke", 316.00),
    ("B-2103", "Klusbedrijf Six", 1204.75),
    ("B-2104", "Dakwerken Lievens", 489.90),
    ("B-2105", "Installatie Vandaele", 655.20),
    ("B-2106", "Schrijnwerk Dobbels", 272.40),
    ("B-2107", "Tuinaanleg Groen", 938.60),
    ("B-2108", "Bouwbedrijf Maes", 501.00),
    ("B-2109", "Renovatie Top", 187.25),
    ("B-2110", "Aannemingen Verbeke", 1476.80),
]
O4_START = 6
O4_EIND = O4_START + len(O4) - 1
O4_ANTWOORD = O4_EIND + 2         # eerste rij van het vragenblok

# ---------------------------------------------------------------- oefening 5
# Klantenbestand: VERT.ZOEKEN. Opmaak: randen, kolombreedte, beeld vastzetten.
O5_KOP = ["Klantcode", "Naam", "Stad"]
O5_ZOEKKOP = ["Klantcode", "Naam", "Stad"]
O5_TABEL = [
    ("K-101", "Bouwbedrijf Maes", "Kortrijk"),
    ("K-102", "Aannemingen Verbeke", "Roeselare"),
    ("K-103", "Klusbedrijf Six", "Menen"),
    ("K-104", "Dakwerken Lievens", "Izegem"),
    ("K-105", "Installatie Vandaele", "Waregem"),
    ("K-106", "Schrijnwerk Dobbels", "Tielt"),
    ("K-107", "Tuinaanleg Groen", "Ardooie"),
    ("K-108", "Renovatie Top", "Deinze"),
]
# De codes die de leerling moet opzoeken, bewust door elkaar.
O5_VRAAG = ["K-104", "K-101", "K-107", "K-103", "K-108", "K-102", "K-105", "K-106"]
O5_START = 4
O5_EIND = O5_START + len(O5_VRAAG) - 1
O5_TAB_START = 4                                     # zoektabel in kolom G:I
O5_TAB_EIND = O5_TAB_START + len(O5_TABEL) - 1


def zoek(code):
    """De juiste rij uit de zoektabel van oefening 5."""
    for rij in O5_TABEL:
        if rij[0] == code:
            return rij
    raise KeyError(code)
