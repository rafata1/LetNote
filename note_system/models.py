from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    created_at = models.DateField(auto_now = True)
    def __str__(self):
        return self.email
        

class NoteItem(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100, blank=False, null=True)
    content = models.CharField(max_length=10000, blank=False, null=True)
    created_at = datetime.now()
    
    def get_shorten_subject(self):
        if len(self.subject) > 30:
            return self.subject[0:29]+'...'
        return self.subject    

    def get_shorten_content(self):
        if len(self.content) > 80:
            return self.content[0:79]+'...'
        return self.content

    def get_created_time(self):
        return self.created_at.strftime('%d-%m-%Y %H:%M')


            

