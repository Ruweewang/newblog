#coding:utf-8
from django import template
register = template.Library()


@register.filter('get_index')
def get_index(value, list_obj):
    try:
        return list(list_obj).index(value) + 1
    except ValueError as e:
        logger.warning("list object is not value./n%s" % e)

@register.filter
def month_to_upper(key):
    return ['一','二','三','四','五','六','七','八','九','十','十一','十二'][key.month-1]

