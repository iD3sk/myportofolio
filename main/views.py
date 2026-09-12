from django.shortcuts import render

from main.models import Experience


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
    }
    return render(request, "about.html", context)
