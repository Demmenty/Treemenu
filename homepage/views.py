from django.shortcuts import render


def homepage(request):
    """главная страница"""

    template = "homepage/home.html"

    if request.GET.get("main_menu") == "25":
        data = {"easter_egg": True}
    else:
        data = {}

    return render(request, template, data)
