from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from main.forms import AchievementForm, ExperienceForm
from main.models import Achievements, Educations, Experience


def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def can_update_portfolio(user):
    return user.is_superuser or is_editor(user)


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Fiqhi",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login", timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    context = {
        "name": "Fiqhi",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
    )

    context = {
        "name": "Fiqhi Deski Ismail",
        "npm": "2506534245",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia for longer than "
            "planned, now a familiar (and slightly dreaded) face "
            "among Fasilkom students as a teaching assistant "
            "across several courses. "
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experiences(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fiqhi Deski Ismail",
        "title_query": title_query,
        "can_update": can_update_portfolio(request.user),
        "form": ExperienceForm(),
    }

    return render(request, "experiences.html", context)


def show_about(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fiqhi Deski Ismail",
        "bio": (
            "CS student at Universitas Indonesia for longer than planned, now a familiar "
            "(and slightly dreaded) face among Fasilkom students as a teaching assistant "
            "across several courses."
        ),
        "UI": Educations.objects.filter(
            institution="Universitas Indonesia",
            program="S1 Ilmu Komputer",
        ).first(),
        "SMA": Educations.objects.filter(
            institution="SMAN 1 Padang Panjang",
        ).first(),
        "SMP": Educations.objects.filter(
            institution="SMP Islam Raudhatul Jannah",
        ).first(),
        "title_query": title_query,
        "can_update": can_update_portfolio(request.user),
    }

    return render(request, "about.html", context)


@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AchievementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement has been added!")
        return redirect("main:show_about")

    context = {
        "name": "Fiqhi",
        "form": form,
    }

    return render(request, "achievement_form.html", context)


def get_achievement_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievements.objects.all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    achievements = achievements.order_by("-year")

    data = []
    for achievement in achievements:
        liked_users = achievement.liked_by.all()
        is_liked = request.user in liked_users if request.user.is_authenticated else False
        liked_by_names = ", ".join([u.username for u in liked_users])

        data.append({
            "pk": str(achievement.id),
            "fields": {
                "title": achievement.title,
                "year": achievement.year,
                "organization": achievement.organization,
                "rank": achievement.rank,
                "description": achievement.description,
                "is_liked": is_liked,
                "liked_by_names": liked_by_names,
            }
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not can_update_portfolio(request.user):
        raise PermissionDenied

    achievement = get_object_or_404(Achievements, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement updated successfully!")
        return redirect("main:show_about")

    context = {
        "name": "Fiqhi",
        "form": form,
        "achievement": achievement,
    }

    return render(request, "achievement_form.html", context)


@login_required(login_url="/login/")
@require_POST
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    achievement = get_object_or_404(Achievements, pk=achievement_id)

    achievement.delete()
    messages.success(request, "Achievement successfully deleted!")

    return redirect("main:show_about")


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience has been added!")
        return redirect("main:show_experiences")

    context = {
        "name": "Fiqhi",
        "form": form,
    }

    return render(request, "experience_form.html", context)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add an experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "New experience has been added.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("liked_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        liked_users = experience.liked_by.all()
        liked_user_ids = {user.pk for user in liked_users}
        is_liked = (
            request.user.is_authenticated and request.user.pk in liked_user_ids
        )
        liked_by_names = ", ".join(user.username for user in liked_users)

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "organization": experience.organization,
                "org_logo": experience.org_logo,
                "location": experience.location,
                "description": experience.description,
                "started_at": experience.started_at,
                "ended_at": experience.ended_at,
                "skills": experience.skills,
                "is_liked": is_liked,
                "like_count": len(liked_user_ids),
                "liked_by_names": liked_by_names,
            },
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not can_update_portfolio(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience updated successfully!")
        return redirect("main:show_experiences")

    context = {
        "name": "Fiqhi",
        "form": form,
        "experience": experience,
    }

    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    experience.delete()
    messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experiences")


@login_required(login_url="/login/")
@require_POST
def toggle_experience_like(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if experience.liked_by.filter(pk=request.user.pk).exists():
        experience.liked_by.remove(request.user)
    else:
        experience.liked_by.add(request.user)

    like_user_ids = {user.pk for user in experience.liked_by.all()}
    is_liked = (request.user.is_authenticated and request.user.pk in like_user_ids)

    return JsonResponse({
        "is_liked": is_liked,
        "like_count": experience.liked_by.count(),
    })


@login_required(login_url="/login/")
@require_POST
def toggle_achievement_like(request, achievement_id):
    achievement = get_object_or_404(Achievements, pk=achievement_id)

    if achievement.liked_by.filter(pk=request.user.pk).exists():
        achievement.liked_by.remove(request.user)
    else:
        achievement.liked_by.add(request.user)
    
    liked_user_ids = {user.pk for user in achievement.liked_by.all()}
    is_liked = (request.user.is_authenticated and request.user.pk in liked_user_ids)

    return JsonResponse({
        "is_liked": is_liked,
        "like_count": achievement.liked_by.count(),
    })
