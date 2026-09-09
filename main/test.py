from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Experience


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
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertQuerySetEqual(
            response.context["experience_list"], [self.experience]
        )
        self.assertContains(response, "<article ", count=1)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.organization)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "May 2026 &mdash; Present")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertQuerySetEqual(response.context["experience_list"], [])
        self.assertContains(response, "Recent Experiences")
        self.assertNotContains(response, "<article ")

    def test_completed_experience(self):
        self.experience.ended_at = date(2026, 7, 1)
        self.experience.save()
        self.experience.refresh_from_db()
        response = self.client.get(reverse("main:show_experience"))

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
        response = self.client.get(reverse("main:show_experience"))

        self.assertQuerySetEqual(
            response.context["experience_list"],
            [self.experience, completed_experience],
            ordered=False,
        )
        self.assertContains(response, "<article ", count=2)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, completed_experience.title)
        self.assertContains(response, "May 2026 &mdash; Present")
        self.assertContains(response, "June 2026 &mdash; July 2026")
