# 07 — AVISOS DE SISTEMA Y RELLENOS GENERALES (`SIS`)

Líneas sistémicas reutilizables en todos los capítulos. **Prioridad:** los avisos críticos (`SIS` crítico) cortan cualquier línea `VIA`/`RLL` al final de la frase en curso; los informativos esperan su turno (ver `00_DOCUMENTO_MAESTRO.md` §5.4).
Cada aviso lleva **la línea de *ERRANTE* (dato)** y una **reacción de GOLIAT** (variantes `a`/`b`/`c`, que se eligen al azar sin repetir). Antes de `F_GOLIAT_RECLUTADO` (capítulo 1, primer viaje) reacciona Lune (variantes `L`).

## 1. Avisos de navegación

| ID | Trigger | Personaje | Línea | Dirección |
|---|---|---|---|---|
| SIS_NAV_010 | Combustible < 25 % | ERRANTE | Combustible al veinticinco por ciento. | Informativo |
| SIS_NAV_011a | CONT | GOLIAT | Veinticinco por ciento. Es como un vaso medio lleno. Pero de un vaso pequeño. | Reacción |
| SIS_NAV_011b | CONT | GOLIAT | ¿Repostamos? Lo pregunto como pasajero preocupado y como robot que no sabe nadar en el vacío. | Reacción |
| SIS_NAV_011L | CONT | LUNE | Anotado. Habrá que repostar pronto. | Reacción (sin GOLIAT) |
| SIS_NAV_020 | Combustible < 10 % | ERRANTE | Combustible crítico. Se recomienda una estación de servicio. | Crítico |
| SIS_NAV_021a | CONT | GOLIAT | ¡Darío! ¡Si nos quedamos a la deriva, te juro que empiezo a cantar! | Reacción |
| SIS_NAV_021b | CONT | GOLIAT | Diez por ciento. Mis sensores de pánico están al noventa. | Reacción |
| SIS_NAV_030 | Colisión leve | ERRANTE | Impacto en el casco. Daño menor. | Informativo |
| SIS_NAV_031a | CONT | GOLIAT | ¡Eso fue una roca! ¡Las rocas me odian! ¡Es mutuo! | Reacción |
| SIS_NAV_031b | CONT | GOLIAT | Te lo digo con cariño: esa roca estaba quieta. | Reacción |
| SIS_NAV_031c | CONT | GOLIAT | Rayón nuevo. Lo voy a llamar «Darío». | Reacción |
| SIS_NAV_031L | CONT | LUNE | Por todas las órbitas… concéntrate. | Reacción (sin GOLIAT) |
| SIS_NAV_040 | Integridad del casco < 30 % | ERRANTE | Integridad del casco: crítica. | Crítico |
| SIS_NAV_041a | CONT | GOLIAT | Esta nave tiene más agujeros que mis excusas. ¡Busca un hangar! | Reacción |
| SIS_NAV_041b | CONT | GOLIAT | Si se abre una grieta, me tapo yo. Soy del tamaño justo. Es broma. No es broma. | Reacción |
| SIS_NAV_050 | Rumbo equivocado > 10 s | ERRANTE | Desviación del rumbo planificado. | Informativo |
| SIS_NAV_051a | CONT | GOLIAT | Eh… el destino está para el otro lado. Por si era un desvío turístico. | Reacción |
| SIS_NAV_051b | CONT | GOLIAT | ¿Paseo panorámico? Me encantan. Pero Corvo cobra por hora. | Reacción |
| SIS_NAV_051L | CONT | LUNE | Hm. Me pasé el desvío. | Reacción (sin GOLIAT) |
| SIS_NAV_060 | Velocidad excesiva cerca de un objeto | ERRANTE | Velocidad de aproximación excesiva. | Crítico |
| SIS_NAV_061a | CONT | GOLIAT | ¡Freno! ¡Freno! ¡La palanca de la izquierda se llama FRENO! | Reacción |
| SIS_NAV_061b | CONT | GOLIAT | Si nos estrellamos, que diga mi lápida que yo avisé. | Reacción |
| SIS_NAV_070 | Entrada en órbita | ERRANTE | Órbita estable alcanzada. | Informativo |
| SIS_NAV_071a | CONT | GOLIAT | Orbitando. Mi actividad favorita después de quejarme. | Reacción |
| SIS_NAV_071b | CONT | GOLIAT | Desde aquí arriba todo parece tranquilo. Siempre parece tranquilo desde arriba. | Reacción |
| SIS_NAV_080 | Aterrizaje correcto | ERRANTE | Aterrizaje completado. | Informativo |
| SIS_NAV_081a | CONT | GOLIAT | Aterrizaje de nueve sobre diez. El punto que falta es por el susto del principio. | Reacción |
| SIS_NAV_081b | CONT | GOLIAT | ¡Tierra firme! O hielo firme. O roca firme. Algo firme, en cualquier caso. | Reacción |
| SIS_NAV_090 | Aterrizaje brusco | ERRANTE | Aterrizaje con impacto. Tren de aterrizaje dañado. | Informativo |
| SIS_NAV_091a | CONT | GOLIAT | Mis tornillos han cambiado de sitio. Todos. | Reacción |
| SIS_NAV_091b | CONT | GOLIAT | Bueno… técnicamente hemos aterrizado. | Reacción |
| SIS_NAV_100 | Nuevo destino marcado | ERRANTE | Destino fijado. Ruta calculada. | Informativo |
| SIS_NAV_101a | CONT | GOLIAT | Rumbo fijado. Allá vamos. Otra vez. Como siempre. | Reacción |
| SIS_NAV_101b | CONT | GOLIAT | Donde vaya la nave. | Reacción (sólo con `F_PACTO`) |
| SIS_NAV_110 | Partida guardada | ERRANTE | Registro de misión actualizado. | Informativo |
| SIS_NAV_111a | CONT | GOLIAT | Guardado en mi memoria EXCELENTE. Y en la de la nave, por si acaso. | Reacción |
| SIS_NAV_120 | Velo activado (con `F_VELO`) | ERRANTE | Velo activo. | Informativo |
| SIS_NAV_121a | CONT | GOLIAT | Modo fantasma. Buuuh. | Reacción |
| SIS_NAV_121b | CONT | GOLIAT | ¡El Espectro ha vuelto! ¡Que tiemblen los malos y los asteroides! | Reacción |
| SIS_NAV_130 | Agrav activado (con `F_AGRAV`) | ERRANTE | Propulsor Agrav activo. | Informativo |
| SIS_NAV_131a | CONT | GOLIAT | Sin peso. Me siento ligero como un pensamiento. Uno pequeño. | Reacción |

