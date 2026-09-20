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
        "achievement_list": Achievements.objects.order_by("-year"),
    }
    return render(request, "about.html", context)


def create_experience(request):
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

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def update_experience(request, experience_id):
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

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "experience berhasil dihapus!")

    return redirect("main:show_experiences")

