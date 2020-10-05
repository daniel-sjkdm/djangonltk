from django.urls import path
from . import views
from . import api

app_name = "posts"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts/", views.postsView, name="posts"),
    path("tell-me/", views.WriteYourOwn.as_view(), name="tell-me"),
    path("parse/", views.ProcessData.as_view(), name="parse"),
    path("chatbot/", views.Chatbot.as_view(), name="chatbot"),
    path("api/posts/all", api.getPosts, name="api-all-posts"), 
    path("api/posts/<int:id>", api.detailPost, name="api-detail-post"),
    path("api/posts/create", api.createPost, name="api-create-post"),
    path("api/posts/search", api.searchPost, name="api-search-post"),
    path("api/posts/parse", api.parsePost, name="api-parse-post"),
    path("api/comments/create", api.createComment, name="api-create-comment"),
    path("api/comments/<int:post_id>", api.getComments, name="api-comments-post-id"),
    path("api/chatbot", api.chatBot, name="api-chatbot"),
]
