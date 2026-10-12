# -*- coding: utf-8 -*-
"""Tekent de beelden voor de theoriebundel over draaitabellen en grafieken.

Zelfde keuze als bij de functiefiches van de basisbundel: geen echte
schermafdrukken maar tekeningen. Een schermafdruk van een draaitabelpaneel
zit vol menubalken die op papier niet leesbaar zijn, en verandert bij elke
Excel-versie. Een tekening toont precies wat er toe doet.

Vijf soorten beeld:
  rooster      een fragment van een rekenblad, met formulebalk en koppen
  veldenpaneel het paneel Draaitabelvelden, met de vier vakken
  dialoog      een dialoogvenster met een lijstje keuzes
  staafdiagram een kolomdiagram
  lijndiagram  een lijndiagram, met de punten erop
  cirkeldiagram een cirkeldiagram
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

SCHAAL = 3                      # renderen op 3x, zodat het scherp afdrukt
RIJHOOGTE = 22
KOPBREEDTE = 30
BALKHOOGTE = 26
MARGE = 2

WIT = (255, 255, 255)
LIJN = (208, 208, 208)
KOPVLAK = (240, 240, 240)
KOPRAND = (190, 190, 190)
TEKST = (0, 0, 0)
GEDEMPT = (90, 90, 90)
SELECTIE = (16, 124, 65)        # het groen dat Excel om de actieve cel zet
ACCENT = (31, 56, 100)
VULKLEUR = (226, 239, 218)      # zachtgroen voor een gemarkeerde cel
GEELVLAK = (255, 242, 204)      # zachtgeel, voor een draaitabelvlak
ROOD = (192, 0, 0)
GROEN = (56, 118, 29)
BALKKLEUR = (68, 114, 196)
BALK2 = (237, 125, 49)
PANEELVLAK = (248, 248, 248)

_LETTERS = [
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
_VETTE = [
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]
_VASTE = [
    '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
]


def _pad(kandidaten):
    for p in kandidaten:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(kandidaten[0])


LETTER = _pad(_LETTERS)
LETTER_VET = _pad(_VETTE)
LETTER_VAST = _pad(_VASTE)


def _font(pad, grootte):
    return ImageFont.truetype(pad, int(grootte * SCHAAL))


def _bewaar(img, pad):
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    img.save(pad, dpi=(300, 300))
    return pad


class _Blad:
    """Een doek waarop in logische punten getekend wordt; de schaal zit erin."""

    def __init__(self, breedte, hoogte, achtergrond=WIT):
        self.b, self.h = breedte, hoogte
        self.img = Image.new('RGB', (int(breedte * SCHAAL), int(hoogte * SCHAAL)),
                             achtergrond)
        self.d = ImageDraw.Draw(self.img)

    def vak(self, x, y, b, h, vul=None, rand=LIJN, dikte=1, rond=0):
        kader = [x * SCHAAL, y * SCHAAL, (x + b) * SCHAAL, (y + h) * SCHAAL]
        if rond:
            self.d.rounded_rectangle(kader, radius=rond * SCHAAL, fill=vul,
                                     outline=rand, width=int(dikte * SCHAAL))
        else:
            self.d.rectangle(kader, fill=vul, outline=rand,
                             width=int(dikte * SCHAAL))

    def lijn(self, x1, y1, x2, y2, kleur=LIJN, dikte=1):
        self.d.line([x1 * SCHAAL, y1 * SCHAAL, x2 * SCHAAL, y2 * SCHAAL],
                    fill=kleur, width=int(dikte * SCHAAL))

    def schrijf(self, x, y, tekst, font, kleur=TEKST, anker='la'):
        self.d.text((x * SCHAAL, y * SCHAAL), str(tekst), font=font, fill=kleur,
                    anchor=anker)

    def breed(self, tekst, font):
        return self.d.textlength(str(tekst), font=font) / SCHAAL

    def pijl(self, x1, y1, x2, y2, kleur=ROOD, dikte=2):
        self.lijn(x1, y1, x2, y2, kleur, dikte)
        hoek = math.atan2(y2 - y1, x2 - x1)
        for kant in (-0.5, 0.5):
            self.lijn(x2, y2,
                      x2 - 7 * math.cos(hoek + kant),
                      y2 - 7 * math.sin(hoek + kant), kleur, dikte)

    def bewaar(self, pad):
        return _bewaar(self.img, pad)


def kolomletter(i):
    return chr(ord('A') + i)


# --------------------------------------------------------------------------
#  1. een fragment van een rekenblad
# --------------------------------------------------------------------------
def rooster(pad, kolommen, rijen, formule=None, geselecteerd=None,
            gemarkeerd=(), rechts=(), vet_rij=None, vet_kolom=(),
            start_rij=1, kaders=()):
    """kolommen : lijst van (letter, breedte)
       rijen    : lijst van lijsten met celwaarden (None of '' = leeg)
       kaders   : lijst van (bereik, kleur) om een dik kader te zetten,
                  bv. ('A1:D5', ROOD)
    """
    breedtes = [b for _, b in kolommen]
    totaal_b = KOPBREEDTE + sum(breedtes) + MARGE * 2
    balk = BALKHOOGTE if formule else 0
    totaal_h = balk + RIJHOOGTE * (len(rijen) + 1) + MARGE * 2
    bl = _Blad(totaal_b, totaal_h)

    f = _font(LETTER, 11)
    fv = _font(LETTER_VET, 11)
    fk = _font(LETTER, 10)
    fm = _font(LETTER_VAST, 10.5)
    letters = [l for l, _ in kolommen]

    def x_van(letter):
        i = letters.index(letter)
        return MARGE + KOPBREEDTE + sum(breedtes[:i])

    if formule:
        y = MARGE
        naamvak = 54
        bl.vak(MARGE, y, naamvak, BALKHOOGTE - 4, WIT, KOPRAND)
        bl.schrijf(MARGE + naamvak / 2, y + (BALKHOOGTE - 4) / 2,
                   geselecteerd or '', f, TEKST, 'mm')
        fx = MARGE + naamvak + 6
        bl.schrijf(fx, y + (BALKHOOGTE - 4) / 2, 'fx', _font(LETTER, 10),
                   GEDEMPT, 'lm')
        bx = fx + 20
        bl.vak(bx, y, totaal_b - bx - MARGE, BALKHOOGTE - 4, WIT, KOPRAND)
        bl.schrijf(bx + 6, y + (BALKHOOGTE - 4) / 2, formule, fm, ACCENT, 'lm')

    y0 = balk + MARGE
    bl.vak(MARGE, y0, KOPBREEDTE, RIJHOOGTE, KOPVLAK, KOPRAND)
    x = MARGE + KOPBREEDTE
    for letter, b in kolommen:
        bl.vak(x, y0, b, RIJHOOGTE, KOPVLAK, KOPRAND)
        bl.schrijf(x + b / 2, y0 + RIJHOOGTE / 2, letter, fk, GEDEMPT, 'mm')
        x += b

    for r, waarden in enumerate(rijen):
        rijnr = start_rij + r
        y = y0 + RIJHOOGTE * (r + 1)
        bl.vak(MARGE, y, KOPBREEDTE, RIJHOOGTE, KOPVLAK, KOPRAND)
        bl.schrijf(MARGE + KOPBREEDTE / 2, y + RIJHOOGTE / 2, rijnr, fk,
                   GEDEMPT, 'mm')
        # eerst alle vakjes, dan pas de tekst: zo mag tekst die te lang is
        # over een lege buurcel heen lopen, net als in Excel
        x = MARGE + KOPBREEDTE
        for i, (letter, b) in enumerate(kolommen):
            bl.vak(x, y, b, RIJHOOGTE,
                   VULKLEUR if f'{letter}{rijnr}' in gemarkeerd else WIT, LIJN)
            x += b
        x = MARGE + KOPBREEDTE
        for i, (letter, b) in enumerate(kolommen):
            w = waarden[i] if i < len(waarden) else None
            if w is not None and w != '':
                font = fv if (vet_rij == rijnr or letter in vet_kolom) else f
                if letter in rechts:
                    bl.schrijf(x + b - 6, y + RIJHOOGTE / 2, w, font, TEKST, 'rm')
                else:
                    bl.schrijf(x + 6, y + RIJHOOGTE / 2, w, font, TEKST, 'lm')
            x += b

    for bereik, kleur in kaders:
        van, tot = bereik.split(':')
        x1, x2 = x_van(van[0]), x_van(tot[0]) + breedtes[letters.index(tot[0])]
        y1 = y0 + RIJHOOGTE * (int(van[1:]) - start_rij + 1)
        y2 = y0 + RIJHOOGTE * (int(tot[1:]) - start_rij + 2)
        bl.vak(x1, y1, x2 - x1, y2 - y1, None, kleur, 2)

    if geselecteerd:
        letter, nummer = geselecteerd[0], int(geselecteerd[1:])
        x = x_van(letter)
        y = y0 + RIJHOOGTE * (nummer - start_rij + 1)
        bl.vak(x, y, breedtes[letters.index(letter)], RIJHOOGTE, None, SELECTIE, 2)

    return bl.bewaar(pad)


# --------------------------------------------------------------------------
#  2. het paneel Draaitabelvelden
# --------------------------------------------------------------------------
def veldenpaneel(pad, velden, filters=(), kolommen=(), rijen=(), waarden=(),
                 aangevinkt=()):
    """velden    : de kolomtitels uit de bronlijst, met een vinkvakje
       filters / kolommen / rijen / waarden : wat er in elk vak ligt
       aangevinkt: welke velden een vinkje krijgen
    """
    b, kop, regel = 210, 20, 19
    hoogte_lijst = kop + regel * len(velden) + 10
    vakhoogte = kop + regel * 2 + 8
    h = 18 + hoogte_lijst + 10 + vakhoogte * 2 + 8 + 6
    bl = _Blad(b, h, PANEELVLAK)

    f = _font(LETTER, 10)
    fv = _font(LETTER_VET, 10)
    fk = _font(LETTER_VET, 10.5)

    bl.vak(0, 0, b, h, None, KOPRAND)
    bl.schrijf(8, 9, 'Draaitabelvelden', fk, ACCENT, 'lm')

    y = 18
    bl.vak(6, y, b - 12, hoogte_lijst, WIT, KOPRAND)
    bl.schrijf(12, y + kop / 2, 'Velden toevoegen aan rapport:', f, GEDEMPT, 'lm')
    for i, veld in enumerate(velden):
        ry = y + kop + regel * i
        bl.vak(12, ry + 4, 10, 10, WIT, GEDEMPT)
        if veld in aangevinkt:
            bl.lijn(14, ry + 9, 16.5, ry + 12, ACCENT, 1.6)
            bl.lijn(16.5, ry + 12, 20, ry + 6, ACCENT, 1.6)
        bl.schrijf(28, ry + 9, veld, fv if veld in aangevinkt else f,
                   TEKST if veld in aangevinkt else GEDEMPT, 'lm')

    y += hoogte_lijst + 10
    paren = [('Filters', filters), ('Kolommen', kolommen),
             ('Rijen', rijen), ('Waarden', waarden)]
    for i, (naam, inhoud) in enumerate(paren):
        vx = 6 + (i % 2) * ((b - 12) / 2)
        vy = y + (i // 2) * vakhoogte
        bl.vak(vx, vy, (b - 12) / 2 - 3, vakhoogte - 4, GEELVLAK, KOPRAND)
        bl.schrijf(vx + 6, vy + 10, naam, fk, ACCENT, 'lm')
        for j, item in enumerate(inhoud):
            iy = vy + kop + regel * j
            bl.vak(vx + 6, iy, (b - 12) / 2 - 15, regel - 3, WIT, GEDEMPT)
            bl.schrijf(vx + 10, iy + (regel - 3) / 2, item, f, TEKST, 'lm')
    return bl.bewaar(pad)


# --------------------------------------------------------------------------
#  3. een dialoogvenster met keuzes
# --------------------------------------------------------------------------
def dialoog(pad, titel, regels, keuzes, gekozen=None, knoppen=('OK', 'Annuleren'),
            breedte=230):
    kop, regel = 24, 18
    h = kop + 8 + regel * len(regels) + 6 + regel * len(keuzes) + 14 + 24
    bl = _Blad(breedte, h, PANEELVLAK)
    f = _font(LETTER, 10)
    fv = _font(LETTER_VET, 10)
    fk = _font(LETTER_VET, 10.5)

    bl.vak(0, 0, breedte, h, None, KOPRAND)
    bl.vak(0, 0, breedte, kop, (231, 236, 244), KOPRAND)
    bl.schrijf(8, kop / 2, titel, fk, ACCENT, 'lm')

    y = kop + 8
    for r in regels:
        bl.schrijf(10, y + regel / 2, r, f, GEDEMPT, 'lm')
        y += regel
    y += 6
    for keuze in keuzes:
        bl.d.ellipse([10 * SCHAAL, (y + 4) * SCHAAL, 19 * SCHAAL, (y + 13) * SCHAAL],
                     fill=WIT, outline=GEDEMPT, width=SCHAAL)
        if keuze == gekozen:
            bl.d.ellipse([12.5 * SCHAAL, (y + 6.5) * SCHAAL,
                          16.5 * SCHAAL, (y + 10.5) * SCHAAL], fill=ACCENT)
        bl.schrijf(26, y + 8.5, keuze, fv if keuze == gekozen else f,
                   TEKST if keuze == gekozen else GEDEMPT, 'lm')
        y += regel

    y = h - 20
    x = breedte - 10
    for knop in reversed(knoppen):
        kb = bl.breed(knop, f) + 18
        bl.vak(x - kb, y, kb, 16, WIT, KOPRAND, rond=2)
        bl.schrijf(x - kb / 2, y + 8, knop, f, TEKST, 'mm')
        x -= kb + 6
    return bl.bewaar(pad)


# --------------------------------------------------------------------------
#  4. grafieken
# --------------------------------------------------------------------------
def _assen(bl, x0, y0, b, h, maximum, stappen=4, eenheid='', laag=0):
    f = _font(LETTER, 9)
    for i in range(stappen + 1):
        waarde = laag + (maximum - laag) * i / stappen
        y = y0 + h - h * i / stappen
        bl.lijn(x0, y, x0 + b, y, LIJN if i else GEDEMPT, 1)
        bl.schrijf(x0 - 5, y, f'{waarde:g}{eenheid}', f, GEDEMPT, 'rm')
    bl.lijn(x0, y0, x0, y0 + h, GEDEMPT, 1)


def staafdiagram(pad, titel, labels, waarden, breedte=330, hoogte=185,
                 kleur=BALKKLEUR, astitel_x=None, astitel_y=None,
                 waardelabels=True, markeer=None, laag=0):
    """laag : waar de verticale as begint. Standaard 0, zoals het hoort.
       Een andere waarde is er alleen om te TONEN wat er dan misgaat."""
    links, boven, onder, rechts = 46, 26, 34, 10
    bl = _Blad(breedte, hoogte)
    f = _font(LETTER, 9)
    ft = _font(LETTER_VET, 11)
    vlak_b = breedte - links - rechts
    vlak_h = hoogte - boven - onder
    top = max(waarden)
    stap = max(1, 10 ** int(math.log10(top - laag or 1)))
    maximum = math.ceil((top - laag) / stap) * stap + laag

    if titel:
        bl.schrijf(breedte / 2, 12, titel, ft, ACCENT, 'mm')
    _assen(bl, links, boven, vlak_b, vlak_h, maximum, laag=laag)

    vak = vlak_b / len(waarden)
    for i, (label, w) in enumerate(zip(labels, waarden)):
        bb = vak * 0.6
        bx = links + vak * i + (vak - bb) / 2
        bh = vlak_h * (w - laag) / (maximum - laag)
        bl.vak(bx, boven + vlak_h - bh, bb, bh,
               BALK2 if markeer == label else kleur, None)
        bl.schrijf(links + vak * (i + 0.5), boven + vlak_h + 7, label, f,
                   GEDEMPT, 'ma')
        if waardelabels:
            bl.schrijf(bx + bb / 2, boven + vlak_h - bh - 4, f'{w:g}', f,
                       TEKST, 'md')
    if astitel_x:
        bl.schrijf(breedte / 2, hoogte - 6, astitel_x, f, GEDEMPT, 'md')
    if astitel_y:
        bl.schrijf(4, boven - 8, astitel_y, f, GEDEMPT, 'ls')
    return bl.bewaar(pad)


def lijndiagram(pad, titel, labels, waarden, breedte=330, hoogte=185,
                kleur=BALKKLEUR, astitel_x=None, astitel_y=None, laag=0):
    """laag : waar de verticale as begint. Zie staafdiagram."""
    links, boven, onder, rechts = 46, 26, 34, 12
    bl = _Blad(breedte, hoogte)
    f = _font(LETTER, 9)
    ft = _font(LETTER_VET, 11)
    vlak_b = breedte - links - rechts
    vlak_h = hoogte - boven - onder

    top = max(waarden)
    stap = max(1, 10 ** int(math.log10(top - laag or 1)))
    maximum = math.ceil((top - laag) / stap) * stap + laag

    if titel:
        bl.schrijf(breedte / 2, 12, titel, ft, ACCENT, 'mm')
    for i in range(5):
        waarde = laag + (maximum - laag) * i / 4
        y = boven + vlak_h - vlak_h * i / 4
        bl.lijn(links, y, links + vlak_b, y, LIJN if i else GEDEMPT, 1)
        bl.schrijf(links - 5, y, f'{waarde:g}', f, GEDEMPT, 'rm')
    bl.lijn(links, boven, links, boven + vlak_h, GEDEMPT, 1)

    vak = vlak_b / max(1, len(waarden) - 1)
    punten = []
    for i, w in enumerate(waarden):
        x = links + vak * i
        y = boven + vlak_h - vlak_h * (w - laag) / (maximum - laag)
        punten.append((x, y))
        bl.schrijf(x, boven + vlak_h + 7, labels[i], f, GEDEMPT, 'ma')
    for (x1, y1), (x2, y2) in zip(punten, punten[1:]):
        bl.lijn(x1, y1, x2, y2, kleur, 2)
    for x, y in punten:
        bl.d.ellipse([(x - 2.5) * SCHAAL, (y - 2.5) * SCHAAL,
                      (x + 2.5) * SCHAAL, (y + 2.5) * SCHAAL], fill=kleur)
    if astitel_x:
        bl.schrijf(breedte / 2, hoogte - 6, astitel_x, f, GEDEMPT, 'md')
    if astitel_y:
        bl.schrijf(4, boven - 8, astitel_y, f, GEDEMPT, 'ls')
    return bl.bewaar(pad)


def cirkeldiagram(pad, titel, labels, waarden, breedte=250, hoogte=180):
    bl = _Blad(breedte, hoogte)
    f = _font(LETTER, 9)
    ft = _font(LETTER_VET, 11)
    bl.schrijf(breedte / 2, 12, titel, ft, ACCENT, 'mm')
    kleuren = [BALKKLEUR, BALK2, (112, 173, 71), (255, 192, 0), (165, 165, 165),
               (91, 155, 213), (237, 160, 120)]
    totaal = sum(waarden)
    mx, my, straal = 78, hoogte / 2 + 6, 56
    hoek = -90
    for i, w in enumerate(waarden):
        boog = 360 * w / totaal
        bl.d.pieslice([(mx - straal) * SCHAAL, (my - straal) * SCHAAL,
                       (mx + straal) * SCHAAL, (my + straal) * SCHAAL],
                      hoek, hoek + boog, fill=kleuren[i % len(kleuren)],
                      outline=WIT, width=SCHAAL)
        hoek += boog
    ly = my - straal + 4
    for i, (label, w) in enumerate(zip(labels, waarden)):
        bl.vak(mx + straal + 14, ly + i * 17, 10, 10,
               kleuren[i % len(kleuren)], None)
        bl.schrijf(mx + straal + 30, ly + i * 17 + 5,
                   f'{label} ({w:g})', f, TEKST, 'lm')
    return bl.bewaar(pad)
