from django.urls import path, include
from .views import HomePageView
from django.contrib.auth import views as auth_views
from .views import CustomUserCreationView, ResultCategoryView, RegistrationSuccessView, CustomLogoutView, CategoryVoteView, ResultCategoryView, CustomLoginView, CategoryListView, CongratulationsView, DeleteAccountView, UserProfileView, RecentVotesView, check_vote_status, CustomPasswordResetView, custom_password_reset_done
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import (
    about_us,
    about_streetsaward,
    privacy_policy,
    terms_and_conditions,
    accessibility_policy,
    security_policy,
    dmca_policy,
    user_agreement, 
    community_guidelines, 
    cookie_policy,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', CustomUserCreationView.as_view(), name='signup'),
    path('custom-login/', CustomLoginView.as_view(), name='custom-login'),
    path('custom-logout/', CustomLogoutView.as_view(), name='custom-logout'),
    path('congratulations/', CongratulationsView.as_view(), name='congratulations'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('recent-votes/', RecentVotesView.as_view(), name='recent_votes'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('voting_resultpage/<slug:slug>/', ResultCategoryView.as_view(), name='voting_resultpage'),
    path('select_category/', CategoryListView.as_view(), name='select_category'),
    path('category_vote/<slug:category_slug>/', CategoryVoteView.as_view(), name='category_vote'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('check_vote_status/', check_vote_status, name='check_vote_status'),
    path('registration_success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('about_us/', about_us, name='about_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('about_streetsaward/', privacy_policy, name='about_streetsaward'),
    path('terms-and-conditions/', terms_and_conditions, name='terms_and_conditions'),
    path('accessibility-policy/', accessibility_policy, name='accessibility_policy'),
    path('security-policy/', security_policy, name='security_policy'),
    path('dmca-policy/', dmca_policy, name='dmca_policy'),
    path('user_agreement/', user_agreement, name='user_agreement'),
    path('community_guidelines/', community_guidelines, name='community_guidelines'),
    path('cookie_policy/', cookie_policy, name='cookie_policy'),
]