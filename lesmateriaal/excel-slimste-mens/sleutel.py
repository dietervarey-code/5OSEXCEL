# -*- coding: utf-8 -*-
"""De oplossing per werkblad, plus het controlegetal dat in de opdracht staat.

Staat apart zodat de lerarensleutel, de opdrachtbundel en controleer.py
allemaal uit dezelfde bron putten. Het controlegetal is wat een leerling die
alleen werkt gebruikt om na te gaan of hij goed zit.
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


def duizend(x):
    return f'{x:,}'.replace(',', '.')


def komma(x, n=1):
    return f'{x:.{n}f}'.replace('.', ',')


E1, T1 = g.B1_EIND, g.B1_TOTAAL                       # 13, 15
E2, S2 = g.B2_EIND, g.B2_SAMENVATTING                 # 22, 24
E3, P3, C3 = g.B3_EIND, g.B3_PER_THEMA, g.B3_CONTROLE  # 27, 30, 37
E4, T4, G4 = g.B4_EIND, g.B4_TOTAAL, g.B4_GEMIDDELDE  # 15, 17, 18
E5, A5 = g.B5_EIND, g.B5_ANTWOORD                     # 12, 14

# Per blad: (cel, formule, antwoord)
SLEUTEL = {
    1: [
        (f'E{g.B1_START}', f'=SOM(B{g.B1_START}:D{g.B1_START})',
         f'doorvoeren tot E{E1} — tien rijtotalen, van {duizend(a.B1_RIJTOTAAL[0])} '
         f'tot {duizend(a.B1_RIJTOTAAL[-1])}'),
        (f'B{T1}', f'=SOM(B{g.B1_START}:B{E1})',
         'naar RECHTS doorvoeren tot E' + str(T1) + ' — '
         + ' / '.join(duizend(x) for x in a.B1_KOLOM)
         + f' / {duizend(a.B1_EINDTOTAAL)}'),
    ],
    2: [
        (f'F{g.B2_START}', f'=ALS(D{g.B2_START}>=$B$2;"ja";"nee")',
         f'doorvoeren tot F{E2} — {a.B2_AANTAL_FINALIST}x ja'),
        (f'B{S2}', f'=SOM(C{g.B2_START}:C{E2})', f'{a.B2_AFLEVERINGEN}'),
        (f'B{S2 + 1}', f'=SOM(D{g.B2_START}:D{E2})', f'{a.B2_OVERWINNINGEN}'),
        (f'B{S2 + 2}', f'=GEMIDDELDE(C{g.B2_START}:C{E2})',
         komma(a.B2_GEM_AFLEVERINGEN)),
        (f'B{S2 + 3}', f'=MAX(D{g.B2_START}:D{E2})', f'{a.B2_MEESTE}'),
        (f'B{S2 + 4}', f'=MIN(D{g.B2_START}:D{E2})', f'{a.B2_MINSTE}'),
        (f'B{S2 + 5}', f'=AANTAL(C{g.B2_START}:C{E2})', f'{a.B2_AANTAL}'),
        (f'B{S2 + 6}', f'=AANTAL.ALS(F{g.B2_START}:F{E2};"ja")',
         f'{a.B2_AANTAL_FINALIST}'),
    ],
    3: [
        (f'B{P3}', f'=AANTAL.ALS($B${g.B3_START}:$B${E3};A{P3})',
         f'doorvoeren tot B{P3 + len(g.B3_THEMAS) - 1} — '
         + ' / '.join(str(n) for n in a.B3_AANTAL_PER)),
        (f'C{P3}',
         f'=SOM.ALS($B${g.B3_START}:$B${E3};A{P3};$D${g.B3_START}:$D${E3})',
         f'doorvoeren tot C{P3 + len(g.B3_THEMAS) - 1} — '
         + ' / '.join(str(n) for n in a.B3_SECONDEN_PER)),
        (f'C{C3}', f'=SOM(D{g.B3_START}:D{E3})', f'{a.B3_TOTAAL}'),
    ],
    4: [
        (f'B{g.B4_START}',
         f'=VERT.ZOEKEN(A{g.B4_START};$G${g.B4_TAB_START}:$I${g.B4_TAB_EIND};2;ONWAAR)',
         f'doorvoeren tot B{E4} — de rondenamen'),
        (f'C{g.B4_START}',
         f'=VERT.ZOEKEN(A{g.B4_START};$G${g.B4_TAB_START}:$I${g.B4_TAB_EIND};3;ONWAAR)',
         f'doorvoeren tot C{E4} — 20, 15, 10, 10, 15 of 20'),
        (f'E{g.B4_START}', f'=C{g.B4_START}*D{g.B4_START}',
         f'doorvoeren tot E{E4}'),
        (f'D{T4}', f'=SOM(D{g.B4_START}:D{E4})',
         f'naar RECHTS doorvoeren tot E{T4} — {a.B4_JUIST} juiste antwoorden, '
         f'{a.B4_SECONDEN} seconden'),
        (f'E{G4}', f'=AFRONDEN(E{T4}/D{T4};1)', komma(a.B4_GEMIDDELDE)),
    ],
    5: [
        (f'B{g.B5_START}',
         f'=VERT.ZOEKEN(A{g.B5_START};$I${g.B5_TAB_START}:$J${g.B5_TAB_EIND};2;ONWAAR)',
         f'doorvoeren tot B{E5} — de acht namen'),
        (f'F{g.B5_START}', f'=SOM(C{g.B5_START}:E{g.B5_START})',
         f'doorvoeren tot F{E5}'),
        (f'G{g.B5_START}', f'=ALS(F{g.B5_START}>=$B$2;"ja";"nee")',
         f'doorvoeren tot G{E5} — {a.B5_AANTAL_DOOR}x ja'),
        (f'B{A5}', f'=AANTAL.ALS(G{g.B5_START}:G{E5};"ja")', f'{a.B5_AANTAL_DOOR}'),
        (f'B{A5 + 1}', f'=GEMIDDELDE(F{g.B5_START}:F{E5})', komma(a.B5_GEM_TOTAAL)),
        (f'B{A5 + 2}', f'=MAX(F{g.B5_START}:F{E5})',
         f'{a.B5_HOOGSTE} — dat is {a.B5_WINNAAR}'),
    ],
}

# Het getal waarmee een leerling die alleen werkt kan nagaan of hij goed zit.
CONTROLE = {
    1: (f'E{T1}', duizend(a.B1_EINDTOTAAL)),
    2: (f'B{S2 + 5}', str(a.B2_AANTAL)),
    3: (f'C{C3}', str(a.B3_TOTAAL)),
    4: (f'E{T4}', str(a.B4_SECONDEN)),
    5: (f'B{A5}', str(a.B5_AANTAL_DOOR)),
}
