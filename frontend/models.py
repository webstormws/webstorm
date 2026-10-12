from django.db import models


class SiteSettings(models.Model):
    """Saytning umumiy sozlamalari (bitta yozuv ishlatiladi)."""
    site_name = models.CharField(max_length=100, default='Web Storm')
    site_tagline = models.CharField(max_length=100, default="IT KOMPANIYA")
    hero_badge = models.CharField(max_length=100, default="BIZ KELAJAKNI QURAMIZ")
    hero_title_line1 = models.CharField(max_length=100, default="Kuchli")
    hero_title_line2 = models.CharField(max_length=100, default="raqamli yechimlar")
    hero_title_line3 = models.CharField(max_length=100, default="o'sishga olib boradi")
    hero_subtitle = models.TextField(
        default="Web Storm — global bizneslar uchun innovatsion dasturiy ta'minot, web va mobil yechimlar yaratuvchi yangi avlod IT kompaniyasi.")
    about_text = models.TextField(
        default="Biz o'zgarish yaratuvchi texnologiyalar yaratishga bag'ishlangan g'ayratli innovatorlar, dasturchilar va muammo yechuvchilar jamoasimiz.")
    mission_text = models.CharField(max_length=300,
                                    default="Dunyo bo'ylab bizneslarni kuchaytiruvchi innovatsion IT yechimlar taqdim etish.")
    vision_text = models.CharField(max_length=300,
                                   default="Texnologiya va raqamli transformatsiyada global yetakchi bo'lish.")
    values_text = models.CharField(max_length=300, default="Innovatsiya, halollik, mukammallik va ta'sir.")
    valuation_value = models.CharField(max_length=30, default='$200,000,000')
    valuation_label = models.CharField(max_length=100, default="Kompaniya qiymati")
    valuation_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Valuation rasm (WebStorm logosi)')
    email = models.EmailField(default='hello@webstorm.com')
    phone = models.CharField(max_length=50, default='+1 (555) 123-4567')
    address = models.CharField(max_length=200, default="Toshkent, O'zbekiston")
    working_hours = models.CharField(max_length=100, default="Dush - Shan: 9:00 - 18:00")
    footer_text = models.TextField(
        default="Kelajakni kod, dizayn va innovatsiya bilan quramiz. Bizneslarni global miqyosda yuqori natijali dasturiy yechimlar bilan ta'minlaymiz.")
    copyright_text = models.CharField(max_length=200, default="© 2026 Web Storm IT kompaniyasi. Barcha huquqlar himoyalangan.")
    trusted_text = models.CharField(max_length=200, default="Dunyo bo'ylab 100+ kompaniya ishonchi")
    clients_count = models.IntegerField(default=100)
    rating = models.CharField(max_length=10, default='4.9/5')
    stats_title = models.CharField(max_length=100, default="Raqamlarimiz")
    services_title = models.CharField(max_length=100, default="Xizmatlarimiz")
    services_text = models.TextField(
        default="Birinchi wireframe'dan yakuniy joylashtirishgacha — natijaga yo'naltirilgan to'liq raqamli yechimlar.")
    projects_title = models.CharField(max_length=100, default="Tanlangan loyihalar")
    projects_text = models.TextField(
        default="Dunyo bo'ylab mijozlarimiz uchun ishlab chiqilgan va yetkazib berilgan mahsulotlardan tanlov.")
    testimonials_title = models.CharField(max_length=100, default="Mijozlarimiz nima deydi")
    testimonials_text = models.TextField(
        default="Biz yordam bergan bizneslarning haqiqiy fikrlari.")
    pricing_title = models.CharField(max_length=100, default="Oddiy, shaffof rejalar")
    pricing_text = models.TextField(default="Maqsadlaringizga mos rejani tanlang.")
    team_title = models.CharField(max_length=100, default="Sehr ortidagi iste'dodlar bilan tanishing")
    team_text = models.TextField(
        default="Texnologiyaga oshiq 50+ muhandis, dizayner va strateg.")
    blog_title = models.CharField(max_length=100, default="So'nggi yangiliklar")
    blog_text = models.TextField(default="Ekspertlarimizdan g'oyalar, maslahatlar va trendlar.")
    faq_title = models.CharField(max_length=100, default="Ko'p beriladigan savollar")
    faq_text = models.TextField(default="Loyihangizni boshlashdan oldin bilishingiz kerak bo'lgan hamma narsa.")
    careers_title = models.CharField(max_length=100, default="O'sib borayotgan jamoamizga qo'shiling")
    careers_text = models.TextField(
        default="Biz doimo ajoyib mahsulotlar yaratishni yaxshi ko'radigan iqtidorli insonlarni qidiramiz.")
    newsletter_title = models.CharField(max_length=100, default="Yangiliklardan xabardor bo'ling")
    newsletter_text = models.TextField(
        default="Eksklyuziv yangiliklar, maslahatlar va texnologik trendlar uchun obuna bo'ling. Hech qachon spam yo'q.")
    contact_title = models.CharField(max_length=100, default="Bog'laning")
    contact_text = models.TextField(
        default="Loyihangiz va maqsadlaringizga qanday yordam bera olishimiz haqida eshitishni xohlaymiz. 24 soat ichida javob beramiz.")
    cta_title = models.CharField(max_length=150, default="Ajoyib narsa yaratishga tayyormisiz?")
    cta_text = models.TextField(
        default="G'oyalaringizni kuchli raqamli yechimlarga aylantiramiz. Bepul maslahat — hech qanday majburiyatsiz.")
    logo_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Logo rasm (ixtiyoriy)')
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Hero markaziy rasm (W o\'rniga)')

    class Meta:
        verbose_name = 'Sayt sozlamalari'
        verbose_name_plural = 'Sayt sozlamalari'

    def __str__(self):
        return 'Sayt sozlamalari'


