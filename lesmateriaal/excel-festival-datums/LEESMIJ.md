# Excel — de planning van Zomerklank

Vijf werkbladen, **50 minuten, 50 punten**. Zeven datumfuncties
en twee menuhandelingen, met een tijdlijn als slot.

De zusterbundel van **`excel-festival-tekst`**: zelfde festival, zelfde opbouw.
Daar kuisen ze de line-up op met tekstfuncties en eindigt blad 5 op een
slicer; hier rekenen ze met de datums en eindigt blad 5 op een tijdlijn. De
twee kunnen in elke volgorde en staan allebei op zichzelf.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `festival-datums-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `festival-datums-opdracht.docx` | leerlingen — per blad wat ze maken, **plus de 9 fiches** |
| `festival-datums-lerarensleutel.docx` | jou — alle kolommen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — alleen voor blad 5 |

De theorie staat **in de opdracht zelf**; voor blad 5 hebben ze het boekje
nodig dat ze al hebben (kaart 3, 4, 8 en 13 — vooral kaart 8, het groeperen).

## De opbouw

| Nr | Blad | Dataset | Wat nieuw is | Fiches | Duur | Pt |
|---|---|---|---|---|---|---|
| 1 | Voorbereiding | 12 voorbereidingstaken | een datum is een getal: aftrekken geeft dagen | 1 | 8 min | 7 |
| 2 | Vrijwilligers | 16 vrijwilligers | `DATUMVERSCHIL` voor leeftijd, en één keer `VANDAAG` | 3, 2 | 10 min | 10 |
| 3 | Ticketverkoop | 18 verkoopdagen | `MAAND`, `WEEKDAG` — en waarom die `;2` ertoe doet | 4, 5 | 10 min | 10 |
| 4 | Opbouw | 12 opbouwtaken | `WERKDAG` en `NETTO.WERKDAGEN`: rekenen zonder weekends | 7, 6 | 12 min | 11 |
| 5 | Verkoop per maand | 37 verkoopregels | Ctrl+T, draaitabel per maand, draaigrafiek, **tijdlijn** | 8, 9 | 10 min | 12 |

**Blad 4 is het zwaarste.** `WERKDAG` en `NETTO.WERKDAGEN` lijken op elkaar en
doen het omgekeerde van elkaar: de eerste geeft een datum, de tweede een
aantal. Zet ze één keer naast elkaar op het bord.

## De peildatum

Rechtsboven op elk blad staat **17/07/2026**, de eerste festivaldag. Daar wordt
overal op gerekend, niet op `VANDAAG()`. Twee redenen:

1. anders verandert elk antwoord elke dag en kan jij niets nakijken;
2. het is ook gewoon hoe het hoort — je rekent naar een deadline toe, niet
   naar vandaag.

`VANDAAG()` komt één keer aan bod, in één losse cel op blad 2, en daar staat
met zoveel woorden bij dat het antwoord elke dag anders is. Die cel heeft
**geen vast antwoord**: kijk alleen of er een formule staat.

Dat de peildatum met dollartekens vastgezet moet worden, is in deze bundel
verreweg de meest gemaakte fout. Herkenbaar aan een kolom die bovenaan klopt
en onderaan niet, of aan een kolom "Op tijd?" die overal hetzelfde zegt.

## Waarom juist deze gegevens

- **Twee vrijwilligers zijn in de festivalweek jarig.** Amina De Smet is
  op 17/07/2026 jarig en dus al 18;
  Noor Janssens is de dag erna jarig en nog 17. Eén dag
  scheelt een heel jaar, en dat is precies waarom je `DATUMVERSCHIL` nodig
  hebt en niet "delen door 365".
- **Precies één opbouwtaak komt te laat**: Licht en geluid Main, klaar op
  20/07/2026. `controleer.py` bewaakt dat het er één blijft
  — geen enkele of twee, en de hele kolom zegt niets meer.
- **Bij de meeste opbouwtaken valt er een weekend in de looptijd.** Was dat
  niet zo, dan gaf gewoon optellen hetzelfde antwoord en leerde `WERKDAG`
  niets. Ook dat wordt bewaakt.
- **Blad 5 is dezelfde verkoop als blad 3, uitgesplitst per kanaal.** De
  dagtotalen moeten dus kloppen, en het eindtotaal van de draaitabel
  (16.870) is precies de som van blad 3. `controleer.py`
  vergelijkt ze dag per dag. Wie dat zelf opmerkt, heeft goed gekeken.
- **10 van de 18 verkoopdagen vielen in het
  weekend.** Vergeet een leerling de `;2` bij `WEEKDAG`, dan komt hij op een
  ander getal uit — en dat is het enige wat hem verraadt.

## De controlegetallen

| Blad | Moet geven |
|---|---|
| 1 | langste taak Campagne online met 102 dagen; van 12/01/2026 tot 16/07/2026 is 185 dagen |
| 2 | 8 van de 16 mogen achter de bar |
| 3 | 10 weekenddagen; drukste dag 04/07/2026 (zaterdag, nummer 6) |
| 4 | precies één keer "nee" in kolom F: Licht en geluid Main |
| 5 | eindtotaal 16.870; beste maand mei; met de tijdlijn op juni blijft 4.310 over |

## Over de gegevens

Zomerklank bestaat niet en de planning is verzonnen. **De kalender wel**:
17/07/2026 is echt een vrijdag en elke weekdag die ze uitrekenen klopt met de
echte kalender. Dat moet ook, anders valt er niets mee te rekenen.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle kolommen uitgerekend
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` kijkt na of:

- de **kalenderhulpjes doen wat Excel doet**: `netto_werkdagen` wordt tegen
  een tweede, trage implementatie gelegd; `werkdag` moet een weekdag geven
  met precies het gevraagde aantal werkdagen na de start; en wie op de
  peildatum jarig is, moet al een jaar ouder zijn
- elke datum in het startbestand een **echte datum** is met datumnotatie —
  staat er tekst, dan werkt geen enkele formule en blijft de tijdlijn grijs
- **elke verwijzing naar de peilrij de vastgezette peildatum is** ($G$1
  en niet G1)
- de les overeind blijft: precies één late taak, weekends in de looptijd,
  weekenddagen in de verkoop, meer dan drie maanden om te groeperen
- blad 3 en blad 5 dag per dag dezelfde verkoop beschrijven
- elke functie een fiche heeft en naar elke fiche verwezen wordt
- het startbestand geen tabel, geen grafiek en geen draaitabel bevat
- de bundel op 50 punten en 50 minuten uitkomt

Getest door er zestien fouten in te spuiten — een peildatum die geen vrijdag
is, een `werkdag` die de startdag meetelt, een `netto_werkdagen` die de
einddag vergeet, een leeftijd die op de verjaardag een jaar achterloopt, nul
of twee late taken, datums als tekst, een peildatum zonder dollartekens, een
functie zonder fiche. Alle zestien worden gevangen.
