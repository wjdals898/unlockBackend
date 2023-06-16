from django.db import models


class Counselee(models.Model):
    token = models.CharField(unique=True, max_length=100)
    user = models.OneToOneField('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Counselee'


class Counselingtype(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'CounselingType'


class Counselor(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING)
    token = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'Counselor'


class Prescription(models.Model):
    result = models.ForeignKey('Result', models.DO_NOTHING)
    content = models.TextField()
    reg_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    mod_date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return f"{self.content} \n--- ({self.reg_date} -> 수정일 {self.mod_date})"
    
    class Meta:
        managed = False
        db_table = 'Prescription'


class Reservation(models.Model):
    id = models.IntegerField(primary_key=True)
    counselor = models.ForeignKey(Counselor, models.DO_NOTHING, db_column='Counselor_id')  # Field name made lowercase.
    counselee = models.ForeignKey(Counselee, models.DO_NOTHING, db_column='Counselee_id')  # Field name made lowercase.
    date = models.DateTimeField()
    type = models.ForeignKey(Counselingtype, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Reservation'


class Result(models.Model):
    counselor = models.ForeignKey(Counselor, models.DO_NOTHING, db_column='Counselor_id')  # Field name made lowercase.
    counselee = models.ForeignKey(Counselee, models.DO_NOTHING, db_column='Counselee_id')  # Field name made lowercase.
    date = models.DateTimeField()
    video_url = models.CharField(unique=True, max_length=100)
    analysis_url = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'Result'



class Selfcheck(models.Model):
    counselee = models.ForeignKey(Counselee, models.DO_NOTHING)
    date = models.DateTimeField()
    public_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'Selfcheck'


class User(models.Model):
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=1)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'User'