from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from accounts import views as acc_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
    path('register/',acc_views.register,name='register'),
    path('profile/',acc_views.profile,name='profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('account_activation_sent/',acc_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', acc_views.activate, name='activate'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('settings/', acc_views.settings, name='settings'),
    path('password/settings/', acc_views.password, name='password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
