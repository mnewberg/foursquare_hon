from django.db import models

class avail_DIDs(models.Model):
    DID=models.CharField(max_length=10)
    def __str__(self):
        return self.DID

class routing(models.Model):
    sender=models.CharField(max_length=10)
    recipient=models.CharField(max_length=10)
    DID=models.ForeignKey(avail_DIDs)
    time_created=models.IntegerField(max_length=20)

    def __str__(self):
        return self.recipient


class log(models.Model):
    time=models.DateTimeField()
    sender=models.CharField(max_length=10)
    recipient=models.CharField(max_length=10)
    from_did=models.CharField(max_length=10)
    to_did=models.CharField(max_length=10)
    message=models.CharField(max_length=400)
    def __str__(self):
        return self.time





# Create your models here.
