from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView

from contact.models import Contact


class Contacts(TemplateView):
    template_name = 'contact/contacts.html'

    def get(self, request):
        search_value = request.GET.get('search')

        if search_value:
            contacts = (
                Contact.objects.select_related('category')
                .filter(
                    Q(first_name__icontains=search_value)
                    | Q(last_name__icontains=search_value)
                    | Q(email__icontains=search_value)
                    | Q(phone__icontains=search_value),
                    show=True,
                )
                .order_by('-id')
            )
        else:
            contacts = Contact.objects.select_related('category').filter(show=True).order_by('-id')

        context = {'contacts': contacts, 'title': 'Contatos'}

        return render(request, self.template_name, context)


class ContactView(TemplateView):
    template_name = 'contact/contact.html'

    def get(self, request, pk):
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            messages.error(request, f'Contato de ID <strong>"{pk}"</strong> não encontrado.')
            return redirect('contact:contacts')

        context = {'contact': contact, 'title': contact.first_name}

        return render(request, self.template_name, context)
