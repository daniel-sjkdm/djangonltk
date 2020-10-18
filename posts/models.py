from django.db import models
from .data_processing import tokenize_words, stem_sentence, pos_tags_sentence, lemmatize_sentence, remove_stop_words


class Post(models.Model):
    post_id = models.CharField(max_length=6, unique=True) 
    title = models.CharField(max_length=300, null=False, unique=True)
    username = models.CharField(max_length=50, null=False)
    ups = models.IntegerField(default=0, blank=True)
    subreddit = models.CharField(max_length=20, null=False, default="")
    created = models.DateTimeField()
    num_comments = models.PositiveSmallIntegerField(default=0)
    url = models.URLField(verbose_name="post_url", null=False)
    sentiment = models.CharField(max_length=10, null=False)

    class Meta:
        order_with_respect_to = "created"

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    tokens = models.TextField(null=True)
    stems = models.JSONField(verbose_name="post stems", null=True)
    pos_tags = models.JSONField(verbose_name="post part of speech tags", null=True)
    lemma = models.JSONField(verbose_name="post lemma", null=True)

    def __str__(self):
        return f"Comment for post {self.post}"

    def save(self, *args, **kwargs):
        tokens = tokenize_words(self.content)
        stems = stem_sentence(tokens)
        pos_tags = pos_tags_sentence(tokens)
        lemma = lemmatize_sentence(tokens)
        self.tokens = "\t".join(tokens)
        self.stems = stems
        self.pos_tags = pos_tags
        self.lemma = lemma
        super(Comment, self).save()