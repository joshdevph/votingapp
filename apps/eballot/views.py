from django.shortcuts import render
import datetime, uuid
from django.utils.crypto import get_random_string
from .forms import SelectElection
from .models import EBallot, EBallotBatch, EBallotNum
from apps.admin_votemaster.models import Attendance, Election

# Create your views here.
def select_election(request):
    voters_list = Attendance.objects.all()

    election_code_list = Election.objects.all()
    form = SelectElection()

    return render(request, 'admin/content/admin_select_election.html', {'form' : form, 'election_code_list' : election_code_list, 'voters_list' : voters_list})


def create_eballot(request):

    #Request data from modal
    election_code = request.POST['code'] 
    sh_id = request.POST['sh_id']
    
    #Filter Voters List by Election Code
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_code = election_code)
    
    #Create Eballot Batch ID
    dt = datetime.datetime.now()
    eballot_batch_id = "BOD-" + dt.strftime("%Y%m%d") + get_random_string(length=6)
    batch_id = EBallotBatch.objects.create(eballot_batch_id = eballot_batch_id)

    #Get Newly Created Batch ID
    eballot_batch_id_entry = EBallotBatch.objects.get(eballot_batch_id = eballot_batch_id)
    
    #Loop thru Attendance: Insert Data To EBallot Form
    for name in voters_list:
        #Generate EBallot Number
        eballot_num = uuid.uuid4().hex[:8].upper()
        eballot_num = EBallotNum.objects.create(eballot_num = eballot_num)

        eballot_num_entry = EBallotNum.objects.get(eballot_num = eballot_num)
        sh_id_entry = Attendance.objects.get(sh_id = name.sh_id)

        EBallot.objects.create(election_code = name.election_code,                              
                                eballot_num = eballot_num_entry,    
                                eballot_batch_id = eballot_batch_id_entry,
                                sh_id = sh_id_entry                  
                                )

    return render(request, 'admin/content/admin_dashboard.html')
    

