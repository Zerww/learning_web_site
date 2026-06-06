from django.contrib import admin

from apps.notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'learning_stage', 'progress',
                    'difficulty', 'status', 'view_count', 'sort_order']
    list_filter = ['learning_stage', 'difficulty', 'status']
    search_fields = ['title']
    raw_id_fields = ['category', 'author', 'parent']
