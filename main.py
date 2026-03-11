from datetime import datetime
from database import cargar_datos, guardar_datos, limpiar_registros_vacios 
from utils import limpiar_pantalla, calcular_factor_energia, obtener_energia_validada, cronometrar_tarea

def mostrar_portada():
    """Despliega la interfaz gráfica de texto (TUI) inicial de la aplicación."""
    limpiar_pantalla()
    print("================================================================")
    print(r"""
  _______ _                 ____        _   _           _  
 |__   __(_)               / __ \      | | (_)         (_)  
    | |   _ _ __ ___   ___| |  | |_ __ | |_ _ _ __ ___  _ _______ _ __ 
    | |  | | '_ ` _ \ / _ \ |  | | '_ \| __| | '_ ` _ \| |_  / _ \ '__|
    | |  | | | | | | |  __/ |__| | |_) | |_| | | | | | | |/ /  __/ |   
    |_|  |_|_| |_| |_|\___|\____/| .__/ \__|_|_| |_| |_|_/___\___|_|   
                                 | |                                   
                                 |_|                                   
    """)
    print("================================================================")
    print("               v1.0 - Single User Local Edition               ")
    print("================================================================")
    print("\n   [OBJETIVO]: Cuantificar, medir y optimizar el tiempo libre.")
    print("   [SISTEMA]:  El call center es temporal, el código es eterno.")
    print("\n" + "-"*64)
    
    # Este input actúa como una barrera de contención. 
    # Congela la pantalla hasta que el usuario decida avanzar.
    input("\n              >>> Presiona ENTER para iniciar <<<")

def personalizar_actividades():
    
        
    """Permite al usuario borrar y añadir actividades segun su necesidad."""
    archivo_tareas = "config_tareas.json"
        
    #Con esto cargamos la base de datos con la tareas ya existentes o una base de datos para las actividades nueva vacia.
    tareas = cargar_datos(archivo_tareas)
        
    if not tareas:
        tareas = {"alta": [], "media": [], "baja": []}
        
    while True:
        limpiar_pantalla()
        #Con este while hacemos que no se salga del menu hasta que se le indique que lo haga.
        print("\n--- Configuracion personalizada de actividades ---")
        print("1. Continuar al Optimizer.")
        print("2. Ver actividades actuales.")
        print("3. Añadir nueva actividad.")
        print("4. Borrar una actividad.")
        print("5. Borrar todo y empezar de cero.")
        print("\n0. Volver.")

        opcion = input("\nSelecciona una opcion: ")
        
        if opcion == "1":
            return "CONTINUAR"
                
        if opcion == "0": 
            return "VOLVER"
        
        elif opcion == "2":
            limpiar_pantalla()
            print("\n--- Catálogo de actividades registradas --- ")
            for categoría, lista in tareas.items():
                print(f"\nENERGÍA {categoría.upper()}:")
                if lista:
                    print(f" > {', '.join(lista)}")
                else:
                    print(" > (Vacio)")
                    
            input("\n[<<<] Presiona ENTER para volver al menú...")
                
        elif opcion == "3":
            limpiar_pantalla()
            
            print("--- Añadir nueva actividad ---")
            print("\nPulse '0' para volver al lobby.")
            
            categoria = input("\nQue nivel de energia es necesario para realizar esta actividad? (alta/media/baja): ").lower()
            
            if categoria == "0":
                continue
            
            if categoria in tareas:
                limpiar_pantalla()
                print("\nPulse '0' para volver al atrás.")
                nueva = input(f"Escribe la nueva actividad para {categoria}: ")
                
                if nueva == "0":
                    continue
                
                #Actualización con la barra de progreso independiente
                try:
                    limpiar_pantalla()
                    print("\nPulse '0' para volver al atrás.")
                    meta_input = input(f"¿Cuál es tu meta en horas para dominar '{nueva}'?: ")
                    
                    if meta_input == "0":
                        continue
                    
                    meta_horas = float(meta_input)
                    
                except ValueError:
                    print("[!] Valor inválido. Se asignará una meta por defecto de 20 horas.")
                    meta_horas = 20.0
                    
                # Guardar la actividad en su categoría
                tareas[categoria].append(nueva)
                guardar_datos(archivo_tareas, tareas)
                
                # Guardar la meta independiente
                archivo_metas = "metas_actividades.json"
                metas = cargar_datos(archivo_metas)
                if not isinstance(metas, dict):
                    metas = {} #Con esto aseguramos que se abra un diccionario cuando el archivo sea nuevo
                    
                metas[nueva] = meta_horas
                guardar_datos(archivo_metas, metas)
                
                print(f"[LOG]: '{nueva}' guardada con exito.")
                input("Presiona ENTER para continuar...")
            else:
                print(f"\n[LOG]: La categoria '{categoria}' no existe.")
                input("Presiona ENTER para reintentar...")
                
        elif opcion == "4":
            
            limpiar_pantalla()
            print("\n" + "="*40)
            print("     --- Borrar actividad ---")
            print("="*40)
            print("\n[INFO]: Escribe '0' para volver atrás.")
            
            categoria = input("¿De que categoria vamos a eliminar una actividad? (alta/media/baja):")
            
            if categoria == "0":
                continue
            
            if categoria in tareas and tareas [categoria]:
                for i, actividad in enumerate(tareas[categoria], 1):
                    print(f"{i}. {actividad}")
            
                try:
                    seleccion = input("\nSeleccione la actividad a borrar o 0 para volver atrás: ").strip()
                    
                    if seleccion == "0":
                        continue
                    
                    indice = int(seleccion) - 1
                    if 0<= indice < len(tareas[categoria]):
                        eliminada = tareas[categoria].pop(indice)
                                        
                        #1. Guardar cambios en el catalogo principal
                        guardar_datos(archivo_tareas, tareas)
                    
                        #2. --- Nueva lógica: Purga de meta asociada ---
                        archivo_metas = "metas_actividades.json"
                        metas = cargar_datos(archivo_metas)
                    
                        if isinstance(metas, dict) and eliminada in metas:
                            del metas[eliminada]
                            guardar_datos(archivo_metas, metas)
                        
                        print(f"[LOG]: Actividad '{eliminada}' y su meta en horas han sido eliminadas del sistema.")
                    
                    else:
                        print("\n[!] Numero fuera de rango.")
                except ValueError:
                    print("\n[!] Entrada no valida. Debe ser un numero.")
                    
                input("\nPresiona ENTER para continuar...")
            
            else:
                print(f"\n[!] No hay actividades para borrar en '{categoria}'.")
                input("\nPresiona ENTER para volver...")            
                
        elif opcion == "5":
            
            limpiar_pantalla()
            
            print("\n" + "!"*45)
            print("  --- PROTOCOLO DE BORRADO TOTAL ---")
            print("!"*45)
            print("\n[ADVERTENCIA]: Esta acción eliminará:")
            print("1. Todas tus actividades personalizadas.")
            print("2. Todas las metas y progresos de horas.")
            print("\n[INFO]: Escribe '0' para cancelar y volver.")
            
            confirmar = input("¿Estás seguro de borrar absolutamente todo? Se perderán las actividades y sus metas (si/no): ").strip()
            
            if confirmar == "0":
                continue
            
            if confirmar == 'si':
                #1. Formateo de las habilidades.
                tareas = {"alta": [], "media": [], "baja": []}
                guardar_datos(archivo_tareas, tareas)
                
                #2. Formateo de barras de progreso.
                archivo_metas = "metas_actividades.json"
                metas_vacias = {}
                guardar_datos(archivo_metas, metas_vacias)
                
                print("[LOG]: Sistemas vaciados. Listas de actividades y metas han sido vaciadas")
            else:
                print("[LOG]: Operación abortada. Tus datos están guardados.")
                    
        else:
            print(f"\n[!] '{opcion}' no es una opcion valida. Por favor, elige de 1 a 5.")

