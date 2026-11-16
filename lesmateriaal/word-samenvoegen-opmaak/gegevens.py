# -*- coding: utf-8 -*-
"""Gegevens voor de tweede samenvoegbundel: alles in Word, en opmaak.

De vervolgbundel op word-samenvoegen. Daar lag het gewicht op Excel: de lijst
samenvoegklaar maken met formules. Hier is dat werk al gedaan — de lijsten
staan helemaal klaar, er komt geen enkele formule aan te pas — en gaat elke
minuut naar Word: etiketten, enveloppen, een brief en een lijst, en bij elk
van de vier de opmaak.

Vier soorten samenvoegdocumenten, en Word kan er precies vijf: brieven,
e-mailberichten, enveloppen, etiketten en lijsten. E-mail laten we liggen —
daar valt in een lokaal niets zinnigs mee te doen.

WAT KLOPT EN WAT NIET
  KSV Zonneveld bestaat niet, en de leden, de trainers en de tornooiclubs
  evenmin. De gemeenten bestaan wel, de huisnummers zijn willekeurig. De
  etiket- en envelopformaten zijn echt: die vind je terug in Word.
"""
import datetime

TITEL = "Word — vier soorten samenvoegen, en de opmaak erbij"
ONDERTITEL = "Lidkaarten, enveloppen, een brief en een ploeglijst"
CLUB = "KSV Zonneveld"
CLUB_ADRES = "Sportlaan 12"
CLUB_POSTCODE = 2860
CLUB_GEMEENTE = "Sint-Katelijne-Waver"
CLUB_MAIL = "secretariaat@ksvzonneveld.be"
CLUB_REKENING = "BE68 5390 0754 7034"
LESUREN = 5
VOORGANGER = "word-samenvoegen"
VOORGANGER_THEORIE = "samenvoegen-theorie.docx"

BRIEFDATUM = datetime.date(2026, 11, 27)
DATUMNOTATIE = 'dd/mm/yyyy'
EURONOTATIE = '€ #,##0.00'

WAARSCHUWING = (
    f"{CLUB} bestaat niet, en de leden en de trainers evenmin. De gemeenten "
    "bestaan wel; de huisnummers zijn willekeurig. Stuur er dus geen echte "
    "post naartoe. Wat wél echt is: de etiket- en envelopformaten, het "
    "rekeningnummer is een testnummer, en de manier waarop een club haar post "
    "maakt. Zo gaat het er echt aan toe — en zo ziet het er ook echt uit als "
    "de opmaak niet klopt."
)

# ======================================================================
#  de ploegen — de gegevens zitten plat in de ledenlijst, zoals het hoort
#  voor een samenvoegbron. Hier staan ze één keer, zodat ze overal gelijk
#  zijn en controleer.py ze kan narekenen.
# ======================================================================
PLOEGEN = {
    # ploeg: (trainer, trainingsdag, trainingsuur, lidgeld, vervaldatum)
    'U13':   ('Peter Claes',   'woensdag',  datetime.time(18, 0), 180.0,
              datetime.date(2026, 12, 15)),
    'U15':   ('Fatima Azzouz', 'donderdag', datetime.time(18, 30), 200.0,
              datetime.date(2026, 12, 15)),
    'U17':   ('Bram Wouters',  'dinsdag',   datetime.time(19, 0), 220.0,
              datetime.date(2027, 1, 15)),
    'Dames': ('Hanne Peeters', 'vrijdag',   datetime.time(19, 30), 240.0,
              datetime.date(2027, 1, 15)),
}
PLOEGORDE = ['U13', 'U15', 'U17', 'Dames']

# ======================================================================
#  de ledenlijst — staat volledig klaar, geen enkele formule nodig
# ======================================================================
LEDEN_BLAD = "Leden"
LEDEN_KOP = ["Lidnummer", "Voornaam", "Achternaam", "Adresregel",
             "Woonplaats", "Ploeg", "Geboortejaar", "Trainer",
             "Trainingsdag", "Trainingsuur", "Lidgeld", "Lidgeld in tekst",
             "Betaald", "Vervaldatum", "Vervaldatum in tekst"]
