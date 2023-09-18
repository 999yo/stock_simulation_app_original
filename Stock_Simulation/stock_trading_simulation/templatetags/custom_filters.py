from django import template

register = template.Library()

@register.filter
def format_number(value):
    if value == int(value):
        return int(value)
    return value

@register.filter
def truncate_decimal(value):
    # 小数点第一位まで残して、それ以降の小数点以下を切り捨てる
    return round(value, 1)
