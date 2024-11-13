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

        # Создание пользователей и профилей
        users = [
            User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
            ) for _ in range(ratio)
        ]
        users = User.objects.bulk_create(users, batch_size=1000)

        profiles = [
            Profile(user=user, avatar=fake.image_url())
            for user in users
        ]
        Profile.objects.bulk_create(profiles, batch_size=1000)

        # Создание тегов
        colors = ["primary", "secondary", "success", "danger", "warning"]
        tags = [
            Tag(name=fake.word(), color=random.choice(colors))
            for _ in range(ratio)
        ]
        tags = Tag.objects.bulk_create(tags, batch_size=1000)

        # Создание вопросов
        questions = [
            Question(
                author=random.choice(users),
                title=fake.sentence(),
                text=fake.text(),
                created_at=timezone.now(),
            ) for _ in range(ratio * 10)
        ]
        questions = Question.objects.bulk_create(questions, batch_size=1000)

        # Присвоение тегов вопросам
        for question in questions:
            question.tags.set(random.sample(tags, min(3, len(tags))))

        # Создание ответов
        answers = [
            Answer(
                author=random.choice(users),
                question=random.choice(questions),
                text=fake.text(),
                is_accepted=random.choice([True, False]),
                created_at=timezone.now(),
            ) for _ in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers, batch_size=1000)

        # Создание лайков к вопросам
        question_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            if not any(l.user_id == user.id and l.question_id == question.id for l in question_likes):
                question_likes.append(QuestionLike(user=user, question=question))
        QuestionLike.objects.bulk_create(question_likes, batch_size=1000)

        # Создание лайков к ответам
        answer_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            if not any(l.user_id == user.id and l.answer_id == answer.id for l in answer_likes):
                answer_likes.append(AnswerLike(user=user, answer=answer))
        AnswerLike.objects.bulk_create(answer_likes, batch_size=1000)