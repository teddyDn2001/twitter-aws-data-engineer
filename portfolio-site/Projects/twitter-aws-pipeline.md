---
title: "End-to-end Twitter AWS Data Engineering"
date: 2025-07-30
tags: ["AWS", "Spark", "Airflow", "Redshift", "Glue", "Athena"]
draft: false
---

## 1) Kiến trúc
![Architecture](/images/architecture.png)

**Dịch vụ:** S3, EMR (Spark), Glue (DB + Crawler), Athena, Redshift, Airflow, QuickSight/Power BI.

## 2) Data Lake layout (S3)
- `s3://social-media-data-tuananh/raw/`
- `s3://social-media-data-tuananh/cleansed/`
- `s3://social-media-data-tuananh/processed/`

## 3) Orchestration
- EMR Step 1: raw → cleansed  
- EMR Step 2: cleansed → processed  
- Redshift COPY từ `processed/` (Parquet)

## 4) Analytics
- Athena/Glue cho ad-hoc queries  
- QuickSight/Power BI: trend tweet/day, top hashtag, sentiment, source device.

## 5) DAG Airflow (tóm tắt)
- EmrAddStepsOperator → EmrStepSensor → RedshiftSQLOperator