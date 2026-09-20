from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Achievements, Educations


class TestMain(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            organization="Fakultas Ilmu Komputer Universitas Indonesia",
            location="Depok, Jawa Barat",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at=date(2026, 5, 1),
            skills=["Django", "Teaching"],
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "Fiqhi Deski Ismail")
        self.assertContains(response, "2506534245")
        self.assertNotContains(response, self.experience.title)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.experience.refresh_from_db()

        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.started_at, date(2026, 5, 1))
        self.assertEqual(self.experience.location, "Depok, Jawa Barat")
        self.assertEqual(self.experience.skills, ["Django", "Teaching"])
        self.assertEqual(self.experience.org_logo, "")
        self.assertIsNone(self.experience.ended_at)
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertQuerySetEqual(
            response.context["experience_list"], [self.experience]
        )
        self.assertContains(response, "<article", count=1)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.organization)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "May 2026 &mdash; Present")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertQuerySetEqual(response.context["experience_list"], [])
        self.assertContains(response, "Recent Experiences")
        self.assertNotContains(response, "<article")

    def test_completed_experience(self):
        self.experience.ended_at = date(2026, 7, 1)
        self.experience.save()
        self.experience.refresh_from_db()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "May 2026 &mdash; July 2026")
        self.assertNotContains(response, "Present")

    def test_experience_page_displays_multiple_experiences(self):
        completed_experience = Experience.objects.create(
            title="Local Volunteer",
            organization="iGV Summer Project 2026 by AIESEC",
            description="Delivered environmental education sessions.",
            started_at=date(2026, 6, 1),
            ended_at=date(2026, 7, 1),
        )
        response = self.client.get(reverse("main:show_experiences"))

        self.assertQuerySetEqual(
            response.context["experience_list"],
            [self.experience, completed_experience],
            ordered=False,
        )
        self.assertContains(response, "<article", count=2)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, completed_experience.title)
        self.assertContains(response, "May 2026 &mdash; Present")
        self.assertContains(response, "June 2026 &mdash; July 2026")

    def test_update_experience_page_prefills_existing_data(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Edit Experience")
        self.assertContains(response, self.experience.title)

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Updated Experience",
                "organization": self.experience.organization,
                "org_logo": "",
                "location": self.experience.location,
                "description": self.experience.description,
                "started_at": "2026-05-01",
                "ended_at": "",
                "skills": "Django, Teaching",
            },
        )

        self.assertRedirects(response, reverse("main:show_experiences"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Experience")
class TestAbout(TestCase):
    def setUp(self):
        self.ui = Educations.objects.create(
            level="Undergraduate",
            institution="Universitas Indonesia",
            program="S1 Ilmu Komputer",
            started_at=2025,
            description="Currently studying Computer Science.",
            display_order=1,
        )
        self.sma = Educations.objects.create(
            level="SMA",
            institution="SMAN 1 Padang Panjang",
            started_at=2022,
            ended_at=2025,
            description="Completed senior high school education.",
            display_order=2,
        )
        self.smp = Educations.objects.create(
            level="SMP",
            institution="SMP Islam Raudhatul Jannah",
            started_at=2019,
            ended_at=2022,
            description="Completed junior high school education.",
            display_order=3,
        )
        self.gold_achievement = Achievements.objects.create(
            title="Gold Achievement",
            organization="Competition Organizer",
            year=2024,
            rank=Achievements.Rank.GOLD,
            description="Won first place.",
            display_order=1,
        )
        self.bronze_achievement = Achievements.objects.create(
            title="Bronze Achievement",
            organization="Another Organizer",
            year=2025,
            rank=Achievements.Rank.BRONZE,
            description="Won third place.",
            display_order=2,
        )

    def test_about_page(self):
        response = self.client.get(reverse("main:show_about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertEqual(response.context["UI"], self.ui)
        self.assertEqual(response.context["SMA"], self.sma)
        self.assertEqual(response.context["SMP"], self.smp)

    def test_education_data(self):
        response = self.client.get(reverse("main:show_about"))

        self.assertContains(response, self.ui.institution)
        self.assertContains(response, self.ui.program)
        self.assertContains(response, self.sma.institution)
        self.assertContains(response, self.smp.institution)

    def test_achievement_data(self):
        response = self.client.get(reverse("main:show_about"))

        self.assertContains(response, self.gold_achievement.title)
        self.assertContains(response, self.gold_achievement.organization)
        self.assertContains(response, self.gold_achievement.description)
        self.assertContains(response, "Gold")
        self.assertContains(response, "Bronze")

    def test_achievements_are_ordered_by_display_order_then_year(self):
        newer_gold = Achievements.objects.create(
            title="Newer Gold Achievement",
            organization="Competition Organizer",
            year=2026,
            rank=Achievements.Rank.GOLD,
            display_order=1,
        )

        response = self.client.get(reverse("main:show_about"))

        self.assertQuerySetEqual(
            response.context["achievement_list"],
            [newer_gold, self.gold_achievement, self.bronze_achievement],
        )

    def test_ongoing_education(self):
        self.assertTrue(self.ui.is_on_going)
        self.assertFalse(self.sma.is_on_going)

    def test_empty_achievement_state(self):
        Achievements.objects.all().delete()

        response = self.client.get(reverse("main:show_about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No achievement available")

    def test_about_page_with_empty_database(self):
        Educations.objects.all().delete()
        Achievements.objects.all().delete()

        response = self.client.get(reverse("main:show_about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No achievement available")
