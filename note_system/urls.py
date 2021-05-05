from django.urls import path
from .views import *

urlpatterns = [
    path('', entry, name="entry"),
    path('register/', register, name="register"),
    path('login/', login_process, name='login'),
    path('logout/', logout_process, name='logout'),
    path('new_note/',go_to_new_note_page, name='new_note'),
    path('add_new_note/',add_new_note,name='add_new_note'),
    path('delete_note/<int:note_id>', delete_note,name='delete_note'),
    path('note_edit/<int:note_id>/<int:type>',edit_note,name='note_edit'),
    path('search/',search_process,name='search'),
]
