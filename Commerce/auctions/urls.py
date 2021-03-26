from django.urls import path

from . import views

app_name="auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("<int:listing_id>", views.test, name="test"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("error", views.error, name="error"),
    path("add_listing", views.add_listing , name="add_listing"),
    path("activelist", views.activelist, name="activelist"),
    path("watchlist", views.watchlist, name="watchlist"),
]
