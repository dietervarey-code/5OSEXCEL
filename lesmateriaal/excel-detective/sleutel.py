# -*- coding: utf-8 -*-
"""De oplossing per zaak: cel, formule, antwoord. Plus de proef en de afloop.

Staat apart zodat de leerkrachtensleutel, de opdracht en controleer.py uit
dezelfde bron putten. controleer.py gebruikt hem onder meer om na te gaan dat
elke basisformule letterlijk in de stappen staat en dat de sleutelformule er
juist NIET in staat.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True   # geen __pycache__ naast het lesmateriaal

HIER = os.path.dirname(os.path.abspath(__file__))


def _laad(naam, bestand):
    spec = importlib.util.spec_from_file_location(naam, os.path.join(HIER, bestand))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _laad('g', 'gegevens.py')
a = _laad('a', 'antwoorden.py')


def euro(x):
    return f'{x:.2f}'.replace('.', ',')


def duizend(x):
    return f'{x:,}'.replace(',', '.')


def procent(x, n=1):
    return f'{x * 100:.{n}f}'.replace('.', ',') + ' %'


S1, E1, A1, T1 = g.Z1_START, g.Z1_EIND, g.Z1_ANTWOORD, g.Z1_TAB_EIND
S2, E2, P2, A2 = g.Z2_START, g.Z2_EIND, g.Z2_PER_CHAUFFEUR, g.Z2_ANTWOORD
S3, E3, A3 = g.Z3_START, g.Z3_EIND, g.Z3_ANTWOORD
S4, E4, P4, A4 = g.Z4_START, g.Z4_EIND, g.Z4_PER_GEBRUIKER, g.Z4_ANTWOORD
S5, E5, A5 = g.Z5_START, g.Z5_EIND, g.Z5_ANTWOORD

# Per zaak: (cel, formule of None als ze het zelf intypen, antwoord)
SLEUTEL = {
    1: [
        (f'F{S1}', f'=VERT.ZOEKEN(E{S1};$J${g.Z1_TAB_START}:$K${T1};2;ONWAAR)',
         f'doorvoeren tot F{E1} — de twintig handelaarsnamen'),
        (f'G{S1}', f'=ALS(EN(B{S1}="overwerk";C{S1}<$B$2);"{g.Z1_LEUGEN}";'
                   f'"{g.Z1_KLOPT}")',
         f'doorvoeren tot G{E1} — {a.Z1_AANTAL_LEUGEN}x {g.Z1_LEUGEN}'),
        (f'C{A1}', f'=AANTAL.ALS(G{S1}:G{E1};"{g.Z1_LEUGEN}")',
         f'{a.Z1_AANTAL_LEUGEN}'),
        (f'C{A1 + 1}', f'=SOM.ALS(G{S1}:G{E1};"{g.Z1_LEUGEN}";D{S1}:D{E1})',
         euro(a.Z1_BEDRAG_LEUGEN)),
        (f'C{A1 + 2}', None, f'{g.Z1_DADERCODE} — zelf in te typen na het lezen '
                             f'van kolom F'),
        (f'C{A1 + 3}', f'=SOM.ALS(E{S1}:E{E1};C{A1 + 2};D{S1}:D{E1})',
         euro(a.Z1_BEDRAG_DADER) + ' — even veel als hierboven, dat is het bewijs'),
        (f'C{A1 + 4}', f'=SOM(D{S1}:D{E1})', euro(a.Z1_TOTAAL)),
        (f'C{A1 + 5}', f'=MAX(D{S1}:D{E1})', euro(a.Z1_GROOTSTE)),
    ],
    2: [
        (f'H{S2}', f'=F{S2}-E{S2}', f'doorvoeren tot H{E2}'),
        (f'B{P2}', f'=AANTAL.ALS($C${S2}:$C${E2};A{P2})',
         f'doorvoeren tot B{P2 + 3} — '
         + ' / '.join(str(n) for n in a.Z2_AANTAL_PER)),
        (f'C{P2}', f'=SOM.ALS($C${S2}:$C${E2};A{P2};$H${S2}:$H${E2})',
         f'doorvoeren tot C{P2 + 3} — ' + ' / '.join(str(n) for n in a.Z2_KM_PER)),
        (f'C{A2}', f'=SOM(H{S2}:H{E2})', f'{duizend(a.Z2_TOTAAL)} km'),
        (f'C{A2 + 1}', f'=MAX(F{S2}:F{E2})-MIN(E{S2}:E{E2})',
         f'{duizend(a.Z2_PROEF)} — even veel als hierboven, dat is de proef'),
        (f'C{A2 + 2}', f'=MAX(H{S2}:H{E2})',
         f'{a.Z2_LANGSTE} (rit {a.Z2_LANGSTE_RIT[0]} naar {a.Z2_LANGSTE_RIT[6]})'),
        (f'C{A2 + 3}', f'=GEMIDDELDE(H{S2}:H{E2})', f'{a.Z2_GEM}'.replace('.', ',')),
        (f'C{A2 + 4}', f'=VERT.ZOEKEN(MAX(F{S2}:F{E2});$F${S2}:$G${E2};2;ONWAAR)',
         f'{a.Z2_BESTEMMING} — rit {a.Z2_LAATSTE[0]}, kilometerstand '
         f'{duizend(a.Z2_HOOGSTE_STAND)}'),
    ],
    3: [
        (f'D{S3}', f'=VERT.ZOEKEN(C{S3};$J${g.Z3_ZAAL_START}:$K${g.Z3_ZAAL_EIND};'
                   f'2;ONWAAR)', f'doorvoeren tot D{E3}'),
        (f'F{S3}', f'=ALS(AANTAL.ALS($H${g.Z3_TEL_START}:$H${g.Z3_TEL_EIND};A{S3})=0;'
                   f'"{g.Z3_GESTOLEN}";"{g.Z3_AANWEZIG}")',
         f'doorvoeren tot F{E3} — {a.Z3_AANTAL_GESTOLEN}x {g.Z3_GESTOLEN}'),
        (f'C{A3}', f'=AANTAL.ALS(F{S3}:F{E3};"{g.Z3_GESTOLEN}")',
         f'{a.Z3_AANTAL_GESTOLEN}'),
        (f'C{A3 + 1}', f'=SOM.ALS(F{S3}:F{E3};"{g.Z3_GESTOLEN}";E{S3}:E{E3})',
         duizend(a.Z3_BUIT) + ' euro'),
        (f'C{A3 + 2}', f'=SOM(E{S3}:E{E3})', duizend(a.Z3_COLLECTIE)),
        (f'C{A3 + 3}', f'=MAX(E{S3}:E{E3})',
         duizend(a.Z3_DUURSTE) + ' — K-104, en die hangt er nog'),
        (f'C{A3 + 4}', f'=GEMIDDELDE(E{S3}:E{E3})', duizend(int(a.Z3_GEM))),
    ],
    4: [
        (f'B{P4}', f'=VERT.ZOEKEN(A{P4};$H${g.Z4_TAB_START}:$J${g.Z4_TAB_EIND};'
                   f'2;ONWAAR)', f'doorvoeren tot B{P4 + 7}'),
        (f'C{P4}', f'=VERT.ZOEKEN(A{P4};$H${g.Z4_TAB_START}:$J${g.Z4_TAB_EIND};'
                   f'3;ONWAAR)', f'doorvoeren tot C{P4 + 7}'),
        (f'D{P4}', f'=AANTAL.ALS($B${S4}:$B${E4};A{P4})',
         f'doorvoeren tot D{P4 + 7} — '
         + ' / '.join(str(r[3]) for r in a.Z4_PER_GEBRUIKER)),
        (f'E{P4}', f'=ALS(SOM.ALS($B${S4}:$B${E4};A{P4};$E${S4}:$E${E4})>$B$2;'
                   f'"{g.Z4_VERDACHT}";"{g.Z4_VRIJ}")',
         f'doorvoeren tot E{P4 + 7} — bestanden per persoon: '
         + ' / '.join(str(r[4]) for r in a.Z4_PER_GEBRUIKER)),
        (f'C{A4}', f'=SOM(E{S4}:E{E4})', f'{a.Z4_TOTAAL}'),
        (f'C{A4 + 1}', f'=MAX(E{S4}:E{E4})',
         f'{a.Z4_GROOTSTE} — logregel L-15, om 23:52'),
        (f'C{A4 + 2}', f'=AANTAL.ALS(E{P4}:E{P4 + 7};"{g.Z4_VERDACHT}")',
         f'{a.Z4_AANTAL_VERDACHT} — dat moet precies 1 zijn'),
    ],
    5: [
        (f'F{S5}', f'=AFRONDEN(E{S5}/D{S5};3)',
         f'doorvoeren tot F{E5}, daarna notatie percentage'),
        (f'G{S5}', f'=ALS(F{S5}>$B$2;VERT.ZOEKEN(B{S5};$J${g.Z5_TAB_START}:'
                   f'$L${g.Z5_TAB_EIND};3;ONWAAR);"{g.Z5_GEEN}")',
         f'doorvoeren tot G{E5} — {len(a.Z5_SLECHT)}x {a.Z5_DADER}, de rest een '
         f'streepje'),
        (f'D{A5}', f'=SOM(D{S5}:D{E5})', duizend(a.Z5_GEPRODUCEERD)),
        (f'D{A5 + 1}', f'=SOM(E{S5}:E{E5})', duizend(a.Z5_AFGEKEURD)),
        (f'D{A5 + 2}', f'=MAX(F{S5}:F{E5})',
         procent(a.Z5_HOOGSTE) + ' — batch B-20'),
        (f'D{A5 + 3}', f'=GEMIDDELDE(F{S5}:F{E5})', procent(a.Z5_GEM)),
        (f'D{A5 + 4}', None, f'{a.Z5_DADER} — zelf in te typen na het lezen van kolom G'),
        (f'D{A5 + 5}', f'=AANTAL.ALS(G{S5}:G{E5};D{A5 + 4})',
         f'{a.Z5_AANTAL_DADER} — even veel als het aantal staven dat in de grafiek '
         f'uitsprong'),
    ],
}

# Wat de leerling op zijn antwoordblad moet schrijven.
OPLOSSING = {
    1: f'Zes avonden ({", ".join(a.Z1_DATA_LEUGEN)}) — telkens bij '
       f'{a.Z1_DADER}, samen {euro(a.Z1_BEDRAG_LEUGEN)} euro.',
    2: f'{a.Z2_BESTEMMING} (rit {a.Z2_LAATSTE[0]}, van '
       f'{a.Z2_LAATSTE[3]} naar {a.Z2_LAATSTE[6]} op {a.Z2_LAATSTE[1]}).',
    3: f'{a.Z3_AANTAL_GESTOLEN} stukken — '
       + ', '.join(nr for nr, _, _, _ in a.Z3_WEG)
       + f' — samen {duizend(a.Z3_BUIT)} euro, allemaal uit de '
       + f'{a.Z3_ZALEN_WEG[0]}.',
    4: f'{a.Z4_DADER[1]} ({a.Z4_DADER[2]}), met {a.Z4_DADER[4]} bestanden. '
       f'Negen om 23:40 en twaalf om 23:52.',
    5: f'Technicus {a.Z5_DADER}. Vijf slechte batches, van '
       + ' en '.join(a.Z5_MACHINES_WEG) + '.',
}
