from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.QuestionListCreateIndexView.as_view(), name='index'),
    path('me', views.Me.as_view(), name='me'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
]