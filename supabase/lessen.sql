-- =====================================================================
--  Lessen bij de oefeningen — één per oefening, veertig in totaal
--
--  Uitvoeren in Supabase › SQL Editor. Mag meermaals draaien: een les die
--  al bij een oefening hoort, wordt niet opnieuw toegevoegd.
--  Bewerken doe je daarna in het portaal, via Lessen beheren.
-- =====================================================================

-- ---------------------------------------------------------------------
--  1 · Voorraadlijst afwerken
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 1,
  'Je eerste formules: vermenigvuldigen en SOM',
  'Laat het rekenblad rekenen. Verwijs naar cellen, tel op met SOM, en zet de juiste getalnotatie.',
$md$
## Wat je na deze les kunt

- Een formule schrijven die naar cellen verwijst in plaats van naar getallen
- Een formule doorvoeren met de vulgreep
- Optellen met `SOM`
- Cellen de getalnotatie valuta geven

## 1. Een formule begint met =

Zolang je gewoon tekst of een getal typt, blijft dat staan zoals je het typt. Begin je
met een **isgelijkteken**, dan gaat het rekenblad rekenen.

| Wat je typt | Wat er in de cel komt |
|---|---|
| `414` | het getal 414 |
| `=120*3,45` | 414 — berekend |
| `=B4*C4` | 414, en het past zich aan als B4 of C4 verandert |

De laatste is bijna altijd de juiste. Op stage verandert een prijs of een aantal
voortdurend. Wie het antwoord overtypt, mag alles opnieuw doen.

## 2. Doorvoeren met de vulgreep

Je hoeft een formule maar één keer te typen. Klik de cel aan, pak het kleine blokje
rechtsonder — de **vulgreep** — en sleep naar beneden.

Excel past de rijnummers vanzelf aan: uit `=B4*C4` wordt `=B5*C5`, dan `=B6*C6`.
Dat heet een **relatieve celverwijzing**: de verwijzing schuift mee.

## 3. Optellen met SOM

Voor een totaal kun je `=D4+D5+D6+D7+D8+D9+D10+D11` typen. Dat werkt, tot er een lijn
bijkomt en je het vergeet aan te passen. Gebruik liever:

```
=SOM(D4:D11)
```

De dubbele punt betekent **tot en met**. `D4:D11` is alles van D4 tot en met D11.

> `SOM` slaat lege cellen en tekst gewoon over. Dat is handig: staat er ergens "ziek"
> of "n.v.t.", dan loopt je totaal niet stuk.

## 4. Inhoud tegenover weergave

Een cel heeft een **inhoud** en een **weergave**. In de cel staat `2838,2`, maar met de
getalnotatie valuta zie je `€ 2.838,20`. De inhoud verandert niet — je rekent verder met
het volledige getal.

Selecteer de kolom met bedragen en kies in de werkbalk de getalnotatie **valuta**.

## Twee dingen over typen in dit portaal

- Je mag **puntkomma's** gebruiken tussen de argumenten, net zoals in de cursus:
  `=ALS(B5>100;"ja";"nee")`. Het portaal zet ze automatisch om.
- Gebruik voor decimalen een **punt**: typ `3.45`, niet `3,45`.

## Veelgemaakte fouten

- **Het antwoord met de hand ingetypt** — dat telt niet als een berekening.
- **Het bereik loopt niet tot de laatste rij** — `=SOM(D4:D10)` vergeet de laatste lijn.
- **`#NAAM?`** — je functienaam bevat een typfout.
$md$,
  'voorraad-basis', true
where not exists (select 1 from lessen where oefening_id = 'voorraad-basis');

-- ---------------------------------------------------------------------
--  2 · Prijslijst bijwerken
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 2,
  'Absolute celverwijzing en AFRONDEN',
  'Eén percentage op een hele lijst toepassen, met een verwijzing die blijft staan.',
$md$
## Wat je na deze les kunt

- Het verschil uitleggen tussen een relatieve en een absolute celverwijzing
- Dollartekens zetten met F4
- Afronden op een aantal decimalen met `AFRONDEN`

## 1. Waarom een verwijzing soms moet blijven staan

Je vermenigvuldigt elke prijs met hetzelfde percentage. Dat percentage staat op
**één** plaats: in `C2`.

Typ je `=C5*(1+C2)` en voer je dat door, dan wordt het in de volgende rij
`=C6*(1+C3)`. Maar `C3` is leeg. Je krijgt de prijs zonder verhoging, en je merkt het
niet meteen, want er verschijnt geen foutmelding.

## 2. Dollartekens

Zet een **dollarteken** voor de kolomletter én voor het rijnummer:

```
=C5*(1+$C$2)
```

Nu blijft `C2` staan, hoe ver je ook doorvoert. Je hoeft die tekens niet zelf te typen:
klik in de formulebalk op de verwijzing en druk op **F4**.

| Schrijfwijze | Wat er meeschuift bij doorvoeren |
|---|---|
| `C2` | kolom én rij |
| `$C2` | alleen de rij |
| `C$2` | alleen de kolom |
| `$C$2` | niets — alles blijft staan |

De vuistregel: **schuift het mee met je lijst, dan relatief. Staat het één keer ergens
apart, dan absoluut.**

## 3. Afronden

Een prijs van `35,7075` bestaat niet. Rond af op twee decimalen:

```
=AFRONDEN(C5*(1+$C$2);2)
```

Het tweede argument is het aantal decimalen. `AFRONDEN(x;0)` rondt af op hele getallen.

> Let op het verschil met **opmaak**. Getalnotatie verandert alleen wat je ziet; de cel
> rekent verder met alle decimalen. `AFRONDEN` verandert de inhoud écht. Voor geld dat
> doorgerekend wordt, gebruik je `AFRONDEN`.

## Veelgemaakte fouten

- **Dollartekens vergeten** — de eerste rij klopt, de rest niet.
- **Alleen de opmaak aangepast** — het ziet er afgerond uit, maar dat is het niet.
- **`AFRONDEN` zonder tweede argument** — geef altijd het aantal decimalen mee.
$md$,
  'prijslijst-verhoging', true
where not exists (select 1 from lessen where oefening_id = 'prijslijst-verhoging');

-- ---------------------------------------------------------------------
--  3 · Verkoopcijfers samenvatten
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 4,
  'Samenvatten: MAX, MIN, GEMIDDELDE, AANTAL',
  'Een reeks cijfers in enkele getallen samenvatten — en weten waarom AANTAL en AANTALARG verschillen.',
$md$
## Wat je na deze les kunt

- De functies `MAX`, `MIN` en `GEMIDDELDE` gebruiken
- Uitleggen wanneer je `AANTAL` neemt en wanneer `AANTALARG`

## 1. De drie vanzelfsprekende

| Functie | Wat ze geeft |
|---|---|
| `=MAX(E4:E9)` | het grootste getal in het bereik |
| `=MIN(E4:E9)` | het kleinste getal |
| `=GEMIDDELDE(E4:E9)` | het gemiddelde |

Ze werken allemaal op een **bereik**, net als `SOM`.

## 2. AANTAL tegenover AANTALARG

Dit is de klassieker op een toets.

- `AANTAL` telt alleen de vakjes met een **getal**.
- `AANTALARG` telt alle vakjes die **niet leeg** zijn, dus ook tekst.

Staat er in de kolom februari bij één verkoper het woord `ziek`, dan geeft
`=AANTAL(C4:C9)` het antwoord **5** en `=AANTALARG(C4:C9)` het antwoord **6**.

> Daarom klopt een gemiddelde soms niet: `GEMIDDELDE` deelt door het aantal **getallen**,
> niet door het aantal rijen.

## 3. Let op bij het gemiddelde

Een leeg vakje en een nul zijn niet hetzelfde. Een leeg vakje telt niet mee in het
gemiddelde, een nul wel — en trekt het naar beneden. Laat een vakje leeg als er geen
cijfer is, en typ er geen 0.

## Veelgemaakte fouten

- **`AANTAL` gebruiken waar `AANTALARG` moet** — of omgekeerd.
- **Het bereik van het totaal in het gemiddelde meenemen** — dan tel je dubbel.
- **Een nul typen bij ontbrekende gegevens.**
$md$,
  'verkoopcijfers', true
where not exists (select 1 from lessen where oefening_id = 'verkoopcijfers');

-- ---------------------------------------------------------------------
--  3 · Factuur vervolledigen
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 3,
  'Een factuur berekenen: SOM en absolute celverwijzing',
  'Bedragen per lijn, een subtotaal met SOM, en btw met een verwijzing die blijft staan als je doorvoert.',
$markdown$
## Wat je na deze les kunt

- Een bedrag per factuurlijn berekenen met een formule in plaats van een rekenmachine
- De functie `SOM` gebruiken voor een subtotaal
- Het verschil uitleggen tussen een relatieve en een absolute celverwijzing
- Cellen de getalnotatie valuta geven

## 1. Reken met cellen, niet met getallen

Een formule begint altijd met een **isgelijkteken**. Verwijs naar cellen, nooit naar
getallen die je zelf overtypt:

| Wat je typt | Wat er gebeurt |
|---|---|
| `=C12*D12` | aantal maal eenheidsprijs — past zich aan als de prijs verandert |
| `403,20` | een dood getal — blijft fout staan als de prijs verandert |

> Op stage verandert een prijslijst voortdurend. Wie getallen overtypt, mag alles
> opnieuw doen. Wie met cellen rekent, past één cel aan.

Typ de formule één keer in `E12` en gebruik dan de **vulgreep** (het blokje
rechtsonder in de cel) om ze door te voeren tot `E16`. Excel past de rijnummers
vanzelf aan: `=C13*D13`, `=C14*D14` …

## 2. Optellen met SOM

Voor het subtotaal zou je `=E12+E13+E14+E15+E16` kunnen typen. Dat werkt, maar het
wordt onhandig zodra er een lijn bijkomt. Gebruik:

```
=SOM(E12:E16)
```

De dubbele punt betekent **tot en met**. `E12:E16` is het bereik van E12 tot en met E16.

## 3. Relatief en absoluut verwijzen

Dit is het stuk waar het vaakst op misgaat.

Standaard werkt Excel met een **relatieve celverwijzing**: kopieer je een formule naar
beneden, dan schuiven de rijnummers mee. Meestal wil je dat — `=C12*D12` hoort in de
volgende rij `=C13*D13` te worden.

Maar soms moet een verwijzing **blijven staan**. Het btw-tarief staat in `B21`, en dat
is voor elke lijn hetzelfde. Als je `=E18*B21` doorvoert, wordt dat in de volgende rij
`=E19*B22` — en `B22` is leeg. Je krijgt nul.

Zet daarom een **dollarteken** voor de kolomletter én voor het rijnummer:

```
=E18*$B$21
```

Nu blijft de verwijzing naar `B21` staan, hoe je de formule ook doorvoert. Je hoeft die
dollartekens niet zelf te typen: klik in de formulebalk op de celverwijzing en druk op
**F4**.

| Schrijfwijze | Wat er meeschuift bij doorvoeren |
|---|---|
| `B21` | kolom én rij |
| `$B21` | alleen de rij |
| `B$21` | alleen de kolom |
| `$B$21` | niets — alles blijft staan |

## 4. Getalnotatie: inhoud tegenover weergave

Een cel heeft een **inhoud** en een **weergave**. In de cel staat `3253,4`, maar op het
scherm zie je `€ 3.253,40`. De inhoud verandert niet door de opmaak — je rekent gewoon
verder met het volledige getal.

Selecteer `E12:E20` en kies in de werkbalk de getalnotatie **valuta**. Twee decimalen,
want een factuur telt in centen.

## 5. Veelgemaakte fouten

- **`#NAAM?`** — je functienaam is verkeerd geschreven. Controleer op een typfout.
- **Alles nul na doorvoeren** — je vergat de dollartekens bij het btw-tarief.
- **Het subtotaal klopt niet** — je bereik loopt niet tot en met de laatste lijn.
- **Een bedrag met de hand ingetypt** — dat telt niet als een berekening.
$markdown$,
  'factuur-basis', true
where not exists (select 1 from lessen where oefening_id = 'factuur-basis');

-- ---------------------------------------------------------------------
--  4 · Bestellingen beoordelen
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 5,
  'Laat het rekenblad beslissen: ALS, AANTAL.ALS en SOM.ALS',
  'Een voorwaarde schrijven, en tellen of optellen alleen waar die voorwaarde klopt.',
$md$
## Wat je na deze les kunt

- Een voorwaarde schrijven met `ALS`
- Tellen op voorwaarde met `AANTAL.ALS`
- Optellen op voorwaarde met `SOM.ALS`

## 1. De functie ALS

`ALS` stelt een vraag en geeft twee mogelijke antwoorden:

```
=ALS(voorwaarde; wat als het klopt; wat als het niet klopt)
```

Concreet:

```
=ALS(C5>=500;"Gratis";"Verzendkosten")
```

Lees dat als: *is C5 minstens 500? Zo ja, zet "Gratis". Zo nee, zet "Verzendkosten".*

Tekst zet je tussen **aanhalingstekens**. Getallen niet.

| Teken | Betekenis |
|---|---|
| `=` | gelijk aan |
| `>` `<` | groter dan, kleiner dan |
| `>=` `<=` | minstens, hoogstens |
| `<>` | niet gelijk aan |

## 2. Zet de drempel in een cel

Schrijf niet `=ALS(C5>=500;…)` maar zet die 500 in een aparte cel en verwijs ernaar:

```
=ALS(C5>=$D$2;"Gratis";"Verzendkosten")
```

Verandert de drempel, dan pas je één cel aan in plaats van acht formules. En vergeet de
dollartekens niet — zonder die schuift `D2` mee naar beneden.

## 3. Tellen en optellen op voorwaarde

```
=AANTAL.ALS(D5:D12;"Gratis")
```

*Hoeveel keer staat "Gratis" in D5:D12?*