class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name='Xizmat nomi')
    description = models.TextField(verbose_name='Tavsif')
    icon = models.CharField(max_length=50, default='fa-solid fa-code',
                            help_text='FontAwesome icon nomi, masalan: fa-solid fa-code',
                            verbose_name='Icon')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'
        ordering = ['order']

    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web ilova'),
        ('mobile', 'Mobil ilova'),
        ('ecommerce', 'Elektron tijorat'),
        ('platform', 'Platforma'),
    ]
    title = models.CharField(max_length=150, verbose_name='Loyiha nomi')
    description = models.TextField(verbose_name='Tavsif')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web',
                                verbose_name='Kategoriya')
    image = models.ImageField(upload_to='projects/', blank=True, null=True,
                              verbose_name='Rasm (ixtiyoriy)')
    gradient = models.CharField(max_length=100, default='from-slate-800 to-slate-900',
                                help_text='Rasm bo\'lmasa ishlatiladigan gradient', verbose_name='Gradient')
    icon = models.CharField(max_length=50, default='fa-solid fa-chart-line',
                            verbose_name='Icon (rasm bo\'lmasa)')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Loyiha'
        verbose_name_plural = 'Loyihalar'
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ism')
    role = models.CharField(max_length=150, verbose_name='Lavozim')
    quote = models.TextField(verbose_name='Fikr')
    rating = models.PositiveIntegerField(default=5, verbose_name='Baho (1-5)')
    avatar_image = models.ImageField(upload_to='testimonials/', blank=True, null=True,
                                     verbose_name='Rasm (ixtiyoriy)')
    initials = models.CharField(max_length=4, default='AK', verbose_name='Harflar (rasm bo\'lmasa)')
    gradient = models.CharField(max_length=100, default='from-brand-600 to-blue-400',
                                verbose_name='Gradient')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Mijoz fikri'
        verbose_name_plural = 'Mijoz fikrlari'
        ordering = ['order']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ism')
    role = models.CharField(max_length=150, verbose_name='Lavozim')
    photo = models.ImageField(upload_to='team/', blank=True, null=True,
                              verbose_name='Rasm (ixtiyoriy)')
    initials = models.CharField(max_length=4, default='AJ', verbose_name='Harflar (rasm bo\'lmasa)')
    gradient = models.CharField(max_length=100, default='from-brand-600 to-blue-500',
                                verbose_name='Gradient')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    twitter = models.URLField(blank=True, verbose_name='Twitter/X')
    github = models.URLField(blank=True, verbose_name='GitHub')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Jamoa a\'zosi'
        verbose_name_plural = 'Jamoa a\'zolari'
        ordering = ['order']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    excerpt = models.TextField(verbose_name='Qisqacha matn')
    category = models.CharField(max_length=100, default="Texnologiya", verbose_name='Kategoriya')
    image = models.ImageField(upload_to='blog/', blank=True, null=True,
                              verbose_name='Rasm (ixtiyoriy)')
    gradient = models.CharField(max_length=100, default='from-brand-600 to-indigo-700',
                                verbose_name='Gradient')
    icon = models.CharField(max_length=50, default='fa-solid fa-microchip',
                            verbose_name='Icon (rasm bo\'lmasa)')
    date = models.DateField(auto_now_add=True, verbose_name='Sana')
    read_time = models.CharField(max_length=20, default="5 daqiqa o'qish", verbose_name='O\'qish vaqti')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog postlar'
        ordering = ['-date']

    def __str__(self):
        return self.title


class FAQItem(models.Model):
    question = models.CharField(max_length=300, verbose_name='Savol')
    answer = models.TextField(verbose_name='Javob')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'FAQ savol'
        verbose_name_plural = 'FAQ savollar'
        ordering = ['order']

    def __str__(self):
        return self.question


class CareerJob(models.Model):
    title = models.CharField(max_length=200, verbose_name='Lavozim')
    location = models.CharField(max_length=100, default="Masofadan", verbose_name='Joylashuv')
    job_type = models.CharField(max_length=50, default="To'liq kun", verbose_name='Ish turi')
    salary = models.CharField(max_length=100, default='$100k - $150k', verbose_name='Maosh')
    icon = models.CharField(max_length=50, default='fa-solid fa-code', verbose_name='Icon')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Ish o\'rni'
        verbose_name_plural = 'Ish o\'rinlari'
        ordering = ['order']

    def __str__(self):
        return self.title


class Stat(models.Model):
    label = models.CharField(max_length=100, verbose_name='Yozuv nomi')
    value = models.PositiveIntegerField(default=100, verbose_name='Qiymat')
    suffix = models.CharField(max_length=10, default='+', verbose_name='Qo\'shimcha belgi')
    prefix = models.CharField(max_length=10, default='', verbose_name='Old belgi (masalan $)')
    icon = models.CharField(max_length=50, default='fa-solid fa-coins', verbose_name='Icon')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'
        ordering = ['order']

    def __str__(self):
        return self.label


class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kompaniya nomi')
    logo_image = models.ImageField(upload_to='partners/', blank=True, null=True,
                                   verbose_name='Logo rasm')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Hamkor logo'
        verbose_name_plural = 'Hamkor logolar (carousel)'
        ordering = ['order']

    def __str__(self):
        return self.name
