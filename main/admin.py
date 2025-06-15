from django.contrib import admin
from .models import Category, Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'slug']
    prepopulated_fields = {'slug': ('category',)}
    search_fields = ['category']
    list_filter = ['category']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_question', 'category', 'short_answer']
    search_fields = ['question', 'answer']
    list_filter = ['category__category']
    ordering = ['category', 'id']
    list_display_links = ['id', 'short_question', 'category']

    def short_question(self, obj):
        return obj.question[:50] + ('...' if len(obj.question) > 50 else '')

    def short_answer(self, obj):
        return obj.answer[:50] + ('...' if len(obj.answer) > 50 else '')

    short_question.short_description = 'Savol'
    short_answer.short_description = 'Javob'
