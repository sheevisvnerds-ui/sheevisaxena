from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    HomeView, BookPickupView, CustomerSignupView, CustomLoginView, 
    CustomerDashboardView, RateCardView, AgentDashboardView, AgentJobDetailView,
    AboutView, ServicesView, PickupDeleteView
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
    
    # Agent Routes
    path('agent/dashboard/', AgentDashboardView.as_view(), name='agent_dashboard'),
    path('agent/job/<int:pk>/', AgentJobDetailView.as_view(), name='agent_job_detail'),
    path('dashboard/delete/<int:pk>/', PickupDeleteView.as_view(), name='pickup_delete'),
]