## 2. Relleno general de viaje (*pool* de reserva)
Se usa cuando el *pool* `R` del tramo se ha agotado. **Condición:** `F_GOLIAT_RECLUTADO`. Las líneas marcadas con un capítulo sólo se activan **a partir** de ese capítulo (hacen referencia a hechos ya vividos).

| ID | Trigger | Personaje | Línea | Dirección |
|---|---|---|---|---|
| SIS_RLL_010 | IDLE ≥15 s | GOLIAT | ¿Sabías que en treinta años de mina nunca vi una estrella? Ahora las veo todo el tiempo. No me acostumbro. | Relleno |
| SIS_RLL_020 | IDLE ≥15 s | GOLIAT | Si la *Errante* hablara de verdad, ¿crees que me caería bien? Yo creo que no. Es demasiado formal. | Relleno |
| SIS_RLL_030 | IDLE ≥15 s | LUNE | ¿Estás contando rocas otra vez? | Relleno |
| SIS_RLL_031 | CONT | GOLIAT | Ochocientas doce. No me interrumpas. | Relleno |
| SIS_RLL_040 | IDLE ≥15 s | GOLIAT | Pregunta seria: ¿los inspectores se jubilan? ¿Y los robots de los inspectores? ¿Nos jubilamos juntos? | Relleno |
| SIS_RLL_050 | IDLE ≥15 s | GOLIAT | Me he cambiado las botas. Magnéticas, color azul cobalto. Nadie lo ha notado. Nadie nota nunca nada. | Relleno; guiño a las botas |
| SIS_RLL_060 | IDLE ≥15 s · desde C2 | GOLIAT | A veces pienso en Tobías Rue y su hija piloto. Ojalá le vaya bien. | Relleno |
| SIS_RLL_070 | IDLE ≥15 s · desde C3 | GOLIAT | Todavía me tiemblan las juntas cuando veo una ondina. De amor. Y de miedo. | Relleno |
| SIS_RLL_080 | IDLE ≥15 s · desde C3 | LUNE | Marco me escribió. Dice que ya no ronca. Miente. | Relleno |
| SIS_RLL_090 | IDLE ≥15 s · desde C4 | GOLIAT | A veces pienso en Centinela. En que nadie le puso nombre. | Relleno; tono serio |
| SIS_RLL_100 | IDLE ≥15 s · desde C4 | GOLIAT | ¿Te acuerdas de mi juicio en Mercurio? «Señoras, señores y doctor Garde». Inolvidable. | Relleno |
| SIS_RLL_110 | IDLE ≥15 s · desde C5 | GOLIAT | ¿Le habrán conseguido ya el perro a Nordin? Un perro de verdad, con pulgas. | Relleno |
| SIS_RLL_120 | IDLE ≥15 s · desde C5 | GOLIAT | Brann me apartó para que pudiera ver por la ventana. Fue la primera vez que un humano grande se hizo pequeño por mí. | Relleno, emotivo |
| SIS_RLL_130 | IDLE ≥15 s | LUNE | GOLIAT, ¿por qué te pusiste ese nombre? | Relleno |
| SIS_RLL_131 | CONT | GOLIAT | Porque los demás robots de la mina se llamaban por número. Y yo quería un nombre que se oyera desde lejos. | Relleno |
| SIS_RLL_140 | IDLE ≥15 s | GOLIAT | Si algún día me desguazan, quiero que mi altavoz vaya a un faro. Para seguir hablando. | Relleno, agridulce |

## 3. Monólogo de Lune sin GOLIAT (*pool* de reserva)
Se usa en el capítulo 1 antes de `F_GOLIAT_RECLUTADO` y en los tramos en que GOLIAT no está (C4_VIA02 si se agota su *pool*).

| ID | Trigger | Personaje | Línea | Dirección |
|---|---|---|---|---|
| SIS_LUN_010 | IDLE ≥15 s | LUNE | (para sí) El silencio del espacio. Me gustaba más antes. | Relleno |
| SIS_LUN_020 | IDLE ≥15 s | LUNE | (para sí) Revisa los hechos. Otra vez. Lo que se repite es la pista. | Relleno |
| SIS_LUN_030 | IDLE ≥15 s | LUNE | (para sí) Helena estará despierta. Siempre está despierta cuando estoy de viaje. | Relleno |
| SIS_LUN_040 | IDLE ≥15 s | LUNE | (para sí) *Errante*, ¿algún comentario? | Relleno |
| SIS_LUN_041 | CONT | ERRANTE | Ninguno registrado. | Relleno |
| SIS_LUN_050 | IDLE ≥15 s | LUNE | (para sí) Mi padre decía que pilotar es escuchar a la nave. La mía no dice nada. | Relleno |
