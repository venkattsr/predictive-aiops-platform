import requests
import docker
import time

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'

client = docker.from_env()

CONTAINER_NAME = "test-app"

THRESHOLD = 0.9

def get_cpu_usage():

    response = requests.get(
        PROMETHEUS_URL,
        params={"query": query}
    )

    data = response.json()

    value = float(
        data['data']['result'][0]['value'][1]
    )

    return value

def restart_container():

    container = client.containers.get(CONTAINER_NAME)

    print(f"\nRestarting container: {CONTAINER_NAME}")

    container.restart()

    print("Container restarted successfully.\n")

print("Starting Real-Time Self-Healing Engine...\n")

while True:

    cpu = get_cpu_usage()

    print(f"Live CPU Usage: {cpu:.2f}%")

    if cpu > THRESHOLD:

        print("Real anomaly detected!")

        restart_container()

    time.sleep(5)
