# Excel — Türkiye in draaitabellen

Vijf werkbladen, **50 minuten, 50 punten**. Eén onderwerp: de draaitabel.
Geen herhaling van basisfuncties, geen opmaakoefening, geen grafieken.

Gemaakt na de streamingles, waar zeven van de negen leerlingen de draaitabel
niet haalden omdat de herhalingsbladen het uur opaten. Hier staat er niets
tussen: op blad 1 maken ze binnen zes minuten hun eerste draaitabel.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `draaitabellen-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `draaitabellen-opdracht.docx` | leerlingen — per blad wat ze maken |
| `draaitabellen-lerarensleutel.docx` | jou — alle vijf de draaitabellen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — **de theorie** |

De theoriebundel is **niet optioneel**. In deze bundel staat met opzet geen
theorie: elk blad verwijst naar de kaarten, en elke kaart staat daar op een
eigen pagina.

## De opbouw

| Nr | Blad | Dataset | Wat nieuw is | Kaarten | Duur | Pt |
|---|---|---|---|---|---|---|
| 1 | Süper Lig | 20 clubs | Rijen + Waarden | 3, 4 | 6 min | 7 |
| 2 | Keuken | 24 gerechten | Kolommen erbij: een kruistabel | 6, 5 | 8 min | 9 |
| 3 | Provincies | 26 provincies | Som in plaats van Aantal, sorteren | 5, 7 | 8 min | 9 |
| 4 | Series | 20 series | Groeperen per decennium, filteren, twee waardevelden | 8, 5, 7 | 12 min | 11 |
| 5 | Transfers | 22 transfers | Eerst aanvullen met `VERT.ZOEKEN`, dan vernieuwen | 2, 9 | 16 min | 14 |

Elk blad is één draaitabel. De moeilijkheid loopt op; wie blad 1 niet rond
krijgt, hoeft aan blad 4 niet te beginnen.

**Blad 5 is de enige waar formules aan te pas komen.** De transferlijst bevat
alleen een clubcode, en een draaitabel kan niet groeperen op een kolom die er
niet is. Ze vullen dus eerst club, stad en regio aan met `VERT.ZOEKEN` en maken
pas daarna de draaitabel. Daarna typen ze er één transfer bij — en ontdekken
dat vernieuwen niet volstaat omdat het bronbereik niet meegroeit. Dat is
kaart 9 in de praktijk.

## Wat echt is en wat verzonnen

Dit zeg je er één keer bij en dan is het duidelijk:

- **Echt**: de clubs, steden, provincies, gerechten en series, de regio waarin
  een stad of provincie ligt, en de oprichtings- en startjaren.
- **Benaderend**: de inwonersaantallen, afgerond op honderdduizendtallen,
  cijfers van rond 2023.
- **Verzonnen**: alle getallen waarmee gerekend wordt — punten, toeschouwers,
  bereidingstijden, afleveringen, kijkcijfers, transferbedragen.

De regio van een gerecht is een keuze, geen feit. Dat staat er ook bij, en het
is zelf een les: een draaitabel is maar zo goed als de kolom waarop je ze bouwt.

## De controlegetallen

| Blad | Moet geven |
|---|---|
| 1 | eindtotaal 20 — evenveel als er clubs zijn |
| 2 | eindtotaal 24, onderste rij 6 en 18 |
| 3 | eindtotaal 62.030.000. Staat er 26, dan telt de draaitabel provincies in plaats van inwoners |
| 4 | 20 series, gemiddelde 2.805 |
| 5 | 148 miljoen vóór de extra transfer, 157 erna |

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle vijf de draaitabellen
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` kijkt na of:

- elke lijst geschikt is als bron: koprij compleet, geen lege rij, één lege
  kolom vóór het vragenblok, en minstens twee lege rijen tussen de lijst en de
  plaats waar de draaitabel komt
- elke draaitabel verwijst naar velden die echt in die lijst staan
- elke vraag **precies één** antwoord heeft — `antwoorden.py` faalt bij een
  gedeelde eerste plaats, zodat een vraag nooit twee goede antwoorden krijgt
- elke verwijzing naar de theorie een kaart 1 tot 9 is (grafiekkaarten horen
  hier niet)
- de opdracht nergens zelf theorie uitlegt
- de bundel op 50 punten en 50 minuten uitkomt

Getest door er fouten in te spuiten: een onbekende regio, een waarde die geen
ja of nee is, een inwonersaantal dat niet afgerond is, een draaitabel te dicht
onder de lijst, een clubnummer dat niet bestaat en een verwijzing naar een
grafiekkaart. Alle zes worden gevangen.

**Geen vaste rijnummers.** De plaats van elke draaitabel wordt uit de lengte
van de lijst afgeleid; zet je er een club bij, dan schuift alles mee.
