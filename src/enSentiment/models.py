from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Results(models.Model):
    userID         = models.ForeignKey(User , on_delete=models.CASCADE)
    resutlDate     = models.DateTimeField(auto_now_add=True)
    Keyword        = models.TextField()
    NumberOftweets = models.TextField()
    FromDate       = models.TextField()
    ToDate         = models.TextField()

class Tweets(models.Model):
    tweetlID        = models.BigIntegerField()
    result          = models.ForeignKey(Results , on_delete=models.CASCADE) #Have assign any tweet to unique result id 
    tweetUsername   = models.CharField(max_length=100)
    tweetNickname   = models.TextField()                                  #the name appare near photo and it's not unique
    tweetText       = models.TextField()
    tweetDate       = models.DateTimeField()
    tweetLikes      = models.IntegerField()
    tweetRetweets   = models.IntegerField()
    tweetReplies    = models.IntegerField()
    tweetLocation   = models.TextField()
    tweetLink       = models.TextField()
    tweetLabel      = models.IntegerField(default=5)

    

    