def ejecutar_optimizer(estado_animo, factor):
    
    limpiar_pantalla()
    #Aqui cargamos las tareas para la sesión
    tareas = cargar_datos("config_tareas.json")
    opciones = tareas.get(estado_animo, [])
    
    if not opciones:
        print(f"\n [!] No hay tareas para energia {estado_animo}.")
        print("Debes añadir actividades en el Lobby para continuar.")
        input("\nPresion ENTER para volver al Lobby...")
        return "VOLVER" 
        
    print(f"\n --- Tareas disponibles para energia {estado_animo} ---")
    print("\n0. Volver")
    for i, tarea in enumerate(opciones, 1):
        print(f"{i}. {tarea}")
        
    try:
        entrada = input("\nSeleccione una tarea (o 0 para volver): ").strip()
        if entrada == "0":
            return "VOLVER"
        
        seleccion = int(entrada)
        tarea_realizada = opciones[seleccion - 1]
    
    except (ValueError, IndexError):
        print("\n[!] Selección no valida. Volviendo al lobby...")
        input("Presiona ENTER")
        return "VOLVER"
        
    # 3. El cronometro
    limpiar_pantalla()
    print(f"\nIniciando cronometro para: {tarea_realizada}")
    tiempo_real = cronometrar_tarea()
    tiempo_efectivo = tiempo_real * factor
    
    # 4. Reporte y metas
    print("\n--- Generando Reporte de Productividad ---")

    # --- Fase de guardado modular ---
    archivo_db = "seguimiento_energia.json"
    historial = cargar_datos(archivo_db)

    # Creamos el nuevo registro
    datos_entrada = {
        "tarea": tarea_realizada,
        "estado_animo": estado_animo,
        "tiempo": tiempo_efectivo,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        }

    # Añadimos el nuevo registro a la lista que ya cargamos
    historial.append(datos_entrada)
    historial = limpiar_registros_vacios(historial)
    guardar_datos(archivo_db, historial)

    #Filtrado de fecha
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # Con esto filtramos la base de datos y hacemos que muestre solo la actividad del dia de hoy
    sesiones_hoy = [reg for reg in historial if reg["fecha"] == fecha_hoy]

    # --- FASE DE REPORTE---
    limpiar_pantalla()
    print(f"\n" + "" * 10 + f"REPORTE DEL DIA: {fecha_hoy}")
    print("-" * 50)

    if sesiones_hoy:
        print(f"{'HORA':<10} | {'TAREA':<20} | {'EFICAZ':10}")
        print("-" * 50)
        for reg in sesiones_hoy:
            # Usamos reg.get() por si hay registros viejos sin la llave "tarea"
            tarea_now = reg.get("tarea", "General")
            print(f"{reg['hora']:<10} | {tarea_now[:20]:20} | {reg['tiempo']:.2f}h")
    else:
        print("No hay sesiones registradas el dia de hoy.")

            #Calculos totales (de todo el historial)
    total_historico = sum(reg["tiempo"] for reg in historial)
    total_hoy = sum(reg["tiempo"] for reg in sesiones_hoy)

    print("-" * 50) 
    print(f"RESUMEN:")
    print(f" > Tiempo efectivo hoy:  {total_hoy:.2f} horas")
    print(f" > Acumulado histórico:  {total_historico:.2f} horas")
    print("-" * 50)



            # --- 7. ANALIZADOR DE METAS

    archivo_metas = "metas_actividades.json"
    metas_por_actividad = cargar_datos(archivo_metas)
    if not isinstance(metas_por_actividad, dict):
        metas_por_actividad = {}
        
    #Obtener la meta que asigna 20h si es una tarea antigua sin meta registrada
    meta_especifica = metas_por_actividad.get(tarea_realizada, 20.0)
    
    #Calcular acumulado aislando estrictamente la tarea actual
    total_tarea_especifica = sum(reg.get("tiempo", 0) for reg in historial if reg.get("tarea") == tarea_realizada)
    
    progreso = (total_tarea_especifica / meta_especifica) * 100

    # Parametros de la barra
    longitud_barra = 25 
    bloques_llenos = int(progreso / (100 / longitud_barra))
    bloques_llenos = min(bloques_llenos, longitud_barra)

    # '█' para lo completado y '-' para lo que falta
    barra_visual = "█" * bloques_llenos + "-" * (longitud_barra - bloques_llenos)

    print("\n" + "="*50)
    print(f"--- PROGRESO EN: {tarea_realizada.upper()} ---")
    print(f"Meta: {meta_especifica}h | Acumulado: {total_tarea_especifica:.2f}h")
    print(f"Progreso: [{barra_visual}] {progreso:.2f}%")
    print("="*50)

    if progreso < 25:
        print("¡Buen inicio! Todo experto comenzo desde tu misma posicion.")
    elif progreso < 50:
        print("Agarrando ritmo. El call es temporal, el codigo es eterno.")
    elif progreso < 75:
        print("Casi dominado. Ya se está conviertiendo en habito.")
    elif progreso < 100:
        print("Estamos a nada. El 80% de las personas ya se rindieron tu no.")
    else:
        print("Meta alcanzada. Estas en el 20% de la poblacion mundial. Eres oficialmente mejor que todos ellos")

    input("\nCiclo finalizado. Presiona ENTER para volver al lobby.")                

