import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(
    page_title="AIOps Dashboard",
    layout="wide"
)

st.title("🚀 Kubernetes Predictive AIOps Platform")

cpu_chart = st.line_chart()

memory_chart = st.line_chart()

status = st.empty()

restart_metric = st.empty()

restart_count = 0

while True:

    cpu = random.uniform(1, 6)

    memory = random.uniform(20, 40)

    cpu_chart.add_rows(
        pd.DataFrame({"CPU": [cpu]})
    )

    memory_chart.add_rows(
        pd.DataFrame({"Memory": [memory]})
    )

    if cpu > 4:

        status.error(
            f"⚠️ Predictive Risk Detected | CPU: {cpu:.2f}%"
        )

        restart_count += 1

    else:

        status.success(
            f"✅ System Stable | CPU: {cpu:.2f}%"
        )

    restart_metric.metric(
        "Kubernetes Heal Count",
        restart_count
    )

    time.sleep(2)
