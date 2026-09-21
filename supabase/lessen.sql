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

-- De factuurles hoort op plaats 3 in de reeks.
update lessen set volgnummer = 3 where oefening_id = 'factuur-basis' and volgnummer <> 3;

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
