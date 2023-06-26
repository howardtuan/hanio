from django.shortcuts import render, redirect, HttpResponseRedirect
from random import sample
from mywebsite.models import *
import random
from django.contrib import messages
from django.db.models import Max
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.db.models import Sum
from collections import defaultdict
from django.db.models.functions import Cast


# Create your views here.

now = datetime.now()
def index_view(request):
    # 使用 annotate() 和 values() 方法對相同 pid 的 pnum 欄位進行加總
    beef_pids = product.objects.filter(PCategory="beef").values_list('PID', flat=True)
    totals = (
        order_detail.objects.filter(PID__in=beef_pids)
        .values('PID')
        .annotate(total_pnum=Sum('PNUM'))
        .order_by('-total_pnum')[:3]
    )
    btop_three_pids = [total['PID'] for total in totals]
    print(btop_three_pids)
    bproducts = product.objects.filter(PID__in=btop_three_pids)

    pork_pids = product.objects.filter(PCategory="pork").values_list('PID', flat=True)
    totals = (
        order_detail.objects.filter(PID__in=pork_pids)
        .values('PID')
        .annotate(total_pnum=Sum('PNUM'))
        .order_by('-total_pnum')[:3]
    )
    ptop_three_pids = [total['PID'] for total in totals]
    print(ptop_three_pids)
    pproducts = product.objects.filter(PID__in=ptop_three_pids)

    sea_pids = product.objects.filter(PCategory="seafood").values_list('PID', flat=True)
    totals = (
        order_detail.objects.filter(PID__in=sea_pids)
        .values('PID')
        .annotate(total_pnum=Sum('PNUM'))
        .order_by('-total_pnum')[:3]
    )
    stop_three_pids = [total['PID'] for total in totals]
    print(stop_three_pids)
    sproducts = product.objects.filter(PID__in=stop_three_pids)
    return render(request, 'index.html', locals())

def dashboard_view(request):
    d = product.objects.all()
    mem = member.objects.all()
    return render(request, 'dashboard.html', locals())

def orders_view(request):
    ord = order_detail.objects.all()

    return render(request, 'orders_page.html', locals())

def about_view(request):
    return render(request, 'about.html', locals())

def contact_view(request):
    return render(request, 'contact.html', locals())

def detail_view(request):
    get_id = request.POST.get('pid', '')
    status = '上架'
    p = product.objects.get( PID = get_id )
    if p.PStatus == '上架' :
        status = '尚有庫存'

    if p.PStatus == '下架' :
        status = '缺貨中'

    if p.PStatus == '缺貨' :
        status = '尚無庫存'    
    # context = {'product_DB': p, 'status': status}
    all_pids = product.objects.values_list('PID', flat=True)

    # 從所有 PID 中隨機選取三個
    random_pids = sample(list(all_pids), 3)

    # 根據選取的 PID 取得對應的 Product 資料
    random_products = product.objects.filter(PID__in=random_pids)

    return render(request, 'detail.html', locals())

def or_e_view(request):
    get_odid = request.POST.get('odid', '')
    ord = order_detail.objects.get( ODID = get_odid )

    return render(request, 'order_edit.html', locals())


def or_edit(request):
    get_odid = request.POST.get('odid', '')
    selected_option = request.POST.get('status', '')
    get_address = request.POST.get('address', '')
    ord = order_detail.objects.get( ODID = get_odid )
    ord.OStatus = selected_option
    ord.OAddr = get_address
    ord.save()

    return redirect('/orders_view/')

def edit_view(request):
    get_id = request.POST.get('pid', '')
    p = product.objects.get( PID = get_id )
    cate = p.PCategory
    if cate == 'beef' :
        category = '日本A5和專賣區'
    elif cate == 'pork' :
        category = '戈登嚴選豬肉'
    elif cate == 'seafood' :
        category = '戈登經典海鮮'
    return render(request, 'product_edit.html', locals())

def edit(request):
    get_id = request.POST.get('pid', '')
    products = product.objects.get( PID = get_id )
    photo = products.PPhoto
    get_name = request.POST.get('product-name', '')
    get_quantity = request.POST.get('product-quantity', '')
    get_price = request.POST.get('product-price', '0')
    get_detail = request.POST.get('product-detail', '')
    get_spec = request.POST.get('product-spec', '')
    get_status = request.POST.get('product-status', '')
    get_photo = request.FILES.get('product-photo', photo)  # 若欄位為檔案上傳，使用FILES.get()
    get_category = request.POST.get('product-category', '')
    products.PName = get_name
    products.Pnum = get_quantity
    products.PPrice = get_price
    products.PDetail = get_detail
    products.Pspec = get_spec
    products.PStatus = get_status
    products.PPhoto = get_photo
    products.PCategory = get_category
    products.save()

    return redirect('/dashboard/')

