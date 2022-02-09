from django.urls import path,converters
from . import views

urlpatterns = [
    # path('<int:month>/<int:day>/', views.get_info_by_date),
    path('', views.index, name='index'),
    path('<int:zodiac>/', views.get_zodiac_int),  # пара строк про конверторы, внимание на последовательноесть
    path('<str:zodiac>/', views.get_zodiac_str, name='horoscope_name'),

]
