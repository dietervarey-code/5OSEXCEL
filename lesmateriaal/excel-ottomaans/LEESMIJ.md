# Excel — Het Ottomaanse Rijk

Vijf werkbladen, **50 minuten**. De eerste drie zijn herhaling van de
basisfuncties; blad 4 en 5 brengen voor het eerst de **draaitabel** en de
**grafiek** binnen.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `ottomaans-startbestand.xlsx` | leerlingen — zes bladen, bewust kaal |
| `ottomaans-opdracht.docx` | leerlingen — per blad wat ze maken, met controlegetal |
| `ottomaans-lerarensleutel.docx` | jou — alle uitkomsten, beide draaitabellen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — de nieuwe theorie |
| `../excel-basis/excel-functiebladen.docx` | leerlingen — de functiefiches die ze al kennen |

Deel **beide** bundels mee uit. De opdracht verwijst naar kaart 1 tot 9 voor
blad 4 en kaart 10 tot 14 voor blad 5.

## De opzet

| Nr | Blad | Duur | Rijen | Functies | Nieuw |
|---|---|---|---|---|---|
| 1 | Sultans | 8 min | 13 | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL`, `AANTAL.ALS` | — |
| 2 | Gebeurtenissen | 12 min | 35 | `VERT.ZOEKEN` (2×), `ALS`, `AANTAL.ALS` (3×) | — |
| 3 | Oorlogen | 10 min | 18 | `ALS`, `SOM`, `GEMIDDELDE`, `MAX`, `MIN`, `AANTAL.ALS`, `SOM.ALS` (2×) | — |
| 4 | Draaitabel | 12 min | — | geen | **twee draaitabellen** |
| 5 | Grafiek | 8 min | 8 | geen | **staafdiagram en lijndiagram** |

**Geen geneste functies.** Wat nieuw is, is nieuw genoeg. `controleer.py` faalt
op elke formule die een functie binnen een functie zet.

75 punten: 64 voor het werk en 11 voor de opmaak. Twee derde daarvan geeft een
score op 50.

## Waarom de bladen er zo uitzien

Blad 2 en 3 zijn **bronlijst van een draaitabel**, en dat verandert de indeling:

- geen totaalrij onder de lijst — die zou als gewone rij meegeteld worden
- geen lege rij in de lijst — daar stopt een draaitabel
- de tellingen staan **naast** de lijst, met precies één lege kolom ertussen

Dat is zelf een les: blad 2 en 3 zien er anders uit dan alle vorige bundels, en
de opdracht zegt waarom. `controleer.py` bewaakt alle drie.

## De draaitabel zit niet in het startbestand

`openpyxl` kan geen draaitabel schrijven. Dat komt goed uit — de leerling hoort
ze zelf te maken. Maar het betekent ook dat er **niets automatisch na te kijken
valt** aan blad 4. Daarom:

- `antwoorden.py` rekent beide draaitabellen cel voor cel uit
- de lerarensleutel drukt ze af als tabel, zodat je het blad ernaast kan leggen
- de vijf vragen op blad 4 worden wél in gewone cellen ingevuld
- het eindtotaal van draaitabel 2 is hetzelfde getal als de `SOM` die ze op
  blad 3 al berekenden — dat is het controlegetal

`controleer.py` telt beide draaitabellen een tweede keer na uit de ruwe
gegevens.

## Over de cijfers

De regeerperiodes, de gebeurtenissen en de oorlogen zijn gewone historische
gegevens. **De bevolkingscijfers op blad 5 zijn ruwe schattingen** — voor het
Ottomaanse Rijk bestaan er geen betrouwbare tellingen van vóór 1831 en de
getallen in de literatuur lopen fors uiteen. Dat staat op het startblad, in de
opdracht én in de sleutel. Ze dienen om mee te rekenen en om een lijn van te
tekenen.

Dertien van de zesendertig sultans staan in de lijst. Mehmed II heeft twee keer
geregeerd; hier staat zijn tweede, lange periode. Dat staat als voetnoot op
blad 1.

## De vallen

| Waar | Wat | Gevolg |
|---|---|---|
| blad 1 | Osman I regeerde precies 25 jaar, de grens zelf | wie `>` typt in plaats van `>=` komt op 8 in plaats van 9 |
| blad 1 | `AANTAL` op een kolom met namen | geeft 0 — `AANTAL` telt alleen getallen |
| blad 2 | de zoektabel niet vastzetten | `#N/B` onderaan kolom G |
| blad 3 | de Tweede Balkanoorlog duurde 0 jaar | wie dat "verbetert" sloopt zijn `MIN` en zijn `SOM` |
| blad 3 | `SOM.ALS` met de bereiken omgewisseld | geeft 0 |
| blad 4 | het waardeveld staat op Aantal | eindtotaal 18 in plaats van 171 |
| blad 5 | de kolom Jaar als reeks meenemen | twee lijnen in plaats van één |

Blad 2 telt met opzet **niet** de drukste eeuw en **niet** de vaakst
voorkomende soort: anders staat het antwoord van blad 4 er al. `controleer.py`
faalt zodra een antwoord dat ze van hun draaitabel moeten aflezen, elders als
criterium in een formule staat.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle uitkomsten en beide draaitabellen
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` dekt 202 te maken cellen, 368 gegeven cellen, 48 cellen van
draaitabel 1 en 9 regels van draaitabel 2, en kijkt verder na of:

- elke gebeurtenis binnen de regeerperiode van zijn sultan valt
- de twee bronlijsten geschikt zijn voor een draaitabel
- de twee draaitabellen elkaar niet in de weg zitten op het blad
- elk controlegetal uit de opdracht echt uit de antwoorden komt
- er nergens een geneste functie in de sleutel staat
- de duur van de bladen optelt tot de aangekondigde 50 minuten

Er staan **geen vaste rijnummers** in de controle: alles komt uit
`gegevens.py`. Voeg je daar een sultan, een gebeurtenis of een oorlog bij, dan
schuift de rest mee en worden alle getallen opnieuw berekend.
