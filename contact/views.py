from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from contact.forms import ContactForm, UserForm
from contact.forms import UserRegisterForm
from contact.models import Contact


class ContactCreate(LoginRequiredMixin, TemplateView):
    template_name = 'contact/contact-form.html'
    title = 'Criar Contato'

    def get(self, request: HttpRequest) -> HttpResponse:
        action_form = reverse('contact:create')

        context = {'action_form': action_form, 'form': ContactForm(), 'title': self.title}

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ContactForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()

            return redirect('contact:update', pk=contact.pk)

        return render(request, self.template_name, {'form': form})


class ContactDelete(LoginRequiredMixin, View):
    def post(
        self, request: HttpRequest, pk: int
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            messages.error(request, f'Contato de ID <b>{pk}</b> não existe. Tente novamente.')
            return redirect('contact:contacts')

        contact.delete()

        return redirect('contact:contacts')


class ContactUpdate(LoginRequiredMixin, TemplateView):
    template_name = 'contact/contact-form.html'
    title = 'Editar Contato'

    def get(self, request: HttpRequest, pk: int) -> HttpResponse | HttpResponseRedirect:
        try:
            contact = Contact.objects.get(owner=request.user, pk=pk)
        except Contact.DoesNotExist:
            messages.error(request, f'Contato de ID <b>{pk}</b> não existe. Tente novamente.')
            return redirect('contact:contacts')

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
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            messages.error(request, f'Contato de ID <b>{pk}</b> não existe. Tente novamente.')
            return redirect('contact:contacts')

        form = ContactForm(data=request.POST, files=request.FILES, instance=contact)

        if form.is_valid():
            form.save()

            messages.success(request, 'Contato atualizado com sucesso.')

            return redirect('contact:update', pk=pk)

        return render(request, self.template_name, {'form': form})


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


class UserRegister(TemplateView):
    template_name = 'register.html'

    def get(
        self, request: HttpRequest
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        return render(request, self.template_name, {'form': UserRegisterForm()})

    def post(
        self, request: HttpRequest
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Bem vindo, {form.cleaned_data['first_name']}!')

            return redirect('user-login')

        return render(request, self.template_name, {'form': form})


class UserUpdate(LoginRequiredMixin, TemplateView):
    template_name = 'user-update-form.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = UserForm(instance=request.user)

        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(request, 'Usuário atualizado com sucesso!')

            return redirect('user-update')

        return render(request, self.template_name, {'form': form})


class Login(LoginView):
    template_name = 'login.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = AuthenticationForm(request)

        return render(request, self.template_name, {'form': form})

    def post(
        self, request: HttpRequest
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        form = AuthenticationForm(request, data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.get_user()

        login(request, user)

        messages.success(request, 'Usuário logado com sucesso.')

        return redirect('contact:contacts')


class Logout(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        logout(request)

        return redirect('user-login')
