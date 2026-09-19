from django.urls import path

from main.views import show_main, show_experiences, show_about, create_experience, get_experience_json, delete_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("experiences/add/", create_experience, name="create_experience"),
    path("experiences/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("about/", show_about, name="show_about"),
]
