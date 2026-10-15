# -*- coding: utf-8 -*-
"""Gegevens voor de streamingbundel: basisfuncties, draaitabel en grafiek.

Tweede bundel rond draaitabellen, met dezelfde opbouw als excel-ottomaans maar
in een andere wereld. Herkenning is het punt: wie de eerste gemaakt heeft,
herkent blad voor blad wat er verwacht wordt.

WAT KLOPT EN WAT NIET
  De titels, de taal en het jaar van verschijnen zijn echt.
  De indeling in genres is onze eigen keuze — veel titels passen in meer dan
  één genre, en dat is in deze oefening juist handig: een draaitabel werkt maar
  zo goed als de kolom waarop je ze bouwt.
  Alle AANTALLEN zijn verzonnen. Er is geen enquête geweest, niet over
  lievelingsgenres, niet over kijkers en niet over schermtijd. Ze zijn gekozen
  om realistisch te lijken en netjes uit te komen.

Er staan nergens vaste rijnummers in de andere scripts: alles wordt hieruit
afgeleid.
"""

TITEL = "Excel — Wat kijkt 5OS?"
ONDERTITEL = "Een streamingaanbod doorrekenen met een draaitabel en een grafiek"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
FUNCTIEBUNDEL = "excel-functiebladen.docx"
EERDERE_BUNDEL = "excel-ottomaans"
DUUR = 50
SCHOOL = 420          # het aantal leerlingen in de verzonnen enquête

WAARSCHUWING = (
    "Let op wat hier echt is en wat niet. De titels, de taal en het jaar van "
    "verschijnen kloppen. De indeling in genres is een keuze die wij gemaakt "
    "hebben — The Queen's Gambit is drama, maar je zou er ook sport van kunnen "
    "maken. ALLE AANTALLEN ZIJN VERZONNEN: er is geen enquête geweest, niet "
    "over lievelingsgenres, niet over kijkers en niet over schermtijd. Je "
    "rekent dus met echte titels en met verzonnen cijfers. Dat mag — zolang je "
    "weet welke van de twee je straks aan iemand doorvertelt."
)

# ---------------------------------------------------------------- blad 1
# De genretabel. Een verzonnen peiling in de school: "wat is je lievelingsgenre?"
# Dit is óók de zoektabel voor blad 2, dus er mag niets aan veranderen.
B1_DREMPEL = 15          # vanaf zoveel erbij noemen we het "groeit sterk"
B1_KOP = ["Code", "Genre", "Stemmen 2024", "Stemmen 2025", "Groei",
          "Groeit sterk?"]
B1 = [
    ("G-01", "Actie",          68,  75),
    ("G-02", "Animatie",       45,  62),
    ("G-03", "Avontuur",       52,  50),
    ("G-04", "Drama",          40,  55),
    ("G-05", "Komedie",        95, 103),
    ("G-06", "Misdaad",        71,  86),
    ("G-07", "Mysterie",       33,  48),
    ("G-08", "Sciencefiction", 58,  66),
    ("G-09", "Thriller",       62,  87),
]
B1_VOETNOOT = (
    f"Verzonnen peiling onder de {SCHOOL} leerlingen van de school: iedereen "
    "mocht één lievelingsgenre aanduiden. Avontuur ging erop achteruit — een "
    "groei kan dus ook negatief zijn."
)
B1_DREMPELTEKST = "Groeit sterk vanaf (stemmen erbij)"
B1_KOPRIJ = 4
B1_START = B1_KOPRIJ + 1                     # 5
B1_EIND = B1_START + len(B1) - 1             # 13
B1_SAMENVATTING = B1_EIND + 2                # 15 — zes regels

# ---------------------------------------------------------------- blad 2
# Het aanbod. Dit is de BRON van allebei de draaitabellen, dus de lijst blijft
# kaarsrecht: één koprij, geen lege rij erin, geen totaalrij eronder. De
# tellingen staan ernaast, met één lege kolom ertussen.
B2_KOP = ["Titel", "Soort", "Genrecode", "Taal", "Jaar", "Kijkers",
          "Genre", "Groei van dat genre", "Groeigenre?"]
