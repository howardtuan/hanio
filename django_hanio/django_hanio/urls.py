from django.contrib import admin
from django.urls import path
from mywebsite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.index_view),
    path('about/', views.about_view),
    path('contact/', views.contact_view),
    path('detail/', views.detail_view),
    path('hanio/', views.hanio_view),
    path('pork/', views.pork_view),
    path('seafood/', views.seafood_view),
    path('login/', views.login_view),
    path('member/', views.member_view),
    path('memberbaseinfo/', views.memberbaseinfo_view),
    path('pay/', views.pay_view),
    path('record/', views.record_view),
    path('signup/', views.signup_view),
    path('cart/', views.cart_view),
    path('update/', views.cart_update),
    path('delete/', views.cart_delete),
    path('add/', views.add_cart),
    path('logout/', views.logout_view, name='logout'),
    path('checkout_process/', views.checkout_process),
    path('dashboard/', views.dashboard_view),
    path('edit_view/', views.edit_view),
    path('edit/', views.edit),
    path('m_e_view/', views.member_e_view),
    path('mem_edit/', views.mem_edit),
    path('orders_view/', views.orders_view),
    path('or_e_view/', views.or_e_view),
    path('or_edit/', views.or_edit),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)