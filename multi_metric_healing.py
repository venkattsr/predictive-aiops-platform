import requests
import time
import pandas as pd
import mlflow
import numpy as np
import subprocess

from datetime import datetime
from sklearn.ensemble import IsolationForest

from telegram_alert import send_telegram_alert

# --------------------------------
# CONFIGURATION
# --------------------------------

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

QUERIES = {
    "cpu":
    '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',

    "memory":
    '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',

    "disk":
    '(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100',

    "network":
    'rate(node_network_receive_bytes_total[1m])'
}

WINDOW_SIZE = 45

SLEEP_INTERVAL = 5

COOLDOWN = 30

PREDICTION_ALERT_COOLDOWN = 120

KUBERNETES_DEPLOYMENT = "aiops-app"

# --------------------------------
# INITIALIZE
# --------------------------------

history = []

cpu_trend_history = []

restart_count = 0

last_restart_time = 0

last_prediction_alert = 0

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

# --------------------------------
# ROOT CAUSE ANALYSIS
# --------------------------------

def analyze_root_cause(metrics):

    cpu = metrics['cpu']
    memory = metrics['memory']
    disk = metrics['disk']
    network = metrics['network']

    if cpu > 4.0 and memory < 40:
        return "High CPU workload detected"

    elif memory > 70:
        return "Possible memory pressure or memory leak"

    elif disk > 80:
        return "Disk space exhaustion risk"

    elif network > 100000:
        return "Unusual network traffic spike"

    elif cpu > 4.0 and memory > 70:
        return "Combined CPU and memory instability"

    else:
        return "General infrastructure anomaly"

# --------------------------------
# PREDICTIVE FORECAST ENGINE
# --------------------------------

def predict_future_risk(cpu_history):

    if len(cpu_history) < 5:
        return False, 0

    recent_values = cpu_history[-5:]

    trend = np.polyfit(
        range(len(recent_values)),
        recent_values,
        1
    )[0]

    predicted_next = recent_values[-1] + trend

    risk_detected = predicted_next > 5.0

    return risk_detected, predicted_next

# --------------------------------
# PROMETHEUS QUERY
# --------------------------------

def query_prometheus(query):

    response = requests.get(
        PROMETHEUS_URL,
        params={"query": query}
    )

    data = response.json()

    try:

        value = float(
            data['data']['result'][0]['value'][1]
        )

    except:

        value = 0.0

    return value

# --------------------------------
# COLLECT METRICS
# --------------------------------

def collect_metrics():

    metrics = {}

    for key, query in QUERIES.items():

        metrics[key] = query_prometheus(query)

    return metrics

# --------------------------------
# KUBERNETES SELF-HEALING
# --------------------------------

def restart_container():

    global restart_count
    global last_restart_time

    current_time = time.time()

    # -----------------------------
    # COOLDOWN PROTECTION
    # -----------------------------

    if current_time - last_restart_time < COOLDOWN:

        print("Cooldown active. Skipping restart.\n")

        return

    last_restart_time = current_time

    print(f"\n[{datetime.now()}]")
    print(
        f"Restarting Kubernetes deployment: {KUBERNETES_DEPLOYMENT}"
    )

    try:

        subprocess.run(
            [
                "kubectl",
                "rollout",
                "restart",
                f"deployment/{KUBERNETES_DEPLOYMENT}"
            ],
            check=True
        )

        restart_count += 1

        print(
            "Kubernetes deployment restarted successfully.\n"
        )

        send_telegram_alert(
            f"""
🚨 Kubernetes Self-Healing Triggered

Deployment: {KUBERNETES_DEPLOYMENT}

Restart Count: {restart_count}

AI successfully restarted Kubernetes deployment.
"""
        )

    except Exception as e:

        print(f"Kubernetes restart failed: {e}")

# --------------------------------
# START MLFLOW
# --------------------------------

mlflow.set_experiment(
    "Kubernetes-Predictive-AIOps"
)

