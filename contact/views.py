from django.shortcuts import render
from django.views.generic import TemplateView


class Contacts(TemplateView):
    template_name = 'contact/contacts.html'

    def get(self, request):
        return render(request, self.template_name)
