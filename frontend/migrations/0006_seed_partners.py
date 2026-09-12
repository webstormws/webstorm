from django.db import migrations


def seed_partners(apps, schema_editor):
    Partner = apps.get_model('frontend', 'Partner')
    partners = [
        ('Google', 'fa-brands fa-google', 'text-blue-500'),
        ('Microsoft', 'fa-brands fa-microsoft', 'text-blue-600'),
        ('Laravel', 'fa-brands fa-laravel', 'text-red-500'),
        ('AWS', 'fa-brands fa-aws', 'text-orange-500'),
        ('DigitalOcean', 'fa-brands fa-digital-ocean', 'text-blue-500'),
        ('React', 'fa-brands fa-react', 'text-cyan-500'),
        ('Apple', 'fa-brands fa-apple', 'text-gray-400'),
        ('Stripe', 'fa-brands fa-stripe', 'text-indigo-500'),
    ]
    for i, (name, icon, color) in enumerate(partners):
        Partner.objects.create(name=name, icon=icon, icon_color=color, order=i)


def remove_partners(apps, schema_editor):
    apps.get_model('frontend', 'Partner').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_partner'),
    ]

    operations = [
        migrations.RunPython(seed_partners, remove_partners),
    ]
