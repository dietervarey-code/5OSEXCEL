# Leerlijn 5OS Excel

Afgeleid uit *ICT-vademecum — Rekenblad*, Focus 1 t.e.m. 9 (de twee cursus-pdf's).
De pdf's zelf staan bewust **niet** in deze repo: het is uitgegeven lesmateriaal en
deze repository is publiek.

## Focusblokken uit de cursus

| Focus | Onderwerp | Kern |
|---|---|---|
| 1 | Rekenblad gebruiken en opmaken | werkmap vs. werkblad, rij/kolom/cel, bereik, getalnotatie, inhoud vs. weergave, doorvoeren, transponeren, sorteren, werkblad beveiligen |
| 2 | Formules en functies | SOM, SOM.ALS, MAX, MIN, GEMIDDELDE, AFRONDEN, AANTAL, AANTALARG, AANTAL.ALS, ALS, relatieve/absolute/gemengde celverwijzing, VERT.ZOEKEN |
| 3 | Afdrukken | marges, kop- en voettekst, paginanummering, afdrukinstellingen |
| 4 | Grafieken | onderdelen, grafiektypes, grafiek maken en aanpassen |
| 5 | Meerdere werkbladen | werken over bladen heen |
| 6 | Koppelen | verwijzingen tussen bladen en bestanden |
| 7 | Draaitabellen | draaitabel opbouwen en gebruiken |
| 8 | Geavanceerde functies | HORIZ.ZOEKEN, datumfuncties, geneste functies, gegevensvalidatie |
| 9 | Databank bevragen | query's, berekende velden, formulieren (Access-luik) |

## De reeks oefeningen

Vijfentwintig oefeningen, gegroepeerd per Focus, en binnen elke Focus oplopend van
● naar ●●●●●.

### Focus 1 · Rekenblad gebruiken en opmaken

| Oefening | Niveau | Waar het om draait |
|---|---|---|
| Getalnotatie toepassen | ● | valuta, percentage, vet, achtergrondkleur |
| Een tabel leesbaar maken | ●● | koptekst, uitlijning, totaalrij |
| Klanten sorteren op omzet | ●● | sorteren zonder de rijen uit elkaar te trekken |
| Titels vastzetten | ●● | koppen in beeld houden bij het scrollen |
| Gegevens van rijen naar kolommen | ●●● | transponeren met Paste Special |

### Focus 2 · Formules en functies

| Oefening | Niveau | Waar het om draait |
|---|---|---|
| Voorraadlijst afwerken | ● | vermenigvuldigen met celverwijzingen, `SOM` |
| Prijslijst bijwerken | ●● | absolute celverwijzing, `AFRONDEN` |
| Factuur vervolledigen | ●● | beide samen op een echte factuur |
| Verkoopcijfers samenvatten | ●● | `MAX`, `MIN`, `GEMIDDELDE`, `AANTAL` vs `AANTALARG` |
| Bestellingen beoordelen | ●●● | `ALS`, `AANTAL.ALS`, `SOM.ALS` |
| Klantenbestand aanvullen | ●●● | `VERT.ZOEKEN` met exacte match |

### Focus 5 · Meerdere werkbladen

| Oefening | Niveau | Waar het om draait |
|---|---|---|
| Cijfers van een ander blad ophalen | ●● | `Januari!D10` |
| Eén filiaal over drie maanden | ●●● | dezelfde cel op meerdere bladen |
| Twee maanden vergelijken | ●●● | bladen combineren in één formule |
| Gemiddelde en uitschieters | ●●● | functies over bladen heen |
| Opzoeken op een ander werkblad | ●●●● | `VERT.ZOEKEN` over de bladgrens |

### Focus 6 · Koppelen

| Oefening | Niveau | Waar het om draait |
|---|---|---|
| Prijzen koppelen aan de centrale lijst | ●● | één bron, alles volgt |
| Koppelen met `VERT.ZOEKEN` | ●●● | koppelen op code in plaats van op positie |
| Drie filialen samenbrengen | ●●● | consolideren |
| Een kapotte koppeling herstellen | ●●●● | fouten in verwijzingen opsporen |
| Een volledig gekoppelde factuur | ●●●●● | alles samen, niets dubbel |

### Focus 8 · Geavanceerde functies

| Oefening | Niveau | Waar het om draait |
|---|---|---|
| Maanddoelen opzoeken | ●●● | `HORIZ.ZOEKEN` |
| Artikelen opzoeken | ●●●● | `X.ZOEKEN` met terugvalwaarde |
| Klantcodes uit elkaar halen | ●●●● | `LINKS`, `RECHTS`, `LENGTE` |
| Korting met geneste functies | ●●●●● | `VERT.ZOEKEN` en `ALS` in één formule |

### Focus 3, 4, 7 en 9 — geen oefeningen

| Focus | Waarom niet |
|---|---|
| 3 · Afdrukken | `@univerjs-pro/sheets-print` — betalende uitbreiding |
| 4 · Grafieken | `@univerjs-pro/sheets-chart` — betalende uitbreiding |
| 7 · Draaitabellen | `@univerjs-pro/sheets-pivot` — betalende uitbreiding |
| 9 · Databank bevragen | gaat over Access, niet over een rekenblad |

Voor die eerste drie is er één beslissing te nemen: een licentie op Univer Pro, of die
leerstof klassikaal in echt Excel houden.

## Stagetaken als vertrekpunt## Stagetaken als vertrekpunt

De oefeningen vertrekken van wat een 5OS'er op stage effectief doet:

1. **Facturen opmaken** — Focus 1 + 2 *(oefening 3)*
2. **Prijslijsten updaten** — Focus 1 + 2 *(oefening 2)*
3. **Klantenbestanden aanvullen** — Focus 2 + 8 *(oefeningen 6 en 7)*
4. **Draaitabellen en rapportage** — Focus 7 *(nog geen oefening, zie hieronder)*
5. **Geneste functies** — Focus 8 *(oefening 8)*
6. **Tabellen en cellen opmaken, beeld vastzetten** — Focus 1
7. **Printklaar maken** (alle kolommen op één pagina) — Focus 3

## Aandachtspunten voor de bouw

- **X.ZOEKEN staat niet in de cursus** (die stopt bij VERT.ZOEKEN/HORIZ.ZOEKEN), maar
  wél in de stagepraktijk. Het is als extra functie voorzien.
- **Focus 9 gaat over Access, niet Excel.** Dat valt buiten dit portaal.
- **Focus 3 (afdrukken) en Focus 7 (draaitabellen)** zijn de twee blokken waarvan nog
  moet blijken of de rekenbladmotor ze aankan — zie `README.md`, sectie Beperkingen.
