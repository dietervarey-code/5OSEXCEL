-- =====================================================================
--  Herstel: transponeren in het rekenblad
--
--  De les en de oefening verwezen naar "Plakken speciaal > Transponeren".
--  Dat menu bestaat alleen in echt Excel; het rekenblad in de browser kent
--  het niet, waardoor de oefening daar niet te maken was. Er is nu een
--  Nederlandse functie TRANSPONEREN, en de les zegt dat er voortaan bij.
--
--  Uitvoeren in Supabase > SQL Editor. Mag meermaals draaien: de tekst wordt
--  alleen aangevuld als de nieuwe alinea er nog niet staat.
-- =====================================================================

update lessen
set inhoud = replace(
      inhoud,
      '> In het Nederlandse Excel: **Plakken speciaal › Transponeren**.',
      '> In het Nederlandse Excel: **Plakken speciaal › Transponeren**.' || chr(10) || chr(10) ||
      '## 3. In het rekenblad hier in de browser' || chr(10) || chr(10) ||
      'Dat menu bestaat hier niet — Plakken speciaal zit alleen in echt Excel. Gebruik in dit' || chr(10) ||
      'portaal daarom de functie:' || chr(10) || chr(10) ||
      '```' || chr(10) ||
      '=TRANSPONEREN(B3:G4)' || chr(10) ||
      '```' || chr(10) || chr(10) ||
      'Je typt ze in de cel waar de linkerbovenhoek moet komen, en het gekantelde blok vult' || chr(10) ||
      'zichzelf over de cellen eronder en ernaast. Eén formule volstaat voor de hele tabel.' || chr(10) || chr(10) ||
      'Op stage werk je met echt Excel, dus leer allebei de wegen kennen: het menu daar, de' || chr(10) ||
      'functie hier.'
    ),
    gewijzigd_op = now()
where oefening_id = 'f1-transponeren'
  and inhoud like '%Plakken speciaal › Transponeren**.%'
  and inhoud not like '%=TRANSPONEREN(B3:G4)%';
