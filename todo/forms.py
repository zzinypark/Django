from django import forms
from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'form-control',
                'placeholder': 'Enter your message',
            }),
        }
        labels = {
            'message': '내용'
        }