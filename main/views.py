from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Educations, Achievements
from main.forms import ExperienceForm, AchievementForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.core import serializers
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

import datetime


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
        user = form.get_user()
        login(request, form.get_user())
        response =  redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')

    context = {
        "name": "Fiqhi Deski Ismail",
        "npm": "2506534245",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia for longer than " "planned, now a familiar (and slightly dreaded) face " "among Fasilkom students as a teaching assistant " "across several courses. "
        ),
        "last_login": last_login
    }
    return render(request, "index.html", context)


def show_experiences(request):
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode('utf-8'),
    )

    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fiqhi Deski Ismail",
        "experience_list": experiences,
        "title_query": title_query,
    }

    return render(request, "experiences.html", context)


def show_about(request):
    json_response = get_achievement_json(request)

    achievements = serializers.deserialize(
        "json",
        json_response.content.decode('utf-8'),
    )

    achievements = [achievement.object for achievement in achievements]
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
        "achievement_list": achievements,
        "title_query": title_query,
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

    achievements_json = serializers.serialize("json", achievements)
    return HttpResponse(achievements_json, content_type="application/json")

@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not request.user.is_superuser:
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
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    achievement = get_object_or_404(Achievements, pk=achievement_id)

    if request.method == "POST":
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

    
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
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
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experiences")



# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi like
@login_required(login_url="/login/")
def toggle_like(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.liked_by.all():
            experience.liked_by.remove(request.user)
        else:
            experience.liked_by.add(request.user)

    return redirect("main:show_experiences")
