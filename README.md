# 5OS Excel — oefenportaal

Oefenportaal voor de Excel-lessen van 5OS. Leerlingen maken stagegerichte opdrachten —
de meeste in een rekenblad in de browser, die rond grafieken, draaitabellen en afdrukken
in Excel zelf. De leerkracht ziet score, aantal pogingen, tijd, schermgebruik en het
ingediende werk.

**Status: werkend portaal.** 40 oefeningen over de acht Focussen van de cursus, elk met
zijn eigen theoriepagina, nakijken en opvolging. De acht Focussen zijn allemaal gedekt: wat een
rekenblad in de browser kan, gebeurt in het portaal; grafieken, draaitabellen en
afdrukken doen de leerlingen in echt Excel en dienen ze als `.xlsx` in.

## Wat werkt

- 40 oefeningen, gegroepeerd per Focus, binnen elke Focus oplopend in moeilijkheid:
  25 in het rekenblad in de browser, 15 in echt Excel (grafieken, draaitabellen, afdrukken)
- Nagekeken wordt niet alleen de uitkomst, maar ook de gebruikte functie, de getalnotatie,
  de celopmaak, de sorteervolgorde en of de titels vastgezet zijn
- 49 lessen met theorie, voorbeelden en tabellen: één bij elke oefening, plus negen
  losse over woordenschat, foutmeldingen, datums, validatie en opmaak
