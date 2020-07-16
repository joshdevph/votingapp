from django.shortcuts import render, redirect
from django.db.models import Q, Sum
import datetime, uuid
from django.utils.crypto import get_random_string
from .forms import SelectElection, EBallotForm, VotersForm
from .models import EBallot, EBallotBatch, EBallotNum, StockholderVote
from apps.admin_votemaster.models import Attendance, Election, Nominee
from apps.admin_newstockholder.models import StockHolder

# Create your views here.
def select_election(request):
    #Select all election create
    election_code_list = Election.objects.all()
    election_code_list = election_code_list.filter(status = 'pending')
   
    #Fetch all stakeholders present as voters
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_status = 0, at_status = 'present')

    form = SelectElection()

    return render(request, 'admin/content/admin_select_election.html', {'form' : form, 'election_code_list' : election_code_list, 'voters_list' : voters_list})


def create_eballot(request):

    #Request data from modal
    election_code = request.POST['code'] 
  
    #Filter voters list by election code
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_code = election_code, election_status = 0, at_status = 'present')
    
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

        EBallot.objects.create(election_code = name.election_code,                              
                                eballot_num = eballot_num_entry,    
                                eballot_batch_id = eballot_batch_id_entry, 
                                sh_id = name.sh_id,
                                sh_fullname = name.sh_fullname,
                                vote_allocated = name.sh_shares,
                                remain_vote = name.sh_shares            
                                )
        Attendance.objects.filter(election_code = name.election_code).update(election_status = 1)
        Election.objects.filter(code = name.election_code).update(status = 'active')

    return redirect('eballot_list')

def eballot_list(request):
    #Fetch all eballot form to list
    eballot = EBallot.objects.all()

    return render(request, 'admin/content/admin_eballot_list.html', {'eballot' : eballot})

def eballot_form(request, id):
    eballot = EBallot.objects.all()
    eballot = eballot.filter(eballot_num_id = int(id))
    eballot_data = EBallot.objects.get(eballot_num_id = int(id))

    election = Election.objects.all()
    election_desc = election.filter(code = eballot_data.election_code).values_list('description', flat=True)[0]

    nominee = Nominee.objects.all()
    nominee = nominee.filter(election_code = eballot_data.election_code)

    stockholdervote = StockholderVote.objects.all()
    stockholdervote = stockholdervote.filter(election_code = eballot_data.election_code, eballot_num = eballot_data.eballot_num)

    form = VotersForm()

    return render(request, 'eballot_form/content/form.html', {
        'form' : form, 
        'nominee' : nominee, 
        'eballot_data' : eballot_data,
        'election_desc' : election_desc,
        'stockholdervote' : stockholdervote,
        'count' : {
            'nominee_count' : nominee.count(),
            'stockholdervote_count' : stockholdervote.count()
        }
        })


def cast_vote(request, id):
    
    vote_pts = request.POST.get('vote_pts')

    eballot = EBallot.objects.all() # select Eballot model
    eballot = eballot.filter(eballot_num_id = int(id)) # filter eballot_num in Eballot model
    eballot_data = EBallot.objects.get(eballot_num_id = int(id)) # get objects inside Eballot
    
    remain_vote = eballot_data.remain_vote #Fetch remaing vote allocation
    remain_vote = int(remain_vote) - int(vote_pts)
    EBallot.objects.filter(eballot_num_id = int(id)).update(remain_vote = remain_vote)

    # select StockholderVote model
    stockholder_vote = StockholderVote.objects.all()
   
    if request.method == 'POST': # check for post
        StockholderVote.objects.create(
            election_code = request.POST.get('election_code'),
            eballot_num = request.POST.get('eballot_num'),
            sh_fullname = request.POST.get('sh_fullname'),
            sh_id = request.POST.get('sh_id'),
            vote_pts = request.POST.get('vote_pts')
        )
            
    return redirect('eballot_form', id=eballot_data.eballot_num_id) # redirect to same page with id as param

def cast_remove(request, id, sh_id):
    eballot = EBallot.objects.all()
    eballot = EBallot.objects.filter(sh_id_id = sh_id)

    eballot_data = EBallot.objects.get(sh_id_id = sh_id)
    StockholderVote.objects.filter(id=id).delete()

    return redirect('eballot_form', id=eballot_data.eballot_num_id)

def result(request):
    election = Election.objects.all()
    election = election.filter(status = 'Active')
    election_data = Election.objects.get(status = 'Active')

    result = StockholderVote.objects.all()
    result = result.filter(election_code = election_data.code).order_by('sh_fullname').annotate(votes_pts=Sum('vote_pts'))
    
    return render(request, 'admin/content/admin_result.html', { 'result' : result })

def update_elected(request, id):
    election = Election.objects.all()
    election = election.filter(status = 'Active')
    election_data = Election.objects.get(status = 'Active')

    nominee = Nominee.objects.all()
    nominee = nominee.filter(sh_fullname = id)
    nominee_data = nominee.get(sh_fullname = id)

    stockholder = StockHolder.objects.all()
    stockholder = stockholder.filter(id = nominee_data.sh_id).update(sh_position = 'Board of Director')

    result = StockholderVote.objects.all()
    result = result.filter(election_code = election_data.code).order_by('sh_fullname').annotate(votes_pts=Sum('vote_pts'))
    
    return render(request, 'admin/content/admin_result.html', { 'result' : result })