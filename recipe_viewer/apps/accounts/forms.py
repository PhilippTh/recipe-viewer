from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class EmailAuthenticationForm(AuthenticationForm):
    """Authentication form that relabels the username field as email."""

    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("you@example.com"),
            }
        ),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("••••••••"),
            }
        ),
    )
