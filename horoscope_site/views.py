from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
import requests
from datetime import datetime

zodiac_dict = {"aries": "Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля)",
               "taurus": "Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая)",
               "gemini": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня)",
               "cancer": "Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля)",
               "leo": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа)",
               "virgo": "Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября)",
               "libra": "Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября)",
               "scorpio": "Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября)",
               "sagittarius": "Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря)",
               "capricorn": "Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января",
               "aquarius": "Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля)",
               "pisces": "Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта)"
               }

type_zodiac = {'fire': ['aries', "leo", "sagittarius"], 'air': ["gemini", "libra", "aquarius"],
               'earth': ["taurus", "virgo", "capricorn"], 'water': ["cancer", "scorpio", "pisces"]}

mon = {"aries": ['03 21 2000', '04 20 2000'],
       "taurus": ['04 21 2000', '05 21 2000'],
       "gemini": ['05 22 2000', '06 21 2000'],
       "cancer": ['06 22 2000', '07 22 2000'],
       "leo": ['7 30 2000', '8 21 2000'],
       "virgo": ['8 22 2000', '9 23 2000'],
       "libra": ['9 28 2000', '10 23 2000'],
       "scorpio": ['10 24 2000', '11 22 2000'],
       "sagittarius": ['11 23 2000', '12 22 2000'],
       "capricorn": ['12 23 2000', '1 20 2001'],
       "aquarius": ['1 21 2000', '2 19 2000'],
       "pisces": ['2 20 2000', '3 20 2000'], }

zodiac_dicti = {}
zodiac_date_dict = ''


def get_zodiac_str(request, zodiac: str):
    global zodiac_date_dict
    global zodiac_dicti
    description = zodiac_dict.get(zodiac)
    now = datetime.now()
    if zodiac_date_dict != now.strftime(
            "%d-%m-%Y") and zodiac in zodiac_dict:  # провека , чтобы не делать много гет запросов
        xml_string = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text
        soup = BeautifulSoup(xml_string, 'xml')
        zodiac_date_dict = '-'.join(soup.date['today'].split('.'))
        zodiac_dicti = result_horoscope_zodiac()

    if zodiac not in zodiac_dict:
        return render(request, 'horoscope_site/info_zodiac.html', context={
            'sign': zodiac,
            'zodiac_dict': zodiac_dict, })
    data = {
        'description': description,
        'sign': zodiac,
        'zodiac_dict': zodiac_dict,
        'today': zodiac_dicti[zodiac][1],
        'tommorow': zodiac_dicti[zodiac][2],
        'tommorow2': zodiac_dicti[zodiac][3],
    }
    return render(request, 'horoscope_site/info_zodiac.html', context=data)


def get_zodiac_int(request, zodiac: int):  # учимся по порядковому номеру перенаправлять на список обратно
    zodiac_list = list(zodiac_dict)  # сделали список из ключей
    if zodiac > len(zodiac_list):  # проверили число
        return HttpResponseNotFound(f'Неправильный порядковый номер знака зодиака {zodiac}')
    result = zodiac_list[zodiac - 1]  # в результат взяли ключ
    redirect_url = reverse('horoscope_name', args=(result,))  # создали ссылку для динамического url
    return HttpResponseRedirect(redirect_url)  # перенаправление


def index(request):
    global zodiac_dict
    zodiac_dict = zodiac_dict
    date = {
        'zodiac_dict': zodiac_dict,
    }
    return render(request, 'horoscope_site/index.html', context=date)


def result_horoscope_zodiac():
    xml_string = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text
    soup = BeautifulSoup(xml_string, 'xml')
    dict = {}
    for tag in soup.find_all(True):
        if tag.name in ['aries', "leo", "sagittarius", "gemini", "libra", "aquarius", "taurus", "virgo",
                        "capricorn", "cancer", "scorpio", "pisces"]:
            dict[tag.name] = []
            for j in soup.find_all(tag.name):
                list_result_horos = [str(k.text).strip() for k in j if k.text != '\n']
                dict[tag.name] = list_result_horos
    return dict

# def get_info_by_date(request, month, day):
#     try:
#         if day <= 20 and month == 1:
#             user_day = '' + str(month) + ' ' + str(day) + ' ' + '2001'
#         else:
#             user_day = '' + str(month) + ' ' + str(day) + ' ' + '2000'
#         result = strptime(user_day, "%m %d %Y")
#         for i, j in mon.items():
#             if result >= strptime(j[0], "%m %d %Y") and result <= strptime(j[1], "%m %d %Y"):
#                 redirect_path = reverse('horoscope_name', args=[str(i)])
#                 return HttpResponseRedirect(redirect_path)
#     except ValueError:
#         return HttpResponseNotFound('Введены некорректные денные')
