# -*- coding: utf-8 -*-
"""Kijkt na of gegevens, opdracht, startbestand en sleutel bij elkaar passen.

Twee dingen krijgen hier extra aandacht:
  1. de datums moeten ECHTE datums zijn in het startbestand, anders werkt er
     geen formule en blijft de tijdlijn van blad 5 grijs;
  2. de peildatum moet in elke formule vastgezet zijn, want dat is de fout
     die in deze bundel het vaakst gemaakt wordt.
"""
import calendar
import collections
import datetime
import importlib.util
import os
import re
import sys
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))


def laad(naam, bestand):
    s = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


g = laad('g', 'gegevens.py')
a = laad('a', 'antwoorden.py')
o = laad('o', 'oefeningen.py')
f = laad('f', 'fiches.py')

WERKBOEK = os.path.join(HIER, 'festival-datums-startbestand.xlsx')
FOUTEN, GETELD = [], collections.Counter()


def eis(voorwaarde, bericht):
    if not voorwaarde:
        FOUTEN.append(bericht)
    return bool(voorwaarde)


def cel_van(adres):
    m = re.match(r'^([A-Z]{1,2})(\d+)$', adres)
    return (column_index_from_string(m.group(1)), int(m.group(2))) if m else None


# ==========================================================================
#  1. de kalender zelf — de helpers moeten doen wat Excel doet
# ==========================================================================
eis(g.PEILDATUM.weekday() == 4,
    f'de peildatum {g.PEILDATUM} is een {g.dagnaam(g.PEILDATUM)}; een festival '
    'begint op vrijdag, en de voorbeelden in de fiches gaan daarvan uit')
eis(g.weekdagnummer(g.PEILDATUM) == 5, 'weekdagnummer telt niet als WEEKDAG(;2)')
eis(g.maandnaam(g.PEILDATUM.month) == 'juli', 'maandnaam klopt niet')

# netto_werkdagen langs een tweede weg: alle dagen aflopen met calendar
def _netto_traag(van, tot):
    dagen, d = 0, van
    while d <= tot:
        if calendar.weekday(d.year, d.month, d.day) < 5:
            dagen += 1
        d += datetime.timedelta(days=1)
    return dagen


_proef = [(datetime.date(2026, 6, 29), datetime.date(2026, 7, 17)),
          (datetime.date(2026, 7, 13), datetime.date(2026, 7, 17)),
          (datetime.date(2026, 3, 2), datetime.date(2026, 3, 6)),
          (datetime.date(2026, 1, 1), datetime.date(2026, 12, 31))]
for van, tot in _proef:
    eis(g.netto_werkdagen(van, tot) == _netto_traag(van, tot),
        f'netto_werkdagen({van};{tot}) klopt niet met de kalender')
    GETELD['kalenderproeven'] += 1
# werkdag is het omgekeerde: van start n werkdagen verder, start telt niet mee
for start, n in ((datetime.date(2026, 7, 13), 5),
                 (datetime.date(2026, 6, 29), 12),
                 (datetime.date(2026, 7, 15), 2)):
    klaar = g.werkdag(start, n)
    eis(klaar.weekday() < 5, f'werkdag({start};{n}) valt in het weekend')
    eis(_netto_traag(start, klaar) == n + 1,
        f'werkdag({start};{n}) geeft {klaar}, maar daar zitten '
        f'{_netto_traag(start, klaar) - 1} werkdagen na de start in')
    GETELD['kalenderproeven'] += 1
# leeftijd_op: de dag van je verjaardag ben je al een jaar ouder
eis(g.leeftijd_op(datetime.date(2008, 7, 17), g.PEILDATUM) == 18,
    'wie op de peildatum jarig is, hoort al 18 te zijn')
eis(g.leeftijd_op(datetime.date(2008, 7, 18), g.PEILDATUM) == 17,
    'wie de dag na de peildatum jarig is, hoort nog 17 te zijn')

# ==========================================================================
#  2. de gegevens
# ==========================================================================
for taak, start, einde in g.B1:
    eis(einde > start, f'{taak}: het einde ligt niet na de start')
    eis(start.year == g.PEILDATUM.year, f'{taak} valt niet in het festivaljaar')
    GETELD['taken nagerekend'] += 1
eis(len({r[0] for r in g.B1}) == len(g.B1), 'dubbele taaknaam op blad 1')
eis(max(g.B1, key=lambda r: (r[2] - r[1]).days)[2] <= g.PEILDATUM,
    'een voorbereidingstaak loopt door na de eerste festivaldag')

