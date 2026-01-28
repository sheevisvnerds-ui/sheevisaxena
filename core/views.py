from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView, View, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PickupRequestForm, CustomerSignupForm
from .models import PickupRequest, ScrapCategory, PickupItem

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
        return PickupRequest.objects.filter(agent=self.request.user, status=PickupRequest.Status.ASSIGNED).order_by('scheduled_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        from django.utils import timezone
        today = timezone.now().date()
        
        assigned = PickupRequest.objects.filter(agent=user, status=PickupRequest.Status.ASSIGNED).order_by('scheduled_date')
        
        context['assigned_pickups'] = assigned
        context['today_pickups'] = [p for p in assigned if p.scheduled_date.date() == today]
        context['future_pickups'] = [p for p in assigned if p.scheduled_date.date() > today]
        context['completed_pickups'] = PickupRequest.objects.filter(agent=user, status=PickupRequest.Status.COLLECTED).order_by('-updated_at')
        context['available_pickups'] = PickupRequest.objects.filter(status=PickupRequest.Status.PENDING, agent__isnull=True).order_by('scheduled_date')
        return context

class AgentJobDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pickup = get_object_or_404(PickupRequest, pk=pk, agent=request.user)
        categories = ScrapCategory.objects.all()
        return render(request, 'core/agent_job_detail.html', {
            'pickup': pickup,
            'categories': categories
        })

    def post(self, request, pk):
        pickup = get_object_or_404(PickupRequest, pk=pk, agent=request.user)
        
        category_ids = request.POST.getlist('category[]')
        weights = request.POST.getlist('weight[]')
        
        total_weight = 0.0
        total_amount = 0.0
        
        # Clear existing items if re-submitting (optional safety)
        pickup.items.all().delete()
        
        for cat_id, weight_str in zip(category_ids, weights):
            if not weight_str or float(weight_str) <= 0:
                continue
                
            weight = float(weight_str)
            category = ScrapCategory.objects.get(id=cat_id)
            amount = weight * float(category.rate_per_kg)
            
            PickupItem.objects.create(
                pickup=pickup,
                category=category,
                weight=weight,
                amount=amount
            )
            
            total_weight += weight
            total_amount += amount

        pickup.actual_weight = total_weight
        pickup.total_amount = total_amount
        pickup.status = PickupRequest.Status.COLLECTED
        pickup.save()
        
        messages.success(request, f"Job Completed! Amount to Pay: ₹{total_amount:.2f}")
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
