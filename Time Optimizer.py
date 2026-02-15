import json
from datetime import datetime

# --- Herramientas --- (funciones)
def cargar_datos(nombre_archivo):
    """Esto nos va a cargar el historial de datos de la base de datos que hayamos puesto segun todos los registros, en caso de que no haya nada nos va a devolver una lista vacia."""
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(nombre_archivo, historial):
    """"Esto y la opcion anterior hacen exactamente lo mismo que un guardado en los juegos de toda la vida pero pues dentro de nuestro codigo"""
    with open(nombre_archivo, "w") as archivo:
        json.dump(historial, archivo, indent=4)
    print("\n[LOG]: Datos guardados correctamente en JSON.")
          
          
def calcular_factor_energia(estado):
    """Este ya lo que hace es indicarnos el multiplicador bajo el cual vamos a estar calculando la cantidad de tiempo "util" que realmente tenemos"""
    if estado == "baja":
        return 0.5
    elif estado == "media":
        return 0.75
    else:
        return 1.0
    
# Time optimizer --- Codigo base

print("--- Bienvenido al Time Optimizer ---")

    # Datos fijos que podemos ajustar luego con un input
horas_dias = 24
trabajo_bpo = 9
moto_transporte = 3
sueno_ideal = 7

    # Calculo bruto del tiempo libre
tiempo_obligatorio = trabajo_bpo + moto_transporte + sueno_ideal
tiempo_restante = horas_dias - tiempo_obligatorio

print(f"Tiempo libre para tus actividades diarias: {tiempo_restante} horas")

    # Aqui es donde entra el factor que cambia el proposito de la app
estado_animo = input("¿Cómo está tu energia hoy? (opciones: 'alta', 'media', 'baja'): ").lower()

# Aqui venimos a llamar a la funcion que acabamos de poner al inicio.

factor = calcular_factor_energia(estado_animo)
tiempo_efectivo = tiempo_restante * factor
print(f"Tu capacidad cognitiva es {estado_animo}. Tiempo efectivo:{tiempo_efectivo} horas")


#------------------------------------------------------------------------------------------------------------------------------------------------



# --- Nuevo modulo: Selector de tareas o actividades ---

print("\n--- ¿Qué te gustaría hacer el dia de hoy? ---" )

# Ahora vamos con lo siguiente a elegir una lista segun el estado de animo.

if estado_animo == "alta": 
    opciones = ["Trabajar codigo en VS code", "Laboratorio de AWS", "Estudiar un tema nuevo"]

elif estado_animo == "media":
    opciones = ["Revisar documentacion", "Hacer tareas de SENA", "Llamar a algun amigo"]

else:
    opciones = ["Dormir", "Ver algo, cualquier cosa", "Tiempo con Juanita"]

# Con esto vamos a ennumerar las opciones que tengamos, segun el estado de animo que hayamos indicado

for i, tarea in enumerate(opciones, 1):
    print(f"{i}. {tarea}")
    
# Ahora el usuario va a tener que elegir

try:
    seleccion = int(input("\nSelecciona una tarea: "))
    tarea_realizada = opciones[seleccion - 1] # Restamos 1 porque las listas empiezan en 0
    
except (ValueError, IndexError): 
    print("Selección no valida, se asignará Actividad general.")
    tarea_realizada = "Actividad general"
    
print(f" Has elegido: {tarea_realizada}")
    
# Consejo basado en mi situacion de Call center.

if datetime.now().hour >= 17:
    print("Recuerda que ya saliste, no hay ningun afán :D")

#------------------------------------------------------------------------------------------------------------------------------

    # --- FASE DE LECTURA Y ANÁLISIS ---
print("\n--- Generando Reporte de Productividad ---")


# --- Fase de guardado modular ---
archivo_db = "seguimiento_energia.json"
historial = cargar_datos(archivo_db)

# 2. Creamos el nuevo registro
datos_entrada = {
    "estado_animo": estado_animo,
    "tiempo": tiempo_efectivo,
    "fecha": datetime.now().strftime("%Y-%m-%d"),
    "hora": datetime.now().strftime("%H:%M:%S"),
}

# 3. Añadimos el nuevo registro a la lista que ya cargamos
historial.append(datos_entrada)
guardar_datos(archivo_db, historial)

# --- FASE DE REPORTE---
print("\n--- Generando Reporte de Productividad ---")
total_horas = 0
conteo = len(historial)

# El cambio está aquí adentro:
for i, registro in enumerate(historial, 1):
    # Esto te mostrará el proceso paso a paso
    print(f"Leyendo registro {i}: {registro['fecha']} | Energía: {registro['estado_animo']} | Horas: {registro['tiempo']}")
    total_horas += registro["tiempo"]

promedio = total_horas / conteo if conteo > 0 else 0

print("-" * 30) # Una línea decorativa
print(f"Sesiones registradas: {conteo}")
print(f"Total acumulado: {total_horas} horas")
print(f"Promedio: {promedio:.2f} horas/sesión")

