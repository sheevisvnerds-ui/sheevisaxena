from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PickupRequestForm, CustomerSignupForm
from .models import PickupRequest, ScrapCategory

class HomeView(TemplateView):
    template_name = 'core/home.html'

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ServicesView(TemplateView):
    template_name = 'core/services.html'

class RateCardView(ListView):
    model = ScrapCategory
    template_name = 'core/rate_card.html'
    context_object_name = 'categories'

class BookPickupView(LoginRequiredMixin, CreateView):
    model = PickupRequest
    form_class = PickupRequestForm
    template_name = 'core/pickup_form.html'
    success_url = reverse_lazy('dashboard') # We need to create this

    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, "Pickup scheduled successfully!")
        return super().form_valid(form)

class CustomerDashboardView(LoginRequiredMixin, ListView):
    model = PickupRequest
    template_name = 'core/dashboard.html'
    context_object_name = 'pickups'

    def get_queryset(self):
        return PickupRequest.objects.filter(customer=self.request.user).order_by('-created_at')

class AgentDashboardView(LoginRequiredMixin, ListView):
    model = PickupRequest
    template_name = 'core/agent_dashboard.html'
    context_object_name = 'pickups'

    def get_queryset(self):
        # In a real app, filter by role=AGENT check too
        return PickupRequest.objects.filter(agent=self.request.user, status=PickupRequest.Status.ASSIGNED).order_by('scheduled_date')

class AgentJobDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pickup = get_object_or_404(PickupRequest, pk=pk, agent=request.user)
        return render(request, 'core/agent_job_detail.html', {'pickup': pickup})

    def post(self, request, pk):
        pickup = get_object_or_404(PickupRequest, pk=pk, agent=request.user)
        actual_weight = float(request.POST.get('actual_weight', 0))
        
        # Simplified Pricing Logic: Avg rate 15/kg for MVP as we don't have category split in form yet
        # future: logic to split weight by category
        AVG_RATE = 15.0 
        total_amount = actual_weight * AVG_RATE

        pickup.actual_weight = actual_weight
        pickup.total_amount = total_amount
        pickup.status = PickupRequest.Status.COLLECTED
        pickup.save()
        
        messages.success(request, f"Job Completed! Amount to Pay: ₹{total_amount}")
        return redirect('agent_dashboard')

class CustomerSignupView(CreateView):
    form_class = CustomerSignupForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Account created! Please login.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
