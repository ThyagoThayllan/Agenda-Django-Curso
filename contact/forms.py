from django.forms import ModelForm
from django.forms import Textarea

from contact.models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = {
            'category',
            'description',
            'email',
            'first_name',
            'image',
            'last_name',
            'owner',
            'phone',
        }
        widgets = {
            'description': Textarea(attrs={'style': 'resize: none'})
        }

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
