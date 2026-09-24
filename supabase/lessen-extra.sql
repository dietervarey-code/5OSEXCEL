-- =====================================================================
--  Extra theorielessen — losse onderwerpen, zonder eigen oefening
--
--  Deze lessen horen niet bij één oefening: ze vullen onderwerpen aan uit de
--  cursus waar wel theorie voor nodig is, maar geen aparte opdracht.
--
--  Uitvoeren in Supabase › SQL Editor, ná supabase/lessen.sql.
--  Mag meermaals draaien: een les die al bestaat wordt overgeslagen.
--
--  Let op de controle onderaan elke les: die kijkt naar de TITEL, niet naar
--  oefening_id. Deze lessen hebben namelijk geen oefening, en in SQL is
--  "null = null" nooit waar — een controle op oefening_id zou dus bij elke
--  run opnieuw invoegen.
-- =====================================================================

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 0,
  'Werkmap, werkblad, cel en bereik',
  'De woorden die je nodig hebt om de rest te begrijpen — en om uit te leggen wat er misging.',
$md$## Wat je na deze les kunt

- De onderdelen van een rekenblad bij naam noemen
- Een cel en een bereik correct aanduiden
- Uitleggen wat het verschil is tussen een werkmap en een werkblad

## 1. Waarom woorden ertoe doen

Op stage zeg je niet "dat vakje daar, links van dat andere". Je zegt: *"in cel D12"*.
Met de juiste woorden los je een probleem in één zin op; zonder die woorden ben je vijf
minuten aan het wijzen.

## 2. De onderdelen

| Woord | Wat het is |
|---|---|
| **Werkmap** | Het bestand. Eén `.xlsx` is één werkmap. |
| **Werkblad** | Een tabblad in dat bestand. Eén werkmap kan er tientallen hebben. |
| **Kolom** | Staat rechtop, heeft een **letter**: A, B, C … |
| **Rij** | Ligt horizontaal, heeft een **nummer**: 1, 2, 3 … |
| **Cel** | Het kruispunt van een kolom en een rij: **D12** |
| **Bereik** | Een rechthoek van cellen: **D4:D11** |

Onthoud de volgorde in een celadres: **eerst de letter, dan het cijfer**. `D12`, nooit
`12D`.

## 3. Het bereik en de dubbele punt

De dubbele punt betekent **tot en met**:

| Bereik | Wat het is |
|---|---|
| `D4:D11` | acht cellen onder elkaar in kolom D |
| `A3:G3` | zeven cellen naast elkaar in rij 3 |
| `A3:G9` | een rechthoek van 7 kolommen op 7 rijen |

En de puntkomma betekent **en ook**: `=SOM(D4:D11;F4:F11)` telt twee losse bereiken samen op.

## 4. Over de bladgrens heen

Verwijs je naar een cel op een ander werkblad, dan zet je de bladnaam ervoor met een
uitroepteken:

```
=Januari!D10
```

Staat er een spatie in de bladnaam, dan komen er apostroffen omheen: `='Januari 2026'!D10`.
Daar gaat Focus 5 verder op in.

## 5. Het naamvak

Links boven je blad, naast de formulebalk, staat een klein vak met het adres van de cel
waar je staat. Dat is het **naamvak**.

Je kunt er ook in typen: tik `D250`, druk op Enter, en je springt erheen. Bij een lange
lijst is dat sneller dan scrollen.

## Veelgemaakte fouten

- **Werkmap en werkblad door elkaar halen.** De werkmap is het bestand, het werkblad is
  het tabblad.
- **Een bereik met een puntkomma schrijven** waar een dubbele punt hoort. `D4;D11` zijn
  twee losse cellen, `D4:D11` zijn er acht.
- **Het rijnummer eerst zetten.**
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Werkmap, werkblad, cel en bereik');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 6,
  'Een werkblad beveiligen',
  'Bepalen wie wat mag wijzigen — en waarom je eerst de invulcellen vrijgeeft.',
$md$## Wat je na deze les kunt

- Een werkblad beveiligen
- De cellen vrijgeven die wél ingevuld mogen worden
- De volgorde uitleggen waarin dat moet gebeuren

## 1. Waarom

