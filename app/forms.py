from django import forms
# from app.models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     data = super().clean()
    #
    #     username = data.get('username')
    #     if username != username.lower():
    #         self.add_error('username', 'Error')
    #
    #     return data

class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise ValidationError("Passwords do not match")

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()

        Profile.objects.create(
            user=user,
            avatar=self.cleaned_data.get('picture')
        )

        return user

class AskForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')

    def save(self, profile, commit=True):
        question = Question.objects.create(
            author=profile,
            title=self.cleaned_data.get('title'),
            text=self.cleaned_data.get('text'),
            created_at=timezone.now(),
        )
        question.tags.set(self.cleaned_data.get('tags'))

        return question.id

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)

    def save(self, profile, question, commit=True):
        Answer.objects.create(
            author=profile,
            question=question,
            text=self.cleaned_data.get('text'),
            is_accepted=False,
            created_at=timezone.now(),
        )