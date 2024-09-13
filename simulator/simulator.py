import requests
import random
import time
import statistics
import csv

# Ruta del archivo CSV dentro del contenedor
csv_file_path = '/app/data_SD.csv'

# Leer dominios desde el archivo CSV
def load_domains_from_csv(file_path):
    domains = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            domains.append(row[0])
    return domains

# Cargar dominios
domains = load_domains_from_csv(csv_file_path)

api_url = "http://api_container:5000/resolve"

response_times = []
hits = 0
misses = 0
partition_stats = {0: 0, 1: 0, 2: 0, 3: 0}

for _ in range(500):  
    domain = random.choice(domains)
    start_time = time.time()  # Inicia el temporizador
    response = requests.post(api_url, json={"domain": domain})
    end_time = time.time()  # Detiene el temporizador
    response_data = response.json()
    
    # Mide el tiempo de respuesta
    response_time = end_time - start_time
    response_times.append(response_time)

    # Actualizar los balances de carga
    partition = response_data["partition"]
    partition_stats[partition] += 1
    
    # Analiza la respuesta para determinar si es un hit o miss
    if response_data['source'] == 'cache':
        hits += 1
    else:
        misses += 1
    
    #print(f"Sent domain: {domain}, Response: {response.text}, Response Time: {response_time:.4f} seconds, Partition: {partition}")

# Calcula el promedio y la desviación estándar de los tiempos de respuesta
average_response_time = statistics.mean(response_times)
std_deviation_response_time = statistics.stdev(response_times)

# Calcula el Hit/Miss rate
total_requests = hits + misses
hit_rate = (hits / total_requests)
miss_rate = (misses / total_requests)

# Muestra los resultados
print(f"\nAverage Response Time: {average_response_time:.4f} seconds")
print(f"Standard Deviation of Response Time: {std_deviation_response_time:.4f} seconds")
print(f"Hit Rate: {hit_rate:.2f}")
print(f"Miss Rate: {miss_rate:.2f}")
print("Balances de carga:", partition_stats)