import json
import hashlib
import os
import urllib.request
import urllib.error
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from .models import Booking, Enquiry, PortfolioPhoto, SiteVisit, WorkerApplication, CustomerReview


CHATBOT_SYSTEM_PROMPT = """You are Shivam, a friendly and helpful assistant for VTHomeFix (run by Vinay Tiwari), a professional home services company based in Vasai, Mumbai, India, serving the entire Western Line from Virar to Borivali.

ABOUT THE BUSINESS:
- Owner: Vinay Tiwari, 20+ years experience
- Location: Vasai, Maharashtra (Western Line, Mumbai)
- Phone: 9503833197
- Email: Vinaytiwari59352@gmail.com
- WhatsApp: 9503833197
- Working Hours: Monday to Saturday, 8 AM to 8 PM
- Languages: Hindi, English

SERVICES OFFERED:
1. PAINTING SERVICES (starts ₹12/sq.ft): Interior/exterior painting, putty work, texture paint, waterproofing, enamel paint, wood polish.
2. CARPENTRY: Modular kitchen, wardrobes, TV units, door/window frames, false ceiling frames, loft storage.
3. TILES FITTING (starts ₹25/sq.ft): Floor/wall tiles, bathroom/kitchen tiles, marble & granite, grouting, old tile replacement.
4. ELECTRICAL WORK: Complete home wiring, switchboard installation, fan/light fitting, MCB/DB box, AC point, geyser point, short circuit repair.
5. POP CEILING (starts ₹55/sq.ft): POP false ceiling, gypsum board ceiling, ceiling design, punning, LED cove lighting.

SERVICE AREAS: Vasai, Virar, Nalasopara, Mira Road, Bhayandar, Naigaon, Borivali, Kandivali, Malad, Andheri, Dadar — full Western Line Mumbai.

HIRING: VTHomeFix is also hiring skilled painters, carpenters, tile-fitters, electricians, and plumbers. Direct interested workers to the "Join Our Team" page.

KEY SELLING POINTS: Free site visit and quotation, on-time guarantee, transparent pricing, quality guarantee, clean worksite, background-verified team, 500+ happy customers.

Be conversational, helpful, and friendly in Hinglish or English as the user prefers. Keep responses short (2-4 sentences). Always encourage them to call 9503833197, WhatsApp, or use the Book a Service page. If asked about pricing, give the approximate ranges above but mention final quote depends on a free site visit."""


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_reply(request):
    """Securely proxy chat messages to Claude API using a server-side key."""
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return JsonResponse({
            'success': False,
            'reply': "Sorry, I'm not fully set up yet! Please call us directly at 9503833197 or WhatsApp us — we're happy to help. 😊"
        })

    try:
        data = json.loads(request.body)
        messages = data.get('messages', [])[-10:]  # last 10 turns only

        payload = json.dumps({
            'model': 'claude-sonnet-4-6',
            'max_tokens': 400,
            'system': CHATBOT_SYSTEM_PROMPT,
            'messages': messages,
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
            },
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        reply_text = ''
        for block in result.get('content', []):
            if block.get('type') == 'text':
                reply_text += block.get('text', '')

        if not reply_text:
            reply_text = "Sorry, I couldn't understand that. Please call us at 9503833197!"

        return JsonResponse({'success': True, 'reply': reply_text})

    except urllib.error.HTTPError as e:
        return JsonResponse({
            'success': False,
            'reply': "Sorry, I'm having trouble right now! Please call us at 9503833197 or WhatsApp us directly. 😊"
        })
    except Exception:
        return JsonResponse({
            'success': False,
            'reply': "Sorry, something went wrong! Please call us at 9503833197 or WhatsApp us directly. 😊"
        })


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


# ─── Customer Review API ─────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def create_review(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        review_text = data.get('reviewText', '').strip()

        if not name or not review_text:
            return JsonResponse({'success': False, 'error': 'Name and review text are required.'}, status=400)

        rating = data.get('rating', 5)
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        CustomerReview.objects.create(
            name        = name,
            location    = data.get('location', '').strip(),
            rating      = rating,
            review_text = review_text,
            service     = data.get('service', '').strip(),
        )
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your review has been submitted and will appear soon.',
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Something went wrong. Please try again.'}, status=500)


@require_http_methods(["GET"])
def get_reviews(request):
    reviews = CustomerReview.objects.filter(is_approved=True)[:12]
    data = [{
        'name':     r.name,
        'location': r.location,
        'rating':   r.rating,
        'text':     r.review_text,
        'service':  r.service,
    } for r in reviews]
    return JsonResponse({'success': True, 'reviews': data})


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
