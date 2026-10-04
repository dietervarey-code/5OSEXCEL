# -*- coding: utf-8 -*-
"""De oplossing: per werkblad de cel, de formule, het antwoord en de punten.

Staat apart zodat zowel de verbetersleutel als controleer.py ermee kan werken.
controleer.py gebruikt hem om na te gaan dat elke cel uit de opdracht ook een
oplossing heeft, dat de punten kloppen, en dat geen enkele formule per ongeluk
in het opdrachtdocument terechtkomt.
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


def _komma(x, n=2):
    return f'{x:.{n}f}'.replace('.', ',')


E1, S1 = g.B1_EIND, g.B1_SAMENVATTING          # 26, 28
E2, T2, A2 = g.B2_EIND, g.B2_TOTAAL, g.B2_ANTWOORD   # 11, 13, 15
E3, P3, C3 = g.B3_EIND, g.B3_PER_POSITIE, g.B3_CONTROLE   # 19, 22, 27
E4, T4 = g.B4_EIND, g.B4_TOTAAL                # 12, 14
E5, A5, TE = g.B5_EIND, g.B5_ANTWOORD, g.B5_TAB_EIND     # 14, 16, 25

# Per blad: (cel, formule, antwoord, punten, opmerking voor bij het verbeteren)
SLEUTEL = {
    1: [
        (f'F{g.B1_START}', f'=ALS(D{g.B1_START}>=$B$2;"ja";"nee")',
         f'{a.B1_AANTAL_ERVAREN}x ja, {len(g.B1) - a.B1_AANTAL_ERVAREN}x nee', 2,
         f'doorvoeren tot F{E1}. Zonder dollartekens loopt het vanaf rij '
         f'{g.B1_START + 1} mis.'),
        (f'B{S1}', f'=SOM(D{g.B1_START}:D{E1})', f'{a.B1_CAPS}', 1, ''),
        (f'B{S1 + 1}', f'=SOM(E{g.B1_START}:E{E1})', f'{a.B1_DOELPUNTEN}', 1, ''),
        (f'B{S1 + 2}', f'=GEMIDDELDE(C{g.B1_START}:C{E1})',
         f'{_komma(a.B1_GEM_LEEFTIJD, 1)}', 1,
         'de cel bevat meer cijfers; met één decimaal toont ze dit'),
        (f'B{S1 + 3}', f'=MAX(C{g.B1_START}:C{E1})', f'{a.B1_OUDSTE}', 1,
         'zelf te kiezen functie'),
        (f'B{S1 + 4}', f'=MIN(C{g.B1_START}:C{E1})', f'{a.B1_JONGSTE}', 1,
         'zelf te kiezen functie'),
        (f'B{S1 + 5}', f'=AANTAL(C{g.B1_START}:C{E1})', f'{a.B1_AANTAL}', 1,
         'elke getallenkolom mag: C, D of E'),
        (f'B{S1 + 6}', f'=AANTAL.ALS(F{g.B1_START}:F{E1};"ja")',
         f'{a.B1_AANTAL_ERVAREN}', 1, 'telt in kolom F, waar de woorden staan'),
    ],
    2: [
        (f'F{g.B2_START}', f'=D{g.B2_START}-E{g.B2_START}',
         ' / '.join(str(s) for s in a.B2_SALDO), 1, f'doorvoeren tot F{E2}'),
        (f'G{g.B2_START}', f'=ALS(D{g.B2_START}>E{g.B2_START};"ja";"nee")',
         f'{a.B2_AANTAL_GEWONNEN}x ja', 2,
         f'doorvoeren tot G{E2}. Een gelijkspel is geen overwinning: > en niet >='),
        (f'D{T2}', f'=SOM(D{g.B2_START}:D{E2})',
         f'{a.B2_VOOR} / {a.B2_TEGEN} / {a.B2_SALDO_TOTAAL}', 2,
         f'naar RECHTS doorvoeren tot F{T2}'),
        (f'B{A2}', f'=AANTAL.ALS(G{g.B2_START}:G{E2};"ja")',
         f'{a.B2_AANTAL_GEWONNEN}', 1, ''),
        (f'B{A2 + 1}', f'=GEMIDDELDE(D{g.B2_START}:D{E2})',
         f'{_komma(a.B2_GEM_VOOR, 3)}', 1,
         f'met één decimaal toont de cel {_komma(a.B2_GEM_VOOR, 1)}'),
        (f'B{A2 + 2}', f'=MAX(F{g.B2_START}:F{E2})', f'{a.B2_MAX_SALDO}', 1,
         'zelf te kiezen functie'),
    ],
    3: [
        (f'B{P3}', f'=AANTAL.ALS($B${g.B3_START}:$B${E3};A{P3})',
         ' / '.join(str(n) for n in a.B3_AANTAL_PER), 2,
         f'doorvoeren tot B{P3 + len(g.POSITIES) - 1}. Het bereik staat vast, '
         f'het criterium A{P3} niet.'),
        (f'C{P3}',
         f'=SOM.ALS($B${g.B3_START}:$B${E3};A{P3};$C${g.B3_START}:$C${E3})',
         ' / '.join(str(n) for n in a.B3_DOELPUNTEN_PER), 3,
         f'doorvoeren tot C{P3 + len(g.POSITIES) - 1}. De doelmannen geven 0 — '
         f'dat hoort zo.'),
        (f'C{C3}', f'=SOM(C{g.B3_START}:C{E3})', f'{a.B3_TOTAAL}', 1,
         'zelf te kiezen functie'),
    ],
    4: [
        (f'C{g.B4_START}', f'=AFRONDEN(B{g.B4_START}*$B$2;2)',
         ' / '.join(_komma(k) for k in a.B4_KORTING), 3,
         f'doorvoeren tot C{E4}. Zonder $B$2 wijst de verwijzing vanaf rij '
         f'{g.B4_START + 1} naar een lege cel.'),
        (f'D{g.B4_START}', f'=B{g.B4_START}-C{g.B4_START}',
         ' / '.join(_komma(p) for p in a.B4_ABONNEE), 1, f'doorvoeren tot D{E4}'),
        (f'B{T4}', f'=SOM(B{g.B4_START}:B{E4})',
         f'{_komma(a.B4_SOM_NORMAAL)} / {_komma(a.B4_SOM_KORTING)} / '
         f'{_komma(a.B4_SOM_ABONNEE)}', 2,
         f'naar RECHTS doorvoeren tot D{T4}'),
    ],
    5: [
        (f'B{g.B5_START}',
         f'=VERT.ZOEKEN(A{g.B5_START};$F${g.B5_TAB_START}:$H${TE};2;ONWAAR)',
         'elf spelersnamen', 3,
         f'doorvoeren tot B{E5}. Zonder dollartekens schuift de lijst mee '
         f'en volgt #N/B.'),
        (f'C{g.B5_START}',
         f'=VERT.ZOEKEN(A{g.B5_START};$F${g.B5_TAB_START}:$H${TE};3;ONWAAR)',
         'elf posities', 2, f'dezelfde formule met 3 in plaats van 2'),
        (f'B{A5}', f'=SOM(D{g.B5_START}:D{E5})', f'{a.B5_MINUTEN}', 1, ''),
        (f'B{A5 + 1}', f'=AANTAL.ALS(C{g.B5_START}:C{E5};"{g.B5_TELLEN}")',
         f'{a.B5_AANTAL_TELLEN}', 1, 'telt in kolom C, die ze zelf opgehaald hebben'),
        (f'B{A5 + 2}', f'=GEMIDDELDE(D{g.B5_START}:D{E5})',
         f'{_komma(a.B5_GEM_MINUTEN, 3)}', 1,
         f'met één decimaal toont de cel {_komma(a.B5_GEM_MINUTEN, 1)}'),
    ],
}
