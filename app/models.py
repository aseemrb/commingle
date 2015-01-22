from django.db import models

# Create your models here.
class Feeds(models.Model):
	user = models.CharField(max_length=50)
	verb = models.CharField(max_length=200)
	event = models.CharField(max_length=50)
	place = models.CharField(max_length=50)
	link = models.CharField(max_length=200)
	time = models.BigIntegerField()
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)

class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	college = models.CharField(max_length=150)
	bio = models.CharField(max_length=500)
	favs = models.BinaryField()
	# attended events
	# interest filters

class Comments(models.Model):
	username = models.CharField(max_length=50)
