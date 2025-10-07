from main.views import delete_item_ajax, edit_item_ajax, get_items_json, item_detail_json, login_ajax, logout_ajax, register, register_ajax
from main.views import edit_items
from main.views import login_user
from main.views import logout_user
from django.urls import path
from main.views import delete_items
from main.views import add_item_ajax
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
    path('api/items/', get_items_json, name='get_items_json'),
    path('api/items/<uuid:id>/', item_detail_json, name='item_detail_json'),
    path('api/items/create/', add_item_ajax, name='add_item_ajax'),
    path('api/items/<uuid:id>/edit/', edit_item_ajax, name='edit_item_ajax'),
    path('api/items/<uuid:id>/delete/', delete_item_ajax, name='delete_item_ajax'),

    path('register-ajax/', register_ajax, name='register_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('logout-ajax/', logout_ajax, name='logout_ajax'),




]