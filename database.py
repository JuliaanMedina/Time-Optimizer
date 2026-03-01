import json

def cargar_datos(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(nombre_archivo, historial):
    with open(nombre_archivo, "w") as archivo:
        json.dump(historial, archivo, indent=4)
    print("\n[LOG]: Datos guardados correctamente en JSON.")

def limpiar_registros_vacios(historial, umbral=0.001):
    original = len(historial)
    historial_limpio = [reg for reg in historial if reg.get("tiempo", 0) > umbral]
    eliminados = original - len(historial_limpio)
        
    if eliminados > 0:
        print(f"\n[SISTEMA]: Se han limpiado {eliminados} registros de prueba.")
            
    return historial_limpio