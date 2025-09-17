from django.urls import path
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
    path('delete/<str:id>/', views.delete_item, name='delete_item'),
]