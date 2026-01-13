"""
Enunciado:
Este ejercicio introduce el uso de bibliotecas especializadas para acceder a APIs de forma
sencilla y estructurada. En concreto, utilizaremos la biblioteca pybikes que proporciona
wrappers para múltiples sistemas de bicicletas compartidas en todo el mundo.

En lugar de construir nuestro propio cliente HTTP y procesar manualmente los datos JSON,
aprenderemos a utilizar herramientas existentes que hacen este trabajo por nosotros.

Tareas:
1. Explorar los sistemas de bicicletas disponibles
2. Obtener información sobre el sistema de Barcelona (Bicing)
3. Analizar los datos de las estaciones

Esta práctica ilustra cómo las bibliotecas especializadas simplifican el acceso a APIs
y permiten concentrarse en el análisis de datos en lugar de en los detalles técnicos
de la comunicación con la API.
"""

import pybikes
import pandas as pd
import time
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import sys


def listar_sistemas_disponibles() -> List[str]:
    """
    Obtiene una lista de todos los sistemas de bicicletas disponibles en pybikes.

    Returns:
        List[str]: Lista de identificadores de sistemas disponibles
    """
    # Implementa aquí la lógica para obtener y devolver la lista
    # de sistemas disponibles en pybikes
    try:
        # Obtener todas las instancias de sistemas
        instances = list(pybikes.get_instances())
        # Extraer los tags (identificadores) de cada instancia
        tags = [instance[1]['tag'] for instance in instances]
        return tags
    except Exception:
        return []


def buscar_sistema_por_ciudad(ciudad: str) -> List[str]:
    """
    Busca sistemas de bicicletas que contengan el nombre de la ciudad especificada.

    Args:
        ciudad (str): Nombre de la ciudad a buscar

    Returns:
        List[str]: Lista de sistemas que coinciden con la búsqueda
    """
    # Implementa aquí la lógica para buscar y devolver sistemas
    # que coincidan con la ciudad especificada
    try:
        resultados = []
        ciudad_lower = ciudad.lower()
        
        # Obtener todas las instancias
        instances = list(pybikes.get_instances())
        
        # Iterar sobre todas las instancias
        for class_name, instance_info in instances:
            # Verificar si el nombre de la ciudad está en los metadatos
            meta = instance_info.get('meta', {})
            city = meta.get('city', '').lower()
            name = meta.get('name', '').lower()
            tag = instance_info.get('tag', '')
            
            # Buscar coincidencias en city o name
            if ciudad_lower in city or ciudad_lower in name:
                if tag and tag not in resultados:
                    resultados.append(tag)
        
        return resultados
    except Exception:
        return []


def obtener_info_sistema(tag: str) -> Dict[str, Any]:
    """
    Obtiene la información del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Dict[str, Any]: Metadatos del sistema o None si no existe
    """
    # Implementa aquí la lógica para obtener y devolver
    # los metadatos del sistema especificado
    try:
        # Obtener todas las instancias
        instances = list(pybikes.get_instances())
        
        # Buscar la instancia con el tag especificado
        for class_name, instance_info in instances:
            if instance_info.get('tag') == tag:
                meta = instance_info.get('meta', {})
                
                # Crear un diccionario con los metadatos relevantes
                result = {
                    'tag': tag,
                    'name': meta.get('name', ''),
                    'city': meta.get('city', ''),
                    'country': meta.get('country', '')
                }
                
                return result
        
        # Si no se encuentra, devolver None
        return None
    except Exception:
        return None


def obtener_estaciones(tag: str) -> Optional[List]:
    """
    Obtiene la lista de estaciones del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Optional[List]: Lista de objetos estación o None si hay error
    """
    # Implementa aquí la lógica para obtener y devolver
    # la lista de estaciones del sistema especificado
    try:
        # Obtener el sistema de bicicletas
        bike_system = pybikes.get(tag)
        
        # Actualizar la información de las estaciones
        bike_system.update()
        
        # Devolver la lista de estaciones
        return bike_system.stations
    except Exception:
        return None


def crear_dataframe_estaciones(estaciones: List) -> pd.DataFrame:
    """
    Convierte la lista de estaciones en un DataFrame de pandas.

    Args:
        estaciones (List): Lista de objetos estación

    Returns:
        pd.DataFrame: DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para convertir la lista de estaciones
    # en un DataFrame de pandas con al menos las columnas:
    # nombre, latitud, longitud, bicicletas disponibles, espacios libres
    
    # Crear una lista de diccionarios con los datos de cada estación
    data = []
    for station in estaciones:
        data.append({
            'name': station.name,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'bikes': station.bikes,
            'free': station.free
        })
    
    # Convertir la lista a un DataFrame
    df = pd.DataFrame(data)
    return df


def visualizar_estaciones(df: pd.DataFrame) -> None:
    """
    Genera una visualización simple de la disponibilidad de bicicletas.

    Args:
        df (pd.DataFrame): DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para crear un gráfico de barras que muestre
    # las 10 estaciones con más bicicletas disponibles
    
    # Ordenar por número de bicicletas disponibles y tomar las 10 primeras
    top_10 = df.nlargest(10, 'bikes')
    
    # Crear el gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.barh(top_10['name'], top_10['bikes'])
    plt.xlabel('Bicicletas disponibles')
    plt.ylabel('Estación')
    plt.title('Top 10 estaciones con más bicicletas disponibles')
    plt.tight_layout()
    
    # Mostrar el gráfico
    plt.show()


if __name__ == "__main__":
    # Listar sistemas disponibles
    print("\nSistemas de bicicletas disponibles:")
    sistemas = listar_sistemas_disponibles()
    print(f"Total: {len(sistemas)} sistemas")
    print(f"Algunos ejemplos: {sistemas[:5]}")

    # Buscar sistemas en Barcelona
    print("\nBuscando sistemas en Barcelona:")
    sistemas_barcelona = buscar_sistema_por_ciudad("Barcelona")
    print(f"Encontrados: {len(sistemas_barcelona)}")
    for sistema in sistemas_barcelona:
        print(f"- {sistema}")

    # Si se encuentra el sistema de Barcelona (Bicing), obtener información
    if "bicing" in sistemas:
        print("\nInformación del sistema Bicing de Barcelona:")
        info = obtener_info_sistema("bicing")
        for key, value in info.items():
            print(f"{key}: {value}")

        # Obtener estaciones
        print("\nObteniendo estaciones...")
        estaciones = obtener_estaciones("bicing")
        if estaciones:
            print(f"Obtenidas {len(estaciones)} estaciones")

            # Convertir a DataFrame
            print("\nConvirtiendo a DataFrame...")
            df = crear_dataframe_estaciones(estaciones)
            print(df.head())

            # Estadísticas básicas
            print("\nEstadísticas de bicicletas disponibles:")
            print(df['bikes'].describe())

            # Visualización
            print("\nVisualizando estaciones con más bicicletas disponibles...")
            visualizar_estaciones(df)
        else:
            print("No se pudieron obtener las estaciones.")
    else:
        print("El sistema 'bicing' no está disponible en pybikes.")