for naam, geboorte in g.B2:
    leeftijd = g.leeftijd_op(geboorte, g.PEILDATUM)
    eis(10 < leeftijd < 80, f'onwaarschijnlijke leeftijd bij {naam}')
    GETELD['vrijwilligers nagerekend'] += 1
eis(len({r[0] for r in g.B2}) == len(g.B2), 'dubbele vrijwilliger')
eis(0 < a.B2_AANTAL_MAG < len(g.B2),
    f'{a.B2_AANTAL_MAG} van de {len(g.B2)} mogen achter de bar — dan zegt de '
    'kolom niets')
eis(len(a.B2_NIPT) >= 2,
    'er is niemand die vlak voor of vlak na de peildatum jarig is — dan '
    'verdwijnt de les over hele jaren')
eis(len({g.leeftijd_op(gb, g.PEILDATUM) for _n, gb in g.B2}) > 3,
    'te weinig verschillende leeftijden')

eis([d for d, _t in g.B3] == sorted(d for d, _t in g.B3),
    'de verkoopdagen staan niet op datum')
eis(len({d for d, _t in g.B3}) == len(g.B3), 'twee keer dezelfde verkoopdag')
for datum, tickets in g.B3:
    eis(tickets > 0, f'geen tickets op {datum}')
    eis(datum < g.PEILDATUM, f'{datum} ligt na de eerste festivaldag')
    GETELD['verkoopdagen nagerekend'] += 1
eis(0 < a.B3_WEEKENDDAGEN < len(g.B3),
    'alle of geen enkele verkoopdag valt in het weekend — dan leert WEEKDAG '
    'niets')
eis(len({t for _d, t in g.B3}) == len(g.B3),
    'twee verkoopdagen met hetzelfde aantal tickets — dan is de drukste dag '
    'niet eenduidig')

for taak, start, dagen in g.B4:
    eis(dagen > 0, f'{taak} duurt geen enkele werkdag')
    eis(start.weekday() < 5, f'{taak} start in het weekend ({start})')
    GETELD['opbouwtaken nagerekend'] += 1
eis(len({r[0] for r in g.B4}) == len(g.B4), 'dubbele opbouwtaak')
eis(len(a.B4_TE_LAAT) == 1,
    f'{len(a.B4_TE_LAAT)} taken komen te laat in plaats van precies één: '
    f'{a.B4_TE_LAAT}')
eis(len({r[2] for r in g.B4}) > 1, 'alle taken duren even lang')
# zonder een weekend in de looptijd zou gewoon optellen ook werken
_zonder_weekend = [taak for taak, start, dagen in g.B4
                   if (g.werkdag(start, dagen) - start).days == dagen]
eis(len(_zonder_weekend) < len(g.B4),
    'bij geen enkele taak valt er een weekend in de looptijd — dan geeft '
    'gewoon optellen hetzelfde antwoord en leert WERKDAG niets')

for datum, kanaal, tickets in g.B5:
    eis(kanaal in g.B5_KANALEN, f'onbekend kanaal {kanaal!r} op {datum}')
    eis(tickets > 0, f'geen tickets bij {kanaal} op {datum}')
    GETELD['verkoopregels nagerekend'] += 1
eis(len({(d, k) for d, k, _t in g.B5}) == len(g.B5),
    'twee regels met dezelfde datum én hetzelfde kanaal')
eis(len(a.B5_MAANDEN) >= 3,
    'minder dan drie maanden — dan valt er na het groeperen niets te zien')
eis(g.B5_TIJDLIJN_MAANDNUMMER in a.B5_PER_MAAND,
    f'de tijdlijn staat op {g.B5_TIJDLIJN_MAAND}, en die maand komt niet voor')
eis(g.maandnaam(g.B5_TIJDLIJN_MAANDNUMMER) == g.B5_TIJDLIJN_MAAND,
    'het maandnummer van de tijdlijn hoort niet bij de maandnaam')
# blad 5 is de detaillijst achter blad 3: de dagtotalen moeten kloppen
_per_dag = collections.Counter()
for datum, _k, tickets in g.B5:
    _per_dag[datum] += tickets
for datum, tickets in g.B3:
    eis(_per_dag[datum] == tickets,
        f'{datum}: blad 3 zegt {tickets} tickets, blad 5 telt op tot '
        f'{_per_dag[datum]}')
    GETELD['dagtotalen vergeleken'] += 1
eis(set(_per_dag) == {d for d, _t in g.B3},
    'blad 3 en blad 5 gaan niet over dezelfde dagen')
eis(a.B5_TOTAAL == a.B3_TOTAAL,
    f'blad 5 telt op tot {a.B5_TOTAAL} en blad 3 tot {a.B3_TOTAAL}')

