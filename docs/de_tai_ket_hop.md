# Đề tài hợp nhất

## Tên đề tài

**Xây dựng hệ thống gợi ý sản phẩm thương mại điện tử đa tín hiệu: kết hợp độ phổ biến, lọc cộng tác, tìm kiếm, hồ sơ người dùng và xu hướng thị trường**

## 1. Mục tiêu và câu hỏi nghiên cứu

Với mỗi khách hàng, hệ thống xếp hạng các sản phẩm có khả năng được mua trong 7 ngày tiếp theo và trả về top-12. Hệ thống kết hợp lịch sử giao dịch với tương tác ngầm, thuộc tính sản phẩm, truy vấn tìm kiếm, hồ sơ người dùng và tín hiệu xu hướng.

Câu hỏi nghiên cứu chính: việc bổ sung từng nhóm tín hiệu vào baseline lọc cộng tác có cải thiện chất lượng gợi ý, đặc biệt với người dùng mới hoặc ít lịch sử, hay không?

## 2. Cách kết hợp hai hướng

Đề tài hiện tại cung cấp bài toán H&M và các tín hiệu tìm kiếm, hồ sơ, xu hướng. Repo tham khảo cung cấp các nhóm thuật toán popularity/rank-based, user-based collaborative filtering và model-based collaborative filtering. Các nhóm này được đưa vào làm baseline và nguồn tạo ứng viên trong cùng một pipeline.

Không gộp trực tiếp dataset Amazon Electronics trong repo tham khảo với H&M: hai bộ dữ liệu khác miền sản phẩm, hệ ID và kiểu phản hồi. Dữ liệu Amazon có rating tường minh, còn giao dịch H&M được diễn giải là phản hồi ngầm. Vì vậy, không dùng rating Amazon để huấn luyện hoặc đánh giá mô hình H&M; chỉ kế thừa ý tưởng phương pháp và triển khai lại trên tương tác H&M phù hợp.

## 3. Dữ liệu và giả định

- **Dữ liệu lõi:** customers, articles và transactions từ bộ H&M; giao dịch mua được xem là tương tác dương.
- **Popularity:** tính độ phổ biến sản phẩm từ số tương tác/mua trong cửa sổ thời gian trước ngày dự đoán; đây là baseline và phương án cho cold start.
- **Lọc cộng tác:** so sánh user-based cosine similarity trên mẫu phù hợp và matrix factorization. ALS trên tương tác ngầm là baseline cộng tác chính; SVD được giữ làm đối chứng khi biểu diễn ma trận và quy mô cho phép.
- **Tìm kiếm và xem:** search_log, view_events và add_to_cart có thể được mô phỏng theo cấu hình cố định. Kết quả dùng các tín hiệu mô phỏng phải được báo cáo tách biệt và không được diễn giải như bằng chứng hiệu quả trên log thực.
- **Hồ sơ:** tuổi và trạng thái thành viên lấy từ dữ liệu; gender nếu sử dụng là nhãn suy ra, có nhóm unknown, không phải thông tin người dùng khai báo.
- **Xu hướng:** điểm Google Trends và độ bán chạy nội bộ theo tuần; chỉ dùng giá trị có sẵn trước thời điểm dự đoán.

## 4. Pipeline mô hình

### Giai đoạn A: sinh ứng viên

Gộp ứng viên từ top sản phẩm phổ biến, mua lại gần đây, ALS, sản phẩm tương tự theo thuộc tính/mô tả, truy vấn tìm kiếm gần nhất, và sản phẩm được xem hoặc thêm giỏ. User-based collaborative filtering và SVD là các nhánh đối chứng; chỉ giữ trong pipeline ứng viên nếu chi phí và độ phủ phù hợp.

### Giai đoạn B: xếp hạng

Tạo một hàng cho mỗi cặp người dùng-sản phẩm ứng viên. Nhãn dương là sản phẩm được mua trong 7 ngày tiếp theo. Dùng LightGBM ranker để kết hợp điểm từ các bộ sinh ứng viên với đặc trưng lịch sử mua, tìm kiếm, xem/giỏ, hồ sơ, sản phẩm và xu hướng. Lọc sản phẩm vừa mua và áp dụng giới hạn đa dạng sau xếp hạng.

Mọi đặc trưng phải được tính từ dữ liệu trước mốc dự đoán để tránh rò rỉ thời gian.

## 5. Thiết kế thực nghiệm

Chia dữ liệu theo thời gian: train trên các tuần cũ, validation trên tuần liền trước test và test trên tuần cuối. Tất cả baseline phải dùng cùng mốc chia và tập ứng viên tương đương khi có thể.

So sánh các cấu hình:

| Mã | Cấu hình |
| --- | --- |
| P | Popularity/rank-based, ưu tiên cho người dùng mới |
| U | User-based collaborative filtering |
| S | SVD model-based collaborative filtering, nếu khả dụng |
| A | ALS trên tương tác ngầm H&M |
| H | Hybrid: ALS + nội dung sản phẩm + LightGBM ranker |
| H+ | H + tìm kiếm, xem/giỏ, hồ sơ và xu hướng |

Đánh giá bằng MAP@12 (chính), Recall@12, NDCG@12, coverage và diversity. Phân tích riêng người dùng mới, người dùng có 1-3 giao dịch và người dùng có ít nhất 10 giao dịch. Ablation so sánh H với H+ để đo phần đóng góp của các tín hiệu mở rộng; bootstrap có thể dùng để ước lượng độ bất định.

RMSE chỉ phù hợp khi có rating tường minh thực sự. Vì H&M không cung cấp rating như Amazon Electronics, không báo cáo RMSE trên giao dịch H&M như thể đó là rating; dùng các metric top-K ở trên.

## 6. Phạm vi ưu tiên

Để giữ đề tài khả thi, thứ tự triển khai là popularity và ALS trước, tiếp theo là LightGBM ranker, rồi mới thêm nội dung, tìm kiếm và xu hướng. User-based CF/SVD là baseline đối chiếu, có thể giới hạn trên mẫu nếu tốn bộ nhớ hoặc thời gian. Nếu phải giảm phạm vi, giữ ablation và đánh giá cold-start; bỏ SVD hoặc Google Trends trước khi bỏ các kiểm tra chống rò rỉ.

## 7. Tiêu chí báo cáo

- Nêu rõ nguồn nào là dữ liệu thật, suy ra hay mô phỏng.
- Không coi các kết quả mẫu/giả lập là kết quả thực nghiệm; chỉ công bố metric sau khi pipeline chạy trên dữ liệu và phép chia thời gian thật.
- Báo cáo hiệu năng theo từng nhóm người dùng, cùng độ phủ và mức đa dạng.
- So sánh với popularity và ALS, không chỉ so sánh các cấu hình hybrid với nhau.
- Ghi nhận giới hạn ngoại suy từ log tìm kiếm/xem mô phỏng sang hành vi người dùng thực.