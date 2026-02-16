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

def personalizar_actividades():
    
    """Permite al usuario borrar y añadir actividades segun su necesidad."""
    archivo_tareas = "config_tareas.json"
    
    #Con esto cargamos la base de datos con la tareas ya existentes o una base de datos para las actividades nueva vacia.
    tareas = cargar_datos(archivo_tareas)
    
    if not tareas:
        tareas = {"alta": [], "media": [], "baja": []}
    
    while True:
        #Con este while hacemos que no se salga del menu hasta que se le indique que lo haga.
        print("\n--- Configuracion personalizada de actividades ---")
        print("1. Continuar al Optimizer.")
        print("2. Ver actividades actuales.")
        print("3. Añadir nueva actividad.")
        print("4. Borrar una actividad.")
        print("5. Borrar todo y empezar de cero.")
    
        opcion = input("\nSelecciona una opcion: ")
    
        if opcion == "1":
            print("\n[>>>] Cargando configuracion y entrando al Optimizer...")
            break
            #Este break lo que hace es romper el bucle y continuar con el programa.
    
        elif opcion == "2":
            for categoria, lista in tareas.items():
                print(f"Energia: {categoria.upper()}: {lista}")
            
        elif opcion == "3":
            categoria = input("Que nivel de energia es necesario para realizar esta actividad? (alta/media/baja): ").lower()
            if categoria in tareas:
                nueva = input(f"Escribe la nueva actividad para {categoria}: ")
                tareas[categoria].append(nueva)
                guardar_datos(archivo_tareas, tareas)
                print(f"[LOG]: '{nueva}' añadida.")
            
        elif opcion == "4":
            categoria = input("¿De que categoria vamos a eliminar una actividad? (alta/media/baja):")
            if categoria in tareas and tareas [categoria]:
                for i, actividad in enumerate(tareas[categoria], 1):
                    print(f"{i}. {actividad}")
        
                try:
                    indice = int(input("\nIndicador de actividad a eliminar: ")) - 1
                    eliminada = tareas[categoria].pop(indice)
                    guardar_datos(archivo_tareas, tareas)
                    print(f"[LOG]: '{eliminada}.")
            
                except (ValueError, IndexError):
                    print("[!] Opcion no valida.")
            else:
                print(f"[!] Nada que borrar en {categoria}")
            
        elif opcion == "5":
            confirmar = input("¿Estás seguro de borrar todas las actividades? (si/no): ").lower()
            if confirmar == 'si':
                tareas = {"alta": [], "media": [], "baja": []}
                guardar_datos(archivo_tareas, tareas)
                print("[LOG]: Listas vaciadas.")
                
        else:
            print(f"\n[!] '{opcion}' no es una opcion valida. Por favor, elige de 1 a 5.")
            
    return tareas
    


# Time optimizer --- Codigo base

print("--- Bienvenido al Time Optimizer ---")



#--- 1. BIENVENIDA Y CALCULO INICIAL
horas_dias = 24
trabajo_bpo = 9
moto_transporte = 3
sueno_ideal = 7

# Calculo bruto del tiempo libre
tiempo_obligatorio = trabajo_bpo + moto_transporte + sueno_ideal
tiempo_restante = horas_dias - tiempo_obligatorio

print(f"Tiempo libre para tus actividades diarias: {tiempo_restante} horas")



#--- 2. VALIDACION DE ENERGIA
estado_animo = obtener_energia_validada()
# Aqui venimos a llamar a la funcion que acabamos de poner al inicio.
factor = calcular_factor_energia(estado_animo)



#--- 3. SELECTOR DE TAREAS

print("\n--- ¿Qué te gustaría hacer el dia de hoy? ---" )

#Selector de tareas dinamico

# Aqui usamos la funcion definida para el indice para gestionar las actividades.
while True:

    catalogo_personal = personalizar_actividades()
    #Este lo que hace es mostrarnos la lista de actividades que hay segun el nivel de energia que hayamos indicado.
    opciones = catalogo_personal.get(estado_animo, [])

    if not opciones:
        print(f"\n[!] No tienes actividades registradas para energia {estado_animo}.")
        print("Debes añadir al menos una actividad en esta categoria para continuar.")
        
    else:
        #En case de que si hayan opciones entonces salimos del bucle y mostramos el menu de seleccion para seleccionar la actividad.
        print(f"\n --- Tareas disponibles para energia {estado_animo} ---")


# Con esto vamos a ennumerar las opciones que tengamos, segun el estado de animo que hayamos indicado

        for i, tarea in enumerate(opciones, 1):
            print(f"{i}. {tarea}")
        break
    
    

# --- 4. SELECCION DE ACTIVIDAD

try:
    seleccion = int(input("\nSelecciona una tarea: "))
    tarea_realizada = opciones[seleccion - 1] # Restamos 1 porque las listas empiezan en 0
    
except (ValueError, IndexError): 
    print("Selección no valida, se asignará Actividad general.")
    tarea_realizada = "Actividad general"
    
print(f"\n >>> Has elegido: {tarea_realizada}")



# --- 5. MEDICION DEL TIEMPO

# Aqui llamamos ahora a la nueva funcion que definimos para medir el tiempo que llevamos haciendo alguna tarea en especifico
print(f"\nIniciando cronometro para: {tarea_realizada}")
tiempo_real_dedicado = cronometrar_tarea()

# Los numeros de los factores ya estan definidos en las funciones anteriormente
tiempo_efectivo = tiempo_real_dedicado * factor

print(f"\n[RESULTADO]: Trabajaste {tiempo_real_dedicado: .2f} horas reales. ")
print(f" Debido a tu energia ({estado_animo}), esto equivale a {tiempo_efectivo: .2f} horas de progreso real.")

# Consejo basado en mi situacion de Call center.
if datetime.now().hour >= 17:
    print("Recuerda que ya saliste, no hay ningun afán :D")



# --- 6. GUARDADO Y REPORTE
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



# --- 7. ANALIZADOR DE METAS

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
    