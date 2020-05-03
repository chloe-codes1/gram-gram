from django.urls import path
from . import views 

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:article_id>/', views.comments, name='comments'),
    path('<int:article_id>/comments/', views.comment_create, name='comment_create'),
    path('<int:article_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:article_id>/like/', views.like, name='like'),
    path('explore/<tag>/',  views.index, name='tag'),
    path('search/', views.search, name='search')
]