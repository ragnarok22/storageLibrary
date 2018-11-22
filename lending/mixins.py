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
                'object_list': objects
            }
            return JsonResponse(data)
        return response


class AjaxableDetailMixin(generic.DetailView):
    def get(self, request, *args, **kwargs):
        response = super(AjaxableDetailMixin, self).get(request, *args, **kwargs)
        data = self.object.to_dict()
        if self.extra_context:
            data.update(self.extra_context)
        if request.is_ajax():
            return JsonResponse(data)
        return response
