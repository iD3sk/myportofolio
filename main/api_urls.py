from django.urls import path
from rest_framework.authtoken import views as authtoken_views
from main import api_views

app_name = "api"

urlpatterns = [
    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_views.api_logout, name="logout"),
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