```
=SOM.ALS(D5:D12;"Gratis";C5:C12)
```

*Zoek in D5:D12 naar "Gratis", en tel telkens het bedrag uit C5:C12 op.*

Let op de volgorde: **eerst waar je zoekt, dan wat je zoekt, dan wat je optelt.** Laat je
het derde bereik weg, dan telt `SOM.ALS` op in het bereik waarin het zoekt.

Een criterium mag ook een vergelijking zijn, tussen aanhalingstekens:
`=AANTAL.ALS(C5:C12;">500")`.

## Veelgemaakte fouten

- **Aanhalingstekens vergeten rond tekst** — `=ALS(C5>=500;Gratis;…)` werkt niet.
- **De bereiken van `SOM.ALS` in de verkeerde volgorde.**
- **De drempel hard in de formule typen** — werkt, maar is onhandig bij elke wijziging.
$md$,
  'bestellingen-als', true
where not exists (select 1 from lessen where oefening_id = 'bestellingen-als');

-- ---------------------------------------------------------------------
--  5 · Klantenbestand aanvullen
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 6,
  'Opzoeken in een andere tabel: VERT.ZOEKEN',
  'Een naam of prijs ophalen op basis van een code, in plaats van ze over te typen.',
$md$
## Wat je na deze les kunt

- `VERT.ZOEKEN` gebruiken om gegevens uit een andere tabel te halen
- Uitleggen waarom de tabel absoluut moet zijn
- Het verschil tussen exact zoeken en zoeken bij benadering

## 1. Waarvoor het dient

Je lijst bevat alleen klantnummers. De namen staan in een andere tabel. Overtypen is
traag en foutgevoelig: wijzigt een naam, dan klopt jouw lijst niet meer.

`VERT.ZOEKEN` haalt de naam op. **Vert** staat voor verticaal: de functie zoekt van boven
naar beneden in de **eerste kolom** van de tabel.

## 2. De vier argumenten

```
=VERT.ZOEKEN(B4; $G$4:$I$9; 2; ONWAAR)
```

| Argument | Wat het is |
|---|---|
| `B4` | wat je zoekt — hier het klantnummer |
| `$G$4:$I$9` | waarin je zoekt — de hele tabel |
| `2` | de hoeveelste kolom van die tabel je wil terugkrijgen |
| `ONWAAR` | exact zoeken |

Het kolomnummer telt **binnen de tabel**, niet in het werkblad. Begint je tabel in kolom
G, dan is G kolom 1, H kolom 2, I kolom 3.

## 3. Twee valkuilen

**De tabel moet absoluut zijn.** Zonder dollartekens schuift `G4:I9` bij het doorvoeren
mee naar `G5:I10`, en verdwijnt de bovenste klant uit beeld. Resultaat: `#N/B` onderaan.

**Sluit af met ONWAAR.** Laat je dat weg, dan zoekt Excel bij *benadering* en neemt het
de dichtstbijzijnde kleinere waarde. Bij codes en namen is dat bijna altijd fout. Alleen
bij schijven — een tarief per bedrag — wil je `WAAR`.

## 4. Wat je zoekt, staat links

`VERT.ZOEKEN` kan alleen naar **rechts** kijken. De kolom waarin je zoekt moet de eerste
van de tabel zijn. Staat de code rechts van de naam, dan lukt het niet — daarvoor bestaat
`X.ZOEKEN`, de volgende les.

## Veelgemaakte fouten

- **`#N/B`** — de waarde staat niet in de eerste kolom, of er staat een spatie te veel.
- **Tabel niet absoluut** — de eerste rijen kloppen, de laatste niet.
- **Kolomnummer verkeerd geteld** — tel vanaf de eerste kolom van de tabel.
$md$,
  'klanten-vertzoeken', true
where not exists (select 1 from lessen where oefening_id = 'klanten-vertzoeken');


-- ---------------------------------------------------------------------
--  6 · Artikelen opzoeken met X.ZOEKEN
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 7,
  'X.ZOEKEN: de opvolger van VERT.ZOEKEN',
  'Eenvoudiger zoeken, in beide richtingen, en zelf bepalen wat er staat als iets niet bestaat.',
$md$
## Wat je na deze les kunt

- `X.ZOEKEN` gebruiken in plaats van `VERT.ZOEKEN`
- Zelf bepalen wat er verschijnt als er niets gevonden wordt
- Uitleggen waarom `X.ZOEKEN` minder snel stukgaat

## 1. Hetzelfde idee, eenvoudiger

`VERT.ZOEKEN` wil een tabel én een kolomnummer. `X.ZOEKEN` wil gewoon twee kolommen:
waar het zoekt, en waar het antwoord staat.

```
=X.ZOEKEN(A4; $G$4:$G$10; $H$4:$H$10; "niet gevonden")
```

| Argument | Wat het is |
|---|---|
| `A4` | wat je zoekt |
| `$G$4:$G$10` | de kolom waarin gezocht wordt |
| `$H$4:$H$10` | de kolom met het antwoord |
| `"niet gevonden"` | wat je krijgt als er niets gevonden wordt |

Geen kolommen tellen meer, en geen `ONWAAR`: `X.ZOEKEN` zoekt standaard exact.

## 2. Het vierde argument is het belangrijkste

Zonder vierde argument krijg je bij een onbekende code `#N/B` — en dan loopt alles wat
je daarna nog berekent óók stuk.

Met een vierde argument bepaal je zelf wat er staat: `"niet gevonden"` bij tekst, `0` bij
een bedrag. Je lijst blijft leesbaar en je totaal blijft werken.

> Op stage is dat het verschil tussen "er klopt iets niet aan één lijn" en "het hele
> overzicht staat vol foutmeldingen".

## 3. Het kan ook naar links

`VERT.ZOEKEN` kan alleen naar rechts kijken. `X.ZOEKEN` niet: de zoekkolom en de
antwoordkolom mogen in elke volgorde staan. Je hoeft je tabel dus niet te verbouwen.

## 4. Wanneer toch nog VERT.ZOEKEN?

`X.ZOEKEN` bestaat niet in oudere versies van Excel. Werk je op stage op een oud
systeem, dan heb je `VERT.ZOEKEN` nodig. Ken ze allebei.

## Veelgemaakte fouten

- **Zoekkolom en antwoordkolom even lang maken** — `$G$4:$G$10` en `$H$4:$H$9` geeft rommel.
- **Het vierde argument vergeten** — één verkeerde code en je lijst staat vol `#N/B`.
- **De kolommen niet absoluut maken** — ze schuiven mee bij het doorvoeren.
$md$,
  'xzoeken-artikelen', true
where not exists (select 1 from lessen where oefening_id = 'xzoeken-artikelen');

-- ---------------------------------------------------------------------
--  7 · Geneste functies
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 8,
  'Geneste functies: twee functies in één formule',
  'Een VERT.ZOEKEN en een ALS combineren, en weten in welke volgorde het rekenblad werkt.',
$md$
## Wat je na deze les kunt

- Een functie binnen een andere functie gebruiken
- Een formule van binnen naar buiten lezen
- Een lange formule opbouwen in stukken, zonder te verdwalen

## 1. Wat nesten is

Een functie geeft een waarde terug. Overal waar een waarde mag staan, mag dus ook een
functie staan. Dat heet **nesten**.

```
=VERT.ZOEKEN(B5;$H$5:$I$7;2;ONWAAR) + ALS(C5>100;0.02;0)
```

Hier staan er twee naast elkaar: de ene haalt het basispercentage op, de andere telt er
eventueel iets bij.

## 2. Lees van binnen naar buiten

Het rekenblad werkt de **binnenste** functie eerst af en gebruikt dat resultaat in de
buitenste. Bij twijfel: klik in de formulebalk een stuk van de formule aan en druk op
**F9**. Je ziet dan wat dat stuk oplevert. Druk daarna op **Esc**, niet op Enter.

## 3. Bouw op in stukken

Probeer nooit een lange formule in één keer te typen. Werk zo:

1. Zet in een lege cel `=VERT.ZOEKEN(B5;$H$5:$I$7;2;ONWAAR)`. Klopt het?
2. Zet er in een andere cel `=ALS(C5>100;0.02;0)` naast. Klopt het?
3. Voeg ze pas dan samen in één formule.
4. Voer door en controleer de laatste rij.

Zo weet je meteen welk stuk fout is.

## 4. Haakjes

Elk haakje dat opengaat, moet dicht. Excel kleurt bij elkaar horende haakjes. Krijg je de
melding dat er iets mis is met je formule, tel dan eerst je haakjes.

> Een formule met drie niveaus is bijna altijd een teken dat je het eenvoudiger kunt.
> Zet een tussenstap in een extra kolom. Je collega — en jijzelf over drie maanden —
> begrijpen dat sneller.

## Veelgemaakte fouten

- **Een haakje te veel of te weinig.**
- **De binnenste functie niet apart getest** — je zoekt de fout dan in het verkeerde stuk.
- **Vergeten dollartekens in de binnenste functie** — pas zichtbaar bij het doorvoeren.
$md$,
  'geneste-functies', true
where not exists (select 1 from lessen where oefening_id = 'geneste-functies');
-- ---------------------------------------------------------------------
--  FOCUS 1 · Rekenblad gebruiken en opmaken
-- ---------------------------------------------------------------------

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 1,
  'Getalnotatie: inhoud tegenover weergave',
  'Waarom dezelfde cel er anders kan uitzien zonder dat er iets aan het getal verandert.',
$md$
## Wat je na deze les kunt

- Uitleggen wat het verschil is tussen de inhoud en de weergave van een cel
- De notaties valuta, percentage en getal toepassen
- Een koptekst laten opvallen met vet en een achtergrondkleur

## 1. Eén cel, twee dingen

Elke cel heeft een **inhoud** en een **weergave**.

| In de cel staat | Met notatie | Je ziet |
|---|---|---|
| `0.84` | getal | 0,84 |
| `0.84` | valuta | € 0,84 |
| `0.21` | percentage | 21% |

Het getal verandert níét. Je verandert alleen hoe het op je scherm komt. Klik op de cel
en kijk in de formulebalk: daar staat nog altijd `0.21`.

> Dat is meteen de valkuil bij percentages. `21` met de notatie percentage wordt
> **2100%**, want de notatie vermenigvuldigt met honderd. Een btw-tarief typ je dus als
> `0.21`, niet als `21`.

## 2. Waarom het uitmaakt

Een prijs van `0.8` en een prijs van `0,80 euro` zijn hetzelfde getal, maar niet
hetzelfde document. Op een factuur die naar een klant gaat, horen twee decimalen en een
euroteken. Dat is geen versiering: het is duidelijkheid over wat er betaald moet worden.

Omdat de inhoud niet verandert, blijf je gewoon verder rekenen met het volledige getal.
Zie je `€ 3.253,40` staan, dan kan er in de cel nog altijd `3253.4` zitten.

## 3. De notatie kiezen

Selecteer de cellen en kies de notatie in de werkbalk bovenaan, bij de keuzelijst die op
**General** staat. De namen staan er in het Engels:

| In het portaal | In het Nederlandse Excel |
|---|---|
| Currency | Valuta |
| Percentage | Percentage |
| Number | Getal |
| Accounting | Boekhoudkundig |

## 4. Vet en kleur

Een koptekst hoort eruit te springen. Twee dingen volstaan:

- **Vet**: selecteer de cellen en klik op **B**, of druk op **Ctrl+B**.
- **Achtergrondkleur**: het emmertje in de werkbalk.

Hou het rustig. Een tabel waarin alles gekleurd is, leest even slecht als een tabel
waarin niets gekleurd is.

## Veelgemaakte fouten

- **`21` typen bij een percentage** — dat wordt 2100%. Typ `0.21`.
- **Denken dat opmaak afrondt** — `AFRONDEN` verandert de inhoud, opmaak niet.
- **Een getal als tekst invoeren** — begin nooit met een apostrof of een spatie, anders
  rekent het rekenblad er niet meer mee.
$md$,
  'f1-getalnotatie', true
where not exists (select 1 from lessen where oefening_id = 'f1-getalnotatie');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 2,
  'Een tabel leesbaar maken',
  'Koptekst, uitlijning en een duidelijke totaalrij — zodat een collega je werk meteen begrijpt.',
$md$
## Wat je na deze les kunt

- Een koptekst herkenbaar maken
- Uitlijning bewust kiezen
- Een totaalrij laten opvallen

## 1. Opmaak is geen versiering

Op stage komt jouw tabel op het bureau van iemand anders terecht. Die persoon heeft geen
tijd om te zoeken waar de koppen staan en welke rij het totaal is. Opmaak is de kortste
weg naar begrip.

Drie ingrepen volstaan voor bijna elke tabel:

1. Koptekst **vet**, met een lichte **achtergrondkleur**
2. Koptekst **gecentreerd**
3. Totaalrij **vet**, eventueel met een lijn erboven

## 2. Uitlijning: de regel

| Soort gegeven | Uitlijning |
|---|---|
| tekst (namen, omschrijvingen) | links |
| getallen en bedragen | rechts |
| koptekst | gecentreerd |

Het rekenblad doet de eerste twee vanzelf: tekst gaat naar links, getallen naar rechts.
Dat is meteen een handige controle. **Staat een getal links, dan is het geen getal maar
tekst** — en dan telt het niet mee in je `SOM`.

De koptekst centreer je zelf, met de knop voor centreren in de werkbalk.

## 3. De totaalrij

Een totaal dat er precies hetzelfde uitziet als de rest, wordt over het hoofd gezien.
Zet het in het vet. Een randlijn erboven maakt het af.

## 4. Kolombreedte

Staat er `####` in een cel, dan is de kolom te smal voor het getal. De inhoud is niet
kwijt — de kolom is gewoon te klein. Sleep de rand tussen twee kolomletters, of
dubbelklik erop om de kolom automatisch passend te maken.

## Veelgemaakte fouten

