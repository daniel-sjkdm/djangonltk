"""
    Post will be created by fetching data from the reddit api
    about some topics: China
"""

import os
import sys
import json
import requests
from helpers import get_posts



create_post_url = "http://127.0.0.1:8000/api/posts/create"
create_comments_url = "http://127.0.0.1:8000/api/comments/create"

def get_auth_headers():
    return {
        "Authorization": "Basic admin:admin"
    }


# datetime.strptime(ps[0].get("created"), "%d/%m/%Y %H:%M:%S")

def create_posts(posts):
    data = []

    for post in posts:

        data = {
            "username": post["author"],
            "ups": post["ups"],
            "downs": post["downs"],
            "subreddit": post["subreddit"],
            "title": post["title"],
            "url": post["url"]
        }

        r = requests.post(create_post_url, data=data)

        for comment in post["comments"]:
            data = {
                "comment": comment,
                "title": post["title"]
            }
            r = requests.post(create_comments_url, data=data)


if __name__ == "__main__":
    posts = get_posts("Python", write_json=True)
    create_posts(posts)