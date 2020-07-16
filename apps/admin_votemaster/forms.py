from django.contrib.auth.models import User
import datetime
from django import forms
from apps.admin_votemaster.models import Election

dt = datetime.datetime.now()
code = "BOD-" + dt.strftime("%Y%m%d")

class DateInput(forms.DateInput):
    input_type = 'date'

class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = ('description','code', 'target_date')
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),

            'target_date': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'onchange': 'changeTDate(this.value)'
            })
        }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['description'].widget.attrs.update(
    #         {'class': 'form-control',
    #          'value': 'Board of Directors Election'})
    #     self.fields['code'].widget.attrs.update({
    #         'class': 'form-control',
    #         'readonly': 'true',
    #         'value': code
    #     })
    #
    #     self.fields['target_date'].widget.attrs.update({
    #         'class': 'form-control',
    #         'type': 'date',
    #     })


class AttendanceForm(forms.Form):
    class Meta:
        model = Election
        fields = ('description', 'code')