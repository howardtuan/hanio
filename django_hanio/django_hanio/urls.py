from django.contrib import admin
from django.urls import path
from mywebsite import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.index_view),
    path('about/', views.about_view),
    path('contact/', views.contact_view),
    path('detail/', views.detail_view),
    path('hanio/', views.hanio_view),
    path('login/', views.login_view),
    path('member/', views.member_view),
    path('pay/', views.pay_view),
    path('record/', views.record_view),
    path('signup/', views.signup_view),
]
