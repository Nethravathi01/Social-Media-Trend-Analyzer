import json
import pandas as pd
import csv
from googleapiclient.discovery import build

API_KEY = "AIzaSyBerJajnHyW0vywekOhliUMx_05Ff9WrNg"
youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="IN",
    maxResults=50
)
response = request.execute()
csv_filename = "youtube_trending.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Channel", "Views", "URL"])
    for video in response.get("items", []):
        title = video["snippet"]["title"]
        channel = video["snippet"]["channelTitle"]
        views = video["statistics"].get("viewCount", "0")
        video_id = video["id"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        writer.writerow([title, channel, views, url])
df = pd.read_csv(csv_filename)
df["Views"] = df["Views"].astype(int)
df_sorted = df.sort_values(by="Views", ascending=False).reset_index(drop=True)
df_sorted.to_csv("youtube_trending_cleaned.csv", index=False, encoding="utf-8", header=True)
print(df_sorted)



