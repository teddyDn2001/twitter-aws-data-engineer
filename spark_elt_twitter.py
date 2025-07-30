from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import StructType, StringType, StructField, IntegerType, ArrayType
import sys

def main():
    if len(sys.argv) != 3:
        print("❌ Usage: spark-submit script.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]    
    output_path = sys.argv[2]   

    spark = SparkSession.builder \
        .appName("TestTwitterCleansedOutput") \
        .getOrCreate()

    try:
        # === SCHEMA CHUẨN ===
        public_metrics_schema = StructType([
            StructField("retweet_count", IntegerType(), True),
            StructField("reply_count", IntegerType(), True),
            StructField("like_count", IntegerType(), True),
            StructField("quote_count", IntegerType(), True),
            StructField("bookmark_count", IntegerType(), True),
            StructField("impression_count", IntegerType(), True)
        ])

        schema = StructType([
            StructField("id", StringType(), True),
            StructField("created_at", StringType(), True),
            StructField("text", StringType(), True),
            StructField("author_id", StringType(), True),
            StructField("lang", StringType(), True),
            StructField("source", StringType(), True),
            StructField("public_metrics", public_metrics_schema, True),
            StructField("edit_history_tweet_ids", ArrayType(StringType()), True)
        ])

        # === ĐỌC FILE RAW ===
        df_raw = spark.read.json(input_path, schema=schema)
        print(f"✅ Raw rows count: {df_raw.count()}")
        df_raw.show(3)
        df_raw.printSchema()

        # === CLEANED DATA ===
        df_cleaned = (
            df_raw
            .dropna(subset=["id", "created_at", "text"])
            .withColumn("created_at", to_timestamp("created_at"))
            .select(
                "id", "created_at", "author_id", "text", "source",
                col("public_metrics.retweet_count").alias("retweet_count"),
                col("public_metrics.reply_count").alias("reply_count"),
                col("public_metrics.like_count").alias("like_count"),
                col("public_metrics.quote_count").alias("quote_count"),
                col("public_metrics.bookmark_count").alias("bookmark_count"),
                col("public_metrics.impression_count").alias("impression_count"),
            )
        )

        print(f"✅ Cleaned row count: {df_cleaned.count()}")
        df_cleaned.show(5)
        df_cleaned.groupBy("author_id").count().show()

        # === GHI FILE PARQUET KHÔNG PARTITION ===
        df_cleaned.write \
            .mode("overwrite") \
            .parquet(output_path)

        print(f"✅ ✅ Successfully wrote cleaned data to: {output_path}")

    except Exception as e:
        print(f"❌ ERROR during processing: {e}")
        sys.exit(1)

    finally:
        spark.stop()

if __name__ == "__main__":
    main()