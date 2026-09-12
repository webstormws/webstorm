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
        ('Web Development', 'Modern, responsive, and high-performance websites and web apps built with modern stacks.', 'fa-solid fa-code'),
        ('Mobile App Dev', 'iOS & Android apps that deliver seamless user experiences.', 'fa-solid fa-mobile-screen'),
        ('Cloud Solutions', 'Scalable, secure, and cost-effective cloud infrastructure & DevOps.', 'fa-solid fa-cloud'),
        ('IT Consulting', 'Strategic technology consulting to accelerate your growth.', 'fa-solid fa-shield-halved'),
        ('UI/UX Design', 'Beautiful, intuitive, and user-centered digital designs.', 'fa-solid fa-pen-nib'),
        ('AI & Machine Learning', 'Smart automation, predictive analytics and AI integrations.', 'fa-solid fa-robot'),
        ('E-Commerce', 'Online stores with payments, inventory and marketing built-in.', 'fa-solid fa-cart-shopping'),
        ('Digital Marketing', 'SEO, performance marketing and analytics that grow revenue.', 'fa-solid fa-chart-line'),
        ('Data & Analytics', 'Dashboards, data pipelines and insights that drive decisions.', 'fa-solid fa-database'),
    ]
    for i, (title, desc, icon) in enumerate(services):
        Service.objects.create(title=title, description=desc, icon=icon, order=i)

    projects = [
        ('FinTrack', 'Personal finance platform with AI-powered analytics.', 'web', 'from-slate-800 to-slate-900', 'fa-solid fa-chart-line'),
        ('EduPlatform', 'E-learning marketplace with live classes and certificates.', 'platform', 'from-blue-600 to-indigo-700', 'fa-solid fa-graduation-cap'),
        ('ShopEase', 'Headless commerce storefront with one-click checkout.', 'ecommerce', 'from-emerald-600 to-teal-800', 'fa-solid fa-cart-shopping'),
        ('TravelGo', 'Travel app with real-time flight tracking and local guides.', 'mobile', 'from-amber-500 to-orange-600', 'fa-solid fa-plane'),
        ('RentHub', 'Real estate marketplace with smart search and secure payments.', 'platform', 'from-sky-600 to-blue-800', 'fa-solid fa-building'),
        ('HealthTrack', 'Health monitoring app with wearable integrations and alerts.', 'mobile', 'from-fuchsia-600 to-purple-800', 'fa-solid fa-heart-pulse'),
    ]
    for i, (title, desc, cat, grad, icon) in enumerate(projects):
        Project.objects.create(title=title, description=desc, category=cat, gradient=grad, icon=icon, order=i)

    testimonials = [
        ('Sarah Kim', 'CEO, FinTrack',
         'Web Storm delivered our fintech platform three weeks early. The code quality, communication and attention to detail are the best we have experienced from any agency.',
         5, 'SK', 'from-brand-600 to-blue-400'),
        ('David Martinez', 'Founder, TravelGo',
         'Their mobile app helped us double our user base in six months. The team truly cares about the product and it shows in every release.',
         5, 'DM', 'from-indigo-600 to-sky-400'),
        ('Aisha Noor', 'COO, ShopEase',
         'From strategy to launch, Web Storm was with us every step of the way. Our e-commerce revenue grew 248% in the first year.',
         5, 'AN', 'from-emerald-600 to-teal-400'),
    ]
    for i, (name, role, quote, rating, initials, grad) in enumerate(testimonials):
        Testimonial.objects.create(name=name, role=role, quote=quote, rating=rating, initials=initials, gradient=grad, order=i)

    team = [
        ('Alex Johnson', 'CEO & Co-Founder', 'AJ', 'from-brand-600 to-blue-500'),
        ('Maria Lopez', 'CTO & Co-Founder', 'ML', 'from-indigo-600 to-sky-500'),
        ('James Carter', 'Head of Design', 'JC', 'from-emerald-600 to-teal-500'),
        ('Emma Stone', 'Lead Full-Stack Engineer', 'ES', 'from-amber-500 to-orange-500'),
    ]
    for i, (name, role, initials, grad) in enumerate(team):
        TeamMember.objects.create(name=name, role=role, initials=initials, gradient=grad, order=i)

    posts = [
        ('How AI Is Reshaping Software Development in 2026',
         'From AI pair programmers to automated testing, here is what is changing the way we build.',
         'Technology', 'from-brand-600 to-indigo-700', 'fa-solid fa-microchip', '5 min read'),
        ('7 Web Security Mistakes That Cost Businesses Millions',
         'Security is not optional. Learn the critical pitfalls and how to avoid them from day one.',
         'Security', 'from-emerald-600 to-teal-700', 'fa-solid fa-shield-halved', '7 min read'),
        ('Flutter vs React Native: Which One Wins in 2026?',
         'A practical comparison to help you pick the right cross-platform framework for your app.',
         'Mobile', 'from-amber-500 to-orange-600', 'fa-solid fa-mobile-screen-button', '4 min read'),
    ]
    for i, (title, excerpt, cat, grad, icon, read_time) in enumerate(posts):
        BlogPost.objects.create(title=title, excerpt=excerpt, category=cat, gradient=grad, icon=icon, read_time=read_time, order=i)

    faqs = [
        ('How long does a typical project take?',
         'Landing pages typically ship in 2-3 weeks, full websites in 4-8 weeks, and complex web or mobile apps in 3-6 months. We will give you a precise timeline after the discovery call.'),
        ('How much does a project cost?',
         'Projects start at $1,499 for a landing page. Pricing depends on scope, complexity and features. After a free consultation we will provide a transparent fixed-price quote — no surprises.'),
        ('Do you provide support after launch?',
         'Yes! Every project includes free support (30 days to 6 months depending on plan). We also offer ongoing maintenance and 24/7 monitoring packages for enterprise clients.'),
        ('Who owns the code and design?',
         'You do — 100%. Once the project is paid for, all code, designs and intellectual property belong entirely to you.'),
        ('Can you work with our existing team or stack?',
         'Absolutely. We integrate seamlessly with in-house teams and work across React, Vue, Django, Laravel, Flutter, AWS and more. We adapt to your tech stack, not the other way around.'),
        ('How do we get started?',
         'Just hit "Let\'s Talk" and book a free consultation. We will discuss your goals, answer your questions, and send you a proposal within 48 hours.'),
    ]
    for i, (question, answer) in enumerate(faqs):
        FAQItem.objects.create(question=question, answer=answer, order=i)

    jobs = [
        ('Senior Full-Stack Developer', 'Remote', 'Full-time', '$120k - $160k', 'fa-solid fa-code'),
        ('Product Designer (UI/UX)', 'Tashkent / Remote', 'Full-time', '$80k - $110k', 'fa-solid fa-pen-nib'),
        ('Machine Learning Engineer', 'San Francisco', 'Full-time', '$140k - $190k', 'fa-solid fa-database'),
    ]
    for i, (title, location, jtype, salary, icon) in enumerate(jobs):
        CareerJob.objects.create(title=title, location=location, job_type=jtype, salary=salary, icon=icon, order=i)

    stats = [
        ('Company Valuation', 200, 'M', '$', 'fa-solid fa-coins'),
        ('Projects Delivered', 100, '+', '', 'fa-solid fa-briefcase'),
        ('Skilled Professionals', 50, '+', '', 'fa-solid fa-users'),
        ('Countries Served', 20, '+', '', 'fa-solid fa-globe'),
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
