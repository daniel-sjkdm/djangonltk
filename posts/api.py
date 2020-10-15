from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, RedditPostSerializer
from .data_processing import (
    tokenize_words, 
    stem_sentence, 
    pos_tags_sentence, 
    lemmatize_sentence, 
    remove_stop_words, 
    chat_bot, 
    get_sentiment_score,
    random_tweet
)
from reddit.helpers import search_for_subreddit



bot_name = "rude"
bot = chat_bot(bot_name)



@api_view(["GET", "POST"])
def posts(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK)  

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def posts_detail(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getComments(request, post_id):
    if request.method == "GET":
        comments = Comment.objects.filter(post__id__iexact=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["POST"])
def createComment(request):
    if request.method == "POST":
        post = get_object_or_404(Post, title=request.data.get("title"))
        data = {
            "content": request.data.get("comment"),
            "post": post.id
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def searchPost(request):
    if request.method == "GET":
        title = request.data.get("title")
        post = get_object_or_404(Post, title=title)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET", "POST"])
def chatBot(request):
    """
        Interact with the existing NLTK chatbots
    """
    global bot, bot_name
    if request.method == "GET":
        bot_name = request.query_params.get("bot_name").strip()
        bot = chat_bot(bot_name)
        return Response({"message": "Bot name changed"}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        human_message = request.data.get("human_message")
        bot_message = bot.respond(human_message)
        return Response({"data": bot_message, "bot_name": bot_name}, status=status.HTTP_200_OK)


@api_view(["POST"])
def parse_post(request):
    sentence = request.data.get("tms")
    sentence_tokens = tokenize_words(sentence)
    sentence_stems = stem_sentence(sentence_tokens)
    sentence_stems = [ ": ".join(item) for item in stem_sentence(sentence_tokens).items() ]
    sentence_pos = [ ": ".join(item) for item in pos_tags_sentence(sentence_tokens).items() ]
    sentence_lemma = lemmatize_sentence(sentence_tokens)
    sentence_no_stop_words = remove_stop_words(sentence)
    sentence_sentiment = get_sentiment_score(" ".join(sentence_no_stop_words))
    return Response({
        "sentence_tokens": sentence_tokens,
        "sentence_stems": sentence_stems,
        "sentence_pos": sentence_pos,
        "sentence_lemma": sentence_lemma,
        "sentence_no_stop_words": sentence_no_stop_words,
        "sentence_sentiment": sentence_sentiment
    }, status=status.HTTP_200_OK)



@api_view(["GET"])
def search_reddit_api(request):
    """
        Searches for a given subreddit and type.
    """
    if request.method == "GET":
        subreddit = request.GET.get("subreddit")
        kind = request.GET.get("kind")
        limit = int(request.GET.get("limit"))
        posts = search_for_subreddit(subreddit, kind, limit)
        serializer = RedditPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_random_tweet(request):
    if request.method == "GET":
        tweet = random_tweet()
        return Response({"tweet": tweet}, status=status.HTTP_200_OK)