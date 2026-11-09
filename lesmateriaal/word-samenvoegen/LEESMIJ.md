# Word en Excel — brieven en etiketten uit één lijst

**6 lesuren, vijf stappen, 100 punten.** Word en Excel samen:
uit één lijst 24 brieven en twee bladen etiketten maken, zonder
één brief te hertypen.

Derde bundel rond Zomerklank. In `excel-festival-tekst` kuisten ze de
line-up op met tekstfuncties, in `excel-festival-datums` rekenden ze met de
planning van editie 2026. Hier bereiden ze editie 2027 voor: de post
naar de vrijwilligers en naar de sponsors.

## Wat je uitdeelt

| Bestand | Voor wie | Wanneer |
|---|---|---|
| `samenvoegen-startbestand.xlsx` | leerlingen | stap 1, en daarna elke stap |
| `samenvoegen-opdracht.docx` | leerlingen | de hele reeks |
| `samenvoegen-theorie.docx` | leerlingen — **de theorie**, 13 fiches | de hele reeks |
| `samenvoegen-brief-vrijwilligers.docx` | leerlingen | stap 3 en 4 |
| `samenvoegen-brief-sponsors.docx` | leerlingen | stap 5 |
| `samenvoegen-lerarensleutel.docx` | jou | — |

## Bij elke kolom staat wat erin moet komen

In de opdracht staat per kolom drie dingen: de kolomletter, een omschrijving
die zegt uit welke stukken de inhoud bestaat, en **wat er in de eerste
gegevensrij hoort te staan als het klopt**. Dus niet "de aanspreking voor de
brief", maar "het woord Beste, een spatie, en de voornaam" met `Beste Lotte`
ernaast.

Die laatste kolom komt uit `antwoorden.py` en kan dus nooit uit elkaar lopen
met de sleutel. `controleer.py` eist dat elke te maken kolom er een heeft.

Twee vragen die daardoor gratis werden, zijn vervangen: de taakvraag van stap
3 gaat nu over een andere vrijwilliger dan het voorbeeld, en de etiketvraag
van stap 2 vraagt naar het veld «Volgende record» in plaats van naar iets wat
al in "Loop je vast?" stond. `controleer.py` kijkt nu ook na dat **geen enkel
tekstantwoord elders in diezelfde stap te lezen staat** — niet in de
omschrijving, niet in het voorbeeld, niet in de controle en niet in het
lijstje "Loop je vast?".

En er staat vooraan een kader **Wat je NIET zelf typt**: geen aanspreking
bedenken (de vrijwilligerslijst heeft geen geslacht, dus daar is het "Beste"
plus de voornaam; de sponsorlijst heeft er wél een kolom voor), geen naam of
adres of bedrag in een brief intypen, en de punthaken van een samenvoegveld
nooit zelf.

## De briefmodellen

De twee briefmodellen zijn er om tijd te winnen. De brief staat er al in; ze
hoeven hem niet te typen. In de vrijwilligersbrief staan oranje markers tussen
dubbele haken op de plaatsen waar een samenvoegveld komt. In de sponsorbrief
staan er géén — dat is de eindopdracht.

## De opbouw

| Stap | Wat | Waar | Lesuren | Fiches | Pt |
|---|---|---|---|---|---|
| 1 | De lijst samenvoegklaar maken | Excel | 1 | 1, 2, 3, 4 | 20 |
| 2 | Etiketten | Word | 1 | 5, 6, 7, 8, 9 | 15 |
| 3 | De brief | Word | 1 | 6, 7, 9, 12 | 20 |
| 4 | Regels en filters | Word | 1 | 10, 11, 13 | 15 |
| 5 | Eindopdracht: de sponsorbrief | Excel en Word | 2 | 2, 4, 7, 8, 10, 11 | 30 |

## Hoeveel lesuren echt?

Op papier **6**. Met deze groep zou ik er **7**
inschrijven. Stap 4 is het uur dat je kan laten vallen als het krap wordt:
filteren en sorteren is nuttig maar niet nodig om de eindopdracht te kunnen.

Wat je **niet** mag laten vallen is stap 1. Elk probleem in stap 3 komt
daarvandaan.

## De spil van de hele bundel

Eén misverstand draagt deze reeks, en het is het waard om er een kwartier aan
te besteden: **de opmaak van een cel is niet de inhoud van een cel.**

In de takentabel staat netjes `14:00` en
`€ 45,00`. Voeg je die cel samen, dan staat er in de brief
`0,5833333333` en `45`. Word neemt de waarde over, niet
de opmaak.

Daarom bestaat stap 1, en daarom is `TEKST` de enige echt nieuwe Excelfunctie
in deze bundel. `controleer.py` weigert een opdracht waarin de kolommen
Startuur, Vergoeding of Bedrag in tekst zonder `TEKST` gemaakt worden.

Fiche 12 geeft ook de andere oplossing — de opmaakschakelaar
`\#` en `\@` in het veld zelf, met Alt+F9 — voor wie een lijst krijgt waar hij
geen kolom aan mag toevoegen.

## Wat nieuw is en wat herhaling

- **Nieuw aan Excelkant**: `TEKST`. Dat is alles.
- **Herhaling aan Excelkant**: plakken met `&` (uit `excel-festival-tekst`),
  `VERT.ZOEKEN`, `DATUMVERSCHIL` (uit `excel-festival-datums`) en `ALS`.
