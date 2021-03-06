import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.serializers.json import DjangoJSONEncoder

from .models import Kaal, Kaal_uuendus
from .forms import KaalForm
# Create your views here.


class DashboardView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Kaal_uuendus
    form_class = KaalForm
    success_url = reverse_lazy('dashboard')
    success_message = "Kaal uuendatud"

    def form_valid(self, form):
        form.instance.KaalID = Kaal.objects.get(user=self.request.user)
        return super(DashboardView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DashboardView,self).get_context_data(**kwargs)
        context["kaalud"] = Kaal.objects.order_by('user')
        return context


class DetailView(LoginRequiredMixin,ListView):
    model = Kaal_uuendus
    ordering = ("change_date")
    context_object_name = "andmed"
    template_name = "kaaluleht/detail.html"

    def Decimal(self,num):
        return num

    def get_context_data(self, **kwargs):
        context = super(DetailView,self).get_context_data(**kwargs)
        andmed = Kaal_uuendus.objects.filter(KaalID=self.kwargs['pk']).order_by("change_date")

        data_raw = andmed.values_list('kaal', flat=True)
        labels_raw = andmed.values_list('change_date',flat=True)

        data = json.dumps(list(data_raw),cls=DjangoJSONEncoder)
        labels = json.dumps(list(labels_raw),cls=DjangoJSONEncoder)

        chart_padding = 5

        graafik = {
            'labels': labels,
            'data': data,
            'chart_min': min(data_raw) - chart_padding,
            'chart_max': max(data_raw) + chart_padding
        }
        context['graafik'] = graafik
        return context

    def get_queryset(self):
        return Kaal_uuendus.objects.filter(KaalID=self.kwargs['pk']).order_by("change_date")