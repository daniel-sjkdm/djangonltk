from django.urls import path
from . import views
from . import api

app_name = "posts"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts", views.postsView, name="posts"),
    path("tell-me", views.WriteYourOwn.as_view(), name="tell-me"),
=    path("chatbot", views.Chatbot.as_view(), name="chatbot"),
    path("reddit", views.RedditSearch.as_view(), name="reddit"),
    path("api/posts", api.posts, name="api-posts"), 
    path("api/posts/<int:id>", api.posts_detail, name="api-detail-post"),
    path("api/posts/search", api.searchPost, name="api-search-post"),
    path("api/posts/parse", api.parse_post, name="api-parse-post"),
    path("api/reddit/search", api.search_reddit_api, name="api-reddit-post"),
    path("api/comments/create", api.createComment, name="api-create-comment"),
    path("api/comments/<int:post_id>", api.getComments, name="api-comments-post-id"),
    path("api/chatbot", api.chatBot, name="api-chatbot"),
    path("api/tweet/random", api.get_random_tweet, name="api-random-tweet")
]