def hanio_view(request):
    Category = product.objects.filter( PCategory = 'beef' )
    count = Category.count()
    # i = product.objects.get( PID = 2 )
    return render(request, 'hanio.html', locals())

def pork_view(request):
    Category = product.objects.filter( PCategory = 'pork' )
    count = Category.count()
    return render(request, 'for_pork.html', locals())

def seafood_view(request):
    Category = product.objects.filter( PCategory = 'seafood' )
    count = Category.count()
    return render(request, 'for_seafood.html', locals())

def login_view(request):
    if request.method == "POST":
        MAccount = request.POST.get("account")
        MPW = request.POST.get("password")
        try:
            manager = Manager.objects.get(username=MAccount)  # 使用 manager 代替 super
            if manager.password != MPW:
                messages.error(request, "帳號或密碼錯誤")
                return render(request, 'login.html')
            else:
                # 登入成功，將用戶名稱存入 Session
                request.session['MAccount'] = MAccount
                request.session.save()
                return redirect('/dashboard/')
        except Manager.DoesNotExist:
            try:
                user = member.objects.get(MAccount=MAccount)
                if user.MPW != MPW:
                    messages.error(request, "帳號或密碼錯誤")
                    return render(request, 'login.html')
                else:
                    # 登入成功，將用戶名稱存入 Session
                    request.session['MAccount'] = MAccount
                    request.session.save()
                    return redirect('/index')
            except member.DoesNotExist:
                messages.error(request, "帳號不存在")
                return render(request, 'login.html')
    return render(request, 'login.html')

def member_e_view(request):
    get_id = request.POST.get('mid', '')
    mem = member.objects.get( MID = get_id )
    return render(request, 'member_edit.html', locals())

def mem_edit(request):
    get_id = request.POST.get('mid', '')
    mem = member.objects.get( MID = get_id )
    get_account = request.POST.get('account', '')
    get_password = request.POST.get('password', '')
    get_phone = request.POST.get('phone', '')
    get_name = request.POST.get('name', '')
    get_mail = request.POST.get('mail', '')
    get_address = request.POST.get('address', '')
    get_visa = request.POST.get('visa', '')
    get_mck = request.POST.get('mck', '')
    mem.MAccount = get_account
    mem.MPW = get_password
    mem.MPhone = get_phone
    mem.MName = get_name
    mem.MEmail = get_mail
    mem.MAddr = get_address
    mem.MVISA = get_visa
    mem.MCK = get_mck
    mem.save()
    return redirect('/dashboard/')

def member_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    
    user_info = {}
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
    else:
        try:
            user = member.objects.get(MAccount=MAccount)
            user_info = {
                'MAccount': user.MAccount,
                'MName': user.MName,
                'MPhone': user.MPhone,
                'MPW': user.MPW,
                'MEmail': user.MEmail,
                'MAddr': user.MAddr,
                'MVISA': user.MVISA,
                'MCK': user.MCK,
                # ... 其他信息
            }
        except member.DoesNotExist:
            messages.error(request, "用戶不存在")
            return redirect('/member')
    mem = member.objects.get( MAccount = MAccount )
    mid = mem.MID
    ors = order_detail.objects.filter(MID=mid)
    grouped_data = {}
    for orderdetail in ors:
        odate = orderdetail.ODate
        if odate in grouped_data:
            grouped_data[odate].append(orderdetail)
        else:
            grouped_data[odate] = [orderdetail]

    result = []
    for odate, orders in grouped_data.items():
        data = {'odate': odate, 'products': []}
        for orr in orders:
            pid = orr.PID
            pnum = orr.PNUM
            products = product.objects.get(PID=pid)
            pname = products.PName
            pprice = products.PPrice
            total_price = pnum * pprice
            data['products'].append({'pname': pname, 'pnum': pnum, 'total_price': total_price})
        result.append(data)

    print(result)


    return render(request, 'member.html', locals())

