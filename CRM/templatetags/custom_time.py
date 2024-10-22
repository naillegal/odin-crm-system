from django import template
from datetime import datetime

register = template.Library()

@register.filter
def to_date_only(value):
    try:
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M')
        return dt.strftime('%d-%B-%Y')
    except ValueError:
        return value 


@register.filter
def to_date_time(value):
    try:
        # Tarix və saatı parse edir
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M')
        # İstədiyiniz formatda qaytarır
        return dt.strftime('%d-%B-%Y %H:%M')
    except ValueError:
        # Əgər format uyğun gəlmirsə, orijinal dəyəri qaytarır
        return value