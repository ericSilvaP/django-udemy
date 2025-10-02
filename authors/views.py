from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    login_url = reverse("authors:login")

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

    return redirect(login_url)


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if request.method != "POST":
        return redirect("authors:login")

    logout(request)
    return redirect("authors:login")
