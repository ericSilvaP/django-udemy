from django.shortcuts import render


# Create your views here.
def recipe(request):
    context = {"nome": "Eric Silva"}
    return render(request, "recipes/pages/home.html", context)
