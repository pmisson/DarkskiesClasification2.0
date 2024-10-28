# Clasificación de Imágenes de la ISS

Este proyecto proporciona un conjunto de herramientas para la búsqueda, descarga y clasificación de imágenes capturadas por la Estación Espacial Internacional (ISS). Utiliza datos de la API de la NASA para localizar imágenes específicas, las descarga y las procesa mediante técnicas de clasificación de imágenes basadas en aprendizaje profundo. Este software se basa en el feedback proporcionado por ChatGPT, Cities at Night y Nguyen Minh Hieu. 

Cities at Night Colaboration. (2016). Dark Skies Clasification of ISS images. [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7708316

Nguyen Minh Hieu. (2016). Transfer Learning for Classification of Nighttime Images. Zenodo. https://doi.org/10.5281/zenodo.1452011

ChatGPT. (2024). Respuesta generada por el modelo ChatGPT de OpenAI. Disponible en https://chat.openai.com/ 

## Características

1. **Búsqueda de Imágenes**: 
   - El script `busqueda.py` utiliza la API de la NASA para buscar imágenes de la ISS en función de ciertos criterios, como la misión, la latitud y la longitud, o la elevación. Los resultados se filtran en función de la distancia angular a un punto de interés (por ejemplo, Madrid).
   - Los resultados de la búsqueda se guardan en un archivo CSV llamado `nasa_ids.csv`, con detalles sobre las imágenes encontradas.

2. **Descarga y Clasificación de Imágenes**:
   - El script `clasifica2.py` descarga las imágenes basadas en el archivo `nasa_ids.csv` generado y las clasifica utilizando un modelo de aprendizaje profundo, como InceptionV3.
   - Las imágenes se preprocesan antes de la clasificación, y los resultados se almacenan en un archivo CSV con probabilidades asociadas a cada categoría.

3. **Automatización por Misión**:
   - Un script Bash automatiza el procesamiento de múltiples misiones, ejecutando `busqueda.py` y `clasifica2.py` para cada misión especificada.
   - También se incluye un script para concatenar los archivos CSV generados por diferentes misiones en un solo archivo unificado.

## Requisitos

- Python 3.6 o superior
- Bibliotecas de Python: `requests`, `math`, `csv`, `argparse`, `tensorflow`, `pandas`
- Clave de la API de la NASA almacenada en un archivo externo (`api_key.key`)

## Uso

1. **Buscar Imágenes por Misión**:
   ```bash
   python busqueda.py ISS049
   ```
   Esto buscará imágenes para la misión `ISS049` y guardará los resultados en `nasa_ids.csv`.

2. **Clasificar Imágenes**:
   ```bash
   python clasifica2.py nasa_ids.csv
   ```
   Clasificará las imágenes listadas en `nasa_ids.csv` y guardará los resultados.

3. **Automatizar el Proceso para Varias Misiones**:
   Ejecuta el script Bash para procesar múltiples misiones secuencialmente:
   ```bash
   ./procesar_misiones.sh
   ```
Trainaed model:https://drive.google.com/file/d/1wHxQt43cHLOWw0_zH-25S6KqnOV6cdu3/view?usp=sharing

## Scripts Principales

- `busqueda.py`: Busca imágenes en la base de datos de la NASA y las filtra por criterios específicos.
- `clasifica2.py`: Descarga y clasifica las imágenes en función de los resultados de la búsqueda.
- `procesar_misiones.sh`: Automáticamente ejecuta los scripts de búsqueda y clasificación para varias misiones.

## Contribución

Si deseas contribuir, por favor envía un pull request o abre un issue para reportar errores o sugerir mejoras.
# DarkskiesClasification2.0