with mlflow.start_run(
    run_name="Predictive-AIOps-Run"
):

    print("\n======================================")
    print("KUBERNETES PREDICTIVE AIOPS PLATFORM")
    print("======================================\n")

    while True:

        try:

            metrics = collect_metrics()

            timestamp = datetime.now()

            print(f"\n[{timestamp}]")

            for key, value in metrics.items():

                print(f"{key.upper()}: {value:.2f}")

            history.append(metrics)

            cpu_trend_history.append(metrics['cpu'])

            # --------------------------------
            # PREDICTIVE ANALYSIS
            # --------------------------------

            risk_detected, predicted_cpu = predict_future_risk(
                cpu_trend_history
            )

            if risk_detected:

                print("\nPredictive Risk Detected!")
                print(
                    f"Predicted CPU: {predicted_cpu:.2f}%"
                )

                mlflow.log_metric(
                    "predicted_cpu",
                    predicted_cpu
                )

                mlflow.flush_async_logging()

                current_alert_time = time.time()

                # -----------------------------
                # ALERT COOLDOWN
                # -----------------------------

                if (
                    current_alert_time
                    - last_prediction_alert
                    > PREDICTION_ALERT_COOLDOWN
                ):

                    send_telegram_alert(
                        f"""
⚠️ Predictive Infrastructure Risk

Predicted CPU: {predicted_cpu:.2f}%

Potential overload likely soon.
"""
                    )

                    last_prediction_alert = current_alert_time

            # --------------------------------
            # MACHINE LEARNING ANALYSIS
            # --------------------------------

            if len(history) >= WINDOW_SIZE:

                df = pd.DataFrame(history)

                predictions = model.fit_predict(df)

                latest_prediction = predictions[-1]

                # --------------------------------
                # ANOMALY DETECTED
                # --------------------------------

                if latest_prediction == -1:

                    print("\nML Anomaly Detected!")

                    root_cause = analyze_root_cause(metrics)

                    print(
                        f"Root Cause: {root_cause}"
                    )

                    # --------------------------------
                    # TELEGRAM ALERT
                    # --------------------------------

                    send_telegram_alert(
                        f"""
🚨 AIOps Alert

Root Cause: {root_cause}

CPU: {metrics['cpu']:.2f}
Memory: {metrics['memory']:.2f}
Disk: {metrics['disk']:.2f}
Network: {metrics['network']:.2f}

Kubernetes Healing Triggered
"""
                    )

                    # --------------------------------
                    # LOGGING
                    # --------------------------------

                    for key, value in metrics.items():

                        mlflow.log_metric(
                            key,
                            value
                        )

                        mlflow.flush_async_logging()

                    mlflow.log_metric(
                        "restart_count",
                        restart_count
                    )

                    mlflow.flush_async_logging()

                    mlflow.log_metric(
                        "anomaly_detected",
                        1
                    )

                    mlflow.flush_async_logging()

                    mlflow.log_text(
                        root_cause,
                        "root_cause.txt"
                    )

                    # --------------------------------
                    # SELF-HEALING
                    # --------------------------------

                    restart_container()

                # --------------------------------
                # NORMAL SYSTEM
                # --------------------------------

                else:

                    print("\nSystem Normal")

                    for key, value in metrics.items():

                        mlflow.log_metric(
                            key,
                            value
                        )

                        mlflow.flush_async_logging()

                    mlflow.log_metric(
                        "restart_count",
                        restart_count
                    )

                    mlflow.flush_async_logging()

                    mlflow.log_metric(
                        "anomaly_detected",
                        0
                    )

                    mlflow.flush_async_logging()

            time.sleep(SLEEP_INTERVAL)

        except KeyboardInterrupt:

            print(
                "\nStopping Kubernetes Predictive AIOps Platform..."
            )

            break

        except Exception as e:

            print(f"\nError: {e}")

            time.sleep(5)