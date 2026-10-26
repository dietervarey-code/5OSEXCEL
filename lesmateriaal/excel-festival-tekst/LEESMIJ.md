# Excel — de line-up van Zomerklank opkuisen

Vijf werkbladen, **50 minuten, 50 punten**. Negen tekstfuncties
en drie menuhandelingen. Geen draaitabellen behalve op het slotblad, geen
herhaling van de basisfuncties.

Gemaakt als vervolg op de draaitabel- en grafiekbundels, voor wie daar
voorbij is. Dit is de vaardigheid waar op een werkvloer het meeste tijd in
gaat zitten: je krijgt een export die niet deugt en je maakt er een lijst van
waar je iets mee kan.

**De zusterbundel is `excel-festival-datums`**: zelfde festival, zelfde opbouw,
maar dan met de datums. Daar eindigt blad 5 op een tijdlijn in plaats van een
slicer. De twee kunnen in elke volgorde.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `festival-tekst-startbestand.xlsx` | leerlingen — zes bladen, vijf lijsten klaar |
| `festival-tekst-opdracht.docx` | leerlingen — per blad wat ze maken, **plus de 12 fiches** |
| `festival-tekst-lerarensleutel.docx` | jou — alle kolommen uitgeschreven |
| `../excel-draaitabel/draaitabellen-en-grafieken.docx` | leerlingen — alleen voor blad 5 |

Anders dan bij de draaitabelbundels staat de theorie **in de opdracht zelf**.
Dit is een nieuw onderwerp, dus er is geen apart boekje — net zoals bij
`excel-basis` en `excel-uitdaging`. Het boekje dat ze al hebben, is alleen
nodig voor de draaitabel en de draaigrafiek van blad 5 (kaart 3, 4 en 13).

## De opbouw

| Nr | Blad | Dataset | Wat nieuw is | Fiches | Duur | Pt |
|---|---|---|---|---|---|---|
| 1 | Artiestcodes | 16 artiestcodes | `LINKS`, `RECHTS`, en dat geknipte tekst géén getal is | 1, 2 | 8 min | 8 |
| 2 | Podia | 18 systeemregels | `VIND.ALLES` en `LENGTE`: knippen zonder vaste lengte | 3, 4, 1 | 12 min | 11 |
| 3 | Boekingscodes | 20 boekingscodes | `DEEL`: een stuk uit het midden | 5, 2 | 10 min | 9 |
| 4 | Vrijwilligers | 16 vrijwilligers | `SPATIES.WISSEN`, `BEGINLETTERS`, `SUBSTITUEREN`, plakken met `&` | 6, 7, 8, 9 | 10 min | 8 |
| 5 | Line-up | 26 line-upregels | Duplicaten verwijderen, Ctrl+T, draaitabel, draaigrafiek, slicer | 10, 11, 12 | 10 min | 14 |

**Blad 2 is het moeilijkste en staat met opzet vooraan.** Wie
`=RECHTS(A4;LENGTE(A4)-VIND.ALLES("|";A4)-1)` rond krijgt, heeft de rest ook.
Blad 3 lijkt zwaarder maar is lichter: daar hoeft niets gezocht te worden,
want elke boekingscode telt precies 16 tekens. Zeg dat erbij,
anders schrikken ze van de code.

**Blad 5 heeft geen enkele formule.** Ze kuisen de export op, maken er een
tabel van en zetten er een draaitabel, een draaigrafiek en een slicer op. Dat
sluit meteen het open eindje van kaart 9 uit de draaitabelbundel: een tabel
groeit wél mee als er een rij bijkomt.

## Waarom juist deze gegevens

- **Blad 1 heeft een kolom die overbodig lijkt.** Kolom D is het jaar zoals
  `RECHTS` het teruggeeft, kolom E hetzelfde jaar na `WAARDE`. Ze zien er
  identiek uit; D staat links in de cel en E rechts. Zet er `MIN` onder en D
  geeft 0. Dat is de hele les, en het is ook de reden dat hun `VERT.ZOEKEN`
  later `#N/B` geeft.
- **Blad 2 heeft podiumnamen van verschillende lengte** (van
  6 tot 10
  tekens). Waren ze even lang, dan kon blad 2 met `LINKS` alleen en leerde
  `VIND.ALLES` niets. `controleer.py` bewaakt dat.
- **Blad 4 heeft drie dubbele achternamen** (De Smet, De Cock, Van Damme).
  Daar staat een spatie MIDDEN in, en die moet blijven staan in de naam en
  een punt worden in het e-mailadres. Dat is precies het verschil tussen
  `SPATIES.WISSEN` en `SUBSTITUEREN`, en zonder die namen is de fiche over
  `SUBSTITUEREN` overbodig.
- **Blad 5 telt 26 regels waarvan er 3
  dubbel staan.** Wie eerst de draaitabel maakt en pas daarna opkuist, krijgt
  26 als eindtotaal in plaats van 23 — en
  merkt het meestal niet.

## De controlegetallen

| Blad | Moet geven |
|---|---|
| 1 | `MIN` op kolom D geeft 0, op kolom E 2013 |
| 2 | langste artiestennaam 17 tekens (Lotte & de Wolken); 18 betekent een spatie te veel |
| 3 | alleen VR, ZA, ZO in kolom B, alleen BOST, KLUB, MAIN, STRA in kolom C |
| 4 | langste adres 32 tekens (lotte.vandenberghe@zomerklank.be); nergens een spatie in kolom D |
| 5 | eindtotaal 23; met de slicer op Hiphop blijven er 6 over |

## Over de gegevens

Zomerklank bestaat niet en de artiesten evenmin. Alles is verzonnen —
**behalve de rommel**. Zo ziet een lijst er echt uit als ze uit een
boekingssysteem komt. Dat zeg je er één keer bij en dan is het duidelijk.

## Opnieuw bouwen

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle kolommen uitgerekend
python3 maak-startbestand.py
python3 maak-documenten.py
python3 controleer.py
```

`controleer.py` kijkt na of:

- de **rommel er nog in zit**: genoeg losse spaties om `SPATIES.WISSEN` nodig
  te maken, genoeg hoofdletters voor `BEGINLETTERS`, minstens één dubbele
  achternaam voor `SUBSTITUEREN`, en genoeg dubbele regels voor blad 5
- elke code even lang is waar de opdracht met vaste posities werkt, en dat
  `DEEL` op die posities er echt uit haalt wat erin zit
- **elke functie in de opdracht een fiche heeft**, en naar elke fiche verwezen
  wordt
- elke formule naar de bovenste rij van haar eigen bereik verwijst, zodat het
  doorvoeren klopt
- het startbestand geen tabel, geen grafiek en geen draaitabel bevat
- geen enkel tekstantwoord op twee bladen tegelijk staat
- de bundel op 50 punten en 50 minuten uitkomt

Getest door er negentien fouten in te spuiten — codes van ongelijke lengte,
twee scheidingstekens in één regel, een opgepoetste naamlijst, een export
zonder dubbels, een slicerkeuze die alles overlaat, een formule die naar de
verkeerde rij verwijst, een functie zonder fiche, hetzelfde antwoord op twee
bladen. Alle negentien worden gevangen.
