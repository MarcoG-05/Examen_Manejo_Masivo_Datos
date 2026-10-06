Examen: Manejo Masivo de Datos

Este repositorio contiene la solución al examen práctico de Manejo Masivo de Datos. El proyecto consiste en un script de Python que procesa y analiza un conjunto de datos proveniente de sensores industriales, extrayendo métricas clave, identificando alertas de temperatura y generando visualizaciones.

Descripción del Proyecto

El script principal (analisis.py) utiliza la biblioteca pandas para leer el archivo sensores_industriales.csv y realiza las siguientes operaciones automáticas:

Conteo general: Calcula la cantidad total de registros y el número de sensores distintos.

Análisis por planta: Determina la temperatura promedio histórica de cada planta.

Detección de máximos: Encuentra la temperatura máxima registrada, indicando el sensor y la fecha exacta.

Filtro de alertas: Cuantifica las lecturas que superan el umbral de peligro (85 °C).

Identificación de riesgos: Detecta la planta con mayor cantidad de alertas, manejando posibles empates.

Exportación de datos: Guarda un nuevo archivo alertas.csv exclusivo con los registros en peligro.

Visualización: Genera una gráfica de barras (temp_promedio.png) con el promedio de temperatura por planta usando matplotlib.

Estructura del Repositorio

 Estructura del Repositorio

A continuación se detalla la organización de los archivos en el proyecto:

📁 data/

---📄 sensores_industriales.csv (Dataset original requerido)

📁 resultados/

---📄 alertas.csv (Dataset filtrado generado automáticamente)

---📄 temp_promedio.png (Gráfica de barras exportada)

📄 .gitignore (Archivos y carpetas ignoradas por Git, como el entorno virtual)

📄 analisis.py (Script principal de ejecución)

📄 informe.md (Documento con las respuestas de la Parte II del examen)

📄 requirements.txt (Lista de dependencias de Python)



Requisitos Previos

Para ejecutar este proyecto, necesitas tener instalado:

Python 3.8 o superior

Git

Instalación y Configuración

Sigue estos pasos para clonar el repositorio y configurar el entorno virtual en tu máquina local:

Clonar el repositorio:

git clone https://github.com/MarcoG-05/Examen_Manejo_Masivo_Datos.git
cd Examen_Manejo_Masivo_Datos


Crear el entorno virtual:

En Windows:

python -m venv .venv


En Linux/Mac:

python3 -m venv .venv


Activar el entorno virtual:

En Windows:

.\.venv\Scripts\activate


En Linux/Mac:

source .venv/bin/activate


Instalar las dependencias:

pip install -r requirements.txt


Ejecución

Una vez que el entorno virtual esté activado y las dependencias instaladas, simplemente ejecuta el script principal desde la raíz del proyecto:

python analisis.py


Al finalizar la ejecución, los resultados se imprimirán en la terminal y se generará automáticamente la carpeta resultados/ con el archivo CSV filtrado y la gráfica correspondiente.