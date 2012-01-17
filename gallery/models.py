from django.db import models

class rating(models.Model):
	pic_id=models.CharField(max_length=30)
	rating=models.IntegerField(max_length=7)
	total_sets=models.IntegerField(max_length=7)
	def __unicode__(self):
		return self.pic_id
	
class user(models.Model):
	fsq_id=models.CharField(max_length=30)
	ratings = models.ManyToManyField(rating)
	phone = models.CharField(max_length=15)
	twitter = models.CharField(max_length=30)
	facebook = models.CharField(max_length=15)
	email = models.EmailField(max_length=75)
	photo = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.fsq_id
		
class target_id(models.Model):
	fsq_id=models.CharField(max_length=30)
	pic_id=models.OneToOne(rating)
	def __unicode__(self):
		return self.fsq_id

