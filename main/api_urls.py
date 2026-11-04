from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("experiences/", api_views.experience_list_create, name="experience_list"),
    path(
        "experiences/<uuid:experience_id>/",
        api_views.experience_detail,
        name="experience_detail",
    ),
    path("experiences/<uuid:experience_id>/like/", api_views.experience_like, name="experience_like"),
    path("achievements/", api_views.achievement_list_create, name="achievement_list"),
    path("achievements/<uuid:achievement_id>/", api_views.achievement_detail, name="achievement_detail"),
    path("achievements/<uuid:achievement_id>/like/", api_views.achievement_like, name="achievement_like"),
]
