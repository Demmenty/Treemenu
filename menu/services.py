from django.db.models.query import QuerySet
from django.template.context import RequestContext

from menu.models import MenuItem


class DrawMenuService:
    """доп.функции для отрисовки меню через кастомный таг"""

    def get_urlstring(self, context: RequestContext, curr_menu: str) -> str:
        """возвращает часть url, определяющую состояние других возможных меню на странице.
        передать контекст и название целевого меню (часть url для целевого опредяется в самом шаблоне).
        """

        args = []

        # собираем аргументы, описывающие состояние других менюшек
        for menu_name in context["request"].GET:
            if menu_name != curr_menu:
                selected_item_id: int = int(context["request"].GET[menu_name])
                arg: str = f"{menu_name}={selected_item_id}"
                args.append(arg)

        # собираем из аргументов целую строку запроса
        urlstring = ("&").join(args)

        return urlstring

    def get_child_items(
        self,
        items_values: QuerySet,
        current_item_id: int,
        selected_items_id_list: list[int],
    ) -> list[dict]:
        """возвращает список дочерних элементов переданного элемента меню. (рекурсивный поиск)
        аргументы:
        items_values - все элементы, относящиеся к выбранноу меню;
        current_item_id - id элемента меню, детей которого требуется найти;
        selected_items_id_list - список id элементов, которые уже выбраны (открыты)
        """

        # получаем элементы, родителем которых является переданный
        child_items: QuerySet[dict] = items_values.filter(
            parent_id=current_item_id
        )
        child_items_list: list[dict] = list(child_items)

        # если id дочернего элемента есть в спике открытых(выбранных) элементов,
        # аналогично находим всех его детей и добавляем элементу инфо о них,
        # чтобы составить правильное открытое дерево
        for item in child_items_list:
            if item["id"] in selected_items_id_list:
                item["child_items"] = self.get_child_items(
                    items_values, item["id"], selected_items_id_list
                )

        return child_items_list

    def get_selected_items_id(
        self, parent: MenuItem, selected_item_id: int, result_items: list[dict]
    ) -> list[int]:
        """возвращает список id элементов меню, которые уже выбраны (открыты).
        аргументы:
        parent - экземпляр элемента меню, который был нажат;
        selected_item_id - id элемента меню, который был нажат;
        result_items - список корневых элементов меню;
        """

        selected_items_id_list = []

        # добавляем в список id родительских элементов
        while parent:
            selected_items_id_list.append(parent.id)
            parent = parent.parent

        if selected_items_id_list:
            return selected_items_id_list

        # если список оказался пуст, выбранным считается только нажатый элемент
        for item in result_items:
            if item["id"] == selected_item_id:
                selected_items_id_list.append(selected_item_id)
                return selected_items_id_list
