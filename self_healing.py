import docker
import random
import time

client = docker.from_env()

CONTAINER_NAME = "test-app"

def restart_container():
    container = client.containers.get(CONTAINER_NAME)

    print(f"\nRestarting container: {CONTAINER_NAME}")

    container.restart()

    print("Container restarted successfully.\n")

while True:

    simulated_cpu = random.randint(1, 100)

    print(f"CPU Usage: {simulated_cpu}%")

    if simulated_cpu > 70:
        print("Anomaly detected!")

        restart_container()

    time.sleep(5)
