from django.shortcuts import render, HttpResponseRedirect
from mywebsite.models import *


# Create your views here.
def index_view(request):
    return render(request, 'index.html', locals())

def about_view(request):
    return render(request, 'about.html', locals())

def contact_view(request):
    return render(request, 'contact.html', locals())

def detail_view(request):
    get_id = request.POST.get('pid', '')
    status = '缺貨中'
    p = product.objects.get( PID = get_id )
    if p.PStatus == '上架' :
        status = '尚有庫存'

    if p.PStatus == '下架' :
        status = '缺貨中'

    if p.PStatus == '缺貨' :
        status = '尚無庫存'    
    # context = {'product_DB': p, 'status': status}
    return render(request, 'detail.html', locals())

def hanio_view(request):
    Category = product.objects.filter( PCategory = 'beef' )
    # i = product.objects.get( PID = 2 )
    return render(request, 'hanio.html', locals())

def pork_view(request):
    Category = product.objects.filter( PCategory = 'pork' )
    return render(request, 'for_pork.html', locals())

def seafood_view(request):
    Category = product.objects.filter( PCategory = 'seefood' )
    return render(request, 'for_seafood.html', locals())

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

def add_cart(request):
    get_id = '001'
    get_pid = request.POST.get('pid', '')
    get_pnum = request.POST.get('number', '')
    c = cart.objects.get( MID = get_id, PID = get_pid )
    if c :
        num = c.NUM + int(get_pnum)
        c.NUM = num
        c.save()
    else :
        cart.objects.create( MID = get_id, PID = get_pid, NUM = get_pnum )

    return HttpResponseRedirect('/index/')  #可更新

def cart_view(request):
    get_id = '001'
    # get_id = request.POST.get('mid', '')
    cart_items = cart.objects.filter( MID = get_id )
    cart_products = []
    for item in cart_items:
        pid = item.PID
        p = product.objects.get( PID = pid )
        number = item.NUM
        sub = p.PPrice * number
        cart_products.append((item, p, sub))
    
    return render(request, 'cart.html', locals())

def cart_update(request):
    #這邊也要取得mid
    get_mid = '001'
    get_pid = request.POST.get('pid', '')
    get_pnum = request.POST.get('num', '')
    cart_item = cart.objects.get( PID = get_pid, MID = get_mid )
    cart_item.NUM = get_pnum
    cart_item.save()
    return HttpResponseRedirect('/cart/')

def cart_delete(request):
    #這邊也要取得mid
    get_mid = '001'
    get_pid = request.POST.get('pid', '')
    cart_item = cart.objects.get( PID = get_pid, MID = get_mid )
    cart_item.delete()
    return HttpResponseRedirect('/cart/')
