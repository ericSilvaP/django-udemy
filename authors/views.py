from random import randint
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from authors.forms.recipe_form import AuthorsRecipeForm
from recipes.models import Recipe

from .forms import RegisterForm, LoginForm


def register_view(request):
    register_form_data = request.session.get("register_form_data")
    form = RegisterForm(register_form_data)
    context = {"form": form, "form_action": reverse("authors:register_create")}

    return render(request, "authors/pages/register_view.html", context)


def register_create(request: HttpRequest):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Usuário cadastrado com sucesso")
        del request.session["register_form_data"]
        return redirect("authors:login")

    return redirect("authors:register")


def login_view(request):
    form = LoginForm()
    context = {"form": form, "form_action": reverse("authors:login_create")}
    return render(request, "authors/pages/login.html", context)


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            request,
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )

        if authenticated_user is not None:
            messages.success(request, "Sucessfully logged.")
            login(request, authenticated_user)
        else:
            messages.error(request, "Incorrect password or username.")

    else:
        messages.error(request, "Error to validate form data.")

    return redirect("authors:dashboard")


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if request.method != "POST":
        return redirect("authors:login")

    logout(request)
    return redirect("authors:login")


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user).order_by(
        "-id"
    )
    context = {"recipes": recipes}
    return render(request, "authors/pages/dashboard.html", context)


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False, author=request.user, id=id
    ).first()

    if not recipe:
        raise Http404()

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
        redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))

    context = {"form": form}
    return render(request, "authors/pages/dashboard_recipe_edit.html", context)


@login_required(login_url="authors:login")
def dashboard_create_recipe(request):
    form = AuthorsRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user

        recipe.save()

        messages.success(request, "Receita criada com sucesso!")
        return redirect("authors:dashboard")

    return render(
        request,
        "authors/pages/dashboard_create_recipe.html",
        context={
            "form": form,
            "form_action": reverse("authors:dashboard_create_recipe"),
        },
    )
