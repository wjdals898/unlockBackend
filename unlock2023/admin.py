from django.contrib import admin

# Register your models here.
from unlock2023.models import Reservation, CounselingType

admin.site.register(Reservation)
admin.site.register(CounselingType)