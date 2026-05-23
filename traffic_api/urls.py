
from django.urls import path
from .views import (
    TrafficDataView,
    TrafficDataListView,
    TrafficDataUpdateView,
    TrafficDataDeleteView,
    ManualOverrideView
)

urlpatterns = [
    path('traffic/', TrafficDataView.as_view()),
    path('all-data/', TrafficDataListView.as_view()),
    
    path('update/<int:pk>/', TrafficDataUpdateView.as_view()),
    path('delete/<int:pk>/', TrafficDataDeleteView.as_view()),

    path('override/', ManualOverrideView.as_view()),
]