# Guion del videojuego *Lune & Goliat: Expedientes del Sistema Solar*

Guion narrativo y de diálogos para un juego de pilotaje espacial punto a punto con investigación: un detective, el inspector Darío Lune, y su compañero robot, GOLIAT. Es una adaptación libre basada en el análisis de la saga *Lucky Starr* (`../analisis/`), con personajes y diálogos originales.

**Empezar por:** [`00_DOCUMENTO_MAESTRO.md`](00_DOCUMENTO_MAESTRO.md) (premisa, personajes, especificación técnica del sistema de diálogos, convenciones e identificadores).

| Archivo | Contenido |
|---|---|
| [00_DOCUMENTO_MAESTRO.md](00_DOCUMENTO_MAESTRO.md) | Documento técnico y creativo maestro |
| [01_CAPITULO_1_COSECHA_NEGRA.md](01_CAPITULO_1_COSECHA_NEGRA.md) | Marte |
| [02_CAPITULO_2_EL_CINTURON.md](02_CAPITULO_2_EL_CINTURON.md) | Asteroides, corona solar, Ganímedes |
| [03_CAPITULO_3_MAREAS_DE_VENUS.md](03_CAPITULO_3_MAREAS_DE_VENUS.md) | Venus |
| [04_CAPITULO_4_SOMBRA_DEL_SOL.md](04_CAPITULO_4_SOMBRA_DEL_SOL.md) | Mercurio |
| [05_CAPITULO_5_LAS_LUNAS_DEL_GIGANTE.md](05_CAPITULO_5_LAS_LUNAS_DEL_GIGANTE.md) | Satélites de Júpiter |
| [06_CAPITULO_6_ANILLOS_DE_SATURNO.md](06_CAPITULO_6_ANILLOS_DE_SATURNO.md) | Saturno, Titán, Vesta (final) |
| [07_AVISOS_Y_RELLENOS_DE_SISTEMA.md](07_AVISOS_Y_RELLENOS_DE_SISTEMA.md) | Avisos de navegación y *pools* de relleno |
| [08_MAPA_DE_NAVEGACION.md](08_MAPA_DE_NAVEGACION.md) | Grafo de rutas y tabla de tramos |
| [ESTADISTICAS.md](ESTADISTICAS.md) | Volumen de texto y audio (generado) |
| [dialogos.csv](dialogos.csv) | Todas las líneas en formato tabla, para importar (generado) |

## Regenerar el CSV y las estadísticas
```bash
python3 guion_videojuego/herramientas/exportar_dialogos.py
```
El script valida que no haya identificadores duplicados ni filas mal formadas, y que cada viaje tenga hitos de ruta y un *pool* de relleno.
