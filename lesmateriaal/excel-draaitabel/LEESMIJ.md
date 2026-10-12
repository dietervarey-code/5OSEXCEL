# Theoriebundel — draaitabellen en grafieken

Veertien kaarten over het enige stuk Excel in deze reeks waar je geen formule
voor typt. **Geen oefening** — dit is naslag, net zoals `excel-functiebladen.docx`
dat is voor de functies.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `draaitabellen-en-grafieken.docx` | leerlingen — veertien kaarten, elk op een eigen pagina |

Deel het uit bij `excel-ottomaans/`, de eerste opdracht die draaitabellen
gebruikt. Hou er een stapel van: de bundel is herbruikbaar en gaat over geen
enkele opdracht in het bijzonder.

## De kaarten

| Nr | Kaart | Waarvoor |
|---|---|---|
| 1 | Wat is een draaitabel? | wanneer je er een gebruikt in plaats van `SOM.ALS` |
| 2 | Eerst je lijst in orde brengen | de zes eisen aan een bronlijst |
| 3 | Een draaitabel invoegen | het veldenpaneel en de vier vakken |
| 4 | Rijen en Waarden | je eerste draaitabel, met twee keer slepen |
| 5 | Aantal of Som? | de waardeveldinstellingen, en waarom Excel verkeerd kiest |
| 6 | Een tweede richting: Kolommen | de kruistabel |
| 7 | Sorteren en filteren | aflopend sorteren vóór je een grafiek maakt |
| 8 | Groeperen | jaartallen per decennium, datums per maand |
| 9 | Vernieuwen | een draaitabel rekent **niet** automatisch mee |
| 10 | Een grafiek invoegen | wat je selecteert bepaalt alles |
| 11 | Welk type bij welke vraag? | staaf, lijn of cirkel — en wanneer niet |
| 12 | Een grafiek leesbaar maken | titel, astitels, gegevenslabels |
| 13 | Een draaigrafiek | een grafiek rechtstreeks op een draaitabel |
| 14 | Wat een grafiek kan verbergen | de as die niet bij nul begint, en de rest |

Achteraan staat een **spiekblad**: de draaitabel in vijf stappen, de vier vakken,
de drie grafiektypes en de drie dingen die het vaakst mislopen. Eén pagina.

## Twee regels waar niet van afgeweken wordt

1. **Een kaart geeft nooit de oplossing van een opdracht.** De voorbeelden spelen
   in de schoolbibliotheek, de kantine en het schoolarchief. `controleer.py`
   laadt de `gegevens.py` van elke andere bundel in `lesmateriaal/` en faalt
   zodra er een naam, plaats of code uit opduikt in de kaarten.
2. **Een kaart staat op zichzelf.** Wie vastloopt bij één ding, pakt die ene
   kaart en kan verder.

## De beelden

Vijfentwintig tekeningen, geen schermafdrukken. Dat is bewust: een schermafdruk
van het draaitabelpaneel zit vol menubalken die op papier onleesbaar worden, en
ziet er in elke Excel-versie anders uit.

`tekening.py` tekent zes soorten: een fragment van een rekenblad, het paneel
Draaitabelvelden, een dialoogvenster, een staafdiagram, een lijndiagram en een
cirkeldiagram. Alles op 3× en met 300 dpi erin, zodat het scherp afdrukt.

Twee tekeningen tonen met opzet hetzelfde **fout en juist** naast elkaar: de
slordige lijst tegenover de nette (kaart 2), en dezelfde drie cijfers met de as
vanaf 0 en vanaf 230 (kaart 14).

## Opnieuw bouwen

```bash
pip install python-docx pillow
python3 maak-documenten.py    # tekent de beelden en bouwt de bundel
python3 controleer.py
```

`controleer.py` bewaakt vier dingen:

- elke kaart is volledig: een omschrijving, uitleg of stappen, en een "de fout
  die iedereen één keer maakt"
- de cijfers in de voorbeelddraaitabellen worden opnieuw uitgerekend uit de
  voorbeeldlijst — een draaitabel in een theoriekaart die niet klopt, is erger
  dan geen kaart
- geen enkele naam, plaats of code uit een andere bundel komt in de kaarten voor
- elk beeld bestaat, geen twee beelden heten hetzelfde, en er staat geen oude
  tekening meer in `beelden/`

Het bewaakt ook dat deel 1 precies negen kaarten telt en er veertien in totaal
zijn: andere bundels verwijzen naar "kaart 1 tot 9" en "kaart 10 tot 14".