- **Nieuw aan Wordkant**: alles. Hoofddocument en gegevensbron, velden
  invoegen, etiketten met Labels bijwerken, voorbeeld en voltooien,
  Als…Dan…Anders, filteren en sorteren.

## Waarom stap 2 de etiketten zijn en niet de brief

Een etiketvel is korter, de typische fout is zichtbaarder (alleen het eerste
etiket gevuld) en ze hebben binnen twintig minuten iets af. Dat scheelt voor
de moed. De brief komt in stap 3, als het mechanisme al zit.

## Over het startbestand

De bladen die Word leest — `Vrijwilligers` en `Sponsors` — bevatten
**niets anders dan de lijst**. Geen titel, geen voetnoot, geen losse cel
ernaast, en de koprij staat op rij 1. Dat is geen netheid: Word neemt de
eerste gebruikte rij van een werkblad als kolomnamen, en een titel erboven
maakt de hele samenvoeging stuk.

Daarom staat de peildatum op het blad `Start`, en verwijst de formule
van stap 1 ernaar met `Start!$B$1`. `controleer.py` kijkt na dat er op die
bladen echt niets buiten de lijst staat — die controle vond deze fout in mijn
eigen eerste versie.

De oranje kolomtitels zijn de kolommen die de leerling maakt; de zwarte staan
klaar.

## De controlegetallen

| Waar | Moet geven |
|---|---|
| stap 1 | overal een € in de kolom Vergoeding; totaal € 1.145,00 |
| stap 1 | 11 van de 24 zijn op 16/07/2027 nog geen 18 |
| stap 2 | 2 bladen, 18 etiketten leeg op het laatste |
| stap 3 | 24 brieven; brief 1 = Bar, 14:00, € 45,00 |
| stap 4 | de extra zin in 11 brieven; filter op Main Stage laat 6 over |
| stap 5 | 12 brieven, 3 met de extra zin; totaal € 10.250,00 |

Snelle test voor stap 4: zoek in het samengevoegde document op het woord
*toelating*. Dat moet 11 keer voorkomen.

## Wat je met het oog moet nakijken

De Excelkolommen staan in de sleutel cel per cel uitgeschreven. De Wordstappen
niet — die moet je zien. Vraag om het **hoofddocument** én het **samengevoegde
document**: in het eerste zie je of er echte velden in zitten (klik erin, het
wordt grijs, of Alt+F9), in het tweede of het resultaat klopt.

Een samenvoegveld schrijft `openpyxl` noch `python-docx` zinvol: een
`MERGEFIELD` kan wel, maar de verwijzing naar de gegevensbron is een pad op
één bepaalde computer. Dat overleeft het uitdelen niet — en de velden
invoegen is net de oefening.

## Over de gegevens

Zomerklank bestaat niet en de vrijwilligers en sponsors evenmin. De
straatnamen en gemeenten bestaan wel; de huisnummers zijn willekeurig. De
kalender klopt: 16/07/2027 is een vrijdag.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle kolommen en brieven uitgerekend
python3 maak-startbestand.py
python3 maak-documenten.py    # vijf documenten in één keer
python3 controleer.py
```

`controleer.py` kijkt na of:

- de bladen die Word leest **samenvoegklaar** zijn: koprij op rij 1, niets
  buiten de lijst, geen samengevoegde cellen, geen lege rij, geen twee
  kolommen met dezelfde naam en geen kolomnaam met tekens waar Word over
  struikelt
- de kolommen Startuur, Vergoeding en Bedrag in tekst door `TEKST` gaan
- elke formule in de juiste kolomletter staat en naar de bovenste
  gegevensrij verwijst
- de takentabel echt opgemaakt is met een uur- en een euronotatie — zonder
  die opmaak ziet de leerling het verschil tussen opmaak en inhoud niet
- **elke `[[marker]]` in het briefmodel een kolom is die echt bestaat**, en
  elke marker die de opdracht noemt ook echt in de brief staat
- in de sponsorbrief **geen enkele** marker staat
- de les overeind blijft: niet iedereen minderjarig, niet elke sponsor boven
  de drempel, beide aansprekingen aanwezig, een filter dat iets wegfiltert,
  en minstens één startuur dat niet op een heel uur valt
- elke fiche gebruikt wordt en elke functie een fiche heeft
- de bundel op 100 punten en 6 lesuren uitkomt

- **geen enkel tekstantwoord elders in diezelfde stap te lezen staat**

Getest met tweeëntwintig ingespoten fouten — een voetnoot onder de lijst, een
losse cel ernaast, samengevoegde cellen, `TEKST` vergeten, een kolom in de
verkeerde letter, een marker die geen kolom is, een marker die uit de brief
verdwenen is, markers in de sponsorbrief, geen enkele minderjarige, alle
sponsors boven de drempel, één aanspreking, twee dezelfde voornamen, een
kolomnaam met een haakje erin, en twee antwoorden die in de opdracht zelf te
lezen stonden. Eenentwintig worden gevangen; de tweeëntwintigste bleek geen
echte fout — die injectie overschreef zichzelf — en is door twee werkende
vervangen.
