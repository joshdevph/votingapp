from django import forms
from .models import EBallot, StockholderVote
from apps.admin_votemaster.models import Election, Attendance

class SelectElection(forms.ModelForm):

    class Meta:
        model = Election
        fields = {'code', 'description'}
        labels = {
            'code' : 'Election Code',
            'description' : 'Election Description'      
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
     

class EBallotForm(forms.ModelForm):
    class Meta:
        model = EBallot
        fields = ('election_code','eballot_batch_id', 'eballot_num', 'sh_fullname')
        labels = {
            'election_code': 'Election Code',
            'eballot_batch_id': 'eBallot Batch ID',
            'eballot_num': 'eBallot No.',
            'sh_fullname': 'Stockholder Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['eballot_batch_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['eballot_num'].widget.attrs.update({'class': 'form-control'})
        self.fields['sh_fullname'].widget.attrs.update({'class': 'form-control'})
        
class VotersForm(forms.ModelForm):
    class Meta:
        model = StockholderVote
        fields = ('vote_pts', )
        vote_pts = forms.IntegerField( 
            widget = forms.NumberInput(attrs={
            'name' : 'vote_pts',
            'class' : 'form-control', 
            'placeholder' : 'Enter vote'    
        })
        )
        
