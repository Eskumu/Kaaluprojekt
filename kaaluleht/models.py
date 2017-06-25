from django.db import models
from django.conf import settings
from datetime import date
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Kaal(models.Model):
    nimi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nimi.username

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk,'slug':slugify(self.nimi)})

    @property
    def alg_kaal(self):
        user_list = Kaal_uuendus.objects.filter(KaalID=self.pk)
        try:
            esimene = user_list.earliest("change_date").kaal
            return esimene
        except:
            return None

    @property
    def viimane_kaal(self):
        user_list = Kaal_uuendus.objects.filter(KaalID= self.pk)
        try:
            viimane = user_list.latest('change_date').kaal
            return viimane
        except:
            return self.alg_kaal

    @property
    def protsent(self):
        try:
            return round((1-self.alg_kaal/self.viimane_kaal)*100,2)
        except TypeError:
            return None
class Kaal_uuendus(models.Model):

    KaalID = models.ForeignKey(Kaal, on_delete=models.CASCADE)
    change_date = models.DateField(default=date.today)
    kaal = models.DecimalField("Uus Kaal",decimal_places=1 ,max_digits=4)

    def __str__(self):
        return "{} {}".format(self.KaalID.nimi.username,self.change_date)