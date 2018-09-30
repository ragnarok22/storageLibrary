from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import forms as auth_forms

from accounts import mixins
from StorageLibrary.settings import LOGIN_URL
from . import forms
from .models import Profile


class DashboardView(mixins.LoginRequiredMixin, mixins.NavbarMixin, generic.TemplateView):
    template_name = 'accounts/dashboard.html'


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('accounts:dashboard'))


class LogoutView(generic.RedirectView):
    pattern_name = LOGIN_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class CreateProfileView(generic.CreateView):
    model = Profile
    form_class = forms.CreateProfileForm
    success_url = reverse_lazy('accounts:dashboard')


class UpdateProfileView(generic.UpdateView):
    model = Profile
    form_class = forms.UpdateProfileForm

    def get_success_url(self):
        return reverse_lazy('accounts:detail', kwargs={'pk': self.object.pk})


class UpdatePasswordView(mixins.SameUserRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = auth_forms.PasswordChangeForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(UpdatePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:detail', kwargs={'pk': self.request.user.pk})


class ListProfileView(generic.ListView):
    model = Profile
    template_name = 'accounts/profile_list.html'
    context_object_name = 'profiles'


class DetailProfileView(generic.DetailView):
    model = Profile


class DeleteProfileView(generic.DeleteView):
    model = Profile
    success_url = reverse_lazy('accounts:list')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:reset-done-password')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    # template_name = 'accounts/password_reset_confirm.html'
    pass


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    # template_name = 'accounts/password_reset_complete.html'
    pass
