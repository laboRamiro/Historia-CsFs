# ANÁLISIS MAESTRO — Saga *Lucky Starr* de Isaac Asimov

> Documento de entrada. Resume el método, el inventario (Fase 0), las conclusiones principales de cada fase y enlaza al resto de los documentos.

## Índice de documentos

| Documento | Contenido |
|---|---|
| [ANALISIS_MAESTRO.md](ANALISIS_MAESTRO.md) | Este documento: inventario, método, conclusiones |
| [ANALISIS_POR_LIBRO.md](ANALISIS_POR_LIBRO.md) | Fase 1: los seis libros, con argumento y final, estructura, géneros, temas, evolución y conexiones |
| [MATRIZ_DE_PERSONAJES_Y_RELACIONES.md](MATRIZ_DE_PERSONAJES_Y_RELACIONES.md) | Fases 2, 3, 4 y 6: Lucky–Bigman, robots, secundarios, extraterrestres, antagonistas |
| [BIBLIA_DEL_UNIVERSO.md](BIBLIA_DEL_UNIVERSO.md) | Fases 5 y 7: geopolítica, Consejo, Sirio, derecho, tecnología, biología, humor |
| [CRONOLOGIA_Y_MAPA_ESPACIAL.md](CRONOLOGIA_Y_MAPA_ESPACIAL.md) | Fases 8 y 9: lugares clasificados, ¿todo en el Sistema Solar?, cronología |
| [PREGUNTAS_ABIERTAS_Y_CONTRADICCIONES.md](PREGUNTAS_ABIERTAS_Y_CONTRADICCIONES.md) | Fase 9: contradicciones, ironías, preguntas abiertas, erratas |
| [ATLAS_DE_CITAS.md](ATLAS_DE_CITAS.md) | Unas 220 citas literales verificadas, con libro, capítulo, quién habla, contexto e importancia |
| [herramientas/](herramientas/) | Scripts de extracción del texto y de verificación de citas |

---

## Fase 0 — Inventario y verificación

**Contenido del repositorio** (commit `c62806a`, «Add files via upload»): exactamente **6 archivos EPUB** y nada más. No hay libros repetidos ni faltantes dentro de la serie original de Lucky Starr (la saga tiene seis novelas: 1952–1958) [la cifra total de la saga es un dato EXTERNO que coincide con lo subido].

| # | Archivo | Título en español | Título original | Año orig. | Traducción | Capítulos | Palabras aprox. | Paratextos |
|---|---|---|---|---|---|---|---|---|
| L1 | `[Lucky Starr 1] El Ranger del espacio [3953] (r1.2).epub` | *El Ranger del espacio* | *David Starr, Space Ranger* | 1952 | Ana Goldar (1976) | 16 | 42.900 | Introducción de Asimov (1970) |
| L2 | `[Lucky Starr 2] Los piratas de los asteroides [4274] (r1.2).epub` | *Los piratas de los asteroides* | *Lucky Starr and the Pirates of the Asteroids* | 1953 | Ana Goldar | 16 | 44.800 | Dedicatoria a Frederick Pohl |
| L3 | `[Lucky Starr 3] Los oceanos de Venus [4521] (r1.4).epub` | *Los océanos de Venus* | *Lucky Starr and the Oceans of Venus* | 1954 | Miguel Giménez Sales | 16 | 40.000 | Dedicatoria a Margaret Lesser; Introducción (1970); notas |
| L4 | `[Lucky Starr 4] El gran sol de Mercurio [4623] (r1.3).epub` | *El gran sol de Mercurio* | *Lucky Starr and the Big Sun of Mercury* | 1956 | Miguel Giménez Sales | 16 | 40.200 | Dedicatoria a Robyn Joan; Introducción (1970) |
| L5 | `[Lucky Starr 5] Las lunas de Jupiter [4692] (r1.4).epub` | *Las lunas de Júpiter* | *Lucky Starr and the Moons of Jupiter* | 1957 | María Teresa Segur | 16 | 40.400 | Notas del traductor |
| L6 | `[Lucky Starr 6] Los anillos de Saturno [4793] (r1.3).epub` | *Los anillos de Saturno* | *Lucky Starr and the Rings of Saturn* | 1958 | Baldomero Porta Gou | 16 | 42.600 | — |

**Total:** unas **251.000 palabras**, 96 capítulos. **Estado de lectura: los seis libros fueron leídos completos**, capítulo por capítulo, incluidas introducciones, dedicatorias y notas.

**Verificación técnica:** cada EPUB se descomprimió y su contenido se convirtió a texto respetando el orden de lectura del EPUB (el «spine»). Todos tienen sus 16 capítulos completos e íntegros. **Ninguno tiene numeración de páginas**, por lo que todas las referencias son de tipo **libro + capítulo**. Los títulos y metadatos (año, traductor) salen de los propios EPUB (edición digital Titivillus).

## Método

1. Extracción del texto (`herramientas/extraer_texto.sh`).
2. Lectura completa con notas capítulo por capítulo.
3. Búsquedas y recuentos en el texto (por ejemplo, menciones de «Sirio» y «robot» por libro).
4. **Verificación automática de todas las citas** entre “…” de los documentos (`herramientas/verificar_atlas.py`): cada una aparece literalmente en el libro indicado. Resultado final: **0 citas fallidas**.
5. Etiquetas de evidencia: **[EXPLÍCITO]** · **[INFERENCIA FUERTE]** · **[HIPÓTESIS]** · **[AMBIGUO]** · **[CONTRADICCIÓN]** · **[NO DETERMINABLE]**; y **[EXTERNO]** para datos que no salen de los EPUB.
6. Convención tipográfica: “…” = cita literal verificada; «…» = término, apodo o paráfrasis.

