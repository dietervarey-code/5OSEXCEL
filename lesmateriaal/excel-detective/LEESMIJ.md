# Excel — vijf detectivezaken

Vijf losse zaken in **echt Excel**, elk ongeveer 25 minuten. Voor leerlingen die
`lesmateriaal/excel-basis/` vlot afwerken en toe zijn aan iets meer, maar voor wie
`lesmateriaal/excel-uitdaging/` (Halloween) te veel ineens was.

**Ook deze bundel wordt zelfstandig gemaakt, zonder leerkracht erbij.** Daarom is de
moeilijkheid op één plaats geconcentreerd:

- **Zes of zeven gewone formules** zetten het dossier op orde. Die staan **letterlijk**
  in de stappen — routinewerk waar niemand op mag stranden.
- **Eén sleutelformule** met een functie binnen een functie kraakt de zaak. Daarvan
  krijgen ze alleen de *vorm*, een uitleg per onderdeel, en de raad om ze in twee
  stappen op te bouwen (eerst het binnenste stuk apart in een hulpcel).
- **Elke zaak heeft een proef**: twee getallen die hetzelfde moeten geven, of een getal
  dat ze op voorhand al weten. Komt het uit, dan hebben ze de zaak — zonder dat iemand
  het hoeft te bevestigen.
- **Elke zaak heeft een lijstje "Loop je vast?"** met de drie fouten die het vaakst
  gemaakt worden.

Achteraan de opdracht staat een **antwoordblad**: per zaak het antwoord, of de proef
klopte, en welke sleutelformule ze gebruikten. Dat is wat ze afgeven.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `detective-startbestand.xlsx` | leerlingen — zes werkbladen, met twee kant-en-klare grafieken |
| `detective-opdracht.docx` | leerlingen — één hoofdstuk per zaak, plus het antwoordblad |
| `detective-leerkrachtensleutel.docx` | jou — de afloop, alle formules, de proef en een nakijkblad |

De functiefiches van de basisbundel mogen erbij: alles behalve de sleutelformule is
gewoon herhaling.

> Personen, bedrijven en voorvallen zijn verzonnen.

## De vijf zaken

| Nr | Zaak | Wat ze uitzoeken | Sleutelformule | Grafiek |
|---|---|---|---|---|
| 1 | De verdwenen avonden | liegt hij over zijn overuren? | `EN` binnen `ALS` | — |
| 2 | De Mercedes van de Koning | waar staat de wagen nu? | `MAX` binnen `VERT.ZOEKEN` | ja |
| 3 | De museumroof | wat is er weg, en voor hoeveel? | `AANTAL.ALS` binnen `ALS` | — |
| 4 | Het gelekte examen | wie zette het online? | `SOM.ALS` binnen `ALS` | — |
| 5 | De sabotage in de chocoladefabriek | wie zat aan de machines? | `VERT.ZOEKEN` binnen `ALS` | ja |

**Vijf verschillende soorten nesting.** Samen dekken ze de manieren waarop een functie
in een andere kan zitten: in de voorwaarde van een `ALS`, in het antwoord van een
`ALS`, en als zoekwaarde van een `VERT.ZOEKEN`. `controleer.py` weigert twee zaken met
dezelfde nesting.

De zaken staan volledig los van elkaar en kunnen in eender welke volgorde.

## De twee grafieken

Ze staan **kant-en-klaar in het startbestand**: lezen, niet maken. Bij elke grafiek
hoort een vraag die ze vóór het rekenen beantwoorden — eerst een vermoeden, dan het
bewijs met een formule.

Zaak 2 gebruikt de grafiek bovendien als valstrik. De hoogste staaf is de laatste rit,
maar de **langste** rit van de maand is een andere (420 km naar Luxemburg, en de wagen
kwam gewoon terug). `controleer.py` bewaakt dat die twee verschillend blijven.

## De afloop van elke zaak

<details>
<summary>Spoilers</summary>

1. Rudi loog zes keer, telkens op donderdag, telkens 45 euro bij **Dansschool Tango
   Nova**. Hij nam in het geheim danslessen voor hun vijfentwintigste
   huwelijksverjaardag.
2. De hoogste kilometerstand hoort bij rit 16: de wagen staat op **Hoeve Ter Linden**
   in Zoutleeuw, gereden door een chauffeur die in het logboek "onbekend" heet.
3. Vier stukken weg — **K-109, K-110, K-112 en K-114**, samen 87 200 euro, allemaal
   kleine zilverstukken uit dezelfde zaal. Het schilderij van 210 000 euro bleef hangen.
4. **Jonas Debbaut** (leerling 6TW), 23 bestanden, waarvan er 21 om 23:40 en 23:52
   geopend werden. Het examen stond om 00:15 online.
5. Technicus **Vercammen**. Vijf slechte batches, van twee machines die hij allebei het
   laatst nakeek. De drie ploegen zijn onschuldig: de slechte batches zijn netjes over
   ploeg A, B en C verdeeld.

</details>

## De bestanden opnieuw maken

```bash
pip install openpyxl python-docx
python3 antwoorden.py         # toont alle vijf de zaken uitgerekend
python3 maak-startbestand.py  # inclusief de twee grafieken
python3 maak-documenten.py
python3 controleer.py         # kijkt na of alles bij elkaar past
```

`controleer.py` bewaakt vijftien dingen. De belangrijkste:

- **precies één geneste functie per zaak**, en de haakjes worden geteld — `=MAX(A1:A9)-MIN(B1:B9)`
  is géén nesting, `=ALS(EN(...);...)` wel
- **alle vijf de nestingen verschillend**
- **de sleutelformule staat nergens letterlijk in de opdracht**, en elke basisformule
  staat er juist wél in
- de twee grafieken bestaan en wijzen naar de juiste kolommen
- per zaak: de proef sluit echt (zaak 1 en 2), er is precies één verdachte / vier
  gestolen stukken, de langste rit is niet de laatste (zaak 2), en geen enkele batch
  ligt zo dicht bij de grens dat een afronding het antwoord kan omgooien (zaak 5)
- elke zaak heeft een dossier, een proef, een vraag, een afloop en minstens drie regels
  bij "Loop je vast?"

Er staan geen vaste rijnummers in: alles wordt afgeleid uit `gegevens.py`.
