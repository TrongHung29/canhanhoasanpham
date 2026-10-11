import pandas as pd
from .config import settings

def create_features(cutoff_day: int):
    print(f"Creating features for cutoff day {cutoff_day}...")
    # In a real scenario, this would create features.
    pass

if __name__ == "__main__":
    for day in settings.cutoff_days:
        create_features(day)
