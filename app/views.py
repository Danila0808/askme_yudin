from math import ceil

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from app.forms import LoginForm, ProfileForm, AskForm, AnswerForm
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
from django.db.models import Count
from django.contrib import auth
from django.urls import reverse

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
    questions = Question.objects.new_questions()  # Получаем все вопросы из базы данных
    page_num, questions_paginated, num_pages = paginate(questions, request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'Askme_yudin',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,
            'questions': questions_paginated,
            'category': 'new',
        },
    )

def hot(request):
    questions = Question.objects.best_questions()
    page_num, questions_paginated, num_pages = paginate(questions, request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'Askme_yudin - Hot',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,
            'questions': questions_paginated,
            'category': 'top',
        },
    )

def tag(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()
    questions_with_tag = Question.objects.filter(tags=tag)
    page_num, questions_paginated, num_pages = paginate(questions_with_tag, request)
    return render(
        request,
        'tag.html',
        {
            'page_title': f'Askme_yudin - Tag: {tag_name}',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': request.user.is_authenticated,
            'tag': tag_name,
            'questions': questions_paginated,
        },
    )

@login_required
def ask(request):
    form = AskForm
    if request.method=="POST":
        form = AskForm(request.POST)
        if form.is_valid():
            id = form.save(request.user)
            return redirect(reverse("question", kwargs={"question_id": id}) + "#answer-form")
    return render(
        request,
        'ask.html',
        {
            'page_title': 'Askme_yudin - Ask',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'is_logged_in': request.user.is_authenticated,
            'form': form,
        },
    )

def question(request, question_id):
    question_data = Question.objects.filter(id=question_id).first()
    answers = Answer.objects.filter(question=question_data)
    form = AnswerForm
    return render(
        request,
        'question.html',
        {
            'page_title': 'Askme_yudin - Question',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'is_logged_in': request.user.is_authenticated,
            'question': question_data,
            'answers': answers,
            'question_id': question_id,
            'answer_form': form
        },
    )

@login_required
def settings(request):
    user = request.user
    return render(
        request,
        'settings.html',
        {
            'page_title': 'Askme_yudin - Settings',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'is_logged_in': request.user.is_authenticated,
            'username': user.username,
            'email': user.email,
        },
    )

def signup(request):
    form = ProfileForm
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            login(request)
            # user = form.save(commit=False)
            # user.set_password(form.cleaned_data['password'])
            # user.save()
            #
            # Profile.objects.create(
            #     user=user,
            #     avatar = form.cleaned_data.get('picture')
            # )
            return redirect(reverse('index'))
    return render(
        request,
        'signup.html',
        {
            'page_title': 'Askme_yudin - Sign Up',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'is_logged_in': request.user.is_authenticated,
            'form': form
        },
    )

def login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                else:
                    return redirect(reverse('index'))
            form.add_error('username', 'Invalid username or password')
            form.add_error('password', 'Invalid username or password')

    return render(
        request,
        'login.html',
        {
            'page_title': 'Askme_yudin - Log In',
            'popular_tags': Tag.objects.all(),  # Получаем все теги
            'best_members': User.objects.all().order_by('-date_joined')[:3],
            'is_logged_in': request.user.is_authenticated,
            'form': form,
        },
    )

@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

@login_required
def answer(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            question_id = request.POST.get('question_id')
            print(question_id)
            question = Question.objects.get(id=question_id)
            form.save(request.user, question)
            return redirect(reverse("question", kwargs={"question_id": question_id}) + "#answer-form")