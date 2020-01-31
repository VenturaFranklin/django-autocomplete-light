try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.forms import formset_factory
from django.views import generic


from select2_foreign_key.forms import TForm
from select2_foreign_key.models import TModel


class UpdateView(generic.UpdateView):
    model = TModel
    form_class = TForm
    template_name = 'clone.html'
    success_url = reverse_lazy('select2_outside_admin')
    formset_class = formset_factory(
        form=TForm,
        extra=1,
    )

    def get_object(self):
        return TModel.objects.first()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        result = super().form_valid(form)
        self.formset.save()
        return result

    @property
    def formset(self):
        if '_formset' not in self.__dict__:
            setattr(self, '_formset', self.formset_class(
                **{"data": self.request.POST if self.request.method == 'POST' else None,
            }))
        return self._formset
