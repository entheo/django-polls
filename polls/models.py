from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
    pub_date = models.DateTimeField('date published')
    question_text = models.TextField(max_length=200)

    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean=True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    vote_num = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
