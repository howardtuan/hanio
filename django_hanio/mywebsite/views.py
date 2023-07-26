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
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import openai
import json
with open('mywebsite/secret.json', 'r') as file:
    data = json.load(file)
OPENAI_API_KEY = data.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
# Create your views here.

now = datetime.now()

def chat_view(request):
    return render(request, 'chat.html', locals())
from django.utils.html import escape

def chat_with_ai(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # 對用戶輸入進行HTML轉義，避免XSS攻擊
        user_input = escape(user_input)
        start="""
        你是戈登肉鋪的小助理，要解決客人所問的問題！當客人問店家地址時，你要回答「桃園市桃園區新埔六街57號1樓」。當客人問你店家電話時，你要回答「03-358-5590」。當客人問你營業時間時，你要回答「每天11:00至20:00」。當客人問你附近有沒有停車位時，你要回答「附近有付費停車場」。當客人問你請問可以刷卡嗎?請回答可以！我們的支付方式有現金、實體卡片、Apple Pay以及Line Pay。
        目前店內的食品有：
        安格斯肋眼牛排，編號2，單價200
        安格斯無骨牛小排，編號3，單價170
        澳洲JOSDAL安格斯菲力牛排，編號5，單價180
        澳洲JOSDALE安格斯羽下牛排，編號6，單價120
        日本A5和牛近江肋眼牛排，編號7，單價210
        安格斯羽下火鍋肉片，編號8，單價140
        無骨牛小排火鍋肉片，編號9，單價200
        安格斯霜降雪花火鍋肉片，編號10，單價210
        美國安格斯牛五花火鍋肉片，編號11，單價190
        美國安格斯頂級牛五花火鍋肉片，編號12，單價150
        日本鹿兒島和牛片 一般版，編號13，單價230
        日本鹿兒島火鍋肉片_長版，編號14，單價250
        桐德盤克夏-豬肉黑豚五花火鍋片，編號15，單價170
        CAB認證安格斯羽下燒烤肉片，編號16，單價190
        CAB認證無骨牛小排燒烤肉片，編號17，單價180
        CAB認證安格斯霜降雪花燒烤肉片，編號18，單價160
        安格斯牛五花燒烤肉片-爆量版，編號19，單價200
        日本鹿兒島燒烤肉片一般版，編號20，單價215
        日本鹿兒島燒烤肉片_長版，編號21，單價240
        黑豚五花燒烤片，編號23，單價180
        黑蜜豬里肌火鍋片，編號24，單價180
        黑蜜豬梅花火鍋片，編號25，單價150
        台南無毒生態白蝦，編號26，單價200
        宜蘭爆卵母香魚，編號27，單價200
        台南無毒文蛤，編號28，單價250
        日本火鍋料選用天然魚漿，編號29，單價220
        日本進口高級火鍋料，編號30，單價300
        伊比利黑豬梅花切片，編號31，單價260
        桐德盤克夏二層肉，編號32，單價150
        黑蜜豬腰內肉片，編號33，單價180
        西班牙Bellota頂級伊比利豬梅花肉片，編號34，單價400
        如果客人說他最近在健康飲食，請推薦他1~3份海鮮類的食品。如果客人說他想吃牛排，請推薦他1~3份牛排類的食品。
        如果客人說他只有2000塊的預算，請幫他搭配食材，總價不得高於顧客要求的價位，產品可重複，但總金額記得要算對，單價要乘以該商品的選購數量，在列出這些商品組合時，不用顯示計算過程，只要總金額是正確的即可。
        回應客人食材時，不需要照以上資料那麼制式化，請自然一點，但少說廢話，也不需要跟他說編號是多少。
        """
        # 使用OpenAI GPT-3.5 Turbo模型進行對話
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": start},
                {"role": "assistant", "content": "此處填入機器人訊息"},
                {"role": "user", "content": "我有1000塊的預算 有推薦的嗎"},
                {"role": "assistant", "content": "當然！根據您的預算，我為您搭配如下食材： 1. 安格斯羽下火鍋肉片 x 3包，單價 140 2. 安格斯無骨牛小排 x 2塊，單價 170 3. 台南無毒文蛤 x 1包，單價 250 總金額為1010，價格符合您的預算。希望這些選擇能符合您的需求！"},
                {"role": "user", "content": user_input},
            ]
        )

        # 獲取機器人的回答
        ai_response = completion.choices[0].message['content']

        # 定義產品資料
        product_data = [
            ("安格斯肋眼牛排", "2", "200"),
            ("安格斯無骨牛小排", "3", "170"),
            ("澳洲JOSDAL安格斯菲力牛排", "5", "180"),
            ("澳洲JOSDALE安格斯羽下牛排", "6", "120"),
            ("日本A5和牛近江肋眼牛排", "7", "210"),
            ("安格斯羽下火鍋肉片", "8", "140"),
            ("無骨牛小排火鍋肉片", "9", "200"),
            ("安格斯霜降雪花火鍋肉片", "10", "210"),
            ("美國安格斯牛五花火鍋肉片", "11", "190"),
            ("美國安格斯頂級牛五花火鍋肉片", "12", "150"),
            ("日本鹿兒島和牛片 一般版", "13", "230"),
            ("日本鹿兒島火鍋肉片_長版", "14", "250"),
            ("桐德盤克夏-豬肉黑豚五花火鍋片", "15", "170"),
            ("CAB認證安格斯羽下燒烤肉片", "16", "190"),
            ("CAB認證無骨牛小排燒烤肉片", "17", "180"),
            ("CAB認證安格斯霜降雪花燒烤肉片", "18", "160"),
            ("安格斯牛五花燒烤肉片-爆量版", "19", "200"),
            ("日本鹿兒島燒烤肉片一般版", "20", "215"),
            ("日本鹿兒島燒烤肉片_長版", "21", "240"),
            ("黑豚五花燒烤片", "23", "180"),
            ("黑蜜豬里肌火鍋片", "24", "180"),
            ("黑蜜豬梅花火鍋片", "25", "150"),
            ("台南無毒生態白蝦", "26", "200"),
            ("宜蘭爆卵母香魚", "27", "200"),
            ("台南無毒文蛤", "28", "250"),
            ("日本火鍋料選用天然魚漿", "29", "220"),
            ("日本進口高級火鍋料", "30", "300"),
            ("伊比利黑豬梅花切片", "31", "260"),
            ("桐德盤克夏二層肉", "32", "150"),
            ("黑蜜豬腰內肉片", "33", "180"),
            ("西班牙Bellota頂級伊比利豬梅花肉片", "34", "400"),
        ]


        # 將產品名稱替換為超連結
        for product_name, product_num, product_price in product_data:
            if product_name in ai_response:
                link = f"<a href='http://127.0.0.1:8000/{product_num}/' target='_blank'>{product_name}</a>"
                ai_response = ai_response.replace(product_name, link)

        print(ai_response)


        # 返回AI回答
        return JsonResponse({'answer': ai_response})

    return JsonResponse({'error': '無效的請求'})


