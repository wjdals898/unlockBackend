from django.db import models
from accounts.models import *


class Result(models.Model):
    counselor = models.ForeignKey(Counselor, models.CASCADE, db_column='Counselor_id', related_name="result_id")  # Field name made lowercase.
    counselee = models.ForeignKey(Counselee, models.CASCADE, db_column='Counselee_id', related_name="result_id")  # Field name made lowercase.
    date = models.DateField(auto_now_add=True)
    analysis_url = models.URLField(unique=True, max_length=100, null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    #result_csv = models.FileField(upload_to='csv_files/', null=True, blank=True)


class Prescription(models.Model):
    result = models.ForeignKey(Result, models.CASCADE, related_name="prescription_id", db_column='result')
    content = models.TextField()
    reg_date = models.DateField(blank=True, null=True, auto_now_add=True)
    mod_date = models.DateField(blank=True, null=True, auto_now=True)


class CSVFile(models.Model):
    emotion1 = models.FloatField()
    emotion2 = models.FloatField()
    emotion3 = models.FloatField()
    emotion4 = models.FloatField()
    emotion5 = models.FloatField()
    emotion6 = models.FloatField()
    emotion7 = models.FloatField()

