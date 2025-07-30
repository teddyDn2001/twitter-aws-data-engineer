from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# 🔧 Step 1: Spark job từ raw → cleansed
SPARK_RAW_TO_CLEANSED = [
    {
        'Name': 'Spark ETL Raw to Cleansed',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                's3://social-media-data-tuananh/scripts/spark_elt_twitter.py',
                's3://social-media-data-tuananh/raw/',
                's3://social-media-data-tuananh/cleansed/'
            ]
        }
    }
]

# 🔧 Step 2: Spark job từ cleansed → processed
SPARK_CLEANSED_TO_PROCESSED = [
    {
        'Name': 'Spark ETL Cleansed to Processed',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                's3://social-media-data-tuananh/scripts/processed.py',
                's3://social-media-data-tuananh/cleansed/',
                's3://social-media-data-tuananh/processed/twitter/'
            ]
        }
    }
]

with DAG(
    dag_id='twitter_full_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Full ETL từ raw đến Redshift cho Twitter data',
    tags=['twitter', 'spark', 'redshift']
) as dag:

    start = DummyOperator(task_id='start_pipeline')

    # 🟡 Bước 1: Raw → Cleansed
    add_raw_to_cleansed = EmrAddStepsOperator(
        task_id='run_spark_raw_to_cleansed',
        job_flow_id='j-2T5432XTB1TJO',  # Thay bằng Cluster ID của bạn nếu đổi
        steps=SPARK_RAW_TO_CLEANSED,
        aws_conn_id='aws_default',
        region_name='ap-southeast-1'
    )

    wait_raw_to_cleansed = EmrStepSensor(
        task_id='wait_for_raw_to_cleansed',
        job_flow_id='j-2T5432XTB1TJO',
        step_id="{{ task_instance.xcom_pull(task_ids='run_spark_raw_to_cleansed', key='return_value')[0] }}",
        aws_conn_id='aws_default',
        region_name='ap-southeast-1'
    )

    # 🟡 Bước 2: Cleansed → Processed
    add_cleansed_to_processed = EmrAddStepsOperator(
        task_id='run_spark_cleansed_to_processed',
        job_flow_id='j-2T5432XTB1TJO',
        steps=SPARK_CLEANSED_TO_PROCESSED,
        aws_conn_id='aws_default',
        region_name='ap-southeast-1'
    )

    wait_cleansed_to_processed = EmrStepSensor(
        task_id='wait_for_cleansed_to_processed',
        job_flow_id='j-2T5432XTB1TJO',
        step_id="{{ task_instance.xcom_pull(task_ids='run_spark_cleansed_to_processed', key='return_value')[0] }}",
        aws_conn_id='aws_default',
        region_name='ap-southeast-1'
    )

    # 🟢 Bước 3: Load vào Redshift
    redshift_copy = RedshiftSQLOperator(
        task_id='load_to_redshift',
        sql="""
            COPY processed_tweets
            FROM 's3://social-media-data-tuananh/processed/twitter/'
            IAM_ROLE 'arn:aws:iam::318574063161:role/RedshiftS3Access'
            FORMAT AS PARQUET;
        """,
        redshift_conn_id='redshift_default'
    )

    end = DummyOperator(task_id='end_pipeline')

    # DAG flow
    start >> add_raw_to_cleansed >> wait_raw_to_cleansed
    wait_raw_to_cleansed >> add_cleansed_to_processed >> wait_cleansed_to_processed
    wait_cleansed_to_processed >> redshift_copy >> end