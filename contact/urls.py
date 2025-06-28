from django.urls import path
from contact.views import Contacts
from contact.views import ContactView


app_name = 'contact'

urlpatterns = [
    path('', Contacts.as_view(), name='contacts'),
    path('contact/<int:pk>/', ContactView.as_view(), name='contact'),
]
