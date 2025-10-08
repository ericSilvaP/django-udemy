from django import forms

from recipes.models import Recipe


class AuthorsRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        ]

    preparation_steps = forms.CharField(
        widget=forms.Textarea(attrs={"class": "span-2"})
    )
    cover = forms.ImageField(widget=forms.FileInput(attrs={"class": "span-2"}))
