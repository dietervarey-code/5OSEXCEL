# Excel — Minecraft in draaitabellen

Vijf werkbladen, **50 minuten, 50 punten**. Eén onderwerp: de
draaitabel. Geen herhaling van basisfuncties, geen opmaakoefening, geen
grafieken.

Dit is dezelfde bundel als `excel-draaitabellen` (Türkiye), met ander
materiaal. Zelfde opbouw, zelfde kaarten, zelfde puntenverdeling — alleen het
thema is Minecraft. Wie de ene al maakte, herkent elk blad en gaat sneller.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `minecraft-draaitabellen-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `minecraft-draaitabellen-opdracht.docx` | leerlingen — per blad wat ze maken |
| `minecraft-draaitabellen-lerarensleutel.docx` | jou — alle vijf de draaitabellen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — **de theorie** |

De theoriebundel is **niet optioneel**. In deze bundel staat met opzet geen
theorie: elk blad verwijst naar de kaarten, en elke kaart staat daar op een
eigen pagina.

## De opbouw

| Nr | Blad | Dataset | Wat nieuw is | Kaarten | Duur | Pt |
|---|---|---|---|---|---|---|
| 1 | Mobs | 32 mobs | Rijen + Waarden | 3, 4 | 6 min | 7 |
| 2 | Blokken | 32 blokken | Kolommen erbij: een kruistabel | 6, 5 | 8 min | 9 |
| 3 | Gereedschap | 30 stuks gereedschap | Som in plaats van Aantal, sorteren | 5, 7 | 8 min | 9 |
| 4 | Updates | 22 updates | Groeperen per 5 jaar, filteren, twee waardevelden | 8, 5, 7 | 12 min | 11 |
| 5 | Dorpelingen | 20 dorpelingen | Eerst aanvullen met `VERT.ZOEKEN`, dan vernieuwen | 2, 9 | 16 min | 14 |

Elk blad is één draaitabel. De moeilijkheid loopt op; wie blad 1 niet rond
krijgt, hoeft aan blad 4 niet te beginnen.

**Blad 5 is het enige waar formules aan te pas komen.** De dorpelingenlijst
bevat alleen een beroepcode, en een draaitabel kan niet groeperen op een kolom
die er niet is. Ze vullen dus eerst beroep, werkblok en categorie aan met
`VERT.ZOEKEN` en maken pas daarna de draaitabel. Daarna typen ze er één
dorpeling bij — en ontdekken dat vernieuwen niet volstaat omdat het bronbereik
niet meegroeit. Dat is kaart 9 in de praktijk.

## Waarom juist deze datasets

- **Blad 3 is met opzet gemeen.** Van elk materiaal zijn er evenveel stuks
  gereedschap, dus met *Aantal* geeft élke rij 5 — een tabel
  die er geloofwaardig uitziet en niets zegt. Alleen met *Som* zie je dat
  Netheriet op 10.155 uitkomt en Goud op
  160 — lager nog dan hout.
  `controleer.py` bewaakt dat die aantallen gelijk blijven.
- **Blad 4 heeft twee waardevelden om één reden**: de periode met de meeste
  updates (2010 - 2014, 9) is niet de periode met de
  grootste updates (2020 - 2024, gemiddeld
  32,50). Zonder dat verschil valt er in de
  tweede kolom niets te zien, en ook dát wordt bewaakt.
- **Blad 2 heeft 7 lege vakjes.** Dat is geen slordigheid: de
  derde vraag gaat er zelfs over (Erts is de enige categorie
  waarin élk blok hetzelfde gereedschap vraagt).

## Wat echt is en wat verzonnen

Dit zeg je er één keer bij en dan is het duidelijk:

- **Echt** (Java-editie): de namen van de mobs, blokken, gereedschappen,
  updates en dorpelingenberoepen, hun categorie en dimensie, de levenspunten,
  de duurzaamheid, de jaartallen van de updates en het werkblok van elk beroep.
- **Een keuze van ons**: de indeling van de blokken in categorieën en van de
  updates in een hoofdthema.
- **Verzonnen**: het aantal aanbiedingen van de dorpelingen en het aantal
  nieuwe blokken per update.

Alles mag nagekeken worden op de wiki, en dat zeg je er ook bij. Een leerling
die opmerkt dat netherrack net zo goed een bouwblok kan heten, heeft precies
begrepen waar blad 2 om draait: een draaitabel is maar zo goed als de kolom
waarop ze gebouwd is.

## De controlegetallen

| Blad | Moet geven |
|---|---|
| 1 | eindtotaal 32 — evenveel als er mobs zijn |
| 2 | eindtotaal 32, onderste rij 4, 3, 19, 6 |
| 3 | eindtotaal 20.320. Staat er 30, dan telt de draaitabel stuks gereedschap in plaats van duurzaamheid |
| 4 | 22 updates, gemiddelde 28,18 |
| 5 | 131 aanbiedingen vóór de extra dorpeling, 143 erna |

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
- elke draaitabel verwijst naar velden die echt in die lijst staan, en op
  blad 5 groepeert op een kolom die ze eerst moeten aanvullen
- elke vraag **precies één** antwoord heeft — `antwoorden.py` faalt bij een
  gedeelde eerste plaats — en geen antwoord op twee bladen tegelijk staat
- de drie lessen van hierboven overeind blijven: gelijke aantallen op blad 3,
  een verschil tussen drukste en grootste op blad 4, lege vakjes op blad 2
- elke verwijzing naar de theorie een kaart 1 tot 9 is (grafiekkaarten horen
  hier niet)
- de opdracht nergens zelf theorie uitlegt
- de bundel op 50 punten en 50 minuten uitkomt

Getest door er drieëntwintig fouten in te spuiten — een onbekende dimensie,
een duurzaamheid die niet bij het materiaal hoort, een update buiten het
groepeerbereik, een filter dat alles of niets overlaat, twee beroepen met
hetzelfde werkblok, een draaitabel te dicht onder de lijst, een zoektabel
zonder dollartekens, hetzelfde antwoord op twee bladen, een verwijzing naar
een grafiekkaart, en meer.

Eenentwintig daarvan worden gevangen. De twee andere waren geen echte fout:
een gelijkspel om de tweede plaats op blad 5 (daar vraagt niemand naar) en een
filter dat 14 van de 22 updates overlaat (dat is gewoon een filter). In beide
gevallen had de controle gelijk en de test niet.

**Geen vaste rijnummers.** De plaats van elke draaitabel wordt uit de lengte
van de lijst afgeleid; zet je er een mob bij, dan schuift alles mee.
