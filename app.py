# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HCri8TuzpU7vkjoZzhNQy8mlXcuPwHUD
"""

import streamlit as st

# Streamlit app interface
st.title("Social Media Sentiment Analyzer")

keyword = st.text_input("Enter a keyword to analyze:")
count = st.slider("Number of tweets to fetch", min_value=10, max_value=100, step=10, value=50)

if st.button("Analyze"):
    st.write(f"Fetching {count} tweets for keyword: '{keyword}'...")
    tweets_df = fetch_tweets(keyword, count)
    if tweets_df.empty:
        st.warning("No tweets found. Try a different keyword.")
    else:
        st.write("Analyzing sentiments...")
        tweets_df = analyze_sentiments(tweets_df)
        st.write("Sentiment Results:")
        st.dataframe(tweets_df)

        st.write("Visualization:")
        sentiment_counts = tweets_df["sentiment"].value_counts()
        st.bar_chart(sentiment_counts)