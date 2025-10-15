from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authors.forms.recipe_form import AuthorsRecipeForm
from recipes.models import Recipe


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class Dashboard(View):
    def get(self, request):
        recipes = Recipe.objects.filter(
            author=request.user, is_published=False
        ).order_by("-id")
        return render(request, "authors/pages/dashboard.html", {"recipes": recipes})


@method_decorator(login_required(login_url="authors:login"), name="dispatch")
class DashboardRecipe(View):
    def render_edit_recipe(self, form):
        return render(
            self.request,
            "authors/pages/dashboard_recipe_edit.html",
            context={"form": form},
        )

    def get_published_recipe(self, id):
        return Recipe.objects.filter(
            is_published=False, author=self.request.user, id=id
        ).first()

    def get(self, request, id=None):
        recipe = self.get_published_recipe(id)
        form = AuthorsRecipeForm(instance=recipe)
        return self.render_edit_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_published_recipe(id)

        form = AuthorsRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.is_published = False
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.save()

            messages.success(request, "Sua receita foi salva com sucesso!")
            return redirect("authors:dashboard_recipe_edit", id=recipe.id)

        return self.render_edit_recipe(form)


class DashboardDeleteRecipe(View):
    @method_decorator(login_required(login_url="authors:login"))
    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        recipe.delete()
        messages.success(request, "Receita apagada com sucesso!")
        return redirect("authors:dashboard")
