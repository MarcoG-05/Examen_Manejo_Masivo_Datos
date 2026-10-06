

---

## Las 5 V 

| V | Relación con el sistema de sensores | Ejemplo concreto | ¿Dónde aparece? |
|---|---|---|---|
| Volumen:| Cantidad de datos que generan los sensores y que hay que almacenar y procesar y trabajar. | El CSV tiene 100,000 datitos. Con miles de sensores a una lectura por segundo, 5,000 sensores producirían 5,000 lectura, es decir, unas 432 millones de lecturas al día | El volumen actual es el CSV. El volumen masivo es de la ampliación a futuro. |
| Velocidad: | Ritmo en el que llegan los datos y rapidez con la que se deben trabajar. | Cada sensor reporta una vez por minuto. Pasar a una lectura por segundo multiplica por 60 la frecuencia, y una alerta útil debe salir practicamente al instante. | La frecuencia de 1 lectura/min está en el CSV. La llegada continua cada segundo es parte de la posible ampliación futura |
| Variedad: | Diferentes formatos y fuentes de datos. | Hoy solo hay filas de seis columnas. A futuro se pondrian mensajes JSON de sensores, fotografías de maquinas y texto. | El CSV tiene un solo formato ( el tabular). La variedad real es de la ampliación a futuro. |
| Veracidad| Confiabilidad y calidad de los datos. | El archivo no tiene nulos ni "id_registro" repetidos (0 y 0).| La revisión de calidad se hizo en el csv. Los fallos reales de sensores son de la ampliación futura. el archivo no los contiene. |
| Valor:| los datos son para la toma de deciciones, ese es su valor. | Detectar 6,954 lecturas > 85 °C  y ver que Planta 3 concentra más alertas nos permite comprender que es una zona donde se necesita prestar atención de manera mas frecuente. | Este valor se obtuvo del CSV.|

---

##  Tipos de datos y procesamiento tradicional

### Clasificación:

| Elemento | Tipo | Justificación |
|---|---|---|
| CSV de sensores | Estructurado| Filas y columnas fijas con tipos definidos como los enteros, fechas, textos, decimales. |
| Mensaje JSON de un sensor | Semiestructurado | Tiene etiquetas y jerarquía, pero el esquema es flexible por que cada mensaje puede traer campos distintos. |
| Fotografía de una máquina | No estructurado | son pixeles sin campos o esquemas. |
| Texto libre de un reporte de mantenimiento | No estructurado| Lenguaje natural sin formato. |

### ¿Por qué 100,000 registros no son automáticamente Big Data?

el volumen solo es una parte de el Big Data. si solo tienes una de las 5 v no es Big Data, ya que es algo manejable en un solo dispositivo con herramientas "convencionales"

### Limitaciones al aumentar la escala

- Memoria y almacenamiento: cargar todo el archivo en una sola máquina deja de ser viable, matas a un solo dispositivo :c.
- Tiempo de procesamiento: un script secuencial tardaría demasiado y el resultado llegaría tarde.
- Un solo punto de falla: si la máquina se cae, se pierde todo.
- Variedad: un CSV y pandas no sirven para fotos ni texto libre, hacen falta otras herramientas.
- Escalabilidad: harían falta almacenamiento y cómputo distribuidos.

---

## Batch y Streaming

### Tipo de procesamiento que realizamos

Fue procesamiento por lotes (batch). El programa lee un archivo completo que ya estaba guardado ( los 100,000 registros), lo procesa de una sola vez y entrega resultados al terminar. Los datos son finitos y no importa la inmediatez, estos resultados se obtienen después de que los datos ya fueron generados.

### Alerta pocos segundos después de una lectura > 85 °C

streaming  (procesamiento de flujo) es la mejor opción. Cada lectura se evalúa en cuanto llega, evento por evento, y si la temperatura es mayor a los 85°c se emite la alerta de inmediato. Un proceso batch revisaría el archivo hasta que se cerrara todo el lote, y la alerta llegaría en un momento donde ya seria inutil. Aquí el resultado se necesita en segundos.

### Resumen al terminar el día

Usaría batch. Se necesitan promedios, máximos y conteos del día completo, y esas cifras solo existen cuando el día terminó. No hay urgencias de algun tipo,solo mandar tu paquete de datos (en este caso el reporte)

