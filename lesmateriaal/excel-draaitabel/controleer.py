# -*- coding: utf-8 -*-
"""Kijkt de theoriebundel na.

Drie dingen worden bewaakt:

1. Elke kaart is volledig: ze zegt wat het is, hoe het werkt, en welke fout
   iedereen één keer maakt.
2. De cijfers in de voorbeeldtabellen kloppen met de voorbeeldlijst. Een
   draaitabel in een theoriekaart die niet klopt, is erger dan geen kaart.
3. Geen enkel woord uit een opdrachtbundel komt in de kaarten voor. De
   voorbeelden moeten in hun eigen wereldje blijven, anders staat de oplossing
   van een opdracht in de theorie.
"""
import collections
import glob
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True

HIER = os.path.dirname(os.path.abspath(__file__))
LESMATERIAAL = os.path.dirname(HIER)


def laad(naam, pad):
    s = importlib.util.spec_from_file_location(naam, pad)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


f = laad('f', os.path.join(HIER, 'fiches.py'))
t = laad('t', os.path.join(HIER, 'tekening.py'))

FOUTEN = []
GETELD = collections.Counter()


def eis(voorwaarde, bericht):
    if not voorwaarde:
        FOUTEN.append(bericht)
    return bool(voorwaarde)


# ==========================================================================
#  1. elke kaart is volledig
# ==========================================================================
namen = set()
for nummer, k in enumerate(f.KAARTEN, 1):
    waar = f'kaart {nummer} ({k.get("naam", "?")})'
    eis(k.get('naam'), f'{waar}: geen naam')
    eis(k.get('wat'), f'{waar}: geen korte omschrijving')
    eis(k.get('uitleg') or k.get('stappen'),
        f'{waar}: geen uitleg en geen stappen')
    eis(k.get('fout'), f'{waar}: geen "de fout die iedereen één keer maakt"')
    eis(k.get('deel') in f.DELEN, f'{waar}: onbekend deel {k.get("deel")!r}')
    eis(k['naam'] not in namen, f'{waar}: twee kaarten met dezelfde naam')
    namen.add(k['naam'])
    for spec in k.get('beelden', ()):
        eis(spec.get('onderschrift'), f'{waar}: een beeld zonder onderschrift')
        eis(spec.get('bestand'), f'{waar}: een beeld zonder bestandsnaam')
    GETELD['kaarten'] += 1
    GETELD['beelden'] += len(k.get('beelden', ()))

# de twee delen staan netjes na elkaar, niet door elkaar
volgorde = [k['deel'] for k in f.KAARTEN]
eis(volgorde == sorted(volgorde, key=f.DELEN.index),
    'de kaarten van de twee delen staan door elkaar')

# andere bundels verwijzen naar "kaart 1 tot 9" en "kaart 10 tot 14"
grens = volgorde.index(f.DEEL_GRAFIEK)
eis(grens == 9, f'het eerste deel telt {grens} kaarten; andere bundels '
                'verwijzen naar "kaart 1 tot 9"')
eis(len(f.KAARTEN) == 14, f'er zijn {len(f.KAARTEN)} kaarten; andere bundels '
                          'verwijzen naar "kaart 10 tot 14"')

# ==========================================================================
#  2. de voorbeeldcijfers kloppen
# ==========================================================================
_i = {naam: i for i, naam in enumerate(f.BIB_KOP)}
som = collections.defaultdict(int)
aantal = collections.Counter()
for rij in f.BIB:
    som[(rij[_i['Soort']], rij[_i['Klas']])] += rij[_i['Dagen']]
    aantal[(rij[_i['Soort']], rij[_i['Klas']])] += 1

klassen = f.DRAAI_KOP[1:-1]
for rij in f.DRAAI[:-1]:
    soort = rij[0]
    for j, klas in enumerate(klassen, start=1):
        verwacht = som.get((soort, klas), 0)
        gekregen = rij[j] if rij[j] != '' else 0
        eis(gekregen == verwacht,
            f'DRAAI: {soort}/{klas} staat op {gekregen}, de lijst geeft {verwacht}')
        GETELD['cellen nagerekend'] += 1
    eis(rij[-1] == sum(som.get((soort, k), 0) for k in klassen),
        f'DRAAI: rijtotaal van {soort} klopt niet')
