from django.urls import path
from contact.views import Contacts


app_name = 'contact'

urlpatterns = [
    path('', Contacts.as_view(), name='contacts'),
]