Je maakt een bestelformulier voor een collega. Die moet een aantal en een klantnaam
invullen — en verder niets. Zonder beveiliging overschrijft hij op een dag je formule met
een getal, en valt je hele berekening om. Zonder foutmelding.

Beveiligen is dus geen wantrouwen; het is je eigen werk beschermen tegen een ongelukje.

## 2. Het punt dat iedereen mist

Elke cel in Excel staat standaard op **geblokkeerd**. Dat lijkt vreemd — je kunt toch
gewoon overal typen?

Dat klopt, want *geblokkeerd* doet pas iets zodra je het blad beveiligt. Beveilig je het
blad meteen, dan staat **alles** op slot en kan niemand nog iets invullen.

De volgorde is dus omgekeerd aan wat je zou verwachten:

1. **Eerst** de cellen die wél ingevuld mogen worden **deblokkeren**
2. **Daarna** pas het blad beveiligen

## 3. Zo doe je het

**Stap 1 — de invulcellen vrijgeven.** Selecteer ze, druk **Ctrl+1** (Celeigenschappen),
ga naar het tabblad **Bescherming** en haal het vinkje bij **Geblokkeerd** weg.

**Stap 2 — het blad beveiligen.** Ga naar **Controleren › Blad beveiligen**. Je mag een
wachtwoord instellen, en je vinkt aan wat er nog wel mag.

Vanaf nu kan iemand alleen nog in de cellen die je hebt vrijgegeven. Probeert hij een
formule te overschrijven, dan krijgt hij een melding.

> **Een wachtwoord hier is geen beveiliging tegen kwaad opzet.** Het beschermt tegen
> vergissingen. Vergeet je het wachtwoord zelf, dan geraak je er ook niet meer in — noteer
> het dus ergens.

## 4. Formules verbergen

Op datzelfde tabblad **Bescherming** staat ook **Verborgen**. Vink je dat aan, dan is de
formule na het beveiligen niet meer te zien in de formulebalk; het resultaat blijft wel
staan.

Handig voor een prijsberekening die je niet wil prijsgeven.

## Veelgemaakte fouten

- **Het blad beveiligen zonder eerst te deblokkeren**, en dan concluderen dat er niets
  meer werkt.
- **Het wachtwoord vergeten.**
- **Denken dat beveiligen het bestand versleutelt.** Dat is iets anders: dat is
  *Bestand › Info › Werkmap beveiligen › Versleutelen met wachtwoord*.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Een werkblad beveiligen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 1, 7,
  'Sneltoetsen die tijd winnen',
  'Een handvol toetsencombinaties die op stage het verschil maken tussen tien minuten en één.',
$md$## Wat je na deze les kunt

- Sneller door een lange lijst bewegen
- De sneltoetsen gebruiken die je elke dag nodig hebt

## 1. Bewegen en selecteren

Dit is waar de meeste tijd te winnen valt. Een lijst van 800 rijen scrol je niet.

| Toetsen | Wat het doet |
|---|---|
| `Ctrl` + pijl | springt naar het einde van de gevulde reeks |
| `Ctrl` + `Shift` + pijl | **selecteert** tot het einde van de reeks |
| `Ctrl` + `Home` | terug naar A1 |
| `Ctrl` + `End` | naar de laatste gevulde cel |

Met `Ctrl+Shift+pijl omlaag` selecteer je een kolom van duizend rijen in één tik — precies
wat je nodig hebt voor een `SOM` of een grafiek.

## 2. Invullen en bewerken

| Toetsen | Wat het doet |
|---|---|
| `F2` | de cel bewerken zonder opnieuw te typen |
| `Ctrl` + `Enter` | vult je typwerk in **alle** geselecteerde cellen |
| `Alt` + `=` | zet er automatisch een `SOM` onder |
| `Ctrl` + `;` | zet de datum van vandaag als vaste waarde |
| `Ctrl` + `1` | Celeigenschappen (opmaak, notatie, bescherming) |

`F2` is er één die je snel mist zodra je hem kent. Klik je een gevulde cel aan en begin je
te typen, dan gooi je de inhoud weg. Met `F2` zet je de cursor in wat er al staat.

## 3. F4: twee verschillende dingen

`F4` doet iets anders naargelang waar je zit:

- **Terwijl je een formule typt**, met de cursor op een celverwijzing: het wisselt tussen
  `A1` → `$A$1` → `A$1` → `$A1` → `A1`. Dat spaart je het typen van dollartekens.
- **Buiten een formule**: het herhaalt je laatste handeling. Heb je net een rij
  ingekleurd, dan kleurt `F4` de volgende ook.

## 4. En verder

| Toetsen | Wat het doet |
|---|---|
| `Ctrl` + `Z` | ongedaan maken |
| `Ctrl` + `T` | van je lijst een opgemaakte tabel maken |
| `Ctrl` + `P` | afdrukvoorbeeld |
| `Ctrl` + `Shift` + `L` | filterknopjes aan- en uitzetten |

> **In het rekenblad hier in de browser werken niet al deze toetsen.** Sommige combinaties
> pakt je browser zelf af. Leer ze voor Excel: daar werken ze allemaal, en daar zit je op
> stage.

## Veelgemaakte fouten

- **Slepen met de muis over duizend rijen** in plaats van `Ctrl+Shift+pijl`.
- **Een cel overtypen** in plaats van `F2` te gebruiken.
- **Dollartekens met de hand typen** in plaats van `F4`.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Sneltoetsen die tijd winnen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 7,
  'Gemengde celverwijzing: $A1 en A$1',
  'De derde soort verwijzing: één helft staat vast, de andere schuift mee.',
$md$## Wat je na deze les kunt

- Het verschil uitleggen tussen `A1`, `$A$1`, `A$1` en `$A1`
- Een kruistabel invullen met één formule

## 1. Waar het dollarteken staat, staat iets vast

Je kent er al twee uit Focus 2:

| Schrijfwijze | Wat er meeschuift |
|---|---|
| `A1` | **relatief** — allebei schuiven mee |
| `$A$1` | **absoluut** — er schuift niets mee |

Maar het dollarteken werkt per helft. Dat geeft nog twee mogelijkheden:

| Schrijfwijze | Kolom | Rij |
|---|---|---|
| `A$1` | schuift mee | **staat vast** |
| `$A1` | **staat vast** | schuift mee |

Het dollarteken hoort bij wat er **achter** staat. In `A$1` staat het voor de 1, dus de
**rij** ligt vast.

## 2. Waarvoor je dat nodig hebt

Neem een tabel waarin je voor elk artikel de prijs met 5 %, 10 % en 15 % wil verhogen:

|  | **B** 5 % | **C** 10 % | **D** 15 % |
|---|---|---|---|
| **A4** 12,50 | | | |
| **A5** 8,00 | | | |

De percentages staan in **rij 3**, de prijzen in **kolom A**. In B4 zet je:

```
=$A4*(1+B$3)
```

- `$A4` — de kolom met prijzen ligt vast, de rij schuift mee naar beneden
- `B$3` — de rij met percentages ligt vast, de kolom schuift mee naar rechts

Nu mag je die ene formule in **twee richtingen** doorvoeren, en overal klopt hij. Eén
formule voor de hele tabel, in plaats van twaalf.

## 3. Hoe je ze typt

Zet de cursor op de verwijzing en druk op **F4**. Je fietst door de vier mogelijkheden:

```
A1  →  $A$1  →  A$1  →  $A1  →  A1
```

Stop waar je moet zijn. Dat is sneller en betrouwbaarder dan de dollartekens zelf typen.

## 4. Welke moet vaststaan?

Stel jezelf per helft één vraag: *"als ik deze formule doorvoer, moet dit dan meeschuiven?"*

- Voer je naar **beneden** door, dan schuiven de **rijnummers**. Wat niet mag schuiven,
  krijgt een `$` voor zijn cijfer.
- Voer je naar **rechts** door, dan schuiven de **kolomletters**. Wat niet mag schuiven,
  krijgt een `$` voor zijn letter.

## Veelgemaakte fouten

- **Overal `$A$1` zetten "voor de zekerheid".** Dan schuift er niets meer mee en staat
  overal hetzelfde antwoord.
- **Het dollarteken aan de verkeerde helft zetten.** Controleer altijd één cel verderop of
  de formule nog naar de juiste plaats wijst.
