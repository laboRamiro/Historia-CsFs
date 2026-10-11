"""Genera el PDF ilustrado del guion (GUION_LUNE_GOLIAT.pdf) a partir de los capítulos en Markdown.

Uso:  python3 guion_videojuego/herramientas/generar_pdf_guion.py [--html-solo]
Requiere Chromium (variable CHROMIUM o /opt/pw-browsers/chromium) y conexión para las fuentes de Google.
"""
import html, os, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contexto_escenas import TEMAS, ESCENAS, TIPOS

RAIZ = Path(__file__).resolve().parent.parent
SALIDA_HTML = RAIZ / "herramientas" / "_guion_pdf.html"
SALIDA_PDF = RAIZ / "GUION_LUNE_GOLIAT.pdf"

TEMA_CAPITULO = {1: "marte", 2: "cinturon", 3: "venus", 4: "mercurio_dia", 5: "jupiter", 6: "saturno"}

# Color de voz por personaje (constante en todo el guion)
VOCES = {
    "LUNE": "#B4461D", "ESPECTRO": "#B4461D", "GOLIAT": "#137A73", "ERRANTE": "#5E6B7D",
    "CORVO": "#8C6A12", "FERRÁN": "#6B5B95", "DRA. SALEH": "#8C6A12", "WESSEL": "#2F6B9A",
    "SILENTE JOVEN": "#2453C9", "SILENTE ANCIANO": "#1A3A8F", "VOZ DE LAS ONDINAS": "#2E7D4F",
    "DRAVIN": "#6A4C93", "ZETA": "#6A4C93", "ROBOTS VEGANOS": "#6A4C93", "CAPITANA YON": "#6A4C93",
    "ALTAVOZ VEGANO": "#6A4C93", "CENTINELA": "#7A4A2A",
}
COLOR_PNJ = "#33363D"

def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t

def acotaciones(t):
    """Paréntesis del texto hablado → acotación en cursiva."""
    t = md_inline(t)
    return re.sub(r"\(([^)]*)\)", r'<span class="acot">(\1)</span>', t)

def celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]

FILA_ID = re.compile(r"^\|\s*((?:C[1-6]|SIS)_[A-Z]+\d*_[0-9A-Za-z]+)\s*\|")
TITULO_ESC = re.compile(r"^#{3,4}\s+((C[1-6])_([A-Z]+)(\d+))\s+—\s+(.*)$")

def parse_capitulo(path):
    lineas = path.read_text(encoding="utf-8").splitlines()
    cap = {"titulo": lineas[0].lstrip("# ").strip(), "ficha": [], "personajes": [], "escenas": []}
    seccion, esc = None, None
    for l in lineas[1:]:
        if l.startswith("## "):
            seccion = l[3:].strip()
            esc = None
            continue
        m = TITULO_ESC.match(l)
        if m:
            esc = {"id": m.group(1), "tipo": m.group(3), "titulo": m.group(5).strip(), "meta": [], "filas": []}
            cap["escenas"].append(esc)
            continue
        if esc is None:
            if l.startswith("|") and not l.startswith("|---"):
                c = celdas(l)
                if seccion == "Ficha" and c[0] != "Campo":
                    cap["ficha"].append(c)
                elif seccion and seccion.startswith("Personajes") and c[0] != "Personaje":
                    cap["personajes"].append(c)
            continue
        if FILA_ID.match(l):
            c = celdas(l)
            if len(c) == 5:
                esc["filas"].append(dict(zip(["id", "trigger", "personaje", "texto", "direccion"], c)))
        elif l.startswith("**") or (l.strip() and not l.startswith("|") and not esc["filas"]):
            esc["meta"].append(l.strip())
    return cap

def voz(personaje):
    base = personaje.split(" (")[0].strip()
    return base, VOCES.get(base, COLOR_PNJ)

