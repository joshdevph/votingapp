from django.shortcuts import render, redirect
import datetime, uuid
from django.utils.crypto import get_random_string
from .forms import SelectElection, EBallotForm
from .models import EBallot, EBallotBatch, EBallotNum, StockholderVote
from apps.admin_votemaster.models import Attendance, Election, Nominee
from apps.admin_newstockholder.models import StockHolder

# Create your views here.
def select_election(request):
    #Fetch all stakeholders present as voters
    voters_list = Attendance.objects.all()

    #Select all election create
    election_code_list = Election.objects.all()
    form = SelectElection()

    return render(request, 'admin/content/admin_select_election.html', {'form' : form, 'election_code_list' : election_code_list, 'voters_list' : voters_list})


def create_eballot(request):

    #Request data from modal
    election_code = request.POST['code'] 
    sh_id = request.POST['sh_id']
  
    #Filter voters list by election code
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_code = election_code)
    
    #Create eballot batch id
    dt = datetime.datetime.now()
    eballot_batch_id = dt.strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6].upper()
    batch_id = EBallotBatch.objects.create(eballot_batch_id = eballot_batch_id)

    #Get newly created batch id
    eballot_batch_id_entry = EBallotBatch.objects.get(eballot_batch_id = eballot_batch_id)
    
    #Loop thru attendance: insert data to eballot form
    for name in voters_list:
        #Generate eballot number
        eballot_num = uuid.uuid4().hex[:8].upper()
        eballot_num = EBallotNum.objects.create(eballot_num = eballot_num)

        eballot_num_entry = EBallotNum.objects.get(eballot_num = eballot_num)
        sh_id_entry = Attendance.objects.get(sh_id = name.sh_id)

        EBallot.objects.create(election_code = name.election_code,                              
                                eballot_num = eballot_num_entry,    
                                eballot_batch_id = eballot_batch_id_entry, 
                                sh_id = sh_id_entry,
                                sh_fullname = name.sh_fullname                  
                                )

    return render(request, 'admin/content/admin_dashboard.html')

def eballot_list(request):
    #Fetch all eballot form to list
    eballot = EBallot.objects.all()

    return render(request, 'admin/content/admin_eballot_list.html', {'eballot' : eballot})

def eballot_form(request, id):
    #Fetch data from eBallot pass to template
    eballot_form = EBallot.objects.all()
    eballot_form = EBallot.objects.filter(eballot_num_id = int(id))

    #Get election_code field from EBallot model
    code = EBallot.objects.only('election_code').get(eballot_num_id = int(id)).election_code
    sh_id = EBallot.objects.only('sh_id').get(eballot_num_id = int(id)).sh_id

    #Fetch data from Nominee filtered by election code
    nominees = Nominee.objects.all()
    nominees = nominees.filter(election_code = code)


    form = EBallotForm()

    return render(request, 'eballot_form/content/form.html', {'form' : form, 'eballot_form' : eballot_form, 'nominees' : nominees})


def save_vote(request, id):

    return 