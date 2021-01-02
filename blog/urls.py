from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete', views.delete_post, name='delete_post'),
    path('info_superuser/', views.info_superuser, name='info_superuser'),
    path('last_hour_post/', views.last_hour_post, name='last_hour_post'),
    path('search_str/', views.search_str, name='search_str')
]
