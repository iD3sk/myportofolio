from datetime import date

from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse

from main.models import Achievements, Educations, Experience


class TestMain(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
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
        api_response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, 'id="experience-grid"')
        self.assertContains(response, reverse("main:get_experience_json"))
        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response["Content-Type"], "application/json")
        self.assertEqual(
            api_response.json(),
            [
                {
                    "pk": str(self.experience.id),
                    "fields": {
                        "title": self.experience.title,
                        "organization": self.experience.organization,
                        "org_logo": "",
                        "location": self.experience.location,
                        "description": self.experience.description,
                        "started_at": "2026-05-01",
                        "ended_at": None,
                        "skills": self.experience.skills,
                        "is_liked": False,
                        "like_count": 0,
                        "liked_by_names": "",
                    },
                }
            ],
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))
        api_response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, "Recent Experiences")
        self.assertContains(response, 'id="experience-empty"')
        self.assertEqual(api_response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = date(2026, 7, 1)
        self.experience.save()
        self.experience.refresh_from_db()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertEqual(response.json()[0]["fields"]["started_at"], "2026-05-01")
        self.assertEqual(response.json()[0]["fields"]["ended_at"], "2026-07-01")

    def test_experience_page_displays_multiple_experiences(self):
        completed_experience = Experience.objects.create(
            title="Local Volunteer",
            organization="iGV Summer Project 2026 by AIESEC",
            description="Delivered environmental education sessions.",
            started_at=date(2026, 6, 1),
            ended_at=date(2026, 7, 1),
        )
        response = self.client.get(reverse("main:get_experience_json"))

        items = {item["pk"]: item["fields"] for item in response.json()}
        self.assertEqual(
            set(items), {str(self.experience.id), str(completed_experience.id)}
        )
        self.assertEqual(items[str(self.experience.id)]["title"], self.experience.title)
        self.assertEqual(items[str(completed_experience.id)]["ended_at"], "2026-07-01")

    def test_experience_json_filters_titles_case_insensitively(self):
        Experience.objects.create(
            title="Local Volunteer",
            organization="AIESEC",
            description="Environmental education.",
            started_at=date(2026, 6, 1),
        )

        response = self.client.get(
            reverse("main:get_experience_json"), {"title": "TEACHING"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        response = self.client.get(
            reverse("main:get_experience_json"), {"title": "asisten"}
        )
        self.assertEqual(
            [item["pk"] for item in response.json()], [str(self.experience.id)]
        )

    def test_update_experience_page_prefills_existing_data(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Edit Experience")
        self.assertContains(response, self.experience.title)

    def test_update_experience(self):
        self.client.force_login(self.owner)
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


class TestExperienceAjaxCreate(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        self.regular = User.objects.create_user(
            username="regular", password="test-password"
        )
        self.url = reverse("main:create_experience_ajax")
        self.valid_data = {
            "title": "Teaching Assistant",
            "organization": "Universitas Indonesia",
            "org_logo": "",
            "location": "Depok",
            "description": "Teaching web development.",
            "started_at": "2026-05-01",
            "ended_at": "",
            "skills": "Django, Teaching",
        }

    def test_owner_can_create_experience(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 201)
        experience = Experience.objects.get(title=self.valid_data["title"])
        self.assertEqual(response.json()["pk"], str(experience.pk))
        self.assertEqual(experience.organization, self.valid_data["organization"])

    def test_invalid_data_returns_errors_without_creating_experience(self):
        self.client.force_login(self.owner)

        response = self.client.post(self.url, self.valid_data | {"title": ""})

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertFalse(Experience.objects.exists())

    def test_guests_and_regular_users_cannot_create_experience(self):
        for user in [None, self.regular]:
            with self.subTest(user=user):
                if user is not None:
                    self.client.force_login(user)

                response = self.client.post(self.url, self.valid_data)
                self.assertEqual(response.status_code, 403)
                self.assertFalse(Experience.objects.exists())
                self.client.logout()

    def test_create_endpoint_requires_post_and_csrf(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        self.assertEqual(csrf_client.post(self.url, self.valid_data).status_code, 403)
        self.assertFalse(Experience.objects.exists())

        page = csrf_client.get(reverse("main:show_experiences"))
        csrf_token = page.cookies["csrftoken"].value
        response = csrf_client.post(
            self.url, self.valid_data | {"csrfmiddlewaretoken": csrf_token}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Experience.objects.filter(title=self.valid_data["title"]).exists()
        )


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
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        self.client.force_login(self.owner)
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
        response = self.client.post(reverse("main:create_achievement"), self.valid_data)

        self.assertRedirects(response, reverse("main:show_about"))
        created_achievement = Achievements.objects.get(title=self.valid_data["title"])
        self.assertEqual(created_achievement.year, self.valid_data["year"])
        self.assertEqual(created_achievement.rank, self.valid_data["rank"])
        self.assertEqual(created_achievement.org_logo, self.valid_data["org_logo"])

    def test_create_achievement_with_invalid_data_shows_errors(self):
        invalid_data = self.valid_data | {"title": "", "year": "not-a-year"}

        response = self.client.post(reverse("main:create_achievement"), invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")
        self.assertFormError(
            response.context["form"], "title", "This field is required."
        )
        self.assertFormError(response.context["form"], "year", "Enter a whole number.")
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

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Achievements.objects.filter(pk=self.achievement.id).exists())

    def test_delete_achievement_with_post(self):
        response = self.client.post(
            reverse("main:delete_achievement", args=[self.achievement.id])
        )

        self.assertRedirects(response, reverse("main:show_about"))
        self.assertFalse(Achievements.objects.filter(pk=self.achievement.id).exists())

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

        response = self.client.get(reverse("main:show_about"), {"title": "science"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title_query"], "science")
        self.assertQuerySetEqual(
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

        response = self.client.get(
            reverse("main:get_achievement_json"), {"title": "programming"}
        )
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            [item["pk"] for item in payload],
            [str(self.achievement.id), str(older_achievement.id)],
        )


class TestAuthorizationAndLikes(TestCase):
    def setUp(self):
        self.regular = User.objects.create_user(
            username="regular", password="test-password"
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password"
        )
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password"
        )
        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)

        self.experience = Experience.objects.create(
            title="Teaching Assistant",
            organization="Universitas Indonesia",
            location="Depok",
            description="Teaching web development.",
            started_at=date(2026, 5, 1),
            skills="Django, Teaching",
        )
        self.achievement = Achievements.objects.create(
            title="Programming Contest",
            organization="Competition Organizer",
            year=2025,
            rank=Achievements.Rank.GOLD,
            description="Won the final.",
        )

    def test_guest_is_redirected_from_every_mutating_action(self):
        requests = [
            ("get", reverse("main:create_experience")),
            ("get", reverse("main:update_experience", args=[self.experience.id])),
            ("post", reverse("main:delete_experience", args=[self.experience.id])),
            ("post", reverse("main:toggle_experience_like", args=[self.experience.id])),
            ("get", reverse("main:create_achievement")),
            ("get", reverse("main:update_achievement", args=[self.achievement.id])),
            ("post", reverse("main:delete_achievement", args=[self.achievement.id])),
            (
                "post",
                reverse("main:toggle_achievement_like", args=[self.achievement.id]),
            ),
        ]

        for method, url in requests:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/login/?next="))

    def test_regular_user_cannot_create_update_or_delete(self):
        self.client.force_login(self.regular)
        requests = [
            ("get", reverse("main:create_experience")),
            ("get", reverse("main:update_experience", args=[self.experience.id])),
            ("post", reverse("main:delete_experience", args=[self.experience.id])),
            ("get", reverse("main:create_achievement")),
            ("get", reverse("main:update_achievement", args=[self.achievement.id])),
            ("post", reverse("main:delete_achievement", args=[self.achievement.id])),
        ]

        for method, url in requests:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 403)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        experience_response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Updated by Editor",
                "organization": self.experience.organization,
                "org_logo": "",
                "location": self.experience.location,
                "description": self.experience.description,
                "started_at": "2026-05-01",
                "ended_at": "",
                "skills": self.experience.skills,
            },
        )
        achievement_response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.id]),
            {
                "title": "Achievement Updated by Editor",
                "organization": self.achievement.organization,
                "org_logo": "",
                "year": self.achievement.year,
                "rank": self.achievement.rank,
                "description": self.achievement.description,
            },
        )

        self.assertRedirects(experience_response, reverse("main:show_experiences"))
        self.assertRedirects(achievement_response, reverse("main:show_about"))
        self.experience.refresh_from_db()
        self.achievement.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by Editor")
        self.assertEqual(self.achievement.title, "Achievement Updated by Editor")

        forbidden_requests = [
            ("get", reverse("main:create_experience")),
            ("post", reverse("main:delete_experience", args=[self.experience.id])),
            ("get", reverse("main:create_achievement")),
            ("post", reverse("main:delete_achievement", args=[self.achievement.id])),
        ]
        for method, url in forbidden_requests:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 403)

    def test_superuser_has_full_crud_access(self):
        self.client.force_login(self.owner)

        self.assertEqual(
            self.client.get(reverse("main:create_experience")).status_code, 200
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_experience", args=[self.experience.id])
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_achievement")).status_code, 200
        )
        self.assertEqual(
            self.client.get(
                reverse("main:update_achievement", args=[self.achievement.id])
            ).status_code,
            200,
        )
        self.assertRedirects(
            self.client.post(
                reverse("main:delete_experience", args=[self.experience.id])
            ),
            reverse("main:show_experiences"),
        )
        self.assertRedirects(
            self.client.post(
                reverse("main:delete_achievement", args=[self.achievement.id])
            ),
            reverse("main:show_about"),
        )

    def test_authenticated_user_can_toggle_each_like(self):
        self.client.force_login(self.regular)
        cases = [
            (
                self.experience,
                reverse("main:toggle_experience_like", args=[self.experience.id]),
            ),
            (
                self.achievement,
                reverse("main:toggle_achievement_like", args=[self.achievement.id]),
            ),
        ]

        for item, url in cases:
            with self.subTest(url=url):
                response = self.client.post(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"is_liked": True, "like_count": 1})
                self.assertTrue(item.liked_by.filter(pk=self.regular.pk).exists())
                self.assertEqual(item.liked_by.count(), 1)

                response = self.client.post(url)
                self.assertEqual(response.json(), {"is_liked": False, "like_count": 0})
                self.assertFalse(item.liked_by.filter(pk=self.regular.pk).exists())
                self.assertEqual(item.liked_by.count(), 0)

    def test_like_endpoints_only_accept_post(self):
        self.client.force_login(self.regular)
        urls = [
            reverse("main:toggle_experience_like", args=[self.experience.id]),
            reverse("main:toggle_achievement_like", args=[self.achievement.id]),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 405)

    def test_like_endpoints_require_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.regular)
        urls = [
            reverse("main:toggle_experience_like", args=[self.experience.id]),
            reverse("main:toggle_achievement_like", args=[self.achievement.id]),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(csrf_client.post(url).status_code, 403)

    def test_experience_page_exposes_permissions_to_card_renderer(self):
        url = reverse("main:show_experiences")
        cases = [
            (None, False, False, False),
            (self.regular, True, False, False),
            (self.editor, True, True, False),
            (self.owner, True, True, True),
        ]

        for user, authenticated, can_update, can_delete in cases:
            with self.subTest(user=user):
                if user is None:
                    self.client.logout()
                else:
                    self.client.force_login(user)

                response = self.client.get(url)
                self.assertContains(
                    response,
                    f'const IS_AUTHENTICATED = "{str(authenticated).lower()}"',
                )
                self.assertContains(
                    response, f'const CAN_UPDATE = "{str(can_update).lower()}"'
                )
                self.assertContains(
                    response, f'const CAN_DELETE = "{str(can_delete).lower()}"'
                )
                if can_delete:
                    self.assertContains(response, 'id="add-experience-modal"')
                else:
                    self.assertNotContains(response, 'id="add-experience-modal"')

    def test_about_page_action_controls_match_each_role(self):
        urls = {
            "create": reverse("main:create_achievement"),
            "edit": reverse("main:update_achievement", args=[self.achievement.id]),
            "delete": reverse("main:delete_achievement", args=[self.achievement.id]),
            "like": reverse("main:toggle_achievement_like", args=[self.achievement.id]),
        }

        response = self.client.get(reverse("main:show_about"))
        self.assertContains(response, "0 likes")
        for action_url in urls.values():
            self.assertNotContains(response, action_url)

        for user, visible, hidden in [
            (self.regular, ("like",), ("create", "edit", "delete")),
            (self.editor, ("like", "edit"), ("create", "delete")),
            (self.owner, tuple(urls), ()),
        ]:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(reverse("main:show_about"))
                for action in visible:
                    self.assertContains(response, urls[action])
                for action in hidden:
                    self.assertNotContains(response, urls[action])
                self.client.logout()

    def test_json_exposes_like_state_without_internal_user_ids(self):
        self.experience.liked_by.add(self.regular)
        self.achievement.liked_by.add(self.regular)

        for endpoint in ["main:get_experience_json", "main:get_achievement_json"]:
            with self.subTest(endpoint=endpoint):
                guest_fields = self.client.get(reverse(endpoint)).json()[0]["fields"]
                self.assertFalse(guest_fields["is_liked"])
                self.assertEqual(guest_fields["liked_by_names"], "regular")
                self.assertNotIn("liked_by", guest_fields)

                self.client.force_login(self.regular)
                user_fields = self.client.get(reverse(endpoint)).json()[0]["fields"]
                self.assertTrue(user_fields["is_liked"])
                if endpoint == "main:get_experience_json":
                    self.assertEqual(user_fields["like_count"], 1)
                self.client.logout()
