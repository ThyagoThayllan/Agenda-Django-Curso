from django.db import models


class Category(models.Model):
    name = models.CharField('Categoria', max_length=50)


class Contact(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    description = models.TextField('Descrição', blank=True)

    email = models.EmailField('E-mail', blank=True, max_length=100)

    first_name = models.CharField('Nome', max_length=50)

    image = models.ImageField('Imagem', blank=True, upload_to='images/contact/%Y/%m/')

    last_name = models.CharField('Sobrenome', blank=True, max_length=50)

    phone = models.CharField('Telefone', max_length=50)

    show = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.id} | {self.first_name} | {self.phone}'
