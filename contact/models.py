from django.db import models


class Contact(models.Model):
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    description = models.TextField('Descrição', blank=True)

    email = models.EmailField('E-mail', blank=True, max_length=100)

    first_name = models.CharField('Nome', max_length=50)

    last_name = models.CharField('Sobrenome', blank=True, max_length=50)

    phone = models.CharField('Telefone', max_length=50)

    def __str__(self) -> str:
        return f'{self.id} | {self.first_name} | {self.phone}'
