from django.db import models

class rating(models.Model):
	pic_id=models.CharField(max_length=30)
	rating=models.IntegerField(max_length=7)
	def __unicode__(self):
		return self.pic_id
	
class user(models.Model):
	fsq_id=models.CharField(max_length=30)
	ratings = models.ManyToManyField(rating)
	contact= models.CharField(max_length=100)
	photo = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.fsq_id
	