eis(f.DRAAI[-1][-1] == sum(r[_i['Dagen']] for r in f.BIB),
    'DRAAI: het eindtotaal klopt niet met de lijst')

for rij in f.DRAAI_AANTAL[:-1]:
    soort = rij[0]
    for j, klas in enumerate(klassen, start=1):
        verwacht = aantal.get((soort, klas), 0)
        gekregen = rij[j] if rij[j] != '' else 0
        eis(gekregen == verwacht,
            f'DRAAI_AANTAL: {soort}/{klas} staat op {gekregen}, '
            f'de lijst geeft {verwacht}')
        GETELD['cellen nagerekend'] += 1
eis(f.DRAAI_AANTAL[-1][-1] == len(f.BIB),
    'DRAAI_AANTAL: het eindtotaal is niet het aantal regels van de lijst')

for rij in f.DRAAI_KAAL[:-1]:
    verwacht = sum(som.get((rij[0], k), 0) for k in klassen)
    eis(rij[1] == verwacht, f'DRAAI_KAAL: {rij[0]} klopt niet')
    GETELD['cellen nagerekend'] += 1
eis(f.DRAAI_KAAL[-1][1] == sum(r[_i['Dagen']] for r in f.BIB),
    'DRAAI_KAAL: het eindtotaal klopt niet')

# de gegroepeerde draaitabel tegen het archief
groepen = collections.Counter(f'{j // 10 * 10} - {j // 10 * 10 + 9}'
                              for j, _ in f.ARCHIEF)
for label, waarde in f.DRAAI_GROEP[:-1]:
    eis(groepen.get(label) == waarde,
        f'DRAAI_GROEP: {label} staat op {waarde}, het archief geeft '
        f'{groepen.get(label)}')
    GETELD['cellen nagerekend'] += 1
eis(f.DRAAI_GROEP[-1][1] == len(f.ARCHIEF),
    'DRAAI_GROEP: het eindtotaal is niet het aantal verbouwingen')
eis(set(groepen) == {r[0] for r in f.DRAAI_GROEP[:-1]},
    'DRAAI_GROEP: er ontbreekt of er staat een decennium te veel')

# ==========================================================================
#  3. geen woord uit een opdrachtbundel in de kaarten
# ==========================================================================
# alle tekst van alle kaarten op één hoop
def kaarttekst():
    stukken = []
    for k in f.KAARTEN:
        for sleutel in ('naam', 'wat', 'waar', 'fout'):
            if k.get(sleutel):
                stukken.append(k[sleutel])
        for sleutel in ('uitleg', 'stappen', 'weten'):
            stukken.extend(k.get(sleutel) or [])
        for spec in k.get('beelden', ()):
            stukken.append(spec.get('onderschrift', ''))
            stukken.append(spec.get('titel', ''))
            for rij in spec.get('rijen', ()):
                stukken.extend(str(w) for w in rij)
            stukken.extend(str(w) for w in spec.get('labels', ()))
            stukken.extend(str(w) for w in spec.get('velden', ()))
    return '\n'.join(stukken)


TEKST = kaarttekst().lower()

# Gewone Nederlandse woorden die in een opdracht toevallig een kolomtitel zijn.
# Ze verklappen niets: "Verschil" of "Categorie" in een theoriekaart verwijst
# niet naar één bepaalde opdracht. Zet hier alleen woorden bij die je ook in een
# willekeurige andere les zou gebruiken — nooit een naam, een plaats of een code.
# Excel-woorden. Een draaitabelinstelling als "Gemiddelde" of een veldnaam als
# "Waarden" staat in de gegevens van een bundel én in deze kaarten, en hoort
# daar allebei thuis. Dat is geen lek.
EXCEL = {
    'aantal', 'draaitabel', 'eindtotaal', 'filters', 'gemiddelde', 'grafiek',
    'kolommen', 'rijen', 'totaal', 'waarde', 'waarden',
}
ALGEMEEN = EXCEL | {
    'aandeel', 'afstand', 'bedrag', 'categorie', 'dagen', 'datum', 'december',
    'februari', 'porties',
    'januari', 'jaar', 'klas', 'maand', 'naslag', 'november', 'oktober',
    'onbekend', 'punten', 'resultaat', 'roman', 'september', 'soort', 'strip',
    'verbouwing', 'verschil',
}
# Deze lijst groeit mee met het aantal bundels: hoe meer datasets er zijn, hoe
# vaker een gewoon Nederlands woord toevallig ook een kolomtitel is. Zet er
# alleen woorden bij die je in een willekeurige andere les ook zou gebruiken —
# nooit een naam, een plaats of een code.

