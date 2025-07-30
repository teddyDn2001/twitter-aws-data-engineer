---
title: "3. Airflow DAGs"
draft: false
---
DAG `twitter_full_etl_pipeline`:
- `EmrAddStepsOperator` chạy Spark trên EMR
- `EmrStepSensor` chờ step hoàn tất
- `RedshiftSQLOperator` COPY vào Redshift