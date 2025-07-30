from django.db import models
from django.contrib.auth.models import User

# If you want to store Auth0 user info separately
class UserProfile(models.Model):
    auth0_id = models.CharField(max_length=255, unique=True)  # e.g., "auth0|abc123"
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.auth0_id


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="courses"
    )
    tags = models.JSONField(default=list, blank=True)  # stores list of tags

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.JSONField(default=list)  # structured blocks (list of dicts)
    is_enriched = models.BooleanField(default=False)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.module.title} - {self.title}"
