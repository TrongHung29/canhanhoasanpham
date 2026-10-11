# Từ Điển Dữ Liệu (Data Dictionary)

Dự án: Gợi ý sản phẩm theo tìm kiếm, giới tính và xu hướng

Phạm vi đã được hợp nhất với các hướng popularity/rank-based và collaborative filtering (user-based, SVD) từ một dự án tham khảo. Dataset Amazon Electronics của dự án đó không được ghép vào H&M do khác miền và hệ ID; các phương pháp được đánh giá lại trên tương tác H&M. Xem [đề tài hợp nhất](docs/de_tai_ket_hop.md).

## 1. Nguồn Dữ Liệu Thực Tế & Mô Phỏng

Trong các thí nghiệm, giao dịch H&M là phản hồi ngầm (implicit feedback), không phải rating. Popularity và ALS là các baseline chính; user-based CF và SVD là phương pháp đối chiếu. Không diễn giải RMSE từ rating Amazon thành metric của dữ liệu H&M.

| Nguồn | Định dạng / Nơi lưu trữ | Nội dung | Thật / Mô phỏng |
| --- | --- | --- | --- |
| `customers` | PostgreSQL (bảng `customers`) | Thông tin người dùng (tuổi, hạng thành viên, giới tính) | Tuổi, thành viên: Thật. Giới tính: Suy ra |
| `articles` | CSV (`articles.csv`) | Thuộc tính sản phẩm (loại, màu, nhóm hàng, mô tả) | Thật |
| `transactions` | Data lake (Parquet) | Lịch sử mua hàng (giá, kênh bán, ngày mua) | Thật |
| `search_log` | Data lake (JSON/Parquet) | Từ khóa tìm kiếm của người dùng theo thời gian | Mô phỏng |
| `view_events` | Data lake (Parquet) | Hành vi xem sản phẩm, thêm vào giỏ hàng | Mô phỏng |
| `trends` | CSV / API | Dữ liệu Google Trends & độ bán chạy nội bộ | Google Trends: Thật. Bán chạy: Tính toán |

## 2. Chi Tiết Các Bảng / File

### 2.1. Bảng `customers` (PostgreSQL)
- **`customer_id`** (VARCHAR): ID định danh người dùng (đã được hash).
- **`age`** (INT): Tuổi của người dùng.
- **`club_member_status`** (VARCHAR): Trạng thái thành viên.
- **`gender`** (VARCHAR): Giới tính (female / male / unknown) - Được suy ra từ hành vi mua hàng.

### 2.2. File `articles.csv`
- **`article_id`** (VARCHAR): ID định danh sản phẩm.
- **`product_type_name`** (VARCHAR): Loại sản phẩm (ví dụ: T-shirt, Trousers).
- **`product_group_name`** (VARCHAR): Nhóm sản phẩm (ví dụ: Garment Upper body).
- **`colour_group_name`** (VARCHAR): Tên màu sắc.
- **`index_group_name`** (VARCHAR): Nhóm hàng (Ladieswear, Menswear...).
- **`detail_desc`** (TEXT): Mô tả chi tiết sản phẩm.

### 2.3. Lịch sử `transactions` (Parquet)
- **`t_dat`** (DATE): Ngày giao dịch.
- **`customer_id`** (VARCHAR): ID khách hàng.
- **`article_id`** (VARCHAR): ID sản phẩm đã mua.
- **`price`** (FLOAT): Giá mua.
- **`sales_channel_id`** (INT): Kênh bán hàng (Online / Offline).

### 2.4. Log `search_log` (Mô phỏng - Parquet)
- **`timestamp`** (DATETIME): Thời điểm tìm kiếm (đặt trước lúc mua 0-7 ngày).
- **`customer_id`** (VARCHAR): ID khách hàng.
- **`query`** (VARCHAR): Từ khóa tìm kiếm (sinh từ thuộc tính sản phẩm + thêm nhiễu).

### 2.5. Sự kiện `view_events` (Mô phỏng - Parquet)
- **`timestamp`** (DATETIME): Thời điểm xem/thêm giỏ hàng.
- **`customer_id`** (VARCHAR): ID khách hàng.
- **`article_id`** (VARCHAR): ID sản phẩm.
- **`event_type`** (VARCHAR): Loại sự kiện (`view` hoặc `add_to_cart`).

### 2.6. Xu hướng `trends` (CSV)
- **`date_week`** (DATE): Tuần tương ứng.
- **`keyword`** (VARCHAR): Từ khóa tìm kiếm hoặc loại sản phẩm.
- **`google_trend_score`** (FLOAT): Điểm số quan tâm trên Google Trends.
- **`internal_sales_score`** (FLOAT): Điểm độ bán chạy nội bộ.
