from django.contrib import admin
from django.urls import path
from .models import Menu
from django.shortcuts import render


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url', 'order')
    list_filter = ('name', 'parent')
    search_fields = ('name', 'url')


admin.site.register(Menu, MenuAdmin)


def page_with_menu(request):
    menu_name = 'main_menu'
    menu_items = Menu.objects.filter(name=menu_name, parent=None)
    context = {'menu_items': menu_items}
    return render(request, 'page_with_menu.html', context)
