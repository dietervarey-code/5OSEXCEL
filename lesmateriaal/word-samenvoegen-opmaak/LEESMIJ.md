# Word — vier soorten samenvoegen, en de opmaak erbij

**5 lesuren, vijf stappen, 100 punten, waarvan 37 op de opmaak alleen.**
Vervolg op `word-samenvoegen`. Daar lag het werk in Excel: de lijst
samenvoegklaar maken met `TEKST`, `&` en `ALS`. Hier **hoeft er niets
uitgerekend te worden** — de drie lijsten staan helemaal klaar. Elke minuut
gaat naar Word: samenvoegen en lay-outten.

Thema: **KSV Zonneveld**, een voetbalclub met 26 leden en een jeugdtornooi.

## Wat je uitdeelt

| Bestand | Voor wie | Wanneer |
|---|---|---|
| `samenvoegen-opmaak-startbestand.xlsx` | leerlingen | elke stap |
| `samenvoegen-opmaak-opdracht.docx` | leerlingen | de hele reeks |
| `samenvoegen-opmaak-theorie.docx` | leerlingen — **8 fiches, 14 tot 21** | de hele reeks |
| `samenvoegen-opmaak-brief-leden.docx` | leerlingen | stap 3 |
| `samenvoegen-opmaak-brief-tornooi.docx` | leerlingen | stap 5 |
| `samenvoegen-opmaak-lerarensleutel.docx` | jou | — |

De theoriebundel van de vorige reeks (`samenvoegen-theorie.docx`, fiches 1 tot
13) hebben ze erbij nodig: deze fiches gaan verder waar die stopten en
verwijzen er zeven keer naar. De nummering loopt daarom door vanaf 14.

## De vier soorten

Word kent vijf soorten samenvoegdocumenten. Ze doen er hier **vier** van.
E-mailberichten laat ik met opzet vallen: dat vraagt een mailaccount in Word
en levert didactisch niets nieuws op.

| Stap | Soort | Wat ze maken | Lesuren | Fiches | Pt (waarvan opmaak) |
|---|---|---|---|---|---|
| 1 | Etiketten | 26 lidkaarten, 14 per blad | 1 | 16 | 20 (8) |
| 2 | Enveloppen | 9 enveloppen, gefilterd | 1 | 14 | 15 (5) |
| 3 | Brieven | 26 brieven met een tabel | 1 | 17, 18, 19, 20 | 25 (12) |
| 4 | Lijst | één ploeglijst op één blad | 1 | 15 | 15 (4) |
| 5 | Alles samen | de tornooibrief + lijst + enveloppen | 1 | 14, 15, 17, 19, 21 | 25 (8) |

## Waar het in deze bundel echt om gaat

Niet om de knop. Die kennen ze na de vorige reeks. Het gaat om **de twee
dingen die ze fout doen zodra het eruit moet zien als post**:

1. **Spaties zijn geen tabstops.** Ze zetten de datum rechts door er
   vijfendertig keer op de spatiebalk te drukken. Bij de volgende naam staat
   hij weer scheef, want «Voornaam» is niet overal even lang. Stap 3 geeft
   daar 4 punten voor, en fiche 17 legt uit waarom. Dit is de reden dat de
   bundel bestaat.
2. **Opmaak hoort bij de plaats, niet bij de tekst.** Op een etiket maak je de
   **eerste** kaart op en dan klik je Labels bijwerken. Doen ze het omgekeerd,
   dan is alleen kaart 1 mooi. Voordoen op het bord, één keer, fout.

De derde is de valkuil van stap 4: bij een **Lijst** herhaalt Word het
**hele document** per record, niet één blad. Zetten ze de koprij in het
hoofddocument, dan staat die er zeven keer. De koprij hoort in het
samengevoegde **resultaat**.

## De opmaak wordt apart gequoteerd

Bij elke stap staan twee lijstjes met een eigen puntentelling: *het
samenvoegwerk* en *de opmaak*. Zo kan je het samenvoegen goedrekenen en de
lay-out niet, zonder discussie. De 37 opmaakpunten liggen zo:

