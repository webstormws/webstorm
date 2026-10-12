import json
import urllib.request
import urllib.parse

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import (SiteSettings, Service, Project, Testimonial, TeamMember,
                     BlogPost, FAQItem, CareerJob, Stat, Partner)


def base(request):
    settings_obj = SiteSettings.objects.first()
    if settings_obj is None:
        settings_obj = SiteSettings.objects.create()

    context = {
        'settings': settings_obj,
        'services': Service.objects.all(),
        'projects': Project.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'team_members': TeamMember.objects.all(),
        'posts': BlogPost.objects.all(),
        'faqs': FAQItem.objects.all(),
        'jobs': CareerJob.objects.all(),
        'stats': Stat.objects.all(),
        'partners': Partner.objects.all(),
    }
    return render(request, 'base.html', context)


def projects_all(request):
    settings_obj = SiteSettings.objects.first()
    if settings_obj is None:
        settings_obj = SiteSettings.objects.create()

    all_projects = Project.objects.all()
    category = request.GET.get('category', 'all')
    if category != 'all':
        all_projects = all_projects.filter(category=category)

    context = {
        'settings': settings_obj,
        'projects': all_projects,
        'current_category': category,
        'web_count': Project.objects.filter(category='web').count(),
        'mobile_count': Project.objects.filter(category='mobile').count(),
        'ecommerce_count': Project.objects.filter(category='ecommerce').count(),
        'platform_count': Project.objects.filter(category='platform').count(),
    }
    return render(request, 'projects.html', context)


def send_telegram_message(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_ids = settings.ADMIN_CHAT_IDS
    if not token or not chat_ids:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chat_id in chat_ids:
        data = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            return False
    return True


@csrf_exempt
@require_POST
def contact_send(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    name = body.get("name", "").strip()
    email = body.get("email", "").strip()
    phone = body.get("phone", "").strip()
    service = body.get("service", "").strip()
    subject = body.get("subject", "").strip()
    message = body.get("message", "").strip()

    if not name or not email or not message:
        return JsonResponse({"success": False, "error": "Name, email and message are required"}, status=400)

    text = (
        "📩 <b>New Contact Form Message</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Name:</b> {name}\n"
        f"📧 <b>Email:</b> {email}\n"
    )
    if phone:
        text += f"📞 <b>Phone:</b> {phone}\n"
    text += (
        f"💼 <b>Service:</b> {service or 'N/A'}\n"
        f"📝 <b>Subject:</b> {subject or 'N/A'}\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"💬 <b>Message:</b>\n{message}"
    )

    if send_telegram_message(text):
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Failed to send message"}, status=500)
