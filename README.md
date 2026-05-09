# Kubernetes-Native Predictive Self-Healing AIOps Platform and MLflow Experiment Tracking

An intelligent AIOps platform that performs:

- Real-time infrastructure monitoring
- Predictive anomaly forecasting
- Root cause analysis
- Kubernetes autonomous healing
- Telegram alerting
- MLflow experiment tracking
- Streamlit live dashboard visualization

## Technologies Used

- Python
- Prometheus
- Grafana
- Docker
- Kubernetes (Minikube)
- MLflow
- Streamlit
- Isolation Forest
- NumPy
- Telegram Bot API

---

## Features

### Predictive AI Monitoring
Forecasts infrastructure overload before failure occurs.

### Autonomous Kubernetes Healing
Automatically restarts unhealthy deployments.

### Telegram Incident Alerts
Sends real-time predictive and anomaly alerts.

### Root Cause Analysis
Analyzes CPU, memory, disk, and network anomalies.

### Real-Time Dashboard
Live monitoring dashboard built using Streamlit.


---

# MLflow Experiment Tracking

This platform integrates MLflow for real-time experiment tracking and infrastructure telemetry logging.

## Tracked Metrics

- CPU utilization
- Memory utilization
- Disk usage
- Network traffic
- Predicted CPU risk
- Anomaly detection events
- Kubernetes restart count

## MLflow Features Used

- Experiment tracking
- Metric logging
- Root cause artifact logging
- Predictive telemetry storage
- Infrastructure event monitoring

## Example MLflow Logs

- Predictive CPU forecasting
- Infrastructure anomaly scores
- Kubernetes self-healing activity
- Incident recovery tracking

## MLflow UI

Start MLflow UI locally:

```bash
mlflow ui
```

Open:

```text
http://127.0.0.1:5000
```
---

## Architecture

Prometheus → AI Engine → ML Prediction → Kubernetes Healing → Telegram Alerts → Dashboard

---

## Run Project

### Start Monitoring Stack

```bash
docker-compose up -d
```

### Start Kubernetes

```bash
minikube start --driver=docker
```

### Run AI Engine

```bash
python multi_metric_healing.py
```

### Run Dashboard

```bash
streamlit run dashboard.py
```

---

## Future Enhancements

- LSTM Failure Prediction
- Multi-node Kubernetes Monitoring
- Reinforcement Learning Recovery
- Slack Integration
- OpenTelemetry Support

---

## Author

Venkata Krishnan
