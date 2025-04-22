#https://www.askpython.com/python/examples/reddit-web-scraper-in-python
#https://praw.readthedocs.io/en/stable/index.html

import praw
import pandas as pd
import re
from praw.models import MoreComments

reddit_authorized = praw.Reddit(user_agent=" ",
                                client_id=" ",
                                client_secret=" ",
                                username=" ",
                                password=" ")

subreddit = reddit_authorized.subreddit("AskPH+buhaydigital+InternetPH+ShopeePH+Tech_Philippines")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s']", '', text)
    return text.strip()

posts_dict = {
    "Post ID": [],
    "Title": [],
    "Cleaned Title": [],
    "Description": [],
    "Cleaned Description": [],
    "Total Comments": []
}
comment_data = []

search_terms = ['shopee', 'shoppee', 'lazada', 'tiktok shop']
keywords = ['recommend', 'suggest', 'good', 'better', 'best', 'where to buy', 'lf', 'looking for']

unique_posts = set()

for term in search_terms:
    for keyword in keywords:
        query = f'({term}) ({keyword})'
        # Search posts from the past month
        posts = subreddit.search(query=query, time_filter='month', limit=None)

        for post in posts:
            # Skip posts without comments
            if post.num_comments == 0:
                continue

            if post.id in unique_posts:
                continue

            unique_posts.add(post.id)
            title = post.title
            post_id = post.id

            # Use the selftext as the description; if None, use an empty string
            description = post.selftext if post.selftext is not None else ""

            posts_dict["Post ID"].append(post_id)
            posts_dict["Title"].append(title)
            posts_dict["Cleaned Title"].append(clean_text(title))
            posts_dict["Description"].append(description)
            posts_dict["Cleaned Description"].append(clean_text(description) if description else "")
            posts_dict["Total Comments"].append(post.num_comments)

            # Process comments
            submission = reddit_authorized.submission(id=post_id)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if comment.author is None or (comment.author.name == "AutoModerator"):
                    continue
                if comment.body.strip().lower() in ['[deleted]', '[removed]']:
                    continue
                cleaned_comment = clean_text(comment.body)
                if cleaned_comment:
                    comment_data.append({
                        "Post ID": post_id,
                        "Original Comment": comment.body,
                        "Cleaned Comment": cleaned_comment
                    })

# Convert dictionaries to DataFrames and export as CSVs
posts_df = pd.DataFrame(posts_dict)
comments_df = pd.DataFrame(comment_data)

posts_df.to_csv("posts.csv", index=False)
comments_df.to_csv("comments.csv", index=False)

print("Number of posts extracted:", posts_df.shape[0])
print("Number of comments extracted:", comments_df.shape[0])