# (voornaam, achternaam, straat, nummer, postcode, gemeente, ploeg,
#  geboortejaar, betaald)
LEDEN_RUW = [
    ("Lotte", "Vandenberghe", "Kerkstraat", 12, 2860, "Sint-Katelijne-Waver",
     "U17", 2010, "ja"),
    ("Jonas", "Peeters", "Lange Zandstraat", 88, 2860,
     "Sint-Katelijne-Waver", "U13", 2014, "nee"),
    ("Amina", "De Smet", "Stationsstraat", 4, 2800, "Mechelen", "U15",
     2012, "ja"),
    ("Youssef", "Willems", "Bruul", 31, 2800, "Mechelen", "U17", 2010, "nee"),
    ("Elise", "Mertens", "Dorpsstraat", 7, 2860, "Sint-Katelijne-Waver",
     "U13", 2014, "ja"),
    ("Bilal", "Claes", "Grote Markt", 19, 2500, "Lier", "Dames", 2007, "ja"),
    ("Noor", "Janssens", "Molenstraat", 45, 2860, "Sint-Katelijne-Waver",
     "U15", 2012, "nee"),
    ("Sam", "Maes", "Statielei", 3, 2640, "Mortsel", "U13", 2015, "ja"),
    ("Ayla", "Wouters", "Vredestraat", 22, 2800, "Mechelen", "Dames",
     2006, "ja"),
    ("Liam", "Goossens", "Boomgaardstraat", 61, 2500, "Lier", "U15",
     2013, "ja"),
    ("Fatima", "De Cock", "Kloosterstraat", 154, 2860,
     "Sint-Katelijne-Waver", "Dames", 2005, "nee"),
    ("Thibault", "Hermans", "Diksmuidelaan", 9, 2600, "Berchem", "U17",
     2011, "ja"),
    ("Zeynep", "Lambrechts", "Lammekensstraat", 27, 2800, "Mechelen", "U15",
     2012, "ja"),
    ("Robbe", "Van Damme", "Antwerpsesteenweg", 76, 2860,
     "Sint-Katelijne-Waver", "U13", 2015, "nee"),
    ("Ilyas", "Segers", "Sint-Jansstraat", 15, 2500, "Lier", "U17",
     2010, "ja"),
    ("Margot", "Boeckx", "Kapelstraat", 38, 2860, "Sint-Katelijne-Waver",
     "Dames", 2007, "ja"),
    ("Mehdi", "Verhoeven", "Puttestraat", 104, 2800, "Mechelen", "U13",
     2014, "ja"),
    ("Febe", "Declercq", "Markgravelei", 57, 2600, "Berchem", "U15",
     2013, "nee"),
    ("Arne", "Stevens", "Liersesteenweg", 12, 2640, "Mortsel", "U17",
     2011, "ja"),
    ("Yasmine", "Dubois", "Kroonstraat", 83, 2800, "Mechelen", "Dames",
     2006, "ja"),
    ("Wout", "Baeten", "Hoogstraat", 26, 2860, "Sint-Katelijne-Waver",
     "U13", 2015, "nee"),
    ("Imane", "Bogaerts", "Veldstraat", 210, 2500, "Lier", "U15", 2012,
     "ja"),
    ("Senne", "Michiels", "Gitschotellei", 68, 2600, "Berchem", "U17",
     2010, "nee"),
    ("Lina", "Smets", "Boechoutselei", 41, 2640, "Mortsel", "Dames", 2005,
     "ja"),
    ("Tuur", "Van Loon", "Beekstraat", 5, 2860, "Sint-Katelijne-Waver",
     "U13", 2014, "ja"),
    ("Nour", "El Amrani", "Nieuwstraat", 71, 2800, "Mechelen", "U15",
     2013, "nee"),
]
LEDEN_KOPRIJ = 1
LEDEN_START = LEDEN_KOPRIJ + 1
LEDEN_EIND = LEDEN_START + len(LEDEN_RUW) - 1

