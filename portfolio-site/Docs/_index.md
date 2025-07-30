---
title: "Docs"
draft: false
---

## Hướng dẫn nhanh
1. **Crawl** Twitter → S3 `raw/`.
2. **Spark on EMR** chuẩn hoá → `cleansed/`, tổng hợp → `processed/`.
3. **Glue Crawler** tạo bảng `twitter_cleansed`, `twitter_processed`.
4. **Athena** truy vấn nhanh; **Redshift** cho BI / dashboard.
5. **Airflow** lên lịch tự động.
6. **QuickSight / Power BI** trực quan hoá KPIs.

> Xem repo để biết script: `crawl_tweets.py`, `spark_elt_twitter.py`, `processed.py`, `airflow_dags.py`.