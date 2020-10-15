from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "username",
            "content",
            "tokens",
            "stems",
            "pos_tags",
            "lemma",
            "post"
        ]
        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "post_id",
            "title",
            "username",
            "ups",
            "created",
            "url",
            "sentiment"
        ]



class RedditCommentSerializer(serializers.Serializer):
    id = serializers.CharField()


class RedditPostSerializer(serializers.Serializer):
    id = serializers.CharField(max_length="6")
    title = serializers.CharField()
    username = serializers.CharField()
    subreddit = serializers.CharField()
    created = serializers.DateField(format="%Y-%m-%d %H:%M:%S")
    ups = serializers.IntegerField()
    num_comments = serializers.IntegerField()
    url = serializers.URLField()
    comments = serializers.JSONField()
    sentiment = serializers.IntegerField(read_only=True)