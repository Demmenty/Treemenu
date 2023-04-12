from django import template
from django.db.models.query import QuerySet

from menu.models import MenuItem
from menu.services import DrawMenuService


register = template.Library()


# кастомный таг, рендерящий меню
@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu) -> dict:
    """возвращает словарь параметров для рендеринга меню.
    необходимо передать название меню."""

    service = DrawMenuService()

    # получем все элементы меню, название которого передано
    menu_items: QuerySet[MenuItem] = MenuItem.objects.filter(menu__name=menu)
    items_values: QuerySet[dict] = menu_items.values()

    # добавляем в результат элементы меню без родителя
    root_items: QuerySet[dict] = items_values.filter(parent=None)
    result_items: list[dict] = list(root_items)

    # определяем, что нажат какой-то элемент, и мы не в корне меню
    # и в таком случае дополняем результирующий словарь дочерними элементами открытых
    selected_item_id = context["request"].GET.get(menu)

    if selected_item_id:
        # определяем нажатый элемент
        selected_item_id: int = int(context["request"].GET[menu])
        selected_item: MenuItem = menu_items.get(id=selected_item_id)

        # составляем список id уже открытых элементов по нажатому
        selected_items_id_list: list[int] = service.get_selected_items_id(
            selected_item, selected_item_id, result_items
        )

        for item in result_items:
            # если id корневого элемента меню есть в списке id открытых
            if item["id"] in selected_items_id_list:
                # дополняем его словарь информацией о дочерних элементах
                item["child_items"]: list[dict] = service.get_child_items(
                    items_values, item["id"], selected_items_id_list
                )

    result = {
        "menu": menu,
        "items": result_items,
        "selected_item_id": selected_item_id,
        "other_urlstring": service.get_urlstring(context, menu),
    }

    return result
