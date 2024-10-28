import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import pandas as pd
from tqdm import tqdm  # Biblioteca para mostrar el progreso

# Ruta del modelo guardado y la carpeta de imágenes
model_path = "inceptionV3_finetuned_darkskies.h5"
test_dir = "test_release"

# Cargar el modelo entrenado
model = tf.keras.models.load_model(model_path)

# Definir el preprocesamiento de imágenes
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión para el batch
    img_array /= 255.0  # Normalizar como se hizo en el entrenamiento
    return img_array

# Obtener la lista de archivos en la carpeta de test
image_files = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]

# Limitar a las primeras 100 imágenes (puedes ajustar este valor según sea necesario)
image_files = image_files[:]

# Definir las clases manualmente o extraerlas del generador de datos utilizado anteriormente
class_indices = {
    'astronaut': 0,
    'aurora': 1,
    'black': 2,
    'city': 3,
    'none': 4,
    'stars': 5,
    'unknown': 6
}
# Ordenar las clases por el índice
class_names = [k for k, v in sorted(class_indices.items(), key=lambda item: item[1])]

# Realizar la clasificación y almacenar los resultados
results = []

# Usar tqdm para mostrar el progreso
for img_file in tqdm(image_files, desc="Clasificando imágenes", unit="imagen"):
    img_path = os.path.join(test_dir, img_file)
    img_array = preprocess_image(img_path)
    
    # Realizar la predicción
    prediction = model.predict(img_array)
    
    # Obtener la clase con mayor probabilidad
    predicted_class = np.argmax(prediction, axis=1)[0]
    
    # Almacenar los resultados en un diccionario con una clave para cada clase
    result = {"file_name": img_file, "predicted_class": class_names[predicted_class]}
    for i, class_name in enumerate(class_names):
        result[class_name] = prediction[0][i]
    stess
    results.append(result)

# Guardar los resultados en un archivo CSV
df = pd.DataFrame(results)
df.to_csv("classification_results.csv", index=False)

print("Clasificación completada y guardada en classification_results.csv")

