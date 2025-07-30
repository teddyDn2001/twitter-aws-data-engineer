---
title: "Twitter AWS Data Engineering Pipeline"
date: 2025-07-30
draft: false
weight: 1
---

## Kiến trúc tổng quan
Luồng xử lý:
1. **Raw → Cleansed**: Spark job trên EMR (`spark_elt_twitter.py`) đọc S3 `raw/`, clean, ghi ra `cleansed/`.
2. **Cleansed → Processed**: Spark job `processed.py`, ghi Parquet sang `processed/`.
3. **Glue Crawler**: scan `processed/`, tạo bảng **Glue Data Catalog** (`social_media`).
4. **Athena/Redshift**: Truy vấn & nạp vào Redshift với `COPY`.
5. **Airflow**: orchestration EMR steps + Redshift load (DAG `twitter_full_etl_pipeline`).
6. **BI**: QuickSight/Power BI dashboard.

## AWS Architecture
![AWS Architecture](/images/architecture.png)

## QuickSight Dashboard
![QuickSight Dashboard](/images/quicks.png)

## Redshift COPY
```sql
COPY processed_tweets
FROM 's3://social-media-data-tuananh/processed/twitter/'
IAM_ROLE 'arn:aws:iam::<ACCOUNT_ID>:role/RedshiftS3Access'
FORMAT AS PARQUET;