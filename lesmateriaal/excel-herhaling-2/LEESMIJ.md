# Excel — herhalingsbundel 2

Zeven korte oefeningen in **echt Excel**, samen 40 minuten.
Tweede vervolg op `lesmateriaal/excel-basis/`: **geen nieuwe leerstof**, alleen nog
meer kilometers op dezelfde tien functies.

Bedoeld voor wie na `lesmateriaal/excel-herhaling/` nog niet vlot werkt. De opbouw
is met opzet **identiek** aan die bundel — blad 1 is opnieuw optellen in twee
richtingen, blad 7 opnieuw `VERT.ZOEKEN` — met een ander bedrijf en andere cijfers.
Wie de vorige bundel af heeft, herkent elke stap en gaat sneller door.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `excel-herhaling-2-startbestand.xlsx` | leerlingen — acht werkbladen, bewust kaal |
| `excel-herhaling-2-opdrachten.docx` | leerlingen — overzicht plus één pagina per werkblad |
| `excel-herhaling-2-lerarensleutel.docx` | jou — oplossingen, tijdsindeling, veelgemaakte fouten |

**Deel er de functiefiches van de basisbundel bij uit** (`excel-functiebladen.docx`).
Die zijn niet veranderd; deze bundel verwijst ernaar in plaats van ze te herhalen.
Zonder die fiches lopen blad 6 en 7 vast.

## De zeven oefeningen

| Nr | Werkblad | Functies | Opmaak |
|---|---|---|---|
| 1 | Weekomzet | `SOM` | valuta, koptekst, totaalrij |
| 2 | Kwekers | `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `ALS`, `AANTAL.ALS` | duizendscheiding, achtergrondkleur |
| 3 | Prijsverhoging | `AFRONDEN`, `SOM` | percentage, valuta, randen |
| 4 | Bezoekers | `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | voorwaardelijke opmaak |
| 5 | Snoeicursus | `ALS`, `AANTAL.ALS`, `GEMIDDELDE` | voorwaardelijke opmaak |
| 6 | Leveranciers | `AANTAL.ALS`, `SOM.ALS`, `SOM` | valuta, randen |
| 7 | Zaden | `VERT.ZOEKEN`, `AFRONDEN`, `SOM`, `SOM.ALS` | valuta, beeld vastzetten, randen |

**Geen geneste functies.** Elke formule gebruikt hoogstens één functie.

## Waar de herhaling zit

Dertig formules over zeven bladen. Elke functie komt minstens twee keer terug:

| Functie | Formules | Functie | Formules |
|---|---|---|---|
| `SOM` | 8 | `ALS` | 2 |
| `AANTAL.ALS` | 5 | `AFRONDEN` | 2 |
| `GEMIDDELDE` | 3 | `SOM.ALS` | 2 |
| `MAX` / `MIN` / `AANTAL` | 2 elk | `VERT.ZOEKEN` | 2 |

Vier dingen zitten er bewust in:

- **Blad 3 gaat de andere kant op.** Vorige bundel ging een korting eraf, hier komt
  een verhoging erbij. Wie op de automatische piloot `=B5-C5` typt, krijgt een nieuwe
  prijs die lager is dan de oude. De controle onderaan het blad vangt dat.
- **Blad 2** heeft één kweker op precies 1200 planten, de grens. Dat is de enige rij
  waar het verschil tussen `>` en `>=` zichtbaar wordt.
- **Blad 5** heeft één cursist met precies 50 punten, om dezelfde reden.
- **Blad 4** stelt twee vragen die op elkaar lijken maar niet hetzelfde zijn: vijf
  maanden liggen boven het *gemiddelde* (4100), maar maar drie boven de *5000* van
  de `AANTAL.ALS`. Laat ze dat zelf vaststellen.

Elke oefening eindigt met een **controle die de leerling zelf kan doen**: een totaal
dat langs twee wegen moet kloppen, of deeltotalen die samen het geheel geven.

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

`controleer.py` bewaakt negen dingen:

- elke cel die als *te maken* opgegeven staat, is leeg in het startbestand
- elke cel die als *gegeven* opgegeven staat, is gevuld
- de stappen laten nergens typen in een cel die buiten de omschrijving valt
- deze bundel gebruikt geen enkele functie waar de basisbundel geen fiche voor heeft
- elke functie komt minstens twee keer voor — anders is het geen herhaling
- de brongegevens in het startbestand komen overeen met `gegevens.py`
- op blad 2 en blad 5 zit precies één rij op de grens
- de drempel op blad 4 geeft een ander antwoord dan "boven het gemiddelde"
- elke code uit de bestelling op blad 7 staat in de zoektabel (anders `#N/B`)

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
