# Welke backend en frontend moet je aanmaken?

Kort antwoord: **je hoeft maar twee accounts te maken — Supabase en Vercel — en die
via GitHub aan deze repo te koppelen.** Verder niets.

## Frontend

**Next.js (React + TypeScript).** Staat al in deze repo, je moet niets aanmaken.

Waarom niet zoals `fleur-leerlingenportaal` (losse HTML + JS)? Dat werkt prima voor
een portaal dat vooral toont. Hier zitten rollen, een leerkrachtendashboard, live
opvolging en nakijklogica die niet in de browser mag staan. In losse JS-bestanden
loopt dat binnen een paar weken vast.

## Backend

**Supabase** — dat is in één dienst alles wat we nodig hebben:

| Onderdeel | Waarvoor |
|---|---|
| Postgres | leerlingen, oefeningen, pogingen, scores, schermgebruik |
| Row Level Security | een leerling kan alleen zijn eigen werk opvragen, ook via de console |
| Auth | de sessies, met de gebruikersnamen en wachtwoorden die jij aanmaakt |
| Realtime | jij ziet tijdens de les binnenkomen wie waar zit |
| Storage | start- en uploadbestanden (.xlsx) |
| Edge Functions | nakijken buiten het bereik van de leerling |

Gratis tier is ruim genoeg voor een paar klassen.

**Vercel** — voor het hosten van de Next.js-app. Gratis voor onderwijsgebruik,
koppelt rechtstreeks aan GitHub: elke push naar `main` staat binnen de minuut online.

## Wat jij concreet moet doen

1. **Supabase** — account op [supabase.com](https://supabase.com), nieuw project,
   regio *Frankfurt* (dichtst bij, en de gegevens blijven in de EU). Noteer uit
   *Project Settings › API*: de **Project URL**, de **anon key** en de
   **service role key**.
2. **Vercel** — account op [vercel.com](https://vercel.com), inloggen met GitHub,
   deze repo importeren.
3. In Vercel bij *Settings › Environment Variables* zetten:
   ```
   NEXT_PUBLIC_SUPABASE_URL=...
   NEXT_PUBLIC_SUPABASE_ANON_KEY=...
   SUPABASE_SERVICE_ROLE_KEY=...
   SESSIE_GEHEIM=<willekeurige reeks van 32+ tekens>
   ```
   De **service role key hoort alleen in Vercel**, nooit in de repo en nooit in een
   bestand dat met `NEXT_PUBLIC_` begint — daarmee kan iemand álle gegevens lezen
   en wijzigen.
4. Laat het me weten, dan zet ik de databank op en vervang ik `lib/opslag.ts`.

## Wat er dan verandert in de code

Alleen `lib/opslag.ts`. Dat bestand is met opzet dun gehouden: elke functie erin
wordt een Supabase-query, de rest van de app merkt er niets van.

## Wat nog beslist moet worden

- **Waar draait het?** Vercel is het eenvoudigst. Draait de school liever alles op
  eigen servers, dan kan dat ook, maar dan heb je iemand van IT nodig.
- **Draaitabellen** (Focus 7) zitten niet in het gratis deel van de rekenbladmotor.
  Ofwel een licentie, ofwel die leerstof op een andere manier oefenen. Ik zoek dat
  uit voor we eraan beginnen.
