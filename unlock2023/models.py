
from django.db import models
from accounts.models import *

TIME_CHOICES = [
        ('09:00', '1'),
        ('10:00', '2'),
        ('11:00', '3'),
        ('12:00', '4'),
        ('13:00', '5'),
        ('14:00', '6'),
        ('15:00', '7'),
        ('16:00', '8'),
        ('17:00', '9'),
        ('18:00', '10')
    ]



class Reservation(models.Model):
    counselor_id = models.ForeignKey(Counselor, on_delete=models.CASCADE, db_column='counselor_id')
    counselee_id = models.ForeignKey(Counselee, on_delete=models.CASCADE, db_column='counselee_id')
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    type = models.ForeignKey(CounselingType, on_delete=models.CASCADE, db_column='type')
