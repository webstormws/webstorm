from django.contrib import admin
from .models import (SiteSettings, Service, Project, Testimonial, TeamMember,
                     BlogPost, FAQItem, CareerJob, Stat, Partner)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title',)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'order')
    list_editable = ('order',)
    search_fields = ('name',)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    search_fields = ('name',)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title',)


class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)


class CareerJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'salary', 'order')
    list_editable = ('order',)
    search_fields = ('title',)


class StatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('order',)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)


admin.site.register(SiteSettings)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(FAQItem, FAQItemAdmin)
admin.site.register(CareerJob, CareerJobAdmin)
admin.site.register(Stat, StatAdmin)
admin.site.register(Partner, PartnerAdmin)
