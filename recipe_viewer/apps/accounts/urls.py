from django.urls import path

from recipe_viewer.apps.accounts.views import AsyncLoginView
from recipe_viewer.apps.accounts.views import AsyncLogoutView
from recipe_viewer.apps.accounts.views import set_language

app_name = "accounts"

urlpatterns = [
    path("login/", AsyncLoginView.as_view(), name="login"),
    path("logout/", AsyncLogoutView.as_view(), name="logout"),
    path("set-language/", set_language, name="set_language"),
]
