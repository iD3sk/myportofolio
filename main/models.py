import uuid

from django.db import models


class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, default="")
    org_logo = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, null=True)
    description = models.TextField()
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)
    skills = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

    @property
    def skills_list(self):
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]


class Educations(models.Model):
    level = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=255)
    program = models.CharField(max_length=255, blank=True)
    started_at = models.PositiveIntegerField()
    ended_at = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)

    @property
    def is_on_going(self):
        return self.ended_at is None


class Achievements(models.Model):
    class Rank(models.TextChoices):
        BRONZE = "bronze", "Bronze"
        SILVER = "silver", "Silver"
        GOLD = "gold", "Gold"

    title = models.CharField(max_length=255)
    year = models.IntegerField()
    organization = models.CharField(max_length=255)
    rank = models.CharField(max_length=10, choices=Rank.choices)
    description = models.TextField(blank=True)