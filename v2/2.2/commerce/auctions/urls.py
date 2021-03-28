from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:list_id>", views.views_list, name="views_list"),
    path("active-list", views.active_list, name="active_list"),
    path("<int:list_id>/com_make", views.com_make, name="com_make")

]
