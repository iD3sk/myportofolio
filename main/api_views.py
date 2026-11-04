from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.models import Experience, Achievements
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ExperienceSerializer, AchievementsSerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list_create(request):
    if request.method == "GET":
        title_query = request.query_params.get("title", "").strip()
        experiences = Experience.objects.prefetch_related("liked_by").all()
        if title_query:
            experiences = experiences.filter(title__icontains=title_query)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data, context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("liked_by"), pk=experience_id,
    )
    if request.method == "GET":
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)
    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_list_create(request):
    if request.method == "GET":
        title_query = request.query_params.get("title", "").strip()
        achievements = Achievements.objects.prefetch_related("liked_by").order_by("-year")
        if title_query:
            achievements = achievements.filter(title__icontains=title_query)
        serializer = AchievementsSerializer(
            achievements, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = AchievementsSerializer(
        data=request.data, context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def achievement_detail(request, achievement_id):
    achievement = get_object_or_404(
        Achievements.objects.prefetch_related("liked_by"), pk=achievement_id,
    )
    if request.method == "GET":
        serializer = AchievementsSerializer(achievement, context={"request": request})
        return Response(serializer.data)
    if request.method == "DELETE":
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AchievementsSerializer(
        achievement,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_like(request, experience_id):
    item = get_object_or_404(Experience, pk=experience_id)
    if item.liked_by.filter(pk=request.user.pk).exists():
        item.liked_by.remove(request.user)
        is_liked = False
    else:
        item.liked_by.add(request.user)
        is_liked = True
    return Response({"is_liked": is_liked, "like_count": item.liked_by.count()})


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def achievement_like(request, achievement_id):
    item = get_object_or_404(Achievements, pk=achievement_id)
    if item.liked_by.filter(pk=request.user.pk).exists():
        item.liked_by.remove(request.user)
        is_liked = False
    else:
        item.liked_by.add(request.user)
        is_liked = True
    return Response({"is_liked": is_liked, "like_count": item.liked_by.count()})
