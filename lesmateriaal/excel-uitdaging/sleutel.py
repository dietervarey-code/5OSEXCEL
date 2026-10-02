# -*- coding: utf-8 -*-
"""De oplossing: per werkblad de cel, de formule en wat ze oplevert.

Staat apart zodat zowel de lerarensleutel als controleer.py ermee kan werken.
controleer.py gebruikt hem om na te gaan dat geen enkele kaart uit uitleg.py
een van deze formules weggeeft.
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

E = g.B1_EIND          # 23
A1 = g.B1_ANTWOORD     # 25
T = g.B1_TAR_EIND      # 7
P = g.B3_EIND          # 19
S = g.B3_SAMENVATTING  # 22
V = g.B4_EIND          # 12
R = g.B5_RIJ

SLEUTEL = {
    1: [
        ('F4', f'=VERT.ZOEKEN(C4;$I${g.B1_TAR_START}:$K${T};3;WAAR)',
         f'doorvoeren tot F{E}'),
        ('G4', '=AFRONDEN(C4*F4;2)', f'doorvoeren tot G{E}'),
        (f'C{A1}', f'=SOM(C4:C{E})', f'{a.B1_BEZOEKERS} bezoekers'),
        (f'C{A1 + 1}', f'=SOM(G4:G{E})', f'{a.B1_OMZET:.2f}'),
        (f'C{A1 + 2}',
         f'=SOMMEN.ALS(G4:G{E};E4:E{E};"online";C4:C{E};">={g.B1_GROOT}")',
         f'{a.B1_OMZET_ONLINE_GROOT:.2f} — let op: optelbereik vooraan'),
        (f'C{A1 + 3}', f'=AANTALLEN.ALS(E4:E{E};"kassa";C4:C{E};"<{g.B1_KLEIN}")',
         f'{a.B1_KASSA_KLEIN} boekingen'),
        (f'C{A1 + 4}', f'=GEMIDDELDE.ALS(E4:E{E};"online";C4:C{E})',
         f'{a.B1_GEM_ONLINE} — hier staat het bereik juist vooraan'),
        (f'C{A1 + 5}', f'=MAX(C4:C{E})', f'{a.B1_GROOTSTE} personen'),
        (f'C{A1 + 6}', f'=INDEX(B4:B{E};VERGELIJKEN(C{A1 + 5};C4:C{E};0))',
         a.B1_GROOTSTE_NAAM),
    ],
    2: [
        ('G4', '=SOM(B4:F4)', f'doorvoeren tot G{g.B2_EIND}'),
        (f'B{g.B2_TOTAALRIJ}', f'=SOM(B4:B{g.B2_EIND})',
         f'naar RECHTS doorvoeren tot G{g.B2_TOTAALRIJ}'),
        (f'B{g.B2_ANTWOORD}',
         f'=INDEX(A4:A{g.B2_EIND};VERGELIJKEN(MAX(G4:G{g.B2_EIND});G4:G{g.B2_EIND};0))',
         f'{a.B2_DRUKSTE_NAAM} ({a.B2_DRUKSTE} bezoekers)'),
        (f'B{g.B2_ANTWOORD + 1}',
         f'=INDEX(B3:F3;VERGELIJKEN(MAX(B{g.B2_TOTAALRIJ}:F{g.B2_TOTAALRIJ});'
         f'B{g.B2_TOTAALRIJ}:F{g.B2_TOTAALRIJ};0))',
         f'{a.B2_DRUKSTE_UUR} ({max(a.B2_UURTOTAAL)}) — zijwaarts'),
        (f'B{g.B2_ANTWOORD + 2}',
         f'=INDEX(A4:A{g.B2_EIND};VERGELIJKEN(GROOTSTE(G4:G{g.B2_EIND};2);'
         f'G4:G{g.B2_EIND};0))',
         f'{a.B2_TWEEDE_NAAM}'),
        (f'B{g.B2_ANTWOORD + 3}',
         f'=AFRONDEN(MAX(G4:G{g.B2_EIND})/G{g.B2_TOTAALRIJ};4)',
         f'{a.B2_AANDEEL:.2%} — notatie percentage'),
    ],
    3: [
        ('F4', '=(E4-D4)*24', f'doorvoeren tot F{P}. Notatie Getal, niet Tijd'),
        ('G4', '=ALS(EN(E4>$J$3;F4>=$J$4);"ja";"nee")', f'doorvoeren tot G{P}'),
        (f'B{S}', f'=AANTAL.ALS(B4:B{P};"{g.B3_ROL_TELLEN}")', f'{a.B3_AANTAL_ROL}'),
        (f'B{S + 1}', f'=AANTAL.ALS(G4:G{P};"ja")', f'{a.B3_AANTAL_NACHT}'),
        (f'B{S + 2}',
         f'=AANTALLEN.ALS(B4:B{P};"{g.B3_ROL_KRUIS[0]}";C4:C{P};"{g.B3_ROL_KRUIS[1]}")',
         f'{a.B3_KRUIS}'),
        (f'B{S + 3}', f'=SOM(F4:F{P})', f'{a.B3_TOTAAL_UREN} uur'),
        (f'B{S + 4}', f'=GEMIDDELDE.ALS(B4:B{P};"{g.B3_ROL_TELLEN}";F4:F{P})',
         f'{a.B3_GEM_ROL} (de cel bevat 4,428571…)'),
        (f'B{S + 5}', f'=MAX(F4:F{P})', f'{a.B3_LANGSTE}'),
        (f'B{S + 6}', f'=INDEX(A4:A{P};VERGELIJKEN(B{S + 5};F4:F{P};0))',
         a.B3_LANGSTE_NAAM),
    ],
    4: [
        ('F5', f"=VERT.ZOEKEN(A5;'3 Ploegen'!$A$4:$E${P};5;ONWAAR)",
         f'doorvoeren tot F{V}. Notatie uu:mm'),
        ('G5', '=ALS(EN(F5>$B$2;B5>=1;C5=$B$3;D5="ja";E5="geen");'
               f'"{g.B4_MOGELIJK}";"{g.B4_UITGESLOTEN}")',
         f'doorvoeren tot G{V}'),
        (f'B{g.B4_ANTWOORD}', f'=AANTAL.ALS(G5:G{V};"{g.B4_MOGELIJK}")',
         f'{a.B4_AANTAL_OVER} — dit is het bewijs'),
        (f'B{g.B4_ANTWOORD + 1}',
         f'=INDEX(A5:A{V};VERGELIJKEN("{g.B4_MOGELIJK}";G5:G{V};0))',
         f'{a.B4_DADER}'),
    ],
    5: [
        (f'B{R["ticket"]}', "='1 Boekingen'!C26", f'{a.B5_TICKETS:.2f}'),
        (f'B{R["opbrengst"]}', f'=SOM(B{R["ticket"]}:B{R["bar"]})',
         f'{a.B5_OPBRENGST:.2f}'),
        (f'B{R["uren"]}', "='3 Ploegen'!B25", f'{a.B5_UREN}'),
        (f'B{R["loonkost"]}', f'=AFRONDEN(B{R["uren"]}*B{R["uurloon"]};2)',
         f'{a.B5_LOONKOST:.2f}'),
        (f'B{R["kosten"]}', f'=SOM(B{R["loonkost"]}:B{R["catering"]})',
         f'{a.B5_KOSTEN:.2f}'),
        (f'B{R["winst"]}', f'=B{R["opbrengst"]}-B{R["kosten"]}', f'{a.B5_WINST:.2f}'),
        (f'B{R["marge"]}', f'=AFRONDEN(B{R["winst"]}/B{R["opbrengst"]};4)',
         f'{a.B5_MARGE:.2%} — notatie percentage'),
        (f'B{R["per_bezoeker"]}',
         f"=AFRONDEN(B{R['opbrengst']}/'1 Boekingen'!C25;2)",
         f'{a.B5_PER_BEZOEKER:.2f}'),
    ],
}

