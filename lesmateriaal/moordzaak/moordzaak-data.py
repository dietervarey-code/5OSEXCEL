# -*- coding: utf-8 -*-
"""De gegevens van de moordzaak. Eén bron voor het startbestand én de sleutel."""

TITEL = "Hotel Astrid — nacht van 14 op 15 maart 2026"

SLACHTOFFER = "Frank Lievens"
KAMER_SLACHTOFFER = 312
DADER = "Greet Coucke"

GASTEN = [
    (207, "Joris Maes",       "14/03/2026", "16/03/2026", "België"),
    (210, "Nadia Top",        "13/03/2026", "15/03/2026", "België"),
    (214, "Peter Loncke",     "14/03/2026", "15/03/2026", "België"),
    (218, "Hilde Cattoor",    "14/03/2026", "16/03/2026", "België"),
    (301, "Marleen Dobbels",  "12/03/2026", "16/03/2026", "België"),
    (304, "Karel Six",        "14/03/2026", "15/03/2026", "Nederland"),
    (308, "Ans Vermeulen",    "14/03/2026", "16/03/2026", "België"),
    (312, "Frank Lievens",    "13/03/2026", "16/03/2026", "België"),
    (315, "Bram De Smet",     "14/03/2026", "15/03/2026", "België"),
    (318, "Elke Vanhoutte",   "14/03/2026", "17/03/2026", "Frankrijk"),
]

# Nr, Naam, Functie, Shift van, Shift tot, Lengte in cm
PERSONEEL = [
    (1, "Ilse Verbeke",      "Nachtreceptionist",  "22:00", "06:00", 165),
    (2, "Tom Vandaele",      "Nachtportier",       "21:00", "05:00", 191),
    (3, "Rachid El Amrani",  "Technische dienst",  "20:00", "04:00", 178),
    (4, "Sofie Groen",       "Kamerdienst",        "06:00", "14:00", 169),
    (5, "Wim Deprez",        "Chef-kok",           "15:00", "23:30", 174),
    (6, "Greet Coucke",      "Hotelmanager",       "08:00", "22:30", 187),
    (7, "Nathalie Six",      "Barverantwoordelijke","18:00", "02:00", 172),
]

# Badge, Houder, Soort
BADGES = [("B-%d" % k, n, "Gast") for k, n, *_ in GASTEN] + [
    ("P-002", "Ilse Verbeke",     "Personeel"),
    ("P-003", "Rachid El Amrani", "Personeel"),
    ("P-004", "Tom Vandaele",     "Personeel"),
    ("P-005", "Wim Deprez",       "Personeel"),
    ("P-006", "Greet Coucke",     "Personeel"),
    ("P-007", "Sofie Groen",      "Personeel"),
    ("P-008", "Nathalie Six",     "Personeel"),
    ("P-001", "Masterbadge (reserve)", "Master"),
]

# (Tijd, Badge, Deur) — bewust door elkaar; sorteren is een opdracht.
LOGBOEK = [
    ("20:02", "P-003", "Personeelsingang"),
    ("20:05", "P-003", "Technische ruimte kelder"),
    ("18:04", "P-008", "Personeelsingang"),
    ("21:03", "P-004", "Personeelsingang"),
    ("19:12", "B-312", "Hoofdingang"),
    ("19:14", "B-312", "Lift verdieping 3"),
    ("19:15", "B-312", "Kamer 312"),
    ("20:41", "B-207", "Hoofdingang"),
    ("20:43", "B-207", "Kamer 207"),
    ("21:10", "B-301", "Hoofdingang"),
    ("21:12", "B-301", "Kamer 301"),
    ("21:26", "B-214", "Hoofdingang"),
    ("21:28", "B-214", "Kamer 214"),
    ("21:44", "P-001", "Personeelsingang"),
    ("21:58", "P-001", "Lift verdieping 2"),
    ("22:03", "P-006", "Receptie achterkamer"),
    ("22:07", "P-002", "Receptie achterkamer"),
    ("22:11", "P-005", "Receptie achterkamer"),
    ("22:02", "P-002", "Personeelsingang"),
    ("22:19", "B-318", "Hoofdingang"),
    ("22:21", "B-318", "Kamer 318"),
    ("22:30", "B-210", "Hoofdingang"),
    ("22:33", "B-210", "Kamer 210"),
    ("22:38", "B-304", "Hoofdingang"),
    ("22:40", "B-304", "Lift verdieping 3"),
    ("22:41", "B-304", "Kamer 304"),
    ("22:52", "P-008", "Bar achterdeur"),
    ("23:04", "B-315", "Hoofdingang"),
    ("23:06", "B-315", "Kamer 315"),
    ("23:18", "P-004", "Lift verdieping 2"),
    ("23:22", "P-004", "Personeelsingang"),
    ("23:27", "B-218", "Hoofdingang"),
    ("23:29", "B-218", "Kamer 218"),
    ("23:33", "P-003", "Technische ruimte kelder"),
    ("23:41", "B-308", "Kamer 308"),
    ("23:39", "B-308", "Lift verdieping 3"),
    ("23:36", "B-308", "Hoofdingang"),
    ("23:52", "P-001", "Lift verdieping 3"),
    ("23:55", "P-001", "Kamer 312"),
    ("23:55", "P-004", "Technische ruimte kelder"),
    ("00:02", "P-004", "Technische ruimte kelder"),
    ("00:04", "P-001", "Lift verdieping 3"),
    ("00:07", "B-315", "Hoofdingang"),
    ("00:09", "B-315", "Kamer 315"),
    ("00:26", "P-008", "Bar achterdeur"),
    ("00:44", "P-003", "Technische ruimte kelder"),
    ("01:15", "B-318", "Kamer 318"),
    ("01:12", "B-318", "Lift verdieping 3"),
    ("01:08", "B-318", "Hoofdingang"),
    ("02:03", "P-008", "Personeelsuitgang"),
    ("02:31", "P-004", "Lift verdieping 2"),
    ("03:10", "P-003", "Technische ruimte kelder"),
    ("04:02", "P-003", "Personeelsuitgang"),
    ("05:04", "P-004", "Personeelsuitgang"),
    ("06:02", "P-007", "Personeelsingang"),
    ("06:38", "P-007", "Lift verdieping 3"),
    ("06:40", "P-007", "Kamer 312"),
    ("21:31", "B-210", "Hoofdingang"),
    ("21:33", "B-210", "Kamer 210"),
    ("22:12", "B-210", "Hoofdingang"),
    ("23:46", "B-304", "Kamer 304"),
    ("23:44", "B-304", "Lift verdieping 3"),
    ("23:43", "B-304", "Hoofdingang"),
]

