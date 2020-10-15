from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer



class Index(View):
    def get(self, request):
        return render(request, "index.html")


def postsView(request):
    if request.method == "GET":
        posts = Post.objects.all()
        paginator = Paginator(posts, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj
        }
        return render(request, "posts.html", context=context)


class WriteYourOwn(View):
    """
        Write your own stuff and then it will be processed 
        with nltk tools
    """
    def get(self, request):
        return render(request, "write_your_own.html", context={})


class Chatbot(View):
    """
        Choose an nltk bot to chat with
    """
    def get(self, request):
        context = {
            "chatbots": [
                "eliza",
                "iesha",
                "rude",
                "suntsu",
                "zen"
            ]
        }
        return render(request, "chatbot.html", context=context)


class RedditSearch(View):
    """
        Use the search bar to fetch posts from reddit
    """
    def get(self, request):
        context = {
            "orderby": ["top", "hot", "new"],
            "limits": [10, 20, 50, 100]
        }
        return render(request, "search_reddit.html", context=context)