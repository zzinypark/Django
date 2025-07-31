from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from todo.views import todo_list, todo_info, todo_create, todo_delete, todo_update
from users import views as user_view


urlpatterns = [
		path('admin/', admin.site.urls),
        # CBV
        path('cbv/', include('todo.urls')),

        #FBV
        path('todo/', todo_list, name='todo_list'), # 추가
        path('todo/<int:todo_id>/', todo_info, name='todo_info'),
        path('todo/create/', todo_create, name='todo_create'),
        path('todo/<int:todo_id>/update/', todo_update, name='todo_update'),
        path('todo/<int:todo_id>/delete/', todo_delete, name='todo_delete'),

        #user
        path('accounts/login/', user_view.user_login, name='user_login'),
        path('accounts/signup/', user_view.user_signup, name='user_signup'),
        path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
