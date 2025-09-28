from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from contact.forms import ContactForm
from contact.models import Contact


class ContactCreate(TemplateView):
    template_name = 'contact/contact-form.html'
    title = 'Criar Contato'

    def get(self, request: HttpRequest) -> HttpResponse:
        action_form = reverse('contact:create')

        context = {'action_form': action_form, 'form': ContactForm(), 'title': self.title}

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ContactForm(data=request.POST)

        if form.is_valid():
            contact = Contact.objects.create(**form.cleaned_data)

            return redirect(reverse('contact:update', kwargs={'pk': contact.pk}))

        return render(request, self.template_name, {'form': form})


class ContactUpdate(TemplateView):
    template_name = 'contact/contact-form.html'
    title = 'Editar Contato'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse | HttpResponseRedirect:
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            breakpoint()
            print('ollaaaaaaaaaaaaaaaaa')
            messages.error(request, f'Contato de ID <b>{pk}</b> não existe. Tente novamente.')
            return redirect('contact:contacts')

        print('ollaaaaaaaaaaaaaaaaa 2222222222')
        action_form = reverse('contact:update', kwargs={'pk': pk})

        form = ContactForm(instance=contact)

        context = {
            'action_form': action_form,
            'contact': contact,
            'form': form,
            'title': self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse | HttpResponseRedirect:
        form = ContactForm(data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()

        return redirect('contact:update')


class ContactView(TemplateView):
    template_name = 'contact/contact.html'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse | HttpResponseRedirect:
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            messages.error(request, f'Contato de ID <strong>"{pk}"</strong> não encontrado.')
            return redirect('contact:contacts')

        context = {'contact': contact, 'title': contact.first_name}

        return render(request, self.template_name, context)


class Contacts(TemplateView):
    template_name = 'contact/contacts.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        search_value = request.GET.get('search')

        contacts = None

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

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'title': 'Contatos'}

        return render(request, self.template_name, context)
