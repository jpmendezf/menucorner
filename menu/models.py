from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Menu(models.Model):
    """A menu created by a user."""

    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Lunch(models.Model):
    """An option in a menu"""

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=128)


class Option(models.Model):
    """A multi-choice option available as part of a menu option."""

    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)


class Submission(models.Model):
    """A set of answers of menu options."""

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    """An answer to a menu's options."""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
