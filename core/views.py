from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PickupRequestForm, CustomerSignupForm
from .models import PickupRequest, ScrapCategory

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scrap_categories'] = ScrapCategory.objects.all()[:4] # Show top 4
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scrap_categories'] = ScrapCategory.objects.all()
        return context

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

class PickupDeleteView(LoginRequiredMixin, DeleteView):
    model = PickupRequest
    success_url = reverse_lazy('dashboard')
    
    def get_queryset(self):
        # Ensure user can only delete their own pickups
        return PickupRequest.objects.filter(customer=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Pickup request deleted successfully.")
        return super().form_valid(form)

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
        
        if pickup.scrap_category:
            rate = float(pickup.scrap_category.rate_per_kg)
        else:
            rate = 0.0 # Or default rate

        total_amount = actual_weight * rate

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
