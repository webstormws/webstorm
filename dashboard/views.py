import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from bot.models import (
    BotUser, BotAdmin, BotSetting, Service, ServicePackage,
    PortfolioItem, WebsiteItem, FAQ, Order
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        messages.error(request, 'Login yoki parol xato!')
    return render(request, 'dashboard/login.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard:login')


@login_required(login_url='dashboard:login')
def index(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    stats = {
        'users': BotUser.objects.count(),
        'active_users': BotUser.objects.filter(is_active=True).count(),
        'services': Service.objects.filter(is_active=True).count(),
        'orders': Order.objects.count(),
        'new_orders': Order.objects.filter(status='new').count(),
        'faqs': FAQ.objects.filter(is_active=True).count(),
        'portfolio': PortfolioItem.objects.filter(is_active=True).count(),
        'websites': WebsiteItem.objects.filter(is_active=True).count(),
    }

    recent_orders = Order.objects.all()[:5]
    recent_users = BotUser.objects.all()[:5]

    order_stats = {
        'new': Order.objects.filter(status='new').count(),
        'contacted': Order.objects.filter(status='contacted').count(),
        'negotiation': Order.objects.filter(status='negotiation').count(),
        'approved': Order.objects.filter(status='approved').count(),
        'in_progress': Order.objects.filter(status='in_progress').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'order_stats': order_stats,
        'page': 'dashboard',
    }
    return render(request, 'dashboard/index.html', context)


# ===================== SERVICES =====================
@login_required(login_url='dashboard:login')
def services_list(request):
    services = Service.objects.all()
    return render(request, 'dashboard/services.html', {'services': services, 'page': 'services'})


@login_required(login_url='dashboard:login')
def service_create(request):
    if request.method == 'POST':
        svc = Service.objects.create(
            icon=request.POST.get('icon', ''),
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            target_audience=request.POST.get('target_audience', ''),
            features=request.POST.get('features', ''),
            price_info=request.POST.get('price_info', ''),
            is_active='is_active' in request.POST,
            order=int(request.POST.get('order', 0)),
        )
        features = request.POST.get('features', '')
        price = request.POST.get('price', '')
        if features or price:
            ServicePackage.objects.create(
                service=svc,
                name=request.POST.get('pkg_name', 'Asosiy'),
                price=price or 'Narx kelishiladi',
                features=features,
                order=1,
            )
        messages.success(request, 'Xizmat yaratildi!')
        return redirect('dashboard:services')
    return render(request, 'dashboard/service_form.html', {'service': None, 'page': 'services'})


@login_required(login_url='dashboard:login')
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.icon = request.POST.get('icon', service.icon)
        service.name = request.POST.get('name', service.name)
        service.description = request.POST.get('description', service.description)
        service.target_audience = request.POST.get('target_audience', service.target_audience)
        service.features = request.POST.get('features', service.features)
        service.price_info = request.POST.get('price_info', service.price_info)
        service.is_active = 'is_active' in request.POST
        service.order = int(request.POST.get('order', service.order))
        service.save()
        messages.success(request, 'Xizmat yangilandi!')
        return redirect('dashboard:services')
    return render(request, 'dashboard/service_form.html', {'service': service, 'page': 'services'})


@login_required(login_url='dashboard:login')
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Xizmat ochirildi!')
        return redirect('dashboard:services')
    return render(request, 'dashboard/confirm_delete.html', {'object': service, 'page': 'services'})


# ===================== SERVICE PACKAGES =====================
@login_required(login_url='dashboard:login')
def packages_list(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    packages = service.packages.all()
    return render(request, 'dashboard/packages.html', {'service': service, 'packages': packages, 'page': 'services'})


@login_required(login_url='dashboard:login')
def package_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        ServicePackage.objects.create(
            service=service,
            name=request.POST.get('name', ''),
            price=request.POST.get('price', ''),
            features=request.POST.get('features', ''),
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, 'Paket yaratildi!')
        return redirect('dashboard:packages', service_id=service_id)
    return render(request, 'dashboard/package_form.html', {'service': service, 'package': None, 'page': 'services'})


@login_required(login_url='dashboard:login')
def package_edit(request, service_id, pk):
    service = get_object_or_404(Service, pk=service_id)
    package = get_object_or_404(ServicePackage, pk=pk)
    if request.method == 'POST':
        package.name = request.POST.get('name', package.name)
        package.price = request.POST.get('price', package.price)
        package.features = request.POST.get('features', package.features)
        package.order = int(request.POST.get('order', package.order))
        package.save()
        messages.success(request, 'Paket yangilandi!')
        return redirect('dashboard:packages', service_id=service_id)
    return render(request, 'dashboard/package_form.html', {'service': service, 'package': package, 'page': 'services'})


@login_required(login_url='dashboard:login')
def package_delete(request, service_id, pk):
    package = get_object_or_404(ServicePackage, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Paket ochirildi!')
        return redirect('dashboard:packages', service_id=service_id)
    return render(request, 'dashboard/confirm_delete.html', {'object': package, 'page': 'services'})


# ===================== PORTFOLIO =====================
@login_required(login_url='dashboard:login')
def portfolio_list(request):
    items = PortfolioItem.objects.all()
    return render(request, 'dashboard/portfolio.html', {'items': items, 'page': 'portfolio'})


@login_required(login_url='dashboard:login')
def portfolio_create(request):
    if request.method == 'POST':
        item = PortfolioItem(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            category=request.POST.get('category', 'website'),
            technologies=request.POST.get('technologies', ''),
            demo_url=request.POST.get('demo_url', ''),
            is_active='is_active' in request.POST,
            order=int(request.POST.get('order', 0)),
        )
        if request.FILES.get('image'):
            item.image = request.FILES['image']
        item.save()
        messages.success(request, 'Loyiha yaratildi!')
        return redirect('dashboard:portfolio')
    return render(request, 'dashboard/portfolio_form.html', {'item': None, 'page': 'portfolio'})


@login_required(login_url='dashboard:login')
def portfolio_edit(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    if request.method == 'POST':
        item.title = request.POST.get('title', item.title)
        item.description = request.POST.get('description', item.description)
        item.category = request.POST.get('category', item.category)
        item.technologies = request.POST.get('technologies', item.technologies)
        item.demo_url = request.POST.get('demo_url', item.demo_url)
        item.is_active = 'is_active' in request.POST
        item.order = int(request.POST.get('order', item.order))
        if request.FILES.get('image'):
            item.image = request.FILES['image']
        item.save()
        messages.success(request, 'Loyiha yangilandi!')
        return redirect('dashboard:portfolio')
    return render(request, 'dashboard/portfolio_form.html', {'item': item, 'page': 'portfolio'})


@login_required(login_url='dashboard:login')
def portfolio_delete(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Loyiha ochirildi!')
        return redirect('dashboard:portfolio')
    return render(request, 'dashboard/confirm_delete.html', {'object': item, 'page': 'portfolio'})


# ===================== WEBSITES =====================
@login_required(login_url='dashboard:login')
def websites_list(request):
    sites = WebsiteItem.objects.all()
    return render(request, 'dashboard/websites.html', {'sites': sites, 'page': 'websites'})


@login_required(login_url='dashboard:login')
def website_create(request):
    if request.method == 'POST':
        site = WebsiteItem(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            url=request.POST.get('url', ''),
            category=request.POST.get('category', ''),
            technologies=request.POST.get('technologies', ''),
            is_active='is_active' in request.POST,
            order=int(request.POST.get('order', 0)),
        )
        if request.FILES.get('image'):
            site.image = request.FILES['image']
        site.save()
        messages.success(request, 'Sayt yaratildi!')
        return redirect('dashboard:websites')
    return render(request, 'dashboard/website_form.html', {'site': None, 'page': 'websites'})


@login_required(login_url='dashboard:login')
def website_edit(request, pk):
    site = get_object_or_404(WebsiteItem, pk=pk)
    if request.method == 'POST':
        site.name = request.POST.get('name', site.name)
        site.description = request.POST.get('description', site.description)
        site.url = request.POST.get('url', site.url)
        site.category = request.POST.get('category', site.category)
        site.technologies = request.POST.get('technologies', site.technologies)
        site.is_active = 'is_active' in request.POST
        site.order = int(request.POST.get('order', site.order))
        if request.FILES.get('image'):
            site.image = request.FILES['image']
        site.save()
        messages.success(request, 'Sayt yangilandi!')
        return redirect('dashboard:websites')
    return render(request, 'dashboard/website_form.html', {'site': site, 'page': 'websites'})


@login_required(login_url='dashboard:login')
def website_delete(request, pk):
    site = get_object_or_404(WebsiteItem, pk=pk)
    if request.method == 'POST':
        site.delete()
        messages.success(request, 'Sayt ochirildi!')
        return redirect('dashboard:websites')
    return render(request, 'dashboard/confirm_delete.html', {'object': site, 'page': 'websites'})


# ===================== FAQ =====================
@login_required(login_url='dashboard:login')
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'dashboard/faq.html', {'faqs': faqs, 'page': 'faq'})


@login_required(login_url='dashboard:login')
def faq_create(request):
    if request.method == 'POST':
        FAQ.objects.create(
            question=request.POST.get('question', ''),
            answer=request.POST.get('answer', ''),
            is_active='is_active' in request.POST,
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, 'FAQ yaratildi!')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/faq_form.html', {'faq': None, 'page': 'faq'})


@login_required(login_url='dashboard:login')
def faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.question = request.POST.get('question', faq.question)
        faq.answer = request.POST.get('answer', faq.answer)
        faq.is_active = 'is_active' in request.POST
        faq.order = int(request.POST.get('order', faq.order))
        faq.save()
        messages.success(request, 'FAQ yangilandi!')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/faq_form.html', {'faq': faq, 'page': 'faq'})


@login_required(login_url='dashboard:login')
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ ochirildi!')
        return redirect('dashboard:faq')
    return render(request, 'dashboard/confirm_delete.html', {'object': faq, 'page': 'faq'})


# ===================== ORDERS =====================
@login_required(login_url='dashboard:login')
def orders_list(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/orders.html', {'orders': orders, 'status_filter': status_filter, 'page': 'orders'})


@login_required(login_url='dashboard:login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST.get('status', order.status)
        order.internal_note = request.POST.get('internal_note', order.internal_note)
        order.save()
        messages.success(request, 'Buyurtma yangilandi!')
        return redirect('dashboard:order_detail', pk=pk)
    return render(request, 'dashboard/order_detail.html', {'order': order, 'page': 'orders'})


@login_required(login_url='dashboard:login')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Buyurtma ochirildi!')
        return redirect('dashboard:orders')
    return render(request, 'dashboard/confirm_delete.html', {'object': order, 'page': 'orders'})


# ===================== USERS =====================
@login_required(login_url='dashboard:login')
def users_list(request):
    users = BotUser.objects.all()
    return render(request, 'dashboard/users.html', {'users': users, 'page': 'users'})


@login_required(login_url='dashboard:login')
def user_detail(request, pk):
    user = get_object_or_404(BotUser, pk=pk)
    orders = Order.objects.filter(user=user)
    return render(request, 'dashboard/user_detail.html', {'bot_user': user, 'orders': orders, 'page': 'users'})


# ===================== SETTINGS =====================
@login_required(login_url='dashboard:login')
def settings_view(request):
    s = BotSetting.objects.first()
    if not s:
        s = BotSetting.objects.create()
    if request.method == 'POST':
        s.bot_name = request.POST.get('bot_name', s.bot_name)
        s.start_message = request.POST.get('start_message', s.start_message)
        s.about_text = request.POST.get('about_text', s.about_text)
        s.phone = request.POST.get('phone', s.phone)
        s.telegram_username = request.POST.get('telegram_username', s.telegram_username)
        s.instagram = request.POST.get('instagram', s.instagram)
        s.website = request.POST.get('website', s.website)
        s.address = request.POST.get('address', s.address)
        s.is_bot_active = 'is_bot_active' in request.POST
        s.save()
        messages.success(request, 'Sozlamalar yangilandi!')
        return redirect('dashboard:settings')
    return render(request, 'dashboard/settings.html', {'settings': s, 'page': 'settings'})
