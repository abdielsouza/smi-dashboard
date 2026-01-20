import pandas as pd
import numpy as np

def generate_data():
    np.random.seed(42)
    n = 3000

    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="H")
    machines = np.random.choice(["MX-01", "MX-02", "MX-03"], n, p=[0.4, 0.35, 0.25])

    temperature = np.random.normal(72, 6, n)
    vibration = np.random.gamma(2.2, 2, n)
    energy = 80 + temperature * 0.6 + vibration * 3 + np.random.normal(0, 8, n)
    production = np.maximum(0, 70 - vibration * 4 + np.random.normal(0, 6, n))

    df = pd.DataFrame({
        "timestamp": timestamps,
        "machine_id": machines,
        "temperature": temperature,
        "vibration": vibration,
        "energy_kwh": energy,
        "production_units": production
    })

    # Regra industrial de falha
    df["failure"] = (
        (df["temperature"] > 88) |
        (df["vibration"] > 9) |
        (df["energy_kwh"] > 150)
    ).astype(int)

    df["status"] = df["failure"].map({0: "Operando", 1: "Falha"})

    df.to_csv("data/dados_maquinas.csv", index=False)
    print("Dados industriais realistas gerados.")

if __name__ == '__main__':
    generate_data()