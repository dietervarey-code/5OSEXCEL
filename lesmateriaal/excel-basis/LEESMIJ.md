# Excel — vijf basisoefeningen

Vijf oefeningen in **echt Excel**, samen ongeveer een lesuur.
Staat los van het oefenportaal: dit zijn bestanden die je uitdeelt.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `excel-startbestand.xlsx` | leerlingen — zes werkbladen, bewust kaal |
| `excel-opdrachtfiche.docx` | leerlingen — één blad met het overzicht en de beoordeling |
| `excel-opdrachtomschrijving.docx` | leerlingen — per werkblad wat gegeven is en wat ze moeten maken |
| `excel-stappenplan.docx` | leerlingen — dezelfde vijf oefeningen, maar stap voor stap |
| `excel-functiebladen.docx` | leerlingen — vijftien fiches met schermbeelden |
| `excel-lerarenuitleg.docx` | jou — oplossingen, tijdsindeling, veelgemaakte fouten |

## De opzet

| Nr | Oefening | Regels | Functies | Opmaak |
|---|---|---|---|---|
| 1 | Voorraadlijst afwerken | 12 | `SOM` (2×) | valuta, koptekst, totaalrij |
| 2 | Prijslijst aanpassen | 10 | `AFRONDEN` | percentage, valuta, randen |
| 3 | Verkoopcijfers samenvatten | 8 | `SOM`, `MAX`, `MIN`, `GEMIDDELDE`, `AANTAL` | achtergrondkleur, centreren |
| 4 | Bestellingen beoordelen | 14 | `ALS`, `AANTAL.ALS` (2×), `SOM.ALS` (2×) | voorwaardelijke opmaak |
| 5 | Klantenbestand aanvullen | 12 | `VERT.ZOEKEN` (2×) | randen, beeld vastzetten |

**Geen geneste functies.** Elke formule gebruikt hoogstens één functie. Optellen,
aftrekken, vermenigvuldigen en delen zijn geen functies, dus die mogen wel binnen
de haakjes staan.

Elke oefening eindigt met een **controle die de leerling zelf kan doen**: een totaal
dat langs twee wegen moet kloppen, of percentages die allemaal rond hetzelfde getal
horen te liggen. Zo zien ze hun eigen fout vóór jij het blad krijgt.

## Omschrijving naast stappenplan

Die twee overlappen bewust en dat is de bedoeling.

De **opdrachtomschrijving** zegt per werkblad *wat* er moet gebeuren: wat er al staat,
welke cellen ze moeten vullen, met welke functie, en welke opmaak erbij hoort. Eén
pagina per blad, in tabelvorm. Wie het doorheeft, heeft daar genoeg aan.

Het **stappenplan** zegt *hoe*: klik deze cel aan, typ dit, voer door tot daar,
controleer dat. Voor wie vastloopt of graag begeleid wordt.

Deel ze allebei uit. Sterkere leerlingen slaan het stappenplan vanzelf over.

## De functiefiches

Tien functiefiches en vijf fiches over dingen die geen functie zijn maar wel nodig:
absolute celverwijzing, getalnotatie, de vulgreep, voorwaardelijke opmaak en beeld
vastzetten.

Twee regels waar niet van afgeweken wordt:

1. **Een fiche geeft nooit de oplossing van een oefening.** De voorbeelden spelen in
   een eigen wereldje — punten van een toets, temperaturen, uitgaven van een uitstap —
   met andere cellen en andere cijfers dan in het startbestand. `controleer.py` faalt
   als er toch een artikelcode, klantcode of bestelnummer uit de opdracht in een fiche
   opduikt.
2. **Een fiche staat op zichzelf.** Wie vastloopt, pakt ze erbij en kan verder zonder
   iets anders te raadplegen.

Elke fiche heeft een of twee **schermbeelden**: een getekend fragment van een rekenblad,
met formulebalk, kolomkoppen en de actieve cel. Getekend en niet gefotografeerd, zodat
er geen menubalken omheen staan en het op papier leesbaar blijft.

De fiche over de dollartekens heeft er twee naast elkaar — één fout en één juist —
zodat ze zien wat er precies gebeurt als een verwijzing meeschuift.

## Nakijken

`nakijken.py` quoteert één ingeleverd bestand op 10: **8 voor het werk** en
**2 voor de inzet**.

```bash
python3 -I nakijken.py <bestand.xlsx> "<naam van de leerling>"
```

De 8 punten komen uit 39 eenheden: de 21 opdrachten uit `maken` en de 18
opmaakeisen, elk even zwaar. Binnen één doorgevoerde kolom wordt wel met delen
gewerkt — elf van de twaalf juist is elf twaalfde. De uitkomst wordt **naar
beneden** afgerond op een half punt: wie iets fout heeft, hoort niet het
maximum te krijgen.

De 2 punten inzet komen uit het aantal opdrachten dat de leerling heeft
aangeraakt, met een halve punt aftrek zodra er ergens een antwoord is
ingetypt in plaats van berekend. Dat is een maatstaf voor wie er niet bij was;
jij stond in de klas en mag ze overrulen.

Twee regels die overal gelden:

1. **Een cel is pas juist als er een formule staat én de uitkomst klopt.** Een
   ingetypt getal dat toevallig klopt, is geen Excel.
2. **Een fout telt één keer.** Wie verder rekent op een fout die hierboven al
   is aangerekend, verliest daar geen punten meer — tenzij zijn eigen formule
   ook fout is.

Het script is geijkt op het onaangeroerde startbestand: dat scoort 0/10, en
0,3 van de 39 eenheden (kolom A op blad 5 is in het startbestand al breed
genoeg). Zonder die ijking zou elke leerling gratis punten krijgen voor dingen
die al goed stonden.

`verwachting.py` houdt bij wat er in elke opdrachtcel hoort te staan. Die
waarden komen uit `antwoorden.py` en de opdrachten uit `oefeningen.py`, dus het
nakijkscript kan nooit uit de pas lopen met de bundel. Een `assert` faalt zodra
er een opdracht bijkomt zonder verwachting, of omgekeerd.

**Ingeleverde bestanden horen niet in deze map.** Ze dragen de namen van
leerlingen en deze repository is openbaar. Werk in een map buiten het project.

## De bestanden opnieuw maken

De gegevens staan in `gegevens.py`, de oefeningen in `oefeningen.py`, de fiches in
`fiches.py`. De rest wordt daaruit gebouwd, zodat stappenplan, fiches en oplossingen
nooit uit elkaar lopen.

```bash
pip install openpyxl python-docx pillow
python3 antwoorden.py         # toont alle uitkomsten
python3 maak-startbestand.py
python3 maak-documenten.py    # tekent ook de schermbeelden
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt vier dingen tegelijk:

- elke cel die de opdrachtomschrijving als *te maken* opgeeft, is leeg in het startbestand
- elke cel die ze als *gegeven* opgeeft, is gevuld
- het stappenplan laat nergens typen in een cel die buiten de omschrijving valt
- geen enkele fiche bevat een artikelcode, klantcode of bestelnummer uit de opdracht

Samen dekt dat 104 te maken cellen en 189 gegeven cellen. Verder controleert het script
nog of elke genoemde functie een fiche heeft, en of de code die bewust `#N/B` moet geven
inderdaad niet in de zoektabel staat.

Er staan **geen vaste rijnummers** in de controle: alles wordt afgeleid uit
`gegevens.py`. Voeg je daar regels toe, dan schuift de rest vanzelf mee.
