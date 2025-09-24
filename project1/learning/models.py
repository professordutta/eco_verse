from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class LevelDefinition(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=80)
    required_points = models.PositiveIntegerField(help_text='Eco points required to reach this level')
    badge_color = models.CharField(max_length=20, default='#2d6a4f')

    class Meta:
        ordering = ['required_points']

    def __str__(self):
        return f"Level {self.number}: {self.name}"    

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    html_content = models.TextField(blank=True, help_text='Inline HTML module (fallback if no SCORM)')
    scorm_package = models.FileField(upload_to='scorm/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='lessons/covers/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='Optional embedded video URL (YouTube, etc.)')
    resource_file = models.FileField(upload_to='lessons/resources/', blank=True, null=True)
    eco_points = models.PositiveIntegerField(default=50)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    eco_points = models.PositiveIntegerField(default=100)
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Quiz: {self.title}"    

class Question(models.Model):
    QUIZ_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
    )
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=5, choices=QUIZ_TYPES, default='MCQ')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} Q{self.order}"    

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice for Q{self.question_id}"    

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    earned_points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'quiz', 'started_at')
        ordering = ['-started_at']

    def mark_complete(self, score_percent, earned_points):
        self.score_percent = score_percent
        self.earned_points = earned_points
        self.completed_at = timezone.now()
        self.save()

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    eco_points = models.PositiveIntegerField(default=150)
    requires_photo = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TaskSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='task_submissions', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tasks/', blank=True, null=True)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewer_notes = models.TextField(blank=True)
    awarded_points = models.IntegerField(default=0)

    class Meta:
        ordering = ['-submitted_at']

    def approve(self, points=None):
        self.status = 'approved'
        self.awarded_points = points if points is not None else self.task.eco_points
        self.save()

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    total_points = models.PositiveIntegerField(default=0)
    current_level = models.ForeignKey(LevelDefinition, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def recalc_level(self):
        level = LevelDefinition.objects.filter(required_points__lte=self.total_points).order_by('-required_points').first()
        self.current_level = level
        self.save()
        return level

    def add_points(self, amount):
        self.total_points += amount
        self.save()
        self.recalc_level()

    def __str__(self):
        return f"Progress {self.user.username}: {self.total_points} pts"
