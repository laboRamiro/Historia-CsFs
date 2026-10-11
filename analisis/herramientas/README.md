# Herramientas

- `extraer_texto.sh <carpeta_epub> <salida>`: descomprime los 6 EPUB y genera `b1.txt` … `b6.txt` en orden de lectura, con marcas `<<<ARCHIVO Text/CapituloN.xhtml>>>` que permiten ubicar el capítulo de cada cita. Requiere `unzip`, `pandoc` y `python3`.
- `verificar_atlas.py <salida> <documento.md>`: comprueba que cada cita entre comillas tipográficas “…” de un documento aparezca literalmente en el libro indicado (`Ln`).
- `verificar_citas.py <salida> <lista.txt>`: versión de trabajo; lee líneas `n|cita` y dice en qué capítulo aparece cada una.

Ejemplo:

```bash
analisis/herramientas/extraer_texto.sh . /tmp/lucky
for f in analisis/*.md; do python3 -I analisis/herramientas/verificar_atlas.py /tmp/lucky "$f"; done
```

Los textos extraídos no se suben al repositorio; sólo los EPUB originales y el análisis.
