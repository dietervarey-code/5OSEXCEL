# -*- coding: utf-8 -*-
"""Gegevens voor de Ottomaanse bundel: basisfuncties, dan draaitabel en grafiek.

De jaartallen van de regeerperiodes, de gebeurtenissen en de oorlogen zijn
historische gegevens. De bevolkingscijfers zijn ruwe schattingen — historici
verschillen daarover sterk. Dat staat ook op het startblad, in de opdracht en
in de sleutel, zodat niemand ze als vaststaande feiten leert.

Er staan nergens vaste rijnummers in de andere scripts: alles wordt hieruit
afgeleid, dus een regel toevoegen schuift de rest vanzelf mee.
"""

TITEL = "Excel — Het Ottomaanse Rijk"
ONDERTITEL = "Basisfuncties, een draaitabel en een grafiek"
THEORIEBUNDEL = "draaitabellen-en-grafieken.docx"
FUNCTIEBUNDEL = "excel-functiebladen.docx"
DUUR = 50

WAARSCHUWING = (
    "Let op: de bevolkingscijfers op blad 5 zijn RUWE SCHATTINGEN. Van het "
    "Ottomaanse Rijk bestaan geen betrouwbare volkstellingen voor 1831, en "
    "historici komen op heel verschillende getallen uit. Ze staan hier om mee "
    "te rekenen en om een grafiek van te maken, niet om uit het hoofd te leren. "
    "De jaartallen van de sultans, de gebeurtenissen en de oorlogen zijn wel "
    "gewone historische gegevens."
)

# ---------------------------------------------------------------- blad 1
# De sultans. Zoektabel voor blad 2 EN rekenwerk op zichzelf.
# Elke regeerperiode is de regeerperiode van die sultan; wie twee keer
# geregeerd heeft, staat hier met zijn langste periode (zie VOETNOOT).
B1_DREMPEL = 25          # vanaf zoveel regeringsjaren noemen we het "lang"
B1_KOP = ["Code", "Sultan", "Eerste jaar", "Laatste jaar",
          "Regeringsjaren", "Lang geregeerd?"]
B1 = [
    ("S-01", "Osman I",       1299, 1324),
    ("S-02", "Orhan",         1324, 1362),
    ("S-03", "Murad I",       1362, 1389),
    ("S-04", "Bayezid I",     1389, 1402),
    ("S-05", "Mehmed II",     1451, 1481),
    ("S-06", "Selim I",       1512, 1520),
    ("S-07", "Süleyman I",    1520, 1566),
    ("S-08", "Mehmed IV",     1648, 1687),
    ("S-09", "Mustafa II",    1695, 1703),
    ("S-10", "Ahmed III",     1703, 1730),
    ("S-11", "Mahmud II",     1808, 1839),
    ("S-12", "Abdülhamid II", 1876, 1909),
    ("S-13", "Mehmed VI",     1918, 1922),
]
B1_VOETNOOT = (
    "Mehmed II heeft twee keer geregeerd: eerst als kind van 1444 tot 1446, "
    "daarna van 1451 tot 1481. Hier staat zijn tweede, lange periode. "
    "Niet elke sultan staat in deze lijst — het zijn er dertien van de zesendertig."
)
B1_DREMPELTEKST = "Lang geregeerd vanaf (jaren)"
B1_KOPRIJ = 4
B1_START = B1_KOPRIJ + 1                     # 5
B1_EIND = B1_START + len(B1) - 1             # 17
B1_SAMENVATTING = B1_EIND + 2                # 19 — zes regels

# ---------------------------------------------------------------- blad 2
# De gebeurtenissenlijst. Dit is straks de BRON van draaitabel 1, dus de
# lijst moet kaarsrecht blijven: één koprij, geen lege rij erin, geen
# totaalrij eronder. Daarom staat de samenvatting ERNAAST, met één lege
# kolom ertussen.
B2_KOP = ["Jaar", "Gebeurtenis", "Soort", "Regio", "Eeuw", "Sultancode",
          "Sultan", "Regeringsjaren", "Tijdens een lange regering?"]
B2_SOORTEN = ["Bestuur", "Beleg", "Opstand", "Veldslag", "Verovering",
              "Vredesverdrag"]
B2_REGIOS = ["Anatolië", "Balkan", "Middellandse Zee", "Midden-Europa",
             "Midden-Oosten", "Noord-Afrika", "Zwarte Zee"]