def cart_quantity_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        return JsonResponse({'quantity': ''})

    get_id = member.objects.get(MAccount=MAccount).MID
    cart_items = cart.objects.filter(MID=get_id)
    quantity=0
    for item in cart_items:
        pid = item.PID
        p = product.objects.get( PID = pid )
        number = item.NUM
        quantity+=number


    return JsonResponse({'quantity': quantity})
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
        category = '日本A5和牛專賣區'
    elif cate == 'pork' :
        category = '戈登嚴選豬肉'
    elif cate == 'seafood' :
        category = '戈登經典海鮮'
    return render(request, 'product_edit.html', locals())

def addp_view(request):
    return render(request, 'product_add.html', locals())

def dedelete(request):  
    pid = request.POST.get('pid', '') 
    product_to_delete = product.objects.get(PID=pid)
    product_to_delete.delete()
    return redirect('/dashboard/')

def add_p_cart(request):   
    get_name = request.POST.get('product-name', '')
    get_quantity = request.POST.get('product-quantity', '')
    get_price = request.POST.get('product-price', '0')
    get_detail = request.POST.get('product-detail', '')
    get_spec = request.POST.get('product-spec', '')
    get_status = request.POST.get('product-status', '')
    get_photo = request.FILES.get('product-photo', '')  # 若欄位為檔案上傳，使用FILES.get()
    get_category = request.POST.get('product-category', '')
    product.objects.create(
        PName = get_name,
        Pnum = get_quantity,
        PPrice = get_price,
        PDetail = get_detail,
        Pspec = get_spec,
        PStatus = get_status,
        PPhoto=get_photo,
        # PPhoto = "product_images/1_cyBXWdt_fJ05J4e.jpg",
        PCategory = get_category
        )
    return redirect('/dashboard/')


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
    selected_price = request.POST.get('price_filter')
    if selected_price is not None:
        try:
            selected_price = int(selected_price)
            print(selected_price)
            Category = product.objects.filter(PCategory='beef', PPrice__lte=selected_price).order_by('PPrice')
        except ValueError:
            Category = product.objects.filter(PCategory='beef')
    else:
        Category = product.objects.filter(PCategory='beef')

    count = Category.count()

    # 將篩選值加入到locals中
    return render(request, 'hanio.html', locals())



