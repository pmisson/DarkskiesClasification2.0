import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import shutil

# Ruta del modelo guardado y el archivo CSV existente
model_path = "inceptionV3_finetuned_darkskies.h5"
csv_file_path = "classification_results.csv"
temp_dir = "temp_images"

# Cargar el modelo entrenado
model = tf.keras.models.load_model(model_path)

# Crear la carpeta temporal si no existe
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Función para descargar una imagen desde una URL
def download_image(nasa_id):
    mission = nasa_id.split('-')[0]
    url = f"https://eol.jsc.nasa.gov/DatabaseImages/ESC/small/{mission}/{nasa_id}.JPG"
    img_path = os.path.join(temp_dir, f"{nasa_id}.JPG")
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"No se pudo descargar {nasa_id}")
    except Exception as e:
        print(f"Error al descargar {nasa_id}: {e}")

    return img_path

# Función para preprocesar una imagen para la clasificación
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión para el batch
    img_array /= 255.0  # Normalizar como se hizo en el entrenamiento
    return img_array

# Función para realizar la clasificación
def classify_image(nasa_id, img_path):
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    
    # Almacenar los resultados en un diccionario con una clave para cada clase
    result = {"file_name": nasa_id, "predicted_class": class_names[predicted_class]}
    for i, class_name in enumerate(class_names):
        result[class_name] = prediction[0][i]
    
    return result

# Leer la lista de IDs desde el archivo CSV
def read_ids_from_csv(csv_input_path):
    df = pd.read_csv(csv_input_path)
    return df['nasa_id'].tolist()

# Leer el archivo de entrada con los IDs de NASA
input_csv = "nasa_ids.csv"  # El CSV debe tener una columna llamada 'nasa_id'
nasa_ids = read_ids_from_csv(input_csv)

# Descargar las imágenes en paralelo
with ThreadPoolExecutor(max_workers=8) as executor:
    list(tqdm(executor.map(download_image, nasa_ids), total=len(nasa_ids), desc="Descargando imágenes"))

# Definir las clases manualmente
class_indices = {
    'astronaut': 0,
    'aurora': 1,
    'black': 2,
    'city': 3,
    'none': 4,
    'stars': 5,
    'unknown': 6
}
class_names = [k for k, v in sorted(class_indices.items(), key=lambda item: item[1])]

# Clasificar las imágenes descargadas
results = []
for nasa_id in tqdm(nasa_ids, desc="Clasificando imágenes", unit="imagen"):
    img_path = os.path.join(temp_dir, f"{nasa_id}.JPG")
    if os.path.exists(img_path):
        result = classify_image(nasa_id, img_path)
        results.append(result)

# Actualizar el archivo CSV existente con los nuevos resultados
df_existing = pd.read_csv(csv_file_path) if os.path.exists(csv_file_path) else pd.DataFrame()
df_new = pd.DataFrame(results)

# Concatenar los datos existentes con los nuevos y ordenar
df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["file_name"], keep="last")
df_combined = df_combined.sort_values(by=["file_name"]).reset_index(drop=True)
df_combined.to_csv(csv_file_path, index=False)

# Borrar la carpeta temporal con las imágenes descargadas
shutil.rmtree(temp_dir)

print(f"Clasificación completada y guardada en {csv_file_path}")
