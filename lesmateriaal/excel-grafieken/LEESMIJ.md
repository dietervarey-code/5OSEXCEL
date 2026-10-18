# Excel — Türkiye in grafieken

Vijf werkbladen, **50 minuten, 50 punten**. Eén onderwerp: de grafiek.
De zusterbundel van `excel-draaitabellen/`, met hetzelfde materiaal en
dezelfde opzet.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `grafieken-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `grafieken-opdracht.docx` | leerlingen — per blad wat ze maken |
| `grafieken-lerarensleutel.docx` | jou — per blad wat je verwacht te zien |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — **de theorie**, kaart 10 tot 14 |

Zoals bij de draaitabelbundel staat er hier geen theorie in. Elk blad verwijst
naar de kaarten.

## De opbouw

| Nr | Blad | Vraag | Type | Kaarten | Duur | Pt |
|---|---|---|---|---|---|---|
| 1 | Toeschouwers | wie is de grootste? | staafdiagram | 10, 12 | 8 min | 9 |
| 2 | Bevolking | hoe verloopt het? | lijndiagram | 11, 12, 14 | 10 min | 11 |
| 3 | Export | welk aandeel van het geheel? | cirkeldiagram | 11, 14 | 8 min | 9 |
| 4 | Toerisme | drie reeksen vergelijken | lijndiagram, 3 reeksen | 12, 14 | 10 min | 10 |
| 5 | Topscorers | eerst aanvullen, dan tekenen | staafdiagram | 10, 13 | 14 min | 11 |

**Het type is het leerdoel, niet het tekenen.** Bij elk blad staat eerst welke
vraag beantwoord wordt, en pas daarna welk type daarbij hoort.

**Blad 1 en 5 oefenen het selecteren met Ctrl**: de twee kolommen die in de
grafiek moeten, staan er niet naast elkaar. Krijgt een leerling steden of
clubcodes onder zijn balken, dan is dat de oorzaak — en dat is precies de
truc van kaart 10.

**Blad 5 begint met `VERT.ZOEKEN`**: de topscorerslijst bevat alleen een
clubcode, en ze vullen club en stad aan voordat ze tekenen.

## Twee gesprekken die deze bundel wil uitlokken

Ze staan allebei op kaart 14 en hebben allebei geen eenduidig antwoord. Dat is
de bedoeling.

- **Blad 2.** De laatste meting beslaat vijf jaar in plaats van tien, en toch
  staan alle punten even ver uit elkaar op de as. Is die lijn dan eerlijk?
- **Blad 4.** Nederland lijkt een vlakke lijn naast Duitsland en Rusland,
  alleen omdat die getallen kleiner zijn. Wat doe je als je juist Nederland
  wil tonen?

## Wat echt is en wat verzonnen

- **Echt**: de clubs, steden en landen, en de volgorde van de jaartallen.
- **Benaderend**: de bevolkingscijfers van Türkiye, afgerond.
- **Verzonnen**: toeschouwers, exportaandelen, bezoekersaantallen, doelpunten.

De exportaandelen komen met opzet uit op ronde percentages (30, 25, 20, 15,
10) die samen 100 % geven — dat maakt de controle op blad 3 eenvoudig.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` kijkt onder meer na of:

- het startbestand **geen enkele grafiek** bevat — die moeten ze zelf maken
- de clublijst op blad 1 aflopend gesorteerd staat, anders klopt de opdracht niet
- het cirkeldiagram hoogstens vijf delen heeft, zoals kaart 11 voorschrijft,
  en of de aandelen op 100 % uitkomen
- de metingen op blad 2 **niet** even ver uit elkaar liggen, want anders
  vervalt het gesprek van kaart 14
- alle drie de basistypes aan bod komen
- elke verwijzing een kaart 10 tot 14 is
- de bundel op 50 punten en 50 minuten uitkomt

Getest met ingespoten fouten: zes taartpunten, gelijke meetintervallen, een
ongesorteerde clublijst, een verwijzing naar een draaitabelkaart en een
grafiek die al in het startbestand zat. Alle vijf worden gevangen.
