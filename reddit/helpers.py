from dotenv import load_dotenv
from praw.models import MoreComments
import datetime
import json
import praw
import os
from pprint import pprint
from posts.data_processing import (
    get_sentiment_score
)


def get_readable_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def get_reddit_client():
    load_dotenv()
    return praw.Reddit(
        client_id=os.environ.get("CLIENT_ID", None),
        client_secret=os.environ.get("CLIENT_SECRET", None),
        user_agent=os.environ.get("USERAGENT", None)
    )


def search_for_subreddit(subreddit, kind, limit):
    posts = []
    reddit = get_reddit_client()

    if kind == "top":
        try:
            reddit_posts = reddit.subreddit(subreddit).top(limit=limit)
            for post in reddit_posts:
                comments = {}
                for i, comment in enumerate(post.comments):
                    if isinstance(comment, MoreComments):
                        continue
                    body = comment.body
                    comments[i] = {
                        "body": body,
                        "sentiment": get_sentiment_score(body)
                    }

                posts.append({
                    "id": post.id,
                    "username": post.author.name,
                    "subreddit": post.subreddit.display_name,
                    "created": get_readable_datetime(post.created_utc),
                    "ups": post.ups, 
                    "num_comments": post.num_comments,
                    "title": post.title,
                    "url": post.url,
                    "comments": comments,
                    "sentiment": get_sentiment_score(post.title)
                })

        except:
            pass
    
    elif kind == "hot":
        try:
            reddit_posts = reddit.subreddit(subreddit).hot(limit=limit)
            for post in reddit_posts:
                comments = {}
                for i, comment in enumerate(post.comments):
                    if isinstance(comment, MoreComments):
                        continue
                    comments[i] = comment.body

                posts.append({
                    "id": post.id,
                    "author": post.author.name,
                    "subreddit": post.subreddit.display_name,
                    "created": get_readable_datetime(post.created_utc),
                    "ups": post.ups, 
                    "downs": post.downs,
                    "num_comments": post.num_comments,
                    "title": post.title,
                    "url": post.url
                })  

        except: 
            pass

    elif kind == "new":
        try:
            reddit_posts = reddit.subreddit(subreddit).new(limit=limit)
            for post in reddit_posts:
                comments = {}
                for i, comment in enumerate(post.comments):
                    if isinstance(comment, MoreComments):
                        continue
                    comments[i] = comment.body

                posts.append({
                    "id": post.id,
                    "author": post.author.name,
                    "subreddit": post.subreddit.display_name,
                    "created": get_readable_datetime(post.created_utc),
                    "ups": post.ups, 
                    "downs": post.downs,
                    "num_comments": post.num_comments,
                    "title": post.title,
                    "url": post.url
                })  
                
        except:
            pass
    
    return posts