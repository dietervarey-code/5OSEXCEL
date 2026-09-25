# Moord in Hotel Astrid

Een speurwerkopdracht van 50 minuten rond Excel. **Staat los van het oefenportaal**:
dit zijn drie bestanden die je uitdeelt, niet iets dat in de webtoepassing zit.

## Wat je uitdeelt

| Bestand | Voor wie |
|---|---|
| `moordzaak-startbestand.xlsx` | de leerlingen — negen bladen met de gegevens van die nacht |
| `moordzaak-opgave.docx` | de leerlingen — de opdracht in vijf fasen |
| `moordzaak-leerkracht.docx` | jou — oplossing, tijdsindeling, formules en de zes dossierkaarten om uit te knippen |

## Hoe het werkt

De werkmap alleen brengt hen er niet. Op zes momenten vraagt de opdracht om een
**dossierkaart**: het verslag van de wetsdokter, wat een getuige zag, hoe het personeel
gekleed gaat. Die staan achteraan in de leerkrachtenbundel en geef je pas op het moment
dat de opdracht erom vraagt. Zo loopt de verhaallijn door op papier, en moeten ze
Excel en redeneren afwisselen.

Excel-vaardigheden die aan bod komen: sorteren op meerdere kolommen, filteren,
`VERT.ZOEKEN`, `AANTAL.ALS`, voorwaardelijke opmaak, en printklaar maken.

De dader staat in de leerkrachtenbundel. Vertel het niet te vroeg.

## De bestanden opnieuw maken

De gegevens staan in `moordzaak-data.py`; de rest wordt daaruit gebouwd:

```bash
pip install openpyxl python-docx
python3 controleer.py     # rekent de bewijsketen na: sluit ze op één persoon?
python3 maak-xlsx.py      # bouwt het startbestand
python3 maak-docs.py      # bouwt de opgave en de leerkrachtenbundel
```

Wil je andere namen, een ander hotel of een ander tijdvak: pas `moordzaak-data.py` aan
en draai `controleer.py` opnieuw. Die zegt het meteen als de keten niet meer sluit.
