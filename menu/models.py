from django.db import models


class Menu(models.Model):
    name = models.CharField("Название", unique=True, max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        Menu, related_name="menu_items", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="childrens",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
