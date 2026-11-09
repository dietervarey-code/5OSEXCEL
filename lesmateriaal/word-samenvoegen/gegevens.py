# -*- coding: utf-8 -*-
"""Gegevens voor de samenvoegbundel: van een Excellijst naar brieven en etiketten.

Vijf stappen over zes lesuren. De eerste stap is Excel: een lijst zo klaarmaken
dat Word ermee kan werken. De drie stappen daarna zijn Word: etiketten,
brieven, en regels en filters. De vijfde is de eindopdracht, op een lijst die
ze nog niet gezien hebben.

Derde bundel rond Zomerklank. In excel-festival-tekst kuisten ze de line-up
op, in excel-festival-datums rekenden ze met de planning van editie 2026.
Hier bereiden ze editie 2027 voor: de post naar de vrijwilligers en naar de
sponsors.

WAT KLOPT EN WAT NIET
  Zomerklank bestaat niet. De vrijwilligers, de sponsors, de adressen en de
  vergoedingen zijn verzonnen. De straatnamen en gemeenten bestaan wel, maar
  de huisnummers zijn willekeurig — schrijf er dus geen echte brief naartoe.
  De kalender klopt: 16 juli 2027 is een vrijdag.
"""
import datetime

TITEL = "Word en Excel — brieven en etiketten uit één lijst"
ONDERTITEL = "Vijf stappen van een rommelige lijst naar vierentwintig brieven"
FESTIVAL = "Zomerklank"
EDITIE = 2027
DOMEIN = "zomerklank.be"
LESUREN = 6
ZUSTERBUNDELS = ["excel-festival-tekst", "excel-festival-datums"]

FESTIVALDAG = datetime.date(2027, 7, 16)     # vrijdag, de eerste festivaldag
BRIEFDATUM = datetime.date(2026, 11, 20)     # de datum op de brief
START_BLAD = "Start"
PEIL_LABEL = "Eerste festivaldag"
PEILRIJ = 1                  # de peildatum staat op het blad Start,
PEILKOLOM = 2                # op B1, met het label in A1
PEILCEL = f"{START_BLAD}!$B${PEILRIJ}"
# Op de bladen die Word leest staat NIETS boven de koprij. Dat is geen
# schoonheidskwestie: Word neemt de eerste gebruikte rij van het blad als
# kolomnamen. Een titel of een voetnoot erboven maakt de hele
# samenvoeging stuk. Daarom staat de peildatum op een apart blad.
DATUMNOTATIE = 'dd/mm/yyyy'
UURNOTATIE = 'hh:mm'
EURONOTATIE = '€ #,##0.00'

WAARSCHUWING = (
    "Zomerklank bestaat niet en de vrijwilligers en sponsors evenmin. De "
    "straatnamen en gemeenten bestaan wel; de huisnummers zijn willekeurig. "
    "Stuur er dus geen echte brief naartoe, ook niet voor de grap. Wat je hier "
    "leert is wél echt: zo maakt een vereniging, een school of een bedrijf "
    "honderden brieven in één keer, en zo gaat het ook mis als de lijst niet "
    "in orde is."
)

# ======================================================================
#  de takentabel — de zoektabel achter stap 1
# ======================================================================
TAKEN_KOP = ["Taakcode", "Taak", "Podium", "Startuur", "Vergoeding"]
# (code, taak, podium, startuur, dagvergoeding in euro)
TAKEN = [
    ("T01", "Bar",             "Main Stage", datetime.time(14, 0),  45.0),
    ("T02", "Bar",             "Klub C",     datetime.time(18, 30),  45.0),
    ("T03", "Kassa",           "Ingang",     datetime.time(11, 0),   50.0),
    ("T04", "Garderobe",       "Klub C",     datetime.time(19, 0),   40.0),
    ("T05", "Afval",           "Terrein",    datetime.time(9, 30),   40.0),
    ("T06", "Podiumhulp",      "Main Stage", datetime.time(12, 0),   55.0),
    ("T07", "Onthaal artiesten", "Backstage", datetime.time(10, 0),  60.0),
    ("T08", "Camping",         "Camping",    datetime.time(8, 0),    50.0),
]
TAKEN_KOPRIJ = 1
TAKEN_START = TAKEN_KOPRIJ + 1
TAKEN_EIND = TAKEN_START + len(TAKEN) - 1
TAKEN_BLAD = "Taken"

# ======================================================================
#  de vrijwilligers — de samenvoegbron van stap 1 tot 4
# ======================================================================
VRIJ_BLAD = "Vrijwilligers"
VRIJ_KOP = ["Voornaam", "Achternaam", "Straat", "Nummer", "Postcode",
            "Gemeente", "Geboortedatum", "Taakcode",
            "Aanhef", "Adresregel", "Woonplaats",
            "Taak", "Startuur", "Vergoeding", "Leeftijd", "Begeleiding"]
