from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import event, Kaal
from .forms import EventForm

class FitView(LoginRequiredMixin, CreateView):
    model = event
    form_class = EventForm
    success_url = reverse_lazy('fit-notes')
    template_name = 'fit_notes/test.html'

    def form_valid(self, form):
        form.instance.user = Kaal.objects.get(user=self.request.user)
        return super(FitView, self).form_valid(form)