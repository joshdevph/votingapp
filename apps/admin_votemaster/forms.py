from django.contrib.auth.models import User
import datetime
from django import forms
from apps.admin_votemaster.models import Election

dt = datetime.datetime.now()
code = "BOD-" + dt.strftime("%Y%m%d")


class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = ('description','code')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control',
             'value': 'Board of Directors Election'})
        self.fields['code'].widget.attrs.update({
            'class': 'form-control',
            'readonly': 'true',
            'value': code
        })
        #
        # self.fields['added_by'].widget.attrs.update({
        #     'class': 'form-control',
        # })

DISPLAY_CHOICES = (
    ("locationbox", "Display Location"),
    ("displaybox", "Display Direction")
)

class AttendanceForm(forms.Form):
    class Meta:
        model = Election
        fields = ('description', 'code')