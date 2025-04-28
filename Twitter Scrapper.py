import tweepy
import pandas as pd
import time

# Twitter API credentials
BEARER_TOKEN = ("AAAAAAAAAAAAAAAAAAAAAPCS0wEAAAAAv1CY2FpiG3PHIST8ORrPXmIYChg%3DLzjSdoWat42CCHJQHmJ2oIV7VsfhxLHfEUmhv5ClJgO1bzgQoE")


# Initialize Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)


# Your Twitter username (without @)
username = "edmondweb_23"

# Get user ID from username
user = client.get_user(username=username)
user_id = user.data.id

# Collect tweets
tweets = []

# Use a paginator to fetch tweets in batches
paginator = tweepy.Paginator(
    client.get_users_tweets,
    id=user_id,
    tweet_fields=['created_at', 'text', 'public_metrics'],
    max_results=100  # Max per request
)

# Fetch tweets page by page
for tweet_page in paginator:
    if tweet_page.data:
        for tweet in tweet_page.data:
            tweets.append({
                "Tweet ID": tweet.id,
                "Created At": tweet.created_at,
                "Text": tweet.text,
                "Likes": tweet.public_metrics['like_count'],
                "Retweets": tweet.public_metrics['retweet_count'],
                "Replies": tweet.public_metrics['reply_count'],
                "Quotes": tweet.public_metrics['quote_count']
            })
        time.sleep(1)  # Add delay to avoid hitting rate limits

# Save collected tweets to a CSV file
df = pd.DataFrame(tweets)
df.to_csv('my_tweets.csv', index=False, encoding='utf-8-sig')

print(f"Successfully saved {len(df)} tweets to 'my_tweets.csv'.")
