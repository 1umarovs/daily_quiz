from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Question
from datetime import datetime, timedelta

def get_daily_question(request, slug):
    session_key = f"viewed_{slug}"
    viewed_data = request.session.get(session_key)

    now = datetime.now()
    today = now.date()

    if viewed_data:
        viewed_time = datetime.fromisoformat(viewed_data['time'])
        if now - viewed_time < timedelta(days=1):
            seconds_left = int((viewed_time + timedelta(days=1) - now).total_seconds())
            return JsonResponse({
                'already_answered': True,
                'question': viewed_data['question'],
                'answer': viewed_data['answer'],
                'seconds_left': seconds_left,
                'error': "Siz bu kategoriyadan bugun savol oldingiz. Ertaga yana urinib ko‘ring."
            })

    try:
        category = Category.objects.get(slug=slug)
        questions = Question.objects.filter(category=category).order_by('id')
        if not questions.exists():
            return JsonResponse({'error': 'Bu kategoriya uchun savollar mavjud emas.'})

        index = today.toordinal() % questions.count()
        question = questions[index]

        # Saqlash
        request.session[session_key] = {
            'question': question.question,
            'answer': question.answer,
            'time': now.isoformat()
        }

        return JsonResponse({
            'question': question.question,
            'answer': question.answer,
            'already_answered': False
        })

    except Category.DoesNotExist:
        return JsonResponse({'error': 'Kategoriya topilmadi.'})

def daily_questions(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request,'index.html' , context)
