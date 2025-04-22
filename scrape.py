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


# subreddits can be combined with a + (i.e. "AskPh+Philippines")
subreddit = reddit_authorized.subreddit("AskPH+buhaydigital+InternetPH+Tech_Philippines")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s']", '', text)
    return text.strip()

posts_dict = {"Post ID": [], "Title": [], "Cleaned Title": [], "Total Comments": []}
comment_data = []

# by default time_filter is set to "all", otherwise: "day", "hour", "month", "week", "year"
# posts = subreddit.controversial()
# posts = subreddit.gilded() # <- gilded are the awarded posts, no time filter
# posts = subreddit.hot() # <- no time filter
# posts = subreddit.new() # <- no time filter
# posts = subreddit.top("month")
posts = subreddit.search(query='(shopee OR shoppee OR lazada) (recommend OR recommendation OR recommendations OR suggest OR best OR "where to buy")', limit=None)

for post in posts:
    title = post.title
    post_id = post.id
    posts_dict["Post ID"].append(post_id)
    posts_dict["Title"].append(title)
    posts_dict["Cleaned Title"].append(clean_text(title))
    posts_dict["Total Comments"].append(post.num_comments)

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

posts_df = pd.DataFrame(posts_dict)
comments_df = pd.DataFrame(comment_data)

posts_df.to_csv("posts.csv", index=False)
comments_df.to_csv("comments.csv", index=False)

print("Number of posts extracted:", posts_df.shape[0])
print("Number of comments extracted:", comments_df.shape[0])