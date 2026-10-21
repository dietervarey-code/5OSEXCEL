# Excel — Minecraft in grafieken

Vijf werkbladen, **50 minuten, 50 punten**. Eén onderwerp: de
grafiek. Geen draaitabellen, geen opmaakoefening.

De zusterbundel van `excel-minecraft-draaitabellen`, en de Minecraft-versie van
`excel-grafieken` (Türkiye). Zelfde opbouw en zelfde puntenverdeling —
op één punt na, zie hieronder bij blad 4.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `minecraft-grafieken-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `minecraft-grafieken-opdracht.docx` | leerlingen — per blad wat ze maken |
| `minecraft-grafieken-lerarensleutel.docx` | jou — per blad wat je verwacht te zien |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — **de theorie**, kaart 10 tot 14 |

In deze bundel staat met opzet geen theorie: elk blad verwijst naar de
kaarten, en elke kaart staat daar op een eigen pagina.

## De opbouw

| Nr | Blad | Dataset | De vraag | Type | Kaarten | Duur | Pt |
|---|---|---|---|---|---|---|---|
| 1 | Levenspunten | 10 mobs | Wie is de grootste? | staafdiagram | 10, 12 | 8 min | 9 |
| 2 | Diepte | 10 diepten | Hoe verloopt het? | lijndiagram | 11, 12, 14 | 10 min | 11 |
| 3 | Ertsvondsten | 5 ertssoorten | Welk deel van het geheel? | cirkeldiagram | 11, 14 | 8 min | 9 |
| 4 | Schade | 3 wapens × 5 materialen | Hoe verhouden drie reeksen zich? | staafdiagram met drie reeksen | 12, 14 | 10 min | 10 |
| 5 | Handel | 12 aanbiedingen | Wie is de grootste — maar eerst aanvullen | staafdiagram | 10, 13 | 14 min | 11 |

Het type is geen smaakkwestie: bij elk blad hoort één vraag, en die vraag
bepaalt het type. Dat is de hele les.

## Waar deze bundel van de Türkiye-versie afwijkt

**Blad 4 is hier een staafdiagram met drie reeksen, geen lijndiagram.** De
horizontale as is geen tijd maar een rijtje materialen, en een lijn tussen
steen en ijzer zou beweren dat er een materiaal tussenin bestaat. Dat verschil
staat ook in de opdracht; wie toch een lijn maakt, vraag je wat het punt
halverwege betekent.

## Waarom juist deze datasets

- **Blad 2 heeft ongelijke intervallen.** Bovenaan springt de reeks per
  20 Y-niveaus, onderaan per 4 — en toch
  staan alle punten even ver uit elkaar op de as. Dat is kaart 14 in één
  grafiek. `controleer.py` bewaakt dat die intervallen ongelijk blijven, én
  dat de piek niet op het eerste of laatste punt ligt (anders is het geen piek
  maar een gewone stijging).
- **Blad 4 heeft met opzet één vlakke reeks.** De hak doet
  altijd 1 schade, wat je materiaal ook is, en verdwijnt daardoor bijna naast
  de bijl op 10. Zonder die reeks valt er niets te
  zeggen over reeksen van heel verschillende grootte, dus ook dat wordt
  bewaakt.
- **Blad 4, nog scherper:** de bijl doet meer schade per slag dan het zwaard,
  maar slaat veel trager. De grafiek zegt dus iets waars en geeft toch een
  verkeerde indruk. Dat is het beste voorbeeld van kaart 14 in de hele bundel,
  en het staat in de voetnoot op het blad zelf.
- **Blad 1 en 5 vragen allebei om Ctrl.** De twee kolommen die ze nodig hebben
  staan niet naast elkaar. Krijgen ze Nether en Nether onder hun
  balken, of beroepcodes, dan is dat de oorzaak.

## Wat echt is en wat verzonnen

- **Echt** (Java-editie): de namen van de mobs en hun dimensie, hun
  levenspunten, de schade per slag van zwaard, bijl en hak per materiaal, de
  dorpelingenberoepen met hun werkblok, en de items die ze verhandelen.
- **Verzonnen**: de diamantvondsten per Y-niveau, de verdeling van de
  ertsvondsten en de prijzen in smaragden.

De vorm van blad 2 klopt wel: boven Y = 16 vind je zo goed als niets, de piek
ligt rond Y = -59, en daaronder zit het grondgesteente in de weg. De getallen
eromheen zijn gekozen om mee te kunnen rekenen.

## De controlegetallen

| Blad | Moet geven |
|---|---|
| 1 | langste balk Hoglin (40), kortste Konijn (3), verschil 37 |
| 2 | som van de verschilkolom 15; piek bij Y = -59 (24) |
| 3 | de aandelen samen 100 %, grootste Redstone met 40% |
| 4 | de hak blijft overal op 1; hoogste balk bijl bij netheriet (10) |
| 5 | hoogste balk Betoverd boek (30 smaragden), bij de bibliothecaris |

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle vijf de datasets uitgerekend
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` kijkt na of:

- het startbestand **geen enkele grafiek** bevat — die moeten ze zelf maken
- elke lijst klaarstaat met een volledige koprij en één lege kolom vóór het
  vragenblok, en de beroepentabel van blad 5 de lijst noch het vragenblok raakt
- elke vraag precies één antwoord heeft: geen twee mobs met evenveel
  levenspunten, geen twee ertssoorten even groot, geen twee items even duur.
  `antwoorden.py` faalt luid bij een gedeelde uitschieter
- de twee lessen van hierboven overeind blijven: ongelijke intervallen en een
  echte piek op blad 2, precies één vlakke reeks op blad 4
- de drie basistypes alledrie aan bod komen en elke kaart van 10 tot 14
  minstens één keer gebruikt wordt
- de opdracht nergens zelf theorie uitlegt
- de bundel op 50 punten en 50 minuten uitkomt

Getest door er veertien fouten in te spuiten — een moblijst die niet aflopend
staat, twee mobs met evenveel levenspunten, metingen die even ver uit elkaar
liggen, een piek op het laatste punt, zes delen in een cirkel, twee
ertssoorten even groot, geen vlakke reeks op blad 4, twee items met dezelfde
prijs, een beroepentabel tegen de lijst aan, een kaart die nergens gebruikt
wordt, een grafiek zonder titel en een bundel die niet op 50 punten
uitkomt. Alle veertien worden gevangen.

**Geen vaste rijnummers.** Alles komt uit `gegevens.py`; zet je er een mob
bij, dan schuift alles mee.
