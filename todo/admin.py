from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from todo.models import Todo, Comment


@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    summernote_fields = ('description',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_completed')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Completed Image', {
            'fields': ('completed_image',)
        })
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'user', 'message', 'created_at')
    list_filter = ('todo', 'user')
    search_fields = ('message', 'user')
    ordering = ('-created_at',)
    list_display_links = ('message',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'user', 'message')
        }),
    )