# (Tijd, Van, Naar, Duur in minuten)
TELEFOON = [
    ("18:22", "Kamer 207", "Receptie", 1),
    ("21:38", "Toestel 100 (directie)", "Kamer 312", 7),
    ("22:47", "Kamer 312", "Buitenlijn 0475 33 21 08", 3),
    ("23:12", "Kamer 207", "Receptie", 1),
    ("23:50", "Kamer 304", "Receptie", 2),
    ("00:10", "Kamer 210", "Receptie", 1),
    ("00:48", "Kamer 318", "Receptie", 1),
    ("06:44", "Kamer 312", "Receptie", 0),
    ("20:15", "Receptie", "Kamer 301", 2),
    ("22:05", "Toestel 100 (directie)", "Buitenlijn 0498 11 76 42", 2),
    ("19:50", "Kamer 214", "Receptie", 3),
]

# (Nr, Voorwerp, Gevonden in, Bijzonderheid)
VOORWERPEN = [
    ("V1", "Donkerblauwe stoffen knoop", "Kamer 312, naast het bed", "Hoort bij een donkerblauwe blazer"),
    ("V2", "Leeg wijnglas", "Kamer 312, op het bureau", "Twee vingerafdrukken, niet van de gast"),
    ("V3", "Zakagenda", "Linnenkast 3e verdieping", "Initialen G.C. op de kaft"),
    ("V4", "Sleutelkaart zonder opdruk", "Kamer 312, onder de kast", "Nummer op de achterkant: P-001"),
    ("V5", "Paraplu", "Lift 3e verdieping", "Eigendom van het hotel"),
    ("V6", "Zakdoek", "Trappenhal 2e verdieping", "Geen bijzonderheden"),
    ("V7", "Bonnetje nachtwinkel", "Kamer 315", "Tijdstip 00:03"),
]

# (Tijd, Wie, Verklaring)
VERKLARINGEN = [
    ("22:20", "Tom Vandaele", "Ik ben de masterbadge kwijt. Ik heb het meteen gemeld aan de receptie."),
    ("23:50", "Karel Six (kamer 304)", "Ik belde de receptie voor een extra deken. Ilse nam onmiddellijk op."),
    ("00:10", "Nadia Top (kamer 210)", "Ik belde de receptie over de verwarming. De receptioniste was er."),
    ("00:14", "Nadia Top (kamer 210)", "Rond middernacht hoorde ik gestommel op de verdieping boven mij."),
    ("00:20", "Bram De Smet (kamer 315)", "Ik was naar de nachtwinkel. Ik heb het bonnetje nog."),
    ("06:40", "Sofie Groen", "De deur van kamer 312 stond op een kier. Toen heb ik de receptie gebeld."),
    ("07:15", "Ilse Verbeke", "Ik heb de balie tussen 22:00 en 00:30 geen moment verlaten."),
    ("07:30", "Wim Deprez", "Ik bleef na mijn shift nog opruimen in de keuken. Ik ben pas 's ochtends buitengegaan."),
    ("08:05", "Nathalie Six", "De bar sloot om 02:00. Daarna heb ik opgeruimd."),
]
