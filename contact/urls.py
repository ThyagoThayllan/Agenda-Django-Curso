from django.urls import path
from contact.views import ContactCreate
from contact.views import ContactDelete
from contact.views import ContactUpdate
from contact.views import ContactView
from contact.views import Contacts


app_name = 'contact'

urlpatterns = [
    # Contact
    path('', Contacts.as_view(), name='contacts'),
    path('contact/<int:pk>/', ContactView.as_view(), name='contact'),
    path('contact/<int:pk>/delete/', ContactDelete.as_view(), name='delete'),
    path('contact/<int:pk>/update/', ContactUpdate.as_view(), name='update'),
    path('contact/create/', ContactCreate.as_view(), name='create'),
]
