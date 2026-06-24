from django.db import models
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [
        ('new',      'New'),
        ('confirmed','Confirmed'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]
    SERVICE_CHOICES = [
        ('painting',    'Painting'),
        ('carpentry',   'Carpentry'),
        ('tiles',       'Tiles Fitting'),
        ('electrical',  'Electrical'),
        ('pop_ceiling', 'POP Ceiling'),
        ('multiple',    'Multiple Services'),
    ]

    name        = models.CharField(max_length=120)
    phone       = models.CharField(max_length=15)
    area        = models.CharField(max_length=150)
    services    = models.CharField(max_length=300)          # comma-separated
    date        = models.DateField(null=True, blank=True)
    time_slot   = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at  = models.DateTimeField(default=timezone.now)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.name} — {self.services} ({self.created_at.strftime('%d %b %Y')})"


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new',      'New'),
        ('replied',  'Replied'),
        ('closed',   'Closed'),
    ]

    name       = models.CharField(max_length=120)
    phone      = models.CharField(max_length=15)
    email      = models.EmailField(blank=True)
    service    = models.CharField(max_length=80, blank=True)
    message    = models.TextField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)
    reply      = models.TextField(blank=True, help_text="Admin reply notes")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.name} — {self.service or 'General'} ({self.created_at.strftime('%d %b %Y')})"


class PortfolioPhoto(models.Model):
    CATEGORY_CHOICES = [
        ('painting',    'Painting'),
        ('carpentry',   'Carpentry'),
        ('tiles',       'Tiles Fitting'),
        ('electrical',  'Electrical'),
        ('pop_ceiling', 'POP Ceiling'),
        ('other',       'Other'),
    ]

    title      = models.CharField(max_length=160)
    category   = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    image      = models.ImageField(upload_to='portfolio/%Y/%m/')
    caption    = models.CharField(max_length=200, blank=True)
    location   = models.CharField(max_length=100, blank=True, help_text="e.g. Vasai West")
    is_visible = models.BooleanField(default=True)
    order      = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Portfolio Photo'
        verbose_name_plural = 'Portfolio Photos'

    def __str__(self):
        return f"{self.title} ({self.category})"


class CustomerReview(models.Model):
    name        = models.CharField(max_length=120)
    location    = models.CharField(max_length=100, blank=True, help_text="e.g. Vasai West")
    rating      = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    review_text = models.TextField()
    service     = models.CharField(max_length=80, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Only approved reviews show on the site")
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer Review'
        verbose_name_plural = 'Customer Reviews'

    def __str__(self):
        return f"{self.name} — {self.rating}★ ({self.created_at.strftime('%d %b %Y')})"


class WorkerApplication(models.Model):
    STATUS_CHOICES = [
        ('new',       'New'),
        ('reviewing', 'Reviewing'),
        ('contacted', 'Contacted'),
        ('hired',     'Hired'),
        ('rejected',  'Not Suitable'),
    ]
    TRADE_CHOICES = [
        ('painting',    'Painting'),
        ('carpentry',   'Carpentry'),
        ('tiles',       'Tiles Fitting'),
        ('electrical',  'Electrical'),
        ('pop_ceiling', 'POP Ceiling'),
        ('plumbing',    'Plumbing'),
        ('other',       'Other'),
    ]

    name          = models.CharField(max_length=120)
    phone         = models.CharField(max_length=15)
    email         = models.EmailField(blank=True)
    trade         = models.CharField(max_length=30, choices=TRADE_CHOICES, default='other')
    experience_years = models.PositiveIntegerField(null=True, blank=True, help_text="Years of experience")
    address       = models.CharField(max_length=200, help_text="Short address")
    pincode       = models.CharField(max_length=10)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes   = models.TextField(blank=True)
    created_at    = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Worker Application'
        verbose_name_plural = 'Worker Applications'

    def __str__(self):
        return f"{self.name} — {self.get_trade_display()} ({self.created_at.strftime('%d %b %Y')})"


class SiteVisit(models.Model):
    """Simple analytics — track page visits"""
    page       = models.CharField(max_length=100)
    ip_hash    = models.CharField(max_length=64)        # hashed, not raw IP
    user_agent = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.page} — {self.created_at.strftime('%d %b %Y %H:%M')}"
