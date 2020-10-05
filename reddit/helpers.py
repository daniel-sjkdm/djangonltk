from dotenv import load_dotenv
from praw.models import MoreComments
import datetime
import json
import praw
import os
from django.conf import settings


DEVELOPMENT_MODE = False

if settings.DEBUG == True and DEVELOPMENT_MODE == True:
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    user_agent = os.getenv('USERAGENT')
else:
    client_id = os.environ.get("REDDIT_CLIENT_ID", None)
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", None)
    user_agent = os.environ.get("REDDIT_USERAGENT", None)


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


def get_readable_datetime(timestamp):
  return datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")


def get_posts(subreddit, write_json=False):
    posts = []

    for post in reddit.subreddit(subreddit).hot(limit=100):
        comments = []
        for comment in post.comments:
            if isinstance(comment, MoreComments):
                continue
            comments.append(comment.body)

        posts.append({
            "id": post.id, 
            "author": post.author.name,
            "subreddit": post.subreddit.display_name,
            "created": get_readable_datetime(post.created_utc),
            "distinguished": post.distinguished,
            "fullname": post.fullname,
            "downs": post.downs,
            "num_comments": post.num_comments,
            "title": post.title,
            "view_count": post.view_count,
            "ups": post.ups,
            "url": post.url,
            "comments": comments,
        })

    if write_json:

        if os.path.exists("posts.json"):
            with open("posts.json", "r") as f:
                json_posts = json.load(f)
                json_posts.extend(posts)
                with open("posts.json", "w") as f:
                    json.dump(json_posts, f, indent=4)
        else:
            with open("posts.json", "w") as f:
                json.dump(posts, f, indent=4)

    return posts


def get_redditors():
    redditors = []
    for redditor in reddit.redditors.popular(limit=100):
        redditors.append({
            "id": redditor.id,
            "name": redditor.display_name,
            "created": get_readable_datetime(redditor.created_utc),
            "description": redditor.description,
            "subcribers": redditor.subscribers
        })
    return redditors
