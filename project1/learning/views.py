from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Lesson, Quiz, Task, UserProgress, LevelDefinition, QuizAttempt
from .models import Question, Choice
from django.utils import timezone
from django.contrib import messages
from .forms import LessonForm

@login_required
def lesson_list(request):
    lessons = Lesson.objects.filter(is_published=True).order_by('id')
    progress = getattr(request.user, 'progress', None)
    return render(request, 'learning/lesson_list.html', {'lessons': lessons, 'progress': progress})

@login_required
def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, is_published=True)
    quiz = lesson.quizzes.first()
    attempt = None
    if quiz and request.user.is_authenticated:
        attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz, completed_at__isnull=False).order_by('-completed_at').first()
    return render(request, 'learning/lesson_detail.html', {
        'lesson': lesson,
        'quiz_attempt': attempt,
    })

@login_required
def progress_dashboard(request):
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    levels = LevelDefinition.objects.all()
    return render(request, 'learning/progress.html', {'progress': progress, 'levels': levels})

@login_required
def task_list(request):
    tasks = Task.objects.filter(is_active=True)
    return render(request, 'learning/task_list.html', {'tasks': tasks})

# Placeholder quiz taking (basic MCQ flow without timing yet)
@login_required
def quiz_take(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)
    questions = quiz.questions.prefetch_related('choices')
    if request.method == 'POST':
        total = questions.count()
        correct = 0
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected and q.choices.filter(id=selected, is_correct=True).exists():
                correct += 1
        score_percent = (correct / total) * 100 if total else 0
        earned = int(quiz.eco_points * (score_percent / 100))
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, score_percent=score_percent, earned_points=earned, completed_at=timezone.now())
        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        progress.add_points(earned)
        messages.success(request, f'Quiz completed: {score_percent:.0f}% — {earned} eco-points earned!')
        return redirect('learning:progress')
    return render(request, 'learning/quiz_take.html', {'quiz': quiz, 'questions': questions})


def staff_check(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(staff_check)
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('learning:lesson_detail', slug=lesson.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LessonForm()
    return render(request, 'learning/lesson_form.html', {'form': form})


@login_required
@user_passes_test(staff_check)
def lesson_quiz_build(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    quiz = lesson.quizzes.first()
    if request.method == 'POST':
        title = request.POST.get('quiz_title') or 'Lesson Quiz'
        eco_points = int(request.POST.get('quiz_points') or 100)
        time_limit = request.POST.get('time_limit_seconds') or None
        if quiz is None:
            quiz = Quiz.objects.create(lesson=lesson, title=title, eco_points=eco_points, time_limit_seconds=time_limit or None)
        else:
            quiz.title = title
            quiz.eco_points = eco_points
            quiz.time_limit_seconds = time_limit or None
            quiz.save()
        # Clear existing questions for simplicity (could diff update later)
        quiz.questions.all().delete()
        total_questions = int(request.POST.get('total_questions') or 0)
        for idx in range(1, total_questions + 1):
            q_text = request.POST.get(f'q{idx}_text')
            q_type = request.POST.get(f'q{idx}_type') or 'MCQ'
            if not q_text:
                continue
            question = Question.objects.create(quiz=quiz, text=q_text, question_type=q_type, order=idx)
            if q_type == 'TF':
                correct_val = request.POST.get(f'q{idx}_tf_correct') == 'true'
                Choice.objects.create(question=question, text='True', is_correct=correct_val)
                Choice.objects.create(question=question, text='False', is_correct=not correct_val)
            else:
                choice_count = int(request.POST.get(f'q{idx}_choice_count') or 0)
                for c in range(1, choice_count + 1):
                    c_text = request.POST.get(f'q{idx}_choice{c}_text')
                    is_correct = request.POST.get(f'q{idx}_choice{c}_correct') == 'on'
                    if c_text:
                        Choice.objects.create(question=question, text=c_text, is_correct=is_correct)
        messages.success(request, 'Quiz saved successfully!')
        return redirect('learning:lesson_detail', slug=lesson.slug)
    existing_questions = []
    if quiz:
        for q in quiz.questions.prefetch_related('choices'):
            existing_questions.append({
                'id': q.id,
                'text': q.text,
                'type': q.question_type,
                'choices': [{'text': c.text, 'is_correct': c.is_correct} for c in q.choices.all()]
            })
    return render(request, 'learning/quiz_builder.html', {
        'lesson': lesson,
        'quiz': quiz,
        'existing_questions': existing_questions,
    })
