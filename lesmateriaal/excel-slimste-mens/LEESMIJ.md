# Excel — De Slimste Mens Ter Wereld (zelfstudiebundel)

Vijf werkbladen in **echt Excel**, samen 40 minuten. Laatste herhaling op
`lesmateriaal/excel-basis/`, voor wie het nog niet vast heeft.

**Deze bundel is gemaakt om alleen af te werken, zonder leerkracht in de buurt.**
Dat verandert drie dingen tegenover de gewone herhalingsbundels:

1. **De stappen geven elke formule letterlijk.** Zonder iemand om iets aan te vragen
   mag niemand vastlopen op routinewerk; de winst zit in het juist uitvoeren.
2. **Elk blad heeft een controlegetal.** Dat staat in de opdracht, bij een cel die
   van bijna het hele blad afhangt. Komt die cel op dat getal uit, dan mogen ze
   verder — zonder dat iemand het hoeft te bevestigen.
3. **Elk blad heeft een lijstje "Loop je vast?"** met de drie fouten die het vaakst
   gemaakt worden en wat ze er zelf aan doen.

Achteraan de opdracht staat een **afvinklijst**. Daarop vullen ze na elk blad hun
controlegetal in. Jij ziet achteraf in één oogopslag waar iemand is blijven steken.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `slimste-mens-startbestand.xlsx` | leerlingen — zes werkbladen, bewust kaal |
| `slimste-mens-opdracht.docx` | leerlingen — één pagina per werkblad, plus de afvinklijst |
| `slimste-mens-lerarensleutel.docx` | jou — formules, uitkomsten, controlegetallen, veelgemaakte fouten |

De functiefiches hoeven er niet bij: de stappen geven elke formule. Leg ze wel klaar
voor wie wil weten *waarom* iets werkt.

> Het spelprogramma bestaat echt, dit seizoen niet. Deelnemers, kijkcijfers en
> uitslagen zijn verzonnen oefengegevens. Dat staat ook op het startbestand en in
> beide documenten.

## De vijf werkbladen

| Nr | Werkblad | Functies | Opmaak | Duur | Controlegetal |
|---|---|---|---|---|---|
| 1 | Kijkcijfers | `SOM` | duizendtalscheiding, koptekst, totaalrij | 5 min | `E15` = 11.830.070 |
| 2 | Deelnemers | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | koptekst, decimalen, kader, beeld vastzetten | 10 min | `B29` = 18 |
| 3 | Themas | `AANTAL.ALS`, `SOM.ALS`, `SOM` | koptekst, randen, voorwaardelijke opmaak | 9 min | `C37` = 360 |
| 4 | Rondes | `VERT.ZOEKEN`, `SOM`, `AFRONDEN` | koptekst, vulling, randen | 9 min | `E17` = 800 |
| 5 | Finaleweek | `VERT.ZOEKEN`, `SOM`, `ALS`, `AANTAL.ALS`, `GEMIDDELDE`, `MAX` | koptekst, decimalen, voorwaardelijke opmaak | 7 min | `B14` = 6 |

23 formules. De drie functies waar het vaakst op vastgelopen wordt staan vooraan:
**`SOM` 7×, `VERT.ZOEKEN` 3×, `AANTAL.ALS` 3×**. Alle tien de functies en alle vijf
de hulpfiches van de basisbundel komen aan bod. **Geen geneste functies.**

De bladen staan los van elkaar: wie halverwege strandt, heeft niets verloren.

## Wat er bewust in zit

- **Blad 2: twee deelnemers met precies 3 overwinningen**, de grens zelf. Stap 2 wijst
  hen met naam aan, zodat wie alleen werkt het verschil tussen `>` en `>=` zelf kan
  vaststellen.
- **Blad 3 zet een fout voor**: stap 3 laat eerst de verkeerde kolom intypen en
  corrigeert die meteen, zodat ze zien waar SOM.ALS naar kijkt.
- **Blad 5: één finalist op precies 150 seconden.** Wie `>` gebruikt, krijgt een 5 in
  plaats van een 6 — en dat is net het controlegetal, dus ze merken het zelf.
- **Blad 4 en 5 zijn allebei `VERT.ZOEKEN`**, eerst stap voor stap uitgelegd, dan in
  een iets andere vorm. Dat is met opzet: één keer is te weinig.

## De bestanden opnieuw maken

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle uitkomsten
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt twaalf dingen. Drie daarvan horen specifiek bij een bundel
die zonder begeleiding gemaakt wordt:

- **elke formule uit de sleutel staat LETTERLIJK in de stappen.** Loopt dat uit
  elkaar, dan typt een leerling iets anders dan wat de sleutel verwacht en kan
  niemand het rechtzetten
- **er zit nergens een geneste functie in** — de belofte van deze bundel
- **elk blad heeft een controlegetal** bij een cel die de leerling zelf maakt, en
  **minstens drie regels** bij "Loop je vast?"
- daarnaast: lege cellen waar gemaakt moet worden, gevulde cellen waar gegeven staat,
  de brongegevens, iemand precies op elke grens (en met naam genoemd in de stappen),
  elk thema aanwezig, en elke zoeksleutel precies één keer in de zoektabel

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
