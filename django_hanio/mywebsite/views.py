from django.shortcuts import render, redirect, HttpResponseRedirect
from mywebsite.models import *

from django.contrib import messages

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
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
    if request.method == "POST":
        MAccount = request.POST.get("account")
        MPW = request.POST.get("password")

        try:
            user = member.objects.get(MAccount=MAccount)
        except member.DoesNotExist:
            messages.error(request, "帳號不存在")
            return render(request, 'login.html')

        if user.MPW != MPW:
            messages.error(request, "帳號或密碼錯誤")
        else:
            # 登入成功，將用戶名稱存入 Session
            request.session['MAccount'] = MAccount
            return redirect('/index')
    
    return render(request, 'login.html')


@login_required(login_url='/login/')
def member_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
        
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "確認修改密碼失敗")
        else:
            # 更新會員資料
            try:
                user = member.objects.get(MAccount=MAccount)  # 獲取用戶對象
            except member.DoesNotExist:
                messages.error(request, "用戶不存在")
                return redirect('/member')
            
            user.MPW = password  # 更新用戶密碼
            user.save()  # 保存用戶對象
            messages.success(request, "修改成功")
            return redirect('/member')

    return render(request, 'member.html', {'MAccount': MAccount})


def pay_view(request):
    return render(request, 'pay.html', locals())

def record_view(request):
    return render(request, 'record.html', locals())

def signup_view(request):
    if request.method == "POST":
        MName = request.POST.get("MName")
        MAccount = request.POST.get("MAccount")
        MPW = request.POST.get("MPW")
        MPhone = request.POST.get("MPhone")
        MEmail = request.POST.get("MEmail")

        # 檢查帳號是否已經存在
        if member.objects.filter(MAccount=MAccount).exists():
            messages.error(request, "已有此帳號")
        else:
            # 儲存新的會員到資料庫
            new_member = member(
                MName=MName, 
                MAccount=MAccount, 
                MPW=MPW, 
                MPhone=MPhone, 
                MEmail=MEmail,
            )
            new_member.save()
            messages.success(request, "帳號創建成功")
            # 我們不再導向到登入頁面，而是留在註冊頁面

    # 對於 GET 請求，或者其他的請求方法，我們只顯示表單
    return render(request, 'signup.html')

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