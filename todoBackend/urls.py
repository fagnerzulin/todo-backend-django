from django.contrib import admin
from django.urls import path, include
from todo.views import RegisterView, TodoView, LoginView
from knox import views as knox_views


urlpatterns = [
    path('', include('todo.urls')),
    path('admin/', admin.site.urls),
    path('api/todo/', TodoView.as_view(), name='todo'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
