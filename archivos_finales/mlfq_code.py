"""
 * Archivo: mlfq_code.cpp
 * Autor: geovanny.barbosa@correounivalle.edu.co
 * Fecha creacion: 2024-12-06
 * Fecha ultima modificacion: 2024-12-06
 * Licencia: GNU-GPL
 """

# Código para implementar el algoritmo MLFQ en Python

# Clases necesarias para simular el MLFQ
from collections import deque
import csv

# Clase para representar un Proceso
class Process:
    def __init__(self, label, burst_time, arrival_time, queue, priority): # funcion constructora
        self.label = label
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.priority = priority
        self.wait_time = 0
        self.completion_time = 0
        self.response_time = None
        self.turnaround_time = 0

# Función para leer los procesos desde el archivo de entrada
def read_input_file(filename):
    processes = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("#") or not line.strip(): # se descartan las lineas con comentarios y las lineas vacias
                continue
            label, bt, at, q, pr = line.strip().split(';')
            processes.append(Process(label, int(bt), int(at), int(q), int(pr)))
    return processes # processes contiene los datos  leidos del archivo de texto

# Función para escribir los resultados en el archivo de salida
def write_output_file(filename, processes, metrics):
    with open(filename, 'w') as file:
        file.write("# archivo: salida_1.txt\n")
        file.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
        for p in processes:
            file.write(f"{p.label};{p.burst_time};{p.arrival_time};{p.queue};{p.priority};"
                       f"{p.wait_time};{p.completion_time};{p.response_time};{p.turnaround_time}\n")
        file.write(f"WT={metrics['average_wt']:.2f}; "
                   f"CT={metrics['average_ct']:.2f}; "
                   f"RT={metrics['average_rt']:.2f}; "
                   f"TAT={metrics['average_tat']:.2f};\n")

# Función para ejecutar el algoritmo MLFQ
def mlfq_scheduler(processes, time_quantum):
    # Separar procesos por cola
    queues = {1: deque(), 2: deque(), 3: deque()} # se generan las tres colas 
    for process in processes:
        queues[process.queue].append(process) # configura las 

    time = 0 # acumulador de los tiempos del proceso
    completed = [] # lista de procesos completados
    response_times = {}
    
    while any(queues.values()):
        for priority in sorted(queues.keys()):
            queue = queues[priority]
            while queue:
                process = queue.popleft()

                if process.response_time is None:
                    process.response_time = max(0, time - process.arrival_time)
                
                execution_time = min(process.remaining_time, time_quantum[priority])
                process.remaining_time -= execution_time
                time += execution_time

                if process.remaining_time > 0:
                    queue.append(process)
                else:
                    process.completion_time = time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.wait_time = process.turnaround_time - process.burst_time
                    completed.append(process)

    # Calcular métricas
    total_wt = sum(p.wait_time for p in completed)
    total_ct = sum(p.completion_time for p in completed)
    total_rt = sum(p.response_time for p in completed)
    total_tat = sum(p.turnaround_time for p in completed)

    metrics = { # diccionario de informacion de las metricas
        "average_wt": total_wt / len(completed),
        "average_ct": total_ct / len(completed),
        "average_rt": total_rt / len(completed),
        "average_tat": total_tat / len(completed),
    }

    return completed, metrics

# Configuración de los tiempos por cola
time_quantum = {1: 3, 2: 5, 3: 8}

# Leer archivo de entrada
input_file = "archivos_finales\mlq003.txt"
processes = read_input_file(input_file)

# Ejecutar el algoritmo
completed_processes, metrics = mlfq_scheduler(processes, time_quantum)

# Escribir el resultado en archivo de salida
output_file = "archivos_finales\salida_generada_1.txt"
write_output_file(output_file, completed_processes, metrics)

output_file
