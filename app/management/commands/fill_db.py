from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
import random
from faker import Faker

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        # Генерация пользователей
        for _ in range(ratio):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
            )
            Profile.objects.create(user=user, avatar=fake.image_url())

        # Генерация тегов
        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(name=fake.word())
            tags.append(tag)

        # Генерация вопросов
        for _ in range(ratio * 10):
            author = User.objects.order_by('?').first()  # Выбираем случайного пользователя
            question = Question.objects.create(
                author=author,
                title=fake.sentence(),
                text=fake.text(),
                created_at=timezone.now(),
            )
            question.tags.set(random.sample(tags, min(3, len(tags))))  # Присваиваем случайные теги

        # Генерация ответов
        for _ in range(ratio * 100):
            question = Question.objects.order_by('?').first()  # Выбираем случайный вопрос
            author = User.objects.order_by('?').first()  # Выбираем случайного пользователя
            answer = Answer.objects.create(
                author=author,
                question=question,
                text=fake.text(),
                is_accepted=random.choice([True, False]),
                created_at=timezone.now(),
            )

        # Генерация лайков для вопросов
        for _ in range(ratio * 200):
            user = User.objects.order_by('?').first()  # Выбираем случайного пользователя
            question = Question.objects.order_by('?').first()  # Выбираем случайный вопрос
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                QuestionLike.objects.create(user=user, question=question)

        # Генерация лайков для ответов
        for _ in range(ratio * 200):
            user = User.objects.order_by('?').first()  # Выбираем случайного пользователя
            answer = Answer.objects.order_by('?').first()  # Выбираем случайный ответ
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                AnswerLike.objects.create(user=user, answer=answer)
