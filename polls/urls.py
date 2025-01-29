from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.all_migthy_method, name='index'),
    path('<int:pk>/', views.all_migthy_method, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('me/', views.me, name='me'),
]