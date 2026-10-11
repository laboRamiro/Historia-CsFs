"""Exporta todas las líneas del guion a dialogos.csv, valida los IDs y genera ESTADISTICAS.md.

Uso:  python3 guion_videojuego/herramientas/exportar_dialogos.py
Lee las tablas Markdown de 01_…07_*.md cuyas filas empiezan por un ID C1_…C6_ o SIS_.
Columnas esperadas en cada tabla: ID | Trigger | Personaje | Línea | Dirección
"""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PALABRAS_POR_SEGUNDO = 2.6
FILA = re.compile(r"^\|\s*((?:C[1-6]|SIS)_[A-Z]+\d*_[0-9A-Za-z]+)\s*\|(.*)\|\s*$")

def celdas(resto):
    return [c.strip() for c in resto.split("|")]

def palabras(texto):
    # Sin acotaciones entre paréntesis ni marcas de formato
    limpio = re.sub(r"\([^)]*\)", " ", texto)
    limpio = re.sub(r"[*_`\[\]]", " ", limpio)
    return len(re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ']+", limpio))

def main():
    filas, errores, avisos = [], [], []
    vistos = {}
    for md in sorted(RAIZ.glob("0[1-7]_*.md")):
        for n, linea in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            m = FILA.match(linea)
            if not m:
                continue
            ident, resto = m.group(1), celdas(m.group(2))
            if len(resto) != 4:
                errores.append(f"{md.name}:{n} {ident}: se esperaban 5 columnas, hay {len(resto) + 1}")
                continue
            trigger, personaje, texto, direccion = resto
            if ident in vistos:
                errores.append(f"{md.name}:{n} ID duplicado {ident} (ya en {vistos[ident]})")
            vistos[ident] = f"{md.name}:{n}"
            cap = ident.split("_")[0]
            bloque = "_".join(ident.split("_")[:2])
            p = palabras(texto)
            filas.append({"id": ident, "capitulo": cap, "bloque": bloque, "trigger": trigger,
                          "personaje": personaje, "texto": texto, "direccion": direccion,
                          "palabras": p, "duracion_s": round(p / PALABRAS_POR_SEGUNDO, 1)})

    # Validación de la cobertura de los viajes: hitos RUTA y pool de relleno
    por_bloque = defaultdict(list)
    for f in filas:
        por_bloque[f["bloque"]].append(f)
    for bloque, fs in por_bloque.items():
        if "_VIA" not in bloque:
            continue
        hitos = {f["trigger"] for f in fs if f["trigger"].startswith("RUTA")}
        relleno = [f for f in fs if re.search(r"_R\d+$", f["id"])]
        if len(hitos) < 4:
            avisos.append(f"{bloque}: sólo {len(hitos)} hitos RUTA distintos")
        if not relleno:
            avisos.append(f"{bloque}: sin pool de relleno R")

    with open(RAIZ / "dialogos.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    # Estadísticas
    por_cap = defaultdict(lambda: [0, 0, 0.0])
    por_pers = Counter()
    por_tipo = defaultdict(lambda: [0, 0.0])
    for f in filas:
        c = por_cap[f["capitulo"]]; c[0] += 1; c[1] += f["palabras"]; c[2] += f["duracion_s"]
        por_pers[f["personaje"].split(" (")[0]] += f["palabras"]
        tipo = re.sub(r"\d+", "", f["bloque"].split("_")[1])
        t = por_tipo[tipo]; t[0] += 1; t[1] += f["duracion_s"]
    out = ["# Estadísticas del guion (generado automáticamente)", "",
           "| Capítulo | Líneas | Palabras | Audio estimado (min) |", "|---|---|---|---|"]
    tot = [0, 0, 0.0]
    for cap in sorted(por_cap):
        l, p, d = por_cap[cap]; tot[0] += l; tot[1] += p; tot[2] += d
        out.append(f"| {cap} | {l} | {p} | {d/60:.1f} |")
    out.append(f"| **Total** | **{tot[0]}** | **{tot[1]}** | **{tot[2]/60:.1f}** |")
    out += ["", "| Tipo de bloque | Líneas | Audio (min) |", "|---|---|---|"]
    for t, (l, d) in sorted(por_tipo.items()):
        out.append(f"| {t} | {l} | {d/60:.1f} |")
    out += ["", "| Personaje | Palabras |", "|---|---|"]
    for pers, p in por_pers.most_common():
        out.append(f"| {pers} | {p} |")
    if avisos:
        out += ["", "## Avisos de cobertura", ""] + [f"- {a}" for a in avisos]
    (RAIZ / "ESTADISTICAS.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"Líneas exportadas: {len(filas)} · palabras: {tot[1]} · audio ≈ {tot[2]/60:.1f} min")
    for a in avisos:
        print("AVISO:", a)
    for e in errores:
        print("ERROR:", e)
    sys.exit(1 if errores else 0)

if __name__ == "__main__":
    main()
