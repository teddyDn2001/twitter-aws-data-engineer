# AWS Twitter Data Engineering Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Made with](https://img.shields.io/badge/made%20with-Python%20%26%20Spark-blue)

> End‑to‑end data engineering pipeline trên AWS để thu thập, xử lý, catalog, phân tích và trực quan hóa dữ liệu Twitter.  
> Triển khai theo mô hình Data Lake (Raw → Cleansed → Processed), có thể mở rộng cho doanh nghiệp.

---

## 📚 Mục lục
- [1. Giới thiệu](#-giới-thiệu)
- [2. Kiến trúc](#-kiến-trúc)
- [3. Luồng xử lý dữ liệu](#-luồng-xử-lý-dữ-liệu)
- [4. Cách chạy (Demo)](#-cách-chạy-demo)
- [5. SQL mẫu (Athena)](#-sql-mẫu-athena)
- [6. Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [7. Hướng phát triển](#-hướng-phát-triển)
- [8. Cấu trúc repo](#-cấu-trúc-repo)
- [9. Tác giả](#-tác-giả)
- [10. License](#-license)

---

## 🔎 Giới thiệu
Dự án mô phỏng quy trình **ETL/ELT hiện đại**:
- Thu thập dữ liệu Twitter (script Python hoặc API).
- Lưu trữ trên **S3** (Raw → Cleansed → Processed).
- Xử lý/làm sạch bằng **Spark trên EMR** (trigger qua **Airflow**).
- Tạo **Glue Data Catalog** & query bằng **Athena**.
- Tải vào **Redshift** (tuỳ chọn) cho analytics chuyên sâu.
- Trực quan hóa bằng **QuickSight** hoặc **PowerBI**.

> **Mục tiêu:** Portfolio Data Engineer/Analyst có tính thực chiến, dễ mở rộng.

---

## 🏗 Kiến trúc
Twitter (API/Crawler)
|
v
S3 / raw  ––>  EMR (Spark jobs)  ––>  S3 / cleansed  ––>  S3 / processed
|                                   |
v                                   v
Glue Crawler  ——————>  Glue Catalog
|                                   |
+–––––> Athena  <–––––––+
|
+–> Redshift (tuỳ chọn)
|
+–> QuickSight / PowerBI
Orchestration: Airflow (DAG: twitter_full_etl_pipeline)


---

## 🔄 Luồng xử lý dữ liệu

1. **Crawl dữ liệu Twitter**  
   - Script: `crawl_tweets.py`  
   - Output: `s3://<bucket>/raw/...`

2. **Spark ETL trên EMR (Raw → Cleansed → Processed)**  
   - Job: `spark_elt_twitter.py` (chuẩn hoá schema, làm sạch, chuẩn Parquet)
   - Trigger bởi **Airflow DAG** `twitter_full_etl_pipeline.py`

3. **Data Catalog với Glue Crawler**  
   - Crawler chỉ vào prefixes `s3://.../cleansed/` và `s3://.../processed/`
   - Tạo bảng trong **Glue Database** (ví dụ: `social_media` / `twitter_analytics`)

4. **Query bằng Athena / Load vào Redshift**  
   - SQL truy vấn trực tiếp data processed  
   - Copy vào Redshift (nếu cần BI nặng, phân tích OLAP)

5. **BI Layer**  
   - **QuickSight** (AWS-native) hoặc **PowerBI** (kết nối Athena ODBC)

---

## 🧪 Cách chạy (Demo)

### Yêu cầu
- Python 3.9+
- Đã cấu hình **AWS CLI**: `aws configure`
- Quyền IAM cho S3/EMR/Glue/Athena/Redshift (nếu dùng)

### 1) Clone project
```bash
git clone https://github.com/<your-username>/twitter-aws-data-engineer.git
cd twitter-aws-data-engineer

2) Cài đặt Python packages
pip install -r requirements.txt

3) Chạy Airflow cục bộ (tuỳ chọn demo)
export AIRFLOW_HOME=~/airflow
airflow db init
# Copy DAG vào thư mục:
#   cp airflow_dags.py  ~/airflow/dags/twitter_full_etl_pipeline.py
airflow webserver -p 8080 &
airflow scheduler &
# Mở http://localhost:8080 rồi bật DAG

4) Spark job trên EMR (production)
	•	Upload scripts vào s3://<bucket>/scripts/
	•	Airflow → EmrAddStepsOperator gọi spark-submit với input/output tương ứng:
	•	Input: s3://<bucket>/raw/
	•	Output: s3://<bucket>/cleansed/ → s3://<bucket>/processed/

5) Glue & Athena
	•	Tạo Glue Database (ví dụ social_media)
	•	Tạo Glue Crawler → trỏ vào cleansed/ & processed/ → chạy crawler
	•	Vào Athena → chọn database vừa tạo → chạy SQL (ví dụ ở bên dưới)

⸻

🧾 SQL mẫu (Athena)
-- Top 10 user tweet nhiều nhất
SELECT user_name, COUNT(*) AS tweet_count
FROM twitter_processed
GROUP BY user_name
ORDER BY tweet_count DESC
LIMIT 10;

-- Hashtag phổ biến
SELECT lower(hashtag) AS tag, COUNT(*) as cnt
FROM twitter_processed
CROSS JOIN UNNEST(hashtags) AS t(hashtag)
GROUP BY lower(hashtag)
ORDER BY cnt DESC
LIMIT 20;

-- Tương tác theo ngày
SELECT date_trunc('day', created_at) AS d, COUNT(*) AS tweets
FROM twitter_processed
GROUP BY 1
ORDER BY 1;

🛠 Công nghệ sử dụng
	•	AWS: S3, EMR (Spark), Glue Crawler & Catalog, Athena, (tuỳ chọn) Redshift, QuickSight
	•	Processing: Apache Spark (PySpark)
	•	Orchestration: Apache Airflow
	•	Ngôn ngữ: Python
	•	BI: PowerBI / QuickSight

⸻

🚀 Hướng phát triển
	•	Thêm ML/AI: Sentiment Analysis, Topic Modeling (SageMaker / Bedrock)
	•	Streaming real‑time với Kafka/MSK
	•	Redshift Spectrum / Iceberg table để tối ưu chi phí query

⸻

🗂 Cấu trúc repo
twitter-aws-data-engineer/
├── airflow_dags.py                 # DAG Airflow (gọi EMR + Redshift COPY)
├── spark_elt_twitter.py            # Spark job: raw -> cleansed -> processed
├── crawl_tweets.py                 # (Tuỳ chọn) Crawl dữ liệu Twitter
├── bootstrap.sh                    # (Tuỳ chọn) Script bootstrap EMR
├── PROJECT DATA ENGINEERING.docx   # Proposal (bản thảo)
├── README.md
└── images/
    ├── architecture.png            # (Tuỳ chọn) Kiến trúc
    └── dashboard-demo.png          # (Tuỳ chọn) Dashboard

👤 Tác giả
	•	Tên: Doanh Teddy
	•	LinkedIn: https://www.linkedin.com/in/adoan2201/
	•	GitHub: https://github.com/teddyDn2001

⸻

📜 License

Phát hành dưới giấy phép MIT – xem file LICENSE để biết thêm chi tiết.