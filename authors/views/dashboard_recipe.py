from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render

from authors.forms.recipe_form import AuthorsRecipeForm
from recipes.models import Recipe


class DashboardEditRecipe(View):
    def render_edit_recipe(self, form):
        return render(
            self.request,
            "authors/pages/dashboard_recipe_edit.html",
            context={"form": form},
        )

    def get_published_recipe_or_404(self, id):
        return get_object_or_404(
            Recipe, is_published=False, author=self.request.user, id=id
        )

    def get(self, request, id):
        recipe = self.get_published_recipe_or_404(id)
        form = AuthorsRecipeForm(instance=recipe)
        return self.render_edit_recipe(form)

    def post(self, request, id):
        recipe = self.get_published_recipe_or_404(id)

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
            return redirect("authors:dashboard_recipe_edit", id=id)

        return self.render_edit_recipe(form)
