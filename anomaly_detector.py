import requests
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'

def get_cpu_usage():
    response = requests.get(PROMETHEUS_URL, params={"query": query})
    data = response.json()

    value = float(data['data']['result'][0]['value'][1])
    return value

cpu_data = []

print("Collecting CPU metrics...")

for i in range(30):
    cpu = get_cpu_usage()
    cpu_data.append(cpu)

    print(f"CPU Usage: {cpu:.2f}%")

    time.sleep(2)

df = pd.DataFrame(cpu_data, columns=['cpu'])

model = IsolationForest(contamination=0.1)

df['anomaly'] = model.fit_predict(df[['cpu']])

print("\nResults:")
print(df)