B2 = [
    (1299, "Osman sticht zijn eigen vorstendom", "Bestuur", "Anatolië", "S-01"),
    (1326, "Inname van Bursa", "Verovering", "Anatolië", "S-02"),
    (1354, "Oversteek naar Europa bij Gallipoli", "Verovering", "Balkan", "S-02"),
    (1365, "Edirne wordt hoofdstad", "Bestuur", "Balkan", "S-03"),
    (1389, "Slag op het Merelveld", "Veldslag", "Balkan", "S-03"),
    (1396, "Slag bij Nicopolis", "Veldslag", "Balkan", "S-04"),
    (1402, "Slag bij Ankara", "Veldslag", "Anatolië", "S-04"),
    (1453, "Val van Constantinopel", "Beleg", "Balkan", "S-05"),
    (1459, "Inlijving van Servië", "Verovering", "Balkan", "S-05"),
    (1475, "De Krim wordt vazalstaat", "Verovering", "Zwarte Zee", "S-05"),
    (1480, "Mislukt beleg van Rhodos", "Beleg", "Middellandse Zee", "S-05"),
    (1514, "Slag bij Çaldiran", "Veldslag", "Midden-Oosten", "S-06"),
    (1517, "Verovering van Egypte", "Verovering", "Noord-Afrika", "S-06"),
    (1521, "Verovering van Belgrado", "Verovering", "Balkan", "S-07"),
    (1522, "Beleg van Rhodos", "Beleg", "Middellandse Zee", "S-07"),
    (1526, "Slag bij Mohács", "Veldslag", "Midden-Europa", "S-07"),
    (1529, "Eerste beleg van Wenen", "Beleg", "Midden-Europa", "S-07"),
    (1534, "Verovering van Bagdad", "Verovering", "Midden-Oosten", "S-07"),
    (1551, "Verovering van Tripoli", "Verovering", "Noord-Afrika", "S-07"),
    (1555, "Vrede van Amasya", "Vredesverdrag", "Midden-Oosten", "S-07"),
    (1669, "Verovering van Kreta", "Beleg", "Middellandse Zee", "S-08"),
    (1676, "Vrede van Zuravno", "Vredesverdrag", "Zwarte Zee", "S-08"),
    (1683, "Tweede beleg van Wenen", "Beleg", "Midden-Europa", "S-08"),
    (1699, "Vrede van Karlowitz", "Vredesverdrag", "Balkan", "S-09"),
    (1718, "Vrede van Passarowitz", "Vredesverdrag", "Balkan", "S-10"),
    (1727, "Eerste drukkerij in Istanbul", "Bestuur", "Anatolië", "S-10"),
    (1730, "Opstand van Patrona Halil", "Opstand", "Anatolië", "S-10"),
    (1821, "Begin van de Griekse opstand", "Opstand", "Balkan", "S-11"),
    (1826, "Afschaffing van de janitsaren", "Bestuur", "Anatolië", "S-11"),
    (1831, "Eerste volkstelling van het rijk", "Bestuur", "Anatolië", "S-11"),
    (1876, "Eerste grondwet", "Bestuur", "Anatolië", "S-12"),
    (1878, "Congres van Berlijn", "Vredesverdrag", "Balkan", "S-12"),
    (1908, "Jong-Turkse revolutie", "Opstand", "Balkan", "S-12"),
    (1920, "Verdrag van Sèvres", "Vredesverdrag", "Anatolië", "S-13"),
    (1922, "Einde van het sultanaat", "Bestuur", "Anatolië", "S-13"),
]
B2_KOPRIJ = 3
B2_START = B2_KOPRIJ + 1                     # 4
B2_EIND = B2_START + len(B2) - 1             # 38
B2_VRAAGKOL = 11                             # kolom K — kolom J blijft leeg
B2_VRAAGRIJ = B2_KOPRIJ                      # vragenblokje begint op de koprij
B2_TELREGIO = "Balkan"
B2_TELSOORT = "Vredesverdrag"   # bewust NIET de drukste soort: die moet blad 4 opleveren
B2_TELEEUW = "19e eeuw"        # bewust NIET de drukste eeuw: die moet blad 4 opleveren

# ---------------------------------------------------------------- blad 3
# De oorlogen. Bron van draaitabel 2 en van het staafdiagram. Zelfde regel:
# samenvatting ERNAAST, met een lege kolom ertussen.
B3_DREMPEL = 10          # vanaf zoveel jaar noemen we een oorlog "lang"
B3_KOP = ["Oorlog", "Tegenstander", "Begin", "Einde", "Duur (jaren)",
          "Uitkomst", "Lange oorlog?"]
