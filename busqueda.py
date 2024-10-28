import requests
import math
import csv
import argparse

BASE_URL = 'https://eol.jsc.nasa.gov/SearchPhotos/PhotosDatabaseAPI/PhotosDatabaseAPI.pl'

def load_api_key(file_path='api_key.key'):
    """Carga la API key desde un archivo."""
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f'Error: No se encontró el archivo {file_path}')
        exit(1)

def angular_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia angular en grados entre dos puntos especificados por latitud y longitud."""
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat_rad = lat2_rad - lat1_rad
    delta_lon_rad = math.radians(lon2 - lon1)
    # Fórmula de Haversine
    a = math.sin(delta_lat_rad/2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(delta_lon_rad/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # c es la distancia angular en radianes
    # Convertir a grados
    angular_distance_deg = math.degrees(c)
    return angular_distance_deg

def query_api(table, mission, api_key):
    if table == 'frames':
        query = '|'.join([
            f'{table}|mission|eq|{mission}',
            f'{table}|elev|lt|0',
            f'{table}|lat|ge|10',
            f'{table}|lat|le|70',
            f'{table}|lon|ge|-33',
            f'{table}|lon|le|27',
            f'{table}|fclt|ge|50',
            f'{table}|fclt|le|85'
        ])
        return_fields = '|'.join([
            f'{table}|mission',
            f'{table}|roll',
            f'{table}|frame',
            f'{table}|lat',
            f'{table}|lon',
            f'{table}|elev',
            f'{table}|fclt'
        ])
    elif table == 'nadir':
        query = '|'.join([
            f'{table}|mission|eq|{mission}',
            f'{table}|elev|lt|0',
            f'{table}|lat|ge|10',
            f'{table}|lat|le|70',
            f'{table}|lon|ge|-33',
            f'{table}|lon|le|27',
            f'camera|fclt|ge|50',
            f'camera|fclt|le|85'
        ])
        return_fields = '|'.join([
            f'{table}|mission',
            f'{table}|roll',
            f'{table}|frame',
            f'{table}|lat',
            f'{table}|lon',
            f'{table}|elev',
            f'camera|fclt'
        ])
    else:
        raise ValueError('La tabla debe ser "frames" o "nadir"')
    
    params = {
        'query': query,
        'return': return_fields,
        'key': api_key
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f'Error al consultar la tabla {table}: HTTP {response.status_code}')
        return []
    try:
        data = response.json()
    except ValueError:
        print(f'Error al decodificar JSON de la respuesta de la tabla {table}')
        return []
    return data

def main():
    # Cargar la API key desde el archivo externo
    api_key = load_api_key()

    # Configuración del argumento de línea de comando para la misión
    parser = argparse.ArgumentParser(description="Buscar imágenes de la NASA por misión.")
    parser.add_argument("mission", help="La misión ISS para buscar (por ejemplo, ISS060).")
    args = parser.parse_args()

    # Coordenadas de Madrid
    madrid_lat = 40.0
    madrid_lon = -3.0
    
    # Consultar la tabla frames
    print(f'Consultando la tabla frames para la misión {args.mission}...')
    data_frames = query_api('frames', args.mission, api_key)
    if not isinstance(data_frames, list):
        data_frames = []  # Asegurarse de que sea una lista vacía si no es del tipo correcto
    print(f'Número de registros de la tabla frames: {len(data_frames)}')
    
    # Consultar la tabla nadir
    print(f'Consultando la tabla nadir para la misión {args.mission}...')
    data_nadir = query_api('nadir', args.mission, api_key)
    if not isinstance(data_nadir, list):
        data_nadir = []  # Asegurarse de que sea una lista vacía si no es del tipo correcto
    print(f'Número de registros de la tabla nadir: {len(data_nadir)}')
    
    # Combinar resultados
    results = data_frames + data_nadir
    
    print(f'Número total de registros: {len(results)}')
    
    # Filtrar resultados basados en la distancia angular
    filtered_results = []
    for item in results:
        if 'frames.mission' in item:
            prefix = 'frames'
        elif 'nadir.mission' in item:
            prefix = 'nadir'
        else:
            continue
        
        try:
            mission = item[f'{prefix}.mission']
            roll = item[f'{prefix}.roll']
            frame = item[f'{prefix}.frame']
            lat = float(item[f'{prefix}.lat'])
            lon = float(item[f'{prefix}.lon'])
            elev = float(item[f'{prefix}.elev'])
            fclt = float(item.get(f'{prefix}.fclt') or item.get('camera.fclt'))
        except KeyError as e:
            print(f'Clave faltante {e} en el elemento: {item}')
            continue
        except TypeError:
            print(f'Error al convertir fclt a float en el elemento: {item}')
            continue
        
        dist = angular_distance(lat, lon, madrid_lat, madrid_lon)
        if dist <= 30.0:
            nasa_id = f"{mission}-{roll}-{frame}"
            filtered_results.append({
                'nasa_id': nasa_id,
                'lat': lat,
                'lon': lon,
                'elev': elev,
                'fclt': fclt,
                'distance_deg': dist
            })
    
    print(f'Se encontraron {len(filtered_results)} imágenes dentro de 30 grados de Madrid')
    # Guardar resultados en CSV con columna 'nasa_id'
    output_csv = f'nasa_ids.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['nasa_id', 'lat', 'lon', 'elev', 'fclt', 'distance_deg']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for res in filtered_results:
            writer.writerow(res)
            print(res['nasa_id'])
    
    print(f'Los resultados se han guardado en el archivo {output_csv}')

if __name__ == '__main__':
    main()



