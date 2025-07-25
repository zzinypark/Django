from django.contrib import admin
from django.urls import path, include
from todo.views import todo_list, todo_info # 추가
from users import views as user_view


urlpatterns = [
		path('admin/', admin.site.urls),
        path('todo/', todo_list, name='todo_list'), # 추가
        path('todo/<int:todo_id>/', todo_info, name='todo_info'),
        path('accounts/login/', user_view.user_login, name='user_login'),
        path('accounts/signup/', user_view.user_signup, name='user_signup'),
        path('accounts/', include('django.contrib.auth.urls')),
]
