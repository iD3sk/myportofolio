import uuid

from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class TestExperienceAPI(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username="owner", is_superuser=True)
        self.user = User.objects.create(username="visitor")
        self.payload = {
            "title": "Teaching Assistant", "organization": "UI",
            "description": "Teaching", "location": "Depok",
            "started_at": "2026-01-01", "ended_at": "2026-06-01",
        }
        self.experience = Experience.objects.create(**self.payload)
        self.list_url = reverse("api:experience_list")
        self.detail_url = reverse(
            "api:experience_detail", args=[self.experience.pk],
        )

    def test_public_list_search_and_detail(self):
        response = self.client.get(self.list_url, {"title": "teaching"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)

    def test_anonymous_and_regular_users_cannot_write(self):
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload).status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}).status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload).status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_owner_crud_and_validation(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())
        response = self.client.patch(self.detail_url, {"title": "Updated"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated")
        self.assertEqual(self.experience.organization, "UI")
        self.assertEqual(self.client.patch(self.detail_url, {"ended_at": "2025-01-01"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertEqual(self.client.get(self.detail_url).status_code, 404)

    def test_list_is_empty_when_no_experiences_exist(self):
        Experience.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_search_trims_spaces_and_excludes_nonmatching_objects(self):
        Experience.objects.create(**{**self.payload, "title": "Developer"})
        response = self.client.get(self.list_url, {"title": " TEACHING "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [str(self.experience.pk)])

    def test_detail_exposes_computed_fields_without_sensitive_user_data(self):
        self.experience.liked_by.add(self.user)
        self.experience.skills = "Python, Django, , SQL"
        self.experience.save()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["like_counts"], 1)
        self.assertEqual(response.data["liked_by_name"], "visitor")
        self.assertEqual(response.data["skills_list"], ["Python", "Django", "SQL"])
        self.assertFalse(response.data["is_ongoing"])
        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["liked_by"], [self.user.pk])

    def test_create_rejects_invalid_fields_without_saving(self):
        self.client.force_authenticate(user=self.owner)
        invalid_values = {
            "title": ["", "<b></b>", "x" * 256],
            "description": ["<p></p>"],
            "started_at": ["not-a-date"],
            "ended_at": ["2025-12-31"],
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    response = self.client.post(
                        self.list_url, {**self.payload, field: value}, format="json",
                    )
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.data)
                    self.assertEqual(Experience.objects.count(), 1)

    def test_create_strips_html_from_text(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            {**self.payload, "title": "<b>Assistant</b>", "description": "<p>Teaching</p>"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Assistant")
        self.assertEqual(created.description, "Teaching")

    def test_patch_validates_start_against_existing_end_without_saving(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"started_at": "2026-07-01"}, format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("ended_at", response.data)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.started_at.isoformat(), "2026-01-01")

    def test_patch_accepts_null_end_and_same_day_dates(self):
        self.client.force_authenticate(user=self.owner)
        for ended_at, ongoing in ((None, True), ("2026-01-01", False)):
            with self.subTest(ended_at=ended_at):
                response = self.client.patch(
                    self.detail_url, {"ended_at": ended_at}, format="json",
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["is_ongoing"], ongoing)

    def test_client_cannot_overwrite_id_or_computed_fields(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url,
            {"id": str(uuid.uuid4()), "like_counts": 99,
             "liked_by_name": "fake", "is_ongoing": True, "skills_list": ["fake"]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.experience.pk))
        self.assertEqual(response.data["like_counts"], 0)
        self.assertEqual(response.data["liked_by_name"], "")
        self.assertFalse(response.data["is_ongoing"])
        self.assertEqual(response.data["skills_list"], [])

    def test_missing_object_returns_404_for_each_detail_method(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("api:experience_detail", args=[uuid.uuid4()])
        for method in ("get", "put", "patch", "delete"):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 404)
                self.assertIn("detail", response.data)

    def test_unsupported_methods_return_405(self):
        self.client.force_authenticate(user=self.owner)
        for method, url in (("delete", self.list_url), ("post", self.detail_url)):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 405)

    def test_malformed_json_returns_400_without_saving(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, '{"title":', content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_writes_require_valid_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        request = RequestFactory().get("/")
        token = get_token(request)
        client.cookies["csrftoken"] = request.META["CSRF_COOKIE"]

        for headers in ({}, {"HTTP_X_CSRFTOKEN": "invalid"}):
            with self.subTest(headers=headers):
                response = client.post(self.list_url, self.payload, format="json", **headers)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(Experience.objects.count(), 1)

        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)
from django.contrib.auth.models import Group
from main.models import Achievements


class TestPortfolioAPIRolesAndLikes(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username="portfolio-owner", is_superuser=True)
        self.visitor = User.objects.create(username="reader")
        self.editor = User.objects.create(username="editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.resources = [
            ("experience", Experience, {
                "title": "Experience", "organization": "UI", "location": "Depok",
                "description": "Work", "started_at": "2026-01-01",
            }),
            ("achievement", Achievements, {
                "title": "Award", "organization": "UI", "year": 2026,
                "rank": "gold", "description": "Prize",
            }),
        ]

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        for name, model, payload in self.resources:
            with self.subTest(resource=name):
                item = model.objects.create(**payload)
                url = reverse(f"api:{name}_detail", args=[item.pk])
                self.assertEqual(self.client.post(reverse(f"api:{name}_list"), payload).status_code, 403)
                self.assertEqual(self.client.patch(url, {"title": "Edited"}).status_code, 200)
                self.assertEqual(self.client.put(url, payload).status_code, 200)
                self.assertEqual(self.client.delete(url).status_code, 403)
                self.assertTrue(model.objects.filter(pk=item.pk).exists())

    def test_achievement_crud_search_and_rank_display(self):
        self.client.force_authenticate(self.owner)
        url = reverse("api:achievement_list")
        payload = self.resources[1][2]
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        detail = reverse("api:achievement_detail", args=[response.data["id"]])
        self.assertEqual(response.data["rank_display"], "Gold")
        self.assertEqual(self.client.get(detail).status_code, 200)
        self.assertEqual(len(self.client.get(url, {"title": "AWARD"}).data), 1)
        self.assertEqual(self.client.get(url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.patch(detail, {"rank": "invalid"}).status_code, 400)
        self.assertEqual(self.client.patch(detail, {"title": "<b></b>"}).status_code, 400)
        self.assertEqual(self.client.delete(detail).status_code, 204)
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_like_toggle_is_scoped_to_logged_in_user(self):
        for name, model, payload in self.resources:
            with self.subTest(resource=name):
                item = model.objects.create(**payload)
                item.liked_by.add(self.owner)
                url = reverse(f"api:{name}_like", args=[item.pk])
                self.client.force_authenticate(None)
                self.assertEqual(self.client.post(url).status_code, 403)
                self.client.force_authenticate(self.visitor)
                self.assertEqual(self.client.get(url).status_code, 405)
                self.assertEqual(self.client.post(url).data, {"is_liked": True, "like_count": 2})
                detail = self.client.get(reverse(f"api:{name}_detail", args=[item.pk]))
                self.assertTrue(detail.data["is_liked"])
                self.assertEqual(self.client.post(url).data, {"is_liked": False, "like_count": 1})
                self.assertTrue(item.liked_by.filter(pk=self.owner.pk).exists())
                missing = reverse(f"api:{name}_like", args=[uuid.uuid4()])
                self.assertEqual(self.client.post(missing).status_code, 404)

    def test_client_cannot_assign_likes_through_update(self):
        self.client.force_authenticate(self.owner)
        for name, model, payload in self.resources:
            with self.subTest(resource=name):
                item = model.objects.create(**payload)
                url = reverse(f"api:{name}_detail", args=[item.pk])
                response = self.client.patch(url, {"liked_by": [self.visitor.pk]}, format="json")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(item.liked_by.count(), 0)

    def test_templates_use_new_api_contract(self):
        for page, name in (("main:show_experiences", "experience"), ("main:show_about", "achievement")):
            with self.subTest(page=page):
                response = self.client.get(reverse(page))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, reverse(f"api:{name}_list"))
                self.assertContains(response, "data-delete-form")
                self.assertContains(response, 'method: "DELETE"')
                self.assertNotContains(response, "item.fields")
                self.assertNotContains(response, "item.pk")

    def test_like_session_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.visitor)
        request = RequestFactory().get("/")
        token = get_token(request)
        client.cookies["csrftoken"] = request.META["CSRF_COOKIE"]
        for name, model, payload in self.resources:
            with self.subTest(resource=name):
                item = model.objects.create(**payload)
                url = reverse(f"api:{name}_like", args=[item.pk])
                self.assertEqual(client.post(url).status_code, 403)
                self.assertEqual(item.liked_by.count(), 0)
                self.assertEqual(client.post(url, HTTP_X_CSRFTOKEN=token).status_code, 200)
