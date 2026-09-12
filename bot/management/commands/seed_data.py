from django.core.management.base import BaseCommand
from bot.models import BotSetting, Service, ServicePackage, FAQ, PortfolioItem, WebsiteItem


class Command(BaseCommand):
    help = 'Bot uchun boshlang\'ich ma\'lumotlarni yaratadi'

    def handle(self, *args, **options):
        settings, _ = BotSetting.objects.get_or_create(
            pk=1,
            defaults={
                'bot_name': 'Web Storm Bot',
                'start_message': '🚀 <b>WEB STORM</b>\n\nBiznesingiz uchun zamonaviy IT yechimlar.\n\nQuyidagi menyulardan birini tanlang:',
                'about_text': 'Web Storm — zamonaviy IT kompaniya.\n\nBiz biznesingiz uchun professional veb-saytlar, mobil ilovalar, CRM tizimlari, Telegram botlar va avtomatlashtirish yechimlari yaratamiz.\n\n🎯 Missiyamiz: Texnologiya orqali biznesingizni rivojlantirish.',
                'phone': '+998 XX XXX XX XX',
                'telegram_username': '@webstorm',
            }
        )
        self.stdout.write(self.style.SUCCESS('Bot sozlamalari yaratildi!'))

        services_data = [
            {'icon': '💻', 'name': 'CRM / ERP', 'description': 'Biznesingiz uchun maxsus CRM yoki ERP tizimi. Mijozlar bazasi, hisobotlar, avtomatlashtirish.', 'target_audience': 'Tadbirkorlar, kompaniya egalarini', 'features': 'Mijozlar bazasi\nHisobotlar\nAvtomatik xabarlar\nRol tizimi\nAPI integratsiya', 'price_info': '5 000 000 so\'mdan'},
            {'icon': '🤖', 'name': 'Telegram Bot', 'description': 'Professional Telegram bot yaratish. Bot, admin panel, to\'lov tizimi integratsiyasi.', 'target_audience': 'Biznes egalar, onlayn do\'konlar', 'features': 'Maxsus dizayn\nAdmin panel\nTo\'lov integratsiya\nXabar yuborish\nStatistika', 'price_info': '2 000 000 so\'mdan'},
            {'icon': '🌐', 'name': 'Web Sayt', 'description': 'Zamonaviy, responsive veb-sayt yaratish. Landing page, korporativ sayt, onlayn do\'kon.', 'target_audience': 'Har qanday biznes', 'features': 'Responsive dizayn\nSEO optimallashtirish\nAdmin panel\nKontakt forma\nTelegram integratsiya', 'price_info': '1 500 000 so\'mdan'},
            {'icon': '📱', 'name': 'Web App', 'description': 'Zamonaviy web ilova yaratish. PWA, SaaS platformalar, onlayn xizmatlar.', 'target_audience': 'Startaplar, texnologiya kompaniyalari', 'features': 'PWA qo\'llab-quvvatlash\nOffline rejim\nPush bildirishnomalar\nAPI backend', 'price_info': '8 000 000 so\'mdan'},
            {'icon': '📲', 'name': 'Mobile App', 'description': 'iOS va Android uchun mobil ilova yaratish. Flutter, React Native.', 'target_audience': 'Katta biznes, startaplar', 'features': 'Cross-platform\nPush bildirishnomalar\nOfflayn rejim\nTo\'lov tizimi', 'price_info': '15 000 000 so\'mdan'},
            {'icon': '⚙️', 'name': 'Biznes avtomatlashtirish', 'description': 'Biznes jarayonlarini avtomatlashtirish. API integratsiya, webhook, skriptlar.', 'target_audience': 'Har qanday biznes', 'features': 'API integratsiya\nWebhook\nSkriptlar\nHisobotlar', 'price_info': '3 000 000 so\'mdan'},
        ]

        for i, data in enumerate(services_data):
            svc, created = Service.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'order': i, 'is_active': True}
            )
            if created:
                if data['name'] == 'Web Sayt':
                    ServicePackage.objects.create(service=svc, name='START', price='1 500 000 so\'m', features='Zamonaviy dizayn\nResponsive\nKontakt forma\nTelegram integratsiya', order=1)
                    ServicePackage.objects.create(service=svc, name='BUSINESS', price='3 000 000 so\'m', features='Professional dizayn\nAdmin panel\nBackend\nDatabase\nTelegram integratsiya', order=2)
                elif data['name'] == 'Telegram Bot':
                    ServicePackage.objects.create(service=svc, name='ODDIY', price='2 000 000 so\'m', features='Asosiy funksiyalar\nInline keyboard\n1 ta buyruq', order=1)
                    ServicePackage.objects.create(service=svc, name='PRO', price='5 000 000 so\'m', features='To\'liq funksional\nAdmin panel\nTo\'lov tizimi\nStatistika', order=2)

        self.stdout.write(self.style.SUCCESS(f'{len(services_data)} ta xizmat yaratildi!'))

        faqs = [
            {'question': 'Web sayt qancha turadi?', 'answer': 'Sayt narxi funksiyalar va dizaynga qarab belgilanadi. Boshlang\'ich narxlarimizni "Narxlar" bo\'limidan ko\'rishingiz mumkin.', 'order': 1},
            {'question': 'CRM qancha vaqtda tayyor bo\'ladi?', 'answer': 'Oddiy CRM 2-3 haftada, murakkab tizim 1-2 oyda tayyor bo\'ladi. Aniq muddat loyiha hajmiga bog\'liq.', 'order': 2},
            {'question': 'Telegram bot yaratib bera olasizlarmi?', 'answer': 'Ha, albatta! Professional Telegram botlar yaratamiz. Admin panel, to\'lov tizimi va boshqa integratsiyalar bilan.', 'order': 3},
            {'question': 'Loyiha uchun qanday murojaat qilish mumkin?', 'answer': 'Bot orqali "Loyiha buyurtma qilish" bo\'limidan yoki admin bilan bog\'lanish orqali murojaat qilishingiz mumkin.', 'order': 4},
            {'question': 'To\'lov qanday amalga oshiriladi?', 'order': 5, 'answer': 'To\'lov naqd pul, bank o\'tkazmasi yoki onlayn to\'lov orqali amalga oshirilishi mumkin. Shartnoma tuziladi.'},
        ]
        for data in faqs:
            FAQ.objects.get_or_create(question=data['question'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'{len(faqs)} ta FAQ yaratildi!'))

        self.stdout.write(self.style.SUCCESS('Boshlang\'ich ma\'lumotlar tayyor!'))
