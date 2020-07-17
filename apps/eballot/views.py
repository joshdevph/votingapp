from django.shortcuts import render, redirect
from django.db.models import Q, Sum
import datetime, uuid
from django.utils.crypto import get_random_string
from .forms import SelectElection, EBallotForm, VotersForm
from .models import EBallot, EBallotBatch, EBallotNum, StockholderVote
from apps.admin_votemaster.models import Attendance, Election, Nominee
from apps.admin_newstockholder.models import StockHolder
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required(login_url="/")
def select_election(request):
    #Select all election create
    election_code_list = Election.objects.all()
    election_code_list = election_code_list.filter(status = 'pending')
   
    #Fetch all stakeholders present as voters
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_status = 0, at_status = 'present')

    form = SelectElection()

    return render(request, 'admin/content/admin_select_election.html', {'form' : form, 'election_code_list' : election_code_list, 'voters_list' : voters_list})

@login_required(login_url="/")
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
        #Sending Email
        subject = 'User Access'
        message = 'http://127.0.0.1:8000/eballot/eballot_list/eballot_form/'+str(eballot_num_entry.id)
        email_from = settings.EMAIL_HOST_USER
        recipient_list =[name.sh_email]
        send_mail( subject, message, email_from, recipient_list )

        EBallot.objects.create(election_code = name.election_code,                              
                                eballot_num = eballot_num_entry,    
                                eballot_batch_id = eballot_batch_id_entry, 
                                sh_id = name.sh_id,
                                sh_fullname = name.sh_fullname,
                                vote_allocated = name.sh_shares,
                                remain_vote = name.sh_shares,
                                sh_classification = name.sh_classification            
                                )
        Attendance.objects.filter(election_code = name.election_code).update(election_status = 1)
        Election.objects.filter(code = name.election_code).update(status = 'active')

    return redirect('eballot_list')

def eballot_list(request):
    #Fetch all eballot form to list
    eballot = EBallot.objects.all()
    eballot = eballot.filter(election_status = 0)

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
    total_vote_cast = stockholdervote.aggregate(total_cast = Sum('vote_pts'))
    total_vote_cast = total_vote_cast['total_cast']

    form = VotersForm()

    return render(request, 'eballot_form/content/form.html', {
        'form' : form, 
        'nominee' : nominee, 
        'eballot_data' : eballot_data,
        'election_desc' : election_desc,
        'total_vote_cast' :total_vote_cast,
        'stockholdervote' : stockholdervote,
        'count' : {
            'nominee_count' : nominee.count(),
            'stockholdervote_count' : stockholdervote.count()
        }
        })


@login_required(login_url="/")
def cast_vote(request, id):
    
    vote_pts = request.POST.get('vote_pts')

    vote_code = uuid.uuid4().hex[:16].upper() # generate unique identifier for every casting vote

    eballot = EBallot.objects.all() # select Eballot model
    eballot = eballot.filter(eballot_num_id = int(id)) # filter eballot_num in Eballot model
    eballot_data = EBallot.objects.get(eballot_num_id = int(id)) # get objects inside Eballot

    # select StockholderVote model
    stockholder_vote = StockholderVote.objects.all()
    check_record = stockholder_vote.filter(sh_fullname = request.POST.get('sh_fullname'),
        eballot_num = eballot_data.eballot_num).count()
   
    if request.method == 'POST': # check for post 
        if check_record == 0:
            StockholderVote.objects.create(
                election_code = request.POST.get('election_code'),
                eballot_num = request.POST.get('eballot_num'),
                sh_fullname = request.POST.get('sh_fullname'),
                sh_id = request.POST.get('sh_id'),
                vote_pts = request.POST.get('vote_pts'),
                vote_code = vote_code
            )

            remain_vote = eballot_data.remain_vote #Fetch remaing vote allocation
            remain_vote = int(remain_vote) - int(vote_pts)
            if remain_vote < 0:
                remain_vote = 0
            EBallot.objects.filter(eballot_num_id = int(id)).update(remain_vote = remain_vote)
            
    return redirect('eballot_form', id=eballot_data.eballot_num_id) # redirect to same page with id as param