- **Vergeten dat je in twee richtingen doorvoert**, en alleen naar beneden testen.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Gemengde celverwijzing: $A1 en A$1');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 8,
  'Foutmeldingen lezen',
  'Een rekenblad dat een fout toont, vertelt je precies wat er scheelt — als je de code kunt lezen.',
$md$## Wat je na deze les kunt

- De courante foutmeldingen herkennen
- Per melding weten waar je moet kijken

## 1. Een foutmelding is een aanwijzing

`#WAARDE!` in een cel voelt als falen. Het is het tegenovergestelde: het rekenblad heeft
gemerkt dat er iets niet klopt en zegt het meteen. Veel erger is een formule die een
verkeerd antwoord geeft **zonder** te klagen.

Elke code wijst naar een ander soort probleem. Leer ze lezen en je zoekt gericht in plaats
van overal.

## 2. De courante meldingen

| Melding | Wat er aan de hand is | Waar je kijkt |
|---|---|---|
| `######` | Geen fout — de kolom is te smal | Maak de kolom breder |
| `#DEEL/0!` | Je deelt door nul of door een lege cel | De cel onder de deelstreep |
| `#NAAM?` | Het rekenblad kent die naam niet | Een typfout in de functienaam, of tekst zonder aanhalingstekens |
| `#WAARDE!` | Verkeerd soort gegeven | Je rekent met een cel waar tekst in staat |
| `#N/B` | Niet gevonden | Je zoekfunctie vindt de waarde niet |
| `#VERW!` | Verwijzing naar iets dat er niet meer is | Je hebt een rij of kolom verwijderd |
| `#GETAL!` | Een getal dat niet kan | Bv. de wortel uit een negatief getal |

## 3. De drie die je het vaakst zult zien

**`#NAAM?`** is bijna altijd een typfout: `=SMO(A1:A5)` in plaats van `=SOM(A1:A5)`. Het
komt ook voor als je tekst vergeet tussen aanhalingstekens te zetten: `=ALS(A1>10;ja;nee)`
moet `=ALS(A1>10;"ja";"nee")` zijn.

**`#WAARDE!`** betekent dat er tekst zit waar een getal hoort. Vaak is de boosdoener
onzichtbaar: een spatie achter een getal, of een getal dat als tekst is ingevoerd. Zulke
cellen staan meestal links uitgelijnd terwijl echte getallen rechts staan — dat is je
aanwijzing.

**`#N/B`** komt van `VERT.ZOEKEN` of `X.ZOEKEN` die niets vindt. Drie klassieke oorzaken:
de code bestaat echt niet, er staat een spatie te veel, of je zoekt een getal terwijl de
tabel tekst bevat (of omgekeerd).

## 4. Een fout netjes opvangen

Soms is `#N/B` terecht en wil je gewoon niet dat het op je factuur staat. Bij `X.ZOEKEN`
kun je zelf zeggen wat er dan moet komen:

```
=X.ZOEKEN(A4;Prijslijst!A:A;Prijslijst!C:C;"niet gevonden")
```

Doe dat met mate. Een fout wegwerken die je niet begrepen hebt, is hetzelfde als het
waarschuwingslampje in je auto afplakken.

## 5. In dit portaal

Let op: het nakijken hier geeft **geen punten** voor een cel met een foutmelding erin,
ook niet als de formule er verder goed uitziet. Los de fout dus eerst op.

## Veelgemaakte fouten

- **`######` aanzien voor een fout.** Sleep gewoon de kolomrand breder.
- **Een fout laten staan** omdat "de rest toch klopt".
- **`#N/B` wegwerken met een standaardwaarde** zonder eerst te kijken waarom er niets
  gevonden werd.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Foutmeldingen lezen');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 5,
  'Werken met datums: VANDAAG, JAAR, MAAND en DAG',
  'Waarom een datum eigenlijk een getal is, en wat je daarmee kunt.',
$md$## Wat je na deze les kunt

- Uitleggen waarom je met datums kunt rekenen
- `VANDAAG`, `JAAR`, `MAAND` en `DAG` gebruiken
- Het aantal dagen tussen twee datums berekenen

## 1. Een datum is een getal

Dit is de sleutel tot alles wat volgt. Achter `15/09/2026` zit gewoon een getal: het
aantal dagen sinds 1 januari 1900. De datumnotatie is alleen een **weergave** — precies
hetzelfde idee als bij valuta in Focus 1.

