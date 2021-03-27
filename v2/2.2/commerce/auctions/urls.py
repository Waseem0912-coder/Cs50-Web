from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:list_id>", views.test, name="test"),
    path("<int:list_id>/com_make", views.com_make, name="com_make")

]
