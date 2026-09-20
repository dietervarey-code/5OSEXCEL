-- =====================================================================
--  5OS Excel — databankschema
--
--  Uitvoeren in Supabase: SQL Editor › New query › plakken › Run.
--  Het script mag meermaals draaien zonder schade aan te richten.
-- =====================================================================

-- ---------------------------------------------------------------------
--  Leerlingen en leerkrachten
--
--  Jij beheert deze tabel met scripts/maak-leerlingen.mjs. Wachtwoorden
--  staan er nooit in klare tekst in, enkel een scrypt-hash met salt.
-- ---------------------------------------------------------------------
create table if not exists leerlingen (
  gebruikersnaam   text primary key,
  naam             text not null,
  klas             text not null,
  rol              text not null default 'leerling'
                     check (rol in ('leerling', 'leerkracht')),
  wachtwoord_hash  text not null,
  aangemaakt_op    timestamptz not null default now()
);

create index if not exists leerlingen_klas_idx on leerlingen (klas);

-- ---------------------------------------------------------------------
--  Sessies — één rij per keer dat iemand een oefening opent
--
--  Hieraan hangen zowel de pogingen als het schermgebruik, zodat je
--  achteraf kunt zien: "in die ene sessie van 20 minuten klikte ze
--  zeven keer weg en deed ze vier pogingen".
-- ---------------------------------------------------------------------
create table if not exists sessies (
  id                uuid primary key default gen_random_uuid(),
  gebruikersnaam    text not null references leerlingen (gebruikersnaam) on delete cascade,
  oefening_id       text not null,
  gestart_op        timestamptz not null default now(),
  laatst_actief_op  timestamptz not null default now()
);

create index if not exists sessies_gebruiker_idx on sessies (gebruikersnaam, gestart_op desc);
create index if not exists sessies_oefening_idx on sessies (oefening_id);

-- ---------------------------------------------------------------------
--  Pogingen — één rij per keer dat er op Nakijken geklikt wordt
-- ---------------------------------------------------------------------
create table if not exists pogingen (
  id              uuid primary key default gen_random_uuid(),
  sessie_id       uuid not null references sessies (id) on delete cascade,
  gebruikersnaam  text not null references leerlingen (gebruikersnaam) on delete cascade,
  oefening_id     text not null,
  nummer          integer not null,          -- hoeveelste poging van deze leerling
  score           numeric(6, 2) not null,
  max_score       numeric(6, 2) not null,
  resultaten      jsonb not null default '[]'::jsonb,
  ingediend_op    timestamptz not null default now()
);

create index if not exists pogingen_gebruiker_idx on pogingen (gebruikersnaam, oefening_id);
create index if not exists pogingen_sessie_idx on pogingen (sessie_id);

-- ---------------------------------------------------------------------
--  Gebeurtenissen — schermgebruik
--
--  Let op wat hier NIET in staat: er wordt nergens vastgelegd wat de
--  leerling in een ander venster deed. Enkel of dit tabblad zichtbaar
--  was, en hoe lang niet.
-- ---------------------------------------------------------------------
create table if not exists gebeurtenissen (
  id              bigserial primary key,
  sessie_id       uuid not null references sessies (id) on delete cascade,
  gebruikersnaam  text not null references leerlingen (gebruikersnaam) on delete cascade,
  soort           text not null
                    check (soort in ('gestart', 'verborgen', 'zichtbaar',
                                     'focus_weg', 'focus_terug', 'hartslag', 'geplakt')),
  tijdstip        timestamptz not null,
  duur_ms         integer
);

create index if not exists gebeurtenissen_sessie_idx on gebeurtenissen (sessie_id);
create index if not exists gebeurtenissen_gebruiker_idx on gebeurtenissen (gebruikersnaam, tijdstip desc);

-- =====================================================================
--  Afscherming
--
--  De app praat met de databank via de secret key, op de server, en
--  komt dus niet langs RLS. De browser krijgt nooit een databanksleutel.
--
--  We zetten RLS toch aan en geven bewust GEEN policies: mocht er ooit
--  per ongeluk een publishable key in de frontend belanden, dan is het
--  antwoord op elke query een lege lijst in plaats van de volledige
--  klasgegevens.
-- =====================================================================
alter table leerlingen     enable row level security;
alter table sessies        enable row level security;
alter table pogingen       enable row level security;
alter table gebeurtenissen enable row level security;

revoke all on leerlingen, sessies, pogingen, gebeurtenissen from anon, authenticated;
revoke all on all sequences in schema public from anon, authenticated;
