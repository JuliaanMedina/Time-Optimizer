    #V1.2 importamos datatime para manejar fechas automaticamente

import json
from datetime import datetime
    # Tenemos que llamar desde el sistema operativo la fecha e importarla al codigo

    # The time optimizer - Fase 1: El filtro de realidad
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

if estado_animo == 'baja':        
        # Si la energia es baja, el tiempo rinde la mitad que cuando estamos bien (factor 0.5)
        tiempo_efectivo = tiempo_restante * 0.5
        print(f"Alerta: Tu capacidad cognitiva está reducida. Tiempo efectivo disponible: {tiempo_efectivo} horas")
            
elif estado_animo == 'media':
        # Si la energia es media, el tiempo rinde un 75% (factor 0.75), podemos realizar actividades que no sean muy demandantes
        tiempo_efectivo = tiempo_restante * 0.75
        print(f"Atención: Tu capacidad cognitiva está moderada. Tiempo efectivo disponible: {tiempo_efectivo} horas")

else:
        # Si la energia es alta, el tiempo rinde al 100% (factor 1)
        tiempo_efectivo = tiempo_restante
        print(f"Excelente: Tu capacidad cognitiva está óptima. Tiempo efectivo disponible: {tiempo_efectivo} horas")
            
    # Ahora que tenemos la base de la energia, podemos empezar a organizar las actividades

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

    # 1. Cargar datos existentes (si el archivo no existe o está mal, empezamos con lista vacía)
try:
    with open("seguimiento_energia.json", "r") as archivo:
        historial = json.load(archivo)
except (FileNotFoundError, json.JSONDecodeError):
    historial = []

# 2. Creamos el nuevo registro
datos_entrada = {
    "estado_animo": estado_animo,
    "tiempo": tiempo_efectivo,
    "fecha": datetime.now().strftime("%Y-%m-%d"),
    "hora": datetime.now().strftime("%H:%M:%S"),
}

# 3. Añadimos el nuevo registro a la lista que ya cargamos
historial.append(datos_entrada)

# 4. Guardamos TODA la lista actualizada (usamos "w" para sobrescribir con la lista legal)
with open("seguimiento_energia.json", "w") as archivo:
    json.dump(historial, archivo, indent=4)

print("\n[LOG]: Datos guardados correctamente en JSON.")

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

