from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


class TaskList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_lists"
    )
    name = models.CharField(max_length=100)
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_lists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default_list(cls, user):
        """Get or create the default 'My Tasks' list for a user"""
        default_list, created = cls.objects.get_or_create(
            name="My Tasks", user=user, defaults={}
        )
        return default_list


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )

    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,  # Can be blank in forms
        null=True
    )

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "-priority", "created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Handle task completed_at timestamp and assign to default list if required"""

        # Handle completed_at timestamp
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None

        super().save(*args, **kwargs)

    @property
    def priority_color_class(self):
        """CSS class for priority color"""
        return f"priority-{self.priority}"

    @property
    def priority_badge_class(self):
        """Bootstrap badge class for priority"""
        return f"badge-priority-{self.priority}"
