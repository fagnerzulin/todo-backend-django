from django.contrib import admin
from todo.models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'createdAt', 'updateAt')
    list_filter = ('completed', )
    search_fields = ('title',)


admin.site.register(Todo, TodoAdmin)
