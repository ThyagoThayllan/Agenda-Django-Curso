from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import FileInput
from django.forms import HiddenInput
from django.forms import ModelForm
from django.forms import Textarea
from django.forms import ValidationError

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
            'description': Textarea(attrs={'style': 'resize: none'}),
            'image': FileInput(attrs={'accept': 'image/*'}),
            'owner': HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class UserRegisterForm(UserCreationForm):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)
        model = User

    def clean_email(self) -> str | None:
        if not (email := self.cleaned_data.get('email')):
            raise ValidationError('Preencha o seu e-mail.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já existe. Por favor, tente novamente.')

        return email


class UserForm(ModelForm):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email')
        model = User
