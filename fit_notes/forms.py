from django.forms.models import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Div, Field

from DurationFieldForm.Field import MultiValueDurationField
from .models import event

class EventForm(ModelForm):

    class Meta:
        model = event
        fields = ['activity', 'duration', 'avg_pulse', 'comment', 'event_date']

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        super(EventForm, self).__init__(*args,**kwargs)
        self.fields['duration'] = MultiValueDurationField()

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = "col-sm-6"
        self.helper.field_class = "col-sm-6"
        self.helper.layout = Layout(
            Div(
                'event_date',
                css_class="hidden"),
            'activity',
            Field(
                'duration',
                template='DurationFieldForm/multifield-inline.html'),
            'avg_pulse',
            'comment'
        )
        self.helper.add_input(Submit('submit',"UPDATE"))