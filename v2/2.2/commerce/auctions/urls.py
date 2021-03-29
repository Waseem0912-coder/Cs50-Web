from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:list_id>", views.views_list, name="views_list"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("cat", views.cat, name="cat"),
    path("cat_view", views.cat, name="cat_view"),
    path("<int:list_id>/make_bid", views.make_bid, name="make_bid"),
    path("active-list", views.active_list, name="active_list"),
    path("<int:list_id>/com_make", views.com_make, name="com_make")

]