# de eerste acht kolommen staan klaar, de acht daarna maken ze zelf
VRIJ_KLAAR = 8
# (voornaam, achternaam, straat, nummer, postcode, gemeente, geboorte, taakcode)
VRIJWILLIGERS = [
    ("Lotte", "Vandenberghe", "Kerkstraat",      12, 2000, "Antwerpen",
     datetime.date(2007, 3, 14), "T01"),
    ("Jonas", "Peeters",      "Lange Nieuwstraat", 88, 2000, "Antwerpen",
     datetime.date(2010, 11, 2), "T05"),
    ("Amina", "De Smet",      "Stationsstraat",  4,  2800, "Mechelen",
     datetime.date(2009, 7, 16), "T03"),
    ("Youssef", "Willems",    "Bruul",           31, 2800, "Mechelen",
     datetime.date(2008, 1, 30), "T06"),
    ("Elise", "Mertens",      "Dorpsstraat",     7,  2500, "Lier",
     datetime.date(2010, 4, 8), "T04"),
    ("Bilal", "Claes",        "Grote Markt",     19, 2500, "Lier",
     datetime.date(2006, 9, 21), "T02"),
    ("Noor", "Janssens",      "Molenstraat",     45, 2600, "Berchem",
     datetime.date(2009, 7, 17), "T01"),
    ("Sam", "Maes",           "Statielei",       3,  2640, "Mortsel",
     datetime.date(2011, 2, 5), "T05"),
    ("Ayla", "Wouters",       "Vredestraat",     22, 2600, "Berchem",
     datetime.date(2005, 12, 11), "T07"),
    ("Liam", "Goossens",      "Boomgaardstraat", 61, 2018, "Antwerpen",
     datetime.date(2010, 8, 27), "T04"),
    ("Fatima", "De Cock",     "Turnhoutsebaan",  154, 2140, "Borgerhout",
     datetime.date(2004, 5, 3), "T08"),
    ("Thibault", "Hermans",   "Diksmuidelaan",   9,  2600, "Berchem",
     datetime.date(2009, 10, 19), "T06"),
    ("Zeynep", "Lambrechts",  "Lammekensstraat", 27, 2140, "Borgerhout",
     datetime.date(2008, 6, 24), "T03"),
    ("Robbe", "Van Damme",    "Antwerpsesteenweg", 76, 2800, "Mechelen",
     datetime.date(2011, 9, 9), "T05"),
    ("Ilyas", "Segers",       "Sint-Katelijnevest", 15, 2000, "Antwerpen",
     datetime.date(2003, 1, 16), "T07"),
    ("Margot", "Boeckx",      "Kapelstraat",     38, 2500, "Lier",
     datetime.date(2010, 12, 30), "T02"),
    ("Mehdi", "Verhoeven",    "Berchemlei",      104, 2140, "Borgerhout",
     datetime.date(2007, 2, 22), "T08"),
    ("Febe", "Declercq",      "Markgravelei",    57, 2018, "Antwerpen",
     datetime.date(2009, 5, 12), "T01"),
    ("Arne", "Stevens",       "Liersesteenweg",  12, 2640, "Mortsel",
     datetime.date(2006, 11, 25), "T06"),
    ("Yasmine", "Dubois",     "Kroonstraat",     83, 2140, "Borgerhout",
     datetime.date(2010, 3, 3), "T04"),
    ("Wout", "Baeten",        "Vlaamse Kaai",    26, 2000, "Antwerpen",
     datetime.date(2008, 8, 14), "T03"),
    ("Imane", "Bogaerts",     "Herentalsebaan",  210, 2100, "Deurne",
     datetime.date(2011, 1, 7), "T05"),
    ("Senne", "Michiels",     "Gitschotellei",   68, 2140, "Borgerhout",
     datetime.date(2005, 6, 29), "T02"),
    ("Lina", "Smets",         "Boechoutselei",   41, 2640, "Mortsel",
     datetime.date(2009, 9, 18), "T07"),
]
VRIJ_KOPRIJ = 1
VRIJ_START = VRIJ_KOPRIJ + 1
VRIJ_EIND = VRIJ_START + len(VRIJWILLIGERS) - 1
MEERDERJARIG = 18

# ======================================================================
#  de sponsors — de eindopdracht, een lijst die ze nog niet kennen
# ======================================================================
SPON_BLAD = "Sponsors"
SPON_KOP = ["Bedrijf", "Voornaam", "Naam", "Aanspreking", "Straat", "Nummer",
            "Postcode", "Gemeente", "Pakket", "Bedrag",
            "Aanhef", "Adresregel", "Woonplaats", "Bedrag in tekst"]
