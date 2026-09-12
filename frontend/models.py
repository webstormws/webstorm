from django.db import models


class SiteSettings(models.Model):
    """Saytning umumiy sozlamalari (bitta yozuv ishlatiladi)."""
    site_name = models.CharField(max_length=100, default='Web Storm')
    site_tagline = models.CharField(max_length=100, default='IT COMPANY')
    hero_badge = models.CharField(max_length=100, default='WE BUILD THE FUTURE')
    hero_title_line1 = models.CharField(max_length=100, default='Building Powerful')
    hero_title_line2 = models.CharField(max_length=100, default='Digital Solutions')
    hero_title_line3 = models.CharField(max_length=100, default='That Drive Growth')
    hero_subtitle = models.TextField(
        default='Web Storm is a next-generation IT company delivering innovative software, web, and mobile solutions for global businesses.')
    about_text = models.TextField(
        default='We are a team of passionate innovators, developers, and problem solvers dedicated to building technology that makes a difference.')
    mission_text = models.CharField(max_length=300,
                                    default='Deliver innovative IT solutions that empower businesses worldwide.')
    vision_text = models.CharField(max_length=300,
                                   default='Be a global leader in technology and digital transformation.')
    values_text = models.CharField(max_length=300, default='Innovation, Integrity, Excellence, and Impact.')
    valuation_value = models.CharField(max_length=30, default='$200,000,000')
    valuation_label = models.CharField(max_length=100, default='Company Valuation')
    valuation_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Valuation rasm (WebStorm logosi)')
    email = models.EmailField(default='hello@webstorm.com')
    phone = models.CharField(max_length=50, default='+1 (555) 123-4567')
    address = models.CharField(max_length=200, default='123 Innovation Drive, San Francisco, CA')
    working_hours = models.CharField(max_length=100, default='Mon - Sat: 9:00 - 18:00')
    footer_text = models.TextField(
        default='Building the future with code, design, and innovation. Empowering businesses globally with high-impact software solutions.')
    copyright_text = models.CharField(max_length=200, default='© 2026 Web Storm IT Company. All rights reserved.')
    trusted_text = models.CharField(max_length=200, default='Trusted by 100+ companies worldwide')
    clients_count = models.IntegerField(default=100)
    rating = models.CharField(max_length=10, default='4.9/5')
    stats_title = models.CharField(max_length=100, default='Our Numbers')
    services_title = models.CharField(max_length=100, default='Our Services')
    services_text = models.TextField(
        default='End-to-end digital solutions designed to move the needle — from first wireframe to final deployment.')
    projects_title = models.CharField(max_length=100, default='Featured Projects')
    projects_text = models.TextField(
        default='A selection of products we have designed, built and shipped for clients around the world.')
    testimonials_title = models.CharField(max_length=100, default='What Our Clients Say')
    testimonials_text = models.TextField(
        default='Real feedback from the businesses we have helped grow.')
    pricing_title = models.CharField(max_length=100, default='Simple, Transparent Plans')
    pricing_text = models.TextField(default='Choose a plan that fits your goals.')
    team_title = models.CharField(max_length=100, default='Meet the Minds Behind the Magic')
    team_text = models.TextField(
        default='50+ engineers, designers and strategists passionate about technology.')
    blog_title = models.CharField(max_length=100, default='Latest Insights')
    blog_text = models.TextField(default='Ideas, tips and trends from our team of experts.')
    faq_title = models.CharField(max_length=100, default='Frequently Asked Questions')
    faq_text = models.TextField(default='Everything you need to know before starting your project.')
    careers_title = models.CharField(max_length=100, default='Join Our Growing Team')
    careers_text = models.TextField(
        default="We're always looking for talented people who love building great products.")
    newsletter_title = models.CharField(max_length=100, default='Stay Ahead of the Curve')
    newsletter_text = models.TextField(
        default='Subscribe to our newsletter for exclusive insights, tips and tech trends. No spam, ever.')
    contact_title = models.CharField(max_length=100, default='Get In Touch')
    contact_text = models.TextField(
        default="We'd love to hear about your project and how we can help you achieve your goals. We reply within 24 hours.")
    cta_title = models.CharField(max_length=150, default='Ready to Build Something Amazing?')
    cta_text = models.TextField(
        default="Let's turn your ideas into powerful digital solutions. Free consultation — no strings attached.")
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
        ('web', 'Web App'),
        ('mobile', 'Mobile App'),
        ('ecommerce', 'E-Commerce'),
        ('platform', 'Platform'),
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
    category = models.CharField(max_length=100, default='Technology', verbose_name='Kategoriya')
    image = models.ImageField(upload_to='blog/', blank=True, null=True,
                              verbose_name='Rasm (ixtiyoriy)')
    gradient = models.CharField(max_length=100, default='from-brand-600 to-indigo-700',
                                verbose_name='Gradient')
    icon = models.CharField(max_length=50, default='fa-solid fa-microchip',
                            verbose_name='Icon (rasm bo\'lmasa)')
    date = models.DateField(auto_now_add=True, verbose_name='Sana')
    read_time = models.CharField(max_length=20, default='5 min read', verbose_name='O\'qish vaqti')
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
    location = models.CharField(max_length=100, default='Remote', verbose_name='Joylashuv')
    job_type = models.CharField(max_length=50, default='Full-time', verbose_name='Ish turi')
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
