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
        entrada = input("¿Como está tu energía el dia de hoy(alta, media, baja): ").lower()
        if entrada in opciones:
            return entrada
        print(f"[!] '{entrada}' no es valido. Elige una de las 3 opciones.")

def cronometrar_tarea():
    input("\n >>> Presiona ENTER para empezar a trabajar :)")
    inicio = time.time()
        
    input(">>> Trabajando... Presiona ENTER para detener el cronometro.")
    fin = time.time()
     
    segundos = fin - inicio
    horas = segundos / 3600 
    return horas