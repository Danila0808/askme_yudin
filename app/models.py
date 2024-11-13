from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default="primary")

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def best_questions(self):
        return self.annotate(likes_count=Count('likes')).order_by('-likes_count')

    def new_questions(self):
        return self.order_by('-created_at')

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField(null=False, max_length=5000)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, through='QuestionLike', related_name='liked_questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/question/{self.title}/"

    def get_likes_count(self):
        return self.likes.count()

    def is_popular(self):
        return self.get_likes_count() > 10

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(null=False, max_length=5000)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, through='AnswerLike', related_name='liked_answers')

    def __str__(self):
        return f"Answer by {self.author.username} on '{self.question.title}'"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} likes '{self.question.title}'"

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} likes an answer to '{self.answer.question.title}'"
