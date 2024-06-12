from django.urls import path
from .import views

urlpatterns = [
    path("",views.index),
    path("register/",views.register),
    path("login/",views.login1),
    path("saveRegister/",views.saveRegister),
    path("checklogin/",views.checklogin),
    path("user_home/",views.user_home),
    path("admin_login/",views.admin_login),
    path("admin_check/",views.admin_check),
    path("adminhome/",views.adminhome),
    path("create_product/",views.create_product),
    path("save_product/",views.save_product),
    path("product_details/",views.product_details),
    path("check_product/",views.check_product),
    path("review/",views.review,name="review")
]