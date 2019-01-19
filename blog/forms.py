from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post, Comment


# class UserLoginForm(forms.Form):
#     username =  forms.CharField()
#     password = forms.CharField(widget = forms.Password_Input)
#
#     def clean(self, *args, **kwargs):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#
#         if username and password:
#             user = authenticate(username = username, password = password)
#             if user is not None:
#                 #
#             else:
#                 #

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)
        widgets = {
            'post_text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
            'comment_text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)
        widgets = {
            'post_text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