Wil je het zien? Zet een cel met een datum eens op de notatie *Standaard*. Je krijgt een
getal van vijf cijfers.

Daarom kun je met datums rekenen alsof het gewone getallen zijn.

## 2. Het aantal dagen tussen twee datums

Trek ze gewoon van elkaar af:

```
=B4-A4
```

Staat in A4 de factuurdatum en in B4 de betaaldatum, dan krijg je het aantal dagen
ertussen. Eén valkuil: het **resultaat** krijgt vaak ook een datumnotatie mee. Zet die
cel op *Standaard* en je ziet het getal.

En een datum een week later:

```
=A4+7
```

## 3. De functies

| Functie | Wat ze geeft |
|---|---|
| `=VANDAAG()` | de datum van vandaag |
| `=JAAR(A4)` | het jaartal uit een datum: 2026 |
| `=MAAND(A4)` | het maandnummer: 9 |
| `=DAG(A4)` | de dag van de maand: 15 |

`VANDAAG()` heeft **lege haakjes**, en dat hoort zo: de functie heeft geen gegevens nodig.
De haakjes weglaten geeft `#NAAM?`.

## 4. Vandaag verandert elke dag

`=VANDAAG()` rekent zichzelf opnieuw uit telkens als het bestand opengaat. Dat is precies
wat je wil voor *"hoeveel dagen staat deze factuur open?"*:

```
=VANDAAG()-A4
```

Maar het is precies wat je **niet** wil op een factuur die verstuurd is. Daar hoort een
vaste datum. Gebruik dan `Ctrl+;` — die zet de datum van vandaag als een vaste waarde, die
nooit meer verandert.

> Kort: `VANDAAG()` voor een overzicht dat moet meebewegen, `Ctrl+;` voor een document dat
> moet vastliggen. Hetzelfde onderscheid als tussen koppelen en waarden plakken in Focus 6.

## 5. Een voorbeeld dat je op stage tegenkomt

Een openstaande factuur moet binnen 30 dagen betaald zijn. Staat de factuurdatum in A4:

```
=ALS(VANDAAG()-A4>30;"vervallen";"loopt nog")
```

Dat is een geneste functie zoals in Focus 8: een berekening binnen een `ALS`.

## Veelgemaakte fouten

- **`=VANDAAG` zonder haakjes** — dat geeft `#NAAM?`.
- **Het verschil tussen twee datums als datum laten staan**, waardoor er 12/01/1900 komt
  in plaats van 12.
- **`VANDAAG()` op een verstuurd document** gebruiken, waardoor de datum blijft opschuiven.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Werken met datums: VANDAAG, JAAR, MAAND en DAG');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 6,
  'Meerdere voorwaarden: EN, OF en NIET',
  'Twee eisen tegelijk in één ALS, zonder een formule van drie regels.',
$md$## Wat je na deze les kunt

- `EN` en `OF` gebruiken binnen een `ALS`
- Kiezen welke van de twee je nodig hebt

## 1. Eén ALS, meer dan één eis

In Focus 2 schreef je `=ALS(B5>100;"ja";"nee")`. Eén voorwaarde, één test.

Maar de werkelijkheid heeft er vaak twee: *korting geldt vanaf 100 euro **én** alleen voor
vaste klanten*. Daarvoor bestaan `EN` en `OF`.

## 2. Het verschil in één tabel

| Functie | Waar is het resultaat WAAR? |
|---|---|
| `EN(...)` | als **alle** voorwaarden kloppen |
| `OF(...)` | als **minstens één** voorwaarde klopt |
| `NIET(...)` | draait het om: waar wordt onwaar |

Lees `EN` als *"en ook"*, en `OF` als *"of anders"*. Dat is meteen het hele verschil.

## 3. Zo schrijf je het

De voorwaarden komen tussen de haakjes, gescheiden door een puntkomma:

```
=ALS(EN(B5>100;C5="vast");"korting";"geen korting")
```

Lees het van binnen naar buiten:

1. `B5>100` — is het bedrag groter dan 100?
2. `C5="vast"` — is het een vaste klant?
3. `EN(...)` — kloppen **allebei**?
4. `ALS(...)` — zo ja, dan "korting", anders "geen korting"

