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
            "id",
            "title",
            "username",
            "ups",
            "downs",
            "created",
            "url"
        ]