| Stap | Waarop |
|---|---|
| 1 | vier regels op de kaart, elk met een eigen grootte, vet en kleur (8) |
| 2 | afzender linksboven klein, geadresseerde rechtsonder groot (5) |
| 3 | briefhoofd, **de datum met een tabstop op 16 cm**, de tabel zonder randen, de voettekst (12) |
| 4 | koprij in het resultaat, de tabel leesbaar (4) |
| 5 | de hele lay-out van de tornooibrief is hun werk (8) |

Elke opmaakeis staat uitgeschreven: niet "maak het netjes", maar "regel 2:
14 pt, vet, zwart, gecentreerd". `controleer.py` weigert een voorschrift van
minder dan veertig tekens.

## De twee briefmodellen zijn met opzet lelijk

Alles links, één lettergrootte, geen tabstops, geen tabel, geen uitlijning.
De tekst staat er al — die hoeven ze niet te typen — maar **de lay-out is de
oefening**, dus die zit er niet in.

- `samenvoegen-opmaak-brief-leden.docx` heeft oranje `[[markers]]` tussen
  dubbele haken op de plaatsen waar een samenvoegveld hoort (stap 3).
- `samenvoegen-opmaak-brief-tornooi.docx` heeft **geen** markers en **geen**
  aanwijzingen over de vorm. Dat is de eindopdracht.

`controleer.py` leest die twee bestanden na en eist dat er in de brief zelf
geen lettergrootte, geen tab en geen uitlijning staat. Zodra ik per ongeluk
iets voordoe, valt de checker erover.

## Over het startbestand

Drie bladen die Word leest — `Leden` (15 kolommen × 26 rijen), `Tornooi`
(10 × 14) en `Antwoorden` — en een blad `Start` met de uitleg.

De lijsten bevatten **niets anders dan de lijst**: koprij op rij 1, geen
titel erboven, geen losse cel ernaast, geen samengevoegde cellen. Dat is geen
netheid. Word neemt de eerste gebruikte rij van een werkblad als kolomnamen,
en een titel erboven maakt de hele samenvoeging stuk.

Twee kolommen staan er twee keer in: `Lidgeld` (een getal met euronotatie) en
`Lidgeld in tekst` (de tekst `€ 180,00`). Dat is de les van de vorige reeks,
hier als herinnering: **voeg je het getal samen, dan staat er 180 in de
brief.** In de brief gebruiken ze de tekstkolom. Idem voor `Trainingsuur` en
`Vervaldatum in tekst`.

## De controlegetallen

| Waar | Moet geven |
|---|---|
| stap 1 | 14 kaarten per blad, 2 bladen, 2 leeg op het laatste |
| stap 2 | 9 enveloppen met het filter Betaald = nee, 26 zonder |
| stap 2 | laatste envelop: El Amrani |
| stap 3 | 26 brieven; bij Jonas Peeters € 180,00; Bilal Claes traint vrijdag |
| stap 3 | de aanmaningszin in 9 brieven |
| stap 4 | 7 regels in de lijst van U15, bovenaan Bogaerts |
| stap 5 | 5 clubs in categorie U15; 4 clubs met de extra zin; totaal € 1.120,00 |

Snelle test voor stap 3: zoek in het samengevoegde document op het woord
*vervaldatum*. Dat moet 9 keer voorkomen.

De vier vragen van stap 1 en 2 zijn geen leesvragen: de laatste van stap 1
vraagt om het **in de verkeerde volgorde te proberen** en te tellen hoeveel
kaarten er dan opgemaakt zijn (antwoord 1), en stap 2 vraagt naar de
**laatste** envelop, niet naar de eerste — die staat als voorbeeld in de
opdracht.

## Hoeveel lesuren echt?

Op papier **5**. Reken er **6** als je de eindopdracht ook degelijk wil
quoteren. Stap 2 is het uur dat je kan laten vallen: een envelop is de
makkelijkste van de vier en voegt na de etiketten weinig nieuws toe.

Stap 4 zou ik **niet** laten vallen. Een Lijst-samenvoeging is de enige soort
die ze nergens anders tegenkomen, en de valkuil ervan (het hele document
herhaalt) begrijpen ze alleen door hem één keer te zien.

## Wat je met het oog moet nakijken

