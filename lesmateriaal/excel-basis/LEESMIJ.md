# Excel — vijf basisoefeningen

Vijf oefeningen van tien minuten in **echt Excel**, samen één lesuur.
Staat los van het oefenportaal: dit zijn bestanden die je uitdeelt.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `excel-startbestand.xlsx` | leerlingen — zes werkbladen, bewust kaal |
| `excel-opdrachtfiche.docx` | leerlingen — één blad met het overzicht en de beoordeling |
| `excel-stappenplan.docx` | leerlingen — de vijf oefeningen, stap voor stap |
| `excel-functiebladen.docx` | leerlingen — vijftien fiches om bij te pakken |
| `excel-lerarenuitleg.docx` | jou — oplossingen, tijdsindeling, veelgemaakte fouten |

## De opzet

| Nr | Oefening | Functies | Opmaak |
|---|---|---|---|
| 1 | Voorraadlijst afwerken | `SOM` | valuta, koptekst |
| 2 | Prijslijst aanpassen | `AFRONDEN` | percentage, valuta, randen |
| 3 | Verkoopcijfers samenvatten | `SOM`, `MAX`, `MIN`, `GEMIDDELDE`, `AANTAL` | achtergrondkleur |
| 4 | Bestellingen beoordelen | `ALS`, `AANTAL.ALS`, `SOM.ALS` | voorwaardelijke opmaak |
| 5 | Klantenbestand aanvullen | `VERT.ZOEKEN` | randen, beeld vastzetten |

**Geen geneste functies.** Elke formule gebruikt hoogstens één functie, zodat een
leerling die vastloopt maar één ding tegelijk hoeft op te zoeken.

## De functiefiches

Tien functiefiches en vijf fiches over dingen die geen functie zijn maar wel nodig:
absolute celverwijzing, getalnotatie, de vulgreep, voorwaardelijke opmaak en beeld
vastzetten.

Elke fiche staat op zichzelf: wat de functie doet, hoe je ze schrijft met elk argument
apart uitgelegd, een voorbeeld met de cijfers uit de oefening zelf, wat je moet weten,
en de fout die het vaakst gemaakt wordt. Een leerling die vastloopt, kan met de fiche
alleen verder.

## De bestanden opnieuw maken

De gegevens staan in `gegevens.py`, de oefeningen in `oefeningen.py` en de fiches in
`fiches.py`. De rest wordt daaruit gebouwd, zodat stappenplan, fiches en oplossingen
nooit uit elkaar lopen.

```bash
pip install openpyxl python-docx
python3 antwoorden.py        # toont alle uitkomsten
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py        # kijkt na of fiches, stappen en bestand bij elkaar passen
```

`controleer.py` faalt als een stap naar een cel verwijst die niet leeg is, als een
genoemde functie geen fiche heeft, of als een brongegeven verschoven is. Handig als je
later bedragen of namen aanpast.
