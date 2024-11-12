import random
import string
from math import ceil
from django.shortcuts import render

COLORS = ["primary", "secondary", "success", "danger", "warning"]

def generate_text(word_count):
    words = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7))) for _ in range(word_count)]
    return ' '.join(words)

QUESTIONS = [
    {
        'id': idx,
        'title': f"Question Title {random.randint(1, 23)}",
        'text': generate_text(idx + 3),
        'answer_count': random.randint(0, 10),
        'tags': [[f"tag{tag_idx}", COLORS[tag_idx % len(COLORS)]] for tag_idx in range(random.randint(1, 4))],
        'likes': random.randint(1, 100),
    }
    for idx in range(1, 23)
]

ANSWERS = [
    {
        'id': idx,
        'text': generate_text(idx + 5),
        'likes': random.randint(0, 50),
        'is_correct': (idx == 1),
    }
    for idx in range(1, 5)
]

POPULAR_TAGS = [[f"tag{idx}", COLORS[idx % len(COLORS)]] for idx in range(1, 10)]

BEST_MEMBERS = [f"member{random.choice(string.ascii_uppercase)}{random.randint(1, 20)}" for _ in range(3)]

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
    page_num, questions, num_pages = paginate(QUESTIONS, request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'AskPupkin',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': False,
            'questions': questions,
            'category': 'new',
        },
    )


def hot(request):
    page_num, questions, num_pages = paginate(list(reversed(QUESTIONS)), request)
    return render(
        request,
        'index.html',
        {
            'page_title': 'AskPupkin - Hot',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': True,
            'questions': questions,
            'category': 'top',
        },
    )


def tag(request, tag_name):
    questions_with_tag = [question for question in QUESTIONS if any(tag[0] == tag_name for tag in question['tags'])]
    page_num, questions, num_pages = paginate(questions_with_tag, request)
    return render(
        request,
        'tag.html',
        {
            'page_title': f'AskPupkin - Tag: {tag_name}',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'page': page_num,
            'num_pages': num_pages,
            'is_logged_in': True,
            'tag': tag_name,
            'questions': questions,
        },
    )


def ask(request):
    return render(
        request,
        'ask.html',
        {
            'page_title': 'AskPupkin - Ask',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'is_logged_in': True,
        },
    )


def question(request, question_id):
    question_data = next((q for q in QUESTIONS if q['id'] == question_id), None)
    return render(
        request,
        'question.html',
        {
            'page_title': 'AskPupkin - Question',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'is_logged_in': True,
            'question': question_data,
            'answers': ANSWERS,
        },
    )


def settings(request):
    return render(
        request,
        'settings.html',
        {
            'page_title': 'AskPupkin - Settings',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'is_logged_in': True,
        },
    )


def signup(request):
    return render(
        request,
        'signup.html',
        {
            'page_title': 'AskPupkin - Sign Up',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'is_logged_in': False,
        },
    )


def login(request):
    return render(
        request,
        'login.html',
        {
            'page_title': 'AskPupkin - Log In',
            'popular_tags': POPULAR_TAGS,
            'best_members': BEST_MEMBERS,
            'is_logged_in': False,
        },
    )