def memberbaseinfo_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')

    user_info = {}

    try:
        user = member.objects.get(MAccount=MAccount)
    except member.DoesNotExist:
        messages.error(request, "用戶不存在")
        return redirect('/member')
    if request.method == "POST":
        MName = request.POST.get("MName")
        MPhone = request.POST.get("MPhone")
        MEmail = request.POST.get("MEmail")
        MAddr = request.POST.get("MAddr")
        MVISA = request.POST.get("MVISA")
        MCK = request.POST.get("MCK")           
        user.MName = MName  
        user.MPhone = MPhone
        user.MEmail = MEmail
        user.MAddr = MAddr
        user.MVISA = MVISA
        user.MCK = MCK
        user.save()  # 保存用戶對象
        messages.success(request, "修改成功")
        return redirect('/member')
    else:
        try:
            user = member.objects.get(MAccount=MAccount)
            user_info = {
                'MAccount': user.MAccount,
                'MName': user.MName,
                'MPhone': user.MPhone,
                'MPW': user.MPW,
                'MEmail': user.MEmail,
                'MAddr': user.MAddr,
                'MVISA': user.MVISA,
                'MCK': user.MCK,
                # ... 其他信息
            }
        except member.DoesNotExist:
            messages.error(request, "用戶不存在")
            return redirect('/member')
    return render(request, 'memberbaseinfo.html', {'user_info': user_info})


def pay_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    # get_id = request.POST.get('mid', '')
    cart_items = cart.objects.filter( MID = get_id )
    cart_products = []
    total_price=0
    total_num=0
    for item in cart_items:
        pid = item.PID
        p = product.objects.get( PID = pid )
        number = item.NUM
        sub = p.PPrice * number
        total_price+=sub
        total_num+=number
        cart_products.append((item, p, sub))

    
    return render(request, 'pay.html', locals())


def checkout_process(request):
    if request.method == 'POST':
        address = request.POST.get('address') 
        payment_method = request.POST.get('paymentMethod')
        if payment_method == 'credit':
            payment = 'COD'
        elif payment_method == 'debit':
            payment = 'CC'
        elif payment_method == 'paypal':
            payment = 'CVS'
    
    # 取得目前資料庫中的最大 OID 值
    max_oid = order.objects.aggregate(max_oid=Max(Cast('OID', models.IntegerField())))['max_oid']
    print('max_id: ')
    print(max_oid)
    # 為了避免第一筆資料時 max_oid 為 None 的情況，需要進行檢查
    if max_oid is not None:
        new_oid = int(max_oid) + 1
    else:
        new_oid = 1

    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    cart_items = cart.objects.filter(MID=get_id)
    
    for cart_item in cart_items:
        pid = cart_item.PID
        pnum = cart_item.NUM
        
        order.objects.create(
            OID=new_oid,
            MID=get_id,
            PID=pid
        )
        order_detail.objects.create(
            OID=new_oid,
            MID=get_id,
            PID=pid,
            PNUM=pnum,
            ODate=now,
            OAddr=address,
            OStatus='NOT_SHIPPED',
            OPayment=payment
        )
        
    cart.objects.filter(MID=get_id).delete()
    return redirect('/member')



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
            return redirect('/login')


    # 對於 GET 請求，或者其他的請求方法，我們只顯示表單
    return render(request, 'signup.html')

def add_cart(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    print('ur id:',get_id)
    get_pid = request.POST.get('pid', '')
    get_pnum = request.POST.get('number', '')
    print('get_pnum',get_pnum)
    try:   
        c = cart.objects.get( MID = get_id, PID = get_pid )
        num = c.NUM + int(get_pnum)
        c.NUM = num
        c.save()
    except:
        cart.objects.create( MID = get_id, PID = get_pid, NUM = get_pnum )
    finally:
        pass
    

    return HttpResponseRedirect('/index/')  #可更新

def cart_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
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
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    #這邊也要取得mid
    get_mid = member.objects.get(MAccount=MAccount).MID
    get_pid = request.POST.get('pid', '')
    get_pnum = request.POST.get('num', '')
    cart_item = cart.objects.get( PID = get_pid, MID = get_mid )
    print('id',get_pid)
    print('數量',get_pnum)
    cart_item.NUM = get_pnum
    cart_item.save()
    return HttpResponseRedirect('/cart/')

def cart_delete(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    #這邊也要取得mid
    get_mid = member.objects.get(MAccount=MAccount).MID
    get_pid = request.POST.get('pid', '')
    cart_item = cart.objects.get( PID = get_pid, MID = get_mid )
    cart_item.delete()
    return HttpResponseRedirect('/cart/')

def logout_view(request):
    try:
        del request.session['MAccount']
    except KeyError:
        pass
    return redirect('/login')

def search_products(request):
    keyword = request.POST.get('searchbox', '')
    products = product.objects.filter(PName__icontains=keyword)
    count = products.count()
    return render(request, 'search.html', locals())
