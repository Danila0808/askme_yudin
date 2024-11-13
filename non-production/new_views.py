from math import ceil
from django.shortcuts import render
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike

def paginate(items, request, per_page=5):
    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    max_pages = ceil(len(items) / per_page)
    current_page = max(1, min(current_page, max_pages))
    paginated_items = items[(current_page - 1) * per_page: current_page * per_page]
    return current_page, paginated_items, max_pages

def index(request):
    questions = Question.objects.all()  # Получаем все вопросы из базы данных
    page_num, questions_paginated, num_pages = paginate(questions, request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'Askme_yudin',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,  # Проверка, авторизован ли пользователь
            'questions': questions_paginated,
            'category': 'new',
        },
    )

def hot(request):
    questions = Question.objects.all().order_by('-created_at')  # Получаем все вопросы, отсортированные по времени создания
    page_num, questions_paginated, num_pages = paginate(questions, request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'Askme_yudin - Hot',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,
            'questions': questions_paginated,
            'category': 'top',
        },
    )

def tag(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()  # Получаем тег по имени
    questions_with_tag = Question.objects.filter(tags=tag)  # Получаем все вопросы с этим тегом
    page_num, questions_paginated, num_pages = paginate(questions_with_tag, request)
    return render(
        request,
        'tag.html',
        {
            'page_title': f'Askme_yudin - Tag: {tag_name}',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,
            'tag': tag_name,
            'questions': questions_paginated,
        },
    )

def ask(request):
    return render(
        request,
        'ask.html',
        {
            'page_title': 'Askme_yudin - Ask',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'is_logged_in': request.user.is_authenticated,
        },
    )

def question(request, question_id):
    question_data = Question.objects.filter(id=question_id).first()  # Получаем конкретный вопрос по ID
    answers = Answer.objects.filter(question=question_data)  # Получаем все ответы на этот вопрос
    return render(
        request,
        'question.html',
        {
            'page_title': 'Askme_yudin - Question',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'is_logged_in': request.user.is_authenticated,
            'question': question_data,
            'answers': answers,
        },
    )

def settings(request):
    return render(
        request,
        'settings.html',
        {
            'page_title': 'Askme_yudin - Settings',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'is_logged_in': request.user.is_authenticated,
        },
    )

def signup(request):
    return render(
        request,
        'signup.html',
        {
            'page_title': 'Askme_yudin - Sign Up',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'is_logged_in': request.user.is_authenticated,
        },
    )

def login(request):
    return render(
        request,
        'login.html',
        {
            'page_title': 'Askme_yudin - Log In',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],  # Получаем 3 лучших пользователей по дате регистрации
            'is_logged_in': request.user.is_authenticated,
        },
    )