# ==========================================================================
#  3. de antwoorden, langs een tweede weg
# ==========================================================================
eis(a.B1_LANGSTE_DAGEN == max((e - s).days for _t, s, e in g.B1),
    'B1_LANGSTE_DAGEN klopt niet')
eis(a.B1_SPANNE == (max(e for _t, _s, e in g.B1)
                    - min(s for _t, s, _e in g.B1)).days,
    'B1_SPANNE klopt niet')
eis(a.B2_AANTAL_MAG == sum(1 for _n, gb in g.B2
                           if g.leeftijd_op(gb, g.PEILDATUM)
                           >= g.B2_MEERDERJARIG), 'B2_AANTAL_MAG klopt niet')
eis(a.B3_WEEKENDDAGEN == sum(1 for d, _t in g.B3
                             if calendar.weekday(d.year, d.month, d.day) >= 5),
    'B3_WEEKENDDAGEN klopt niet met de kalender')
eis(a.B3_DRUKSTE_TICKETS == max(t for _d, t in g.B3),
    'B3_DRUKSTE_TICKETS klopt niet')
eis(a.B4_MEESTE_WERKDAGEN == max(a.B4_WERKDAGEN_TOT),
    'B4_MEESTE_WERKDAGEN klopt niet')
eis(a.B5_TOPMAAND_TICKETS == max(a.B5_PER_MAAND.values()),
    'B5_TOPMAAND_TICKETS klopt niet')
eis(a.B5_TOTAAL == sum(t for _d, _k, t in g.B5), 'B5_TOTAAL klopt niet')

for oef in o.OEFENINGEN:
    for cel, wat, antwoord, punten in oef['vragen']:
        eis(antwoord is not None and antwoord != '',
            f"{oef['blad']} {cel}: geen antwoord")
        eis(punten > 0, f"{oef['blad']} {cel}: geen punten")
        GETELD['vragen gekeurd'] += 1

_tekst = collections.defaultdict(list)
for oef in o.OEFENINGEN:
    for cel, _wat, antwoord, _p in oef['vragen']:
        if isinstance(antwoord, str):
            _tekst[antwoord].append(f"{oef['blad']} {cel}")
for antwoord, plekken in _tekst.items():
    eis(len(plekken) == 1,
        f'het antwoord {antwoord!r} staat op {len(plekken)} plaatsen: '
        f'{", ".join(plekken)}')

# ==========================================================================
#  4. de opdracht
# ==========================================================================
FUNCTIE = re.compile(r'\b([A-Z][A-Z.]{2,})\(')
BEKEND_ELDERS = {'ALS'}          # dat kennen ze al uit excel-basis
geleerd = {naam for kaart in f.FICHES for naam in kaart['functies']}
gebruikt = set()


def _formules(oef):
    for waar, _wat, formule, _p in oef.get('vullen', []):
        yield waar, formule
    if oef.get('los'):
        yield oef['los'][0], oef['los'][2]


for oef in o.OEFENINGEN:
    for _waar, formule in _formules(oef):
        gebruikt |= set(FUNCTIE.findall(formule))
eis(gebruikt <= geleerd | BEKEND_ELDERS,
    f'de opdracht gebruikt functies zonder fiche: '
    f'{sorted(gebruikt - geleerd - BEKEND_ELDERS)}')
for kaart in f.FICHES:
    if kaart['functies']:
        eis(set(kaart['functies']) & gebruikt,
            f"fiche {kaart['naam']} leert iets dat nergens gebruikt wordt")
GETELD['functies gekeurd'] += len(geleerd)

verwezen = {n for oef in o.OEFENINGEN for n in oef['fiches']}
eis(verwezen == set(range(1, len(f.FICHES) + 1)),
    f'niet naar elke fiche wordt verwezen: '
    f'{sorted(set(range(1, len(f.FICHES) + 1)) - verwezen)}')
for kaart in f.FICHES:
    eis(kaart['deel'] in f.DELEN, f"onbekend deel bij {kaart['naam']}")
    eis(kaart.get('wat') and kaart.get('fout'),
        f"fiche {kaart['naam']} is niet volledig")
    eis(kaart.get('schrijf') or kaart.get('stappen'),
        f"fiche {kaart['naam']} zegt niet hoe het moet")
    GETELD['fiches gekeurd'] += 1
volgorde = [k['deel'] for k in f.FICHES]
eis(volgorde == sorted(volgorde, key=f.DELEN.index),
    'de fiches van de delen staan door elkaar')
