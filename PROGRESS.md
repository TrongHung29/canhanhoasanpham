# Tiến độ dự án

## Phạm vi đề tài đã hợp nhất
- [x] Bổ sung popularity/rank-based làm baseline và hướng xử lý cold-start.
- [x] Đưa user-based CF và SVD vào nhóm phương pháp đối chiếu; giữ ALS làm baseline cộng tác chính cho tương tác ngầm H&M.
- [x] Chốt không trộn dataset Amazon Electronics với H&M; log tìm kiếm/xem mô phỏng phải được đánh dấu và báo cáo riêng.
- [ ] Cập nhật triển khai/đánh giá để so sánh popularity, user-based CF, SVD (nếu khả thi), ALS và hybrid theo cùng phép chia thời gian.
- [ ] Thay kết quả placeholder bằng metric thu được khi pipeline chạy trên dữ liệu thực.

Tài liệu tổng hợp: [docs/de_tai_ket_hop.md](docs/de_tai_ket_hop.md).

## Môi trường và dữ liệu (Bước 1)
- [x] Tạo cấu trúc thư mục (`configs`, `src`, `tests`, `notebooks`, `docs`, `data`).
- [x] Cập nhật `docker-compose.yml` cho PostgreSQL.
- [x] Tạo `configs/simulation.yaml` lưu trữ tham số sinh dữ liệu.
- [ ] Thiết lập môi trường ảo Python.
- [ ] Cài đặt `kaggle`, `pandas`, `duckdb`, `scikit-learn`, `implicit`, `lightgbm`, `sentence-transformers`, `mlflow`, `fastapi`, `streamlit`, `pytrends`.
- [ ] Tải bộ dữ liệu `h-and-m-personalized-fashion-recommendations` bằng Kaggle CLI.
- [ ] Khởi chạy PostgreSQL và lấy mẫu 100.000 khách hàng.

**Vấn đề hiện tại:** Cần thiết lập môi trường ảo, cài đặt Kaggle CLI và tải dữ liệu.
