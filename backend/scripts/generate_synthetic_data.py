import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data(rows=5000, filename="synthetic_data.csv"):
    random.seed(42)

    regions = ["North", "South", "East", "West"]
    statuses = ["success", "failed"]

    data = []

    base_date = datetime.now() - timedelta(days=30)

    for i in range(rows):
        record = {
            "record_id": i + 1,
            "user_id": random.randint(1, int(rows * 0.2)),  # repeated users
            "transaction_amount": round(random.normalvariate(500, 120), 2),
            "region": random.choice(regions),
            "event_date": (base_date + timedelta(days=random.randint(0, 30))).date(),
            "status": random.choice(statuses)
        }

        data.append(record)

    df = pd.DataFrame(data)

    # 🔴 Inject NULL values (5%)
    for col in ["transaction_amount", "region"]:
        df.loc[df.sample(frac=0.05).index, col] = None

    # 🔴 Inject duplicates (3%)
    duplicates = df.sample(frac=0.03)
    df = pd.concat([df, duplicates], ignore_index=True)

    # 🔴 Inject anomalies (1%)
    anomaly_indices = df.sample(frac=0.01).index
    df.loc[anomaly_indices, "transaction_amount"] *= 10

    df.to_csv(filename, index=False)
    print(f"Generated {len(df)} rows → {filename}")


if __name__ == "__main__":
    generate_data(rows=10000, filename="synthetic_10k.csv")
