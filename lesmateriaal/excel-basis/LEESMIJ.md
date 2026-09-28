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