for n in {n for oef in o.OEFENINGEN for n in oef.get('kaarten_elders', ())}:
    eis(n in f.KAARTEN_ELDERS, f'kaart {n} van het andere boekje is onbekend')

for oef in o.OEFENINGEN:
    vk = oef['vraagkol']
    peil = o.peil(vk)
    for waar, formule in _formules(oef):
        eerste = waar.split(':')[0]
        kolom, rij = cel_van(eerste)
        losse = set(re.findall(r'(?<!\$)\b[A-Z]+(\d+)', formule))
        if ':' in waar:
            eis(losse == {str(rij)},
                f'{oef["blad"]} {waar}: de formule verwijst naar rij '
                f'{sorted(losse)} in plaats van naar rij {rij} — dan loopt '
                'het doorvoeren mis')
        eis(f'{get_column_letter(kolom)}{rij}' not in formule,
            f'{oef["blad"]} {waar}: de formule verwijst naar zichzelf')
        # elke verwijzing naar de peilrij moet de peildatum zijn, en vast
        for verwijzing in re.findall(r'\$?[A-Z]+\$?' + str(o.PEILRIJ) + r'\b',
                                     formule):
            eis(verwijzing == peil,
                f'{oef["blad"]} {waar}: {verwijzing} verwijst naar rij '
                f'{o.PEILRIJ} maar is niet de vastgezette peildatum {peil} — '
                'bij het doorvoeren zakt ze mee')
        GETELD['formules gekeurd'] += 1

eis(sum(int(oef['duur'].split()[0]) for oef in o.OEFENINGEN) == g.DUUR,
    'de duur van de bladen telt niet op tot de aangekondigde duur')
eis(o.TOTAAL == 50, f'de bundel staat op {o.TOTAAL} punten in plaats van 50')

# ==========================================================================
#  5. het startbestand
# ==========================================================================
LIJSTEN = [
    ('1 Voorbereiding', g.B1_KOPRIJ, g.B1_START, g.B1_EIND, g.B1_KOP, o.V1),
    ('2 Vrijwilligers', g.B2_KOPRIJ, g.B2_START, g.B2_EIND, g.B2_KOP, o.V2),
    ('3 Ticketverkoop', g.B3_KOPRIJ, g.B3_START, g.B3_EIND, g.B3_KOP, o.V3),
    ('4 Opbouw', g.B4_KOPRIJ, g.B4_START, g.B4_EIND, g.B4_KOP, o.V4),
    ('5 Verkoop per maand', g.B5_KOPRIJ, g.B5_START, g.B5_EIND, g.B5_KOP, o.V5),
]
eis({x[0] for x in LIJSTEN} == {oef['blad'] for oef in o.OEFENINGEN},
    'de bladen van LIJSTEN en van OEFENINGEN lopen uit elkaar')
eis([x[5] for x in LIJSTEN] == [oef['vraagkol'] for oef in o.OEFENINGEN],
    'de vraagkolommen van LIJSTEN en van OEFENINGEN lopen uit elkaar')

eis(os.path.exists(WERKBOEK), 'het startbestand bestaat niet — draai eerst '
                              'maak-startbestand.py')
