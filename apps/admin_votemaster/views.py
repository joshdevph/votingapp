from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.admin_votemaster.models import Election, Attendance, Nominee
from apps.admin_votemaster.forms import ElectionForm
from django.contrib.auth.models import User
from apps.admin_newstockholder.models import StockHolder

# Create your views here.

@login_required(login_url="")
def admin_votemaster(request):
    context = {'form': ElectionForm,
               'message': {'message': ''}
               }

    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid(): #check if form is valid
            code = form['code'].value()
            desc = form['description'].value()

            election_norepeat = Election.objects.filter(code=code) #Check if the election code is already used

            if election_norepeat:
                return render(request, 'admin/content/admin_votemaster.html', {'form': ElectionForm, 'message': {'message': 'repeat'}})
            else:
                election = Election.objects.create(code=code, description=desc)
                return render(request, 'admin/content/admin_votemaster.html',  {'form': ElectionForm, 'message': {'message': 'success'}})
    else:
        form = ElectionForm()

    return render(request, 'admin/content/admin_votemaster.html', context)


@login_required(login_url="")
def admin_votemaster_attendance(request):
    stock_holder = StockHolder.objects.all()
    latest_election = Election.objects.latest('date_added') #get latest election, meaning last created election or this day's election
    current_attendance = Attendance.objects.filter(election_code=latest_election.code) #get current elections attendance record

    context = {
        'form': ElectionForm,
        'stock_holder': stock_holder,
        'attendance': current_attendance,
        'count':  {
            'stock_holder_count': stock_holder.count(),
            'attendance_count': current_attendance.count()
        }
    }

    if request.method == "POST":
        if request.POST.get("save"): # check if save button is clicked
            for item in stock_holder: # loop all the stakeholders
                if not request.POST.get('stock_holder' + str(item.id), None) == None:  #check if the checkbox in its corresponding stakehokder id is checked
                    if Attendance.objects.filter(sh_id=item.id, election_code=latest_election.code):  #if this stakeholder has an attendance record for the current election, his/her status will just be updated as 'present'
                        Attendance.objects.filter(sh_id=item.id).update(at_status='present')
                    else:
                        attendance_record = Attendance(
                            sh_id=item.id,
                            election_code=latest_election.code,
                            sh_fullname=item.sh_fname + " " + item.sh_lname,
                            at_status="present"
                        )

                        attendance_record.save()

                else: # codes in this section applies when the checkbox is unchecked
                    if Attendance.objects.filter(sh_id=item.id, election_code=latest_election.code):  # if this stakeholder has an attendance record for the current election, his/her status will just be updated as 'absent'
                        Attendance.objects.filter(sh_id=item.id).update(at_status='absent')

                    else:  # will add new attendance record for this specific stakeholder with the status 'absent'
                        attendance_record = Attendance(
                            sh_id=item.id,
                            election_code=latest_election.code,
                            sh_fullname=item.sh_fname + " " + item.sh_lname,
                            at_status="absent"
                        )
                        attendance_record.save()
        else:
            print("invalid")

        context = {
            'form': ElectionForm,
            'stock_holder': stock_holder,
            'attendance': current_attendance,
            'count': {
                'stock_holder_count': stock_holder.count(),
                'attendance_count': current_attendance.count()
            }
        }# new database content

        return render(request, 'admin/content/admin_votemaster_attendance.html', context)
    return render(request, 'admin/content/admin_votemaster_attendance.html', context)

@login_required(login_url="")
def admin_votemaster_nomination(request):
    stock_holder = StockHolder.objects.all()
    latest_election = Election.objects.latest('date_added') #get latest election, meaning last created election or this day's election
    current_attendance = Attendance.objects.filter(election_code=latest_election.code) #get current elections attendance record
    nominees = Nominee.objects.all()

    context = {
        'form': ElectionForm,
        'stock_holder': stock_holder,
        'attendance': current_attendance,
        'nominees': nominees,
        'count':  {
            'stock_holder_count': stock_holder.count(),
            'attendance_count': current_attendance.count(),
            'nominees_count': nominees.count()
        }
    }

    return render(request, 'admin/content/admin_votemaster_nomination.html', context)

def admin_votemaster_add_nominee(request, id):
    stock_holder = StockHolder.objects.all()
    latest_election = Election.objects.latest('date_added') #get latest election, meaning last created election or this day's election
    current_attendance = Attendance.objects.filter(election_code=latest_election.code) #get current elections attendance record
    selected_stockholder = StockHolder.objects.get(id=int(id))
    nominees = Nominee.objects.all()

    if not Nominee.objects.filter(sh_id=id):
        new_nominee = Nominee(
            sh_id=id,
            election_code=latest_election.code,
            sh_fullname=selected_stockholder.sh_fname + " " + selected_stockholder.sh_lname,
        )
        new_nominee.save()

    context = {
        'form': ElectionForm,
        'stock_holder': stock_holder,
        'attendance': current_attendance,
        'nominees': nominees,
        'count':  {
            'stock_holder_count': stock_holder.count(),
            'attendance_count': current_attendance.count(),
            'nominees_count': nominees.count()
        }
    }

    return redirect('admin_votemaster_nomination')

def admin_votemaster_remove_nominee(request, id):
    Nominee.objects.filter(id=id).delete()
    return redirect('admin_votemaster_nomination')