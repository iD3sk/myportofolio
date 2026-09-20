import os
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
django.setup()

from main.models import Achievements, Educations, Experience


Experience.objects.update_or_create(
    title="Local Volunteer",
    organization="iGV Summer Project 2026 by AIESEC",
    defaults={
        "org_logo": "",
        "location": "Depok",
        "description": "Delivered SDG 15 education sessions across five schools in Jakarta and Depok, led a beach cleanup at Bokor Island with BKSDA, and visited more than ten partner organizations to build environmental and social awareness.",
        "started_at": date(2026, 6, 1),
        "ended_at": date(2026, 7, 1),
        "skills": "Environmental Education, SDG 15, Volunteering",
    },
)

Experience.objects.update_or_create(
    title="Staff of IT Force Division",
    organization="Forum Ukhuwah dan Kajian Islam Fasilkom UI",
    defaults={
        "org_logo": "",
        "location": "Depok, Jawa Barat",
        "description": "Designed the curriculum and timeline for an internal class program, coordinated updates and assignments, and developed frontend and backend features for FUKI's learning-resources website.",
        "started_at": date(2026, 5, 1),
        "ended_at": None,
        "skills": "Curriculum Design, Frontend, Backend",
    },
)

Experience.objects.update_or_create(
    title="Staff of Academic and Profession",
    organization="BEM Fakultas Ilmu Komputer Universitas Indonesia",
    defaults={
        "org_logo": "",
        "location": "Depok, Jawa Barat",
        "description": "Managed Ajar.in, a peer-mentoring program connecting students to support academic learning.",
        "started_at": date(2026, 5, 1),
        "ended_at": None,
        "skills": "Peer Mentoring, Program Management",
    },
)

Experience.objects.update_or_create(
    title="Staff of Academic",
    organization="Dasar-Dasar Pemrograman",
    defaults={
        "org_logo": "",
        "location": "Depok, Jawa Barat",
        "description": "Created learning modules on basic programming concepts with Python and developed quiz problems for the course.",
        "started_at": date(2026, 5, 1),
        "ended_at": None,
        "skills": "Python, Learning Materials, Quiz Development, Teaching",
    },
)

Experience.objects.update_or_create(
    title="Staff of Data Science Academy",
    organization="COMPFEST",
    defaults={
        "org_logo": "",
        "location": "Depok, Jawa Barat",
        "description": "Curated program content and selected participants for the Data Science Academy.",
        "started_at": date(2026, 4, 1),
        "ended_at": None,
        "skills": "Content Curation, Participant Selection",
    },
)

Experience.objects.update_or_create(
    title="Staff of Mentor and Mentees Division",
    organization="BETIS Fasilkom UI 2026",
    defaults={
        "org_logo": "",
        "location": "Depok, Jawa Barat",
        "description": "Onboarded new mentees, coordinated and led regular group mentoring sessions, and reviewed academic progress to provide targeted feedback.",
        "started_at": date(2026, 1, 1),
        "ended_at": None,
        "skills": "Mentoring, Onboarding, Academic Feedback",
    },
)


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
        "org_logo": "img/osn.webp",
    },
)

Achievements.objects.update_or_create(
    title="Indonesian National Olympiad in Informatics at City Level (OSN-K)",
    year=2024,
    organization="Pusat Prestasi Nasional",
    defaults={
        "rank": Achievements.Rank.GOLD,
        "description": "Ranked first at the city-level selection for the Indonesian National Olympiad in Informatics.",
        "org_logo": "img/osn.webp",
    },
)

print("Seed data completed.")
