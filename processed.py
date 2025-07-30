from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, expr
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: spark-submit process.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]    # cleansed
    output_path = sys.argv[2]   # processed

    spark = SparkSession.builder.appName("ProcessToMetrics").getOrCreate()

    try:
        df = spark.read.parquet(input_path)

        # Tính thêm chỉ số
        df_processed = (
            df
            .withColumn("date", to_date("created_at"))
            .withColumn("engagement_score", expr("""
                (like_count + reply_count + retweet_count + quote_count) 
                / nullif(impression_count, 0)
            """))
            .select(
                "id", "author_id", "date", "text", "source",    
                "like_count", "reply_count", "retweet_count", "quote_count",
                "bookmark_count", "impression_count", "engagement_score"
            )
        )

        df_processed.write \
            .mode("overwrite") \
            .parquet(output_path)

        print("✅ Done writing processed data")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()