Met `OF` ziet het er net zo uit, maar dan volstaat één van de twee:

```
=ALS(OF(B5>500;C5="vast");"gratis levering";"leveringskosten")
```

## 4. Meer dan twee

Je mag er gerust meer opgeven:

```
=EN(B5>100;C5="vast";D5<>"")
```

Alle drie moeten kloppen. Het teken `<>` betekent **is niet gelijk aan**, dus `D5<>""`
betekent *"D5 is niet leeg"*.

## 5. NIET

`NIET` draait één voorwaarde om:

```
=ALS(NIET(C5="vast");"nieuwe klant";"vaste klant")
```

Je kunt hetzelfde vaak eenvoudiger schrijven met `<>`. Gebruik `NIET` wanneer het je
formule **leesbaarder** maakt, niet omdat het kan.

## 6. Op zichzelf

`EN` en `OF` mogen ook zonder `ALS`. Dan krijg je gewoon `WAAR` of `ONWAAR` in de cel:

```
=EN(B5>100;C5="vast")
```

Handig om te controleren of je voorwaarde klopt, vóór je ze in een `ALS` stopt. Dat is een
goede gewoonte bij een formule die niet doet wat je verwacht: haal hem uit elkaar en test
de stukken apart.

## Veelgemaakte fouten

- **`EN` gebruiken waar `OF` moet staan.** Vraag je af: moeten ze allebei kloppen, of
  volstaat er één?
- **De voorwaarden met een komma scheiden.** In dit portaal mag je puntkomma’s gebruiken,
  net als in de cursus.
- **Tekst vergeten tussen aanhalingstekens**: `C5=vast` geeft `#NAAM?`, het moet
  `C5="vast"` zijn.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Meerdere voorwaarden: EN, OF en NIET');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 7,
  'Gegevensvalidatie: fouten voorkomen bij het invoeren',
  'Een keuzelijst in plaats van vrij typen — zodat er geen "Roeselare " met een spatie in je lijst komt.',
$md$## Wat je na deze les kunt

- Een keuzelijst in een cel zetten
- Grenzen opleggen aan wat er ingevuld mag worden

## 1. Waarom vooraf beter is dan achteraf

Een collega vult een filiaalnaam in. De ene keer *Roeselare*, de andere keer *roeselare*,
en een derde keer *Roeselare* met een spatie erachter.

Voor jou zijn dat drie keer hetzelfde. Voor het rekenblad zijn het drie verschillende
waarden. Je draaitabel toont drie regels, je `VERT.ZOEKEN` geeft `#N/B`, en niemand
begrijpt waarom.

**Gegevensvalidatie** lost dat op aan de bron: je laat gewoon niet toe dat er iets anders
ingetypt wordt.

## 2. Een keuzelijst maken

Zet ergens de toegelaten waarden onder elkaar — bijvoorbeeld op een apart blad
*Instellingen*, in A1:A4.

Selecteer dan de cellen die ingevuld moeten worden en ga naar
**Gegevens › Gegevensvalidatie**. Bij *Toestaan* kies je **Lijst**, en bij *Bron* wijs je
je lijstje aan.

In die cellen staat nu een pijltje. Je collega kiest, en typen kan niet meer.

> Zet je toegelaten waarden in een echte lijst op een blad, niet met de hand getypt in het
> venster. Komt er een filiaal bij, dan vul je gewoon een regel aan — precies hetzelfde
> idee als koppelen in Focus 6: één plaats waar het staat.

## 3. Niet alleen lijsten

Bij *Toestaan* kun je ook kiezen voor:

| Soort | Waarvoor |
|---|---|
| **Geheel getal** | een aantal: minstens 1, hoogstens 500 |
| **Decimaal** | een bedrag binnen een marge |
| **Datum** | een leveringsdatum die in de toekomst ligt |
| **Tekstlengte** | een postcode van precies 4 tekens |

## 4. De twee tabbladen die je niet mag vergeten

In hetzelfde venster:

- **Invoerbericht** — het tekstje dat verschijnt als iemand de cel aanklikt. *"Kies een
  filiaal uit de lijst."* Dat voorkomt de vraag nog vóór ze gesteld wordt.
