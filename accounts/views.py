from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import generic

from StorageLibrary.settings import LOGIN_URL
from accounts import mixins
from . import forms
from .models import Profile


class DashboardView(mixins.LoginRequiredMixin, mixins.NavbarMixin, generic.TemplateView):
    template_name = 'accounts/dashboard.html'


class AdministratorDashboardView(mixins.SuperuserRequiredMixin, mixins.NavbarMixin, generic.ListView):
    model = Profile
    template_name = 'accounts/administrator.html'
    tab_name = 'administrator'


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('accounts:administrator'))


class LogoutView(generic.RedirectView):
    pattern_name = LOGIN_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class CreateProfileView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Profile
    form_class = forms.CreateProfileForm
    success_url = reverse_lazy('accounts:administrator')


class UpdateProfileView(mixins.SameUserRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = forms.UpdateProfileForm
    template_name = 'accounts/profile_update_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:detail', kwargs={'pk': self.object.pk})


class UpdatePasswordView(mixins.SameUserRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = forms.PasswordUpdateForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(UpdatePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:detail', kwargs={'pk': self.request.user.pk})


class DetailProfileView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Profile


class DeleteProfileView(mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Profile
    success_url = reverse_lazy('accounts:administrator')


class PasswordResetView(mixins.SameUserRequiredMixin, auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:reset-done-password')


class PasswordResetDoneView(mixins.SameUserRequiredMixin, auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(mixins.SameUserRequiredMixin, auth_views.PasswordResetConfirmView):
    # template_name = 'accounts/password_reset_confirm.html'
    pass


class PasswordResetCompleteView(mixins.SameUserRequiredMixin, auth_views.PasswordResetCompleteView):
    # template_name = 'accounts/password_reset_complete.html'
    pass


class ChangeActiveUsersView(mixins.SuperuserRequiredMixin, generic.FormView):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk', None)
        if pk:
            user = Profile.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            if request.is_ajax():
                return JsonResponse({'active': user.is_active, 'pk': user.pk})
        return HttpResponseRedirect('/')