def render_fila(f):
    trig, pers, texto, dirc = f["trigger"], f["personaje"], f["texto"], f["direccion"]
    nombre, color = voz(pers)
    extra = ""
    clases = ["linea"]
    etiqueta = ""
    if trig.startswith("ELECCIÓN"):
        clases.append("eleccion")
        letra = re.search(r"\((A|B|C)\)", pers)
        etiqueta = f'<span class="chip chip-elec">Opción {letra.group(1) if letra else ""} del jugador</span>'
        if "BLOQUEADA" in trig:
            clases.append("bloqueada")
            etiqueta = '<span class="chip chip-bloq">Opción bloqueada</span>'
    elif trig.startswith("COND("):
        cond = trig[5:].rstrip(")")
        etiqueta = f'<span class="chip chip-cond">Si se eligió {html.escape(cond)}</span>'
    elif trig.startswith("ACUSACIÓN"):
        ok = "correcta" in trig
        clases.append("acus-ok" if ok else "acus-mal")
        etiqueta = f'<span class="chip {"chip-ok" if ok else "chip-mal"}">{html.escape(trig.capitalize())}</span>'
    if "EVT(" in trig or trig.startswith("EVT"):
        evento = re.search(r"EVT\(([^)]*)\)", trig)
        nombre_evt = evento.group(1) if evento else trig.replace("EVT", "").strip() or "evento"
        extra = f'<div class="evento"><span>EVENTO</span> {html.escape(nombre_evt)}</div>'
    if trig.startswith("CIN") and not extra:
        extra = '<div class="evento cine"><span>CINEMÁTICA</span></div>'
    ruta = re.search(r"RUTA (\d+)%", trig)
    if ruta:
        p = int(ruta.group(1))
        extra = (f'<div class="hito"><div class="barra"><div style="width:{max(p,2)}%"></div></div>'
                 f'<span>{p}% del trayecto</span></div>') + extra
    sfx = texto.startswith("(") and texto.endswith(")")
    if sfx:
        clases.append("sfx")
    dir_html = md_inline(dirc)
    return (f'{extra}<div class="{" ".join(clases)}">'
            f'<div class="meta-l"><code>{f["id"]}</code><small>{html.escape(trig)}</small></div>'
            f'<div class="cuerpo"><div class="quien" style="color:{color}">{html.escape(nombre)}'
            f'{etiqueta}</div>'
            f'<div class="texto">{acotaciones(texto)}</div>'
            f'<div class="direccion">{dir_html}</div></div></div>')

def render_escena(e, n_cap):
    tema_k, lugar, situacion = ESCENAS[e["id"]]
    nombre_t, fondo, papel, tinta, acento, suave, arte = TEMAS[tema_k]
    filas = [f for f in e["filas"] if not re.search(r"_R\d+$", f["id"])]
    relleno = [f for f in e["filas"] if re.search(r"_R\d+$", f["id"])]
    vistos = []
    for f in e["filas"]:
        n, _ = voz(f["personaje"])
        if n not in vistos and not n.startswith(("PNJ", "DELEGADOS")):
            vistos.append(n)
    quienes = " · ".join(f'<span style="color:{voz(n)[1]}">{html.escape(n.title() if n not in ("GOLIAT", "ERRANTE") else n)}</span>' for n in vistos)
    meta = "".join(f"<p>{md_inline(m)}</p>" for m in e["meta"])
    titulo = re.sub(r"\s*\((?:CIN01|DED final)\)", "", e["titulo"])
    cuerpo = "".join(render_fila(f) for f in filas)
    if relleno:
        cuerpo += ('<div class="relleno"><h4>Relleno de viaje · suena tras 15 s de silencio</h4>'
                   + "".join(render_fila(f) for f in relleno) + "</div>")
    tipo = TIPOS.get(e["tipo"], e["tipo"])
    return f"""
<section class="escena tipo-{e['tipo']}" style="page:t_{tema_k};--papel:{papel};--tinta:{tinta};--acento:{acento};--suave:{suave};">
  <header class="banda" style="background:{fondo};">
    <div class="velo"></div>
    <div class="banda-txt">
      <div class="banda-sup"><span>CAPÍTULO {n_cap}</span><span>{tipo.upper()}</span><span>{e['id']}</span></div>
      <h2>{md_inline(titulo)}</h2>
      <div class="lugar">{html.escape(lugar)}</div>
    </div>
  </header>
  <div class="contexto">
    <div class="ctx-col">
      <h5>Situación</h5><p class="situacion">{html.escape(situacion)}</p>
      <h5>En escena</h5><p class="quienes">{quienes}</p>
    </div>
    <div class="ctx-col">
      <h5>Ambiente · {html.escape(nombre_t)}</h5><p class="arte">{html.escape(arte)}</p>
      {('<h5>Notas de juego</h5><div class="notas">' + meta + '</div>') if meta else ''}
    </div>
  </div>
  <div class="dialogo">{cuerpo}</div>
</section>"""

