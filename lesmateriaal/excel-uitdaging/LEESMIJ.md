# Halloween op Kasteel Ravenstein — uitdagingsopdracht

Eén avond, vijf werkbladen, 40 minuten in **echt Excel**.
Voor leerlingen die `lesmateriaal/excel-basis/` en de herhalingsbundels vlot afwerken
en meer willen.

Dit is **geen zwaardere versie van de herhaling**. Het is een ander soort opdracht:
er staat nergens welke formule ze moeten typen, alleen wat eruit moet komen en met
welke functie. Geneste functies mogen, en op sommige plaatsen moet het.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `halloween-startbestand.xlsx` | leerlingen — zes werkbladen, bewust kaal |
| `halloween-opdracht.docx` | leerlingen — de situatie, tien kaarten *Nieuw gereedschap*, één pagina per werkblad |
| `halloween-lerarensleutel.docx` | jou — de ontknoping, alle formules, de uitkomsten en de veelgemaakte fouten |

De functiefiches van de basisbundel hoeven er niet bij, maar laat ze beschikbaar:
de tien basisfuncties worden hier als gekend beschouwd.

## Het verhaal

31 oktober. De leerling is coördinator van de Halloweennacht op het kasteel. De
avond is voorbij en er zijn twee dingen te doen: de avond afsluiten, en uitzoeken
wie de **Zilveren Pompoen** uit de schatkamer meenam. Vijf getuigenverklaringen
staan bij werkblad 4; samen worden ze één formule, en die laat precies één naam
overeind.

> **De dader is Ella Lammens**, gids in het doolhof.
> Zij is bewust géén lid van de nachtploeg die ze op werkblad 3 berekenen — wie die
> lijst als verdachtenlijst gebruikt, sluit net de dader uit.

## De vijf werkbladen

| Nr | Werkblad | Wat erin zit | Duur |
|---|---|---|---|
| 1 | Boekingen | `VERT.ZOEKEN` met **WAAR** (staffel), `SOMMEN.ALS`, `AANTALLEN.ALS`, `GEMIDDELDE.ALS`, `INDEX`+`VERGELIJKEN` | 12 min |
| 2 | Attracties | kruistabel, `INDEX`+`VERGELIJKEN` (ook zijwaarts), `GROOTSTE` | 7 min |
| 3 | Ploegen | rekenen met tijden, `ALS` met `EN`, `AANTALLEN.ALS`, `GEMIDDELDE.ALS` | 8 min |
| 4 | Verdachten | `VERT.ZOEKEN` naar een ander werkblad, `ALS` met vijf voorwaarden in `EN` | 9 min |
| 5 | Afrekening | verwijzingen over de bladen heen, `AFRONDEN`, percentage | 4 min |

36 formules in totaal. De bladen hangen aan elkaar: 4 heeft 3 nodig, 5 heeft 1 én 3.

**De ruggengraat is 1 → 3 → 4.** Kom je tijd tekort, dan is werkblad 2 het eerste dat
mag wegvallen (het staat helemaal los) en werkblad 5 het tweede. Werkblad 4 is de
ontknoping: laat dat nooit vallen.

## Nieuw gereedschap

De opdrachtbundel bevat tien kaarten met uitleg, varianten, veelgemaakte fouten en
negen getekende schermbeelden:

`VERT.ZOEKEN` met WAAR · `SOMMEN.ALS` · `AANTALLEN.ALS` · `GEMIDDELDE.ALS` ·
`EN`/`OF` binnen `ALS` · geneste functies · `INDEX`+`VERGELIJKEN` ·
`GROOTSTE`/`KLEINSTE` · rekenen met tijden · verwijzen naar een ander werkblad

Net als bij de functiefiches van de basisbundel spelen **alle voorbeelden in een
eigen wereldje** — een rapport, een fruithandel, een uurrooster. `controleer.py`
weigert elke kaart die een naam, een groep, een attractie of een bladnaam uit het
startbestand bevat, of die letterlijk een formule uit de sleutel toont.

## Wat er bewust in zit

- **De staffel op blad 1** gebruikt alle vier de schijven. Zie je in kolom F maar drie
  verschillende prijzen, dan zit er een fout in het benaderend zoeken.
- **`SOMMEN.ALS` begint met het optelbereik**, `GEMIDDELDE.ALS` niet. Eén blad, twee
  volgordes — dat is de val van blad 1.
- **Twee mensen stoppen precies om 22:30**, de grens van de nachtploeg. Wie `>=`
  gebruikt waar de omschrijving *later dan* zegt, krijgt er twee te veel.
- **Eén iemand werkt precies 4 uur** maar stopt te vroeg. Hij toont waarom het `EN`
  moet zijn en geen `OF`.
- **De controle van blad 5** is de beste van de bundel: verander op blad 3 één einduur
  en de winst moet meteen meebewegen. Doet ze dat niet, dan is er een getal overgetypt.

## De bestanden opnieuw maken

```bash
pip install openpyxl python-docx pillow
python3 antwoorden.py         # toont alle uitkomsten en waarom elke verdachte afvalt
python3 maak-startbestand.py
python3 maak-documenten.py    # tekent ook de negen schermbeelden in beelden/
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt veertien dingen, waaronder:

- elke cel die als *te maken* opgegeven staat, is leeg in het startbestand; elke cel
  die als *gegeven* opgegeven staat, is gevuld
- **de opdrachttekst bevat nergens een formule** — dat is het verschil met de
  basisbundel
- geen enkele kaart lekt gegevens uit het startbestand of toont een oplossing
- de staffel loopt op, begint laag genoeg, en alle schijven worden gebruikt
- nergens een gelijkspel aan de top, zodat `INDEX`+`VERGELIJKEN` één antwoord heeft
- iemand zit precies op de tijdsgrens, iemand precies op de urengrens
- geen enkele dienst loopt over middernacht
- elke verdachte staat in de ploegenlijst, en **precies één** blijft over
- elke verklaring sluit minstens één verdachte uit — anders staat ze er voor niets

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
`schermbeeld.py` is een kopie van die uit `excel-basis`, met een formulebalk die
meegroeit met lange formules.