### Relación con el tiempo en que se necesita el resultado

| Necesidad | Tiempo requerido | Enfoque |
|---|---|---|
| Alerta de sobretemperatura | Segundos | Streaming |
| Resumen diario | Horas (al cierre del día) | Batch |

---

## Lambda y Kappa

### Escenario A: Arquitectura Lambda

por que? el escenario pide dos rutas, una que recalcule el historial por lotes y otra que procese lo reciente rápidamente. Eso es lo que define a Lambda: una capa batch (resultados completos y precisos sobre el historial) y una capa de velocidad (resultados rápidos sobre lo reciente), unidas por la capa de servicio que combina ambas.

```
                    +------------------------+
                +-->| Capa batch             |--+
                |   | (recalcula historial)  |  |
+----------+    |   +------------------------+  |   +-------------------+   +------------+
| Sensores |----+                               +-->| Capa de servicio  |-->| Consultas  |
| (datos)  |    |   +------------------------+  |   | (une ambas vistas)|   | / alertas  |
+----------+    +-->| Capa de velocidad      |--+   +-------------------+   +------------+
                    | (datos recientes)      |
                    +------------------------+
```

### Escenario B: Arquitectura Kappa

por que? se pide una sola lógica de procesamiento de eventos y conservar las mediciones para reprocesarlas. Kappa trata todo como un flujo de eventos.
una sola ruta de código en streaming y un registro de eventos inmutable donde se conservan las mediciones. Si cambia la lógica, se vuelve a procesar el historial reproduciendo el log con el código nuevo. Es más simple de mantener que Lambda porque no hay dos bases de código.

```
+----------+    +---------------------------+    +----------------------+    +------------------+
| Sensores |--->| Registro de eventos (log) |--->| Procesamiento de     |--->| Resultados /     |
| (datos)  |    | conserva las mediciones   |    | flujo (una sola      |    | alertas          |
+----------+    +---------------------------+    | lógica)              |    +------------------+
                           ^                     +----------------------+
                           |                                |
                           +-- reprocesar el historial -----+
                               (reproducir el log con la lógica nueva)
```

---

## Analítica descriptiva, predictiva y prescriptiva

### Descriptiva:

1. Hubo 6,954 lecturas con temperatura mayor que 85 °C. Planta_3 tuvo más alertas (unas 1,777), seguida de Planta_1 (1,737), Planta_4 (1,732) y Planta_2 (1,708). La diferencia entre la primera y la última es de 69 alertas. Los promedios de temperatura por planta son casi iguales ( ntre 66.53 y 66.77 °C)
2. La temperatura máxima fue 104.99 °C y se repitió en 4 lecturas de 4 sensores distintos, el S023 y S030 (Planta_3) y S019 y S014 (Planta_2). esta analitica nos sirve como historial y es indispensable para comprender la situación que se analiza y los posibles futuros

### Predictiva:

 ¿qué sensores o máquinas tienen más probabilidad de mantener temperaturas > 85 °C durante varias lecturas seguidas en las próximas horas, y cuáles podrían fallar en los próximos días?

Datos adicionales necesarios:
- Historial de fallas y paros de cada máquina (la variable que se quiere predecir; el CSV no la tiene).
- La relación entre id_sensor y la máquina real, porque el CSV no dice qué máquina mide a cada sensor.
- Historial más largo (el CSV cubre unas 41 horas) para ver patrones por hora, día o temporada, entre mayor sea el historial se tiene mas materia prima para trabajar, de ahí surge la importancia de la analitica descriptiva
- Condiciones de operación: carga de trabajo, temperatura del ambiente, horas de uso y fecha del último mantenimiento.

### Prescriptiva:

Riesgo previsto: un modelo predictivo señala que una máquina de Planta_3 tiene gran probabilidad de sobrecalentarse en las próximas horas. 

una vez que se tiene la amenaza, hay que buscar como contrarestarla, se le realiza una inspección preventiva y si no se ven cambios se debe detener o disminuir su uso 

**Información que revisaría antes de decidir:**
- Si las alertas son constantes o picos aislados.
- Que el sensor esté bien calibrado y que no sea una lectura falsa.
- Historial del mantenimiento y fallas de la máquina.
- es mas costoso detener la maquina o asumir la falla?
- Disponibilidad de personal y refacciones.