import 'server-only';
import * as XLSX from 'xlsx';
import type { UploadOpgave } from '@/lib/werkblad-types';

/**
 * Maakt het .xlsx-bestand dat de leerling downloadt om mee te beginnen.
 *
 * We genereren het bij elke download opnieuw, zodat er geen binaire bestanden
 * in de repo hoeven te staan en een wijziging aan de opgave meteen doorwerkt.
 */
export function maakStartbestand(opgave: UploadOpgave): Uint8Array {
  const { bladnaam, rijen, breedtes } = opgave.startbestand;

  const blad = XLSX.utils.aoa_to_sheet(rijen);
  if (breedtes) blad['!cols'] = breedtes.map((w) => ({ wch: w }));

  const werkmap = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(werkmap, blad, bladnaam);

  return new Uint8Array(XLSX.write(werkmap, { type: 'array', bookType: 'xlsx' }));
}

/** Bestandsnaam waaronder de leerling het bestand krijgt. */
export function startbestandNaam(opgave: UploadOpgave): string {
  return `${opgave.id}.xlsx`;
}
