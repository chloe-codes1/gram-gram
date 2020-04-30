from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='Title',
        help_text='Your title must be no more than 100 characters in length',
        widget=forms.TextInput(
            attrs={
                'class':'my_input',
                'placeholder': "What's on your mind?"
            }
        )
    )
    content = forms.CharField(
        label='Content',
        help_text='Jot down random musings and thoughts',
        widget=forms.Textarea(
            attrs={
                'row':5,
                'col':50,
                'placeholder': "You can add tags by putting pound sign (#) infront of it!"
            }
        )
    )
    class Meta:
        model = Article 
        exclude = ['created_at', 'updated_at', 'user', 'liked_users','tags',]


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs={
                'row':2,
                'col':10,
                'placeholder':'Add a comment...',
                'class':'form-control',
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']