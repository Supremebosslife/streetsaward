from django import template

register = template.Library()

@register.filter(name='group_by_category')
def group_by_category(queryset):
    grouped = {}
    for item in queryset:
        category_name = item.nominee.category.name
        if category_name not in grouped:
            grouped[category_name] = [item]
        else:
            grouped[category_name].append(item)
    return grouped.items()
