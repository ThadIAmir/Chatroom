from django import forms
from django.forms import ModelForm, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, Message, Topic


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    topic = CharField(max_length=150, required=True)

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

    def clean_topic(self):
        topic_name = self.cleaned_data.get('topic', '').strip()

        if not topic_name:
            raise forms.ValidationError("Topic cannot be empty.")

        topic, created = Topic.objects.get_or_create(name=topic_name)
        return topic


# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['body']
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'replied_msg']
        widgets = {'replied_msg': forms.HiddenInput()}


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
