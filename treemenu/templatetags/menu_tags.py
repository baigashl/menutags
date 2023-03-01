from django import template
from django.urls import reverse, resolve
from treemenu.models import Menu
from django.views.decorators.cache import cache_page
import json
from django.http import HttpResponse, HttpResponseRedirect



register = template.Library()


def build_menu(menu_items, current_url):
    """
    Функция, которая рекурсивно строит дерево меню
    """
    menu_html = "<ul>"
    for item in menu_items:
        active = ""
        if current_url == item.url:
            active = "active"
        menu_html += f'<li class="{active}"><a href="{item.url}">{item.name}</a>'
        children = item.menu_set.all()
        if children:
            menu_html += build_menu(children, current_url)
        menu_html += "</li>"
    menu_html += "</ul>"
    # print(json.loads(menu_html))
    return menu_html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu_items = Menu.objects.filter(name=menu_name, parent=None)
    menu_html = build_menu(menu_items, current_url)
    return menu_html

# from django import template
# from django.urls import reverse
# from treemenu.models import Menu
#
#
# register = template.Library()
#
#
# @register.simple_tag(takes_context=True)
# def draw_menu(context, menu_name):
#     # Получаем текущий URL
#     current_url = context['request'].path
#
#     # Получаем все пункты меню с указанным именем
#     menu_items = Menu.objects.filter(menu__name=menu_name)
#
#     # Строим дерево меню
#     menu_tree = build_menu_tree(menu_items)
#
#     # Отображаем дерево меню в шаблоне
#     return render_menu_tree(menu_tree, current_url)
#
#
# def build_menu_tree(menu_items):
#     """
#     Строит древовидное дерево меню на основе плоского списка пунктов меню.
#     """
#     # Создаем словарь для быстрого поиска элементов по ID
#     item_dict = {}
#     for item in menu_items:
#         item_dict[item.id] = item
#
#     # Создаем словарь для быстрого поиска дочерних элементов
#     child_dict = {}
#     for item in menu_items:
#         child_dict[item.id] = []
#
#     # Строим список дочерних элементов для каждого элемента
#     for item in menu_items:
#         if item.parent_id:
#             child_dict[item.parent_id].append(item)
#
#     # Строим дерево, начиная с корневых элементов
#     tree = []
#     for item in menu_items:
#         if not item.parent_id:
#             tree.append(item)
#
#     # Рекурсивно добавляем дочерние элементы в дерево
#     def add_children(parent):
#         parent.children = child_dict.get(parent.id, [])
#         for child in parent.children:
#             add_children(child)
#
#     for item in tree:
#         add_children(item)
#
#     return tree
#
#
# def render_menu_tree(menu_tree, current_url):
#     """
#     Отображает древовидное дерево меню в HTML-код.
#     """
#     # Открываем корневой список
#     html = '<ul>'
#
#     # Рекурсивно отображаем каждый элемент меню
#     for item in menu_tree:
#         html += render_menu_item(item, current_url)
#
#     # Закрываем корневой список
#     html += '</ul>'
#
#     return html
#
#
# def render_menu_item(item, current_url):
#     """
#     Отображает отдельный пункт меню в HTML-код.
#     """
#     # Проверяем, является ли этот элемент текущим пунктом меню
#     active = (current_url == item.get_absolute_url())
#
#     # Открываем новый элемент меню
#     html = '<li{}>'.format(' class="active"' if active else '')
#
#     # Отображаем

