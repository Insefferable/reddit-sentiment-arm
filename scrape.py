#https://www.askpython.com/python/examples/reddit-web-scraper-in-python
#https://praw.readthedocs.io/en/stable/index.html

import praw
import pandas as pd
from praw.models import MoreComments

reddit_authorized = praw.Reddit(user_agent="",
                                client_id="",
                                client_secret="",
                                username="",
                                password="")


# subreddits can be combined with a + (i.e. "AskPh+Philippines")
subreddit = reddit_authorized.subreddit("AskPH")

# by default time_filter is set to "all", otherwise: "day", "hour", "month", "week", "year"
# posts = subreddit.controversial()
# posts = subreddit.gilded() # <- gilded are the awarded posts, no time filter
# posts = subreddit.hot() # <- no time filter
# posts = subreddit.new() # <- no time filter
posts = subreddit.search(query="Shopee") 
#posts = subreddit.top("month")
 
posts_dict = {"Title": [],
              "Total Comments": [],
              "Post URL": []}
 
for post in posts:
    posts_dict["Title"].append(post.title)
    posts_dict["Total Comments"].append(post.num_comments)
    posts_dict["Post URL"].append(post.url)
 
posts_month = pd.DataFrame(posts_dict)
 
print("Number of posts extracted : ",posts_month.shape[0])
#posts_month.head()

all_comments = []

for url in posts_month['Post URL']:
    submission = reddit_authorized.submission(url=url)
    
    post_comments = []
    for comment in submission.comments:
        if isinstance(comment, MoreComments):
            continue
        post_comments.append(comment.body)
    
    # Optionally add a reference to the post URL
    for c in post_comments:
        all_comments.append({'Post URL': url, 'comment': c})

# Create DataFrame from all comments
comments_df = pd.DataFrame(all_comments)
 
print("Number of Comments : ",comments_df.shape[0])
#comments_df.head()

posts_month.to_csv("posts_askph.csv", index=False)
comments_df.to_csv("comments_askph.csv", index=False)