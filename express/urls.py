from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('add_comment/<int:message_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)