B2_SOORTEN = ["Film", "Serie"]
B2_TALEN = ["Duits", "Engels", "Frans", "Japans", "Koreaans", "Nederlands",
            "Noors", "Spaans"]
# (titel, soort, genrecode, taal, jaar, kijkers)
B2 = [
    ("Stranger Things",                 "Serie", "G-08", "Engels",     2016, 285),
    ("Squid Game",                      "Serie", "G-09", "Koreaans",   2021, 310),
    ("La Casa de Papel",                "Serie", "G-06", "Spaans",     2017, 245),
    ("Dark",                            "Serie", "G-08", "Duits",      2017, 155),
    ("Lupin",                           "Serie", "G-06", "Frans",      2021, 135),
    ("The Crown",                       "Serie", "G-04", "Engels",     2016,  60),
    ("Peaky Blinders",                  "Serie", "G-06", "Engels",     2013, 150),
    ("Black Mirror",                    "Serie", "G-08", "Engels",     2011, 120),
    ("Sex Education",                   "Serie", "G-05", "Engels",     2019, 175),
    ("Elite",                           "Serie", "G-04", "Spaans",     2018, 165),
    ("Alice in Borderland",             "Serie", "G-09", "Japans",     2020, 150),
    ("The Queen's Gambit",              "Serie", "G-04", "Engels",     2020,  95),
    ("Wednesday",                       "Serie", "G-07", "Engels",     2022, 260),
    ("Bridgerton",                      "Serie", "G-04", "Engels",     2020, 110),
    ("Undercover",                      "Serie", "G-06", "Nederlands", 2019,  95),
    ("Knokke Off",                      "Serie", "G-04", "Nederlands", 2023, 180),
    ("Chantal",                         "Serie", "G-05", "Nederlands", 2022,  70),
    ("Avatar: De Legende van Aang",     "Serie", "G-02", "Engels",     2005, 140),
    ("Red Notice",                      "Film",  "G-01", "Engels",     2021, 130),
    ("Don't Look Up",                   "Film",  "G-05", "Engels",     2021, 105),
    ("Extraction",                      "Film",  "G-01", "Engels",     2020, 125),
    ("The Adam Project",                "Film",  "G-08", "Engels",     2022,  90),
    ("Enola Holmes",                    "Film",  "G-03", "Engels",     2020, 115),
    ("Glass Onion",                     "Film",  "G-07", "Engels",     2022, 100),
    ("Leave the World Behind",          "Film",  "G-09", "Engels",     2023,  70),
    ("Society of the Snow",             "Film",  "G-04", "Spaans",     2023,  90),
    ("Im Westen nichts Neues",          "Film",  "G-04", "Duits",      2022,  85),
    ("Troll",                           "Film",  "G-03", "Noors",      2022,  60),
    ("Spider-Man: Into the Spider-Verse", "Film", "G-02", "Engels",    2018, 190),
    ("Parasite",                        "Film",  "G-09", "Koreaans",   2019, 180),
    ("Your Name",                       "Film",  "G-02", "Japans",     2016, 120),
    ("Intouchables",                    "Film",  "G-05", "Frans",      2011, 105),
    ("Rebel",                           "Film",  "G-04", "Nederlands", 2022, 115),
    ("The Platform",                    "Film",  "G-09", "Spaans",     2019, 100),
    ("Klaus",                           "Film",  "G-02", "Engels",     2019,  80),
]
B2_VOETNOOT = (
    "Taal = de oorspronkelijke taal, niet de taal waarin jij het gekeken hebt. "
    "Klaus is in Spanje gemaakt maar in het Engels ingesproken, dus die staat "
    "bij Engels."
)
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1                     # 4
B2_EIND = B2_START + len(B2) - 1             # 38
B2_VRAAGKOL = 11                             # kolom K — kolom J blijft leeg
B2_VRAAGRIJ = B2_KOPRIJ
B2_TELSOORT = "Film"
B2_TELTAAL = "Nederlands"

# ---------------------------------------------------------------- blad 3
# De schermtijdenquête. Twintig leerlingen, anoniem. Alles verzonnen.
B3_DREMPEL = 1500        # minuten per week; vanaf hier noemen we het "veel"
B3_KOP = ["Code", "Leeftijd", "Schooldag (min)", "Weekenddag (min)",
          "Per week (min)", "Veel?"]
