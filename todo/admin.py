from django.contrib import admin
from todo.models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'completed', 'createdAt', 'updatedAt')
    list_filter = ('completed', )
    search_fields = ('title', 'user')


admin.site.register(Todo, TodoAdmin)
