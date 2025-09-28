from main.views import register
from main.views import edit_items
from main.views import login_user
from main.views import logout_user
from django.urls import path
from main.views import delete_items
from main.views import aku_cinta
from main import views
from main.views import show_main, create_items, show_items, show_xml, show_json, show_json_by_id, show_xml_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-items/', create_items, name='create_items'),
    path('items/<str:id>/', show_items, name='show_items'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:items_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:items_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('news/<uuid:id>/edit', edit_items, name='edit_items'),
    path('news/<uuid:id>/delete', delete_items, name='delete_items'),
]