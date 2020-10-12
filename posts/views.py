from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from reddit.helpers import get_posts



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



class ProcessData(View):
    """
        Process the data sent from the client by ajax
        and return all the parsed data
    """
    def post(self, request):
        if request.is_ajax():
            print(request.POST)
    


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


class RedditSearh(View):
    """
        Use the search bar to fetch posts from reddit
    """
    def get(self, request):
        context = {
            "orderby": ["top", "hot", "new"]
        }
        return render(request, "search_reddit.html", context=context)


'''



const alpha = {
  "a": 1,
  "b": 2,
  "c": 3,
  "d": 4,
  "e": 5,
  "f": 6,
  "g": 7,
  "h": 8,
  "i": 9,
  "j": 10,
  "k": 11,
  "l": 12,
  "m": 13,
  "n": 14,
  "o": 15,
  "p": 16,
  "q": 17,
  "r": 18,
  "s": 19,
  "t": 20,
  "u": 22,
  "v": 23,
  "w": 24,
  "x": 25,
  "y": 26,
  "z": 27,
}


function alphabetPosition(text) {
  return text.split('').map(char => isNaN(char)? alpha[char.toLowerCase()]).join(' ')
}
'''