def pork_view(request):
    selected_price = request.POST.get('price_filter')
    if selected_price is not None:
        try:
            selected_price = int(selected_price)
            Category = product.objects.filter(PCategory='pork', PPrice__lte=selected_price).order_by('PPrice')
        except ValueError:
            Category = product.objects.filter(PCategory='pork')
    else:
        Category = product.objects.filter(PCategory='pork')

    count = Category.count()
    return render(request, 'for_pork.html', locals())


def seafood_view(request):
    Category = product.objects.filter( PCategory = 'seafood' )
    selected_price = request.POST.get('price_filter')
    if selected_price is not None:
        try:
            selected_price = int(selected_price)
            print(selected_price)
            Category = product.objects.filter(PCategory='seafood', PPrice__lte=selected_price).order_by('PPrice')
        except ValueError:
            Category = product.objects.filter(PCategory='seafood')
    else:
        Category = product.objects.filter(PCategory='seafood')

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
    memn = member.objects.get(MAccount=MAccount)

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


def detail_view(request, pid=None):
    if request.method == 'POST':
        get_id = request.POST.get('pid', '')
    else:
        get_id = pid
    
    status = '上架'
    try:
        p = product.objects.get(PID=get_id)
        if p.PStatus == 'IN_STOCK':
            status = '尚有庫存'
        elif p.PStatus == 'OUT_OF_STOCK':
            status = '缺貨中'
        elif p.PStatus == 'UNAVAILABLE':
            status = '尚無庫存'
    except product.DoesNotExist:
        # 处理找不到产品的情况，例如显示错误信息或重定向到其他页面
        pass
    
    all_pids = product.objects.values_list('PID', flat=True)
    random_pids = sample(list(all_pids), 3)
    random_products = product.objects.filter(PID__in=random_pids)

    isFAV = False
    MAccount = request.session.get('MAccount')

    if MAccount:
        get_mid = member.objects.get(MAccount=MAccount).MID
        fav_obj = fav.objects.filter(MID=get_mid, PID=get_id).count()
        if fav_obj > 0 :
            isFAV = True
        
    
    return render(request, 'detail.html', locals())


# def detail_back(request, pid):
#     get_id = pid
#     status = '上架'
#     p = product.objects.get(PID=get_id)
#     if p.PStatus == '上架':
#         status = '尚有庫存'
#     if p.PStatus == '下架':
#         status = '缺貨中'
#     if p.PStatus == '缺貨':
#         status = '尚無庫存'
#     # context = {'product_DB': p, 'status': status}
#     all_pids = product.objects.values_list('PID', flat=True)
#     # 從所有 PID 中隨機選取三個
#     random_pids = sample(list(all_pids), 3)
#     # 根據選取的 PID 取得對應的 Product 資料
#     random_products = product.objects.filter(PID__in=random_pids)
#     return render(request, 'detail.html', locals())


def add_cart(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    print('ur id:',get_id)
    get_pid = request.POST.get('pid', '')
    get_pnum = request.POST.get('number', '')
    cat = request.POST.get('pcate', '')
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

    redirect_url = reverse('detail', kwargs={'pid': get_pid})    
    return redirect(redirect_url)
        

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
    yn=True
    if len(cart_products)==0:
        yn=False
    print(yn)
    
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
    print(cart_item)
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

def add_favorite(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    get_pid = request.POST.get('pid', '')
    fav.objects.create( MID = get_id, PID = get_pid)
    redirect_url = reverse('detail', kwargs={'pid': get_pid})    
    return redirect(redirect_url)

def del_favorite(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')
    get_id = member.objects.get(MAccount=MAccount).MID
    get_pid = request.POST.get('pid', '')
    fav_to_delete = fav.objects.filter(MID=get_id, PID=get_pid)
    fav_to_delete.delete()

    redirect_url = reverse('detail', kwargs={'pid': get_pid})    
    return redirect(redirect_url)

 

def fav_view(request):
    MAccount = request.session.get('MAccount')
    if not MAccount:
        messages.error(request, "請先登入")
        return redirect('/login')

    # 獲取會員編號
    get_id = member.objects.get(MAccount=MAccount).MID

    # 從 fav 資料表中獲取客戶加入最愛的商品資訊
    fav_list = fav.objects.filter(MID=get_id)
    fav_products = []
    count=0     
    for fav_item in fav_list:
        try:
            p = product.objects.get(PID=fav_item.PID)
            fav_products.append(p)
            count+=1
        except product.DoesNotExist:
            # 在 product 資料庫中找不到對應的產品
            pass
    

    return render(request, 'fav.html', locals())