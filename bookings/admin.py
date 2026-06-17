from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, Enquiry, PortfolioPhoto, SiteVisit, WorkerApplication


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'services', 'area', 'date', 'status_badge', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('name', 'phone', 'area', 'services')
    list_editable = ('status',) if False else ()  # enable inline editing below
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'phone', 'area')
        }),
        ('Service Details', {
            'fields': ('services', 'date', 'time_slot', 'description')
        }),
        ('Admin', {
            'fields': ('status', 'admin_notes', 'created_at')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new':         '#2E86DE',
            'confirmed':   '#F4A61D',
            'in_progress': '#9B59B6',
            'completed':   '#27AE60',
            'cancelled':   '#E74C3C',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'service', 'status_badge', 'created_at')
    list_filter   = ('status', 'service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)

    fieldsets = (
        ('Contact', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Enquiry', {
            'fields': ('service', 'message')
        }),
        ('Admin', {
            'fields': ('status', 'reply', 'created_at')
        }),
    )

    def status_badge(self, obj):
        colors = {'new': '#2E86DE', 'replied': '#27AE60', 'closed': '#999'}
        color  = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display  = ('thumb', 'title', 'category', 'location', 'is_visible', 'order', 'created_at')
    list_editable = ('is_visible', 'order')
    list_filter   = ('category', 'is_visible')
    search_fields = ('title', 'location', 'caption')
    ordering      = ('order', '-created_at')

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '—'
    thumb.short_description = 'Preview'


@admin.register(WorkerApplication)
class WorkerApplicationAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'trade', 'experience_years', 'pincode', 'status_badge', 'created_at')
    list_filter   = ('status', 'trade', 'created_at')
    search_fields = ('name', 'phone', 'email', 'address', 'pincode')
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Applicant Info', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Skill & Experience', {
            'fields': ('trade', 'experience_years')
        }),
        ('Location', {
            'fields': ('address', 'pincode')
        }),
        ('Admin', {
            'fields': ('status', 'admin_notes', 'created_at')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'new':       '#2E86DE',
            'reviewing': '#F4A61D',
            'contacted': '#9B59B6',
            'hired':     '#27AE60',
            'rejected':  '#E74C3C',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('page', 'created_at')
    list_filter  = ('page', 'created_at')
    readonly_fields = ('page', 'ip_hash', 'user_agent', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
