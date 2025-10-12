from django import forms

from recipes.models import Recipe
from utils.strings import is_positive_number


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
    cover = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "span-2"}), required=False
    )
    servings_unit = forms.ChoiceField(
        choices=(
            ("porções", "Porções"),
            ("fatias", "Fatias"),
            ("pessoas", "Pessoas"),
        )
    )

    preparation_time_unit = forms.ChoiceField(
        choices=(
            ("minutos", "Minutos"),
            ("horas", "Horas"),
        )
    )

    def clean_title(self):
        field_value = self.cleaned_data.get("title", "")

        if len(field_value) < 5:
            raise forms.ValidationError("Must have at least 5 characters.")

        return field_value

    def clean_description(self):
        field_value = self.cleaned_data.get("description", "")

        if len(field_value) < 5:
            raise forms.ValidationError("Must have at least 5 characters.")

        return field_value

    def clean_preparation_steps(self):
        field_value = self.cleaned_data.get("preparation_steps", "")

        if len(field_value) < 5:
            raise forms.ValidationError("Must have at least 5 characters.")

        return field_value

    def clean_preparation_time(self):
        field_value = self.cleaned_data.get("preparation_time", "")

        if not is_positive_number(field_value):
            raise forms.ValidationError("Must be a positive number.")

        return field_value

    def clean_servings(self):
        field_value = self.cleaned_data.get("servings", "")

        if not is_positive_number(field_value):
            raise forms.ValidationError("Must be a positive number.")

        return field_value
