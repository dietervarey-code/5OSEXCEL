# -*- coding: utf-8 -*-
import importlib.util
spec = importlib.util.spec_from_file_location('m','/tmp/ctrl/moordzaak-data.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

houder = {b: h for b, h, _ in m.BADGES}
soort  = {b: s for b, _, s in m.BADGES}
lengte = {n: l for _, n, _, _, _, l in m.PERSONEEL}

def mins(t):
    u, mi = t.split(':'); u = int(u)
    if u < 12: u += 24          # na middernacht
    return u * 60 + int(mi)

print("STAP 1 — wie was tussen 23:40 en 00:20 op de 3e verdieping?")
raam = [(t, b, d) for t, b, d in m.LOGBOEK
        if mins('23:40') <= mins(t) <= mins('00:20')
        and ('verdieping 3' in d or (d.startswith('Kamer 3')))]
for t, b, d in sorted(raam, key=lambda r: mins(r[0])):
    print(f"   {t}  {b}  {d:26s} -> {houder[b]} ({soort[b]})")
kandidaten = {houder[b] for _, b, _ in raam}
print("   kandidaten:", sorted(kandidaten))

print("\nSTAP 2 — kaart B: donkerblauwe blazer = personeel, geen gast. Gasten vallen af.")
over = {h for h in kandidaten if soort[[b for b in houder if houder[b]==h][0]] != 'Gast'}
print("   blijft over:", sorted(over))

print("\nSTAP 3 — kaart C: de masterbadge was sinds ~22:00 weg bij de portier.")
print("   Wie kon hem nemen? Receptie achterkamer tussen 21:58 en 22:15:")
namers = [(t, b) for t, b, d in m.LOGBOEK
          if d == 'Receptie achterkamer' and mins('21:58') <= mins(t) <= mins('22:15')]
for t, b in sorted(namers, key=lambda r: mins(r[0])):
    print(f"   {t}  {b} -> {houder[b]}")
verdachten = {houder[b] for _, b in namers}

print("\nSTAP 4 — kaart D: Ilse Verbeke stond onafgebroken aan de balie (gasten bevestigen).")
verdachten.discard('Ilse Verbeke')
print("   blijft over:", sorted(verdachten))

print("\nSTAP 5 — kaart A: de dader is minstens 1m85.")
verdachten = {v for v in verdachten if lengte.get(v, 0) >= 185}
print("   lengtes:", {v: lengte[v] for v in sorted(lengte)})
print("   blijft over:", sorted(verdachten))

print("\nSTAP 6 — controle: klopt het alibi van de langste persoon (Tom Vandaele)?")
tom = [(t, d) for t, b, d in m.LOGBOEK if b == 'P-004' and mins('23:40') <= mins(t) <= mins('00:20')]
print("   badge P-004 in het tijdvak:", sorted(tom, key=lambda r: mins(r[0])))

print("\nSTAP 7 — kaart E: alleen Greet Coucke en Rachid El Amrani zijn linkshandig.")
print("   kaart F: Rachid werkte in de kelder. Zijn badge in het tijdvak:")
ra = [(t, d) for t, b, d in m.LOGBOEK if b == 'P-003' and mins('23:00') <= mins(t) <= mins('01:00')]
print("  ", sorted(ra, key=lambda r: mins(r[0])))

print("\nRESULTAAT:", sorted(verdachten))
assert verdachten == {m.DADER}, f"keten sluit niet: {verdachten}"
print("   -> de keten sluit op precies één persoon:", m.DADER)

print("\nBEVESTIGING in de gegevens:")
for t, v, n, d in m.TELEFOON:
    if 'directie' in v and '312' in n: print(f"   telefoon {t}: {v} -> {n}, {d} min")
for nr, vw, waar, bijz in m.VOORWERPEN:
    if 'P-001' in bijz or 'G.C.' in bijz or 'damesblazer' in bijz:
        print(f"   {nr}: {vw} — {waar} ({bijz})")
uit = [t for t, b, d in m.LOGBOEK if b == 'P-006' and 'uitgang' in d.lower()]
print(f"   badge P-006 (Greet Coucke) bij een uitgang: {uit or 'NOOIT — ze is het gebouw niet uit gegaan'}")
