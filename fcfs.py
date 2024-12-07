def fcfs_scheduling(processes):
    """
    Simulación del algoritmo de planificación FCFS (First-Come, First-Served).
    
    Args:
        processes: Lista de tuplas, donde cada tupla contiene el ID del proceso,
                   tiempo de llegada y tiempo de ráfaga (ID, tiempo_llegada, tiempo_rafaga).
                   
    Returns:
        result: Diccionario con detalles de cada proceso y métricas de planificación.
    """
    # Ordenar los procesos por tiempo de llegada
    processes.sort(key=lambda x: x[1])
    
    current_time = 0
    waiting_times = []
    turnaround_times = []
    completion_times = []
    
    print("\nOrden de ejecución (FCFS):")
    
    for process in processes:
        process_id, arrival_time, burst_time = process
        
        if current_time < arrival_time:
            current_time = arrival_time  # Si la CPU está inactiva, espera hasta que llegue el proceso
            
        start_time = current_time
        completion_time = start_time + burst_time
        turnaround_time = completion_time - arrival_time
        waiting_time = turnaround_time - burst_time
        
        current_time = completion_time  # Avanzar el tiempo actual
        
        # Guardar resultados
        waiting_times.append(waiting_time)
        turnaround_times.append(turnaround_time)
        completion_times.append(completion_time)
        
        print(f"Proceso {process_id}: Inicio = {start_time}, Final = {completion_time}")
    
    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
    
    result = {
        "Procesos": processes,
        "Tiempos de finalización": completion_times,
        "Tiempos de espera": waiting_times,
        "Tiempos de retorno": turnaround_times,
        "Promedio de espera": avg_waiting_time,
        "Promedio de retorno": avg_turnaround_time,
    }
    
    return result


# Ejemplo de entrada
procesos = [
    (1, 0, 4),  # (ID, tiempo_llegada, tiempo_rafaga)
    (2, 1, 3),
    (3, 2, 1),
    (4, 3, 2),
]

resultado = fcfs_scheduling(procesos)

# Mostrar resultados
print("\n--- Resultados ---")
print("Procesos: ", resultado["Procesos"])
print("Tiempos de finalización: ", resultado["Tiempos de finalización"])
print("Tiempos de espera: ", resultado["Tiempos de espera"])
print("Tiempos de retorno: ", resultado["Tiempos de retorno"])
print(f"Tiempo promedio de espera: {resultado['Promedio de espera']:.2f}")
print(f"Tiempo promedio de retorno: {resultado['Promedio de retorno']:.2f}")


"""
Orden de ejecución (FCFS):
Proceso 1: Inicio = 0, Final = 4
Proceso 2: Inicio = 4, Final = 7
Proceso 3: Inicio = 7, Final = 8
Proceso 4: Inicio = 8, Final = 10

--- Resultados ---
Procesos:  [(1, 0, 4), (2, 1, 3), (3, 2, 1), (4, 3, 2)]
Tiempos de finalización:  [4, 7, 8, 10]
Tiempos de espera:  [0, 3, 5, 5]
Tiempos de retorno:  [4, 6, 6, 7]
Tiempo promedio de espera: 3.25
Tiempo promedio de retorno: 5.75
"""