- **Foutmelding** — wat er gebeurt bij een verkeerde invoer. Zet er een zin in die
  **zegt wat er wél mag**. "Fout" helpt niemand; "Vul een aantal in tussen 1 en 500" wel.

## 5. Wat het niet doet

Validatie werkt bij **typen**. Plakt iemand een waarde uit een ander bestand, dan glipt
die er vaak gewoon door.

Het is dus een goede zeef, geen slot. Wil je echt vastleggen wat er mag gebeuren, dan
combineer je het met een beveiligd werkblad.

## Veelgemaakte fouten

- **De toegelaten waarden met de hand in het venster typen**, waardoor je ze bij elke
  wijziging moet gaan zoeken.
- **Geen foutmelding instellen**, waardoor de standaardmelding verschijnt die niets uitlegt.
- **Denken dat validatie alles tegenhoudt.** Plakken omzeilt het.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Gegevensvalidatie: fouten voorkomen bij het invoeren');

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 8, 8,
  'Voorwaardelijke opmaak',
  'Cellen die zichzelf inkleuren zodra er iets misgaat — zodat je het ziet zonder te zoeken.',
$md$## Wat je na deze les kunt

- Een cel automatisch laten inkleuren op basis van zijn waarde
- Een regel schrijven die naar een andere cel kijkt

## 1. Zien zonder zoeken

Een voorraadlijst van 400 artikelen. De vraag: van welke staan er minder dan tien in stock?

Je kunt sorteren, of filteren. Maar met **voorwaardelijke opmaak** kleuren die regels
zichzelf rood, en zie je het meteen — ook morgen, als de cijfers veranderd zijn.

De opmaak hangt aan de **regel**, niet aan de cel. Verandert de waarde, dan verandert de
kleur mee.

## 2. De snelle manier

Selecteer je kolom en ga naar **Start › Voorwaardelijke opmaak › Regels voor markeren**.
Daar staan de courante gevallen klaar: *Kleiner dan*, *Groter dan*, *Tussen*,
*Gelijk aan*, *Tekst die bevat*.

Kies *Kleiner dan*, vul `10` in, kies een opvulkleur. Klaar.

Daarnaast staat **Boven/onder**, met bijvoorbeeld *Top 10* of *Boven gemiddelde* — handig
om er in één klik de beste klanten uit te lichten.

## 3. Gegevensbalken en kleurenschalen

Onder **Gegevensbalken** en **Kleurenschalen** vind je opmaak die de grootte zelf toont:
een balkje in de cel, of een kleurverloop van rood naar groen.

Dat leest sneller dan cijfers wanneer je alleen de verhoudingen wil zien. Voor een rapport
dat afgedrukt wordt, is het vaak net te druk — daar kies je beter één duidelijke regel.

## 4. Een regel die naar een andere cel kijkt

Dit is de stap die het pas echt bruikbaar maakt. Je wil **de hele rij** kleuren wanneer de
voorraad in kolom D te laag is.

Selecteer de hele tabel en kies **Voorwaardelijke opmaak › Nieuwe regel › Een formule
gebruiken**. Vul in:

```
=$D4<10
```

Let op het dollarteken: `$D4` betekent *"altijd kolom D, maar de rij schuift mee"*. Dat is
de gemengde verwijzing uit Focus 2, en precies daarom staat ze hier.

Zonder dat dollarteken kleurt elke cel op zijn eigen kolom — niet wat je bedoelt.

## 5. Regels terugvinden

Vraag je je later af waarom een cel gekleurd is? Ga naar **Voorwaardelijke opmaak ›
Regels beheren**. Daar staan ze allemaal, en kun je ze aanpassen of wissen.

Hou het beperkt. Drie regels op een blad helpen; vijftien maken er een kermis van, en dan
valt niets meer op.

## Veelgemaakte fouten

- **Het dollarteken vergeten** bij een regel voor een hele rij.
- **De cel met de hand inkleuren.** Dat lijkt hetzelfde, maar het blijft rood staan als de
  voorraad morgen weer aangevuld is.
- **Te veel regels**, waardoor het hele blad kleurt en je niets meer ziet.
$md$,
  null, true
where not exists (select 1 from lessen where titel = 'Voorwaardelijke opmaak');

