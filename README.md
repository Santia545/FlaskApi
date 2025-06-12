# Flask API - Mejor Ubicación para Reunión de Amigos

Esta API utiliza el servicio de OpenRouteService para calcular la mejor ubicación de reunión para un grupo de amigos, considerando varias ubicaciones candidatas y minimizando el tiempo total de viaje.

## Requisitos

- Python 3.8+
- Paquetes: `flask`, `flask_cors`, `requests`, `python-dotenv`
- Clave de API de [OpenRouteService](https://openrouteservice.org/)

## Instalación

1. Clona este repositorio.
2. Instala las dependencias:
   ```
   pip install flask flask_cors requests python-dotenv
   ```
3. Crea un archivo `.env` en la raíz del proyecto y agrega tu clave de ORS:
   ```
   ORS_API_KEY=tu_clave_aqui
   ```

## Uso

1. Ejecuta la API:
   ```
   python app.py
   ```
2. Envía una solicitud POST a `/api/best-location` con el siguiente formato JSON:
   ```json
   {
     "friends": [
       {"lat": 20.0, "lng": -103.0},
       {"lat": 20.5, "lng": -103.5}
     ],
     "candidates": [
       {"lat": 20.2, "lng": -103.2},
       {"lat": 20.3, "lng": -103.3}
     ]
   }
   ```
   Donde friends, es un arreglo de cordenadas de las ubicaciones de los participantes y candidates es un arreglo de coordenadas de las ubicaciones de los lugares de reunión
3. La respuesta incluirá la mejor ubicación candidata, el ranking de todas las ubicaciones y el grafo de distancias.

## Notas

- Asegúrate de no exceder los límites de uso de la API de OpenRouteService.
- Esta API está pensada para fines educativos y de demostración.

## Autor
César Covarrubias Rosales
- CETI - Estructuras de Datos y Algoritmia
