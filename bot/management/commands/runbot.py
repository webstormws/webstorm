import asyncio
from django.core.management.base import BaseCommand
from bot.tg_bot import main


class Command(BaseCommand):
    help = 'Telegram botni ishga tushiradi'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot ishga tushmoqda...'))
        asyncio.run(main())
