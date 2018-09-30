from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic

from accounts.models import Profile
from StorageLibrary.settings import DASHBOARD_URL


class AnonymousRequiredMixin(View):
    """Verify if the user is not logged, otherwise redirect to dashboard view"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super(AnonymousRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy(DASHBOARD_URL))


class SuperuserRequiredMixin(LoginRequiredMixin, View):
    """Verify if the user is superuser, otherwise launch permission denied exception."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class SameUserRequiredMixin(LoginRequiredMixin, View):
    """Verify if the user is superuser or the pk belong to the logged user. Otherwise launch permission denied
    exception."""

    def dispatch(self, request, *args, **kwargs):
        logged_user = Profile.objects.get(id=kwargs['pk'])
        if request.user.is_superuser or request.user == logged_user:
            return super(SameUserRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class NavbarMixin:
    tab_name = 'init'

    def get_tab_name(self):
        if self.tab_name:
            return self.tab_name
        else:
            return 'init'

    def get_context_data(self, **kwargs):
        context = {'tab': self.get_tab_name()}
        return context


class AjaxableResponseMixin(generic.FormView):
    """Verify if the request is a ajax request and return the answer in json format"""

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
