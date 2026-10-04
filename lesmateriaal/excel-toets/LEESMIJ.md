# Excel-toets — de Rode Duivels in cijfers

Synthesetoets op `lesmateriaal/excel-basis/`. Vijf werkbladen in **echt Excel**,
**50 minuten, 50 punten**.

Dit is een toets, geen oefening. Het verschil met de herhalingsbundels: er staat
**nergens een formule**. Op elk blad staat wat er moet uitkomen en met welke functie;
bij vier cellen staat zelfs dat niet en kiezen ze zelf. `controleer.py` weigert elke
opdrachttekst waarin toch een formule staat.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `rodeduivels-toets-startbestand.xlsx` | leerlingen — zes werkbladen, bewust kaal |
| `rodeduivels-toets-opdracht.docx` | leerlingen — het toetsblad, één pagina per werkblad |
| `rodeduivels-toets-verbetersleutel.docx` | jou — formules, uitkomsten, verbeterschema en quoteringsadvies |

De functiefiches **niet** uitdelen: dit is een toets op wat ze kennen.

> **De spelersnamen zijn echt, alle cijfers zijn verzonnen.** Leeftijden, caps,
> doelpunten, uitslagen en ticketprijzen zijn oefengegevens, geen statistiek. Dat
> staat ook op het startbestand, op het toetsblad en in de verbetersleutel.
> Wil je echte cijfers, pas dan `gegevens.py` aan en maak de drie bestanden opnieuw:
> alle antwoorden en alle rijnummers schuiven mee.

## De vijf werkbladen

| Nr | Werkblad | Functies | Opmaak | Duur | Punten |
|---|---|---|---|---|---|
| 1 | Selectie | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | koptekst, decimalen, voorwaardelijke opmaak, beeld vastzetten | 13 min | 12 |
| 2 | Wedstrijden | `ALS`, `SOM`, `AANTAL.ALS`, `GEMIDDELDE`, `MAX` | koptekst, totaalrij, randen, voorwaardelijke opmaak | 11 min | 10 |
| 3 | Clubdoelpunten | `AANTAL.ALS`, `SOM.ALS`, `SOM` | koptekst, randen, voorwaardelijke opmaak | 10 min | 9 |
| 4 | Tickets | `AFRONDEN`, `SOM` | percentage, valuta, koptekst, randen | 8 min | 9 |
| 5 | Wedstrijdblad | `VERT.ZOEKEN`, `SOM`, `AANTAL.ALS`, `GEMIDDELDE` | koptekst, vulling, decimalen, uitlijnen | 8 min | 10 |

**Alle tien de functies en alle vijf de hulpfiches van de basisbundel komen aan bod.**
Geen geneste functies, geen verwijzingen over de bladen heen.

37 punten op de formules, 13 op de opmaak. De bladen staan los van elkaar: wie niet
rond geraakt, kan blad 5 laten vallen zonder de rest te verliezen.

## Wat er bewust in zit

- **Eén speler zit precies op de capsgrens** (50). Dat is de enige rij waar `>`
  tegenover `>=` zichtbaar wordt.
- **De voorwaardelijke opmaak op blad 1 geeft een ánder antwoord dan de `ALS`:**
  zeven spelers liggen boven het gemiddelde aantal caps, zes zijn er ervaren. Twee
  vragen die op elkaar lijken.
- **Twee wedstrijden eindigden gelijk.** Wie `>=` gebruikt waar `>` hoort, telt ze
  als overwinningen mee.
- **De doelmannen op blad 3 geven 0 doelpunten.** Geen fout en geen foutmelding —
  maar leerlingen die daarvan schrikken slopen vaak een werkende formule.
- **Twee kortingen vallen op een halve cent** (10,875 en 6,375), zodat `AFRONDEN`
  echt iets doet. Alle acht de prijzen zijn gekozen zodat exacte en drijvende-komma-
  berekening hetzelfde antwoord geven — op een toets mag de sleutel daar niet van
  afhangen. `controleer.py` bewaakt dat.

## De bestanden opnieuw maken

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle uitkomsten
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt twaalf dingen, waaronder:

- elke cel die als *te maken* opgegeven staat, is leeg in het startbestand; elke cel
  die als *gegeven* opgegeven staat, is gevuld
- **het toetsblad bevat nergens een formule**
- elke gevraagde cel heeft een oplossing in de sleutel, met dezelfde punten
- de toets staat op precies 50 punten voor precies 50 minuten
- alle tien de functies en alle vijf de hulpfiches komen aan bod, en er wordt niets
  gebruikt waar de basisbundel geen fiche voor heeft
- precies één speler op de capsgrens, minstens één gelijkspel, minstens één positie
  op nul doelpunten
- geen enkele ticketprijs waar exact en drijvende komma anders afronden
- elk rugnummer uit de basiself staat in de spelerslijst, en geen enkel twee keer

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
