from django.contrib import admin
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

csrf_protect_m = method_decorator(csrf_protect)

__all__ = ('CloneableModelAdminMixed',)


class CloneableModelAdminMixin(admin.ModelAdmin):
    """Cloneable model mixed.

    A mixed that overrides ``changeform_view`` method for adding a ``save_as``
    button. The button makes a clone with all relationships of instance.

    """
    save_as = True

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(
            self, request, object_id=None, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)

        if request.method == 'POST' and '_saveasnew' in request.POST:
            new_obj = obj.clone()

            return self.response_add(request, new_obj)

        return super().changeform_view(
                request, object_id=object_id, form_url='',
                extra_context=extra_context
            )
