from django import forms
from django.forms import RadioSelect

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'rating', 'review')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'name',
                    'aria-describedby': 'nameHelp',
                    'placeholder': 'Представьтесь',
                    'name': 'name',
                    'data-cip-id': 'name'
                }
            ),
            'rating': forms.RadioSelect(
                choices=[
                    (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
                ]
            ),
            'review': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'content',
                    'placeholder': 'Содержание',
                    'name': 'description'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
            self.fields['name'].widget.attrs['readonly'] = True

