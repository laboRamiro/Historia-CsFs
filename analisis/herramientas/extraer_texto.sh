#!/usr/bin/env bash
# Extrae el texto de los 6 EPUB en orden de lectura (spine) a b1.txt … b6.txt,
# con una marca <<<ARCHIVO Text/Nombre.xhtml>>> al inicio de cada archivo/capítulo.
# Uso: extraer_texto.sh <carpeta_con_los_epub> <carpeta_de_salida>
# Requiere: unzip, pandoc, python3.
set -euo pipefail
src="$1"; out="$2"; mkdir -p "$out"
for n in 1 2 3 4 5 6; do
  epub=$(ls "$src"/*"[Lucky Starr $n]"*.epub)
  dir="$out/epub$n"; rm -rf "$dir"; mkdir -p "$dir"
  unzip -q -o "$epub" -d "$dir"
  opf=$(find "$dir" -name '*.opf' | head -1)
  python3 -I - "$opf" > "$out/orden$n.txt" <<'PY'
import sys, re, os
opf = open(sys.argv[1], encoding="utf-8").read()
items = dict(re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
items.update({i: h for h, i in re.findall(r'<item[^>]*href="([^"]+)"[^>]*id="([^"]+)"', opf)})
for idref in re.findall(r'<itemref[^>]*idref="([^"]+)"', opf):
    print(items[idref])
PY
  base=$(dirname "$opf")
  : > "$out/b$n.txt"
  while read -r href; do
    echo "<<<ARCHIVO $href>>>" >> "$out/b$n.txt"
    pandoc -f html -t plain --wrap=none "$base/$href" >> "$out/b$n.txt"
  done < "$out/orden$n.txt"
done
echo "Listo: $out/b1.txt … b6.txt"
