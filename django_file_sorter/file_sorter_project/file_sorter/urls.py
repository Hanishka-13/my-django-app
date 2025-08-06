from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sort/', views.SortFilesView.as_view(), name='sort_files'),
    path('session/<int:session_id>/', views.SessionDetailView.as_view(), name='session_detail'),
]