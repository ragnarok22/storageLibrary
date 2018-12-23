from django.http import JsonResponse
from django.views import generic


class AjaxableListMixin(generic.ListView):
    def get(self, request, *args, **kwargs):
        response = super(AjaxableListMixin, self).get(request, *args, **kwargs)
        if request.is_ajax():
            objects = []
            all_objects = self.object_list
            for o in all_objects:
                objects.append(o.to_dict())
            data = {
                self.get_context_object_name(self.object_list): objects
            }
            return JsonResponse(data)
        return response


class AjaxableDetailMixin(generic.DetailView):
    def get(self, request, *args, **kwargs):
        response = super(AjaxableDetailMixin, self).get(request, *args, **kwargs)
        if request.is_ajax():
            data = self.object.to_dict()
            if self.extra_context:
                data.update(self.extra_context)
            return JsonResponse(data)
        return response


class AjaxablePostMixin(generic.FormView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {'status': 'success'}
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class AjaxableDeleteMixin(generic.DeleteView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            data = {'status': 'success', 'message': 'Ha sido eliminado exitosamente'}
            return JsonResponse(data)
        else:
            return response