verdacht = collections.defaultdict(set)
for pad in sorted(set(glob.glob(os.path.join(LESMATERIAAL, '*', 'gegevens.py')))):
    map_naam = os.path.basename(os.path.dirname(pad))
    if map_naam == os.path.basename(HIER):
        continue
    try:
        mod = laad('bron_' + map_naam.replace('-', '_'), pad)
    except Exception as fout:                       # noqa: BLE001
        FOUTEN.append(f'kan {map_naam}/gegevens.py niet laden: {fout}')
        continue
    GETELD['bundels vergeleken'] += 1

    def verzamel(waarde, diepte=0):
        if diepte > 4:
            return
        if isinstance(waarde, str):
            ruw = waarde.strip()
            schoon = ruw.lower()
            # Alleen eigennamen, plaatsen en codes kunnen een opdracht
            # verklappen: die beginnen met een hoofdletter of bevatten een
            # cijfer. Gewone woorden in lopende tekst laten we links liggen.
            kandidaat = len(schoon) >= 6 and (ruw[:1].isupper()
                                              or any(c.isdigit() for c in ruw))
            if kandidaat and schoon not in ALGEMEEN:
                verdacht[schoon].add(map_naam)
        elif isinstance(waarde, (list, tuple, set)):
            for deel in waarde:
                verzamel(deel, diepte + 1)
        elif isinstance(waarde, dict):
            for deel in waarde.values():
                verzamel(deel, diepte + 1)

    for naam in dir(mod):
        if naam.startswith('_'):
            continue
        waarde = getattr(mod, naam)
        if isinstance(waarde, (list, tuple, dict, str)):
            verzamel(waarde)

# alleen losse woorden en korte namen zijn bruikbaar als lek; hele zinnen uit
# een waarschuwingstekst zoeken heeft geen zin
for term, bundels in sorted(verdacht.items()):
    if len(term) > 40 or term.count(' ') > 3:
        continue
    if re.search(r'\b' + re.escape(term) + r'\b', TEKST):
        FOUTEN.append(f'de kaarten bevatten "{term}" — dat komt uit '
                      f'{", ".join(sorted(bundels))}')
    GETELD['termen gecontroleerd'] += 1

# ==========================================================================
#  4. elk beeld laat zich tekenen
# ==========================================================================
bouwer = laad('b', os.path.join(HIER, 'maak-documenten.py')) if False else None
SOORTEN = {'rooster', 'paneel', 'dialoog', 'staaf', 'lijn', 'cirkel'}
bestanden = set()
for nummer, k in enumerate(f.KAARTEN, 1):
    for spec in k.get('beelden', ()):
        eis(spec['soort'] in SOORTEN,
            f'kaart {nummer}: onbekend soort beeld {spec["soort"]!r}')
        eis(spec['bestand'] not in bestanden,
            f'kaart {nummer}: twee beelden heten {spec["bestand"]!r}')
        bestanden.add(spec['bestand'])
        pad = os.path.join(HIER, 'beelden', spec['bestand'] + '.png')
        eis(os.path.exists(pad),
            f'kaart {nummer}: {spec["bestand"]}.png bestaat niet — draai eerst '
            'maak-documenten.py')

# er mag geen oude tekening blijven rondslingeren
map_beelden = os.path.join(HIER, 'beelden')
if os.path.isdir(map_beelden):
    op_schijf = {os.path.splitext(n)[0] for n in os.listdir(map_beelden)
                 if n.endswith('.png')}
    eis(op_schijf == bestanden,
        f'in beelden/ staan tekeningen die geen kaart meer gebruikt: '
        f'{sorted(op_schijf - bestanden)}')

bundel = os.path.join(HIER, 'draaitabellen-en-grafieken.docx')
eis(os.path.exists(bundel), 'de bundel is nog niet gebouwd')

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
print('de theoriebundel is in orde.')