def render_apertura(n, cap):
    tema = TEMAS[TEMA_CAPITULO[n]]
    titulo = cap["titulo"].split("—", 1)[-1].strip()
    nombre, mundo = (titulo.split("(")[0].strip(), titulo.split("(")[1].rstrip(")") if "(" in titulo else "")
    ficha = {c[0]: c[1] for c in cap["ficha"] if len(c) > 1}
    filas = "".join(f"<tr><th>{html.escape(k)}</th><td>{md_inline(ficha[k])}</td></tr>"
                    for k in ("Mundos", "Mundo", "Caso", "Culpable", "Culpables", "Giro", "Giro del dúo",
                              "Momento clave del dúo", "Objetivo emocional", "Mejora obtenida")
                    if k in ficha)
    elenco = "".join(f"<li><b>{md_inline(p[0])}</b> — {md_inline(p[1])}"
                     f"{(' <i>· ' + md_inline(p[2]) + '</i>') if len(p) > 2 else ''}</li>" for p in cap["personajes"])
    escenas = "".join(f"<li><code>{e['id']}</code> {md_inline(re.sub(r' \((?:CIN01|DED final)\)', '', e['titulo']))}</li>"
                      for e in cap["escenas"])
    return f"""
<section class="apertura" style="background:{tema[1]};">
  <div class="velo-ap"></div>
  <div class="ap-txt">
    <div class="ap-num">{n:02d}</div>
    <h1>{md_inline(nombre)}</h1>
    <div class="ap-mundo">{html.escape(mundo)}</div>
  </div>
</section>
<section class="ficha-cap" style="--acento:{tema[4]};">
  <h3>Capítulo {n} · Ficha del caso</h3>
  <table class="ficha">{filas}</table>
  <div class="dos-col">
    <div><h4>Elenco del capítulo</h4><ul class="elenco">{elenco}</ul></div>
    <div><h4>Escenas en orden de juego</h4><ol class="indice-esc">{escenas}</ol></div>
  </div>
</section>"""

def render_sis():
    texto = (RAIZ / "07_AVISOS_Y_RELLENOS_DE_SISTEMA.md").read_text(encoding="utf-8").splitlines()
    out, filas, titulo = [], [], None
    def volcar():
        if titulo and filas:
            out.append(f'<h3 class="sis-t">{md_inline(titulo)}</h3><div class="dialogo">'
                       + "".join(render_fila(f) for f in filas) + "</div>")
    for l in texto:
        if l.startswith("## "):
            volcar(); titulo, filas = l[3:], []
        elif FILA_ID.match(l):
            c = celdas(l)
            filas.append(dict(zip(["id", "trigger", "personaje", "texto", "direccion"], c)))
    volcar()
    t = TEMAS["espacio"]
    return f"""
<section class="apertura" style="background:{t[1]};"><div class="velo-ap"></div>
<div class="ap-txt"><div class="ap-num">AP</div><h1>Voces del sistema</h1><div class="ap-mundo">Avisos de navegación y relleno general</div></div></section>
<section class="escena" style="page:t_espacio;--papel:{t[2]};--tinta:{t[3]};--acento:{t[4]};--suave:{t[5]};"><div class="contexto solo">
<p class="situacion">Líneas reutilizables en los seis capítulos: la voz de la nave da el dato y GOLIAT reacciona. Antes de conocer a GOLIAT (capítulo 1) reacciona Lune.</p></div>{''.join(out)}</section>"""

