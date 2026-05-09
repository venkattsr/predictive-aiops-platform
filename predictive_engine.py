import numpy as np

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

    risk_detected = predicted_next > 2.2

    return risk_detected, predicted_next
