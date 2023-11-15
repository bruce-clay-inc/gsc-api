from django.db import models

class Search_Console(models.Model):
    date = models.DateField()
    clicks = models.IntegerField()
    impressions = models.IntegerField()
    site = models.URLField()
    ctr = models.FloatField()
    position = models.IntegerField()
    query = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} | {self.query} | {self.clicks} | {self.impressions} | {self.ctr} | {self.position}"
