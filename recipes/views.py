from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    context = {"recipes": recipes}
    return render(request, "recipes/pages/home.html", context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    # if not recipes:
    #     return HttpResponse(content="Not Found", status=404)
    # raise Http404("Not Found :(")

    category_name = getattr(recipes[0].category, "name")

    context = {
        "recipes": recipes,
        "title": f"{category_name} - Category |",
    }
    return render(request, "recipes/pages/category.html", context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    context = {
        "recipe": recipe,
        "is_detail": True,
    }

    return render(request, "recipes/pages/recipe-view.html", context)


def search(request):
    search_term = str(request.GET.get("q", "")).strip()
    if not search_term:
        raise Http404()

    context = {
        "title": f"Pesquisa por {search_term} |",
        "search_term": search_term,
    }

    return render(request, "recipes/pages/search.html", context)
