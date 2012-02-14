from django.db import models

class rating(models.Model):
	pic_id=models.CharField(max_length=30)
	rating=models.IntegerField(max_length=7)
	total_sets=models.IntegerField(max_length=7)
	
	def __unicode__(self):
		return self.pic_id
		
class record(models.Model):
	target=models.ForeignKey(rating, null=True)
	time=models.IntegerField(max_length=20)
	venue_id=models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.venue_id
	
	
class user(models.Model):
	fsq_id=models.CharField(max_length=30)
	date_joined=models.DateTimeField()
	first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=30, null=True)
	records = models.ManyToManyField(record, null=True)
	phone = models.CharField(max_length=15, null=True)
	twitter = models.CharField(max_length=30, null=True)
	facebook = models.CharField(max_length=15, null=True)
	email = models.EmailField(max_length=75, null=True)
	photo = models.CharField(max_length=30, null=True)
	has_shared = models.BooleanField()
	invite = models.BooleanField()
	def __unicode__(self):
		return self.fsq_id

class user_lookup(models.Model):
	fsq_id=models.CharField(max_length=30)
	pic_id=models.CharField(max_length=30, primary_key=True)
	def __unicode__(self):
		return self.fsq_id
		
class invite_codes(models.Model):
	code=models.CharField(max_length=12)
	quota=models.IntegerField(max_length=3)
	def __unicode__(self):
		return self.code
	
class venue_ll(models.Model):
	venue_id=models.CharField(max_length=30, primary_key=True)
	lat=models.FloatField()
        lon=models.FloatField()
	def __unicode__(self):
                return self.venue_id