LEYENDA_VOCES = [("LUNE", "Inspector Darío Lune (protagonista)"), ("GOLIAT", "Robot compañero"),
                 ("ERRANTE", "Sistema de la nave (voz sintética)"), ("CORVO", "Directora de la ACS"),
                 ("FERRÁN", "Científico de la ACS"), ("DRAVIN", "Vega (todos sus personajes)"),
                 ("SILENTE JOVEN", "Seres de energía de Marte"), ("VOZ DE LAS ONDINAS", "La «voz» de Venus")]

def render_portada_y_guia():
    voces = "".join(f'<li><span class="pastilla" style="background:{voz(k)[1]}"></span><b style="color:{voz(k)[1]}">{k}</b> {d}</li>'
                    for k, d in LEYENDA_VOCES)
    voces += f'<li><span class="pastilla" style="background:{COLOR_PNJ}"></span><b>OTROS</b> Personajes de cada capítulo</li>'
    temas = "".join(f'<div class="tema"><div class="muestra" style="background:{t[1]}"></div>'
                    f'<div><b>{html.escape(t[0])}</b><p>{html.escape(t[6])}</p></div></div>' for t in TEMAS.values())
    return f"""
<section class="portada">
  <svg class="orbitas" viewBox="0 0 600 600" aria-hidden="true"><g fill="none" stroke="#3FB8AF" stroke-opacity=".35" stroke-width="1.5"><circle cx="300" cy="300" r="90"/><circle cx="300" cy="300" r="150"/><circle cx="300" cy="300" r="210"/><circle cx="300" cy="300" r="270" stroke-dasharray="4 10"/></g><circle cx="300" cy="300" r="30" fill="#E8B53A"/><circle cx="390" cy="300" r="8" fill="#E0612F"/><circle cx="194" cy="194" r="12" fill="#C9D3E0"/><circle cx="449" cy="449" r="20" fill="#D9A15C"/><ellipse cx="449" cy="449" rx="40" ry="11" fill="none" stroke="#F2E8D5" stroke-width="3" transform="rotate(-25 449 449)"/></svg>
  <div class="port-txt">
    <p class="exp">Guion de diálogos · Versión 1.0</p>
    <h1>Lune <span>&amp;</span> Goliat</h1>
    <p class="sub">Expedientes del Sistema Solar</p>
    <p class="desc">Guion completo de los seis capítulos, con cada escena ambientada según su lugar y contada con su contexto: dónde ocurre, quiénes hablan y qué está en juego.</p>
  </div>
  <p class="pie">[Nombre del estudio] · Documento de trabajo confidencial</p>
</section>
<section class="guia">
  <h3>Cómo leer este guion</h3>
  <div class="dos-col">
    <div>
      <h4>Cada escena</h4>
      <ul class="lista">
        <li><b>Banda superior:</b> el lugar, con la estética de su ambiente.</li>
        <li><b>Contexto:</b> situación dramática, quién está en escena, dirección de arte y notas de juego.</li>
        <li><b>Diálogo:</b> a la izquierda, el identificador y el disparador; a la derecha, quién habla, la línea y la nota de actuación en cursiva.</li>
        <li><b>Barra de trayecto:</b> en los viajes, marca en qué porcentaje de la ruta suena la línea.</li>
        <li><b>Relleno de viaje:</b> líneas que suenan si pasan 15 s de silencio.</li>
      </ul>
      <h4>Marcas</h4>
      <ul class="lista">
        <li><span class="chip chip-elec">Opción del jugador</span> lo que el jugador elige decir.</li>
        <li><span class="chip chip-cond">Si se eligió A</span> la línea depende de esa elección.</li>
        <li><span class="chip chip-ok">Acusación correcta</span> <span class="chip chip-mal">Acusación errónea</span> respuestas del tablero de deducción.</li>
        <li><span class="evento-mini">EVENTO</span> una situación de juego interrumpe el viaje.</li>
      </ul>
    </div>
    <div>
      <h4>Colores de voz</h4>
      <ul class="voces">{voces}</ul>
    </div>
  </div>
</section>
<section class="guia">
  <h3>Ambientes de la saga</h3>
  <p class="intro">Cada escena toma la estética del lugar donde ocurre. La paleta general combina tres épocas: el pulp atómico de los años cincuenta, el modo oscuro de hoy y el holograma del año 3112.</p>
  <div class="temas">{temas}</div>
</section>"""

