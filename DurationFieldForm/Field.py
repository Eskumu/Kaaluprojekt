from datetime import timedelta
from django.forms import MultiWidget, MultiValueField, IntegerField
from django.forms.widgets import Input

'''
This is my try to implement proper form to Duration field. 
Meant to be used with django crispy forms.
App is based on http://www.columbia.edu/~njn2118/journal/2015/10/30.html example. 

To make it work copy  'Templates/numberDiv.html' to 
'VirtualenvName/Lib/site-packages/django/forms/templates/django/forms/widgets' in your python virtualenv'
'''


class NumberInputInline(Input):
    input_type = 'number'
    template_name = 'django/forms/widgets/numberDiv.html'

    def __init__(self, attrs=None, group_addon=None, div_id=None, div_class=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        self.group_addon = group_addon
        self.div_id = div_id
        self.div_class = div_class
        super(Input, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super(Input, self).get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        if self.group_addon is not None:
            context['widget']['group_addon'] = self.group_addon
        if self.div_id is not None:
            context['widget']['id'] = self.div_id
        if self.div_class is not None:
            context['widget']['class'] = self.div_class
        return context


class SplitDurationWidget(MultiWidget):

    def __init__(self, attrs=None):
        widgets = (NumberInputInline(attrs=attrs, group_addon="H:", div_id='Hour', div_class='col-xs-6'),
                   NumberInputInline(attrs=attrs, group_addon="Min", div_id='Minute', div_class='col-xs-6'))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                return [int(hours), int(minutes)]
        return [0, 0]


class MultiValueDurationField(MultiValueField):
    widget = SplitDurationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            IntegerField(),
            IntegerField(),
        )
        super(MultiValueDurationField, self).__init__(
            fields=fields,
            require_all_fields=True,
            *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 2:
            return timedelta(
                hours=int(data_list[0]),
                minutes=int(data_list[1]),
                )
        else:
            return timedelta(0)
