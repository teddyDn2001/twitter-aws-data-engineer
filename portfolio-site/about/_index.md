---
title: "About"
draft: false
---

**Twitter AWS Data Engineering Pipeline**

- **Ingest**: Twitter API → S3 (`raw/`)
- **Transform**: EMR Spark → S3 (`cleansed/`, `processed/`)
- **Load**: Redshift (COPY Parquet) / **Query**: Athena
- **Catalog**: Glue Database + Crawlers
- **Orchestrate**: Airflow
- **Visualize**: QuickSight / Power BI

Repo code: [GitHub](https://github.com/teddyDn2001/twitter-aws-data-engineer)