---

## Conclusiones principales

### 1. La saga en una frase
Seis **novelas policiales disfrazadas de aventura espacial juvenil**: en cada libro, Lucky Starr, agente del Consejo de Ciencias, resuelve un crimen o sabotaje en un mundo distinto del Sistema Solar, acompañado por Bigman, y lo cierra con una «reunión de sospechosos» al estilo clásico.

### 2. Sobre la relación «protagonista–robot» (Fase 2): corrección de la premisa
- **No hay robot compañero.** El compañero es **John Bigman Jones**, un humano nacido en Marte [EXPLÍCITO].
- Los robots (RL-726, Mutt, los robots sirios) aparecen recién en L4–L6 y **siempre del lado del problema**: como arma robada, como espía o como guardianes del enemigo [EXPLÍCITO].
- La **relación Lucky–Bigman** es el corazón emocional de la saga: un pacto («Juntos, pues, adondequiera que vayamos», L1 c16) que atraviesa lealtad, sobreprotección, secretos y reconciliación; ver `MATRIZ…` §1a. Bigman crece de guardaespaldas a detective (L4) y a agente que decide sacrificarse (L6).

### 3. Personajes (Fase 3)
Elenco fijo mínimo: Lucky, Bigman, Conway y Henree. Cada libro tiene su propio elenco cerrado de sospechosos (de 5 a 10 personajes). Los culpables casi nunca son quienes parecen: Benson y no Hennes (L1), Hansen y no Antón (L2), Turner y no Morris ni Evans (L3), Peverale y Cook y no Urteil, Mindes ni el robot (L4), el perro y no un humano (L5).

### 4. Extraterrestres (Fase 4)
Marcianos de energía (L1), V-ranas y fauna de Venus (L3, L5), «cuerdas» de Mercurio (L4). La otredad **migra** de los alienígenas a **otros humanos**: los sirianos son descendientes de terrícolas [EXPLÍCITO]. Las V-ranas, que parecían amos malvados, resultan instrumentos de un humano (L3).

### 5. Humor (Fase 5)
El humor circula por Bigman: estatura, insultos cariñosos, travesuras, y el gag final del genio distraído (L6 c16). Sirve para expresar el afecto que Lucky no verbaliza. Ver `BIBLIA…` §5.

### 6. Antagonistas (Fase 6)
- **Sirio es el antagonista recurrente de fondo desde L2** (confianza **alta**): menciones por libro 0 · 32 · 4 · 107 · 50 · 229.
- **No es el cerebro de todos los crímenes**: L1 no tiene relación con Sirio; en L3 y L4 Sirio es una pista falsa explícitamente descartada (“No hay sirianos en Mercurio. Nunca los ha habido.” (L4 c15)), y el texto critica la paranoia antisiriana.
- Hay un **segundo antagonismo, interno**: los controles políticos sobre el Consejo (Swenson, el almirante, Finney), que Lucky considera legítimos (L4 c16).

### 7. Geopolítica (Fase 7)
Federación democrática del Sistema Solar (con nombres cambiantes), un Consejo de Ciencias que pasó de asesor a agencia de inteligencia, dependencia alimentaria de la Tierra y tensiones de autonomía (Venus, asteroides). Afuera, Sirio: autocracia eugenésica basada en robots. El arco termina en un **principio jurídico**: “la indivisibilidad de los sistemas estelares” (L6 c16). Ver `BIBLIA…` §2.

### 8. Espacio (Fase 8): ¿todo ocurre en el Sistema Solar?
**Sí.** Toda la acción en escena transcurre entre la corona solar y Saturno. Lo extrasolar (Sirio, Elam, Warren, unos cincuenta mundos más) sólo se menciona [EXPLÍCITO]. La serie recorre el Sistema Solar como un catálogo: Marte → asteroides → Venus → Mercurio → Júpiter → Saturno.

### 9. Continuidad (Fase 9)
Continuidad buena en lo esencial (personajes, pacto, Sirio, Consejo) y descuidos en datos: primer hombre en Marte (Wingrad vs Ching), estatura de Bigman, población galáctica (trillones vs menos que el Sistema Solar), fecha del presente (5.000 años después de la bomba atómica vs 1.000 después de la primera nave espacial), edad de Lucky. Detalle en `PREGUNTAS_ABIERTAS_Y_CONTRADICCIONES.md`.

### 10. Evolución de la saga (lectura de conjunto)
[INFERENCIA FUERTE] De L1 a L6 la serie se desplaza:
- de la **fantasía científica** (marcianos de energía, escudo mágico) a la **ciencia plausible** (Agrav, hiperóptica, Tres Leyes) y al **derecho interestelar**;
- del **crimen local** (venenos, piratas) al **conflicto entre Estados** (Sirio);
- de un héroe con **superpoderes prestados** (L1–L2) a un héroe que gana **sólo con la razón** (L3–L6);
- de un Bigman cómico a un Bigman **moralmente central** (L6).

---

## Límites de este análisis
- Se trabajó **sólo con las traducciones al español** del repositorio; algunas contradicciones pueden venir de la traducción y no del original (se indican en cada caso).
- Los datos marcados **[EXTERNO]** (seudónimo Paul French, número total de libros de la saga) no salen de los EPUB.
- Recuentos de palabras: aproximados, sobre el texto extraído.
