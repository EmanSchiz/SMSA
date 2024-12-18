# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rLq5mpeMIoK0lK8h3x4PEfqnDqyy13y5
"""

# Import required libraries
import streamlit as st
from transformers import pipeline
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration for Streamlit
st.set_page_config(
    page_title="Social Media Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)

# Load pre-trained sentiment analysis model from Hugging Face
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

sentiment_analyzer = load_sentiment_model()

# Twitter API authentication function
def authenticate_twitter_api():
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOVgxAEAAAAAgv9p%2F7mxuSraiYZJ7m1E%2BGRFpmk%3DcMWRGfJGcBCrJlBMnCekcLAgsOSkfj8ELkEaVx7lERBiN9cMTK"  # Replace with your actual bearer token
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client

twitter_client = authenticate_twitter_api()

# Function to fetch tweets based on keyword
def fetch_tweets(keyword, count=50):
    try:
        tweets = twitter_client.search_recent_tweets(
            query=keyword,
            max_results=count,
            tweet_fields=["text", "created_at"]
        )
        if tweets.data:
            data = [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets.data]
            return pd.DataFrame(data)
        else:
            st.warning("No tweets found for the given keyword.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching tweets: {e}")
        return pd.DataFrame()

# Function to analyze sentiments
def analyze_sentiments(dataframe):
    sentiments = []
    for text in dataframe["text"]:
        try:
            result = sentiment_analyzer(text)[0]
            sentiments.append(result["label"])
        except Exception as e:
            sentiments.append("Error")
    dataframe["sentiment"] = sentiments
    return dataframe

# Function to visualize sentiment results
def visualize_sentiments(dataframe):
    sentiment_counts = dataframe["sentiment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis", ax=ax)
    ax.set_title("Sentiment Distribution", fontsize=16)
    ax.set_xlabel("Sentiment", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    return fig

# Streamlit interface
st.title("📊 Social Media Sentiment Analyzer")
st.markdown("Analyze public sentiment on social media by entering a keyword or hashtag.")

# Input section
keyword = st.text_input("Enter a keyword or hashtag:", placeholder="e.g., #AI, OpenAI, your product name")
tweet_count = st.slider("Number of tweets to analyze:", min_value=10, max_value=100, value=50, step=10)

# Button to fetch and analyze tweets
if st.button("Analyze Sentiment"):
    if keyword:
        with st.spinner("Fetching tweets and analyzing sentiment..."):
            # Fetch tweets
            tweets_df = fetch_tweets(keyword, count=tweet_count)

            if not tweets_df.empty:
                # Analyze sentiments
                analyzed_df = analyze_sentiments(tweets_df)

                # Display data
                st.subheader("Raw Data")
                st.dataframe(analyzed_df, use_container_width=True)

                # Visualization
                st.subheader("Sentiment Distribution")
                sentiment_chart = visualize_sentiments(analyzed_df)
                st.pyplot(sentiment_chart)
    else:
        st.warning("Please enter a keyword to analyze.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using [Streamlit](https://streamlit.io/) and [Hugging Face](https://huggingface.co/).")