CSS = r"""
@page { size: A4; margin: 14mm 0 16mm 0; @bottom-right { content: counter(page); font: 600 8pt 'JetBrains Mono', monospace; color: #8A8F99; margin-right: 16mm; } @bottom-left { content: "LUNE & GOLIAT · Guion v1.0"; font: 500 7.5pt 'JetBrains Mono', monospace; color: #A0A5AE; margin-left: 16mm; } }
@page completa { margin: 0; @bottom-right { content: none; } @bottom-left { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: 'Space Grotesk', Arial, sans-serif; font-size: 9.6pt; color: #1E2433; line-height: 1.45; }
code { font-family: 'JetBrains Mono', monospace; font-size: .86em; }
h1, h2, h3, h4, h5 { margin: 0; }
.portada, .apertura { page: completa; break-after: page; height: 297mm; width: 210mm; position: relative; overflow: hidden; }
.portada { background: radial-gradient(circle at 75% 35%, #1F3150 0%, #0E1726 62%); color: #F2E8D5; }
.orbitas { position: absolute; right: -30mm; top: 18mm; width: 170mm; height: 170mm; }
.port-txt { position: absolute; left: 18mm; bottom: 46mm; width: 160mm; }
.exp { font-family: 'JetBrains Mono', monospace; color: #3FB8AF; letter-spacing: 3px; text-transform: uppercase; font-size: 9pt; }
.portada h1 { font-family: 'Big Shoulders Display', Impact, sans-serif; font-weight: 900; font-size: 92pt; line-height: .88; text-transform: uppercase; }
.portada h1 span { color: #E0612F; }
.sub { font-family: 'Big Shoulders Display', Impact, sans-serif; font-size: 24pt; letter-spacing: 4px; color: #E8B53A; text-transform: uppercase; margin: 4mm 0 6mm; font-weight: 700; }
.desc { font-size: 11.5pt; color: #C9D3E0; width: 125mm; }
.pie { position: absolute; left: 18mm; bottom: 14mm; font-family: 'JetBrains Mono', monospace; font-size: 8pt; color: #8A97AB; }
.guia, .ficha-cap { break-after: page; padding: 4mm 16mm; }
.guia h3, .ficha-cap h3 { font-family: 'Big Shoulders Display', Impact, sans-serif; font-weight: 800; font-size: 30pt; text-transform: uppercase; color: #0E1726; margin-bottom: 5mm; }
.guia h4, .ficha-cap h4 { font-family: 'JetBrains Mono', monospace; font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase; color: #B4461D; margin: 5mm 0 2.5mm; }
.ficha-cap h4 { color: var(--acento); }
.dos-col { display: grid; grid-template-columns: 1fr 1fr; gap: 9mm; }
.lista { padding-left: 4mm; margin: 0; } .lista li { margin-bottom: 2mm; }
.voces { list-style: none; padding: 0; margin: 0; } .voces li { margin-bottom: 2.6mm; }
.pastilla { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.intro { font-size: 10.5pt; color: #3D3A35; width: 160mm; margin-bottom: 5mm; }
.temas { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 7mm; }
.tema { display: grid; grid-template-columns: 22mm 1fr; gap: 3.5mm; align-items: start; break-inside: avoid; }
.tema .muestra { height: 15mm; border-radius: 3px; }
.tema b { font-size: 9.5pt; } .tema p { margin: .5mm 0 0; font-size: 8.2pt; color: #4A4F59; line-height: 1.35; }
.apertura { display: block; }
.velo-ap { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(8,10,16,.82) 0%, rgba(8,10,16,.15) 55%, rgba(8,10,16,0) 100%); }
.ap-txt { position: absolute; left: 18mm; bottom: 30mm; width: 175mm; color: #F7F2E8; }
.ap-num { font-family: 'Big Shoulders Display', Impact, sans-serif; font-size: 130pt; font-weight: 900; line-height: .8; opacity: .9; }
.apertura h1 { font-family: 'Big Shoulders Display', Impact, sans-serif; font-size: 54pt; font-weight: 900; text-transform: uppercase; line-height: .95; margin-top: 4mm; }
.ap-mundo { font-family: 'JetBrains Mono', monospace; letter-spacing: 3px; text-transform: uppercase; font-size: 10pt; margin-top: 4mm; color: #E8DCC2; }
.ficha { width: 100%; border-collapse: collapse; margin-bottom: 4mm; }
.ficha th { text-align: left; width: 36mm; font-family: 'JetBrains Mono', monospace; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; color: #6A6F78; padding: 2mm 3mm 2mm 0; vertical-align: top; border-top: 1px solid #E2DED6; font-weight: 600; }
.ficha td { padding: 2mm 0; border-top: 1px solid #E2DED6; }
.elenco { list-style: none; padding: 0; margin: 0; font-size: 8.8pt; } .elenco li { margin-bottom: 1.8mm; }
.indice-esc { padding-left: 5mm; margin: 0; font-size: 8.8pt; } .indice-esc li { margin-bottom: 1.2mm; }
.indice-esc code { color: #8A8F99; margin-right: 1.5mm; }
/* ESCENAS */
.escena { break-before: page; background: var(--papel); color: var(--tinta); padding: 0 0 6mm; -webkit-box-decoration-break: clone; box-decoration-break: clone; min-height: 267mm; }
.banda { position: relative; height: 52mm; margin: 0; overflow: hidden; }
.banda .velo { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(6,8,14,.80) 0%, rgba(6,8,14,.35) 55%, rgba(6,8,14,.05) 100%); }
.banda-txt { position: absolute; left: 16mm; right: 16mm; bottom: 6mm; color: #FAF6EE; }
.banda-sup { display: flex; gap: 5mm; font-family: 'JetBrains Mono', monospace; font-size: 7.6pt; letter-spacing: 2px; color: #E9E2D2; margin-bottom: 2mm; }
.banda h2 { font-family: 'Big Shoulders Display', Impact, sans-serif; font-weight: 800; font-size: 25pt; line-height: 1; text-transform: uppercase; }
.lugar { font-size: 9.5pt; margin-top: 1.5mm; color: #EFE7D6; }
.contexto { display: grid; grid-template-columns: 1.1fr 1fr; gap: 7mm; margin: 6mm 16mm 5mm; padding: 4.5mm 5mm; background: rgba(255,255,255,.55); border-left: 3px solid var(--acento); border-radius: 2px; break-inside: avoid; }
.contexto.solo { display: block; margin-top: 4mm; }
.contexto h5 { font-family: 'JetBrains Mono', monospace; font-size: 7.2pt; letter-spacing: 1.6px; text-transform: uppercase; color: var(--acento); margin: 0 0 1mm; }
.contexto p { margin: 0 0 3mm; } .contexto .notas p { margin: 0 0 1.4mm; font-size: 8.3pt; color: #4A4F59; }
.situacion { font-size: 10.2pt; font-weight: 500; }
.arte { font-size: 8.6pt; font-style: italic; color: #4A4F59; }
.quienes { font-weight: 700; font-size: 9pt; }
.dialogo { margin: 0 16mm; }
.linea { display: grid; grid-template-columns: 27mm 1fr; gap: 4mm; padding: 2.2mm 0; border-top: 1px solid var(--suave); break-inside: avoid; }
.meta-l code { display: block; color: #6A6F78; font-size: 7pt; }
.meta-l small { display: block; font-family: 'JetBrains Mono', monospace; font-size: 6.6pt; color: #9198A3; line-height: 1.3; margin-top: .6mm; }
.quien { font-family: 'Big Shoulders Display', Impact, sans-serif; font-weight: 800; font-size: 11.5pt; letter-spacing: 1.2px; text-transform: uppercase; }
.texto { font-size: 10pt; margin-top: .4mm; }
.direccion { font-size: 7.8pt; font-style: italic; color: #747A85; margin-top: .6mm; }
.direccion b { font-style: normal; background: var(--acento); color: #FFF; padding: 0 1.4mm; border-radius: 2px; font-size: 7pt; letter-spacing: .4px; }
.acot { font-style: italic; color: #7A808A; font-size: .92em; }
.sfx .texto { font-style: italic; color: #6A707A; }
.chip { display: inline-block; font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 6.6pt; letter-spacing: .6px; text-transform: uppercase; padding: .4mm 1.6mm; border-radius: 8px; margin-left: 2mm; vertical-align: 2px; }
.chip-elec { background: #E0612F; color: #fff; } .chip-cond { background: #E3DFD6; color: #4A4F59; }
.chip-bloq { background: #B8BCC4; color: #fff; } .chip-ok { background: #1C7A4F; color: #fff; } .chip-mal { background: #9A2F2F; color: #fff; }
.eleccion .cuerpo { background: rgba(224,97,47,.08); border: 1px dashed rgba(224,97,47,.55); border-radius: 3px; padding: 1.6mm 2.4mm; }
.bloqueada .texto { text-decoration: line-through; color: #9AA0AA; }
.acus-mal .cuerpo { border-left: 2px solid #9A2F2F; padding-left: 2.4mm; } .acus-ok .cuerpo { border-left: 2px solid #1C7A4F; padding-left: 2.4mm; }
.hito { display: flex; align-items: center; gap: 3mm; margin: 3mm 0 1mm 31mm; font-family: 'JetBrains Mono', monospace; font-size: 7pt; color: var(--acento); letter-spacing: 1px; text-transform: uppercase; break-after: avoid; }
.barra { width: 40mm; height: 3px; background: var(--suave); border-radius: 2px; } .barra div { height: 3px; background: var(--acento); border-radius: 2px; }
.evento { margin: 3mm 0 1mm 31mm; font-size: 8.4pt; font-weight: 600; color: var(--tinta); break-after: avoid; }
.evento span, .evento-mini { font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; letter-spacing: 1.4px; background: var(--tinta, #1E2433); color: var(--papel, #fff); padding: .5mm 1.8mm; border-radius: 2px; margin-right: 2mm; }
.evento-mini { background: #1E2433; color: #fff; }
.evento.cine span { background: #0B0B0E; color: #F2E8D5; }
.relleno { margin-top: 5mm; padding: 1mm 3mm 2mm; border: 1px solid var(--suave); border-radius: 3px; background: rgba(255,255,255,.4); break-inside: auto; }
.relleno h4 { font-family: 'JetBrains Mono', monospace; font-size: 7.2pt; letter-spacing: 1.6px; text-transform: uppercase; color: var(--acento); margin: 2mm 0 1mm; }
.tipo-CIN .banda::after, .tipo-DED .banda::after { content: ""; position: absolute; left: 0; right: 0; height: 5mm; background: #0B0B0E; top: 0; }
.tipo-CIN .banda::before { content: ""; position: absolute; left: 0; right: 0; height: 5mm; background: #0B0B0E; bottom: 0; z-index: 2; }
.sis-t { font-family: 'Big Shoulders Display', Impact, sans-serif; font-size: 16pt; text-transform: uppercase; margin: 6mm 16mm 2mm; }
"""

