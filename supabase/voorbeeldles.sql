-- =====================================================================
--  Voorbeeldles — optioneel
--
--  Eén uitgewerkte les bij de oefening "Factuur vervolledigen", zodat het
--  portaal niet leeg staat en je meteen ziet welke opmaak mogelijk is.
--  Inhoud volgt het ICT-vademecum, Focus 1 en 2.
--
--  Uitvoeren in Supabase › SQL Editor. Bewerken doe je daarna gewoon in het
--  portaal, via Lessen beheren.
-- =====================================================================

insert into lessen (focus, volgnummer, titel, samenvatting, inhoud, oefening_id, gepubliceerd)
select 2, 1,
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
