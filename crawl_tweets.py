import tweepy
import json

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFo53AEAAAAAqC0zMuFjgCWTzU96nvn4aleI0AU%3DbefX0nKFo0VeF3Y8yuI9nHZHkixNNlpuBKxzcEAdtQ4boze4xH"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "data engineering lang:en -is:retweet"

tweets = client.search_recent_tweets(
    query=query,
    max_results=100,
    tweet_fields=["id", "text", "created_at", "public_metrics"]
)

with open("tweets_api.jsonl", "w") as f:
    for tweet in tweets.data:
        f.write(json.dumps(tweet.data) + "\n")

print("✅ Done")
