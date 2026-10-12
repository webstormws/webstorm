import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Telegram bot webhook'ni o'rnatadi (sayt bilan bot birga ishlashi uchun)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default='',
            help='Webhook URL. Standart: https://SITE_DOMAIN/TELEGRAM_WEBHOOK_PATH'
        )

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            self.stderr.write(self.style.ERROR('TELEGRAM_BOT_TOKEN .env faylida sozlanmagan!'))
            return

        url = options.get('url') or f"https://{settings.SITE_DOMAIN}/{settings.TELEGRAM_WEBHOOK_PATH.strip('/')}/"
        api_url = f"https://api.telegram.org/bot{token}/setWebhook?url={urllib.parse.quote(url)}"

        try:
            with urllib.request.urlopen(api_url, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Webhook o'rnatilmadi: {e}"))
            return

        if data.get('ok'):
            self.stdout.write(self.style.SUCCESS(f"Webhook muvaffaqiyatli o'rnatildi: {url}"))
        else:
            self.stderr.write(self.style.ERROR(f"Telegram xatosi: {data}"))