De sleutel schrijft alle getallen en alle regels uit, maar opmaak kan geen
script nakijken. Vraag per stap twee dingen: het **hoofddocument** (klik in
een veld — het wordt grijs, of Alt+F9) en het **samengevoegde document**.
Kijk in de afdrukweergave, met de zoom op één volledige pagina. Dan zie je in
drie seconden of de datum met spaties rechtgezet is.

Een samenvoegveld schrijft `python-docx` niet zinvol: een `MERGEFIELD` kan
wel, maar de verwijzing naar de gegevensbron is een pad op één bepaalde
computer. Dat overleeft het uitdelen niet — en de velden invoegen is net de
oefening.

## Over de gegevens

KSV Zonneveld bestaat niet, en de leden en de trainers evenmin. De gemeenten
bestaan wel; de huisnummers zijn willekeurig. Het rekeningnummer is een
testnummer. Wat wél echt is: het etiketformaat (Avery L7163, 14 per blad,
99,1 × 38,1 mm), het envelopformaat (DL, 110 × 220 mm) en de manier waarop
een club haar post maakt.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py          # alle kaarten, adressen, brieven en lijsten uitgerekend
python3 oefeningen.py          # de puntentelling per stap
python3 fiches.py              # de inhoud van de theoriebundel
python3 maak-startbestand.py
python3 maak-documenten.py     # vijf documenten in één keer
python3 controleer.py
```

`controleer.py` kijkt na of:

- **elk veld dat in een opmaakvoorschrift genoemd wordt een kolom is die echt
  bestaat** — op de lidkaart, op de envelop, in de brief, in de tabel en in
  de lijst. Een voorschrift dat naar «Roepnaam» verwijst, stuurt de leerling
  naar een veld dat Word niet kent
- de drie bladen **samenvoegklaar** zijn: koprij op rij 1, niets buiten de
  lijst, geen samengevoegde cellen, geen tabel, geen lege rij, geen twee
  kolommen met dezelfde naam en geen kolomnaam met tekens waar Word over
  struikelt
- de ledenlijst **volledig** klaarstaat: alle 390 cellen vergeleken met
  `antwoorden.py`, en de kolom `Lidgeld` met euronotatie, want zonder die
  opmaak ziet de leerling het verschil met de tekstkolom niet
- de **briefmodellen geen opmaak bevatten**: geen lettergrootte, geen tab,
  geen uitlijning, geen tweede tabel — anders is de oefening weg
- de `[[markers]]` in de ledenbrief precies de verwachte kolommen zijn, en de
  tornooibrief er **geen enkele** heeft
- geen enkele lettergrootte onder 8 punten zakt en de vier regels van de
  lidkaart samen op 38 mm passen
- **de les overeind blijft**: een filter dat echt iets wegfiltert (9 van 26),
  een regel die niet voor iedereen geldt (9 van 26), etiketbladen die niet
  precies vollopen, ploegen met een verschillend lidgeld en trainingsuren die
  niet allemaal op een heel uur vallen
- **geen enkel tekstantwoord elders in diezelfde stap te lezen staat** — en
  dat het voorbeeld van stap 4 over een **andere** ploeg gaat dan de oefening,
  anders staan het aantal regels en de bovenste naam al in de opdracht
- elke fiche gebruikt wordt, de nummering op het eerste boekje aansluit, en
  elk opmaakvoorschrift concreet genoeg is
- de bundel op 100 punten en 5 lesuren uitkomt, met minstens een kwart op de
  opmaak

Getest met **eenentwintig ingespoten fouten**: een veld dat geen kolom is, een
letter van 6 punten, alle regels even groot, een filter dat niemand
wegfiltert, een tabstop op 24 cm, een dubbele kolomnaam, een marker zonder
kolom, een lijstkolom zonder kolom, een voorbeeld over dezelfde ploeg als de
oefening, de punten die niet op 100 komen, een opmaakvoorschrift "mooi maken",
een antwoord dat in de opdracht zelf te lezen staat, een fichenummering die
niet aansluit, een notitie onder de lijst, een antwoord dat al ingevuld staat,
samengevoegde cellen, en vier keer opmaak die ik per ongeluk in een briefmodel
voordeed (een lettergrootte, een tab, een uitlijning). Alle eenentwintig
worden gevangen; twee ervan door een leesbare foutmelding uit `antwoorden.py`
zelf in plaats van door de checker.
