from django.db import models

class rating(models.Model):
	pic_id=models.CharField(max_length=30)
	rating=models.IntegerField(max_length=7)
	total_sets=models.IntegerField(max_length=7)
	
	def __unicode__(self):
		return self.pic_id
		
class record(models.Model):
	target=models.ForeignKey(rating)
	time=models.IntegerField(max_length=20)
	venue_id=models.CharField(max_length=30)
	
class user(models.Model):
	fsq_id=models.CharField(max_length=30)
	date_joined=models.DateTimeField()
	first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=30)
	ratings = models.ForeignKey(record, null=True)
	phone = models.CharField(max_length=15)
	twitter = models.CharField(max_length=30)
	facebook = models.CharField(max_length=15)
	email = models.EmailField(max_length=75)
	photo = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.fsq_id
		