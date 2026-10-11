"""Verifica que cada cita “…” de un documento aparezca literalmente en el texto del libro indicado.
El libro es el «(Ln» que sigue a la cita; si no hay, el primer «Ln» de la línea; si no hay, el de la última sección «## Ln».
Uso: python3 -I verificar_atlas.py <dir_con_b1..b6.txt> <documento.md>"""
import re, sys
base, atlas = sys.argv[1], sys.argv[2]
books = {n: open(f"{base}/b{n}.txt", encoding="utf-8").read() for n in range(1, 7)}
ok = bad = 0
seccion = None
for line in open(atlas, encoding="utf-8"):
    h = re.match(r"##+ L([1-6])\b", line)
    if h:
        seccion = int(h.group(1))
    m = re.search(r"\bL([1-6])\b", line)
    if "[PARÁFRASIS]" in line or not (m or seccion):
        continue
    n = int(m.group(1)) if m else seccion
    for mq in re.finditer(r"“(.+?)”(\s*\(L([1-6]))?", line):
        q = mq.group(1)
        k = int(mq.group(3)) if mq.group(3) else n
        if q in books[k]:
            ok += 1
        else:
            bad += 1
            print(f"NO ENCONTRADA L{k}: {q}")
print("verificadas", ok, "fallidas", bad)