- **Alles vet zetten** — dan valt niets meer op.
- **Getallen die links uitgelijnd blijven** — dat zijn getallen die als tekst zijn ingevoerd.
- **Een totaalrij die meegesleept wordt in een sortering** — daarover gaat de volgende les.
$md$,
  'f1-tabel-opmaken', true
where not exists (select 1 from lessen where oefening_id = 'f1-tabel-opmaken');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 3,
  'Sorteren zonder je gegevens te vernielen',
  'De belangrijkste regel: selecteer altijd de hele tabel, nooit één kolom.',
$md$
## Wat je na deze les kunt

- Een lijst sorteren op een kolom naar keuze
- Uitleggen waarom je de hele tabel moet selecteren
- Oplopend en aflopend uit elkaar houden

## 1. De fout die je maar één keer maakt

Stel: je selecteert alleen de kolom **Omzet** en sorteert die van groot naar klein.
De bedragen verhuizen, maar de namen ernaast blijven staan. Resultaat: elke klant heeft
nu de omzet van iemand anders.

Dat ziet er volstrekt normaal uit. Niets is rood, er is geen foutmelding. Je merkt het
pas als iemand vraagt waarom Klusbedrijf Six plots de grootste klant is.

> **Selecteer altijd het hele bereik**, inclusief alle kolommen die bij de rij horen.
> De koptekst laat je erbuiten, of je geeft aan dat je tabel een koptekst heeft.

## 2. Zo doe je het

1. Selecteer het bereik met de gegevens, bijvoorbeeld `A4:C10`.
2. Klik bovenaan op **Data**.
3. Kies de sorteerknop en geef aan op welke kolom je sorteert.
4. Kies oplopend of aflopend.

| Richting | Getallen | Tekst |
|---|---|---|
| oplopend | klein → groot | A → Z |
| aflopend | groot → klein | Z → A |

## 3. Waar let je nog op

- **Een totaalrij hoort niet in de selectie.** Anders wordt die mee gesorteerd en staat
  je totaal plots ergens in het midden.
- **Lege rijen breken je tabel.** Het rekenblad denkt dan dat je tabel daar stopt.
- **Getallen als tekst sorteren verkeerd.** Dan komt `100` vóór `99`, omdat het
  letter voor letter vergelijkt.

## Veelgemaakte fouten

- **Eén kolom selecteren** — de rijen raken door elkaar en je ziet het niet.
- **De koptekst mee sorteren** — die belandt dan ergens middenin.
- **Sorteren terwijl er formules naar de rijen verwijzen** — controleer die achteraf.
$md$,
  'f1-sorteren', true
where not exists (select 1 from lessen where oefening_id = 'f1-sorteren');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 4,
  'Titels vastzetten',
  'Je koptekst in beeld houden terwijl je door honderden rijen scrolt.',
$md$
## Wat je na deze les kunt

- Rijen of kolommen vastzetten
- Kiezen wat je vastzet, en waarom precies daar
- Het verschil uitleggen met verbergen

## 1. Het probleem

Een leveringslijst loopt over tweehonderd rijen. Je scrollt naar rij 150 en vraagt je af
of die kolom nu het aantal was of de eenheidsprijs. Je scrollt terug. Je scrollt weer
naar beneden. Je vergeet het opnieuw.

Titels vastzetten lost dat op: de bovenste rijen blijven staan terwijl de rest
doorschuift.

## 2. Hoe je het doet

Klik met de **rechtermuisknop** op het nummer van de rij **onder** wat je wil vastzetten,
en kies **Freeze**.

Wil je de eerste drie rijen vasthouden, dan klik je dus op rij **4**. Dat is de logica:
alles bóven de cel die je aanduidt, blijft staan.

> In het Nederlandse Excel heet dit **Beeld › Titels blokkeren**. De werking is identiek.

Hetzelfde kan met kolommen. Staan je namen in kolom A en scroll je ver naar rechts, dan
zet je kolom A vast door op kolom B te klikken.

## 3. Wanneer je het gebruikt

- Een lijst die niet op één scherm past
- Een brede tabel waarbij je de namen links in beeld wil houden
- Elke tabel die je aan iemand anders doorgeeft

Het verandert niets aan je gegevens en niets aan het afdrukken. Het is puur een hulp
tijdens het werken.

## 4. Niet verwarren met verbergen

**Vastzetten** houdt rijen in beeld. **Verbergen** haalt ze uit beeld. Dat tweede is
gevaarlijk in een document dat je doorgeeft: de verborgen rijen tellen wél mee in je
`SOM`, maar niemand ziet ze staan.

## Veelgemaakte fouten

- **Op de verkeerde rij klikken** — je zet er één te veel of één te weinig vast.
- **Vastzetten verwarren met een lijn tekenen** — een rand is opmaak, vastzetten is een
  instelling van het beeld.
$md$,
  'f1-vastzetten', true
where not exists (select 1 from lessen where oefening_id = 'f1-vastzetten');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 5,
  'Transponeren: rijen worden kolommen',
  'Een tabel kantelen met Plakken speciaal, in plaats van alles opnieuw te typen.',
$md$
## Wat je na deze les kunt

- Een tabel kantelen met Plakken speciaal
- Kiezen tussen waarden plakken en opmaak plakken
- Herkennen wanneer kantelen de juiste oplossing is

## 1. Waarvoor het dient

Je krijgt cijfers aangeleverd met de maanden naast elkaar:

| | Januari | Februari | Maart |
|---|---|---|---|
| Omzet | 24500 | 21870 | 26340 |

Maar om ermee te werken — sorteren, filteren, een grafiek maken — wil je ze onder elkaar.
Overtypen kan, maar bij zes maanden is dat vervelend en bij zestig maanden onbegonnen.

**Transponeren** kantelt de tabel voor je. Wat naast elkaar stond, komt onder elkaar.

## 2. Zo doe je het

1. Selecteer het bereik dat je wil kantelen, bijvoorbeeld `B3:G4`.
2. Kopieer het, met **Ctrl+C**.
3. Klik in de cel waar de linkerbovenhoek van het resultaat moet komen.
4. **Rechtermuisknop** → **Paste Special** → **Transpose**.

> In het Nederlandse Excel: **Plakken speciaal › Transponeren**.

## 3. Let op met formules

Kantel je cellen met formules, dan schuiven de verwijzingen mee — en die kloppen daarna
meestal niet meer. Ging het je alleen om de cijfers, kies dan in hetzelfde menu voor
**waarden plakken**. Je plakt dan de uitkomsten, zonder de formules erachter.

## 4. Plakken speciaal kan meer

Hetzelfde menu laat je kiezen wát je plakt:

| Optie | Wat er geplakt wordt |
|---|---|
| Alles | inhoud, formules en opmaak |
| Waarden | alleen de uitkomsten |
| Opmaak | alleen het uiterlijk |
| Transponeren | gekanteld |

Waarden plakken is op stage het vaakst nodig: je bevriest een berekening zodat ze niet
meer verandert.

## Veelgemaakte fouten

- **Over bestaande gegevens plakken** — kantelen heeft ruimte nodig, en overschrijft
  zonder waarschuwing.
- **Formules kantelen en de verwijzingen niet controleren.**
- **Gewoon plakken in plaats van Plakken speciaal** — dan gebeurt er niets bijzonders.
$md$,
  'f1-transponeren', true
where not exists (select 1 from lessen where oefening_id = 'f1-transponeren');
-- ---------------------------------------------------------------------
--  FOCUS 5 · Meerdere werkbladen
-- ---------------------------------------------------------------------

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 5, 1,
  'Verwijzen naar een ander werkblad',
  'Het uitroepteken: hoe een formule over de grens van een tabblad heen kijkt.',
$md$
## Wat je na deze les kunt

- Een cel van een ander werkblad aanspreken
- Zo'n verwijzing met de muis laten maken in plaats van ze te typen
- Uitleggen waarom je met tabbladen werkt

## 1. Waarom tabbladen

Eén blad met twaalf maanden onder elkaar wordt onoverzichtelijk. Twaalf tabbladen met
dezelfde opbouw is rustiger: elke maand ziet er hetzelfde uit, en je overzichtsblad haalt
eruit wat het nodig heeft.

De tabbladen staan onderaan. Klikken erop, dubbelklikken om te hernoemen.

## 2. De schrijfwijze

Een verwijzing naar een ander blad ziet eruit als:

```
=Januari!D10
```

De bladnaam, dan een **uitroepteken**, dan het celadres. Lees het als
*"cel D10 op het blad Januari"*.

Staat er een spatie in de bladnaam, dan moeten er aanhalingstekens omheen:

```
='Filiaal Roeselare'!D10
```

> Daarom is het slim om bladnamen kort te houden en zonder spaties: `Januari`,
> `Roeselare`, `Prijslijst`.

## 3. Laat de muis het werk doen

Je hoeft die verwijzing niet uit te typen, en dat is ook minder foutgevoelig:

1. Typ `=` in de cel waar het resultaat moet komen.
2. Klik onderaan op het tabblad **Januari**.
3. Klik de cel aan die je wil ophalen.
4. Druk op **Enter**.

Je springt automatisch terug naar je overzichtsblad, met de juiste formule erin.

## 4. Het blijft meebewegen

Verandert het cijfer op het blad Januari, dan verandert je overzicht mee. Dat is het hele
punt: het cijfer staat op **één** plaats. Overtypen zou betekenen dat je het twee keer
moet bijhouden, en dan loopt het vroeg of laat uiteen.

## Veelgemaakte fouten

- **Het uitroepteken vergeten** — `=JanuariD10` is geen verwijzing maar onzin.
- **De bladnaam verkeerd spellen** — je krijgt `#VERW!` of een lege cel.
- **Een blad hernoemen nadat je ernaar verwees** — het rekenblad past dat meestal
  vanzelf aan, maar controleer het.
$md$,
  'f5-bladen-ophalen', true
