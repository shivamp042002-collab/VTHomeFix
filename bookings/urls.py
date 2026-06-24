from django.urls import path
from . import views

urlpatterns = [
    # Website
    path('',                    views.index,          name='index'),

    # REST API endpoints
    path('api/booking/',        views.create_booking, name='api_booking'),
    path('api/enquiry/',        views.create_enquiry, name='api_enquiry'),
    path('api/join-team/',      views.create_worker_application, name='api_join_team'),
    path('api/reviews/',        views.create_review,  name='api_create_review'),
    path('api/reviews/list/',   views.get_reviews,    name='api_get_reviews'),
    path('api/chat/',           views.chatbot_reply,  name='api_chat'),
    path('api/photos/',         views.get_photos,     name='api_photos'),
    path('api/admin/stats/',    views.admin_stats,    name='api_admin_stats'),
    path('api/track/',          views.track_visit,    name='api_track'),
]
