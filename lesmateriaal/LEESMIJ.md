# Lesmateriaal buiten het portaal

Materiaal voor **echt Excel**, los van de webapplicatie. Elke map maakt zichzelf:
`gegevens.py` is de enige bron, de scripts bouwen het startbestand en de documenten,
en `controleer.py` faalt zodra opdracht, startbestand en sleutel uit elkaar lopen.

| Map | Wat | Voor wie | Duur |
|---|---|---|---|
| `excel-basis/` | 5 oefeningen + 15 functiefiches met schermbeelden | iedereen, als eerste | 50 min |
| `excel-herhaling/` | 7 korte oefeningen, 30 formules | wie de basis nog niet vlot heeft | 40 min |
| `excel-herhaling-2/` | idem, zelfde opbouw, andere wereld | wie na de eerste herhaling nog oefening nodig heeft | 40 min |
| `excel-uitdaging/` | Halloween-moordzaak, nieuwe functies, geneste formules | de sterkste leerlingen | 40 min |
| `excel-toets/` | synthesetoets op de basisfuncties, Rode Duivels | iedereen, als evaluatie | 50 min |
| `excel-slimste-mens/` | zelfstudiebundel op SOM, AANTAL.ALS en VERT.ZOEKEN | wie het nog niet vast heeft | 40 min |
| `excel-detective/` | vijf losse zaken, elk met één geneste functie | wie toe is aan iets meer | 5 × 25 min |
| `excel-ottomaans/` | basisfuncties, dan een draaitabel en een grafiek | hele klas, na de basis | 50 min |
| `excel-draaitabel/` | **theoriebundel**: 14 kaarten over draaitabel en grafiek | hoort bij `excel-ottomaans` | naslag |
| `moordzaak/` | detectivespel met Excel én papieren verhaallijn | hele klas, als spel | 50 min |

## Welke bundel hoort bij welke

- **`excel-basis` is de bron van de functiefiches** (`excel-functiebladen.docx`).
  Beide herhalingsbundels verwijzen ernaar in plaats van ze te herhalen — deel ze er
  dus altijd bij uit.
- **`excel-herhaling` en `excel-herhaling-2`** hebben met opzet dezelfde opbouw: blad 1
  is twee keer optellen in twee richtingen, blad 7 twee keer `VERT.ZOEKEN`. Herkenning
  is het punt.
- **`excel-uitdaging`** staat op zichzelf en brengt tien nieuwe kaarten mee. Het is geen
  zwaardere herhaling maar een ander soort opdracht: er staat nergens welke formule ze
  moeten typen.
- **`excel-toets`** is de evaluatie op `excel-basis`: alle tien de functies en alle vijf
  de hulpfiches in één bundel, op 50 punten. Hier staat géén formule in de opdracht, en
  de functiefiches gaan er niet bij.
- **`excel-slimste-mens` en `excel-detective` zijn gemaakt om alleen af te werken**,
  zonder leerkracht in de buurt. Daarom geven ze elke gewone formule letterlijk, heeft
  elk onderdeel een controlegetal of een proef, en staat er overal een lijstje "Loop je
  vast?" bij. De detectivezaken zijn de lichtere tegenhanger van `excel-uitdaging`: de
  moeilijkheid zit daar op één plaats per zaak in plaats van overal.
- **`excel-ottomaans` is de eerste bundel met een draaitabel.** Blad 1 tot 3 zijn
  herhaling van de basisfuncties, blad 4 en 5 zijn nieuw. Blad 2 en 3 zien er met
  opzet anders uit dan in alle vorige bundels — ze zijn bronlijst van een
  draaitabel en hebben dus geen totaalrij eronder maar een tellingenblokje
  ernaast. De opdracht legt uit waarom.
- **`excel-draaitabel` is de bron van de draaitabel- en grafiekkaarten**, zoals
  `excel-basis` dat is voor de functiefiches. Deel ze samen met `excel-ottomaans`
  uit. De bundel staat los van elke opdracht: de voorbeelden spelen in de
  schoolbibliotheek, de kantine en het schoolarchief, en `controleer.py` faalt
  zodra er een naam uit een andere bundel in opduikt.
- **`moordzaak`** is een spel, geen oefening op functies. Het kan op elk moment.

## Alles opnieuw bouwen

```bash
pip install openpyxl python-docx pillow
for d in excel-basis excel-herhaling excel-herhaling-2 excel-uitdaging \
         excel-toets excel-slimste-mens excel-detective excel-draaitabel \
         excel-ottomaans moordzaak; do
  (cd $d && for f in antwoorden.py maak-*.py controleer.py; do
     [ -f "$f" ] && python3 "$f" > /dev/null || true; done && echo "$d ok")
done
```

Elke map heeft een eigen `LEESMIJ.md` met de details.
