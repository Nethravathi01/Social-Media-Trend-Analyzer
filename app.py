import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("youtube_trending_cleaned.csv")

st.sidebar.header("Filter Options")
selected_channel = st.sidebar.selectbox("Select Channel", ["All"] + list(df['Channel'].unique()))
min_views = st.sidebar.slider("Minimum Views", min_value=int(df['Views'].min()), max_value=int(df['Views'].max()), value=int(df['Views'].min()))
search_query = st.sidebar.text_input("Search Video Title")

filtered_df = df.copy()
if selected_channel != "All":
    filtered_df = filtered_df[filtered_df['Channel'] == selected_channel]
filtered_df = filtered_df[filtered_df['Views'] >= min_views]
if search_query:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(search_query, case=False, na=False)]

st.title("YouTube Trending Videos Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Videos", len(filtered_df))
col2.metric("Total Views", f"{filtered_df['Views'].sum():,}")
col3.metric("Average Views per Video", f"{filtered_df['Views'].mean():,.0f}")

st.subheader("Most Viral Video")
most_viral = filtered_df.loc[filtered_df['Views'].idxmax()]
st.write(f"{most_viral['Title']} - {most_viral['Views']:,} views")

st.subheader("Views Distribution")
fig_views = px.histogram(filtered_df, x='Views', nbins=20, title='Views Distribution')
st.plotly_chart(fig_views)

st.subheader("Video Count by Channel")
channel_count = filtered_df['Channel'].value_counts().reset_index()
channel_count.columns = ['Channel', 'Count']
fig_count = px.bar(channel_count, x='Channel', y='Count', title='Video Count by Channel')
st.plotly_chart(fig_count)

st.subheader("Trending Channels")
trending_channels = df.groupby('Channel').agg({'Views': 'sum', 'Title': 'count'}).rename(columns={'Title': 'Video Count'}).reset_index()
trending_channels = trending_channels.sort_values(by='Views', ascending=False).head(10)
st.dataframe(trending_channels)



