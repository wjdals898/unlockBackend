from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Counselor)
admin.site.register(Counselee)
admin.site.register(CounselingType)
