from django.db import models
from apps.admin_votemaster.models import Election, Attendance, Nominee

# Create your models here.
class EBallotBatch(models.Model):
    eballot_batch_id = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.eballot_batch_id

class EBallotNum(models.Model):
    eballot_num = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.eballot_num

class EBallot(models.Model):
    election_code = models.CharField(max_length=250, null=False)
    eballot_batch_id = models.ForeignKey(EBallotBatch, on_delete=models.CASCADE, null=False)
    eballot_num = models.ForeignKey(EBallotNum, on_delete=models.CASCADE, null=False)
    sh_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=False)
    sh_fullname= models.CharField(max_length=250, null=False)

class StockholderVote(models.Model):
    sh_id = models.CharField(max_length=250, null=False)
    sh_fullname= models.CharField(max_length=250, null=False)
    vote_pts = models.IntegerField(default=0, null=False)