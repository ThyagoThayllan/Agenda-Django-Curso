from django.contrib.auth.models import User
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import Model
from django.db.models import SET_NULL
from django.db.models import TextField


class Category(Model):
    name = CharField('Categoria', max_length=50)

    class Meta:
        verbose_name = 'Categoria'

        verbose_name_plural = 'Categorias'

    def __str__(self) -> str:
        return f'{self.id} - {self.name}'


class Contact(Model):
    category = ForeignKey(
        Category, blank=True, null=True, on_delete=SET_NULL, verbose_name='Categoria'
    )

    created_at = DateTimeField('Data de Criação', auto_now_add=True)

    description = TextField('Descrição', blank=True)

    email = EmailField('E-mail', blank=True, max_length=100)

    first_name = CharField('Nome', max_length=50)

    image = ImageField('Imagem', blank=True, upload_to='images/contact/%Y/%m/')

    last_name = CharField('Sobrenome', blank=True, max_length=50)

    owner = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)

    phone = CharField('Telefone', max_length=50)

    show = BooleanField(default=True)

    class Meta:
        verbose_name = 'Contato'

        verbose_name_plural = 'Contatos'

    def __str__(self) -> str:
        return f'{self.id} - {self.first_name} - {self.phone}'
