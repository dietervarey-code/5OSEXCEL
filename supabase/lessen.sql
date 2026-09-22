-- =====================================================================
--  Lessen bij de acht oefeningen
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
