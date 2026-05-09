import requests
import docker
import time
import pandas as pd
import mlflow

from datetime import datetime
from sklearn.ensemble import IsolationForest

# -----------------------------
# CONFIGURATION
# -----------------------------

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'

CONTAINER_NAME = "test-app"

WINDOW_SIZE = 10

SLEEP_INTERVAL = 5

# -----------------------------
# INITIALIZE
# -----------------------------

client = docker.from_env()

cpu_history = []

restart_count = 0

model = IsolationForest(
    contamination=0.15,
    random_state=42
)

# -----------------------------
# FUNCTIONS
# -----------------------------

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

    global restart_count

    container = client.containers.get(CONTAINER_NAME)

    print(f"\n[{datetime.now()}]")
    print(f"Restarting container: {CONTAINER_NAME}")

    container.restart()

    restart_count += 1

    print("Container restarted successfully.\n")


# -----------------------------
# START MLflow
# -----------------------------

mlflow.set_experiment("Self-Healing-AIOps")

with mlflow.start_run():

    print("\n===================================")
    print("INTELLIGENT SELF-HEALING ENGINE")
    print("===================================\n")

    while True:

        try:

            cpu = get_cpu_usage()

            timestamp = datetime.now()

            print(f"[{timestamp}] CPU Usage: {cpu:.2f}%")

            cpu_history.append(cpu)

            if len(cpu_history) >= WINDOW_SIZE:

                df = pd.DataFrame(
                    cpu_history,
                    columns=['cpu']
                )

                predictions = model.fit_predict(df[['cpu']])

                latest_prediction = predictions[-1]

                # -----------------------------
                # ANOMALY DETECTED
                # -----------------------------

                if latest_prediction == -1:

                    print("\nML Anomaly Detected!")

                    mlflow.log_metric(
                        "cpu_usage",
                        cpu
                    )

                    mlflow.log_metric(
                        "restart_count",
                        restart_count
                    )

                    mlflow.log_metric(
                        "anomaly_detected",
                        1
                    )

                    restart_container()

                # -----------------------------
                # NORMAL SYSTEM
                # -----------------------------

                else:

                    print("System Normal\n")

                    mlflow.log_metric(
                        "cpu_usage",
                        cpu
                    )

                    mlflow.log_metric(
                        "restart_count",
                        restart_count
                    )

                    mlflow.log_metric(
                        "anomaly_detected",
                        0
                    )

            time.sleep(SLEEP_INTERVAL)

        except KeyboardInterrupt:

            print("\nStopping Intelligent Engine...")

            break

        except Exception as e:

            print(f"\nError: {e}")

            time.sleep(5)
