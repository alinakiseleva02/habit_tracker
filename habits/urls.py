from django.urls import path
from . import views

urlpatterns = [
    path('habits', views.HabitListView.as_view()), 
    path('habits/<int:id>', views.HabitDetailView.as_view()),
    
    path('habits/<int:habit_id>/schedules', views.ScheduleListView.as_view()),
    path('habits/<int:habit_id>/schedules/<int:id>', views.ScheduleDetailView.as_view()),
    path('schedules/<int:id>', views.ScheduleGlobalDetailView.as_view()),
    path('schedules/search', views.ScheduleSearchView.as_view()),

    path('habits/<int:habit_id>/logs', views.LogListView.as_view()),
    path('habits/<int:habit_id>/logs/<int:id>', views.LogDetailView.as_view()),
    path('logs/<int:id>', views.LogGlobalDetailView.as_view()),
    path('logs/search', views.LogSearchView.as_view()),

    path('habits/<int:habit_id>/stats', views.StatListView.as_view()),
    path('habits/<int:habit_id>/stats/<int:id>', views.StatDetailView.as_view()),
    path('stats/<int:id>', views.StatGlobalDetailView.as_view()),
    path('stats/search', views.StatSearchView.as_view()),
]