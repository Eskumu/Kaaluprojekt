from django.forms.models import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Kaal_uuendus

class KaalForm(ModelForm):

    class Meta:
        model = Kaal_uuendus
        fields = ['kaal','change_date']

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = "col-sm-6"
        self.helper.field_class = "col-sm-6"

        self.helper.add_input(Submit('submit',"UPDATE"))