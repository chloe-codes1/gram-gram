from django.urls import path
from . import views 

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_id>/like/', views.like, name='like'),
    path('explore/<tag>/',  views.index, name='tag')
]