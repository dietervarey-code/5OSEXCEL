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
- **`moordzaak`** is een spel, geen oefening op functies. Het kan op elk moment.

## Alles opnieuw bouwen

```bash
pip install openpyxl python-docx pillow
for d in excel-basis excel-herhaling excel-herhaling-2 excel-uitdaging moordzaak; do
  (cd $d && for f in antwoorden.py maak-*.py controleer.py; do
     [ -f "$f" ] && python3 "$f" > /dev/null || true; done && echo "$d ok")
done
```

Elke map heeft een eigen `LEESMIJ.md` met de details.
