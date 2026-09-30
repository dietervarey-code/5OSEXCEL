# Excel — herhalingsbundel

Zeven korte oefeningen in **echt Excel**, samen 40 minuten.
Vervolg op `lesmateriaal/excel-basis/`: **geen nieuwe leerstof**, alleen meer kilometers
op dezelfde tien functies.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `excel-herhaling-startbestand.xlsx` | leerlingen — acht werkbladen, bewust kaal |
| `excel-herhaling-opdrachten.docx` | leerlingen — overzicht plus één pagina per werkblad |
| `excel-herhaling-lerarensleutel.docx` | jou — oplossingen, tijdsindeling, veelgemaakte fouten |

**Deel er de functiefiches van de basisbundel bij uit** (`excel-functiebladen.docx`).
Die zijn niet veranderd; deze bundel verwijst ernaar in plaats van ze te herhalen.
Zonder die fiches lopen blad 6 en 7 vast.

## De zeven oefeningen

| Nr | Werkblad | Functies | Opmaak |
|---|---|---|---|
| 1 | Dagontvangsten | `SOM` | valuta, koptekst, totaalrij |
| 2 | Werkuren | `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `ALS`, `AANTAL.ALS` | decimalen, achtergrondkleur |
| 3 | Kortingen | `AFRONDEN`, `SOM` | percentage, valuta, randen |
| 4 | Verbruik | `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | voorwaardelijke opmaak |
| 5 | Inschrijvingen | `ALS`, `AANTAL.ALS`, `GEMIDDELDE` | voorwaardelijke opmaak |
| 6 | Afdelingen | `AANTAL.ALS`, `SOM.ALS`, `SOM` | valuta, randen |
| 7 | Materiaal | `VERT.ZOEKEN`, `AFRONDEN`, `SOM`, `SOM.ALS` | valuta, beeld vastzetten, randen |

**Geen geneste functies.** Elke formule gebruikt hoogstens één functie.

## Waar de herhaling zit

Dertig formules over zeven bladen. Elke functie komt minstens twee keer terug:

| Functie | Formules | Functie | Formules |
|---|---|---|---|
| `SOM` | 8 | `ALS` | 2 |
| `AANTAL.ALS` | 5 | `AFRONDEN` | 2 |
| `GEMIDDELDE` | 3 | `SOM.ALS` | 2 |
| `MAX` / `MIN` / `AANTAL` | 2 elk | `VERT.ZOEKEN` | 2 |

Twee dingen zitten er bewust in:

- **Blad 5** heeft één deelnemer van precies 18 jaar, de leeftijdsgrens. Dat is de enige
  rij waar het verschil tussen `>` en `>=` zichtbaar wordt. Wie `>` gebruikt krijgt 5 en 7
  in plaats van 6 en 6.
- **Blad 6** haalt het criterium van `AANTAL.ALS` en `SOM.ALS` uit een cel, zodat één
  formule volstaat. Het bereik moet vast (`$B$4:$B$18`), het criterium juist niet (`A20`).
  Dat is het lastigste blad van de bundel.

Elke oefening eindigt met een **controle die de leerling zelf kan doen**: een totaal dat
langs twee wegen moet kloppen, of deeltotalen die samen het geheel geven.

## Timing

Blad 7 is de uitsmijter. Wie tot en met blad 6 geraakt, heeft alle tien de functies
gebruikt. Haalt de klas het niet, dan is blad 7 huiswerk: het staat los van de rest.

## De bestanden opnieuw maken

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle uitkomsten
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt vijf dingen:

- elke cel die als *te maken* opgegeven staat, is leeg in het startbestand
- elke cel die als *gegeven* opgegeven staat, is gevuld
- de stappen laten nergens typen in een cel die buiten de omschrijving valt
- deze bundel gebruikt geen enkele functie waar de basisbundel geen fiche voor heeft
- elke functie komt minstens twee keer voor — anders is het geen herhaling

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
