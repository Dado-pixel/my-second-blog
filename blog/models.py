from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blog.utils import sendTransaction
import hashlib

class Post(models.Model):
     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     title = models.CharField(max_length=200)
     text = models.TextField()
     created_date = models.DateTimeField(default=timezone.now)
     published_date = models.DateTimeField(blank=True, null=True)
     hash = models.CharField(max_length=32, default=0, null=True)
     txId = models.CharField(max_length=66, default=0, null=True)

     def writeOnChain(self):
         self.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
         self.txId = sendTransaction(self.hash)
         self.save()

     def publish(self):
         self.published_date = timezone.now()
         self.save()

     def __str__(self):
         return self.title

class IP(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entr_date = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=False, default=0)

    def __str__(self):
        return self.ip_address
