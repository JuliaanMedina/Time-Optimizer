import os
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_factor_energia(estado):
    if estado == "baja": return 0.5
    elif estado == "media": return 0.75
    else: return 1.0

def obtener_energia_validada():
    opciones = ["alta","media","baja"]
    while True:
        print("\n--- Seleccione nivel de energía ---")
        print("1. Alta")
        print("2. Media")
        print("3. Baja")
        print("\n0. Volver")
        
        opcion = input("\n>>> ")
        
        if opcion == "1": return "alta"
        if opcion == "2": return "media"
        if opcion == "3": return "baja"
        if opcion == "0": return "VOLVER"
        print(f"[!] '{opcion}' no es válida. Intente de nuevo.")

def cronometrar_tarea():
    input("\n >>> Presiona ENTER para empezar a trabajar :)")
    inicio = time.time()
        
    input(">>> Trabajando... Presiona ENTER para detener el cronometro.")
    fin = time.time()
     
    segundos = fin - inicio
    horas = segundos / 3600 
    return horas