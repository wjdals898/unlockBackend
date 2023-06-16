from django.db import models

STATUS_CHOICES = [
        ('대인관계', '대인관계'),
        ('외로움', '외로움'),
        ('부정적 사고방식', '부정적 사고방식'),
        ('자존감 하락', '자존감 하락'),
        ('불면증', '불면증'),
        ('알코올 의존증', '알코올 의존증'),
        ('기타', '기타') 
    ]
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
class User(models.Model):
    id = models.IntegerField(primary_key=True)

class Counselor(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

class Counselee(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class Reservation(models.Model):
    Counselor_id = models.ForeignKey(Counselor, on_delete=models.CASCADE, to_field = 'user_id')
    Counselee_id = models.ForeignKey(Counselee, on_delete=models.CASCADE, to_field = 'user_id')
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    type = models.CharField(max_length=10, choices=STATUS_CHOICES)

# Create your models here.
