from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('task/', views.task, name='task'),
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('customer/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customer/delete/<int:id>/', views.delete_customer, name='delete_customer'),
    path('customer/', views.customer, name='customer'),
    path('adminassistprice/', views.adminassistprice, name='adminassistprice'),
    path('adminassistprice/<int:customer_id>/', views.adminassistprice, name='adminassistprice'),
    path('adminsalescontract/', views.adminsalescontract, name='adminsalescontract'),
    path('adminsalescontract/<int:customer_id>/', views.adminsalescontract, name='adminsalescontract'),
    path('assistpricedetail/<int:offer_id>/', views.assistpricedetail, name='assistpricedetail'),
    path('salescontractdetail/<int:id>/', views.salescontractdetail, name='salescontractdetail'),
    path('salescontract/delete/<int:id>/', views.delete_sales_contract, name='delete_sales_contract'),
    path('salescontract/edit/<int:id>/', views.edit_sales_contract, name='edit_sales_contract'),
    path('assistprice/', views.assistprice, name='assistprice'),
    path('assistprice/delete/<int:id>/', views.delete_assist_price, name='delete_assist_price'),
    path('assistprice/edit/<int:id>/', views.edit_assist_price, name='edit_assist_price'),
    path('salescontract/', views.salescontract, name='salescontract'),
    path('customer/<int:id>/', views.customerinfo, name='customerinfo'),
    path('feedback/<int:customer_id>/', views.feedback, name='feedback'),
]
