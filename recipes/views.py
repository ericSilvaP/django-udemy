from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination

from .models import Recipe
import os

PER_PAGE = os.environ.get("PER_PAGE", 6)


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = "-id"
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get("recipes"), PER_PAGE
        )
        context.update(
            {
                "recipes": page_obj,
                "pagination_range": pagination_range,
            }
        )
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(category__id=self.kwargs.get("category_id"))
        if not queryset:
            raise Http404()
        return queryset


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search_term = str(self.request.GET.get("q", "")).strip()
        queryset = queryset.filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = str(self.request.GET.get("q", "")).strip()

        if not search_term:
            raise Http404()

        context.update(
            {
                "title": f'Pesquisa por "{search_term}" |',
                "search_term": search_term,
            }
        )
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"is_detail": True})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        "recipes": page_obj,
        "pagination_range": pagination_range,
    }
    return render(request, "recipes/pages/home.html", context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    category_name = getattr(recipes[0].category, "name")

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        "recipes": page_obj,
        "title": f"{category_name} - Category |",
        "pagination_range": pagination_range,
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

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)),
        is_published=True,
    ).order_by("-id")
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        "title": f"Pesquisa por {search_term} |",
        "search_term": search_term,
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "additional_query_string": f"&q={search_term}",
    }

    return render(request, "recipes/pages/search.html", context)
