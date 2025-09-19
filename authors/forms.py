from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, "placeholder", placeholder_val)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username")
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["first_name"], "Ex.: John")
        add_placeholder(self.fields["last_name"], "Ex.: Doe")
        add_attr(self.fields["username"], "css", "a-css-class")

    password = forms.CharField(
        error_messages={"required": "Password can't be empty"},
        help_text="Password must have at least: one uppercase letter, one lowercase letter and one number. Lenght: minimum 8 characters",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
    )

    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your Password"})
    )

    # validations
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if "1234" in str(password):
            raise forms.ValidationError(
                "Senha fraca", code="invalid", params={"value": password}
            )

    def clean(self):
        data = super().clean()

        password = data.get("password")
        password_repeat = data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Passwords must be equals")

        return data
