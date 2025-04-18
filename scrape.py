#https://www.askpython.com/python/examples/reddit-web-scraper-in-python
#https://praw.readthedocs.io/en/stable/index.html

import praw
import pandas as pd
from praw.models import MoreComments

reddit_authorized = praw.Reddit(client_id="",
                                client_secret=" ",
                                user_agent=" ",
                                username="",
                                password="")


# subreddits can be combined with a + (i.e. "AskPh+Philippines")
subreddit = reddit_authorized.subreddit("AskPH")

# by default time_filter is set to "all", otherwise: "day", "hour", "month", "week", "year"
# posts = subreddit.controversial()
# posts = subreddit.gilded() # <- gilded are the awarded posts, no time filter
# posts = subreddit.hot() # <- no time filter
# posts = subreddit.new() # <- no time filter
posts = subreddit.search(query="online",time_filter="month") 
#posts = subreddit.top("month")
 
posts_dict = {"Title": [],
              "Total Comments": [],
              "Post URL": []}
 
for post in posts:
    posts_dict["Title"].append(post.title)
    posts_dict["Total Comments"].append(post.num_comments)
    posts_dict["Post URL"].append(post.url)
 
top_posts_month = pd.DataFrame(posts_dict)
 
print("Number of posts extracted : ",top_posts_month.shape[0])
top_posts_month.head()

# for only first post, can all loop for below
url = top_posts_month['Post URL'][0]
submission = reddit_authorized.submission(url=url)

# comment extract
post_comments = []
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
    post_comments.append(comment.body)
 
comments_df = pd.DataFrame(post_comments, columns=['comment'])
 
print("Number of Comments : ",comments_df.shape[0])
comments_df.head()

#top_posts_month.to_csv("posts_askph.csv", index=False)
#comments_df.to_csv("comments_askph.csv", index=False)