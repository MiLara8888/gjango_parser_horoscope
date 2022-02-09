from django import template  # создаем фильтры

register = template.Library()  # переменная экземпляр класса librari с помощью нее регистрируем наши фильтры


@register.filter(name='split')  # фильр развание нашего фильтра
def split(value, key=' '):
    return value.split(key)

# фильтр нужно добавлять в шаблоны!!! {% load my_filter %}