SPON_KLAAR = 10
SPON_PAKKETTEN = ["Brons", "Goud", "Zilver"]
SPON_AANSPREKINGEN = ["de heer", "mevrouw"]
# (bedrijf, voornaam, naam, aanspreking, straat, nummer, postcode, gemeente,
#  pakket, bedrag)
SPONSORS = [
    ("Bakkerij Van Hoof", "Karel", "Van Hoof", "de heer",
     "Kerkstraat", 3, 2500, "Lier", "Brons", 250.0),
    ("Garage Dierckx", "Nadia", "Dierckx", "mevrouw",
     "Mechelsesteenweg", 142, 2018, "Antwerpen", "Zilver", 750.0),
    ("Drukkerij Lemmens", "Peter", "Lemmens", "de heer",
     "Industrieweg", 7, 2800, "Mechelen", "Goud", 2000.0),
    ("Fietsen Aerts", "Tom", "Aerts", "de heer",
     "Statielei", 54, 2640, "Mortsel", "Brons", 250.0),
    ("Apotheek De Brug", "Sofie", "Maes", "mevrouw",
     "Turnhoutsebaan", 88, 2140, "Borgerhout", "Zilver", 750.0),
    ("Bouwbedrijf Noels", "Ann", "Noels", "mevrouw",
     "Vaartstraat", 21, 2800, "Mechelen", "Goud", 2000.0),
    ("Slagerij Cuyvers", "Dirk", "Cuyvers", "de heer",
     "Dorpsstraat", 16, 2500, "Lier", "Brons", 250.0),
    ("IT-Partner Zuid", "Hanne", "Devos", "mevrouw",
     "Berchemlei", 33, 2140, "Borgerhout", "Zilver", 750.0),
    ("Taxi Centraal", "Mustafa", "Yildiz", "de heer",
     "Statiestraat", 5, 2600, "Berchem", "Brons", 250.0),
    ("Keurslager Pauwels", "Lieve", "Pauwels", "mevrouw",
     "Gitschotellei", 119, 2140, "Borgerhout", "Zilver", 750.0),
    ("Houthandel Verreth", "Jan", "Verreth", "de heer",
     "Boomsesteenweg", 240, 2610, "Wilrijk", "Goud", 2000.0),
    ("Schoonmaak Helder", "Rania", "Haddad", "mevrouw",
     "Herentalsebaan", 76, 2100, "Deurne", "Brons", 250.0),
]
SPON_KOPRIJ = 1
SPON_START = SPON_KOPRIJ + 1
SPON_EIND = SPON_START + len(SPONSORS) - 1
SPON_DREMPEL = 1000.0        # vanaf dit bedrag een extra zin in de brief

# ======================================================================
#  de etiketten van stap 2
# ======================================================================
ETIKET_SOORT = "Avery A4/A5, L7160 — 21 etiketten per blad (63,5 × 38,1 mm)"
ETIKET_PER_BLAD = 21

# ======================================================================
#  het filter van stap 4
# ======================================================================
FILTER_PODIUM = "Main Stage"


# ---------------------------------------------------------------- helpers
def taak(code):
    """De rij uit de takentabel die bij een taakcode hoort."""
    for rij in TAKEN:
        if rij[0] == code:
            return rij
    raise KeyError(f'taakcode {code!r} bestaat niet — geldig zijn '
                   f'{[r[0] for r in TAKEN]}')


def leeftijd_op(geboortedatum, peil):
    """Zoals DATUMVERSCHIL(geboorte;peil;"J"): hele jaren."""
    jaren = peil.year - geboortedatum.year
    if (peil.month, peil.day) < (geboortedatum.month, geboortedatum.day):
        jaren -= 1
    return jaren


def euro(bedrag):
    """1250.0 -> '€ 1.250,00', zoals TEKST(...;"€ #.##0,00") het geeft."""
    heel = f'{bedrag:,.2f}'
    return '€ ' + heel.replace(',', '\x00').replace('.', ',').replace('\x00', '.')


def uur(tijd):
    """time(14, 0) -> '14:00', zoals TEKST(...;"uu:mm") het geeft."""
    return tijd.strftime('%H:%M')


def datum(d):
    return d.strftime('%d/%m/%Y')


MAANDNAMEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli",
              "augustus", "september", "oktober", "november", "december"]


def datum_lang(d):
    """20 november 2026 — zoals het op een brief hoort."""
    return f'{d.day} {MAANDNAMEN[d.month - 1]} {d.year}'
