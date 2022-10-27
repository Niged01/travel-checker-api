from django.urls import path
from travelled import views

urlpatterns = [
    path('travelled/', views.TravelledList.as_view()),
    path('travelled/<int:pk>/', views.TravelledDetail.as_view()),
]
