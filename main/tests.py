from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Achievements, Educations


class TestAboutAjax(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        self.regular = User.objects.create_user(
            username="regular", password="test-password"
        )
        self.achievement = Achievements.objects.create(
            title="National Programming Contest",
            organization="Competition Organizer",
            year=2025,
            rank=Achievements.Rank.GOLD,
            description="Won the national final.",
            org_logo="img/competition.webp",
        )

    def test_about_page_renders_education_and_ajax_controls(self):
        education = Educations.objects.create(
            level="Undergraduate",
            institution="Universitas Indonesia",
            program="S1 Ilmu Komputer",
            started_at=2025,
        )

        response = self.client.get(reverse("main:show_about"), {"title": "contest"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")
        self.assertContains(response, education.institution)
        self.assertContains(response, 'id="achievement-grid"')
        self.assertContains(response, reverse("main:get_achievement_json"))
        self.assertContains(response, reverse("main:create_achievement_ajax"))
        self.assertEqual(response.context["title_query"], "contest")
        self.assertNotContains(response, self.achievement.title)

    def test_achievement_json_returns_fields_and_like_state(self):
        self.client.force_login(self.regular)
        self.achievement.liked_by.add(self.regular)

        response = self.client.get(reverse("main:get_achievement_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            response.json(),
            [
                {
                    "pk": str(self.achievement.pk),
                    "fields": {
                        "title": self.achievement.title,
                        "year": self.achievement.year,
                        "organization": self.achievement.organization,
                        "org_logo": self.achievement.org_logo,
                        "rank": self.achievement.rank,
                        "rank_display": "Gold",
                        "description": self.achievement.description,
                        "is_liked": True,
                        "like_count": 1,
                        "liked_by_names": "regular",
                    },
                }
            ],
        )

    def test_achievement_json_filters_title_case_insensitively_and_orders_newest(self):
        older = Achievements.objects.create(
            title="Regional Programming Contest",
            organization="Regional Organizer",
            year=2023,
            rank=Achievements.Rank.SILVER,
        )
        Achievements.objects.create(
            title="Science Olympiad",
            organization="Science Organizer",
            year=2026,
            rank=Achievements.Rank.FINALIST,
        )

        response = self.client.get(
            reverse("main:get_achievement_json"), {"title": "PROGRAMMING"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["pk"] for item in response.json()],
            [str(self.achievement.pk), str(older.pk)],
        )

    def test_achievement_json_returns_empty_list_when_no_match(self):
        response = self.client.get(
            reverse("main:get_achievement_json"), {"title": "unmatched"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class TestAchievementAjaxCreate(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        self.regular = User.objects.create_user(
            username="regular", password="test-password"
        )
        self.url = reverse("main:create_achievement_ajax")
        self.valid_data = {
            "title": "International Programming Contest",
            "year": "2026",
            "organization": "International Organizer",
            "rank": Achievements.Rank.SILVER,
            "description": "Placed second in the final.",
            "org_logo": "img/competition.webp",
        }

    def test_superuser_can_create_achievement(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 201)
        created = Achievements.objects.get(title=self.valid_data["title"])
        self.assertEqual(response.json(), {
            "message": "New achievement has been added.",
            "pk": str(created.pk),
        })
        self.assertEqual(created.year, 2026)
        self.assertEqual(created.rank, Achievements.Rank.SILVER)

    def test_invalid_data_returns_field_errors_without_creating_record(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.url, self.valid_data | {"title": "", "year": "not-a-year"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertIn("year", response.json()["errors"])
        self.assertFalse(Achievements.objects.exists())

    def test_guests_and_regular_users_cannot_create_achievement(self):
        for user in (None, self.regular):
            with self.subTest(user=user):
                if user is not None:
                    self.client.force_login(user)

                response = self.client.post(self.url, self.valid_data)

                self.assertEqual(response.status_code, 403)
                self.assertFalse(Achievements.objects.exists())
                self.client.logout()

    def test_create_endpoint_only_accepts_post(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Achievements.objects.exists())

    def test_create_endpoint_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)

        response = csrf_client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Achievements.objects.exists())


class TestAchievementLike(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="regular", password="test-password"
        )
        self.achievement = Achievements.objects.create(
            title="Programming Contest",
            organization="Competition Organizer",
            year=2025,
            rank=Achievements.Rank.GOLD,
        )
        self.url = reverse(
            "main:toggle_achievement_like", args=[self.achievement.pk]
        )

    def test_authenticated_user_can_toggle_achievement_like(self):
        self.client.force_login(self.user)

        liked_response = self.client.post(self.url)
        self.assertEqual(liked_response.status_code, 200)
        self.assertEqual(liked_response.json(), {"is_liked": True, "like_count": 1})
        self.assertTrue(self.achievement.liked_by.filter(pk=self.user.pk).exists())

        unliked_response = self.client.post(self.url)
        self.assertEqual(unliked_response.status_code, 200)
        self.assertEqual(
            unliked_response.json(), {"is_liked": False, "like_count": 0}
        )
        self.assertFalse(self.achievement.liked_by.filter(pk=self.user.pk).exists())

    def test_guest_is_redirected_and_get_is_not_allowed(self):
        guest_response = self.client.post(self.url)
        self.assertEqual(guest_response.status_code, 302)

        self.client.force_login(self.user)
        get_response = self.client.get(self.url)
        self.assertEqual(get_response.status_code, 405)

