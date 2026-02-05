from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    HomeView, BookPickupView, CustomerSignupView, CustomLoginView, 
    CustomerDashboardView, RateCardView, AgentDashboardView, AgentJobDetailView,
    AgentAcceptPickupView, AboutView, ServicesView, PickupDeleteView, AgentSignupView, PartnerWithUsView,
    TrackAgentView, AgentRejectPickupView, ReschedulePickupView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('rate-card/', RateCardView.as_view(), name='rate_card'),
    path('book-pickup/', BookPickupView.as_view(), name='book_pickup'),
    path('signup/', CustomerSignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', CustomerDashboardView.as_view(), name='dashboard'), 
    path('track/<int:pk>/', TrackAgentView.as_view(), name='track_agent'),
    path('pickup/reschedule/<int:pk>/', ReschedulePickupView.as_view(), name='reschedule_pickup'),
    
    # Agent Routes
    path('agent/dashboard/', AgentDashboardView.as_view(), name='agent_dashboard'),
    path('agent/accept/<int:pk>/', AgentAcceptPickupView.as_view(), name='agent_accept_pickup'),
    path('agent/reject/<int:pk>/', AgentRejectPickupView.as_view(), name='agent_reject_pickup'),
    path('agent/job/<int:pk>/', AgentJobDetailView.as_view(), name='agent_job_detail'),
    path('dashboard/delete/<int:pk>/', PickupDeleteView.as_view(), name='pickup_delete'),
    path('partner-with-us/', PartnerWithUsView.as_view(), name='partner_with_us'),
    path('agent/signup/', AgentSignupView.as_view(), name='agent_signup'),
]
