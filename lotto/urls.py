from django.urls import path
from . import views

urlpatterns = [
    path('', views.lotto_index, name='lotto_index'),
    path('buy/', views.buy_lotto, name='buy_lotto'),
    path('check/', views.check_winnings, name='check_winnings'),
]