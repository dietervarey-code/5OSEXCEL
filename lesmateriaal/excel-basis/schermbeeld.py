# -*- coding: utf-8 -*-
"""Tekent een fragment van een rekenblad als afbeelding: formulebalk,
   kolomkoppen, rijnummers, en een cel die geselecteerd is.

   Geen echte schermafdruk — een tekening. Dat is bewust: ze toont precies
   wat er toe doet, zonder de menubalken eromheen, en blijft leesbaar op papier.
"""
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

LETTER = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
LETTER_VET = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
LETTER_VAST = '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'


def _font(pad, grootte):
    return ImageFont.truetype(pad, grootte * SCHAAL)


def kolomletter(i):
    return chr(ord('A') + i)


def teken(pad, kolommen, rijen, formule=None, geselecteerd=None,
          gemarkeerd=(), rechts=(), vet_rij=None, start_rij=1):
    """kolommen : lijst van (letter, breedte in pixels)
       rijen    : lijst van lijsten met celwaarden (None = leeg)
       formule  : tekst voor de formulebalk
       geselecteerd : celadres, bv. 'B7'
       gemarkeerd   : celadressen met een zachte vulkleur
       rechts       : kolomletters waarvan de inhoud rechts uitgelijnd staat
       vet_rij      : rijnummer dat vet gezet wordt (koprij)
    """
    breedtes = [b for _, b in kolommen]
    totaal_b = KOPBREEDTE + sum(breedtes) + MARGE * 2
    balk = BALKHOOGTE if formule else 0
    totaal_h = balk + RIJHOOGTE * (len(rijen) + 1) + MARGE * 2

    img = Image.new('RGB', (totaal_b * SCHAAL, totaal_h * SCHAAL), WIT)
    d = ImageDraw.Draw(img)

    f = _font(LETTER, 11)
    fv = _font(LETTER_VET, 11)
    fk = _font(LETTER, 10)
    fm = _font(LETTER_VAST, 11)

    def vak(x, y, b, h, vul=None, rand=LIJN, dikte=1):
        d.rectangle([x * SCHAAL, y * SCHAAL, (x + b) * SCHAAL, (y + h) * SCHAAL],
                    fill=vul, outline=rand, width=dikte * SCHAAL)

    def schrijf(x, y, tekst, font, kleur=TEKST, anker='la'):
        d.text((x * SCHAAL, y * SCHAAL), tekst, font=font, fill=kleur, anchor=anker)

    # --- formulebalk ---------------------------------------------------
    if formule:
        y = MARGE
        naamvak_b = 52
        vak(MARGE, y, naamvak_b, BALKHOOGTE - 4, WIT, KOPRAND)
        schrijf(MARGE + naamvak_b / 2, y + (BALKHOOGTE - 4) / 2,
                geselecteerd or '', f, TEKST, 'mm')
        fx_x = MARGE + naamvak_b + 6
        schrijf(fx_x, y + (BALKHOOGTE - 4) / 2, 'fx', _font(LETTER, 10), GEDEMPT, 'lm')
        bal_x = fx_x + 20
        vak(bal_x, y, totaal_b - bal_x - MARGE, BALKHOOGTE - 4, WIT, KOPRAND)
        schrijf(bal_x + 6, y + (BALKHOOGTE - 4) / 2, formule, fm, ACCENT, 'lm')

    # --- kolomkoppen ---------------------------------------------------
    y0 = balk + MARGE
    vak(MARGE, y0, KOPBREEDTE, RIJHOOGTE, KOPVLAK, KOPRAND)
    x = MARGE + KOPBREEDTE
    for letter, b in kolommen:
        vak(x, y0, b, RIJHOOGTE, KOPVLAK, KOPRAND)
        schrijf(x + b / 2, y0 + RIJHOOGTE / 2, letter, fk, GEDEMPT, 'mm')
        x += b

    # --- rijen ----------------------------------------------------------
    for r, waarden in enumerate(rijen):
        rijnr = start_rij + r
        y = y0 + RIJHOOGTE * (r + 1)
        vak(MARGE, y, KOPBREEDTE, RIJHOOGTE, KOPVLAK, KOPRAND)
        schrijf(MARGE + KOPBREEDTE / 2, y + RIJHOOGTE / 2, str(rijnr), fk, GEDEMPT, 'mm')
        x = MARGE + KOPBREEDTE
        for i, (letter, b) in enumerate(kolommen):
            adres = f'{letter}{rijnr}'
            vul = VULKLEUR if adres in gemarkeerd else WIT
            vak(x, y, b, RIJHOOGTE, vul, LIJN)
            waarde = waarden[i] if i < len(waarden) else None
            if waarde is not None and waarde != '':
                font = fv if (vet_rij == rijnr) else f
                if letter in rechts:
                    schrijf(x + b - 6, y + RIJHOOGTE / 2, str(waarde), font, TEKST, 'rm')
                else:
                    schrijf(x + 6, y + RIJHOOGTE / 2, str(waarde), font, TEKST, 'lm')
            x += b

    # --- de geselecteerde cel er bovenop --------------------------------
    if geselecteerd:
        letter = geselecteerd[0]
        nummer = int(geselecteerd[1:])
        i = [l for l, _ in kolommen].index(letter)
        x = MARGE + KOPBREEDTE + sum(b for _, b in kolommen[:i])
        y = y0 + RIJHOOGTE * (nummer - start_rij + 1)
        vak(x, y, kolommen[i][1], RIJHOOGTE, None, SELECTIE, 2)

    os.makedirs(os.path.dirname(pad), exist_ok=True)
    img.save(pad, dpi=(300, 300))
    return pad
