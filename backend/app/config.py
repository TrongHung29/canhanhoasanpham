import os
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

from typing import Literal

class Config(BaseModel):
    dataset: Literal["synthetic", "hm"] = "synthetic"
    data_dir: Path = DATA_DIR
    db_path: Path = DATA_DIR / "customers.db"
    articles_path: Path = DATA_DIR / "articles.csv"
    trends_path: Path = DATA_DIR / "trends.csv"
    transactions_path: Path = DATA_DIR / "transactions.parquet"
    search_log_path: Path = DATA_DIR / "search_log.parquet"
    view_events_path: Path = DATA_DIR / "view_events.parquet"
    
    # training params
    cutoff_days: list[int] = [147, 154, 161, 168]
    test_day: int = 175

settings = Config()

if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

