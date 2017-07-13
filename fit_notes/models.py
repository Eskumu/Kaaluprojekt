from django.db import models
from kaaluleht.models import Kaal
from datetime import date

class event(models.Model):

    user = models.ForeignKey(Kaal, on_delete=models.CASCADE)
    event_date = models.DateField(default=date.today)
    activity = models.CharField(max_length=100)
    avg_pulse = models.DecimalField("Average Pulse", decimal_places=0, max_digits=3)
    duration = models.DurationField("Duration of exercise")
    comment = models.TextField("Comment", blank=True, default='')

    def __str__(self):
        return "{} {} |{}".format(self.eventID.user.username, self.event_date, self.id)