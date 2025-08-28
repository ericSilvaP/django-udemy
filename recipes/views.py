from django.shortcuts import render


# Create your views here.
def home(request):
    context = {"nome": "Eric Silva"}
    return render(request, "recipes/pages/home.html", context)


def recipe(request, id):
    return render(request, "recipes/pages/recipe-view.html")
