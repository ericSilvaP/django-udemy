from django import forms
from django.contrib.auth.models import User


def add_widget_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    add_widget_attr(field, "placeholder", placeholder_val)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    password = forms.CharField(
        error_messages={"required": "Password must not be empty"},
        help_text="Password must have at least: one uppercase letter, one lowercase letter and one number. Lenght: minimum 8 characters.",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"},
        ),
        label="Password",
    )

    password_repeat = forms.CharField(
        error_messages={"required": "Please, repeat your password"},
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat your password"},
        ),
        label="Repeat Password",
    )

    first_name = forms.CharField(
        error_messages={"required": "Write your first name"},
        widget=forms.TextInput(
            attrs={"placeholder": "Ex.: John"},
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        error_messages={"required": "Write your last name"},
        widget=forms.TextInput(
            attrs={"placeholder": "Ex.: Doe"},
        ),
        label="Last Name",
    )

    username = forms.CharField(
        help_text="Username must have letters, numbers or one of those @.+-_. "
        "The length should be between 4 and 150 characters.",
        error_messages={
            "required": "Write your username",
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 151 characters",
        },
        widget=forms.TextInput(
            attrs={"placeholder": "Your username"},
        ),
        label="Username",
        min_length=4,
        max_length=150,
    )

    email = forms.CharField(
        error_messages={"required": "Write your e-mail"},
        widget=forms.TextInput(
            attrs={"placeholder": "Your e-mail"},
        ),
        label="E-mail",
    )

    # validations
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Passwords must be equals")

        return cleaned_data
