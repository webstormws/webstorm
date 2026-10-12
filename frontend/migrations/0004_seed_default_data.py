from django.db import migrations


def seed_data(apps, schema_editor):
    SiteSettings = apps.get_model('frontend', 'SiteSettings')
    Service = apps.get_model('frontend', 'Service')
    Project = apps.get_model('frontend', 'Project')
    Testimonial = apps.get_model('frontend', 'Testimonial')
    TeamMember = apps.get_model('frontend', 'TeamMember')
    BlogPost = apps.get_model('frontend', 'BlogPost')
    FAQItem = apps.get_model('frontend', 'FAQItem')
    CareerJob = apps.get_model('frontend', 'CareerJob')
    Stat = apps.get_model('frontend', 'Stat')

    if not SiteSettings.objects.exists():
        SiteSettings.objects.create()

    services = [
        ('Web sayt yaratish', 'Zamonaviy texnologiyalarda qurilgan, moslashuvchan va yuqori unumdorlikdagi web saytlar va ilovalar.', 'fa-solid fa-code'),
        ('Mobil ilova yaratish', 'iOS va Android uchun silliq foydalanuvchi tajribasini taqdim etuvchi ilovalar.', 'fa-solid fa-mobile-screen'),
        ('Bulut yechimlari', 'Kengaytiriladigan, xavfsiz va tejamkor bulut infratuzilmasi va DevOps.', 'fa-solid fa-cloud'),
        ('IT konsalting', "O'sishingizni tezlashtiruvchi strategik texnologik konsalting.", 'fa-solid fa-shield-halved'),
        ('UI/UX dizayn', "Chiroyli, qulay va foydalanuvchiga yo'naltirilgan raqamli dizaynlar.", 'fa-solid fa-pen-nib'),
        ("AI va mashinali o'rganish", 'Aqlli avtomatlashtirish, bashoratli analitika va AI integratsiyalari.', 'fa-solid fa-robot'),
        ('Elektron tijorat', "To'lov, ombor va marketing integratsiyalangan onlayn do'konlar.", 'fa-solid fa-cart-shopping'),
        ('Raqamli marketing', 'Daromadni oshiruvchi SEO, samaradorlik marketingi va analitika.', 'fa-solid fa-chart-line'),
        ("Ma'lumotlar va analitika", "Qarorlar qabul qilishga yordam beruvchi dashboardlar, ma'lumot oqimlari va tahlillar.", 'fa-solid fa-database'),
    ]
    for i, (title, desc, icon) in enumerate(services):
        Service.objects.create(title=title, description=desc, icon=icon, order=i)

    projects = [
        ('FinTrack', 'AI asosidagi analitikaga ega shaxsiy moliya platformasi.', 'web', 'from-slate-800 to-slate-900', 'fa-solid fa-chart-line'),
        ('EduPlatform', "Jonli darslar va sertifikatlarga ega elektron ta'lim bozori.", 'platform', 'from-blue-600 to-indigo-700', 'fa-solid fa-graduation-cap'),
        ('ShopEase', "Bir klikda to'lovga ega headless savdo vitrinasi.", 'ecommerce', 'from-emerald-600 to-teal-800', 'fa-solid fa-cart-shopping'),
        ('TravelGo', "Real vaqtda reys kuzatuvi va mahalliy yo'riqnomalarga ega sayohat ilovasi.", 'mobile', 'from-amber-500 to-orange-600', 'fa-solid fa-plane'),
        ('RentHub', "Aqlli qidiruv va xavfsiz to'lovlarga ega ko'chmas mulk bozori.", 'platform', 'from-sky-600 to-blue-800', 'fa-solid fa-building'),
        ('HealthTrack', "Kiyiladigan qurilmalar integratsiyasi va ogohlantirishlarga ega sog'liq monitoringi ilovasi.", 'mobile', 'from-fuchsia-600 to-purple-800', 'fa-solid fa-heart-pulse'),
    ]
    for i, (title, desc, cat, grad, icon) in enumerate(projects):
        Project.objects.create(title=title, description=desc, category=cat, gradient=grad, icon=icon, order=i)

    testimonials = [
        ('Sarah Kim', 'CEO, FinTrack',
         "Web Storm fintech platformamizni uch hafta oldin yetkazib berdi. Kod sifati, muloqot va tafsilotlarga e'tibor — biz ko'rgan eng yaxshisi.",
         5, 'SK', 'from-brand-600 to-blue-400'),
        ('David Martinez', 'Asoschi, TravelGo',
         "Ularning mobil ilovasi olti oyda foydalanuvchilar bazamizni ikki baravar oshirdi. Jamoa mahsulotga chin dildan g'amxo'rlik qiladi.",
         5, 'DM', 'from-indigo-600 to-sky-400'),
        ('Aisha Noor', 'COO, ShopEase',
         "Strategiyadan ishga tushirishgacha Web Storm har qadamda biz bilan edi. Elektron tijorat daromadimiz birinchi yilda 248% o'sdi.",
         5, 'AN', 'from-emerald-600 to-teal-400'),
    ]
    for i, (name, role, quote, rating, initials, grad) in enumerate(testimonials):
        Testimonial.objects.create(name=name, role=role, quote=quote, rating=rating, initials=initials, gradient=grad, order=i)

    team = [
        ('Alex Johnson', 'CEO va hammuassis', 'AJ', 'from-brand-600 to-blue-500'),
        ('Maria Lopez', 'CTO va hammuassis', 'ML', 'from-indigo-600 to-sky-500'),
        ('James Carter', "Dizayn bo'limi rahbari", 'JC', 'from-emerald-600 to-teal-500'),
        ('Emma Stone', 'Yetakchi Full-Stack dasturchi', 'ES', 'from-amber-500 to-orange-500'),
    ]
    for i, (name, role, initials, grad) in enumerate(team):
        TeamMember.objects.create(name=name, role=role, initials=initials, gradient=grad, order=i)

    posts = [
        ("AI 2026-yilda dasturiy ta'minot ishlab chiqishni qanday o'zgartirmoqda",
         "AI juft dasturchilardan avtomatik testlashgacha — bizning ishlab chiqish usulimizni nima o'zgartirmoqda.",
         'Texnologiya', 'from-brand-600 to-indigo-700', 'fa-solid fa-microchip', "5 daqiqa o'qish"),
        ('Biznesga millionlab zarar keltiradigan 7 ta web xavfsizlik xatosi',
         "Xavfsizlik ixtiyoriy emas. Muhim xatolarni va ulardan boshidanoq qanday qochishni o'rganing.",
         'Xavfsizlik', 'from-emerald-600 to-teal-700', 'fa-solid fa-shield-halved', "7 daqiqa o'qish"),
        ('Flutter yoki React Native: 2026-yilda qaysi biri yutadi?',
         "Ilovangiz uchun to'g'ri cross-platform framework tanlashga yordam beruvchi amaliy taqqoslash.",
         'Mobil', 'from-amber-500 to-orange-600', 'fa-solid fa-mobile-screen-button', "4 daqiqa o'qish"),
    ]
    for i, (title, excerpt, cat, grad, icon, read_time) in enumerate(posts):
        BlogPost.objects.create(title=title, excerpt=excerpt, category=cat, gradient=grad, icon=icon, read_time=read_time, order=i)

    faqs = [
        ('Odatda loyiha qancha vaqt oladi?',
         "Landing sahifalar odatda 2-3 haftada, to'liq saytlar 4-8 haftada, murakkab web yoki mobil ilovalar 3-6 oyda tayyor bo'ladi. Aniq muddatni tanishuv suhbatidan so'ng aytamiz."),
        ('Loyiha qancha turadi?',
         "Loyihalar landing sahifa uchun $1,499 dan boshlanadi. Narx hajm, murakkablik va funksiyalarga bog'liq. Bepul maslahatdan so'ng shaffof qat'iy narx taklifini beramiz — kutilmagan narsalarsiz."),
        ("Ishga tushirgandan keyin qo'llab-quvvatlaysizmi?",
         "Ha! Har bir loyiha bepul qo'llab-quvvatlashni o'z ichiga oladi (rejaga qarab 30 kundan 6 oygacha). Korporativ mijozlar uchun doimiy xizmat va 24/7 monitoring paketlarini ham taklif qilamiz."),
        ('Kod va dizayn kimga tegishli?',
         "Sizga — 100%. Loyiha to'langach, barcha kod, dizayn va intellektual mulk butunlay sizga tegishli."),
        ('Mavjud jamoamiz yoki texnologiyamiz bilan ishlay olasizmi?',
         'Albatta. Biz ichki jamoalar bilan bemalol integratsiyalashamiz va React, Vue, Django, Laravel, Flutter, AWS va boshqalar bilan ishlaymiz. Biz sizning texnologiyangizga moslashamiz.'),
        ('Qanday boshlaymiz?',
         '"Keling gaplashamiz" tugmasini bosing va bepul maslahatga yozing. Maqsadlaringizni muhokama qilamiz, savollaringizga javob beramiz va 48 soat ichida taklif yuboramiz.'),
    ]
    for i, (question, answer) in enumerate(faqs):
        FAQItem.objects.create(question=question, answer=answer, order=i)

    jobs = [
        ('Senior Full-Stack Developer', 'Masofadan', "To'liq kun", '$120k - $160k', 'fa-solid fa-code'),
        ('Product Designer (UI/UX)', 'Toshkent / Masofadan', "To'liq kun", '$80k - $110k', 'fa-solid fa-pen-nib'),
        ('Machine Learning Engineer', 'San Fransisko', "To'liq kun", '$140k - $190k', 'fa-solid fa-database'),
    ]
    for i, (title, location, jtype, salary, icon) in enumerate(jobs):
        CareerJob.objects.create(title=title, location=location, job_type=jtype, salary=salary, icon=icon, order=i)

    stats = [
        ('Kompaniya qiymati', 200, 'M', '$', 'fa-solid fa-coins'),
        ('Yetkazilgan loyihalar', 100, '+', '', 'fa-solid fa-briefcase'),
        ('Malakali mutaxassislar', 50, '+', '', 'fa-solid fa-users'),
        ("Xizmat ko'rsatilgan mamlakatlar", 20, '+', '', 'fa-solid fa-globe'),
    ]
    for i, (label, value, suffix, prefix, icon) in enumerate(stats):
        Stat.objects.create(label=label, value=value, suffix=suffix, prefix=prefix, icon=icon, order=i)


def remove_data(apps, schema_editor):
    for model_name in ['Stat', 'CareerJob', 'FAQItem', 'BlogPost', 'TeamMember',
                       'Testimonial', 'Project', 'Service', 'SiteSettings']:
        apps.get_model('frontend', model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_blogpost_careerjob_faqitem_project_service_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
