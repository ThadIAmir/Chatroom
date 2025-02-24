from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Topic(models.Model):
    name = models.CharField(max_length=150,
                            validators=[MinLengthValidator(3, "Please provide a topic name.")])

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='hosted_rooms')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT,
                              max_length=150, null=False, blank=False, related_name='rooms')

    name = models.CharField(max_length=150, null=False, blank=False,
                            validators=[MinLengthValidator(3, "Please provide a name.")])

    description = models.TextField(null=True, blank=True, max_length=500)
    participants = models.ManyToManyField(
        User, related_name='joined_rooms', blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    replied_msg = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