B3_UITKOMSTEN = ["winst", "verlies", "status quo"]
B3 = [
    ("Ottomaans-Venetiaanse oorlog", "Venetië", 1463, 1479, "winst"),
    ("Ottomaans-Mamelukse oorlog", "Mamelukken", 1516, 1517, "winst"),
    ("Ottomaans-Habsburgse oorlog", "Habsburgers", 1526, 1568, "winst"),
    ("Ottomaans-Safawidische oorlog", "Safawiden", 1532, 1555, "winst"),
    ("Cyprusoorlog", "Venetië", 1570, 1573, "winst"),
    ("Lange Turkse Oorlog", "Habsburgers", 1593, 1606, "status quo"),
    ("Kretenzische Oorlog", "Venetië", 1645, 1669, "winst"),
    ("Grote Turkse Oorlog", "Heilige Liga", 1683, 1699, "verlies"),
    ("Oorlog om de Morea", "Venetië", 1714, 1718, "winst"),
    ("Russisch-Turkse oorlog", "Rusland", 1768, 1774, "verlies"),
    ("Russisch-Turkse oorlog", "Rusland", 1787, 1792, "verlies"),
    ("Griekse Onafhankelijkheidsoorlog", "Griekenland", 1821, 1829, "verlies"),
    ("Russisch-Turkse oorlog", "Rusland", 1828, 1829, "verlies"),
    ("Krimoorlog", "Rusland", 1853, 1856, "winst"),
    ("Russisch-Turkse oorlog", "Rusland", 1877, 1878, "verlies"),
    ("Eerste Balkanoorlog", "Balkanstaten", 1912, 1913, "verlies"),
    ("Tweede Balkanoorlog", "Balkanstaten", 1913, 1913, "winst"),
    ("Eerste Wereldoorlog", "Geallieerden", 1914, 1918, "verlies"),
]
B3_VOETNOOT = (
    "De uitkomst staat er vanuit Ottomaans oogpunt: winst, verlies of status quo. "
    "Grote oorlogen zijn zelden zo zwart-wit — de Oorlog om de Morea leverde "
    "Griekse gebieden op maar kostte Belgrado. Voor deze oefening volstaat één woord."
)
B3_DREMPELTEKST = "Lange oorlog vanaf (jaren)"
B3_KOPRIJ = 4
B3_START = B3_KOPRIJ + 1                     # 5
B3_EIND = B3_START + len(B3) - 1             # 22
B3_VRAAGKOL = 9                              # kolom I — kolom H blijft leeg
B3_VRAAGRIJ = B3_KOPRIJ
B3_SOMLAND = "Rusland"
B3_SOMUITKOMST = "verlies"
B3_TELUITKOMST = "winst"

# ---------------------------------------------------------------- blad 4
# De draaitabellen. Hier staat niets dat de leerling moet berekenen met een
# functie: hier wordt gesleept. De vragen eronder lezen ze AF van hun tabel.
B4_DRAAI1 = dict(
    bron="2 Gebeurtenissen",
    rijen="Soort", kolommen="Eeuw", waarden="Gebeurtenis", bewerking="Aantal",
    anker="A14", titel="Draaitabel 1 — soort gebeurtenis per eeuw",
)
B4_DRAAI2 = dict(
    bron="3 Oorlogen",
    rijen="Tegenstander", kolommen=None, waarden="Duur (jaren)", bewerking="Som",
    anker="A30", titel="Draaitabel 2 — oorlogsjaren per tegenstander",
)
B4_VRAAGRIJ = 5
B4_VRAAGKOL = 11       # kolom K — naast de draaitabellen, niet eronder

# ---------------------------------------------------------------- blad 5
# De bevolkingsschattingen. Rond getal per meting, bewust zonder komma's:
# het gaat om de VORM van de lijn, niet om de precieze hoogte.
B5_KOP = ["Jaar", "Geschat aantal inwoners (miljoen)", "Verschil met vorige meting"]
B5 = [
    (1520, 12),
    (1600, 28),
    (1700, 23),
    (1800, 25),
    (1850, 35),
    (1875, 29),
    (1900, 24),
    (1914, 19),
]
B5_BRONTEKST = (
    "Ruwe schattingen, afgerond op hele miljoenen. Historici verschillen hierover; "
    "gebruik ze om te rekenen en te tekenen, niet om te citeren."
)
B5_KOPRIJ = 3
B5_START = B5_KOPRIJ + 1                     # 4
B5_EIND = B5_START + len(B5) - 1             # 11
B5_VRAAGKOL = 5                              # kolom E — kolom D blijft leeg
B5_VRAAGRIJ = B5_KOPRIJ


# ---------------------------------------------------------------- helpers
def sultan(code):
    """De rij uit de sultantabel die bij een code hoort."""
    for rij in B1:
        if rij[0] == code:
            return rij
    raise KeyError(code)


def regeringsjaren(code):
    _, _, begin, einde = sultan(code)
    return einde - begin


def eeuw(jaar):
    """1453 -> '15e eeuw'. Als tekst, want zo staat het in de lijst en zo
       sorteert een draaitabel het ook chronologisch."""
    return f"{(jaar - 1) // 100 + 1}e eeuw"


def duur(begin, einde):
    return einde - begin
