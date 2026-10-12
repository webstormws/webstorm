from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('services/', views.services_list, name='services'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('services/<int:service_id>/packages/', views.packages_list, name='packages'),
    path('services/<int:service_id>/packages/create/', views.package_create, name='package_create'),
    path('services/<int:service_id>/packages/<int:pk>/edit/', views.package_edit, name='package_edit'),
    path('services/<int:service_id>/packages/<int:pk>/delete/', views.package_delete, name='package_delete'),
    path('portfolio/', views.portfolio_list, name='portfolio'),
    path('portfolio/create/', views.portfolio_create, name='portfolio_create'),
    path('portfolio/<int:pk>/edit/', views.portfolio_edit, name='portfolio_edit'),
    path('portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),
    path('websites/', views.websites_list, name='websites'),
    path('websites/create/', views.website_create, name='website_create'),
    path('websites/<int:pk>/edit/', views.website_edit, name='website_edit'),
    path('websites/<int:pk>/delete/', views.website_delete, name='website_delete'),
    path('faq/', views.faq_list, name='faq'),
    path('faq/create/', views.faq_create, name='faq_create'),
    path('faq/<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('faq/<int:pk>/delete/', views.faq_delete, name='faq_delete'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('settings/', views.settings_view, name='settings'),
]