# ======================================================================
#  het tornooi — de lijst voor de eindopdracht, nog niet gezien
# ======================================================================
TORN_BLAD = "Tornooi"
TORN_KOP = ["Club", "Aanspreking", "Voornaam", "Naam", "Adresregel",
            "Woonplaats", "Categorie", "Aantal ploegen",
            "Inschrijvingsgeld", "Inschrijvingsgeld in tekst"]
TORN_AANSPREKINGEN = ["heer", "mevrouw"]
TORN_PER_PLOEG = 40.0          # inschrijvingsgeld per ingeschreven ploeg
# (club, aanspreking, voornaam, naam, straat, nummer, postcode, gemeente,
#  categorie, aantal ploegen)
TORNOOI_RUW = [
    ("KFC Heideveld", "heer", "Karel", "Van Hoof", "Sportstraat", 3,
     2500, "Lier", "U13", 2),
    ("SK Waterhoek", "mevrouw", "Nadia", "Dierckx", "Dijkstraat", 142,
     2800, "Mechelen", "U15", 3),
    ("VV Eikenlo", "heer", "Peter", "Lemmens", "Molenweg", 7,
     2640, "Mortsel", "U17", 1),
    ("KVC Steenberg", "heer", "Tom", "Aerts", "Bergstraat", 54,
     2600, "Berchem", "U13", 3),
    ("FC Lindehof", "mevrouw", "Sofie", "Maes", "Lindelaan", 88,
     2860, "Sint-Katelijne-Waver", "U15", 2),
    ("KSK Molenbeemd", "mevrouw", "Ann", "Noels", "Beemdstraat", 21,
     2800, "Mechelen", "U17", 2),
    ("Sporting Valkenheide", "heer", "Dirk", "Cuyvers", "Valkenlaan", 16,
     2500, "Lier", "U13", 1),
    ("KFC Zandhoven", "mevrouw", "Hanne", "Devos", "Zandstraat", 33,
     2240, "Zandhoven", "U15", 3),
    ("VK Duinbergen", "heer", "Mustafa", "Yildiz", "Duinweg", 5,
     2640, "Mortsel", "U17", 2),
    ("KFC Beverdonk", "mevrouw", "Lieve", "Pauwels", "Donkstraat", 119,
     2860, "Sint-Katelijne-Waver", "U13", 2),
    ("SV Houtvenne", "heer", "Jan", "Verreth", "Venneweg", 240,
     2230, "Herselt", "U15", 1),
    ("KVV Spoorwijk", "mevrouw", "Rania", "Haddad", "Spoorstraat", 76,
     2600, "Berchem", "U17", 3),
    ("FC Kasteelhoeve", "heer", "Bram", "Nijs", "Kasteeldreef", 9,
     2500, "Lier", "U13", 1),
    ("KSV Nieuwmarkt", "mevrouw", "Ilse", "Goossens", "Marktplein", 44,
     2800, "Mechelen", "U15", 2),
]
TORN_KOPRIJ = 1
TORN_START = TORN_KOPRIJ + 1
TORN_EIND = TORN_START + len(TORNOOI_RUW) - 1
TORN_CATEGORIEEN = ["U13", "U15", "U17"]
TORN_EIND_CATEGORIE = "U15"          # de categorie van de eindopdrachtlijst
TORN_GROOT = 3                       # vanaf dit aantal ploegen een extra zin

