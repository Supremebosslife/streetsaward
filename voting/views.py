from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic import TemplateView
from django.views.generic.list import ListView 
from django.views import View
from django.db.models import F, Sum
from .models import Nominee
from operator import itemgetter
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Nominee, Category, Vote
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordResetForm


class HomePageView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        for category in categories:
            print(category.slug)
        context['categories'] = categories
        return context

class CustomUserCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('registration_success')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        # Manually trigger form validation
        form.is_valid()

        # Check if the email already exists
        if get_user_model().objects.filter(email=email).exists():
            messages.error(self.request, 'Email address already exists. Please choose a different email address.')
            return self.render_to_response(self.get_context_data(form=form))

        user = form.save()

        # Authenticate the user after registration
        authenticated_user = authenticate(
            request=self.request,
            username=email,
            password=form.cleaned_data['password1'],
            backend='voting.backends.EmailBackend'
        )

        if authenticated_user is not None:
            login(self.request, authenticated_user)
            print(f"User {user.email} logged in after registration.")
            print(f"Is Authenticated: {self.request.user.is_authenticated}")
            print(f"User Attributes: {user.__dict__}")
        else:
            print("Authentication failed after registration.")

        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/custom_login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')

class RegistrationSuccessView(TemplateView):
    template_name = 'registration/registration_success.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

def check_vote_status(request):
    user = request.user  # Assuming you have authentication middleware enabled
    category_slug = request.GET.get('category_slug')  # Assuming you pass category_slug in the request
    nominee_slug = request.GET.get('nominee_slug')  # Assuming you pass nominee_slug in the request

    # Fetch the category and nominee IDs based on the provided slugs
    category_id = Category.objects.get(slug=category_slug).id
    nominee_id = Nominee.objects.get(slug=nominee_slug).id

    # Check if the user has voted for the given nominee in the specified category
    user_has_voted = Vote.objects.filter(user=user, nominee_id=nominee_id, category_id=category_id).exists()


class CongratulationsView(View, LoginRequiredMixin):
    template_name = 'congratulations.html'
    already_voted_template = 'already_voted.html'

    def get(self, request, *args, **kwargs):
        selected_nominee = request.GET.get('selected_nominee', '')

        # Check if the selected nominee is valid
        nominee = get_object_or_404(Nominee, nominee_name=selected_nominee)

        # Check if the user has already voted in this category
        if Vote.objects.filter(user=request.user, nominee__category=nominee.category).exists():
            return render(request, self.already_voted_template)

        try:
            # Create a Vote object for the user and selected nominee
            vote = Vote.objects.create(user=request.user, nominee=nominee)

            # Increase the vote count for the selected nominee
            nominee.votes += 1
            nominee.save()

            return render(request, self.template_name, {'nominee': nominee})

        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                # User has already voted in this category
                return render(request, self.already_voted_template)

            # Handle other IntegrityError cases
            return JsonResponse({'error': 'An error occurred.'}, status=400)

class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/custom_password_reset_email.html'  # Custom email template

    def form_valid(self, form):
        # Override this method to customize form submission behavior if needed
        # For example, you can log form submissions or perform additional validation
        return super().form_valid(form)

def custom_password_reset_done(request):
    # You can customize this view if needed
    return render(request, 'registration/custom_password_reset_done.html')

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'
    login_url = '/custom-login/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RecentVotesView(LoginRequiredMixin, View):
    template_name = 'recent_votes.html'

    def get(self, request, *args, **kwargs):
        # Get the user's recent votes
        recent_votes = Vote.objects.filter(user=request.user).select_related('nominee__category')

        context = {
            'recent_votes': recent_votes,
        }

        return render(request, self.template_name, context)

class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'registration/delete_account.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:  
            
            request.user.delete()
            
            # Logout the user after deletion
            logout(request)

            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('home')
        else:
            return redirect('login')

class ResultCategoryView(View):
    template_name = 'voting_resultpage.html'

    def get(self, request, slug, *args, **kwargs):
        # Retrieve category based on the slug
        category = get_object_or_404(Category, slug=slug)

        # Retrieve results for the category
        total_votes = Nominee.objects.filter(category=category).annotate(total_votes=Sum('votes')).order_by('-total_votes')

        # Pass category and results to the template in the context
        return render(request, self.template_name, {'category': category, 'total_votes': total_votes})

class NomineeListView(View):
    template_name = 'nominee_list.html'

    def get(self, request, category_id, *args, **kwargs):
        category = Category.objects.get(id=category_id)
        nominees = Nominee.objects.filter(category=category)
        return render(request, self.template_name, {'nominees': nominees, 'category': category})

class CategoryVoteView(LoginRequiredMixin, View):
    template_name = 'category_vote.html'
    result_url = reverse_lazy('select_category')  # Adjust the URL to your actual result page

    def get(self, request, category_slug, *args, **kwargs):
        # Retrieve category based on the slug
        category = get_object_or_404(Category, slug=category_slug)

        nominees = Nominee.objects.filter(category=category)

        # User hasn't voted, render the regular template
        return render(request, self.template_name, {'category': category, 'nominees': nominees})

def about_us(request):
    return render(request, 'about_us/about_us.html')

def privacy_policy(request):
    return render(request, 'about_us/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'about_us/terms_and_conditions.html')

def accessibility_policy(request):
    return render(request, 'about_us/accessibility_policy.html')

def security_policy(request):
    return render(request, 'about_us/security_policy.html')

def dmca_policy(request):
    return render(request, 'about_us/dmca_policy.html')

def user_agreement(request):
    return render(request, 'about_us/user_agreement.html')

def community_guidelines(request):
    return render(request, 'about_us/community_guidelines.html')

def cookie_policy(request):
    return render(request, 'about_us/cookie_policy.html')

def about_streetsaward(request):
    return render(request, 'about_us/about_streetsaward.html')