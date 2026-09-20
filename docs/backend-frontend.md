# Supabase en Vercel opzetten

Twee diensten, allebei gratis voor dit gebruik. Reken op een halfuur.

---

## 1. Supabase

### Het project

1. Account op [supabase.com](https://supabase.com), **New project**.
2. Regio: **Frankfurt (eu-central-1)** — dichtst bij en je gegevens blijven in de EU.
   Je werkt met gegevens van minderjarigen; die keuze kun je achteraf niet meer wijzigen.
3. Bewaar het databankwachtwoord dat je instelt in je wachtwoordbeheerder.

### De tabellen

Open **SQL Editor › New query**, plak de volledige inhoud van
[`supabase/schema.sql`](../supabase/schema.sql) en klik **Run**.

Dat maakt vier tabellen: `leerlingen`, `sessies`, `pogingen` en `gebeurtenissen`.
Het script mag je meermaals draaien; bestaande tabellen blijven ongemoeid.

### De sleutels

Onder **Project Settings**:

| Wat | Waar | Waarvoor |
|---|---|---|
| **Project URL** | Data API | `SUPABASE_URL` |
| **Secret key** (`sb_secret_…`) | API Keys › Secret keys | `SUPABASE_SECRET_KEY` |

De **publishable key heb je niet nodig.** In dit ontwerp krijgt de browser nooit een
databanksleutel: alles loopt via de server. Dat is precies de bedoeling — zie hieronder.

---

## 2. Vercel

1. Account op [vercel.com](https://vercel.com), inloggen **met GitHub**.
2. **Add New › Project**, kies `dietervarey-code/5OSEXCEL`.
3. Framework wordt automatisch herkend als Next.js. Niets aanpassen.
4. Vóór je op Deploy klikt, open **Environment Variables** en zet deze drie:

   | Naam | Waarde |
   |---|---|
   | `SUPABASE_URL` | je Project URL |
   | `SUPABASE_SECRET_KEY` | je secret key |
   | `SESSIE_GEHEIM` | een willekeurige reeks van 32+ tekens |

   Voor `SESSIE_GEHEIM`: `openssl rand -hex 32` in een terminal, of eender welke
   lange willekeurige reeks. Verander hem niet zonder reden — iedereen wordt dan afgemeld.

   Zet alle drie aan voor **Production, Preview én Development**.

5. **Deploy.** Na een minuut staat het portaal online.

Vanaf dan zet elke push naar deze branch automatisch een nieuwe versie online.

> **Let op bij Preview-deployments.** Vercel maakt voor elke branch een publieke
> URL. Wie die link heeft, kan de aanmeldpagina zien. De gegevens zitten erachter,
> maar zet in *Settings › Deployment Protection* gerust Vercel Authentication aan
> voor previews.

---

## 3. Je klas aanmaken

Lokaal, één keer:

```bash
cp .env.example .env.local     # en de drie waarden invullen
npm install
```

CSV met je klas (`klas5os.csv`, staat in `.gitignore`):

```csv
naam,klas,rol
Dieter Varey,5OS,leerkracht
Lotte Desmet,5OS,leerling
Youssef El Amrani,5OS,leerling
```

```bash
node scripts/maak-leerlingen.mjs klas5os.csv
```

Het script toont de wachtwoorden **één keer** in een tabel. Kopieer ze meteen — ze
worden als scrypt-hash bewaard en zijn daarna niet meer op te vragen. Een leerling die
zijn wachtwoord kwijt is, krijgt een nieuw via `--reset`:

```bash
node scripts/maak-leerlingen.mjs enkel-die-ene.csv --reset
```

Draai je het script een tweede keer met dezelfde CSV zonder `--reset`, dan blijven
bestaande accounts ongemoeid. Zo overschrijf je niet per ongeluk de wachtwoorden van
een halve klas midden in het schooljaar.

---

## Hoe de beveiliging in elkaar zit

De browser krijgt **geen** databanksleutel. Alle lees- en schrijfacties lopen via de
route handlers in `app/api`, op de server, met de secret key. Dat is bewust:

- Een leerling kan niet rechtstreeks de databank bevragen, ook niet via de console.
- Er is geen publishable key die kan uitlekken.
- De antwoordsleutels van de oefeningen blijven op de server (`lib/nakijken.ts` en
  `data/oefeningen/*.sleutel.ts` importeren `server-only`; de build faalt als die ooit
  in een clientbestand belandt).

Row Level Security staat op alle tabellen aan, **zonder policies**. Dat is geen
vergetelheid maar een vangnet: mocht er ooit toch een publishable key in de frontend
belanden, dan levert elke query een lege lijst op in plaats van de volledige klasgegevens.

Wat dit **niet** oplost: een leerling die weet hoe de ontwikkelaarsconsole werkt, kan
een verzonnen resultaat naar `/api/nakijken` sturen. De oplossingssleutel lekt niet,
maar de score is niet fraudebestendig. Voor punten die echt meetellen: klassikaal afnemen.

### Gegevens van één leerling wissen

Eén regel in de SQL Editor. De sessies, pogingen en metingen gaan automatisch mee:

```sql
delete from leerlingen where gebruikersnaam = 'lotte.desmet';
```

---

## Wat er nog open staat

- **Draaitabellen** (Focus 7) zitten niet in het gratis deel van de rekenbladmotor.
  Licentie nemen, of die leerstof anders oefenen. Moet ik nog uitzoeken.
- **Live meekijken tijdens de les.** Het overzicht ververst nu bij het herladen van de
  pagina. Supabase Realtime kan dat live maken, maar dan moet de browser wél een
  sleutel krijgen en zijn er echte RLS-policies nodig. Pas doen als je het echt mist.
