import json
import time
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
    
def cronometrar_tarea():
    """Va a medir el tiempo que va a pasar entre dos marcaciones de enter"""
    input("\n >>> Presiona ENTER para empezar a trabajar :)")
    inicio = time.time()
    
    input(">>> Trabajando... Presiona ENTER para detener el cronometro.")
    fin = time.time()
    
    segundos = fin - inicio
    horas = segundos / 3600 
    return horas

def obtener_energia_validada():
    """Con esto creamos un bucle que obliga al usuario a elegir una de las tres opciones"""
    opciones = ["alta","media","baja"]
    while True:
        entrada = input("¿Como está tu energía el dia de hoy(alta, media, baja): ").lower()
        if entrada in opciones:
            return entrada
        print(f"[!] '{entrada}' no es valido. Elige una de las 3 opciones.")
#-----------------------------------------------------------------------------------------------------------------------------



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
estado_animo = obtener_energia_validada()

# Aqui venimos a llamar a la funcion que acabamos de poner al inicio.

factor = calcular_factor_energia(estado_animo)

# Aqui llamamos ahora a la nueva funcion que definimos para medir el tiempo que llevamos haciendo alguna tarea en especifico
tiempo_real_dedicado = cronometrar_tarea()

# Los numeros de los factores ya estan definidos en las funciones anteriormente
tiempo_efectivo = tiempo_real_dedicado * factor

print(f"\n[RESULTADO]: Trabajaste {tiempo_real_dedicado: .2f} horas reales. ")
print(f" Debido a tu energia ({estado_animo}), esto equivale a {tiempo_efectivo: .2f} horas de progreso real.")


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
    print(f"Leyendo registro {i}: {registro['fecha']} | Energía: {registro['estado_animo']} | Horas: {registro['tiempo']:.2f}")
    total_horas += registro["tiempo"]

promedio = total_horas / conteo if conteo > 0 else 0

print("-" * 30) # Una línea decorativa
print(f"Sesiones registradas: {conteo}")
print(f"Total acumulado: {total_horas} horas")
print(f"Promedio: {promedio:.2f} horas/sesión")

#-----------------------------------------------------------------------------------------------------------------------------

# Nuevo modulo - Analizador de metas

meta_horas = 20
progreso = (total_horas / meta_horas) * 100

print(f"\n--- PROGRESO HACIA LA META (MEJOR QUE EL 80% DEL MUNDO EN ALGO) ---")
print(f"Meta: {meta_horas} horas de practica(estudio o trabajo).")
print(f"Llevas el {progreso:.2f}% de nuestro objetivo")

if progreso < 25:
    print("¡Buen inicio! Todo experto comenzo desde tu misma posicion.")
elif progreso < 75:
    print("¡Vamos por la mitad del camino! Hay que seguir así.")
else:
    print("Lo estamos logrando, estamos a nada de llegar a la meta ¡Sigue así!")