def main():
    while True:    
        #1. Despliegue de la portada gráfica
        mostrar_portada()
        
        while True:
            #2. Bienvenida y datos iniciales
            limpiar_pantalla()



            #--- 1. BIENVENIDA Y CALCULO INICIAL
            horas_dias = 24
            trabajo_bpo = 9
            moto_transporte = 3
            sueno_ideal = 7

            # Calculo bruto del tiempo libre
            tiempo_obligatorio = trabajo_bpo + moto_transporte + sueno_ideal
            tiempo_restante = horas_dias - tiempo_obligatorio

            print(f"\nTiempo libre para tus actividades diarias: {tiempo_restante} horas")



            #--- 2. VALIDACION DE ENERGIA
            estado_animo = obtener_energia_validada()
            
            if estado_animo == "VOLVER":
            #Este break rompe el bucle y devuelve al while anterior
                break
            
            
            # Aqui venimos a llamar a la funcion que acabamos de poner al inicio.
            factor = calcular_factor_energia(estado_animo)
            
            while True:
                #Mostramos el lobby
                decision = personalizar_actividades()
                
                if decision == "VOLVER":
                   break
                
                if decision == "CONTINUAR":
                    resultado = ejecutar_optimizer(estado_animo, factor)    
                    
                    if resultado == "VOLVER":
                        continue
                    
if __name__ == "__main__":
    main()

