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

Dat maakt zes tabellen: `leerlingen`, `sessies`, `pogingen`, `gebeurtenissen`,
`lessen` en `lesmedia`. Het script mag je meermaals draaien; bestaande tabellen
blijven ongemoeid. Draai je het opnieuw op een bestaande databank, dan voegt het
ook de kolom `pogingen.bestand_pad` toe — die houdt bij waar het ingediende
`.xlsx`-bestand van een leerling staat.

### De twee opslagmappen

Ga naar **Storage › New bucket** en maak er **twee**, allebei op **private**:

| Bucket | Waarvoor |
|---|---|
| **`lesmateriaal`** | Voorbeeldwerkmappen, pdf's en schermafbeeldingen bij de lessen. Leerlingen krijgen er een link naartoe die na een uur vervalt. |
| **`inzendingen`** | De `.xlsx`-bestanden die leerlingen indienen bij de oefeningen rond grafieken, draaitabellen en afdrukken. Alleen jij kunt ze openen, via het leerlingoverzicht. |

Vergeet `inzendingen` niet. Zonder die bucket blijft het portaal werken — het werk
wordt nagekeken en de score bewaard — maar het bestand zelf kun je achteraf niet
meer openen. De leerling krijgt dan te zien dat zijn score bewaard is en zijn
bestand niet.

> **Zet hier geen filmpjes in.** De gratis Supabase geeft 1 GB opslag en ongeveer
> 5 GB verkeer per maand. Eén filmpje van 150 MB dat 25 leerlingen bekijken is al
> 3,75 GB. Video's horen op YouTube of Vimeo — zie *Lessen* hieronder.

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
   | `SETUP_SLEUTEL` | tijdelijk, om je eerste login te maken — zie stap 3 |

   Voor `SESSIE_GEHEIM`: `openssl rand -hex 32` in een terminal, of eender welke
   lange willekeurige reeks. Verander hem niet zonder reden — iedereen wordt dan afgemeld.

   Zet alle drie aan voor **Production, Preview én Development**.

5. **Deploy.** Na een minuut staat het portaal online.

6. **Controleer het resultaat** op `/status` (bv. `https://5-osexcel.vercel.app/status`).
   Die pagina zegt in gewone taal wat er nog ontbreekt: een vergeten variabele, een
   schema dat nog niet uitgevoerd is, of een project dat niet bereikbaar is. Ze toont
   nooit de waarde van een instelling, enkel of ze aanwezig is.

> **Variabele toegevoegd of gewijzigd?** Vercel pikt die **niet** op in een bestaande
> build. Ga naar *Deployments*, klik op de drie puntjes bij de laatste deployment en
> kies *Redeploy*. Sla je dit over, dan blijft `/status` hetzelfde melden en zoek je
> je een ongeluk.

Vanaf dan zet elke push naar deze branch automatisch een nieuwe versie online.

> **Let op bij Preview-deployments.** Vercel maakt voor elke branch een publieke
> URL. Wie die link heeft, kan de aanmeldpagina zien. De gegevens zitten erachter,
> maar zet in *Settings › Deployment Protection* gerust Vercel Authentication aan
> voor previews.

---

## 3. Je eigen login aanmaken

Kip en ei: het beheer zit achter een leerkrachtlogin, en die bestaat nog niet. Daarom is
er een eenmalige `/setup`-pagina.

1. Zet in Vercel een extra variabele **`SETUP_SLEUTEL`** met een zelfgekozen waarde van
   minstens 8 tekens.
2. *Deployments* → drie puntjes → **Redeploy**.
3. Ga naar `https://jouwsite.vercel.app/setup`, vul die sleutel in, je naam, je klas en
   een wachtwoord naar keuze. Je gebruikersnaam wordt automatisch gemaakt
   (Dieter Varey wordt `dieter.varey`).
4. **Haal `SETUP_SLEUTEL` daarna weg in Vercel** en doe nog een Redeploy.

De pagina heeft twee sloten: zonder de juiste sleutel gebeurt er niets, en zodra er één
leerkracht bestaat weigert ze sowieso. Toch is het netter de variabele weg te halen —
dan is de route helemaal dood.

## 4. Je klas aanmaken

Meld je aan en klik op **Leerlingen beheren**. Plak de namen van je klas in het
tekstvak, één per lijn:

```
Lotte Desmet
Youssef El Amrani
Noor Vandenberghe
```

Je krijgt meteen een tabel met gebruikersnaam en wachtwoord per leerling, met knoppen om
ze te kopiëren of af te drukken. **Die wachtwoorden zie je maar één keer** — ze worden als
scrypt-hash bewaard en zijn daarna niet meer op te vragen, wel opnieuw in te stellen.

Verder op die pagina:

- **Nieuw wachtwoord** per leerling, voor wie het zijne kwijt is.
- **Verwijderen**, dat ook alle scores en metingen van die leerling meeneemt. Je eigen
  account kun je niet verwijderen.

Dubbele namen krijgen automatisch een cijfer (`lotte.desmet`, `lotte.desmet2`), en
accenten verdwijnen uit de gebruikersnaam omdat die lastig zijn op een schoolklavier.

### Liever vanaf de commandolijn

Kan ook, met een CSV met kolommen `naam,klas,rol`:

```bash
cp .env.example .env.local     # de drie waarden invullen
npm install
node scripts/maak-leerlingen.mjs klas5os.csv
```

Bestaande accounts blijven ongemoeid; pas met `--reset` krijgen ze een nieuw wachtwoord.
Beide wegen gebruiken dezelfde regels, dus een leerling krijgt via het script dezelfde
gebruikersnaam als via het portaal.

---

## 5. Lessen en filmpjes

Onder **Lessen beheren** schrijf je de theorie die bij een oefening hoort. De tekst is
Markdown: `## Kop`, `**vet**`, `` `=SOM(A1:A5)` `` voor formules, lijsten met `-`, en
tabellen met `|`. Er is een voorbeeldknop om te zien hoe het bij de leerling toekomt.

Een les staat eerst in **concept**: alleen jij ziet ze. Met *Publiceren voor de klas*
komt ze in het overzicht van de leerlingen. Koppel je de les aan een oefening, dan
verschijnt daar een link "Theorie herlezen" die in een nieuw tabblad opent — zo blijft
het ingevulde werkblad staan.

### Filmpjes

Zet je filmpje op **YouTube** of **Vimeo** als *verborgen* / *niet-vermeld* en plak de
link in het portaal. Dan is het niet vindbaar via een zoekmachine, maar wel te bekijken
door wie de les opent.

Alleen die twee diensten worden aanvaard. Een willekeurig adres wordt geweigerd: anders
zou een link in een les een vreemde pagina kunnen laden binnen een portaal waar
leerlingen aangemeld zijn. YouTube-video's spelen via `youtube-nocookie.com`.

Waarom geen uploads? Zie het kader bij de opslagmap hierboven — je zou de gratis limiet
met twee filmpjes opgebruiken.

### Bestanden

Een voorbeeldwerkmap, een pdf of een schermafbeelding laad je wel gewoon op, tot 20 MB
per bestand. Verwijder je het item, dan verdwijnt ook het bestand uit de opslag.

### De lessen inladen

`supabase/lessen.sql` bevat de 25 lessen die bij de 25 oefeningen horen. Voer het uit
in de SQL Editor. Het mag meermaals draaien: een les die al bij een oefening hoort, komt
er niet nog eens bij. Daarna bewerk je ze gewoon in het portaal.

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
