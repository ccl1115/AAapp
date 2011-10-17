from django.db import models
from django.contrib.auth.models import User

class AccountInfo(models.Model):
    user = models.OneToOneField(User)
    balence = models.FloatField()

class Expense(models.Model):
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User)
    participants = models.ManyToManyField(User, related_name="participant_set")
    pub_datetime = models.DateTimeField(auto_now_add=True)
    money = models.FloatField()

    def each(self):
        return self.money / len(self.participants.all())

class Approve(models.Model):
    expense = models.OneToOneField(Expense)
    pros = models.ManyToManyField(User, related_name="pro_set")
    cons = models.ManyToManyField(User, related_name="con_set")
    STATUS_CHOICES = (
            ('I', 'Initial'),
            ('A', 'Approving'),
            ('P', 'Pro'),
            ('C', 'Con'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def isInPros(self, user):
        return user in self.pros.all()

    def isInCons(self, user):
        return user in self.cons.all()

    def isInParticipants(self, user):
        return user in self.expense.participants.all()

    def isApproved(self, user):
        return self.isInParticipants(user) and not self.isInCons(user) and not self.isInPros(user)
    
    def doPro(self, user):
        if self.isApproved(user):
            self.pros.add(user)
            self.save()
            return True
        else:
            return False

    def doCon(self, user):
        if self.isApproved(user):
            self.cons.add(user)
            self.save()
            return True
        else:
            return False

    def updateStatus(self):
        if self.unapproved.count() > 0:
            self.status = 'C'
        if self.approved.count() == 0:
            self.status = 'I'
        if self.expense.participants.count() > self.approved.count():
            self.status = 'A'
        if self.expense.participants.count() == self.approved.count():
            self.status = 'P'
        self.save()
