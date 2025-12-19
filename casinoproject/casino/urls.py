from . import views
from django.urls import path

urlpatterns = [
    path('', views.top, name='top'),
    path('bacara_bet/', views.bacara_bet, name='bacara_bet'),
    path('bacarrat/', views.bacarrat, name='bacarrat'),
    path('blackjack_bet/', views.blackjack_bet, name='blackjack_bet'),
    path('blackjack/', views.blackjack, name='blackjack'),
]