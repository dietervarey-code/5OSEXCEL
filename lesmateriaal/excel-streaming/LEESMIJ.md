# Excel — Wat kijkt 5OS?

Vijf werkbladen, **50 minuten**. Tweede bundel rond draaitabellen, met dezelfde
opbouw als `excel-ottomaans/` maar in een wereld die dichter bij hen staat: een
streamingaanbod en een enquête over schermtijd.

Herkenning is het punt. Wie de Ottomaanse bundel gemaakt heeft, ziet blad voor
blad hetzelfde soort werk en kan sneller. Eén ding is nieuw, en dat is met
opzet het enige: **draaitabel 2 heeft twee waardevelden en moet op Gemiddelde
staan in plaats van op Som.**

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `streaming-startbestand.xlsx` | leerlingen — zes bladen, bewust kaal |
| `streaming-opdracht.docx` | leerlingen — per blad wat ze maken, met controlegetal |
| `streaming-lerarensleutel.docx` | jou — alle uitkomsten, beide draaitabellen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — de theorie, ongewijzigd |
| `../excel-basis/excel-functiebladen.docx` | leerlingen — de functiefiches die ze al kennen |

## De opzet

| Nr | Blad | Duur | Rijen | Functies | Nieuw |
|---|---|---|---|---|---|
| 1 | Genres | 8 min | 9 | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | — |
| 2 | Aanbod | 12 min | 35 | `VERT.ZOEKEN` (2×), `ALS`, `GEMIDDELDE`, `AANTAL`, `AANTAL.ALS` (2×) | — |
| 3 | Schermtijd | 10 min | 20 | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL.ALS`, `SOM.ALS` (2×) | — |
| 4 | Draaitabel | 12 min | — | geen | **twee draaitabellen van dezelfde lijst** |
| 5 | Grafiek | 8 min | 10 | geen | **staafdiagram en lijndiagram** |

**Geen geneste functies.** 75 punten: 64 voor het werk en 11 voor de opmaak.
Twee derde daarvan geeft een score op 50 — net als bij de vorige bundel.

## Wat echt is en wat verzonnen

Dit is het enige waar je bij het uitdelen iets over moet zeggen.

- **De titels, de taal en het jaar van verschijnen kloppen.** Dat mag nagekeken
  worden en dat is ook leuk om te doen.
- **De indeling in genres is onze keuze.** Veel titels passen in meer dan één
  genre. Een leerling die vindt dat *Parasite* eerder drama dan thriller is,
  heeft gelijk én ongelijk — en dat is zelf een les: een draaitabel is maar zo
  goed als de kolom waarop je ze bouwt.
- **Alle aantallen zijn verzonnen.** Er is geen peiling over lievelingsgenres
  geweest, geen enquête over kijkers en geen meting van schermtijd. De
  schermtijdreeks op blad 5 heeft wél de vorm die echt onderzoek laat zien (een
  sprong in 2020 die niet helemaal terugzakt), maar het zijn onze cijfers.

Dat staat op het startblad, in de opdracht en in de sleutel.

## De pointe van blad 4

Draaitabel 2 zet per taal het aantal titels naast het gemiddelde aantal
kijkers:

| Taal | Titels | Gemiddeld |
|---|---|---|
| Koreaans | 2 | 245 |
| Spaans | 4 | 150 |
| Japans | 2 | 135 |
| **Engels** | **18** | **133,33** |
| … | | |
| Noors | 1 | 60 |
| **Eindtotaal** | **35** | **136** |

Engels heeft meer dan de helft van alle titels en staat toch pas vierde. Dat is
de hele les in één tabel: *veel* en *populair* zijn niet hetzelfde, en je ziet
het verschil pas als je dezelfde lijst op twee manieren samenvat.

Nuanceer het ook meteen de andere kant op: Koreaans haalt dat gemiddelde uit
twee titels die allebei toevallig grote successen zijn. Een gemiddelde over
twee waarnemingen zegt weinig. Die tegenwerping staat in de sleutel.

`controleer.py` bewaakt deze pointe: zodra de taal met de meeste titels ook die
met het hoogste gemiddelde wordt, faalt het script.

## De controlegetallen

| Blad | Cel | Moet geven |
|---|---|---|
| 1 | totale groei | 108, gemiddelde precies 12 |
| 2 | gemiddeld aantal kijkers | 136 — dit is meteen de controle voor draaitabel 2 |
| 3 | som | 26500, gemiddelde precies 1325 |
| 4 | eindtotaal draaitabel 1 | 35, evenveel als er titels zijn |
| 4 | rij Eindtotaal draaitabel 2 | 136, hetzelfde getal als op blad 2 |
| 5 | som van de verschilkolom | 95 = 190 − 95 |

Staat er bij draaitabel 2 **4760**, dan staat het waardeveld op Som; staat er
**35**, dan op Aantal.

## De vallen

| Waar | Wat | Gevolg |
|---|---|---|
| blad 1 | drie genres groeien met precies 15, de grens zelf | `>` in plaats van `>=` geeft 2 in plaats van 5 |
| blad 1 | Avontuur krimpt met −2 | wie dat "verbetert" sloopt SOM, gemiddelde én MIN |
| blad 1 | `AANTAL` op een kolom met namen | geeft 0 |
| blad 2 | de zoektabel niet vastzetten | `#N/B` onderaan kolom G |
| blad 3 | twee leerlingen zitten op precies 1500 | `>` geeft 6 in plaats van 8 |
| blad 3 | `SOM.ALS` met de bereiken omgewisseld | geeft 0 |
| blad 4 | het waardeveld staat op Som | eindtotaal 4760 in plaats van 136 |
| blad 5 | de kolom met het aantal titels meeselecteren | twee reeksen in het staafdiagram |
| blad 5 | de rij Eindtotaal meeselecteren | één reusachtige balk |

Blad 2 telt met opzet **niet** het genre of de taal die op blad 4 het antwoord
zijn. `controleer.py` faalt zodra dat toch gebeurt.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle uitkomsten en beide draaitabellen
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` dekt 199 te maken cellen, 346 gegeven cellen, 18 cellen van
draaitabel 1 en 8 regels van draaitabel 2, en kijkt verder na of:

- elke genrecode uit het aanbod in de genretabel staat, en elk genre en elke
  taal uit de lijsten ook echt in het aanbod voorkomt
- geen enkele titel meer kijkers heeft dan er leerlingen op de verzonnen school
  zitten
- de bronlijsten geschikt zijn voor een draaitabel
- elke vraag op blad 4 en 5 precies één antwoord heeft — geen twee genres die
  de eerste plaats delen, geen twee even grote jaarsprongen
- de grensvallen op blad 1 en 3 er nog in zitten
- elk controlegetal uit de opdracht echt uit de antwoorden komt
- er nergens een geneste functie in de sleutel staat

Er staan **geen vaste rijnummers** in de controle: alles komt uit
`gegevens.py`. Voeg je een titel toe, dan schuift de rest mee en worden alle
getallen opnieuw berekend — ook de draaitabellen in de sleutel.
