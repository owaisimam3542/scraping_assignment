import requests
import pandas as pd
from datetime import datetime


#url = "https://www.reddit.com/search.json?q=cricket"
url="https://www.reddit.com/search.json?q=nike+shoes"
#url="https://www.reddit.com/r/Python/top.json?limit=30"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
data = response.json()
posts = []
for post in data['data']['children']:
    post_data = post['data']
    title = post_data['title']
    description = post_data.get('selftext', 'No description')
    author = post_data.get('author', 'Unknown')
    image = post_data['url'] if post_data['url'].endswith(('.jpg', '.png')) else post_data.get('thumbnail', "No image")
    video = "No video"
    if post_data.get('media') and post_data['media'].get('reddit_video'):
        video = post_data['media']['reddit_video'].get('fallback_url', 'No video')
    post_timestamp = post_data.get('created_utc', 0)
    post_datetime = datetime.utcfromtimestamp(post_timestamp).strftime(
        '%Y-%m-%d %H:%M:%S') if post_timestamp else "No date available"
    user_url = f"https://www.reddit.com/user/{author}/about.json"
    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json().get('data', {})
        bio = user_data.get('subreddit', {}).get('public_description', "No bio available")
        join_timestamp = user_data.get('created_utc', 0)
        join_date = datetime.utcfromtimestamp(join_timestamp).strftime(
            '%Y-%m-%d') if join_timestamp else "No join date available"
    else:
        bio = "No bio available"
        join_date = "No join date available"
    posts.append({
        "Title": title,
        "Description": description,
        "Author": author,
        "Bio": bio,
        "Join Date": join_date,
        "Post Date & Time (UTC)": post_datetime,
        "Image URL": image,
        "Video URL": video
    })
df = pd.DataFrame(posts)
df.to_excel("reddit_posts_test_ct.xlsx", index=False, engine="openpyxl")

print("Data saved successfully to reddit_posts.xlsx")
