from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Educations, Achievements
from main.forms import ExperienceForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse


def show_main(request):
    context = {
        "name": "Fiqhi Deski Ismail",
        "npm": "2506534245",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia for longer than " "planned, now a familiar (and slightly dreaded) face " "among Fasilkom students as a teaching assistant " "across several courses. "
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fiqhi Deski Ismail",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experiences.html", context)


def show_about(request):
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
        "achievement_list": Achievements.objects.order_by("display_order", "-year"),
    }
    return render(request, "about.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience has been added!")
        return redirect("main:show_experience")

    context = {
        "name": "Fiqhi",
        "form": form,
    }
    return render(request, "experience_form.html", context) 
    
