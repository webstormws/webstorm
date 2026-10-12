from django.db import models
from django.contrib.auth.models import AbstractUser


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    first_name = models.CharField(max_length=200, blank=True, default='', verbose_name='Ism')
    last_name = models.CharField(max_length=200, blank=True, default='', verbose_name='Familiya')
    username = models.CharField(max_length=200, blank=True, default='', verbose_name='Username')
    phone = models.CharField(max_length=30, blank=True, default='', verbose_name='Telefon')
    language = models.CharField(max_length=10, default='uz', verbose_name='Til')
    first_seen = models.DateTimeField(auto_now_add=True, verbose_name='Birinchi kirish')
    last_active = models.DateTimeField(auto_now=True, verbose_name='Oxirgi faollik')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-first_seen']

    def __str__(self):
        return f"{self.first_name} (@{self.username})" if self.username else self.first_name


class BotAdmin(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, related_name='bot_admin_profile', verbose_name='Foydalanuvchi')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin', verbose_name='Rol')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'

    def __str__(self):
        return f"{self.user.first_name} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'


class BotSetting(models.Model):
    bot_name = models.CharField(max_length=100, default='Web Storm Bot', verbose_name='Bot nomi')
    start_message = models.TextField(default='🚀 WEB STORM\n\nBiznesingiz uchun zamonaviy IT yechimlar.', verbose_name='Start xabar')
    about_text = models.TextField(default='Web Storm — zamonaviy IT kompaniya. Biznesingiz uchun professional yechimlar yaratamiz.', verbose_name='Kompaniya haqida')
    phone = models.CharField(max_length=30, default='+998 XX XXX XX XX', verbose_name='Telefon')
    telegram_username = models.CharField(max_length=100, default='@webstorm', verbose_name='Telegram username')
    instagram = models.CharField(max_length=100, blank=True, default='', verbose_name='Instagram')
    website = models.URLField(blank=True, default='', verbose_name='Website')
    address = models.CharField(max_length=300, blank=True, default='', verbose_name='Manzil')
    logo = models.ImageField(upload_to='bot/', blank=True, null=True, verbose_name='Logo')
    is_bot_active = models.BooleanField(default=True, verbose_name='Bot faol')

    class Meta:
        verbose_name = 'Bot sozlamasi'
        verbose_name_plural = 'Bot sozlamalari'

    def __str__(self):
        return self.bot_name

    def save(self, *args, **kwargs):
        if not self.pk and BotSetting.objects.exists():
            raise ValueError('Faqat bitta BotSetting bo\'lishi mumkin!')
        super().save(*args, **kwargs)


class Service(models.Model):
    icon = models.CharField(max_length=50, default='💼', verbose_name='Emoji icon')
    name = models.CharField(max_length=200, verbose_name='Xizmat nomi')
    description = models.TextField(verbose_name='Tavsif')
    target_audience = models.CharField(max_length=300, blank=True, default='', verbose_name='Kimlar uchun')
    features = models.TextField(blank=True, default='', verbose_name='Asosiy imkoniyatlar (qator bo\'yicha)')
    price_info = models.CharField(max_length=200, default='Narx kelishiladi', verbose_name='Narx ma\'lumot')
    image = models.ImageField(upload_to='bot/services/', blank=True, null=True, verbose_name='Rasm')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'
        ordering = ['order']

    def __str__(self):
        return f"{self.icon} {self.name}"


class ServicePackage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packages', verbose_name='Xizmat')
    name = models.CharField(max_length=100, verbose_name='Paket nomi')
    price = models.CharField(max_length=100, verbose_name='Narx')
    features = models.TextField(verbose_name='Imkoniyatlar (qator bo\'yicha)')
    description = models.TextField(blank=True, default='', verbose_name='Tavsif')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Xizmat paketi'
        verbose_name_plural = 'Xizmat paketlari'
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class PortfolioItem(models.Model):
    CATEGORY_CHOICES = [
        ('crm', 'CRM'),
        ('bot', 'Telegram Bot'),
        ('website', 'Web Sayt'),
        ('webapp', 'Web App'),
        ('mobile', 'Mobile App'),
        ('automation', 'Automation'),
    ]
    title = models.CharField(max_length=200, verbose_name='Loyiha nomi')
    description = models.TextField(verbose_name='Tavsif')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='website', verbose_name='Kategoriya')
    technologies = models.CharField(max_length=300, blank=True, default='', verbose_name='Texnologiyalar')
    demo_url = models.URLField(blank=True, default='', verbose_name='Demo URL')
    image = models.ImageField(upload_to='bot/portfolio/', blank=True, null=True, verbose_name='Preview rasm')
    date = models.DateField(auto_now_add=True, verbose_name='Sana')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Portfolio loyiha'
        verbose_name_plural = 'Portfolio loyihalar'
        ordering = ['-date']

    def __str__(self):
        return self.title


class WebsiteItem(models.Model):
    name = models.CharField(max_length=200, verbose_name='Sayt nomi')
    description = models.TextField(verbose_name='Qisqa tavsif')
    url = models.URLField(verbose_name='URL')
    category = models.CharField(max_length=100, blank=True, default='', verbose_name='Kategoriya')
    technologies = models.CharField(max_length=300, blank=True, default='', verbose_name='Texnologiyalar')
    image = models.ImageField(upload_to='bot/websites/', blank=True, null=True, verbose_name='Preview rasm')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        verbose_name = 'Web sayt'
        verbose_name_plural = 'Web saytlar'
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name='Savol')
    answer = models.TextField(verbose_name='Javob')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Savol-javob'
        verbose_name_plural = 'Savol-javoblar'
        ordering = ['order']

    def __str__(self):
        return self.question


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('contacted', 'Bog\'lanildi'),
        ('negotiation', 'Muzokara'),
        ('waiting', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Tugallandi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Foydalanuvchi')
    name = models.CharField(max_length=200, verbose_name='Ism')
    phone = models.CharField(max_length=30, verbose_name='Telefon')
    business_type = models.CharField(max_length=200, blank=True, default='', verbose_name='Biznes turi')
    service = models.CharField(max_length=200, verbose_name='Xizmat')
    description = models.TextField(blank=True, default='', verbose_name='Loyiha haqida')
    budget = models.CharField(max_length=100, blank=True, default='', verbose_name='Taxminiy budjet')
    comment = models.TextField(blank=True, default='', verbose_name='Qo\'shimcha izoh')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Holat')
    assigned_admin = models.ForeignKey(BotAdmin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mas\'ul admin')
    internal_note = models.TextField(blank=True, default='', verbose_name='Ichki izoh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service} ({self.get_status_display()})"