where not exists (select 1 from lessen where oefening_id = 'f5-bladen-ophalen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 5, 2,
  'Dezelfde cel op meerdere bladen',
  'Waarom je maandbladen er allemaal hetzelfde moeten uitzien.',
$md$
## Wat je na deze les kunt

- Uitleggen waarom een vaste structuur per blad belangrijk is
- Eén rij over meerdere bladen volgen
- Een aandeel berekenen als percentage

## 1. Structuur is alles

Als Kortrijk op elk maandblad in dezelfde rij staat, is `=Januari!D6` op elk blad
hetzelfde soort verwijzing. Je typt ze één keer en past alleen de bladnaam aan.

Staat Kortrijk in januari op rij 6 en in februari op rij 4, dan moet je elke formule apart
uitzoeken. Eén vergissing en je vergelijkt het verkeerde filiaal.

> **Vuistregel:** bladen die je met elkaar wil vergelijken, geef je exact dezelfde
> opbouw. Kopieer een leeg blad in plaats van elke maand opnieuw te tikken.

## 2. Een aandeel berekenen

Een aandeel is een deling: het deel gedeeld door het geheel.

```
=B8/(Januari!D10+Februari!D10+Maart!D10)
```

De uitkomst is een getal tussen 0 en 1. Geef de cel de notatie **percentage** en je ziet
bijvoorbeeld 27%.

Denk eraan: de notatie vermenigvuldigt met honderd. Je hoeft in je formule dus **niet**
nog eens `*100` te doen.

## 3. Haakjes

Bij een deling met een optelling eronder zijn haakjes noodzakelijk:

| Formule | Wat er gebeurt |
|---|---|
| `=B8/Januari!D10+Februari!D10` | eerst delen, dan optellen — fout |
| `=B8/(Januari!D10+Februari!D10)` | eerst optellen, dan delen — juist |

Het rekenblad rekent net als op school: eerst vermenigvuldigen en delen, dan optellen en
aftrekken. Haakjes zetten dat naar je hand.

## Veelgemaakte fouten

- **Bladen met een verschillende opbouw** — de oorzaak van bijna elke fout in dit blok.
- **Haakjes vergeten bij een deling.**
- **`*100` doen én de notatie percentage zetten** — dan staat er 2700%.
$md$,
  'f5-bladen-filiaal', true
where not exists (select 1 from lessen where oefening_id = 'f5-bladen-filiaal');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 5, 3,
  'Twee bladen in één formule',
  'Verschillen en groei berekenen met cellen die op verschillende tabbladen staan.',
$md$
## Wat je na deze les kunt

- Cellen van twee bladen in één berekening combineren
- Een verschil en een groeipercentage uitrekenen
- Het verschil zien tussen een verschil en een groei

## 1. Gewoon doorrekenen

Een verwijzing naar een ander blad gedraagt zich als elke andere celverwijzing. Je kunt
ermee rekenen alsof het een gewone cel is:

```
=Maart!D4-Januari!D4
```

Je mag bladen door elkaar gebruiken binnen dezelfde formule. Het rekenblad haalt elke
waarde op waar ze staat.

## 2. Verschil tegenover groei

Dit is een begrip dat op stage vaak fout gaat.

| Vraag | Formule | Antwoord |
|---|---|---|
| Hoeveel euro meer? | `=C4-B4` | een bedrag |
| Hoeveel procent meer? | `=(C4-B4)/B4` | een percentage |

Het **verschil** is het nieuwe min het oude. De **groei** is dat verschil gedeeld door het
oude getal. Deel altijd door het **vertrekpunt**, niet door het eindpunt.

Een omzet die van 100 naar 150 gaat, groeit met 50%. Gaat ze van 150 terug naar 100, dan
daalt ze met 33%, niet met 50%. Dezelfde 50 euro, een ander percentage — omdat je door een
ander getal deelt.

## 3. Doorvoeren over bladen heen

Verwijzingen naar andere bladen schuiven bij het doorvoeren net zo mee als gewone
verwijzingen. `=Januari!D4` wordt een rij lager `=Januari!D5`. De **bladnaam** blijft
staan; alleen het celadres verandert.

## Veelgemaakte fouten

- **Delen door het nieuwe getal** in plaats van door het oude.
- **Een verschil als percentage opmaken** — dan staat er 470000% in plaats van € 4.700.
- **Vergeten dat een daling negatief is** — dat is geen fout, dat is informatie.
$md$,
  'f5-bladen-verschil', true
where not exists (select 1 from lessen where oefening_id = 'f5-bladen-verschil');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 5, 4,
  'Functies over meerdere bladen',
  'GEMIDDELDE, MAX en MIN met cellen die niet naast elkaar staan.',
$md$
## Wat je na deze les kunt

- Een functie gebruiken met losse cellen in plaats van een aaneengesloten bereik
- Uitleggen wanneer je puntkomma's gebruikt en wanneer een dubbele punt

## 1. Bereik tegenover losse cellen

Tot nu gaf je een functie een **bereik** mee:

```
=SOM(D4:D11)
```

De dubbele punt betekent **tot en met**. Dat werkt alleen als de cellen aan elkaar
grenzen. Cellen op drie verschillende bladen grenzen niet aan elkaar, dus som je ze op
als **losse argumenten**, gescheiden door puntkomma's:

```
=GEMIDDELDE(Januari!D4;Februari!D4;Maart!D4)
```

| Teken | Betekent | Voorbeeld |
|---|---|---|
| `:` | tot en met | `D4:D11` — alles daartussen |
| `;` | en ook | `D4;F4;H4` — precies die drie |

Je mag ze ook mengen: `=SOM(D4:D11;Januari!D4)` telt een heel bereik op plus één losse cel.

## 2. Dezelfde regel voor MAX en MIN

```
=MAX(Januari!D4;Februari!D4;Maart!D4)
=MIN(Januari!D4;Februari!D4;Maart!D4)
```

De beste en de zwakste maand van dat filiaal. Zet je ze naast het gemiddelde, dan zie je
in één oogopslag of een filiaal stabiel draait of grote schommelingen kent.

## 3. Waarom niet gewoon optellen en delen

`=(Januari!D4+Februari!D4+Maart!D4)/3` geeft hetzelfde antwoord — tot er een maand leeg
blijft. Dan deel je nog altijd door 3 terwijl er maar twee cijfers zijn.

`GEMIDDELDE` telt alleen de cellen die écht een getal bevatten. Dat is betrouwbaarder.

## Veelgemaakte fouten

- **Een dubbele punt gebruiken tussen bladen** — `Januari!D4:Maart!D4` is geen geldig bereik.
- **Delen door een vast getal** in plaats van `GEMIDDELDE` te gebruiken.
- **Een haakje vergeten** bij drie argumenten.
$md$,
  'f5-bladen-gemiddelde', true
where not exists (select 1 from lessen where oefening_id = 'f5-bladen-gemiddelde');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 5, 5,
  'Opzoeken op een ander werkblad',
  'VERT.ZOEKEN waarbij de tabel op een ander tabblad staat.',
$md$
## Wat je na deze les kunt

- Een zoektabel op een ander blad aanspreken
- De dollartekens op de juiste plaats zetten
- Uitleggen waarom je brongegevens apart houdt

## 1. Brongegevens horen apart

Een verzorgd rekenblad heeft twee soorten bladen:

- **Brongegevens**: de ruwe tabellen. Saai, volledig, zelden zichtbaar.
- **Rapporten**: wat je aan iemand toont. Net, samengevat, alleen het nodige.

Door ze te scheiden kun je je rapport netjes opmaken zonder aan de gegevens te raken, en
kun je de gegevens aanvullen zonder je rapport te verbouwen.

## 2. Het bladvoorvoegsel zit vóór de dollartekens

De schrijfwijze is de gewone `VERT.ZOEKEN`, met de bladnaam voor het bereik:

```
=VERT.ZOEKEN(A4;Maart!$A$4:$D$7;2;ONWAAR)
```

Let op de volgorde: eerst de **bladnaam met uitroepteken**, dan pas de dollartekens.
Het is `Maart!$A$4`, niet `$Maart!A$4`.

De dollartekens doen hier precies wat ze altijd doen: ze zorgen dat het bereik blijft
staan als je de formule doorvoert. De bladnaam schuift sowieso niet mee.

## 3. Bouw het op met de muis

Bij een lange formule is het makkelijkst:

1. Typ `=VERT.ZOEKEN(` en klik de cel aan die je zoekt.
2. Typ `;` en klik onderaan op het tabblad met de tabel.
3. Sleep over de tabel. Druk op **F4** om er dollartekens bij te zetten.
4. Typ `;2;ONWAAR)` en druk op **Enter**.

## 4. Controleer de onderste rij

De klassieke fout: de eerste rijen kloppen, de laatste geven `#N/B`. Dat betekent bijna
altijd dat de dollartekens ontbreken en het bereik mee naar beneden geschoven is.
Klik op de onderste cel en kijk wat er in de formulebalk staat.

## Veelgemaakte fouten

- **`#N/B` onderaan** — dollartekens vergeten.
- **Kolomnummer geteld vanaf kolom A van het werkblad** in plaats van vanaf het begin van
  de tabel.
- **`ONWAAR` vergeten** — dan zoekt het rekenblad bij benadering en krijg je stille fouten.
$md$,
  'f5-bladen-zoeken', true
where not exists (select 1 from lessen where oefening_id = 'f5-bladen-zoeken');
-- ---------------------------------------------------------------------
--  FOCUS 6 · Koppelen
-- ---------------------------------------------------------------------

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 6, 1,
  'Koppelen aan een bronblad',
  'Eén plaats waar een gegeven staat, en overal waar het nodig is een koppeling ernaartoe.',
$md$
## Wat je na deze les kunt

- Uitleggen wat een koppeling is en waarom ze bestaat
- Een prijs ophalen in plaats van ze over te typen
- De gevolgen inschatten van een wijziging aan de bron

## 1. Eén waarheid

Een prijs staat op één plaats: de prijslijst. Overal waar die prijs nodig is — een
bestelbon, een factuur, een offerte — verwijs je ernaar. Zo kan er maar één versie van de
waarheid bestaan.

Het alternatief is overtypen. Dat werkt precies tot de dag dat de leverancier zijn prijs
verandert. Dan moet je alle documenten terugvinden waar die prijs in staat. Eentje
vergeten, en je factureert maanden aan de verkeerde prijs.

## 2. Zo ziet een koppeling eruit

```
=Prijslijst!C4
```

Precies dezelfde schrijfwijze als bij Focus 5: bladnaam, uitroepteken, celadres. Een
koppeling is niets anders dan een verwijzing die over de bladgrens kijkt.

Wijzig je `C4` op het blad Prijslijst, dan verandert je bestelbon mee. Zonder dat je er
iets voor hoeft te doen.

## 3. Wanneer koppelen, wanneer niet

| Situatie | Wat je doet |
|---|---|
| Een gegeven dat op meerdere plaatsen nodig is | koppelen |
| Een gegeven dat kan veranderen | koppelen |
| Een prijs die op een verzonden factuur staat | **niet** koppelen |

Die laatste verdient uitleg. Een factuur die de deur uit is, is een vastgelegd document.
Verandert de prijslijst nadien, dan mag die oude factuur **niet** mee veranderen — dat is
je boekhouding. Daarom gebruik je op een afgewerkte factuur **waarden plakken**, zodat de
bedragen bevroren worden.

Koppel dus terwijl je werkt, en bevries wanneer je verstuurt.

## Veelgemaakte fouten

- **Een prijs overtypen "omdat het sneller gaat"** — het gaat sneller tot het misgaat.
- **De volgorde van de bron wijzigen** nadat je per rij gekoppeld hebt. Daarover gaat de
  volgende les.
- **Een afgewerkt document gekoppeld laten** — dan verandert je boekhouding achteraf.
$md$,
  'f6-prijzen-koppelen', true
where not exists (select 1 from lessen where oefening_id = 'f6-prijzen-koppelen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 6, 2,
  'Koppelen op code, niet op positie',
  'Waarom een koppeling per rij breekt, en hoe VERT.ZOEKEN dat oplost.',
$md$
## Wat je na deze les kunt

- Uitleggen waarom een koppeling per rijnummer riskant is
- Koppelen op basis van een code
- Een zoektabel zo opbouwen dat ze blijft werken

## 1. De zwakke plek van een gewone koppeling

`=Prijslijst!C4` betekent: *"neem wat er toevallig in rij 4 staat"*. Dat klopt zolang
niemand aan de prijslijst raakt.

Voegt een collega bovenaan een artikel toe, dan schuift alles één rij op. Jouw bestelbon
toont nu de prijs van het artikel ernaast. Geen foutmelding, geen kleur — gewoon
verkeerde bedragen.

## 2. Koppel op iets dat niet verschuift

Een **artikelcode** hoort bij het artikel, waar het in de lijst ook staat. Zoek daarop:

```
=VERT.ZOEKEN(A4;Prijslijst!$A$4:$C$9;3;ONWAAR)
```

Nu maakt de volgorde van de prijslijst niet meer uit. Verhuist `CM-225` naar boven, dan
vindt je formule hem daar gewoon.

## 3. Wanneer welke

| Situatie | Koppeling |
|---|---|
| Beide lijsten hebben exact dezelfde volgorde, en dat blijft zo | `=Prijslijst!C4` |
| De volgorde kan verschillen of veranderen | `VERT.ZOEKEN` |
| Je lijst bevat maar een deel van de artikelen | `VERT.ZOEKEN` |

In de praktijk is dat bijna altijd de tweede. Een directe koppeling gebruik je voor één
losse waarde — een btw-tarief, een drempelbedrag — niet voor een lijst.

## 4. Eis: een unieke code

`VERT.ZOEKEN` neemt de **eerste** treffer. Staat een code twee keer in je prijslijst, dan
krijg je altijd de bovenste, en merk je nooit dat er een tweede was.

Controleer dus dat je codekolom uniek is. Dat is geen formaliteit: dubbele codes zijn een
van de vaakst voorkomende oorzaken van foute facturen.

## Veelgemaakte fouten

- **Koppelen per rij bij een lijst die kan veranderen.**
- **De zoekkolom niet als eerste kolom van de tabel** — `VERT.ZOEKEN` kijkt alleen rechts.
- **Dubbele codes in de bron.**
$md$,
  'f6-koppelen-zoeken', true
where not exists (select 1 from lessen where oefening_id = 'f6-koppelen-zoeken');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 6, 3,
  'Consolideren: cijfers samenbrengen',
  'Van drie afzonderlijke bladen naar één overzicht dat vanzelf bijblijft.',
$md$
## Wat je na deze les kunt

- Een overzichtstabel opbouwen uit meerdere bronbladen
- Totalen in twee richtingen berekenen
- Je consolidatie controleren met een kruistelling

## 1. Wat consolideren is

Elk filiaal houdt zijn eigen blad bij. Consolideren is die cijfers samenbrengen in één
tabel, zonder ze over te typen. Elke cel van je overzicht is een koppeling naar het
juiste bronblad.

Het resultaat is een tabel die **vanzelf bijblijft**. Vult een filiaal zijn cijfer aan,
dan staat het meteen in het overzicht.

## 2. Totalen in twee richtingen

Een consolidatietabel heeft twee soorten totalen:

- **Per rij**: het kwartaaltotaal van één filiaal — `=SOM(B4:D4)`
- **Per kolom**: het maandtotaal van alle filialen — `=SOM(B4:B6)`

En in de hoek rechtsonder staat het eindtotaal.

## 3. De kruistelling

Hier zit een gratis controle in. Dat eindtotaal kun je op twee manieren berekenen:

- als som van de rijtotalen
- als som van de kolomtotalen

**Die twee moeten gelijk zijn.** Zijn ze dat niet, dan mist er ergens een cel in een
bereik, of telt er een cel dubbel mee. Het is de snelste manier om een fout in een grote
tabel te vinden.

## 4. Sleep je totalen door

Typ `=SOM(B4:B6)` in B7 en voer door naar rechts. De kolomletters schuiven mee:
`=SOM(C4:C6)`, `=SOM(D4:D6)`. Eén formule, drie totalen.

Doorvoeren werkt in alle richtingen: naar beneden, naar rechts, en ook naar links en
boven.

## Veelgemaakte fouten

- **Het bereik van een totaal laten meelopen tot in de totaalrij** — dan tel je dubbel.
- **Een filiaal vergeten** bij het uitbreiden van de tabel.
- **De kruistelling niet doen** — je enige gratis controle overslaan.
$md$,
  'f6-consolideren', true
where not exists (select 1 from lessen where oefening_id = 'f6-consolideren');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 6, 4,
  'Koppelingen controleren en herstellen',
  'Hoe je een fout vindt die er niet als een fout uitziet.',
$md$
## Wat je na deze les kunt

- Een verdachte koppeling herkennen zonder foutmelding
- Systematisch nagaan of een verwijzing klopt
- De drie meest voorkomende koppelingsfouten benoemen

## 1. De gevaarlijkste fouten zijn stil

`#VERW!` of `#N/B` zijn vervelend, maar eerlijk: je ziet ze staan. Veel erger is een
koppeling die een **geldig maar verkeerd** getal ophaalt. Daar is niets aan te zien.

Drie klassiekers:

| Fout | Wat je ziet | Wat er scheelt |
|---|---|---|
| Verkeerde cel | een plausibel getal | `=Roeselare!B4` haalt één maand op in plaats van het totaal in B8 |
| Verkeerd blad | een plausibel getal | `=Izegem!B8` staat op de rij van Kortrijk |
| Verschoven bereik | klopt bovenaan, fout onderaan | dollartekens vergeten |

## 2. Hoe je controleert

Klik op de cel en **lees de formulebalk**. Dat is de enige plaats waar je ziet wat er
echt staat. Drie vragen:

1. Klopt de **bladnaam** met de rij waar ik sta?
2. Klopt het **celadres** met wat ik wil ophalen?
3. Klopt het bij de **buren** — voeren de cellen erboven en eronder dezelfde logica?

Die derde vraag vangt de meeste fouten. Staat er in B4 `=Roeselare!B8` en in B5
`=Izegem!B5`, dan springt de afwijking eruit zodra je ze naast elkaar leest.

## 3. Een snelle steekproef

Neem één cel en reken haar met de hand na. Klopt die, neem dan de onderste rij — daar
komen verschoven bereiken aan het licht. Twee cellen controleren kost een halve minuut
en vangt het merendeel.

## 4. Voorkomen is beter

- Geef je bladen **korte, duidelijke namen**.
- Bouw elk blad **identiek** op, zodat dezelfde cel hetzelfde betekent.
- Typ formules niet over maar **voer ze door**, zodat ze allemaal dezelfde vorm hebben.

## Veelgemaakte fouten

- **Alleen kijken of er een getal staat** in plaats van welk getal.
- **Een formule per cel overtypen** — elke cel is dan een nieuwe kans op een fout.
- **De onderste rij niet controleren.**
$md$,
  'f6-herstellen', true
where not exists (select 1 from lessen where oefening_id = 'f6-herstellen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 6, 5,
  'Een document waarin niets dubbel staat',
  'Alles samen: koppelen, opzoeken, voorwaarden en instellingen die je op één plaats bewaart.',
$md$
## Wat je na deze les kunt

- Een document ontwerpen waarin elk gegeven maar één keer voorkomt
- Instellingen apart zetten en er absoluut naar verwijzen
- Een berekening opbouwen in logische stappen

## 1. Het ontwerp

Een goed opgebouwde factuur bestaat uit drie soorten cellen:

| Soort | Voorbeeld | Waar |
|---|---|---|
| **Invoer** | artikelcode, aantal | in de factuurlijnen |
| **Instellingen** | btw-tarief, drempel, kortingspercentage | apart, onderaan of op een eigen blad |
| **Berekend** | omschrijving, prijs, bedragen, btw | formules — nooit met de hand |

Alles wat berekend kan worden, wordt berekend. Wat je moet kunnen aanpassen, staat op
één duidelijke plaats.

## 2. Instellingen apart, en absoluut

Het btw-tarief hoort niet in je formule maar in een cel:

```
=(E11-E12)*$B$15
```

Zo pas je het tarief op één plaats aan als de wetgeving verandert, en hoef je niet
zeventien formules na te lopen. De dollartekens zorgen dat die verwijzing blijft staan
bij het doorvoeren.

## 3. Bouw op in stappen

Probeer een factuur niet in één formule te proppen. Elke stap krijgt zijn eigen cel:

1. Subtotaal — `=SOM(E5:E9)`
2. Korting — `=ALS(E11>$B$16;E11*$B$17;0)`
3. Btw op het bedrag **na** korting — `=(E11-E12)*$B$15`
4. Totaal — `=E11-E12+E13`

Elke stap is los te controleren. Klopt het subtotaal, dan hoef je daar niet meer naar te
kijken. En iemand anders kan je werk volgen.

> Let op de volgorde bij stap 3. Btw wordt berekend op het bedrag **na** korting. Zet je
> die twee om, dan factureer je te veel btw — en dat merkt de boekhouding.

## 4. De eindcontrole

Voor je een document doorgeeft:

- Klopt het totaal ongeveer met wat je in je hoofd had?
- Staan alle bedragen in valuta met twee decimalen?
- Zit er ergens een getal dat met de hand is ingetypt terwijl het berekend hoort te zijn?
- Wat gebeurt er als je één aantal wijzigt — volgt alles mee?

Die laatste is de beste test. Verander één aantal en kijk of het totaal meebeweegt. Blijft
er iets staan, dan heb je daar een hardgecodeerd getal.

## Veelgemaakte fouten

- **Btw berekenen vóór de korting.**
- **Een instelling in de formule typen** in plaats van ernaar te verwijzen.
- **Alles in één formule willen proppen** — onleesbaar, en niet te controleren.
$md$,
  'f6-gekoppelde-factuur', true
where not exists (select 1 from lessen where oefening_id = 'f6-gekoppelde-factuur');
-- ---------------------------------------------------------------------
--  FOCUS 8 · Geavanceerde functies — aanvulling
-- ---------------------------------------------------------------------

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 1,
  'HORIZ.ZOEKEN: zoeken in de breedte',
  'Dezelfde logica als VERT.ZOEKEN, maar voor tabellen die liggend zijn opgebouwd.',
$md$
## Wat je na deze les kunt

- Herkennen wanneer je `HORIZ.ZOEKEN` nodig hebt in plaats van `VERT.ZOEKEN`
- De argumenten juist invullen
- Uitleggen waarom liggende tabellen bestaan

## 1. Staand of liggend

`VERT.ZOEKEN` zoekt **naar beneden**, in de eerste kolom van een tabel. Dat werkt als je
gegevens onder elkaar staan — één rij per artikel, per klant, per order.

Soms staan ze naast elkaar: één kolom per maand, per jaar, per schijf. Dan zoek je
**naar rechts**, en gebruik je `HORIZ.ZOEKEN`.

| | Januari | Februari | Maart |
|---|---|---|---|
| **Doel** | 22000 | 21000 | 24000 |
| **Gehaald** | 24500 | 18700 | 26340 |

## 2. De argumenten

```
=HORIZ.ZOEKEN(A11;$B$3:$G$5;2;ONWAAR)
```

| Argument | Wat het is |
|---|---|
| `A11` | wat je zoekt — hier een maandnaam |
| `$B$3:$G$5` | de tabel |
| `2` | de hoeveelste **rij** van die tabel je wil |
| `ONWAAR` | exact zoeken |

Het verschil met `VERT.ZOEKEN` zit in dat derde argument: daar tel je **rijen** in plaats
van kolommen. `HORIZ.ZOEKEN` zoekt in de **eerste rij** van de tabel en geeft iets terug
uit een rij eronder.

## 3. Alles wat je al wist, geldt nog

- Tabel **absoluut** maken, anders schuift ze mee bij het doorvoeren
- Afsluiten met **ONWAAR** om exact te zoeken
- De zoekwaarde moet in de **eerste rij** van de tabel staan

## 4. En X.ZOEKEN dan?

`X.ZOEKEN` kan beide richtingen aan en heeft geen aparte horizontale versie nodig. Toch
moet je `HORIZ.ZOEKEN` kennen: op stage kom je documenten tegen waarin ze gebruikt is, en
op oudere Excel-versies is er geen alternatief.

## Veelgemaakte fouten

- **`VERT.ZOEKEN` gebruiken op een liggende tabel** — je krijgt `#N/B`.
- **Kolommen tellen in plaats van rijen** bij het derde argument.
- **De koprij niet in het bereik opnemen** — de zoekwaarde moet erin staan.
$md$,
  'f8-horiz-zoeken', true
where not exists (select 1 from lessen where oefening_id = 'f8-horiz-zoeken');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 3,
  'Tekst uit elkaar halen: LINKS, RECHTS en LENGTE',
  'Stukken uit een code halen, zonder te knippen en te plakken.',
$md$
## Wat je na deze les kunt

- Een vast aantal tekens uit het begin of het einde van een tekst halen
- Tellen hoeveel tekens er in een cel staan
- Een tekstfunctie combineren met `ALS`

## 1. Waarvoor het dient

Oude systemen leveren vaak alles in één veld aan: `ROE-1042-A`. Daar zitten drie gegevens
in — de stad, het klantnummer en de categorie — maar ze staan aan elkaar geplakt.

Met de hand uit elkaar halen kan bij vijf regels. Bij vijfhonderd niet.

## 2. De drie functies

| Functie | Wat ze doet | Voorbeeld op `ROE-1042-A` |
|---|---|---|
| `=LINKS(A4;3)` | de eerste 3 tekens | `ROE` |
| `=RECHTS(A4;1)` | het laatste teken | `A` |
| `=LENGTE(A4)` | hoeveel tekens er zijn | `10` |

`LINKS` en `RECHTS` willen weten **hoeveel** tekens je wil. `LENGTE` telt gewoon, en heeft
alleen de cel nodig.

## 3. Het resultaat is tekst

Let op: wat deze functies teruggeven is **tekst**, ook als het op een getal lijkt.
`=LINKS("1042-A";4)` geeft `"1042"`, en daar kun je niet zomaar mee rekenen.

Moet je er toch mee rekenen, zet er dan `WAARDE()` omheen, of vermenigvuldig met 1.

## 4. Combineren met ALS

De categorie uit de code halen is pas nuttig als je er iets mee doet:

```
=ALS(C4="A";"Voorrang";"Gewoon")
```

Of in één keer, zonder tussenkolom:

```
=ALS(RECHTS(A4;1)="A";"Voorrang";"Gewoon")
```

Die tweede is korter, maar de eerste is makkelijker te controleren. Bij twijfel: zet de
tussenstap in een eigen kolom. Je kunt ze altijd later verbergen.

## 5. Let op spaties

Een spatie is een teken. `=LENGTE("ROE ")` geeft 4, niet 3. Komt je vergelijking niet
uit terwijl alles er goed uitziet, dan zit er vaak een spatie te veel in. `SPATIES.WISSEN`
haalt die weg.

## Veelgemaakte fouten

- **Rekenen met het resultaat** zonder het eerst naar een getal om te zetten.
- **Verkeerd tellen** — `LINKS(A4;3)` geeft drie tekens, niet drie plus één.
- **Onzichtbare spaties** die een vergelijking laten mislukken.
$md$,
  'f8-tekstfuncties', true
where not exists (select 1 from lessen where oefening_id = 'f8-tekstfuncties');

-- De bestaande Focus 8-lessen kregen nog een doorlopend nummer uit de oude
-- reeks; binnen hun eigen Focus horen ze op 2 en 4.
update lessen set volgnummer = 2 where oefening_id = 'xzoeken-artikelen' and volgnummer <> 2;
update lessen set volgnummer = 4 where oefening_id = 'geneste-functies' and volgnummer <> 4;


-- ---------------------------------------------------------------------
--  FOCUS 3 · Afdrukken
--
--  Deze vijf horen bij de oefeningen die in echt Excel gemaakt worden.
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 3, 1,
  'Van scherm naar papier: stand en marges',
  'Waarom een blad dat er op het scherm goed uitziet, op papier uit elkaar valt — en wat je eraan doet.',
$md$
## Wat je na deze les kunt

- Zien hoe je blad op papier valt vóór je iets afdrukt
- Kiezen tussen staand en liggend
- De marges instellen, en weten wat "Smal" precies verandert

> Deze oefening maak je in **Excel zelf**. Een browser kent geen pagina’s, dus
> afdrukinstellingen bestaan alleen in het echte programma. Op stage werk je daar toch mee.

## 1. Een scherm schuift, papier niet

Op het scherm scrol je gewoon verder naar rechts tot je de laatste kolom ziet. Je merkt
nauwelijks hoe breed je tabel is.

Papier heeft een rand. Alles wat niet past, schuift naar een volgende pagina. Het
klassieke resultaat: vier pagina’s met de tabel, en een vijfde met één eenzame kolom
*Bedrag* erop. Niemand kan daar iets mee.

## 2. Kijk eerst, druk dan af

Druk op **Ctrl+P**. Je krijgt het afdrukvoorbeeld. Kijk onderaan: daar staat
*1 van 4*. Dat getal is je controle — vóór je papier verbruikt.

Ben je één keer in dat voorbeeld geweest, dan verschijnen er **stippellijnen** in je blad.
Dat zijn de paginagrenzen. Handig: nu zie je meteen welke kolom er net naast valt.

## 3. Staand of liggend

| Je tabel | Afdrukstand |
|---|---|
| Meer rijen dan kolommen, smal | **Staand** (portret) |
| Veel kolommen naast elkaar, breed | **Liggend** (landschap) |

Je vindt het bij **Pagina-indeling › Afdrukstand**.

Een lijst met zeven kolommen — leveringsnummer, klant, artikel, datum, aantal, prijs,
bedrag — is breed. Die zet je liggend. Dat is de eerste ingreep, nog vóór je aan marges
of schalen denkt.

## 4. Marges

De marge is de witte rand rond je tabel. **Pagina-indeling › Marges** geeft je drie
kant-en-klare keuzes:

| Keuze | Links en rechts | Boven en onder |
|---|---|---|
| Normaal | 1,8 cm | 1,9 cm |
| Breed | 2,5 cm | 2,5 cm |
| **Smal** | **0,64 cm** | 1,9 cm |

Let op wat *Smal* wél en niet doet: het maakt de **zijkanten** veel smaller, maar laat
boven en onder ongemoeid. Dat is ook logisch — je wint plaats in de breedte, en dat is
net waar een brede tabel plaats tekortkomt.

Met liggend én smalle marges win je samen al snel drie kolommen.

## Veelgemaakte fouten

- **Afdrukken zonder voorbeeld.** Twintig bladen papier later weet je het ook.
- **Kolommen versmallen tot alles past.** Dan past het, maar leest niemand het nog.
  Zet het blad liggend; daarover gaat ook de volgende les.
- **Marges op 0 cm zetten.** Geen enkele printer drukt tot tegen de rand; je verliest
  gewoon de buitenste tekens.
$md$,
  'f3-stand-en-marges', true
where not exists (select 1 from lessen where oefening_id = 'f3-stand-en-marges');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 3, 2,
  'Passend maken: laten krimpen zonder te knoeien',
  'Alle kolommen op één pagina breed, met de juiste instelling in plaats van met trucjes.',
$md$
## Wat je na deze les kunt

- Een tabel laten krimpen tot ze in de breedte past
- Het verschil uitleggen tussen "één pagina breed" en "op één pagina"
- Zien waarom kolommen verbergen geen oplossing is

## 1. Liggend volstaat niet altijd

Je tabel staat liggend, de marges zijn smal, en tóch valt de laatste kolom ernaast. Dan
is er maar één nette oplossing: Excel de tabel laten **schalen**, dus alles evenredig wat
kleiner afdrukken.

## 2. Aanpassen aan

Op het tabblad **Pagina-indeling** staat een groepje met drie vakjes:

```
Breedte:  1 pagina
Hoogte:   Automatisch
Schaal:   (wordt vanzelf ingevuld)
```

Zet **Breedte** op *1 pagina*. Excel rekent zelf uit hoeveel procent er nodig is — bv. 78 %
— en vult dat in bij Schaal.

**Laat Hoogte op Automatisch staan.** Zet je die ook op 1 pagina, dan moet Excel 75 rijen
én 7 kolommen op één blad persen. Het resultaat is leesbaar met een vergrootglas.

> Kort samengevat: **één pagina breed, zoveel pagina’s hoog als nodig.** Een lange lijst
> mag gerust over vijf bladen lopen, zolang elke rij volledig op één blad staat.

## 3. Schalen of "Aanpassen aan"?

Je kunt ook met de hand een percentage invullen bij *Vergroten/verkleinen*. Dat werkt,
maar je moet het zelf blijven bijstellen. Komen er rijen of kolommen bij, dan klopt je
percentage niet meer.

*Aanpassen aan* is slimmer: die instelling blijft kloppen, ook als de lijst groeit.

## 4. Wat je níét doet

| Trucje | Waarom niet |
|---|---|
| Kolommen verbergen | De gegevens zijn weg uit je rapport. Wie het leest, weet dat niet. |
| Lettertype op 6 punten | Het past, maar het is onleesbaar. |
| Kolommen supersmal maken | Getallen worden `####`, of tekst valt af. |

Schalen doet hetzelfde als een kleiner lettertype, maar **evenredig en over alles tegelijk** —
en het blijft op het scherm gewoon normaal groot.

## 5. Pagina-einde-voorbeeld

Wil je precies zien waar Excel de pagina’s legt, kies dan **Beeld › Pagina-einde-voorbeeld**.
Je ziet je blad met blauwe lijnen erdoor, en je kunt die lijnen **verslepen**. Excel past
de schaal dan zelf aan.

## Veelgemaakte fouten

- **Hoogte ook op 1 pagina zetten.** Dan wordt het onleesbaar klein.
- **Een percentage invullen en het vergeten bij te werken** als er rijen bijkomen.
- **Vergeten liggend te zetten** en dan klagen dat de schaal zo klein wordt.
$md$,
  'f3-passend-maken', true
where not exists (select 1 from lessen where oefening_id = 'f3-passend-maken');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 3, 3,
  'Kop- en voettekst: elke pagina herkenbaar',
  'Een titel bovenaan en een paginanummer onderaan, automatisch op elke afgedrukte pagina.',
$md$
## Wat je na deze les kunt

- Een kop- en voettekst instellen
- Een paginanummer laten meelopen
- De codes herkennen die Excel daarvoor gebruikt

## 1. Waarom

Een rapport van tien pagina’s valt op de grond. Als er niets op staat, is de volgorde
weg. Staat er op elke pagina *Leveringen september — Pagina 4 van 10*, dan is het in tien
seconden weer gesorteerd.

Daarom staat op zo goed als elk zakelijk rapport een koptekst en een paginanummer. Dat is
geen opsmuk; dat is bruikbaarheid.

## 2. Kop- en voettekst staan niet in cellen

Dit is het punt waar het bij de meesten misloopt. Een koptekst is **geen rij 1** van je
blad. Het is een aparte laag die alleen bij het afdrukken bestaat.

Zet je je titel gewoon in cel A1, dan staat hij op pagina 1 — en nergens anders.

Je stelt het in via **Invoegen › Kop- en voettekst**. Excel schakelt dan over naar de
weergave *Pagina-indeling*, waar je bovenaan en onderaan drie invulvakken ziet.

## 3. Drie vakken, boven en onder

| Vak | Wat er gewoonlijk in staat |
|---|---|
| Links | de firmanaam, of de datum |
| Midden | de titel van het rapport |
| Rechts | het paginanummer |

Je mag zelf kiezen, maar houd het consequent door heel het rapport.

## 4. De codes

Typ je gewoon `Pagina 1`, dan staat er op élke pagina "Pagina 1". Je hebt een code nodig
die meetelt. Excel heeft daar knoppen voor, maar in het vak zie je de code verschijnen:

| Code | Wat het wordt |
|---|---|
| `&P` | het paginanummer |
| `&N` | het totaal aantal pagina’s |
| `&D` | de datum van afdrukken |
| `&F` | de bestandsnaam |
| `&A` | de naam van het werkblad |

Voor de oefening typ je in het rechtervak van de voettekst:

```
Pagina &P van &N
```

Op papier wordt dat *Pagina 4 van 10*.

## Veelgemaakte fouten

- **De titel in cel A1 zetten** en denken dat dat een koptekst is.
- **"Pagina 1" letterlijk typen** in plaats van `&P` te gebruiken.
- **Een koptekst instellen op het verkeerde werkblad.** Elk blad heeft zijn eigen kop- en
  voettekst.
$md$,
  'f3-kop-en-voettekst', true
where not exists (select 1 from lessen where oefening_id = 'f3-kop-en-voettekst');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 3, 4,
  'Titelrijen herhalen op elke pagina',
  'De koprij laten terugkomen op pagina twee, drie en vier — en waarom dat iets anders is dan beeld vastzetten.',
$md$
## Wat je na deze les kunt

- Een koprij op elke afgedrukte pagina laten herhalen
- Het verschil uitleggen tussen beeld vastzetten en afdruktitels

## 1. Het probleem

Pagina 1 van je afdruk is perfect: bovenaan staat *Leveringsnummer, Klant, Artikel,
Datum, Aantal, Eenheidsprijs, Bedrag*.

Pagina 3 is een blad vol getallen zonder één woord uitleg. Welke kolom was het aantal,
welke de prijs? Niemand die het nog weet.

## 2. Vastzetten is niet hetzelfde als herhalen

In Focus 1 heb je **beeld vastzetten** geleerd: de koprij blijft staan terwijl je scrolt.
Dat is prettig, maar het is een instelling **voor het scherm**. Op papier verandert er
niets van.

| Wat je wilt | Waar je het instelt |
|---|---|
| Koprij blijft staan tijdens het scrollen | Beeld › Blokkeren (Focus 1) |
| Koprij komt terug op elke afgedrukte pagina | Pagina-indeling › **Afdruktitels** |

Twee verschillende instellingen, voor twee verschillende doelen. Je hebt ze allebei nodig.

## 3. Afdruktitels instellen

Ga naar **Pagina-indeling › Afdruktitels**. Er opent een venster met twee velden:

```
Rijen om boven aan elke pagina te herhalen:    $3:$3
Kolommen om links op elke pagina te herhalen:  (leeg laten)
```

Klik in het veld en klik dan op **rijkop 3** in je blad. Excel vult zelf `$3:$3` in.

De dollartekens zijn hier geen keuze: afdruktitels worden altijd absoluut genoteerd. Dat
is hetzelfde principe als bij een absolute celverwijzing uit Focus 2.

> Staat je koptekst over twee rijen? Dan herhaal je `$2:$3`. Je mag een bereik van rijen
> opgeven, zolang het aaneensluitende rijen zijn.

## 4. Kolommen herhalen

Het tweede veld doet hetzelfde in de breedte. Bij een tabel die over meerdere pagina’s
naar rechts loopt, herhaal je zo de kolom met de namen. Bij de oefening laat je dat veld
leeg: daar zorg je er met *Aanpassen aan* voor dat alles op één pagina breed staat.

## Veelgemaakte fouten

- **Beeld vastzetten en denken dat het geregeld is.** Dat geldt alleen voor het scherm.
- **Rij 1 herhalen in plaats van rij 3.** In deze bestanden staat de titel op rij 1 en de
  eigenlijke koprij op rij 3. Kijk dus even welke rij de kolomnamen bevat.
- **De rijnummers intypen als `3:3`** zonder dollartekens. Klik liever gewoon op de rijkop;
  dan vult Excel het correct in.
$md$,
  'f3-titelrijen', true
where not exists (select 1 from lessen where oefening_id = 'f3-titelrijen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 3, 5,
  'Een printklaar rapport: de volgorde van werken',
  'Alles van dit blok samen, in de volgorde die het minste werk kost.',
$md$
## Wat je na deze les kunt

- Een lijst volledig klaarmaken om af te drukken
- In de juiste volgorde werken, zodat je niets twee keer doet

## 1. De volgorde

Je kunt deze instellingen in willekeurige volgorde aanzetten, maar dan stel je de schaal
drie keer opnieuw in. Werk zo:

1. **Afdrukstand** — liggend bij een brede tabel
2. **Marges** — Smal
3. **Aanpassen aan** — Breedte 1 pagina, Hoogte automatisch
4. **Afdruktitels** — rij 3 boven aan elke pagina
5. **Kop- en voettekst** — titel in het midden, `Pagina &P van &N` rechts
6. **Controleren** — Ctrl+P

Stap 1 en 2 maken plaats. Pas daarna laat je Excel de schaal berekenen — anders rekent
hij op de oude, te smalle pagina.

## 2. Afdrukbereik

Wil je maar een deel van het blad afdrukken, selecteer dat dan en kies
**Pagina-indeling › Afdrukbereik › Afdrukbereik instellen**.

Vanaf dan drukt Excel *alleen* dat bereik af. Handig, maar ook een klassieke valkuil:
komen er later rijen bij, dan vallen die buiten het afdrukbereik en verschijnen ze niet
op papier. Zonder waarschuwing.

## 3. Rasterlijnen en koppen

Standaard drukt Excel de grijze rasterlijnen **niet** af. Bij een tabel met echte randen
is dat prima. Bij een ruwe lijst zonder opmaak is het vaak onleesbaar.

Bij **Pagina-indeling › Rasterlijnen › Afdrukken** zet je ze aan. Daarnaast staat
*Koppen*, dat de rij- en kolomletters meedrukt — dat doe je alleen bij een controlelijst,
nooit bij een rapport dat de deur uit gaat.

## 4. De laatste controle

Ga naar het afdrukvoorbeeld en kijk vier dingen na:

- Staat er **1 van N** onderaan, en is N een redelijk getal?
- Staat op **pagina 2** de koprij?
- Staat het **paginanummer** onderaan?
- Valt er **geen enkele kolom** naast de rand?

Pas als die vier kloppen, is je rapport klaar om door te geven.

## Veelgemaakte fouten

- **De schaal instellen vóór je liggend zet.** Dan mag je opnieuw beginnen.
- **Een afdrukbereik laten staan** nadat de lijst gegroeid is.
- **Alleen pagina 1 controleren.** Net op pagina 2 zie je of je titelrijen werken.
$md$,
  'f3-printklaar-rapport', true
where not exists (select 1 from lessen where oefening_id = 'f3-printklaar-rapport');


-- ---------------------------------------------------------------------
--  FOCUS 4 · Grafieken
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 4, 1,
  'Van tabel naar grafiek',
  'Je selectie bepaalt alles. Wat je aanduidt vóór je op Invoegen klikt, is wat er in de grafiek komt.',
$md$
## Wat je na deze les kunt

- Van een tabel een grafiek maken
- De juiste cellen selecteren, inclusief de koptekst
- Een grafiek een titel geven

> Deze oefening maak je in **Excel zelf**. Grafieken zitten niet in het rekenblad hier in
> de browser — en op stage maak je ze toch in het echte programma.

## 1. Waarom een grafiek

Twaalf getallen in een kolom zijn correct, maar je moet ze lezen en vergelijken. Diezelfde
twaalf getallen als staafjes zie je in één oogopslag: welke maand er uitsprong, waar de
dip zat.

De zaakvoerder leest je tabel niet. Je grafiek wel.

## 2. Je selectie bepaalt de grafiek

Dit is het hele geheim. Excel maakt een grafiek van **wat je geselecteerd hebt**, niets
meer en niets minder. Selecteer je verkeerd, dan helpt achteraf bijsturen weinig — opnieuw
beginnen gaat sneller.

Voor een tabel met maanden in kolom A en omzet in kolom B selecteer je:

```
A3:B9
```

Dus: de **koprij** (rij 3) plus de zes maanden met hun omzet.

## 3. Neem de koptekst mee

Waarom rij 3 erbij? Omdat Excel daaruit de **naam van de reeks** haalt. Selecteer je alleen
A4:B9, dan heet je reeks "Reeks1". Met de koptekst erbij heet ze *Omzet*, en dat is wat er
in de legende komt te staan.

Het kost je één rij extra in je selectie en het scheelt achteraf handwerk.

## 4. Invoegen

Met je selectie actief: **Invoegen › Kolom** (het icoontje met de staafjes). Kies het
eerste, gewone type: *Gegroepeerde kolom*.

Excel zet de grafiek als een kader over je blad. Je kunt hem verslepen en aan de hoeken
groter maken.

## 5. Een titel geven

Boven de grafiek staat *Grafiektitel*. Klik erop, selecteer de tekst en typ de jouwe —
voor deze oefening: **Omzet per maand**.

Een grafiek zonder titel is onbruikbaar zodra ze uit haar context gehaald wordt, en dat
gebeurt altijd: ze wordt gekopieerd in een mail, een verslag, een presentatie.

## 6. De grafiek blijft gekoppeld

Verander je een getal in B5, dan beweegt de staaf mee. Je hoeft niets opnieuw te maken.
Dat is hetzelfde principe als bij een formule: verwijzen in plaats van overtypen.

## Veelgemaakte fouten

- **De koprij niet meeselecteren**, waardoor je reeks "Reeks1" heet.
- **De titelcel in A1 meeselecteren.** Die hoort niet bij je gegevens en maakt er een
  rommeltje van. Begin je selectie bij de koprij.
- **De grafiektitel laten staan op "Grafiektitel".**
$md$,
  'f4-staafdiagram', true
where not exists (select 1 from lessen where oefening_id = 'f4-staafdiagram');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 4, 2,
  'Het juiste type kiezen',
  'Kolom, lijn of cirkel: de vraag die je stelt bepaalt het type, niet je smaak.',
$md$
## Wat je na deze les kunt

- Het grafiektype kiezen dat bij je vraag past
- Uitleggen waarom een lijn een verloop toont en een staaf niet

## 1. De vraag bepaalt het type

| Je vraag | Type |
|---|---|
| Hoeveel per maand, per filiaal, per artikel? | **Kolom** of staaf |
| Gaat het de goede kant op? Hoe evolueert het? | **Lijn** |
| Welk aandeel heeft elk deel van het geheel? | **Cirkel** |

Meer keuzes zijn er in de praktijk zelden nodig. De rest van het menu — radar, trechter,
oppervlakte — gebruik je pas als je een goede reden hebt.

## 2. Kolom: hoeveelheden vergelijken

Staven staan naast elkaar en zijn even breed. Je oog vergelijkt automatisch de
**hoogtes**. Daarom is een kolomdiagram het beste antwoord op "welke maand was de beste".

## 3. Lijn: een verloop tonen

Een lijn verbindt de punten. Dat verbinden is precies wat je wilt zeggen: *dit gaat
over in dat*. Je ziet de richting — stijgend, dalend, schommelend.

Gebruik een lijn dus zodra de horizontale as **tijd** is: maanden, kwartalen, jaren.

> Hetzelfde cijfermateriaal, een andere boodschap. Een staafdiagram van de omzet per maand
> zegt *"mei was de beste maand"*. Een lijndiagram van diezelfde cijfers zegt
> *"de omzet klimt sinds februari"*. Kies het type dat past bij wat je wil vertellen.

## 4. Een lijn hoort niet overal

Zet je filialen — Roeselare, Izegem, Kortrijk, Tielt — op een lijn, dan suggereer je dat
Izegem "tussen" Roeselare en Kortrijk ligt. Dat betekent niets. Er is geen volgorde en
geen overgang tussen filialen.

Regel: **alleen een lijn als de as een volgorde heeft.** Tijd heeft dat. Namen niet.

## Veelgemaakte fouten

- **Een lijn gebruiken voor categorieën** zonder natuurlijke volgorde.
- **Een 3D-type kiezen omdat het mooier lijkt.** Het perspectief vervormt de hoogtes; je
  leest er minder nauwkeurig op af.
- **Een type kiezen en de titel vergeten aanpassen** aan wat de grafiek nu toont.
$md$,
  'f4-lijndiagram', true
where not exists (select 1 from lessen where oefening_id = 'f4-lijndiagram');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 4, 3,
  'Cirkeldiagram: delen van één geheel',
  'Wanneer een cirkel het juiste antwoord is — en wanneer hij liegt.',
$md$
## Wat je na deze les kunt

- Een cirkeldiagram maken
- Beoordelen of een cirkel hier wel op zijn plaats is

## 1. Eén geheel, verdeeld in stukken

Een cirkeldiagram toont **aandelen**. De hele cirkel is 100 %, en elke taartpunt is een
deel daarvan.

Dat werkt alleen als je cijfers echt samen één geheel vormen. De omzet van je vier
filialen samen is de totale omzet — dat klopt. Je kunt dus tonen dat Kortrijk een goeie
derde van alles doet.

## 2. Wanneer een cirkel niet mag

| Situatie | Waarom niet |
|---|---|
| De delen vormen geen geheel | 100 % betekent dan niets |
| Meer dan ongeveer zes stukken | De punten worden te dun om te lezen |
| Negatieve getallen | Een negatieve taartpunt bestaat niet |
| Je wil twee periodes vergelijken | Twee cirkels naast elkaar leest niemand |

In elk van die gevallen neem je een kolomdiagram.

## 3. Maken

Selecteer de namen én hun waarden — met de koprij erbij, net als bij een staafdiagram —
en kies **Invoegen › Cirkel**.

Geef hem een titel die zegt wat het geheel ís: *Aandeel per filiaal*. Niet gewoon
"Omzet": bij een cirkel gaat het om de verdeling, niet om het bedrag.

## 4. Percentages erbij

Een cirkel zonder cijfers laat je schatten. Klik met de rechtermuisknop op de taart en
kies **Gegevenslabels toevoegen**. Via *Gegevenslabels opmaken* kun je kiezen voor
**Percentage** in plaats van de absolute waarde.

Dat is meestal de betere keuze: bij een cirkel wil de lezer de verhouding weten.

## Veelgemaakte fouten

- **Een cirkel gebruiken voor cijfers die geen geheel vormen** — bv. de omzet van drie
  willekeurige artikelen uit een catalogus van duizend.
- **Twaalf maanden in een cirkel.** Dat is een kolomdiagram, of een lijn.
- **Het totaal meeselecteren.** Staat er onderaan een rij *Totaal*, laat die dan buiten je
  selectie — anders is de helft van je cirkel het totaal zelf.
$md$,
  'f4-cirkeldiagram', true
where not exists (select 1 from lessen where oefening_id = 'f4-cirkeldiagram');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 4, 4,
  'Een grafiek afwerken',
  'Alles erop zetten wat een buitenstaander nodig heeft om ze te begrijpen zonder uitleg.',
$md$
## Wat je na deze les kunt

- De onderdelen van een grafiek benoemen en aan- of uitzetten
- De klassieke valkuil herkennen waarbij je categorieën een tweede reeks worden

## 1. De test

Kopieer je grafiek in gedachten naar een mail aan iemand die je bestand nooit gezien
heeft. Begrijpt die persoon ze? Zo niet, dan ontbreekt er iets.

Meestal is dat de titel, en soms de eenheid.

## 2. De onderdelen

| Onderdeel | Wanneer nodig |
|---|---|
| **Grafiektitel** | altijd |
| **Legende** | zodra er meer dan één reeks is |
| **Astitels** | als de eenheid niet vanzelf spreekt (euro, stuks, %) |
| **Gegevenslabels** | bij weinig punten, of bij een cirkel |
| **Rasterlijnen** | om hoogtes te kunnen aflezen; laat ze licht |

Je zet ze aan met de **+** rechts naast de geselecteerde grafiek: *Grafiekelementen*.

Bij één reeks zet je de legende juist **uit**. Die zegt dan alleen "Omzet", wat de titel
al vertelt, en hij neemt plaats in.

## 3. De valkuil: je maanden worden een tweede reeks

Dit overkomt iedereen een keer. Je maakt een grafiek en ziet twee reeksen staan, terwijl
je er maar één verwachtte — en op de horizontale as staat 1, 2, 3, 4, 5, 6 in plaats van
de maanden.

Dat gebeurt als Excel je eerste kolom voor **cijfers** aanziet in plaats van voor labels.
Typisch bij jaartallen of bij artikelnummers.

Zo los je het op:

1. Klik de grafiek aan
2. **Grafiekontwerp › Gegevens selecteren**
3. Rechts staat *Horizontale aslabels*: klik **Bewerken** en selecteer je maandenkolom
4. Links staat je reeksenlijst: verwijder daar de reeks die eigenlijk je labels zijn

## 4. Wat de grafiek hier moet worden

Voor deze oefening: een kolomdiagram met de zes maanden onder de staven, één reeks omzet,
en de titel **Omzet eerste halfjaar 2026**.

## Veelgemaakte fouten

- **De standaardtitel laten staan.**
- **Een legende laten staan bij één reeks.**
- **De grafiek zo klein maken** dat de labels schuin gedraaid worden of wegvallen.
$md$,
  'f4-grafiek-opmaken', true
where not exists (select 1 from lessen where oefening_id = 'f4-grafiek-opmaken');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 4, 5,
  'Twee reeksen vergelijken',
  'Omzet en kosten naast elkaar in één grafiek, zodat je ziet waar de marge krimpt.',
$md$
## Wat je na deze les kunt

- Twee gegevensreeksen in één grafiek zetten
- Een reeks toevoegen of verwijderen zonder opnieuw te beginnen
- Zien wanneer een tweede as nodig is

## 1. Waarom twee reeksen

Een omzet van 27 960 euro zegt op zich niets. Staan de kosten van diezelfde maand er
naast, dan zie je wat overblijft. En zet je dat voor zes maanden naast elkaar, dan zie je
of de marge groeit of krimpt.

Dat is het hele nut van een tweede reeks: **vergelijken**.

## 2. Gewoon meer selecteren

Je hoeft niets nieuws te leren. Waar je vorige keer twee kolommen selecteerde, selecteer je
er nu drie:

```
A3:C9
```

Maanden, omzet én kosten — met de koprij erbij, want daar komen nu de twee namen in de
legende vandaan.

Dan **Invoegen › Kolom**. Excel zet per maand twee staafjes naast elkaar.

## 3. De legende wordt noodzakelijk

Bij één reeks zette je de legende uit. Bij twee reeksen **moet** ze erop: anders weet
niemand welk staafje de omzet is.

Controleer ook dat er *Omzet* en *Kosten* staat, en niet *Reeks1* en *Reeks2*. Staat dat
laatste er, dan heb je de koprij niet meegenomen.

## 4. Een reeks bijsturen

Vergeten? Je hoeft niet opnieuw te beginnen. Klik de grafiek aan en kies
**Grafiekontwerp › Gegevens selecteren**. In het linkervak staan je reeksen; met
*Toevoegen* en *Verwijderen* pas je ze aan.

Daar zit ook **Rij/kolom omdraaien**. Handig als Excel de maanden als reeksen genomen
heeft en de omzet en kosten als categorieën — precies andersom dan je wilde.

## 5. Wanneer een tweede as

Liggen twee reeksen heel ver uit elkaar — omzet in tienduizenden, aantal orders in
tientallen — dan is de kleine reeks een plat streepje onderaan.

Dan geef je die tweede reeks een **secundaire as**: rechtermuisknop op de reeks,
*Gegevensreeks opmaken*, en kies *Secundaire as*.

Wees er voorzichtig mee: twee assen betekent twee schalen, en dat leest niet iedereen
goed. Voor omzet tegenover kosten — allebei in euro, allebei dezelfde grootteorde —
heb je het niet nodig.

## Veelgemaakte fouten

- **Twee losse grafieken maken** in plaats van één met twee reeksen. Dan kun je niet
  vergelijken.
- **De koprij vergeten**, waardoor de legende "Reeks1" en "Reeks2" toont.
- **Een secundaire as gebruiken waar het niet hoeft**, waardoor het lijkt alsof de kosten
  even hoog zijn als de omzet.
$md$,
  'f4-twee-reeksen', true
where not exists (select 1 from lessen where oefening_id = 'f4-twee-reeksen');


-- ---------------------------------------------------------------------
--  FOCUS 7 · Draaitabellen
-- ---------------------------------------------------------------------
insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 7, 1,
  'Je eerste draaitabel',
  'Uit een lijst van achtenveertig lijnen in vijf seconden een samenvatting halen, zonder één formule.',
$md$
## Wat je na deze les kunt

- Uitleggen wat een draaitabel doet
- Beoordelen of je brongegevens geschikt zijn
- Een eerste draaitabel maken met rijen en waarden

> Deze oefening maak je in **Excel zelf**. Draaitabellen zitten niet in het rekenblad hier
> in de browser. Ze zijn ook precies het soort werk dat je op stage krijgt: "geef mij eens
> de omzet per filiaal".

## 1. Wat een draaitabel doet

Je hebt een lijst met 48 verkooplijnen. De vraag: **hoeveel omzet per filiaal?**

Met wat je al kent, kan dat: `SOM.ALS` per filiaal, vier formules, en je moet de
filiaalnamen zelf opzoeken en overtypen. Komt er een vijfde filiaal bij, dan mag je
opnieuw.

Een draaitabel doet hetzelfde met slepen. Ze zoekt zelf welke filialen er bestaan, telt
per filiaal de omzet op, en zet er een totaal onder. Komt er een filiaal bij, dan staat
het er na één keer vernieuwen gewoon bij.

**Draaien** betekent: dezelfde cijfers langs een andere kant bekijken.

## 2. Eerst: is je lijst geschikt?

Een draaitabel stelt eisen aan de brongegevens. Dit is het deel dat mensen overslaan, en
het is meteen de reden waarom het bij hen niet lukt.

| Eis | Waarom |
|---|---|
| Eén rij met kolomnamen, en maar één | Die namen worden je veldnamen |
| Geen lege rijen of lege kolommen middenin | Excel denkt dat je lijst daar stopt |
| Geen samengevoegde cellen | Die hebben geen eenduidige waarde |
| Eén gegeven per kolom | Datum en klant samen in één cel kun je niet draaien |
| Eén feit per rij | Elke rij is één verkoop |

In de oefenbestanden staat de titel op rij 1, een lege rij 2, en de kolomnamen op rij 3.
Klik daarom **in de tabel zelf** (bv. in A4) voor je begint; Excel herkent dan het juiste
bereik.

## 3. Invoegen

Klik ergens in de tabel en kies **Invoegen › Draaitabel**. Excel toont het herkende
bereik — controleer dat even — en vraagt waar de tabel moet komen. Kies
**Nieuw werkblad**. Dat houdt je brongegevens ongemoeid.

## 4. De vier gebieden

Rechts verschijnt het veldenpaneel: bovenaan je kolomnamen, onderaan vier vakken.

| Gebied | Wat je erin sleept | Wat je krijgt |
|---|---|---|
| **Rijen** | Filiaal | één rij per filiaal, onder elkaar |
| **Kolommen** | Maand | één kolom per maand, naast elkaar |
| **Waarden** | Omzet | de cijfers in het midden |
| **Filters** | Verkoper | een keuzelijst bovenaan |

Voor deze oefening: sleep **Filiaal** naar *Rijen* en **Omzet** naar *Waarden*. Klaar.
Je hebt vier regels met de omzet per filiaal en een eindtotaal.

## 5. Vernieuwen

Dit is belangrijk. Een draaitabel is een **momentopname**. Verander je iets in de
brongegevens, dan past de draaitabel zich **niet** vanzelf aan — anders dan een formule.

Klik met de rechtermuisknop in de draaitabel en kies **Vernieuwen**, of gebruik
*Draaitabelanalyse › Vernieuwen*.

> Maak er een gewoonte van: vernieuwen vóór je een rapport doorgeeft. Een draaitabel met
> cijfers van vorige week ziet er precies even betrouwbaar uit als een actuele.

## Veelgemaakte fouten

- **Lege rijen in de brongegevens**, waardoor maar de helft meetelt.
- **De titelrij meeselecteren** in plaats van in de tabel te klikken.
- **Vergeten te vernieuwen** nadat de brongegevens veranderd zijn.
$md$,
  'f7-eerste-draaitabel', true
where not exists (select 1 from lessen where oefening_id = 'f7-eerste-draaitabel');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 7, 2,
  'Rijen en kolommen combineren',
  'Twee kenmerken tegelijk bekijken: per filiaal én per maand, in één kruistabel.',
$md$
## Wat je na deze les kunt

- Een kruistabel maken met rijen en kolommen
- Kiezen welk veld waar hoort
- De totalen juist lezen

## 1. Twee vragen tegelijk

"Hoeveel omzet per filiaal" is één vraag, en die heb je opgelost. "Hoeveel omzet per
filiaal, per maand" zijn er eigenlijk twee tegelijk.

Daarvoor bestaat het **kolomgebied**. Zet je Filiaal in de rijen en Maand in de kolommen,
dan krijg je een rooster:

|  | Januari | Februari | Maart | Eindtotaal |
|---|---|---|---|---|
| **Izegem** | 12 400 | 9 800 | 11 200 | 33 400 |
| **Kortrijk** | 18 900 | 17 300 | 21 050 | 57 250 |
| **Roeselare** | 15 600 | 16 100 | 14 800 | 46 500 |
| **Tielt** | 8 200 | 7 900 | 9 400 | 25 500 |
| **Eindtotaal** | 55 100 | 51 100 | 56 450 | 162 650 |

Elk vakje is een doorsnede: *Kortrijk in maart*. Dat heet een **kruistabel**.

## 2. Wat hoort in de rijen, wat in de kolommen?

Technisch mag het allebei. Praktisch is er een vuistregel:

| Gebied | Neem het veld met… |
|---|---|
| **Rijen** | veel verschillende waarden, of lange namen |
| **Kolommen** | weinig waarden, en korte namen |

Twaalf maanden in de kolommen geeft een tabel die niet op je scherm past. Twaalf maanden
in de rijen leest prima. Vier filialen met namen als *Roeselare* horen dus in de rijen,
en drie maanden in de kolommen.

Je kunt het altijd omdraaien: sleep de velden gewoon naar het andere vak. Dat kost geen
seconde — dat is wat "draaien" betekent.

## 3. De drie soorten totalen

- Rechts de **rijtotalen**: alles van dat filiaal samen
- Onderaan de **kolomtotalen**: alles van die maand samen
- In de hoek rechtsonder het **eindtotaal**

Het eindtotaal moet gelijk zijn aan de som van je hele bronkolom. Is dat niet zo, dan
zitten er lege rijen in je brongegevens of staat er een filter aan.

> Dat is meteen een gratis controle: tel de omzetkolom in je bronblad met `SOM` op en
> vergelijk met het eindtotaal van de draaitabel. Wijkt het af, dan klopt er iets niet.

## 4. Meer dan één veld per gebied

Je mag twee velden in de rijen zetten, bv. Filiaal en daaronder Productgroep. Dan krijg je
een genest overzicht: per filiaal uitgesplitst per groep.

Dat is krachtig, maar hou het overzichtelijk. Drie velden in de rijen en twee in de
kolommen levert een tabel op die niemand meer leest.

## Veelgemaakte fouten

- **Een veld met veel waarden in de kolommen zetten**, waardoor de tabel kilometers breed wordt.
- **Het eindtotaal niet controleren.**
- **Denken dat je iets kapotmaakt door te slepen.** Je brongegevens blijven altijd intact;
  proberen kost niets.
$md$,
  'f7-kruistabel', true
where not exists (select 1 from lessen where oefening_id = 'f7-kruistabel');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 7, 3,
  'Niet altijd optellen: Som, Aantal, Gemiddelde',
  'Excel kiest zelf een functie, en dat is niet altijd de juiste. Zo verander je ze.',
$md$
## Wat je na deze les kunt

- De samenvattingsfunctie van een waardeveld veranderen
- Uitleggen waarom Excel soms Aantal kiest in plaats van Som
- Het verschil tussen Aantal en Aantal getallen

## 1. Excel raadt

Sleep je een veld naar *Waarden*, dan kiest Excel zelf wat ermee moet gebeuren:

| Wat je sleept | Wat Excel doet |
|---|---|
| Een kolom met getallen (Omzet) | **Som** |
| Een kolom met tekst (Ordernummer, Klant) | **Aantal** |

Dat is meestal handig. Maar niet altijd — en je ziet het aan de kop van de kolom, waar
*Som van Omzet* of *Aantal van Ordernummer* staat.

## 2. Als het raden fout is

De vraag "hoeveel orders per productgroep" gaat niet over een bedrag. Je wil **tellen**.

Sleep je dan Ordernummer naar Waarden, dan kiest Excel Aantal — precies goed. Maar
bevatten je ordernummers alleen cijfers, dan ziet Excel getallen, kiest hij Som, en krijg
je de optelsom van je ordernummers. Een getal dat nergens op slaat.

## 3. De functie veranderen

Klik op het veld in het vak *Waarden* en kies **Waardeveldinstellingen**. Daar staat de
lijst:

| Functie | Wat ze doet |
|---|---|
| **Som** | telt op |
| **Aantal** | telt hoeveel rijen er zijn |
| **Gemiddelde** | het gemiddelde |
| **Max** / **Min** | de hoogste of laagste waarde |

Kies wat bij je vraag hoort. Voor deze oefening: **Aantal**.

> Het kan ook sneller: rechtermuisknop op een cel in de waardenkolom ›
> *Waarden samenvatten als* › Aantal.

## 4. Aantal tegenover Aantal getallen

Twee keuzes die op elkaar lijken:

- **Aantal** telt alle gevulde cellen, ook tekst
- **Aantal getallen** telt alleen cellen met een getal erin

Dat is exact hetzelfde onderscheid als tussen `AANTALARG` en `AANTAL`, dat je in Focus 2
gezien hebt. Staat er in je kolom hier en daar "n.v.t.", dan geven de twee een ander
resultaat.

## 5. Hernoem de kop

*Aantal van Ordernummer* is lelijk in een rapport. Klik de kop aan en typ er
**Aantal orders** over.

Eén voorwaarde: de nieuwe naam mag niet exact gelijk zijn aan een bestaande veldnaam. Zet
er desnoods een spatie achter, of gebruik een iets andere formulering.

## Veelgemaakte fouten

- **Ordernummers optellen** omdat Excel Som koos.
- **Denken dat een fout getal aan de brongegevens ligt**, terwijl de functie fout staat.
  Kijk altijd eerst naar de kop: staat er Som of Aantal?
- **De kop laten staan als "Som van Omzet"** in een rapport dat de deur uit gaat.
$md$,
  'f7-samenvattingsfunctie', true
where not exists (select 1 from lessen where oefening_id = 'f7-samenvattingsfunctie');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 7, 4,
  'Filteren in een draaitabel',
  'Een deel van de cijfers bekijken zonder de brongegevens aan te raken.',
$md$
## Wat je na deze les kunt

- Een veld in het filtergebied zetten
- Een slicer toevoegen
- Uitleggen waarom filteren je brongegevens niet verandert

## 1. Filteren verandert niets aan je gegevens

Een filter is een **bril**, geen ingreep. Je kijkt naar een deel van de cijfers; alles
blijft staan waar het stond. Zet je het filter weer op *Alles*, dan is je volledige
overzicht terug.

Dat is het grote verschil met rijen verwijderen "omdat ze nu niet nodig zijn". Filteren is
altijd omkeerbaar.

## 2. Het filtergebied

Sleep een veld naar het vak **Filters** — bv. Verkoper. Boven je draaitabel verschijnt
dan een keuzelijst:

```
Verkoper    (Alle)  ▾
```

Kies je *An Peeters*, dan toont je hele draaitabel alleen haar verkopen. Rijen, kolommen,
totalen — alles rekent mee.

Zo bouw je één tabel die de verkoopleider voor elke verkoper kan gebruiken, in plaats van
drie aparte tabellen.

> Vink **Meerdere items selecteren** aan om er twee of drie tegelijk te kiezen.

## 3. Slicers: hetzelfde, maar zichtbaar

Een nadeel van het filtergebied: aan de keuzelijst zie je niet meteen of er gefilterd is.
Iemand die je bestand doorkrijgt, leest cijfers van één verkoper zonder het door te hebben.

Daarom bestaan **slicers**: knoppenbalken naast je tabel, waarop je in één oogopslag ziet
wat aan- en uitstaat.

Je voegt ze toe via **Draaitabelanalyse › Slicer invoegen**, en dan vink je het veld aan.
Klikken op een knop filtert; nog eens klikken zet het weer af.

Voor deze oefening volstaat het filtergebied. Ken de slicer als het nettere alternatief
voor een rapport dat je doorgeeft.

## 4. Filter of rijgebied?

| Je wil | Waar |
|---|---|
| Per verkoper apart kunnen kijken, één tegelijk | **Filters** |
| Alle verkopers naast elkaar zien en vergelijken | **Rijen** |

Filteren is voor *inzoomen*. Vergelijken doe je door het veld gewoon in de rijen of
kolommen te zetten.

## Veelgemaakte fouten

- **Een filter laten staan** en het rapport zo doorgeven. De cijfers kloppen dan niet met
  het totaal.
- **In de brongegevens rijen wissen** om te "filteren". Dan zijn ze echt weg.
- **Het filterveld in de rijen zetten** en je dan afvragen waarom je alle verkopers ziet.
$md$,
  'f7-filteren', true
where not exists (select 1 from lessen where oefening_id = 'f7-filteren');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 7, 5,
  'Van draaitabel naar rapport',
  'De eindproef: samenvatten, in beeld brengen en printklaar maken — alles van deze cursus samen.',
$md$
## Wat je na deze les kunt

- Een draaigrafiek maken bij een draaitabel
- Een draaitabel netjes opmaken
- Een draaitabel printklaar afwerken

## 1. De draaigrafiek

Klik in je draaitabel en kies **Draaitabelanalyse › Draaigrafiek**. Je krijgt dezelfde
keuze aan types als bij een gewone grafiek.

Het verschil: een draaigrafiek is **gekoppeld aan de draaitabel**. Filter je de tabel, dan
verandert de grafiek mee. Sleep je een veld naar een ander gebied, dan volgt de grafiek.

Voor deze oefening maak je er een van de omzet per filiaal, met de titel
**Omzet per filiaal**. De titel zet je er net zo op als bij een gewone grafiek: erop
klikken en typen.

> Je mag ook een gewone grafiek maken van het bereik van de draaitabel. Dat mag voor deze
> opdracht, maar een draaigrafiek blijft netter: die blijft kloppen als de tabel verandert.

## 2. De tabel leesbaar maken

Een draaitabel komt er functioneel uit, niet mooi. Op het tabblad **Ontwerp** vind je:

| Wat | Waar |
|---|---|
| Kleuren en randen | Draaitabelstijlen |
| Compacte, overzichts- of tabelvorm | Rapportindeling |
| Totalen aan- of uitzetten | Subtotalen / Eindtotalen |

**Rapportindeling › Tabelvorm weergeven** zet elk veld in een eigen kolom met een echte
kop erboven. Dat leest veel beter dan de standaard compacte vorm, zeker als je het
doorgeeft aan iemand anders.

Staan je bedragen als kale getallen? Rechtermuisknop › *Getalnotatie* — niet via de
gewone werkbalk, want die opmaak verdwijnt bij het vernieuwen.

## 3. Printklaar maken

Nu komt Focus 3 terug. Een draaitabel drukt precies zo af als elk ander blad:

1. Liggend
2. Smalle marges
3. **Aanpassen aan › Breedte 1 pagina**
4. Kop- en voettekst met `Pagina &P van &N`

Loopt je draaitabel over meerdere pagina’s, dan is er nog een extra: bij
**Draaitabelanalyse › Opties › Afdrukken** staat *Afdruktitels instellen*. Die zorgt dat
de veldkoppen van de draaitabel op elke pagina terugkomen — het equivalent van de
afdruktitels die je in Focus 3 geleerd hebt.

## 4. Vernieuwen, dan pas doorgeven

De laatste stap, elke keer opnieuw: **vernieuwen**. Een draaitabel toont de cijfers van het
moment waarop ze gemaakt of laatst vernieuwd is.

De volgorde voor een rapport dat de deur uit gaat:

1. Brongegevens nakijken
2. Draaitabel vernieuwen
3. Eindtotaal vergelijken met de `SOM` van je bronkolom
4. Grafiek controleren
5. Afdrukvoorbeeld bekijken

## Veelgemaakte fouten

- **Een niet-vernieuwde draaitabel doorgeven.**
- **De grafiek los van de tabel maken** en hem daarna niet meer bijwerken.
- **Opmaak via de gewone werkbalk** in plaats van via de getalnotatie van het veld —
  weg na het eerste vernieuwen.
$md$,
  'f7-draairapport', true
where not exists (select 1 from lessen where oefening_id = 'f7-draairapport');
