from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    path("experiences/add/", views.create_experience, name="create_experience"),
    path("experiences/", views.show_experiences, name="show_experiences"),
    path("experiences/<uuid:experience_id>/edit/", views.update_experience,name="update_experience",),
    path("experiences/<uuid:experience_id>/delete/", views.delete_experience, name="delete_experience"),
    path("api/experience/", views.get_experience_json, name="get_experience_json"),

    path("about/", views.show_about, name="show_about"),
    path("about/achievements/add/", views.create_achievement, name="create_achievement"),
    path("about/achievements/<uuid:achievement_id>/edit/", views.update_achievement, name="update_achievement"),
    path("about/achievements/<uuid:achievement_id>/delete/", views.delete_achievement, name="delete_achievement")
]
