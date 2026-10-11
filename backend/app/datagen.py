import pandas as pd
import numpy as np
import sqlite3
from .config import settings

def generate_synthetic_data(seed: int = 42):
    np.random.seed(seed)
    
    # 1. Customers (SQLite)
    customers = pd.DataFrame({
        'customer_id': range(1, 3001),
        'age': np.random.randint(18, 65, 3000),
        'gender': np.random.choice(['M', 'F'], 3000),
        'member_status': np.random.choice(['Gold', 'Silver', 'Bronze'], 3000)
    })
    conn = sqlite3.connect(settings.db_path)
    customers.to_sql('customers', conn, index=False, if_exists='replace')
    conn.close()
    
    # 2. Articles & Trends (CSV)
    articles = pd.DataFrame({
        'article_id': range(1, 289),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 288),
        'price': np.random.uniform(10, 100, 288)
    })
    articles.to_csv(settings.articles_path, index=False)
    
    trends = pd.DataFrame({
        'week': np.repeat(range(26), 4),
        'category': np.tile(['A', 'B', 'C', 'D'], 26),
        'trend_score': np.random.uniform(0, 1, 26 * 4)
    })
    trends.to_csv(settings.trends_path, index=False)
    
    # 3. Transactions, Search, Views (Parquet)
    num_days = 182
    transactions = pd.DataFrame({
        'transaction_id': range(1, 36001),
        'customer_id': np.random.choice(customers['customer_id'], 36000),
        'article_id': np.random.choice(articles['article_id'], 36000),
        'day': np.random.randint(0, num_days, 36000)
    })
    transactions.to_parquet(settings.transactions_path, index=False)
    
    search_log = pd.DataFrame({
        'customer_id': np.random.choice(customers['customer_id'], 31000),
        'query': np.random.choice(['shirt', 'pants', 'shoes'], 31000),
        'day': np.random.randint(0, num_days, 31000)
    })
    search_log.to_parquet(settings.search_log_path, index=False)
    
    view_events = pd.DataFrame({
        'customer_id': np.random.choice(customers['customer_id'], 50000),
        'article_id': np.random.choice(articles['article_id'], 50000),
        'day': np.random.randint(0, num_days, 50000)
    })
    view_events.to_parquet(settings.view_events_path, index=False)
    
    print("Synthetic data generated successfully.")

if __name__ == "__main__":
    generate_synthetic_data()
