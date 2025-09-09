from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name' : 'Raket Badminton',
        'price': '300000',
        'description': 'Raket badminton dengan kualitas terbaik, memberikan kenyamanan pada saat memainkannya',
        'thumbnail': 'https://down-id.img.susercontent.com/file/2f8367b53ab79fd47069e86fea114328',
        'category': 'Peralatan Olahraga',
        'is_featured': True,
        'stock': 10,
        'brand': 'Yonex'
    }

    return render(request, "main.html", context)