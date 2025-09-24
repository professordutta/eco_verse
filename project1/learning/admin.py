from django.contrib import admin
from .models import (LevelDefinition, Lesson, Quiz, Question, Choice, QuizAttempt, Task, TaskSubmission, UserProgress)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'lesson', 'eco_points', 'is_active')
    list_filter = ('lesson', 'is_active')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('quiz', 'order', 'question_type')
    ordering = ('quiz', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'eco_points', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'short_description')

@admin.register(LevelDefinition)
class LevelDefinitionAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'required_points')
    ordering = ('required_points',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'eco_points', 'requires_photo', 'is_active')
    list_filter = ('is_active', 'requires_photo')

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'submitted_at', 'awarded_points')
    list_filter = ('status', 'task')
    search_fields = ('user__username', 'task__title')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score_percent', 'earned_points', 'completed_at')
    list_filter = ('quiz',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'current_level', 'updated_at')