def main():
    caps = [parse_capitulo(p) for p in sorted(RAIZ.glob("0[1-6]_CAPITULO_*.md"))]
    faltan = [e["id"] for c in caps for e in c["escenas"] if e["id"] not in ESCENAS]
    if faltan:
        sys.exit(f"Escenas sin contexto: {faltan}")
    cuerpo = render_portada_y_guia()
    for n, cap in enumerate(caps, 1):
        cuerpo += render_apertura(n, cap)
        cuerpo += "".join(render_escena(e, n) for e in cap["escenas"])
    cuerpo += render_sis()
    fuentes = ("https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800;900"
               "&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap")
    css_paginas = "".join(f"@page t_{k} {{ background: {t[2]}; }}" for k, t in TEMAS.items())
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Lune &amp; Goliat · Guion</title>'
           f'<link rel="stylesheet" href="{fuentes}"><style>{CSS}{css_paginas}</style></head><body>{cuerpo}</body></html>')
    SALIDA_HTML.write_text(doc, encoding="utf-8")
    print("HTML:", SALIDA_HTML)
    if "--html-solo" in sys.argv:
        return
    chrome = os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={SALIDA_PDF}", SALIDA_HTML.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("PDF:", SALIDA_PDF)

if __name__ == "__main__":
    main()