if os.path.exists(WERKBOEK):
    wb = load_workbook(WERKBOEK)
    eis({x[0] for x in LIJSTEN} <= set(wb.sheetnames), 'ontbrekende bladen')

    for blad, koprij, start, eind, koppen, vraagkol in LIJSTEN:
        if blad not in wb.sheetnames:
            continue
        ws = wb[blad]
        breedte = len(koppen)
        for i, titel in enumerate(koppen, start=1):
            eis(ws.cell(row=koprij, column=i).value == titel,
                f'{blad}: koprij verschilt in kolom {get_column_letter(i)}')
        eis(len(set(koppen)) == breedte, f'{blad}: twee kolommen heten hetzelfde')

        temaken = set()
        for oef in o.OEFENINGEN:
            if oef['blad'] != blad:
                continue
            for waar, *_rest in oef.get('vullen', []):
                temaken.add(column_index_from_string(
                    re.match(r'([A-Z]+)', waar).group(1)))
        for kolom in range(1, breedte + 1):
            heeft = any(ws.cell(row=r, column=kolom).value is not None
                        for r in range(start, eind + 1))
            eis(heeft != (kolom in temaken),
                f'{blad}: kolom {get_column_letter(kolom)} is '
                f'{"gevuld" if heeft else "leeg"} terwijl ze '
                f'{"leeg" if kolom in temaken else "gevuld"} hoort te zijn')

        eis(vraagkol >= breedte + 2,
            f'{blad}: het vragenblok staat in kolom '
            f'{get_column_letter(vraagkol)}, de lijst loopt tot '
            f'{get_column_letter(breedte)} — er hoort een lege kolom tussen')
        for rij in range(start, eind + 1):
            eis(ws.cell(row=rij, column=breedte + 1).value is None,
                f'{blad}: kolom {get_column_letter(breedte + 1)} rij {rij} '
                'hoort leeg te blijven als scheiding')

        # de peildatum staat rechtsboven, als echte datum
        c = ws.cell(row=o.PEILRIJ, column=vraagkol + 1)
        eis(isinstance(c.value, datetime.datetime)
            and c.value.date() == g.PEILDATUM,
            f'{blad}: op {get_column_letter(vraagkol + 1)}{o.PEILRIJ} staat '
            f'{c.value!r} in plaats van de peildatum {g.PEILDATUM}')
        eis(ws.cell(row=o.PEILRIJ, column=vraagkol).value == g.PEIL_LABEL,
            f'{blad}: er staat geen label bij de peildatum')
        GETELD['lijsten gekeurd'] += 1

    # elke datum in de lijsten is een echte datum, geen tekst
    datumkolommen = {'1 Voorbereiding': (2, 3), '2 Vrijwilligers': (2,),
                     '3 Ticketverkoop': (1,), '4 Opbouw': (2,),
                     '5 Verkoop per maand': (1,)}
    for blad, koprij, start, eind, koppen, _vk in LIJSTEN:
        ws = wb[blad]
        for kolom in datumkolommen[blad]:
            for rij in range(start, eind + 1):
                c = ws.cell(row=rij, column=kolom)
                eis(isinstance(c.value, datetime.datetime),
                    f'{blad} {get_column_letter(kolom)}{rij}: {c.value!r} is '
                    'geen echte datum — dan werkt geen enkele formule')
                eis(c.number_format == g.DATUMNOTATIE,
                    f'{blad} {get_column_letter(kolom)}{rij}: geen '
                    'datumnotatie')
                GETELD['datums nagekeken'] += 1

    # geen tabel, geen grafiek, geen draaitabel
    for ws in wb.worksheets:
        eis(not list(ws.tables),
            f'{ws.title}: er staat al een tabel in het startbestand')
        eis(not getattr(ws, '_charts', None),
            f'{ws.title}: er staat al een grafiek in het startbestand')
        eis(not getattr(ws, '_pivots', None),
            f'{ws.title}: er staat al een draaitabel in het startbestand')

    for oef in o.OEFENINGEN:
        ws = wb[oef['blad']]
        for cel, *_rest in oef['vragen']:
            kolom, rij = cel_van(cel)
            eis(ws.cell(row=rij, column=kolom).value is None,
                f"{oef['blad']} {cel} moet leeg zijn in het startbestand")
            eis(ws.cell(row=rij, column=kolom - 1).value is not None,
                f"{oef['blad']} {cel}: er staat geen vraag naast")
            GETELD['antwoordcellen leeg'] += 1
        for waar, *_rest in oef.get('vullen', []):
            k1, r1 = cel_van(waar.split(':')[0])
            k2, r2 = cel_van(waar.split(':')[1])
            for k in range(k1, k2 + 1):
                for r in range(r1, r2 + 1):
                    eis(ws.cell(row=r, column=k).value is None,
                        f"{oef['blad']} {get_column_letter(k)}{r} moet leeg zijn")
                    GETELD['te vullen cellen leeg'] += 1
        if oef.get('los'):
            kolom, rij = cel_van(oef['los'][0])
            eis(ws.cell(row=rij, column=kolom).value is None,
                f"{oef['blad']} {oef['los'][0]} moet leeg zijn")
            eis(ws.cell(row=rij, column=kolom - 1).value is not None,
                f"{oef['blad']} {oef['los'][0]}: er staat geen vraag naast")
            eis(rij != o.PEILRIJ,
                'de losse cel staat op de rij van de peildatum')

# ==========================================================================
#  6. de documenten zijn gebouwd
# ==========================================================================
for naam in ('festival-datums-opdracht.docx',
             'festival-datums-lerarensleutel.docx'):
    eis(os.path.exists(os.path.join(HIER, naam)),
        f'{naam} bestaat niet — draai eerst maak-documenten.py')

# ==========================================================================
print('=' * 72)
for naam, hoeveel in sorted(GETELD.items()):
    print(f'  {hoeveel:>5}  {naam}')
print('=' * 72)
if FOUTEN:
    print(f'{len(FOUTEN)} PROBLEMEN:')
    for fout in FOUTEN:
        print('  !', fout)
    sys.exit(1)
print('alles past bij elkaar.')