# ======================================================================
#  de formaten en de opmaak — als gegevens, zodat opdracht, sleutel en
#  controle nooit uit elkaar kunnen lopen
# ======================================================================
ETIKET_SOORT = "Avery A4/A5, L7163 — 14 etiketten per blad (99,1 × 38,1 mm)"
ETIKET_PER_BLAD = 14
# per regel op de lidkaart: de inhoud, welke velden erin zitten, en de opmaak
LIDKAART = [
    dict(inhoud=f'{CLUB.upper()}', velden=[], grootte=8, vet=True,
         cursief=False, kleur='zwart',
         hoe='de clubnaam in HOOFDLETTERS, vaste tekst — dit staat op elke '
             'kaart hetzelfde'),
    dict(inhoud='«Voornaam» «Achternaam»', velden=['Voornaam', 'Achternaam'],
         grootte=14, vet=True, cursief=False, kleur='zwart',
         hoe='de naam, met één spatie tussen de twee velden en geen komma'),
    dict(inhoud='«Ploeg» · «Trainingsdag» «Trainingsuur»',
         velden=['Ploeg', 'Trainingsdag', 'Trainingsuur'], grootte=9,
         vet=False, cursief=True, kleur='zwart',
         hoe='de ploeg, een punt met een spatie ervoor en erna, de dag en '
             'het uur'),
    dict(inhoud='lidnummer «Lidnummer»', velden=['Lidnummer'], grootte=8,
         vet=False, cursief=False, kleur='grijs',
         hoe='het woord lidnummer en dan het veld'),
]
LIDKAART_UITLIJNING = 'gecentreerd'

ENVELOP_FORMAAT = "DL — 110 × 220 mm"
ENVELOP_AFZENDER = [CLUB, CLUB_ADRES, f'{CLUB_POSTCODE} {CLUB_GEMEENTE}']
ENVELOP_AFZENDER_GROOTTE = 8
ENVELOP_GEADRESSEERDE = [['Voornaam', 'Achternaam'], ['Adresregel'],
                         ['Woonplaats']]
ENVELOP_GEADRESSEERDE_GROOTTE = 11
ENVELOP_FILTER = ('Betaald', 'nee')

BRIEF_LEDEN = "samenvoegen-opmaak-brief-leden.docx"
BRIEF_TORNOOI = "samenvoegen-opmaak-brief-tornooi.docx"
BRIEF_MARKERS = ['Voornaam', 'Achternaam', 'Adresregel', 'Woonplaats',
                 'Ploeg', 'Trainer', 'Trainingsdag', 'Trainingsuur']
BRIEF_TABEL = [
    ('Ploeg', 'Ploeg'),
    ('Lidgeld', 'Lidgeld in tekst'),
    ('Te betalen vóór', 'Vervaldatum in tekst'),
    ('Rekeningnummer', None),          # vaste tekst, geen veld
]
BRIEF_TABSTOP_CM = 16.0
BRIEF_REGEL = ('Betaald', 'nee')       # wie niet betaald heeft, krijgt een zin

LIJST_BLAD_PLOEG = "U15"               # de ploeg van de lijstoefening
LIJST_KOLOMMEN = ['Achternaam', 'Voornaam', 'Geboortejaar', 'Trainer']
LIJST_SORTEER = 'Achternaam'


# ---------------------------------------------------------------- helpers
def ploeg(naam):
    if naam not in PLOEGEN:
        raise KeyError(f'ploeg {naam!r} bestaat niet — geldig zijn '
                       f'{PLOEGORDE}')
    return PLOEGEN[naam]


def lidnummer(index):
    """0 -> 'L-1001'. Een code die er als een lidnummer uitziet."""
    return f'L-{1001 + index}'


def euro(bedrag):
    heel = f'{bedrag:,.2f}'
    return '€ ' + heel.replace(',', '\x00').replace('.', ',').replace('\x00', '.')


def uur(tijd):
    return tijd.strftime('%H:%M')


def datum(d):
    return d.strftime('%d/%m/%Y')


MAANDNAMEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli",
              "augustus", "september", "oktober", "november", "december"]


def datum_lang(d):
    return f'{d.day} {MAANDNAMEN[d.month - 1]} {d.year}'
