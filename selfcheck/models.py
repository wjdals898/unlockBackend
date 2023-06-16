from django.db import models
from accounts.models import Counselee


class SelfCheck(models.Model):
    id = models.AutoField(primary_key=True)
    counselee_id = models.ForeignKey(Counselee, on_delete=models.CASCADE,  db_column="counselee_id", related_name="selfcheck")
    date = models.DateTimeField(auto_now_add=True)

    PUBLIC_CHOICES = [
        ('y', 'Yes'),
        ('n', 'No'),
    ]
    public_yn = models.CharField(max_length=1, choices=PUBLIC_CHOICES, default='n')
    video_url = models.URLField(null=True)
    analysis_url = models.URLField(null=True)

    def __str__(self):
        return f"({self.id}) {self.counselee_id.userkey.name}"
