import sqlite3
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure project root is on sys.path regardless of how Streamlit is invoked
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from backend.app.config import settings


st.set_page_config(
    page_title="Morrow | Gợi ý sản phẩm",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
    :root {
      --ink: #20241f;
      --muted: #74796f;
      --paper: #f7f7f2;
      --line: #e4e6dd;
      --green: #355b45;
      --lime: #d7e69b;
      --coral: #dd775f;
    }
    .stApp { background: var(--paper); color: var(--ink); }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; color: var(--ink); }
    [data-testid="stSidebar"] { background: #eef0e8; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] h1 { font-size: 1.35rem; }
    .eyebrow { color: var(--green); font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .12em; }
    .hero { padding: 1.3rem 0 1.6rem; border-bottom: 1px solid var(--line); margin-bottom: 1.5rem; }
    .hero h1 { font-size: clamp(2rem, 4vw, 3.35rem); line-height: 1.08; margin: .45rem 0; }
    .hero p { color: var(--muted); max-width: 650px; margin: 0; }
    .metric { background: #fff; border: 1px solid var(--line); border-radius: 6px; padding: 1rem 1.1rem; min-height: 94px; }
    .metric-label { color: var(--muted); font-size: .76rem; text-transform: uppercase; font-weight: 700; }
    .metric-value { color: var(--ink); font-size: 1.6rem; font-weight: 700; margin-top: .3rem; }
    .product-art { height: 110px; background: linear-gradient(135deg, #e5e9db, #d5dfcb); border-radius: 4px; display: flex; align-items: center; justify-content: center; color: var(--green); font: 600 2rem 'Playfair Display', Georgia, serif; }
    .product-meta { color: var(--muted); font-size: .8rem; }
    .product-price { color: var(--ink); font-size: 1.05rem; font-weight: 700; }
    .rec-note { background: #edf2e7; border-left: 3px solid var(--green); color: #435245; padding: .75rem 1rem; border-radius: 0 4px 4px 0; font-size: .88rem; }
    .stButton > button { border-radius: 4px; border-color: var(--green); color: var(--green); }
    .stButton > button:hover { background: var(--green); color: white; border-color: var(--green); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    required_paths = [
        settings.db_path,
        settings.articles_path,
        settings.transactions_path,
    ]
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        raise FileNotFoundError(
            "Chưa có dữ liệu demo. Hãy chạy `python -m backend.app.datagen` "
            "từ thư mục dự án trước."
        )

    with sqlite3.connect(settings.db_path) as connection:
        customers = pd.read_sql_query("SELECT * FROM customers", connection)
    articles = pd.read_csv(settings.articles_path)
    transactions = pd.read_parquet(settings.transactions_path)
    return customers, articles, transactions


def get_recommendations(customer_id, articles, transactions, query, limit):
    customer_history = transactions[
        transactions["customer_id"] == customer_id
    ]
    bought_ids = set(customer_history["article_id"])

    item_popularity = transactions.groupby("article_id").size()
    max_popularity = max(int(item_popularity.max()), 1)
    catalog = articles.copy()
    catalog["popularity"] = catalog["article_id"].map(item_popularity).fillna(0)
    catalog["popularity_score"] = catalog["popularity"] / max_popularity

    category_counts = customer_history.merge(
        articles[["article_id", "category"]], on="article_id", how="left"
    )["category"].value_counts(normalize=True)
    catalog["category_score"] = catalog["category"].map(category_counts).fillna(0)

    candidates = catalog[~catalog["article_id"].isin(bought_ids)].copy()
    trimmed_query = query.strip()
    if trimmed_query:
        searchable = (
            candidates["category"].astype(str)
            + " "
            + candidates["article_id"].astype(str)
        )
        candidates = candidates[searchable.str.contains(trimmed_query, case=False, regex=False)]

    if candidates.empty:
        return candidates

    if customer_history.empty:
        candidates["score"] = candidates["popularity_score"]
        candidates["reason"] = "Đang thịnh hành"
    else:
        candidates["score"] = (
            0.65 * candidates["category_score"]
            + 0.35 * candidates["popularity_score"]
        )
        candidates["reason"] = candidates.apply(
            lambda item: "Hợp nhóm hàng bạn thường mua"
            if item["category_score"] > 0
            else "Đang thịnh hành",
            axis=1,
        )

    return candidates.sort_values(
        ["score", "popularity"], ascending=False
    ).head(limit)


try:
    customers, articles, transactions = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

st.sidebar.markdown("# MORROW")
st.sidebar.caption("KHÁM PHÁ SẢN PHẨM · BẢN THỬ")
st.sidebar.markdown("---")
customer_ids = sorted(customers["customer_id"].tolist())
customer_id = st.sidebar.selectbox("Chọn khách hàng", customer_ids)
query = st.sidebar.text_input(
    "Tìm theo nhóm hàng hoặc mã sản phẩm", placeholder="Ví dụ: A hoặc 42"
)
result_count = st.sidebar.slider("Số sản phẩm gợi ý", min_value=4, max_value=12, value=8)

customer = customers.loc[customers["customer_id"] == customer_id].iloc[0]
history = transactions[transactions["customer_id"] == customer_id]
recommendations = get_recommendations(
    customer_id, articles, transactions, query, result_count
)

st.markdown(
    """
    <div class="hero">
    <div class="eyebrow">Gợi ý sản phẩm cá nhân hóa</div>
    <h1>Tìm món đồ<br>tiếp theo của bạn.</h1>
    <p>Khám phá sản phẩm phù hợp với lịch sử mua và nhóm hàng bạn quan tâm.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(3)
metrics = [
    ("Khách hàng", f"{len(customers):,}"),
    ("Sản phẩm", f"{len(articles):,}"),
    ("Lượt mua của bạn", f"{len(history):,}"),
]
for column, (label, value) in zip(metric_columns, metrics):
    column.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")
left, right = st.columns([3, 1])
with left:
    st.markdown("## Gợi ý dành cho bạn")
    st.caption("Xếp hạng theo lịch sử mua và độ phổ biến trong dữ liệu demo")
with right:
    st.markdown(f"**Khách hàng {customer_id}**")
    st.caption(f"{customer['age']} tuổi · Thành viên {customer['member_status']}")

st.markdown(
    '<div class="rec-note">Bản demo dùng dữ liệu synthetic và công thức xếp hạng đơn giản, '
    "chưa phải mô hình ML đã huấn luyện.</div>",
    unsafe_allow_html=True,
)
st.write("")

if recommendations.empty:
    st.info("Không tìm thấy sản phẩm phù hợp với từ khóa này.")
else:
    for start in range(0, len(recommendations), 4):
        product_columns = st.columns(4, gap="medium")
        batch = recommendations.iloc[start : start + 4]
        for column, (_, product) in zip(product_columns, batch.iterrows()):
            with column:
                st.markdown(
                    f'<div class="product-art">{product["category"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Product {int(product['article_id']):04d}**")
                st.markdown(
                                    f'<div class="product-meta">Nhóm {product["category"]} '
                                    f'· {int(product["popularity"]):,} lượt mua</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="product-price">Giá demo: {product["price"]:.2f}</div>',
                    unsafe_allow_html=True,
                )
                st.caption(product["reason"])

st.caption("Catalog và giá được sinh ngẫu nhiên để minh họa; không đại diện giá bán thực tế.")