from django.db import models

class rating(models.Model):
	pic_id=models.CharField(max_length=30)
	rating=models.IntegerField(max_length=7)
	def __unicode__(self):
		return self.pic_id
		
		
class record(models.Model):
	target=models.ForeignKey(rating, null=True)
	time=models.IntegerField(max_length=20)
	def __unicode__(self):
		return self.target.pic_id
	
	
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
	token= models.CharField(max_length=60, null=True)
	last_lat = models.FloatField(null=True)
	last_lon = models.FloatField(null=True)
	gender = models.CharField(max_length=6, null=True)
	def __unicode__(self):
		return self.fsq_id

class user_lookup(models.Model):
	first_name=models.CharField(max_length=20)
	t_handle=models.CharField(max_length=30, null=True)
	facebook = models.CharField(max_length=15, null=True)
	fsq_id=models.CharField(max_length=30)
	pic_id=models.CharField(max_length=30, primary_key=True)	
	unsubscribed=models.BooleanField(default=False)
	blocks=models.ManyToManyField(user, null=True)
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

class game(models.Model):
	gid=models.IntegerField(max_length=3, primary_key=True)
	name=models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class twitter_outreach(models.Model):
	m_target=models.ForeignKey(user_lookup, unique=False)
	sender=models.ForeignKey(user, unique=False)
	uid=models.CharField(max_length=5, primary_key=True)
	message=models.CharField(max_length=140)
	game=models.ForeignKey(game, unique=False)
	venue_id=models.CharField(max_length=30)
	other_venue_id=models.CharField(max_length=30, null=True)
	read=models.BooleanField()
	def __unicode__(self):
		return self.uid

class queue(models.Model):
        fsq_id=models.CharField(max_length=30)
        date_joined=models.DateTimeField()
        first_name=models.CharField(max_length=20)
	last_name=models.CharField(max_length=30, null=True)
	email = models.EmailField(max_length=75, null=True)
        allocated_invite=models.ForeignKey(invite_codes)
	lat = models.FloatField()
        lon = models.FloatField()
	token = models.CharField(max_length=60, null=True)
	has_shared = models.BooleanField()
	def __unicode__(self):
                return self.fsq_id
