"""Busca secuencias de N palabras (6 por defecto) que el guion comparta literalmente con el texto de los libros.
Uso: python3 -I verificar_originalidad.py <carpeta_con_b1..b6.txt> [N]
(b1..b6.txt se generan con analisis/herramientas/extraer_texto.sh)"""
import csv, re, sys
from pathlib import Path
base = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 6
toks = lambda s: re.findall(r"[a-záéíóúüñ]+", s.lower())
grams = set()
for n in range(1, 7):
    t = toks(open(f"{base}/b{n}.txt", encoding="utf-8").read())
    grams.update(tuple(t[i:i + N]) for i in range(len(t) - N + 1))
csv_path = Path(__file__).resolve().parent.parent / "dialogos.csv"
hits = 0
for r in csv.DictReader(open(csv_path, encoding="utf-8")):
    t = toks(r["texto"])
    m = [" ".join(t[i:i + N]) for i in range(len(t) - N + 1) if tuple(t[i:i + N]) in grams]
    if m:
        hits += 1
        print(f"{r['id']}: «{m[0]}»")
print(f"Líneas con coincidencias de {N} palabras: {hits}")
