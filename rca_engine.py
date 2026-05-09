def analyze_root_cause(metrics):

    cpu = metrics['cpu']
    memory = metrics['memory']
    disk = metrics['disk']
    network = metrics['network']

    # -----------------------------
    # ROOT CAUSE RULES
    # -----------------------------

    if cpu > 2.0 and memory < 30:
        return "High CPU workload detected"

    elif memory > 25.1:
        return "Possible memory pressure or memory leak"

    elif disk > 80:
        return "Disk space exhaustion risk"

    elif network > 100000:
        return "Unusual network traffic spike"

    elif cpu > 2.0 and memory > 25:
        return "Combined CPU and memory instability"

    else:
        return "General infrastructure anomaly"
