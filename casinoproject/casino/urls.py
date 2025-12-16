from . import views
from django.urls import path

urlpatterns = [
    path('', views.top, name='top'),
    path('bacara_bet/', views.bacara_bet, name='bacara_bet'),
    path('bacarrat/', views.bacarrat, name='bacarrat'),
]