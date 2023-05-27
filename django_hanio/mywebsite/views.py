from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(request, 'index.html', locals())

def about_view(request):
    return render(request, 'about.html', locals())

def contact_view(request):
    return render(request, 'contact.html', locals())

def detail_view(request):
    return render(request, 'detail.html', locals())

def hanio_view(request):
    return render(request, 'hanio.html', locals())

def login_view(request):
    return render(request, 'login.html', locals())

def member_view(request):
    return render(request, 'member.html', locals())

def pay_view(request):
    return render(request, 'pay.html', locals())

def record_view(request):
    return render(request, 'record.html', locals())

def signup_view(request):
    return render(request, 'signup.html', locals())

def cart_view(request):
    return render(request, 'cart.html', locals())