from apps.admin_newstockholder.models import StockHolder
from django import forms


class AccountForm(forms.ModelForm):
    class Meta:
        model = StockHolder
        fields = ('sh_shares','mobile_no','sh_fname','sh_lname', 'sh_mname', 'sh_email','sh_position','company_images','sh_proxy_fname','sh_proxy_lname','sh_proxy_mname','sh_proxy_email', 'sh_proxy_status', 'sh_classification')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sh_shares'].widget.attrs.update({'class': 'form-control'})
        self.fields['mobile_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_fname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_lname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_mname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_position'].widget.attrs.update({'class': 'form-control'})
        self.fields['company_images'].widget.attrs.update({'class': 'col-4 border-0'})
        self.fields['sh_proxy_fname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_proxy_lname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_proxy_mname'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_proxy_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_proxy_status'].widget = forms.CheckboxInput()
        self.fields['sh_classification'].widget = forms.CheckboxInput()