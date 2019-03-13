from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.AdministratorDashboardView.as_view(), name='administrator'),
    path('change/status/user/', views.ChangeActiveUsersView.as_view(), name='change_active_users'),

    path('profile/create/', views.CreateProfileView.as_view(), name='create'),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update'),
    path('profile/<int:pk>/update/password/', views.UpdatePasswordView.as_view(), name='update-password'),
    path('profile/reset/password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('profile/reset/password/done/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('profile/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/reset/complete/', views.PasswordResetConfirmView.as_view(), name='password-reset-complete'),
    path('profile/<int:pk>/detail/', views.DetailProfileView.as_view(), name='detail'),
    path('profile/<int:pk>/delete/', views.DeleteProfileView.as_view(), name='delete'),
]
