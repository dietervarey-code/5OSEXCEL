# 5OS Excel — oefenportaal

Oefenportaal voor de Excel-lessen van 5OS. Leerlingen maken stagegerichte opdrachten
in een rekenblad in de browser; de leerkracht ziet score, aantal pogingen, tijd en
schermgebruik.

**Status: technische proef (fase 1).** Eén volledige oefening werkt van aanmelden tot
score. De bedoeling van deze fase was uitzoeken of een rekenblad in de browser goed
genoeg is voor deze cursus, vóór er een heel portaal omheen gebouwd wordt.

## Wat werkt

- 25 oefeningen, gegroepeerd per Focus, binnen elke Focus oplopend in moeilijkheid
- Nagekeken wordt niet alleen de uitkomst, maar ook de gebruikte functie, de getalnotatie,
  de celopmaak, de sorteervolgorde en of de titels vastgezet zijn
- 25 lessen met theorie, voorbeelden en tabellen — één per oefening
- Filmpjes en bijlagen bij een les — te beheren in het portaal
- Accountbeheer in het portaal zelf: namen plakken, wachtwoorden krijgen, opnieuw instellen
- Aanmelden met gebruikersnaam en wachtwoord uit een tabel die de leerkracht beheert
- Rekenblad in de browser ([Univer](https://github.com/dream-num/univer), Apache-2.0) met lint, formulebalk, celopmaak en meerdere bladen
- **Nederlandse functienamen**: `=SOM()`, `=ALS()`, `=VERT.ZOEKEN()`, `=AANTAL.ALS()` … werken zoals in de cursus
- Nakijken op de server: uitkomst, gebruikte functie én getalnotatie, met gerichte feedback per deelopdracht
- Opvolging: aantal pogingen, tijd, hoe vaak het oefenscherm uit beeld ging en hoe lang
- Leerkrachtenoverzicht per leerling

## Beperkingen — eerlijk gemeten, niet geschat

| Punt | Stand van zaken |
|---|---|
| Nederlandse functienamen | Werkt. Ze zijn als echte functies geregistreerd, inclusief namen met een punt (`VERT.ZOEKEN`). |
| Puntkomma's en ONWAAR | Werkt. De leerling mag typen zoals de cursus het schrijft: `=ALS(B5>100;"ja";"nee")` en `ONWAAR`. Het portaal vertaalt dat. Decimalen wél met een **punt**: `0.02`. |
| Menubalk | Staat nog in het **Engels**. Univer heeft 19 talen, maar geen Nederlands. Een `nl-NL`-vertaling is handwerk en staat op de planning. |
| Draaitabellen (Focus 7) | **Nog niet getest.** Zit in de commerciële uitbreiding van Univer, niet in het open-source deel. Hier is een aparte beslissing nodig. |
| Afdrukinstellingen (Focus 3) | **Nog niet getest.** Marges, kop-/voettekst en "alles op één pagina" bestaan niet op dezelfde manier in de browser. Mogelijk een aparte oefenvorm nodig. |
| Grafieken (Focus 4) | Nog niet getest. |
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
  oefenen/[id]/             één oefening
  lessen/                   theorie lezen (leerling)
  leerkracht/lessen/        theorie schrijven
  oefenen/page.tsx          werkruimte van de leerling
  leerkracht/page.tsx       opvolging
  leerkracht/leerlingen/    accountbeheer
  api/nakijken/             nakijken op de server (sleutel blijft hier)
  api/gebeurtenissen/       schermgebruik registreren
  api/login/                aanmelden tegen de tabel leerlingen
  api/leerkracht/           accounts aanmaken, resetten, verwijderen
  api/setup/                eerste leerkracht (twee sloten)
  status/page.tsx           controlepagina na een deploy
components/
  Werkblad.tsx              Univer, met Nederlandse functienamen
  OefeningWerkruimte.tsx    opdracht + rekenblad + feedback
lib/
  accounts.mjs              gebruikersnamen en wachtwoorden (gedeeld met het script)
  formules.ts               puntkomma's en WAAR/ONWAAR vertalen
  lessen.ts                 lessen en media  (server-only)
  bestanden.ts              Storage          (server-only)
  video.ts                  YouTube/Vimeo-links veilig insluiten
  nl-functies.ts            SOM, ALS, VERT.ZOEKEN … als echte functies
  nakijken.ts               checks uitvoeren      (server-only)
  telemetrie.ts             schermgebruik meten
  supabase.ts               verbinding            (server-only)
  opslag.ts                 alle databanktoegang  (server-only)
supabase/
  schema.sql                tabellen en afscherming
  lessen.sql                de 25 lessen
data/oefeningen/
  factuur.opgave.ts         startbestand + opdracht (gaat naar de browser)
  factuur.sleutel.ts        antwoordsleutel     (server-only)
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
2. Uitzoeken wat er kan met draaitabellen (Focus 7) en afdrukinstellingen (Focus 3)
3. Focus 3, 4 en 7 (afdrukken, grafieken, draaitabellen) vergen een licentie op Univer Pro
