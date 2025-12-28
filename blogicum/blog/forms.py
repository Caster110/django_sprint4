from django import forms
from django.core.validators import FileExtensionValidator
from .models import Post, Category, Location, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'category', 'location', 'image']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только опубликованные категории и локации
        self.fields['category'].queryset = Category.objects.filter(is_published=True)
        self.fields['location'].queryset = Location.objects.filter(is_published=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }