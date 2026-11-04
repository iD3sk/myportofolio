from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Experience, Educations, Achievements

class ExperienceSerializer(serializers.ModelSerializer):
	is_ongoing = serializers.ReadOnlyField()
	skills_list = serializers.ReadOnlyField()
	is_liked = serializers.SerializerMethodField()
	like_counts = serializers.SerializerMethodField()
	liked_by_name = serializers.SerializerMethodField()

	class Meta:
		model = Experience
		fields = [
			"id",
			"title",
			"organization", 
			"org_logo", 
			"location", 
			"description", 
			"started_at", 
			"ended_at", 
			"skills", 
			"liked_by", 
			"is_ongoing", 
			"skills_list",
			"like_counts",
			"liked_by_name",
			"is_liked"
		]
		read_only_fields = ["id", "liked_by"]

	def get_is_liked(self, obj):
		request = self.context.get("request")
		return bool(request and request.user.is_authenticated and any(
			user.pk == request.user.pk for user in obj.liked_by.all()
		))

	def get_like_counts(self, obj):
		return obj.liked_by.count()
		
	def get_liked_by_name(self, obj):
		return ", ".join(user.username for user in obj.liked_by.all())
		
	def validate(self, attrs):
		text_fields = [
			"title", 
			"organization", 
			"org_logo", 
			"location", 
			"description", 
			"skills"
		]
		required_text_fields = ["title", "organization", "description"]

		errors = {}

		for field in text_fields:
			if field not in attrs:
				continue

			value = attrs[field]
			if isinstance(value, str):
				value = strip_tags(value).strip()
				attrs[field] = value

				if field in required_text_fields and not value:
					errors[field] = f"{field} cannot be empty"

		started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
		ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))

		if (
			started_at is not None
			and ended_at is not None
			and ended_at < started_at
		):
			errors["ended_at"] = "end date cannot be before start date"	

		if errors:
			raise serializers.ValidationError(errors)	

		return attrs

class EducationSerializer(serializers.ModelSerializer):
	is_ongoing = serializers.ReadOnlyField()

	class Meta:
		model = Educations
		fields = ["level", "institution", "program", "started_at", "ended_at", "description", "display_order"]

	def validate(self, attrs):
		text_fields = ["level", "institution", "program", "description", "skills"]
		required_text_fields = ["institution"]

		errors = {}

		for field in text_fields:
			if field not in attrs:
				continue

			value = attrs[field]
			if isinstance(value, str):
				value = strip_tags(value).strip()
				attrs[field] = value

				if field in required_text_fields and not value:
					errors[field] = f"{field} cannot be empty"

		started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
		ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))

		if (
			started_at is not None
			and ended_at is not None
			and ended_at < started_at
		):
			errors["ended_at"] = "end date cannot be before start date"	
		if errors:
			raise serializers.ValidationError(errors)	

		return attrs

class AchievementsSerializer(serializers.ModelSerializer):
	is_liked = serializers.SerializerMethodField()
	rank_display = serializers.CharField(source="get_rank_display", read_only=True)
	like_counts = serializers.SerializerMethodField()
	liked_by_name = serializers.SerializerMethodField()

	class Meta:
		model = Achievements
		fields = [
			"id", 
			"title", 
			"year", 
			"organization", 
			"org_logo", 
			"rank", 
			"rank_display",
			"description", 
			"liked_by",
			"like_counts",
			"liked_by_name",
			"is_liked"
		] 
		read_only_fields = ["id", "liked_by"]

	def get_is_liked(self, obj):
		request = self.context.get("request")
		return bool(request and request.user.is_authenticated and any(
			user.pk == request.user.pk for user in obj.liked_by.all()
		))

	def get_like_counts(self, obj):
		return obj.liked_by.count()

	def get_liked_by_name(self, obj):
		return ", ".join(user.username for user in obj.liked_by.all())

	def validate(self, attrs):
		text_fields = ["title", "organization", "description"]
		required_text_fields = ["title", "organization"]

		errors = {}

		for field in text_fields:
			if field not in attrs:
				continue

			value = attrs[field]
			if isinstance(value, str):
				value = strip_tags(value).strip()
				attrs[field] = value

				if field in required_text_fields and not value:
					errors[field] = f"{field} cannot be empty"

		started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
		ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))

		if (
			started_at is not None
			and ended_at is not None
			and ended_at < started_at
		):
			errors["ended_at"] = "end date cannot be before start date"	

		if errors:
			raise serializers.ValidationError(errors)	

		return attrs
