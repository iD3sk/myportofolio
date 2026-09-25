import json
from datetime import date

from django.test import RequestFactory, TestCase
from django.urls import reverse

from main.models import Achievements, Educations, Experience
from main.views import get_achievement_json


class TestMain(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            organization="Fakultas Ilmu Komputer Universitas Indonesia",
            location="Depok, Jawa Barat",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at=date(2026, 5, 1),
            skills="Django, Teaching",
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
        self.assertEqual(self.experience.skills, "Django, Teaching")
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
        )
        self.sma = Educations.objects.create(
            level="SMA",
            institution="SMAN 1 Padang Panjang",
            started_at=2022,
            ended_at=2025,
            description="Completed senior high school education.",
        )
        self.smp = Educations.objects.create(
            level="SMP",
            institution="SMP Islam Raudhatul Jannah",
            started_at=2019,
            ended_at=2022,
            description="Completed junior high school education.",
        )
        self.gold_achievement = Achievements.objects.create(
            title="Gold Achievement",
            organization="Competition Organizer",
            year=2024,
            rank=Achievements.Rank.GOLD,
            description="Won first place.",
        )
        self.bronze_achievement = Achievements.objects.create(
            title="Bronze Achievement",
            organization="Another Organizer",
            year=2025,
            rank=Achievements.Rank.BRONZE,
            description="Won third place.",
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


class TestAchievementManagement(TestCase):
    def setUp(self):
        self.achievement = Achievements.objects.create(
            title="National Programming Contest",
            organization="Competition Organizer",
            org_logo="img/osn.webp",
            year=2025,
            rank=Achievements.Rank.GOLD,
            description="Won the national final.",
        )
        self.valid_data = {
            "title": "International Programming Contest",
            "organization": "International Organizer",
            "org_logo": "img/osn.webp",
            "year": 2026,
            "rank": Achievements.Rank.SILVER,
            "description": "Placed second in the final.",
        }

    def test_create_achievement_page_displays_form(self):
        response = self.client.get(reverse("main:create_achievement"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")
        self.assertContains(response, "Add Achievement")
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="rank"')

    def test_create_achievement_with_valid_data(self):
        response = self.client.post(
            reverse("main:create_achievement"), self.valid_data
        )

        self.assertRedirects(response, reverse("main:show_about"))
        created_achievement = Achievements.objects.get(
            title=self.valid_data["title"]
        )
        self.assertEqual(created_achievement.year, self.valid_data["year"])
        self.assertEqual(created_achievement.rank, self.valid_data["rank"])
        self.assertEqual(
            created_achievement.org_logo, self.valid_data["org_logo"]
        )

    def test_create_achievement_with_invalid_data_shows_errors(self):
        invalid_data = self.valid_data | {"title": "", "year": "not-a-year"}

        response = self.client.post(
            reverse("main:create_achievement"), invalid_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")
        self.assertFormError(
            response.context["form"], "title", "This field is required."
        )
        self.assertFormError(
            response.context["form"], "year", "Enter a whole number."
        )
        self.assertFalse(
            Achievements.objects.filter(
                organization=self.valid_data["organization"]
            ).exists()
        )

    def test_update_achievement_page_prefills_existing_data(self):
        response = self.client.get(
            reverse("main:update_achievement", args=[self.achievement.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")
        self.assertContains(response, "Edit Achievement")
        self.assertContains(response, self.achievement.title)
        self.assertEqual(response.context["form"].instance, self.achievement)

    def test_update_achievement_with_valid_data(self):
        response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.id]),
            self.valid_data,
        )

        self.assertRedirects(response, reverse("main:show_about"))
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, self.valid_data["title"])
        self.assertEqual(self.achievement.rank, Achievements.Rank.SILVER)
        self.assertEqual(Achievements.objects.count(), 1)

    def test_update_achievement_with_invalid_data_preserves_record(self):
        response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.id]),
            self.valid_data | {"rank": "platinum"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "rank",
            "Select a valid choice. platinum is not one of the available choices.",
        )
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "National Programming Contest")
        self.assertEqual(self.achievement.rank, Achievements.Rank.GOLD)

    def test_delete_achievement_requires_post(self):
        response = self.client.get(
            reverse("main:delete_achievement", args=[self.achievement.id])
        )

        self.assertRedirects(response, reverse("main:show_about"))
        self.assertTrue(
            Achievements.objects.filter(pk=self.achievement.id).exists()
        )

    def test_delete_achievement_with_post(self):
        response = self.client.post(
            reverse("main:delete_achievement", args=[self.achievement.id])
        )

        self.assertRedirects(response, reverse("main:show_about"))
        self.assertFalse(
            Achievements.objects.filter(pk=self.achievement.id).exists()
        )

    def test_update_and_delete_nonexistent_achievement_return_404(self):
        missing_id = "00000000-0000-0000-0000-000000000000"

        update_response = self.client.get(
            reverse("main:update_achievement", args=[missing_id])
        )
        delete_response = self.client.post(
            reverse("main:delete_achievement", args=[missing_id])
        )

        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)

    def test_about_page_filters_achievements_by_title_case_insensitively(self):
        matching_achievement = Achievements.objects.create(
            title="Regional Science Olympiad",
            organization="Science Organizer",
            year=2024,
            rank=Achievements.Rank.FINALIST,
        )

        response = self.client.get(
            reverse("main:show_about"), {"title": "science"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title_query"], "science")
        self.assertEqual(
            response.context["achievement_list"], [matching_achievement]
        )
        self.assertContains(response, matching_achievement.title)
        self.assertNotContains(response, self.achievement.title)

    def test_achievement_json_filters_and_orders_newest_first(self):
        older_achievement = Achievements.objects.create(
            title="Programming Contest Finalist",
            organization="Another Organizer",
            year=2023,
            rank=Achievements.Rank.FINALIST,
        )

        request = RequestFactory().get(
            "/api/achievement/", {"title": "programming"}
        )
        response = get_achievement_json(request)
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            [item["pk"] for item in payload],
            [str(self.achievement.id), str(older_achievement.id)],
        )
