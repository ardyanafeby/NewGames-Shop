from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ItemForm
from main.models import Item

# Create your views here.

def show_main(request):
    items_list = Item.objects.all()
    context = {
        'name' : 'Ardyana Feby Pratiwi',
        'items_list' : items_list
    }

    return render(request, "main.html", context)

def create_items(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_items.html", context)

def show_items(request, id):
    items = get_object_or_404(Item, pk=id)
    items.increment_views()

    context = {
        'items': items
    }

    return render(request, "items_detail.html", context)

def show_xml(request):
     items_list = Item.objects.all()
     xml_data = serializers.serialize("xml", items_list)
     return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    items_list = Item.objects.all()
    json_data = serializers.serialize("json", items_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, items_id):
   try:
        product_item = Item.objects.filter(pk=items_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
   except Item.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, items_id):
   try:
        product_item = Item.objects.get(pk=items_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
   except Item.DoesNotExist:
       return HttpResponse(status=404)
   
def delete_item(request, id):
    item = get_object_or_404(Item, pk=id)
    item.delete()
    return redirect('main:show_main')