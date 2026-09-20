# 5OS Excel — oefenportaal

Oefenportaal voor de Excel-lessen van 5OS. Leerlingen maken stagegerichte opdrachten
in een rekenblad in de browser; de leerkracht ziet score, aantal pogingen, tijd en
schermgebruik.

**Status: technische proef (fase 1).** Eén volledige oefening werkt van aanmelden tot
score. De bedoeling van deze fase was uitzoeken of een rekenblad in de browser goed
genoeg is voor deze cursus, vóór er een heel portaal omheen gebouwd wordt.

## Wat werkt

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

De CSV heeft de kolommen `naam,klas,rol`. Het script toont de wachtwoorden **één keer**
in de terminal — kopieer ze meteen, ze worden als scrypt-hash bewaard en zijn daarna
niet meer op te vragen.

## Hoe het in elkaar zit

```
app/
  page.tsx                  aanmelden
  oefenen/page.tsx          werkruimte van de leerling
  leerkracht/page.tsx       opvolging
  api/nakijken/             nakijken op de server (sleutel blijft hier)
  api/gebeurtenissen/       schermgebruik registreren
  api/login/                aanmelden tegen de tabel leerlingen
components/
  Werkblad.tsx              Univer, met Nederlandse functienamen
  OefeningWerkruimte.tsx    opdracht + rekenblad + feedback
lib/
  nl-functies.ts            SOM, ALS, VERT.ZOEKEN … als echte functies
  nakijken.ts               checks uitvoeren      (server-only)
  telemetrie.ts             schermgebruik meten
  supabase.ts               verbinding            (server-only)
  opslag.ts                 alle databanktoegang  (server-only)
supabase/
  schema.sql                tabellen en afscherming
data/oefeningen/
  factuur.opgave.ts         startbestand + opdracht (gaat naar de browser)
  factuur.sleutel.ts        antwoordsleutel     (server-only)
```

### Een oefening toevoegen

Twee bestanden: een `*.opgave.ts` met het startbestand en de instructies, en een
`*.sleutel.ts` met de checks. Elke check kan drie dingen controleren:

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

Het registreert **niet** wat er in een ander venster gebeurt — dat kan een webpagina
technisch niet zien — en een tweede scherm of gsm valt er helemaal buiten. Het is dus
een indicatie om een gesprek mee te beginnen, geen bewijs.

De leerling ziet dit ook: de meting staat zichtbaar in de balk en er staat een
uitleg in de zijbalk. Stem het gebruik af met de school en de DPO voor je het
klassikaal inzet.

## Volgende stappen

1. `nl-NL`-vertaling van de menubalk
2. Uitzoeken wat er kan met draaitabellen (Focus 7) en afdrukinstellingen (Focus 3)
3. Oefeningen 2 t.e.m. 7 uit `docs/leerlijn.md`
