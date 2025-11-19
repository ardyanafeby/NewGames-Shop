import requests
import datetime
import json
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.forms import ItemForm
from main.models import Item


@login_required(login_url='/login')
def show_main(request):
    context = {
        'name': "Ardyana Feby Pratiwi",
        'kelas': "PBP A",
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)


def create_items(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item_entry = form.save(commit=False)
        item_entry.user = request.user
        item_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_items.html", context)


@login_required(login_url='/login')
def show_items(request, id):
    items = get_object_or_404(Item, pk=id)
    context = {'items': items}
    return render(request, "items_detail.html", context)


def show_xml(request):
    items_list = Item.objects.all()
    xml_data = serializers.serialize("xml", items_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    items = Item.objects.all()
    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "description": item.description,
            "category": item.get_category_display(),
            "is_on_sale": item.is_on_sale,
            "is_featured": item.is_featured,
            "thumbnail": item.thumbnail if item.thumbnail else None,
        })
    return JsonResponse({"items": items_data})


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


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def edit_items(request, id):
    news = get_object_or_404(Item, pk=id)
    form = ItemForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "edit_items.html", context)


def delete_items(request, id):
    news = get_object_or_404(Item, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))



@login_required(login_url='/login')
def get_items_json(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        items = Item.objects.all()
    else:
        items = Item.objects.filter(user=request.user)
    
    items_data = []
    for item in items:
        items_data.append({
            "id": str(item.id),  # Convert UUID to string
            "name": item.name,
            "price": item.price,
            "sale_price": item.sale_price,
            "description": item.description,
            "category": item.category,
            "category_display": item.get_category_display(),
            "is_on_sale": item.is_on_sale,
            "is_featured": item.is_featured,
            "thumbnail": item.thumbnail if item.thumbnail else None,
            "stock": item.stock,
            "brand": item.brand if item.brand else None,
            "seller": item.user.username if item.user else None,
        })
    return JsonResponse({"items": items_data})


@login_required(login_url='/login')
def item_detail_json(request, id):
    try:
        item = Item.objects.get(pk=id)
        data = {
            "id": str(item.id),
            "name": item.name,
            "price": item.price,
            "sale_price": item.sale_price,
            "description": item.description,
            "category": item.category,
            "category_display": item.get_category_display(),
            "is_on_sale": item.is_on_sale,
            "is_featured": item.is_featured,
            "thumbnail": item.thumbnail if item.thumbnail else None,
            "stock": item.stock,
            "brand": item.brand if item.brand else None,
            "seller": item.user.username if item.user else None,
        }
        return JsonResponse(data)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)


@login_required(login_url='/login')
@csrf_exempt
@require_POST
def add_item_ajax(request):
    try:
        name = request.POST.get("name")
        price = request.POST.get("price")
        sale_price = request.POST.get("sale_price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        thumbnail = request.POST.get("thumbnail")
        stock = request.POST.get("stock", 0)
        brand = request.POST.get("brand")
        is_featured = request.POST.get("is_featured") == "on"

        if not name or not price:
            return JsonResponse({"error": "Name and price are required"}, status=400)

        new_item = Item(
            name=name,
            price=int(price),
            sale_price=int(sale_price) if sale_price else None,
            description=description,
            category=category,
            thumbnail=thumbnail,
            stock=int(stock) if stock else 0,
            brand=brand if brand else None,
            is_featured=is_featured,
            user=request.user
        )
        new_item.save()
        
        return JsonResponse({
            "message": "Item created successfully!",
            "item_id": str(new_item.id)
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required(login_url='/login')
@csrf_exempt
@require_POST
def edit_item_ajax(request, id):
    try:
        item = get_object_or_404(Item, pk=id)

        if item.user != request.user:
            return JsonResponse(
                {"error": "Kamu tidak punya izin untuk mengedit item ini."},
                status=403
            )


        item.name = request.POST.get("name", item.name)
        item.price = int(request.POST.get("price", item.price))
        
        sale_price = request.POST.get("sale_price")
        item.sale_price = int(sale_price) if sale_price else None
        
        item.description = request.POST.get("description", item.description)
        item.category = request.POST.get("category", item.category)
        item.thumbnail = request.POST.get("thumbnail", item.thumbnail)
        
        stock = request.POST.get("stock")
        item.stock = int(stock) if stock else 0
        
        brand = request.POST.get("brand")
        item.brand = brand if brand else None
        
        item.is_featured = request.POST.get("is_featured") == "on"
        
        item.save()
        
        return JsonResponse({
            "message": "Item updated successfully!",
            "item_id": str(item.id)
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required(login_url='/login')
@csrf_exempt
@require_POST
def delete_item_ajax(request, id):
    try:
        item = get_object_or_404(Item, pk=id)
        if item.user != request.user:
            return JsonResponse(
                {"error": "Kamu tidak punya izin untuk menghapus item ini."},
                status=403
            )

        item.delete()
        return JsonResponse({"message": "Item deleted successfully!"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Validation
            if not username or not password1 or not password2:
                return JsonResponse({
                    "status": "error",
                    "message": "All fields are required"
                }, status=400)

            if password1 != password2:
                return JsonResponse({
                    "status": "error",
                    "message": "Passwords do not match"
                }, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Username already exists"
                }, status=400)

            if len(password1) < 8:
                return JsonResponse({
                    "status": "error",
                    "message": "Password must be at least 8 characters"
                }, status=400)

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password1
            )
            
            return JsonResponse({
                "status": "success",
                "message": "Registration successful! Redirecting to login...",
                "username": user.username
            }, status=201)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                return JsonResponse({
                    "status": "error",
                    "message": "Username and password are required"
                }, status=400)

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": f"Welcome back, {user.username}!",
                    "username": user.username
                }, status=200)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid username or password"
                }, status=401)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


@login_required(login_url='/login')
@csrf_exempt
def logout_ajax(request):
    if request.method == 'POST':
        try:
            username = request.user.username
            logout(request)
            return JsonResponse({
                "status": "success",
                "message": f"Goodbye {username}! You have been logged out."
            }, status=200)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_product = Item(
            name=name, 
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)