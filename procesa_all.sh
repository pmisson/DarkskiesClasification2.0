#!/bin/bash

# Bucle para procesar misiones de ISS045 a ISS059
for mission in {45..59}
do
    mission_name="ISS0${mission}"
    echo "Procesando misión $mission_name..."

    # Ejecutar el script de búsqueda
    python busqueda.py "$mission_name"

    # Ejecutar el script de descarga y clasificación
    python clasifica2.py "nasa_ids.csv"

    echo "Misión $mission_name procesada."
done

echo "Todas las misiones han sido procesadas."