@login_required(login_url="/")
def cast_remove(request, id, sh_id):
    eballot = EBallot.objects.all()
    eballot = EBallot.objects.filter(sh_id = sh_id)
    eballot_data = EBallot.objects.get(sh_id = sh_id)

    stockholdervote = StockholderVote.objects.all()
    stockholdervote = StockholderVote.objects.get(id=id)

    shv_vote_pts = stockholdervote.vote_pts
    eballot_vote_pts = eballot_data.remain_vote

    total_vote = shv_vote_pts + int(eballot_vote_pts)
    eballot.update(remain_vote = total_vote)
    
    StockholderVote.objects.filter(id=id).delete()

    return redirect('eballot_form', id=eballot_data.eballot_num_id)

@login_required(login_url="/")
def result(request):
    election = Election.objects.all()
    if election.filter(status = 'active'):
        election = election.filter(status = 'active')
        election_data = Election.objects.get(status = 'active')

        result = StockholderVote.objects.all()
        result = result.filter(election_code = election_data.code).values('election_code', 'sh_fullname').annotate(total_vote=Sum('vote_pts')).order_by('-total_vote')
    
        return render(request, 'admin/content/admin_result.html', { 'result' : result , 'election_data' : election_data})
    else:
        return render(request, 'admin/content/admin_result.html')


@login_required(login_url="/")
def update_elected(request, id):
    election = Election.objects.all()
    election = election.filter(status = 'active')
    election_data = Election.objects.get(status = 'active')

    nominee = Nominee.objects.all()
    nominee = nominee.filter(sh_fullname = id)
    nominee_data = nominee.get(sh_fullname = id)

    stockholder = StockHolder.objects.all()
    stockholder = stockholder.filter(id = nominee_data.sh_id).update(sh_position = 'Board of Director')

    result = StockholderVote.objects.all()
    result = result.filter(election_code = election_data.code).order_by('sh_fullname').annotate(votes_pts=Sum('vote_pts'))
    StockholderVote.filter()
    
    return render(request, 'admin/content/admin_result.html', { 'result' : result })

@login_required(login_url="/")
def vote_summary(request, id):
    eballot_num = EBallotNum.objects.all()
    eballot_num = eballot_num.filter(eballot_num = id)
    eballot_num_data = eballot_num.get(eballot_num = id)

    eballot = EBallot.objects.all()
    eballot = eballot.filter(eballot_num_id = eballot_num_data.id)
    eballot_data = eballot.get(eballot_num_id = eballot_num_data.id)

    vote_allocated = eballot_data.vote_allocated

    stockholdervote = StockholderVote.objects.all()
    stockholdervote = stockholdervote.filter(eballot_num = eballot_num_data.eballot_num)
    total_vote_cast = stockholdervote.aggregate(total_cast = Sum('vote_pts'))
    total_vote_cast = total_vote_cast['total_cast']

    if total_vote_cast > int(vote_allocated):
        eballot.filter(eballot_num_id = eballot_num_data.id).update(alert = 1)
        if eballot_data.sh_classification == 'false':
            stockholdervote.filter(eballot_num = eballot_num_data.eballot_num, election_code = eballot_data.election_code).delete()  

        return redirect('eballot_form', id=eballot_data.eballot_num_id)
    else:
        eballot.filter(eballot_num_id = eballot_num_data.id).update(alert = 0)
        return render(request, 'eballot_form/content/thank_you.html')

@login_required(login_url="/")
def end_election(request, id):

    election = Election.objects.all()
    election = election.filter(code = id).update(status = 'completed')

    eballot = EBallot.objects.all()
    eballot = eballot.filter(election_code = id).update(election_status = 1)

    return redirect('result')

def select_election_report(request):
    #Select all election create
    election_code_list = Election.objects.all()
    election_code_list = election_code_list.filter(status = 'pending')
   
    #Fetch all stakeholders present as voters
    voters_list = Attendance.objects.all()
    voters_list = voters_list.filter(election_status = 0, at_status = 'present')

    form = SelectElection()

    return render(request, 'admin/content/admin_select_election_report.html', {'form' : form, 'election_code_list' : election_code_list, 'voters_list' : voters_list})