B3_LEEFTIJD = 17         # voor de SOM.ALS
B3 = [
    ("L-01", 15, 120, 240),
    ("L-02", 16, 180, 300),
    ("L-03", 17,  95, 180),
    ("L-04", 15, 210, 360),
    ("L-05", 18, 150, 240),
    ("L-06", 16, 240, 420),
    ("L-07", 17, 165, 270),
    ("L-08", 15,  75, 150),
    ("L-09", 18, 195, 330),
    ("L-10", 16, 135, 210),
    ("L-11", 17, 225, 390),
    ("L-12", 15, 105, 195),
    ("L-13", 18, 180, 300),
    ("L-14", 16,  60, 120),
    ("L-15", 17, 150, 285),
    ("L-16", 15, 195, 345),
    ("L-17", 18, 120, 210),
    ("L-18", 16, 210, 375),
    ("L-19", 17, 135, 255),
    ("L-20", 18, 165, 300),
]
B3_VOETNOOT = (
    "Verzonnen enquête bij twintig leerlingen. Een schoolweek telt vijf "
    "schooldagen en twee weekenddagen, dus per week = schooldag × 5 + "
    "weekenddag × 2. Schermtijd is alle tijd op een scherm samen: streamen, "
    "sociale media, spelen."
)
B3_DREMPELTEKST = "Veel schermtijd vanaf (min per week)"
B3_KOPRIJ = 4
B3_START = B3_KOPRIJ + 1                     # 5
B3_EIND = B3_START + len(B3) - 1             # 24
B3_VRAAGKOL = 8                              # kolom H — kolom G blijft leeg
B3_VRAAGRIJ = B3_KOPRIJ

# ---------------------------------------------------------------- blad 4
# Allebei de draaitabellen komen van blad 2. Dat is met opzet: één lijst
# beantwoordt heel verschillende vragen, en dat is nu juist het punt.
B4_DRAAI1 = dict(
    bron="2 Aanbod",
    rijen="Genre", kolommen="Soort", waarden="Titel", bewerking="Aantal",
    anker="A14", titel="Draaitabel 1 — aantal titels per genre en per soort",
)
B4_DRAAI2 = dict(
    bron="2 Aanbod",
    rijen="Taal", kolommen=None, waarden="Kijkers", bewerking="Gemiddelde",
    tweede_waarde="Titel", tweede_bewerking="Aantal",
    anker="A30", titel="Draaitabel 2 — kijkers per taal",
)
B4_VRAAGRIJ = 5
B4_VRAAGKOL = 11                             # kolom K — naast de draaitabellen

# ---------------------------------------------------------------- blad 5
# De schermtijd door de jaren. Verzonnen, maar met de vorm die elk echt
# onderzoek laat zien: een sprong in 2020.
B5_KOP = ["Jaar", "Schermtijd per dag (min)", "Verschil met vorig jaar"]
B5 = [
    (2016,  95), (2017, 110), (2018, 125), (2019, 140), (2020, 210),
    (2021, 195), (2022, 170), (2023, 180), (2024, 185), (2025, 190),
]
B5_BRONTEKST = (
    "Verzonnen cijfers, maar met de vorm die elk echt onderzoek naar schermtijd "
    "laat zien: een sprong in het coronajaar 2020 en daarna een daling die niet "
    "helemaal terugkeert naar het oude niveau."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1                     # 4
B5_EIND = B5_START + len(B5) - 1             # 13
B5_VRAAGKOL = 5                              # kolom E — kolom D blijft leeg
B5_VRAAGRIJ = B5_KOPRIJ


# ---------------------------------------------------------------- helpers
def genre(code):
    """De rij uit de genretabel die bij een code hoort."""
    for rij in B1:
        if rij[0] == code:
            return rij
    raise KeyError(
        f'onbekende genrecode {code!r} — ze staat in het aanbod (B2) maar niet '
        f'in de genretabel (B1). Bekend zijn: {", ".join(r[0] for r in B1)}')


def groei(code):
    _, _, oud, nieuw = genre(code)
    return nieuw - oud


def per_week(schooldag, weekenddag):
    return schooldag * 5 + weekenddag * 2
