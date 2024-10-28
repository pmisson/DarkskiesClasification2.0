import re
import argparse
import pandas as pd

def extract_ids_to_csv(input_file, output_csv):
    # Definir el patrón de búsqueda con regex
    pattern = r"ISS0\d{2}-E-\d+"

    # Leer el contenido del archivo de texto
    with open(input_file, 'r') as file:
        content = file.read()

    # Buscar todas las coincidencias en el texto
    matches = re.findall(pattern, content)

    # Crear un DataFrame con los resultados y asignar el nombre de la columna 'nasa_id'
    df = pd.DataFrame(matches, columns=['nasa_id'])

    # Guardar el DataFrame en un archivo CSV
    df.to_csv(output_csv, index=False)
    print(f"El archivo '{output_csv}' ha sido creado con los identificadores extraídos.")

if __name__ == "__main__":
    # Configuración de argparse para recibir argumentos desde la línea de comandos
    parser = argparse.ArgumentParser(description="Extrae cadenas con el formato ISS0XX-E-XXXXX de un archivo de texto y las guarda en un CSV.")
    parser.add_argument("input_file", help="Archivo de entrada (fichero de texto).")
    parser.add_argument("output_csv", help="Archivo CSV de salida con los identificadores extraídos.")

    # Parsear los argumentos
    args = parser.parse_args()

    # Llamar a la función para extraer los IDs y guardarlos en el CSV
    extract_ids_to_csv(args.input_file, args.output_csv)

