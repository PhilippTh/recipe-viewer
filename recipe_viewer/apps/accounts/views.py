from __future__ import annotations

from typing import cast

from asgiref.sync import sync_to_async
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.i18n import set_language as django_set_language

from recipe_viewer.apps.accounts.forms import EmailAuthenticationForm


class AsyncCompatViewMixin:
    """Wrap Django's sync class-based views so they can be awaited."""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)

        async def async_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            handler = sync_to_async(view)
            return await handler(request, *args, **kwargs)

        return async_view


class AsyncLoginView(AsyncCompatViewMixin, LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class AsyncLogoutView(AsyncCompatViewMixin, LogoutView):
    next_page: str | None = cast(str, reverse_lazy("recipe_list"))


@require_http_methods(["POST"])
async def set_language(request: HttpRequest) -> HttpResponse:
    """Delegate to Django's built-in language switcher in an async-friendly way."""

    handler = sync_to_async(django_set_language)
    return await handler(request)
