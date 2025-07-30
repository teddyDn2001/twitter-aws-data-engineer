---
title: "Docs"
date: 2025-07-30
draft: false
---

## Cách chạy / tái lập
1. Tạo các bucket S3: `raw/`, `cleansed/`, `processed/`.
2. Chạy EMR Spark jobs để ETL.
3. Glue Crawler scan `processed/` → tạo bảng trong Glue Data Catalog.
4. **Athena** kiểm tra schema, truy vấn thử.
5. **Redshift**: dùng `COPY` nạp Parquet từ S3.
6. Dashboard BI: QuickSight / Power BI.