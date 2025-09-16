from django.shortcuts import render

from .forms import RegisterForm


# Create your views here.
def home(request):
    form = RegisterForm()
    context = {"form": form}
    return render(request, "authors/pages/register_view.html", context)
