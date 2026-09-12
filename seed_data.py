import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
django.setup()

from main.models import Achievements, Educations


Educations.objects.update_or_create(
    institution="Universitas Indonesia",
    program="S1 Ilmu Komputer",
    defaults={
        "level": "Undergraduate",
        "started_at": 2025,
        "ended_at": None,
        "description": "Currently studying Computer Science at Universitas Indonesia while working on web development, teaching, and student-led projects.",
        "display_order": 1,
    },
)

Educations.objects.update_or_create(
    institution="SMAN 1 Padang Panjang",
    defaults={
        "level": "SMA",
        "started_at": 2022,
        "ended_at": 2025,
        "description": "Completed senior high school education with a growing focus on informatics and academic competitions.",
        "display_order": 2,
    },
)

Educations.objects.update_or_create(
    institution="SMP Islam Raudhatul Jannah",
    defaults={
        "level": "SMP",
        "started_at": 2019,
        "ended_at": 2022,
        "description": "Completed junior high school education at SMP Islam Raudhatul Jannah.",
        "display_order": 3,
    },
)

Achievements.objects.update_or_create(
    title="Indonesian National Olympiad in Informatics at Provincial Level (OSN-P)",
    year=2024,
    organization="Pusat Prestasi Nasional",
    defaults={
        "rank": Achievements.Rank.SILVER,
        "description": "Ranked second among participants in West Sumatra at the provincial-level Informatics Olympiad.",
        "display_order": 1,
    },
)

Achievements.objects.update_or_create(
    title="Indonesian National Olympiad in Informatics at City Level (OSN-K)",
    year=2024,
    organization="Pusat Prestasi Nasional",
    defaults={
        "rank": Achievements.Rank.GOLD,
        "description": "Ranked first at the city-level selection for the Indonesian National Olympiad in Informatics.",
        "display_order": 2,
    },
)

print("Seed data completed.")
