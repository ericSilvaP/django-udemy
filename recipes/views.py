from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from utils.recipes.factory import make_recipe
from .models import Recipe, Category


# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    context = {"recipes": recipes}
    return render(request, "recipes/pages/home.html", context)


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True
    ).order_by("-id")

    if not recipes:
        return HttpResponse(content="Not Found", status=404)
        # raise Http404("Not Found :(")

    category_name = getattr(
        getattr(recipes.first(), "category", None), "name", "Not Found"
    )

    context = {
        "recipes": recipes,
        "title": f"{category_name} - Category |",
    }
    return render(request, "recipes/pages/category.html", context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    context = {
        "recipe": recipe,
        "is_detail": True,
    }

    return render(request, "recipes/pages/recipe-view.html", context)