- Filmpjes en bijlagen bij een les — te beheren in het portaal
- Accountbeheer in het portaal zelf: namen plakken, wachtwoorden krijgen, opnieuw instellen
- Aanmelden met gebruikersnaam en wachtwoord uit een tabel die de leerkracht beheert
- Rekenblad in de browser ([Univer](https://github.com/dream-num/univer), Apache-2.0) met lint, formulebalk, celopmaak en meerdere bladen
- **Nederlandse functienamen**: `=SOM()`, `=ALS()`, `=VERT.ZOEKEN()`, `=AANTAL.ALS()` … werken zoals in de cursus
- Nakijken op de server: uitkomst, gebruikte functie én getalnotatie, met gerichte feedback per deelopdracht
- Opvolging: aantal pogingen, tijd, hoe vaak het oefenscherm uit beeld ging en hoe lang
- Leerkrachtenoverzicht per leerling, met per oefening alle pogingen, wat er misging,
  en het ingediende Excel-bestand om te openen

## Beperkingen — eerlijk gemeten, niet geschat

| Punt | Stand van zaken |
|---|---|
| Nederlandse functienamen | Werkt. Ze zijn als echte functies geregistreerd, inclusief namen met een punt (`VERT.ZOEKEN`). |
| Puntkomma's en ONWAAR | Werkt. De leerling mag typen zoals de cursus het schrijft: `=ALS(B5>100;"ja";"nee")` en `ONWAAR`. Het portaal vertaalt dat. Decimalen wél met een **punt**: `0.02`. |
| Menubalk | Staat nog in het **Engels**. Univer heeft 19 talen, maar geen Nederlands. Een `nl-NL`-vertaling is handwerk en staat op de planning. |
| Grafieken, draaitabellen, afdrukken (Focus 4, 7, 3) | **Opgelost, maar anders.** Die drie zitten in de commerciële uitbreiding van Univer — en die is momenteel niet te koop. Daarom gebeuren ze in **echt Excel**: de leerling downloadt een startbestand, maakt de opdracht in Excel en laadt het bestand op. De server pakt de `.xlsx` uit en leest het grafiektype, de titel, de gegevensbereiken, de opbouw van de draaitabel en alle afdrukinstellingen. Op stage werken ze toch met het echte programma. |
| Nakijken van draaitabellen | Getest tegen bestanden die met openpyxl gemaakt zijn en tegen een met de hand gebouwde OOXML-draaitabel. Eén draaitabel die **Excel zelf** opslaat, zou de laatste twijfel wegnemen. Grafieken en afdrukinstellingen zijn wel tegen echte Excel-structuren getest. |
| Opslag | Supabase (Postgres). Zie `docs/backend-frontend.md` voor het opzetten. |
| Nakijken vervalsen | Een leerling die de ontwikkelaarsconsole kent, kan een verzonnen antwoord naar de server sturen. De oplossingssleutel lekt niet, maar de score is niet fraudebestendig. Voor punten die echt meetellen: laat de toets klassikaal afleggen. |

## Aan de slag

Je hebt een Supabase-project nodig. Het volledige stappenplan staat in
**[`docs/backend-frontend.md`](docs/backend-frontend.md)**; kort samengevat:

```bash
npm install
cp .env.example .env.local        # SUPABASE_URL, SUPABASE_SECRET_KEY, SESSIE_GEHEIM invullen
# supabase/schema.sql uitvoeren in de SQL Editor van Supabase
node scripts/maak-leerlingen.mjs klas5os.csv
npm run dev                       # http://localhost:3000
```

Je eerste leerkrachtaccount maak je op `/setup` (eenmalig, met een `SETUP_SLEUTEL`).
Daarna beheer je je klassen in het portaal zelf, via **Leerlingen beheren**: namen plakken,
wachtwoorden krijgen, opnieuw instellen of verwijderen. Het CLI-script hierboven blijft
bestaan voor wie liever een CSV gebruikt.

Wachtwoorden zie je **één keer** — ze worden als scrypt-hash bewaard en zijn daarna niet
meer op te vragen, wel opnieuw in te stellen.

## Werkt het?

Open `/status` op de draaiende site. Die pagina controleert de instellingen, de
verbinding met Supabase en of het schema uitgevoerd is, en zegt per punt wat er
misgaat. Ze toont nooit de waarde van een instelling.

## Hoe het in elkaar zit

```
app/
  page.tsx                  aanmelden
  setup/page.tsx            eenmalig het eerste leerkrachtaccount
  oefenen/                  overzicht van de reeks
  oefenen/[id]/             één oefening (rekenblad óf uploadopdracht)
  lessen/                   theorie lezen (leerling)
  leerkracht/lessen/        theorie schrijven
  oefenen/page.tsx          werkruimte van de leerling
  leerkracht/page.tsx       opvolging
  leerkracht/leerling/[…]/  alle pogingen van één leerling + ingediend werk
  leerkracht/leerlingen/    accountbeheer
  api/nakijken/             nakijken op de server (sleutel blijft hier)
  api/startbestand/         het .xlsx dat de leerling in Excel opent
  api/indienen/             ingediend .xlsx nakijken en opbergen
  api/gebeurtenissen/       schermgebruik registreren
  api/login/                aanmelden tegen de tabel leerlingen
  api/leerkracht/           accounts aanmaken, resetten, verwijderen
  api/setup/                eerste leerkracht (twee sloten)
  status/page.tsx           controlepagina na een deploy
components/
  Werkblad.tsx              Univer, met Nederlandse functienamen
  OefeningWerkruimte.tsx    opdracht + rekenblad + feedback
  UploadWerkruimte.tsx      opdracht + startbestand + uploadvak + feedback
lib/
  accounts.mjs              gebruikersnamen en wachtwoorden (gedeeld met het script)
  formules.ts               puntkomma's en WAAR/ONWAAR vertalen
  lessen.ts                 lessen en media  (server-only)
  bestanden.ts              Storage          (server-only)
  video.ts                  YouTube/Vimeo-links veilig insluiten
  nl-functies.ts            SOM, ALS, VERT.ZOEKEN … als echte functies
  nakijken.ts               checks uitvoeren      (server-only)
  werkmap-lezen.ts          een .xlsx uitpakken en doorlichten (server-only)
  nakijken-bestand.ts       checks op grafiek, draaitabel en afdruk (server-only)
  startbestand.ts           het startbestand genereren (server-only)
  telemetrie.ts             schermgebruik meten
  supabase.ts               verbinding            (server-only)
  opslag.ts                 alle databanktoegang  (server-only)
supabase/
  schema.sql                tabellen en afscherming
  lessen.sql                de 40 lessen bij de oefeningen
  lessen-extra.sql          9 losse theorielessen zonder oefening
data/oefeningen/
  factuur.opgave.ts         startbestand + opdracht (gaat naar de browser)
  factuur.sleutel.ts        antwoordsleutel     (server-only)
  f3-afdrukken.ts           uploadopdrachten: afdrukken  (+ .sleutel.ts)
  f4-grafieken.ts           uploadopdrachten: grafieken  (+ .sleutel.ts)
  f7-draaitabellen.ts       uploadopdrachten: draaitabellen (+ .sleutel.ts)
```

### Een oefening toevoegen

Twee bestanden in `data/oefeningen/`: een opgave met het startbestand en de instructies,
en een sleutel met de checks. `bouwstenen.ts` bevat de opmaak en een hulpje om een
werkmap te bouwen; kijk naar `01-voorraad.ts` als voorbeeld. Elke check kan drie dingen controleren:

```ts
{
  id: 'subtotaal',
  omschrijving: 'Subtotaal berekend met de functie SOM',
  punten: 2,
  cellen: ['E18'],
  verwachteWaarden: [3253.4],                                  // klopt de uitkomst?
  formulePatronen: [{ patroon: '^=\\s*SOM\\s*\\(', uitleg: 'gebruik SOM' }],  // juiste functie?
  getalnotatiePatroon: '0\\.00',                               // juiste opmaak?
  hint: 'Gebruik =SOM(E12:E16).',
}
```

Registreer ze daarna in `data/oefeningen/index.ts` en `data/oefeningen/sleutels.ts`.

#### Een oefening die in echt Excel gemaakt wordt

Zet `soort: 'upload'` op de opgave en geef ze een `startbestand` (bladnaam, rijen,
kolombreedtes); daar genereert de server het `.xlsx` uit. De checks komen in
`BESTANDSLEUTELS` en kijken naar wat alleen in een echt bestand bestaat:

```ts
{
  id: 'type',
  omschrijving: 'Het is een kolom- of staafdiagram',
  punten: 3,
  eis: { soort: 'grafiek', types: ['barChart', 'bar3DChart'], titelBevat: 'Omzet per maand' },
  hint: 'Kies Invoegen › Kolom.',
}
```

Naast `grafiek` bestaan `draaitabel` (rij-, kolom- en gegevensvelden, veldnamen,
samenvattingsfunctie) en `afdruk` (staand/liggend, passend maken, kop- en voettekst,
paginanummer, titelrijen, rasterlijnen, marges).

## Opvolging van leerlingen

Het portaal registreert per oefensessie hoe lang de leerling bezig is, hoe vaak het
oefenvenster uit beeld gaat en hoe lang, en hoeveel pogingen er nodig waren.

Die cijfers staan **niet** op het scherm van de leerling; alleen de leerkracht ziet ze.

Het registreert **niet** wat er in een ander venster gebeurt — dat kan een webpagina
technisch niet zien — en een tweede scherm of gsm valt er helemaal buiten. Het is dus
een indicatie om een gesprek mee te beginnen, geen bewijs.

In de zijbalk staat één neutrale zin: "Je leerkracht volgt je werk aan deze
oefening op." Wat er precies gemeten wordt, staat er bewust niet bij — anders
leren leerlingen vooral het tabblad open te laten staan. Licht de klas wel één keer
mondeling in, en stem het gebruik af met de school en de DPO voor je het inzet.

## Volgende stappen

1. `nl-NL`-vertaling van de menubalk
2. Eén draaitabel die in Excel zelf gemaakt is, om het nakijken daarvan te bevestigen
3. Filmpjes bij de lessen — de plaats ervoor staat klaar, er staat nog niets in
