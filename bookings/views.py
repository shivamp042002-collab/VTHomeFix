import json
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from .models import Booking, Enquiry, PortfolioPhoto, SiteVisit, WorkerApplication


# ─── Serve the main website ───────────────────────────────────────────────────
def index(request):
    """Serve the main single-page website"""
    photos = PortfolioPhoto.objects.filter(is_visible=True).order_by('order', '-created_at')[:12]
    return render(request, 'index.html', {'photos': photos})


# ─── Booking API ──────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def create_booking(request):
    try:
        data = json.loads(request.body)

        name  = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        area  = data.get('area', '').strip()

        # Validation
        if not all([name, phone, area]):
            return JsonResponse({'success': False, 'error': 'Name, phone and area are required.'}, status=400)
        if not phone.isdigit() or len(phone) != 10:
            return JsonResponse({'success': False, 'error': 'Enter a valid 10-digit phone number.'}, status=400)

        booking = Booking.objects.create(
            name        = name,
            phone       = phone,
            area        = area,
            services    = data.get('services', ''),
            date        = data.get('date') or None,
            time_slot   = data.get('timeSlot', ''),
            description = data.get('description', ''),
        )
        return JsonResponse({
            'success': True,
            'message': 'Booking received! Vinay bhai will call you within 2 hours.',
            'booking_id': booking.id,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please call 9503833197.'}, status=500)


# ─── Enquiry API ──────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def create_enquiry(request):
    try:
        data = json.loads(request.body)

        name    = data.get('name', '').strip()
        phone   = data.get('phone', '').strip()
        message = data.get('message', '').strip()

        if not all([name, phone, message]):
            return JsonResponse({'success': False, 'error': 'Name, phone and message are required.'}, status=400)
        if not phone.isdigit() or len(phone) != 10:
            return JsonResponse({'success': False, 'error': 'Enter a valid 10-digit phone number.'}, status=400)

        enquiry = Enquiry.objects.create(
            name    = name,
            phone   = phone,
            email   = data.get('email', '').strip(),
            service = data.get('service', ''),
            message = message,
        )
        return JsonResponse({
            'success': True,
            'message': 'Enquiry received! We will contact you within 4 hours.',
            'enquiry_id': enquiry.id,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please call 9503833197.'}, status=500)


# ─── Portfolio Photos API ─────────────────────────────────────────────────────
@require_http_methods(["GET"])
def get_photos(request):
    category = request.GET.get('category', '')
    photos = PortfolioPhoto.objects.filter(is_visible=True)
    if category:
        photos = photos.filter(category=category)
    photos = photos[:12]
    data = [{
        'id':       p.id,
        'title':    p.title,
        'category': p.category,
        'image':    request.build_absolute_uri(p.image.url),
        'caption':  p.caption,
        'location': p.location,
    } for p in photos]
    return JsonResponse({'success': True, 'photos': data})


# ─── Worker Application API ──────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def create_worker_application(request):
    try:
        data = json.loads(request.body)

        name    = data.get('name', '').strip()
        phone   = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        pincode = data.get('pincode', '').strip()

        if not all([name, phone, address, pincode]):
            return JsonResponse({'success': False, 'error': 'Name, phone, address and pincode are required.'}, status=400)
        if not phone.isdigit() or len(phone) != 10:
            return JsonResponse({'success': False, 'error': 'Enter a valid 10-digit phone number.'}, status=400)
        if not pincode.isdigit() or len(pincode) != 6:
            return JsonResponse({'success': False, 'error': 'Enter a valid 6-digit pincode.'}, status=400)

        exp_years = data.get('experienceYears', '')
        exp_years = int(exp_years) if str(exp_years).strip().isdigit() else None

        application = WorkerApplication.objects.create(
            name             = name,
            phone            = phone,
            email            = data.get('email', '').strip(),
            trade            = data.get('trade', 'other'),
            experience_years = exp_years,
            address          = address,
            pincode          = pincode,
        )
        return JsonResponse({
            'success': True,
            'message': 'Application received! We will contact you soon.',
            'application_id': application.id,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please call 9503833197.'}, status=500)


# ─── Admin Stats API ─────────────────────────────────────────────────────────
@staff_member_required
def admin_stats(request):
    stats = {
        'total_bookings':    Booking.objects.count(),
        'new_bookings':      Booking.objects.filter(status='new').count(),
        'total_enquiries':   Enquiry.objects.count(),
        'new_enquiries':     Enquiry.objects.filter(status='new').count(),
        'total_applications':WorkerApplication.objects.count(),
        'new_applications':  WorkerApplication.objects.filter(status='new').count(),
        'total_photos':      PortfolioPhoto.objects.count(),
        'visits_today':      SiteVisit.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
    }
    return JsonResponse(stats)


# ─── Track page visit ────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def track_visit(request):
    try:
        data = json.loads(request.body)
        ip   = request.META.get('REMOTE_ADDR', '')
        SiteVisit.objects.create(
            page       = data.get('page', '/')[:100],
            ip_hash    = hashlib.sha256(ip.encode()).hexdigest(),
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:300],
        )
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False})
